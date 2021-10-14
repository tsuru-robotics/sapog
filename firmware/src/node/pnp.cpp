/*
 * Copyright (c) 2021 Zubax, zubax.com
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

static CanardRxSubscription AllocationMessageSubscription;

void node::config::plug_and_play_loop(State &state)
{
    bool already_tried_saving = false;
    save_crc(state);
    while (state.canard.node_id == 0 || state.canard.node_id > 128)
    {
        state.timing.current_time = get_monotonic_microseconds();
        switch (state.plug_and_play.status)
        {
            case node::state::PNPStatus::Subscribing:
                node::config::subscribe_to_plug_and_play_response(state);
                state.plug_and_play.status = node::state::PNPStatus::TryingToSend;
                break;
            case node::state::PNPStatus::TryingToSend:
                if (node::config::send_plug_and_play_request(state))
                {
                    state.plug_and_play.status = node::state::PNPStatus::SentRequest;
                } else {
                    if(already_tried_saving){
                        goto out_of_loop;
                    }
                    already_tried_saving = true;
                }
                break;
            case node::state::PNPStatus::SentRequest:
                // The following should write the received NodeID into the state object
                if (node::config::receive_plug_and_play_response(state))
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
                break;
            case node::state::PNPStatus::ReceivedResponse:
                if (node::config::save_node_id(state))
                {
                    state.plug_and_play.status = node::state::PNPStatus::Done;
                    printf("NodeID was successfully saved to the configuration.");
                } else {
                    assert(false);
                }
                break;
            case node::state::PNPStatus::Done:
                state.plug_and_play.anonymous = false;
                break;
        }
        chThdSleep(1);
    }
    out_of_loop:;
}
void node::config::save_crc(State &state)
{
    auto unique_id = board::read_unique_id();
    auto crc_object = CRC64{};
    crc_object.update(unique_id.data(), sizeof(unique_id));
    state.plug_and_play.unique_id_hash = crc_object.get();
}
bool node::config::send_plug_and_play_request(State &state)
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
        const CanardTransfer transfer = {
                .timestamp_usec = get_monotonic_microseconds() + SECOND_IN_MICROSECONDS,
                .priority       = CanardPrioritySlow,
                .transfer_kind  = CanardTransferKindMessage,
                .port_id        = uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_,
                .remote_node_id = CANARD_NODE_ID_UNSET,
                .transfer_id    = (CanardTransferID) (state.transfer_ids.uavcan_pnp_allocation++),
                .payload_size   = serialized_size,
                .payload        = &serialized[0],
        };
        (void) canardTxPush(&state.canard, &transfer);  // The response will arrive asynchronously eventually.
        transmit(state);
        return true;
    }
    return false;
}

bool node::config::subscribe_to_plug_and_play_response(State &state)
{
    const int8_t res = canardRxSubscribe(&state.canard,
                                         CanardTransferKindMessage,
                                         uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_,
                                         uavcan_pnp_NodeIDAllocationData_1_0_EXTENT_BYTES_,
                                         CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, &AllocationMessageSubscription);
    return res;
}

bool node::config::receive_plug_and_play_response(State &state)
{
    std::optional<CanardTransfer> transfer = receive_transfer(state, 0);
    if (transfer.has_value())
    {
        //printf("Received transfer for port_id %d\n", transfer.value().port_id);
        if (transfer.value().port_id == uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_)
        {
            uavcan_pnp_NodeIDAllocationData_1_0 msg{};
            auto result = uavcan_pnp_NodeIDAllocationData_1_0_deserialize_(&msg,
                                                                           static_cast<const uint8_t*>(transfer->payload),
                                                                           &(transfer->payload_size));
            //printf("The size of allocated_node_id arra is %d\n", msg.allocated_node_id.count);
            if (result < 0)
            {
                printf("Failed to deserialize PNP data\n");
                return false;
            }
            printf("Received ID: %d\n", msg.allocated_node_id.elements[0].value);
            if (msg.unique_id_hash == (state.plug_and_play.unique_id_hash & ((1ULL << 48U) - 1U)))
            {
                printf("Hashes are matching\n");
                if (msg.allocated_node_id.count > 0 && msg.allocated_node_id.elements[0].value > 0)
                {
                    state.canard.node_id =  msg.allocated_node_id.elements[0].value;
                    return true;
                }
            }

        }
    }
    return false;
}

bool node::config::save_node_id(State &state)
{
    uavcan_register_Value_1_0 data2{};
    uavcan_primitive_array_Integer64_1_0 data{};
    data.value.elements[0] = state.canard.node_id;
    data.value.count = 1;
    data2.integer64 = data;
    uavcan_register_Value_1_0_select_integer64_(&data2);
    return ::config::registers::getInstance().registerWrite("uavcan_node_id", &data2);
}
