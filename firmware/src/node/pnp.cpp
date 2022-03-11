/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "libcanard/canard.h"
#include "node/units.hpp"
#include "node/time.h"
#include <board/unique_id.h>
#include "hashing/hash.hpp"
#include "uavcan/pnp/NodeIDAllocationData_1_0.h"
#include "pnp.hpp"
#include "node/reception.hpp"
#include "src/settings/registers.hpp"
#include "transmit.hpp"
#include <stdlib.h>
#include "board/board.hpp"

static CanardRxSubscription AllocationMessageSubscription;
static board::LEDOverlay led_ctl;

static bool send_plug_and_play_request(State &state);

static bool receive_plug_and_play_response(State &state);

static bool subscribe_to_plug_and_play_response(State &state);

static void save_crc(State &state);

static bool unsubscribe_plug_and_play_response(State &state);

static bool save_node_id(State &state);

// Keywords: automatic node id allocation
namespace node::pnp
{
void plug_and_play_loop(State &state)
{
    bool already_tried_saving = false;
    save_crc(state);
    if (state.canard.node_id == CANARD_NODE_ID_UNSET)
    {
        printf("started pnp\n");
    }
    bool do_save = true; // for testing purposes, it is better to have the device allocate every time
    bool needs_pnp = state.canard.node_id == CANARD_NODE_ID_UNSET;
    while (needs_pnp)
    {
        state.timing.current_time = get_monotonic_microseconds();
        // With every success, the state moves to the next element further down in the switch block
        switch (state.plug_and_play.status)
        {
            case node::state::PNPStatus::Subscribing:
                subscribe_to_plug_and_play_response(state);
                state.plug_and_play.status = node::state::PNPStatus::TryingToSend;
                continue;
            case node::state::PNPStatus::TryingToSend:
                if (send_plug_and_play_request(state))
                {
                    state.plug_and_play.status = node::state::PNPStatus::SentRequest;
                    led_ctl.set_hex_rgb(0x003110);
                } else
                {
                    if (already_tried_saving)
                    {
                        goto out_of_loop;
                    }
                    already_tried_saving = true;
                }
                continue;
            case node::state::PNPStatus::SentRequest:
                // The following should write the received NodeID into the state object
                if (receive_plug_and_play_response(state))
                {
                    state.plug_and_play.status = node::state::PNPStatus::ReceivedResponse;
                }
                if (state.timing.current_time >= state.timing.next_pnp_request)
                {
                    srand(state.timing.current_time);
                    state.plug_and_play.status = node::state::PNPStatus::TryingToSend;
                    state.timing.next_pnp_request += SECOND_IN_MICROSECONDS / 2 + rand() % SECOND_IN_MICROSECONDS;
                    state.plug_and_play.request_count += 1;
                    continue;
                }
                continue;
            case node::state::PNPStatus::ReceivedResponse:
                printf("finished pnp.\n");
                if (!do_save)
                {
                    state.plug_and_play.status = node::state::PNPStatus::Done;
                    continue;
                }
                if (save_node_id(state))
                {
                    state.plug_and_play.status = node::state::PNPStatus::Done;
                    printf("NodeID was successfully saved to the configuration.\n");
                } else
                {
                    printf("Failed to save the node_id.\n");
                }
                state.plug_and_play.status = node::state::PNPStatus::Done;
                continue;
            case node::state::PNPStatus::Done:
                led_ctl.set(board::LEDColor::DARK_GREEN);
                unsubscribe_plug_and_play_response(state);
                state.plug_and_play.anonymous = false;
                needs_pnp = false;
                break;
        }
        chThdSleepMicroseconds(30);
    }
out_of_loop:;
}
}

static void save_crc(State &state)
{
    auto unique_id = board::read_unique_id();
    auto crc_object = CRC64{};
    crc_object.update(unique_id.data(), sizeof(unique_id));
    state.plug_and_play.unique_id_hash = crc_object.get();
}

static bool send_plug_and_play_request(State &state)
{
    // Note that a high-integrity/safety-certified application is unlikely to be able to rely on this feature.
    uavcan_pnp_NodeIDAllocationData_1_0 msg{};
    msg.unique_id_hash = state.plug_and_play.unique_id_hash;
    uint8_t serialized[uavcan_pnp_NodeIDAllocationData_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
    size_t serialized_size = sizeof(serialized);
    const int8_t err = uavcan_pnp_NodeIDAllocationData_1_0_serialize_(&msg, &serialized[0], &serialized_size);
    assert(err >= 0);
    if (err >= 0)
    {
        CanardTransferMetadata rtm{};  // Response transfers are similar to their requests.
        rtm.transfer_kind = CanardTransferKindMessage;
        rtm.port_id = uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_;
        rtm.transfer_id = (CanardTransferID) (state.transfer_ids.uavcan_pnp_allocation++);
        rtm.remote_node_id = CANARD_NODE_ID_UNSET;
        rtm.priority = CanardPrioritySlow;
        for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
        {
            int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                             const_cast<CanardInstance *>(&state.canard),
                                                             get_monotonic_microseconds() +
                                                             ONE_SECOND_DEADLINE_usec,
                                                             &rtm,
                                                             serialized_size,
                                                             serialized);
            (void) number_of_frames_enqueued;
        }
        transmit(state);
        return true;
    }
    return false;
}

static bool subscribe_to_plug_and_play_response(State &state)
{
    const int8_t res = canardRxSubscribe(&state.canard,
                                         CanardTransferKindMessage,
                                         uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_,
                                         uavcan_pnp_NodeIDAllocationData_1_0_EXTENT_BYTES_,
                                         CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, &AllocationMessageSubscription);
    return res;
}

static bool unsubscribe_plug_and_play_response(State &state)
{

    auto res = canardRxUnsubscribe(&state.canard, CanardTransferKindMessage,
                                   uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_);
    (void) res;
    assert(res == 1);
    return true;
}

static bool receive_plug_and_play_response(State &state)
{
    std::optional<CanardRxTransfer> transfer = receive_transfer(state).first;
    if (transfer.has_value())
    {
        if (transfer.value().metadata.port_id == uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_)
        {
            uavcan_pnp_NodeIDAllocationData_1_0 msg{};
            auto result = uavcan_pnp_NodeIDAllocationData_1_0_deserialize_(&msg,
                                                                           static_cast<const uint8_t *>(transfer->payload),
                                                                           &(transfer->payload_size));
            if (result < 0)
            {
                return false;
            }
            if (msg.unique_id_hash == (state.plug_and_play.unique_id_hash & ((1ULL << 48U) - 1U)))
            {
                if (msg.allocated_node_id.count > 0 && msg.allocated_node_id.elements[0].value > 0)
                {
                    state.canard.node_id = msg.allocated_node_id.elements[0].value;
                    return true;
                }
            }

        }
    }
    return false;
}

static bool save_node_id(State &state)
{
    uavcan_register_Value_1_0 data2{};
    uavcan_primitive_array_Integer64_1_0 data{};
    data.value.elements[0] = state.canard.node_id;
    data.value.count = 1;
    data2.integer64 = data;
    printf("Writing %d to node_id\n", state.canard.node_id);
    uavcan_register_Value_1_0_select_integer64_(&data2);
    return ::config::registers::getInstance().registerWrite("uavcan.node.id", &data2);
}
