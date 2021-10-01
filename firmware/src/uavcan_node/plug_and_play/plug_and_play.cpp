#include "libcanard/canard.h"
#include "uavcan_node/units.hpp"
#include "uavcan_node/time.h"
#include <board/unique_id.h>
#include "hashing/hash.hpp"
#include "uavcan/pnp/NodeIDAllocationData_1_0.h"
#include "plug_and_play.hpp"
#include "uavcan_node/reception.hpp"
#include "src/settings/registers.hpp"

static CanardRxSubscription AllocationMessageSubscription;

void node::config::plug_and_play_loop(State &state)
{
    while (state.plug_and_play.anonymous)
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
                    state.plug_and_play.status = node::state::PNPStatus::TryingToSend;
                    state.plug_and_play.request_count += 1;
                    continue;
                }
                break;
            case node::state::PNPStatus::ReceivedResponse:
                if (node::config::save_node_id(state))
                {
                    state.plug_and_play.status = node::state::PNPStatus::Done;
                }
                break;
            case node::state::PNPStatus::Done:
                state.canard.node_id = state.plug_and_play.node_id;
                state.plug_and_play.anonymous = false;
                break;
        }
        chThdSleep(1);
    }
}

bool node::config::send_plug_and_play_request(State &state)
{
    // Note that a high-integrity/safety-certified application is unlikely to be able to rely on this feature.
    uavcan_pnp_NodeIDAllocationData_1_0 msg{};
    auto unique_id = board::read_unique_id();
    auto crc_object = CRC64{};
    crc_object.update(unique_id.data(), sizeof(unique_id));
    msg.unique_id_hash = crc_object.get();
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
    if (transfer->port_id == uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_)
    {
        uavcan_pnp_NodeIDAllocationData_1_0 msg{};
        auto result = uavcan_pnp_NodeIDAllocationData_1_0_deserialize_(&msg,
                                                                       reinterpret_cast<uint8_t *>(&(transfer->payload)),
                                                                       &(transfer->payload_size));
        if (result >= 0)
        {
            state.plug_and_play.node_id = msg.allocated_node_id.elements[0].value;
            return true;
        }
    }
    return false;
}

bool node::config::save_node_id(State &state)
{
    uavcan_register_Value_1_0 data2{};
    uavcan_primitive_array_Integer64_1_0 data{};
    data.value.elements[0] = state.plug_and_play.node_id;
    data.value.count = 1;
    data2.integer64 = data;
    uavcan_register_Value_1_0_select_integer64_(&data2);
    return ::config::registers::getInstance().registerWrite("uavcan.node.id", &data2);
}
