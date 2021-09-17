#ifndef FIRMWARE_LOOPS_H
#define FIRMWARE_LOOPS_H

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include "node_state.h"
#include "publishes.hpp"
#include "reception.h"

using namespace node::state;
namespace node::loops
{
void handle1HzLoop(__attribute__((unused)) State &state)
{
    const bool anonymous = state.canard.node_id > CANARD_NODE_ID_MAX;
    if (!anonymous)
    {
        node::communications::publish_heartbeat(state.canard, state);
    } else
    {
        /*if (rand() > RAND_MAX / 2)  // NOLINT
        {
            uavcan_pnp_NodeIDAllocationData_1_0 msg{};
            msg.allocated_node_id.elements =  // node_id.value = UINT16_MAX;
            uint8_t serialized[uavcan_pnp_NodeIDAllocationData_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_] = {0};
            size_t serialized_size = sizeof(serialized);
            const int8_t err = uavcan_pnp_NodeIDAllocationData_1_0_serialize_(&msg, &serialized[0],
                                                                              &serialized_size);
            assert(err >= 0);
            if (err >= 0)
            {
                const CanardTransfer transfer = {
                        .timestamp_usec = getMonotonicMicroseconds() + MEGA,
                        .priority       = CanardPrioritySlow,
                        .transfer_kind  = CanardTransferKindMessage,
                        .port_id        = uavcan_pnp_NodeIDAllocationData_2_0_FIXED_PORT_ID_,
                        .remote_node_id = CANARD_NODE_ID_UNSET,
                        .transfer_id    = (CanardTransferID) (state.transfer_ids.uavcan_pnp_allocation++),
                        .payload_size   = serialized_size,
                        .payload        = &serialized[0],
                };
                (void) canardTxPush(&state.canard,
                                    &transfer);  // The response will arrive asynchronously eventually.
            }
        }*/
    }
}

void handle01HzLoop(__attribute__((unused)) State &state)
{
}

void handleFastLoop(__attribute__((unused)) State &state)
{
    receiveTransfer(state, 0);
    //receiveTransfer(state, 1);
    transmit(state);
}
}


#endif //FIRMWARE_LOOPS_H
