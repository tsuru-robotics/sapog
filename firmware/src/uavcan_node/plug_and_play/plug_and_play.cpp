#include <unique_id/unique_id.h>
#include "plug_and_play.hpp"
#include "libcanard/canard.h"
#include "uavcan_node/time.h"
#include "uavcan_node/units.hpp"
#include "uavcan/pnp/NodeIDAllocationData_1_0.h"
#include "hashing/hash.hpp"
bool node::config::plug_and_play(State &state)
{
    // Note that a high-integrity/safety-certified application is unlikely to be able to rely on this feature.
    uavcan_pnp_NodeIDAllocationData_1_0 msg{};
    auto unique_id = board::read_unique_id();
    auto crc_object = CRC64{};
    crc_object.update(unique_id.data(), sizeof(unique_id));
    msg.unique_id_hash = crc_object.getBytes();
    uint8_t serialized[uavcan_pnp_NodeIDAllocationData_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
    size_t serialized_size = sizeof(serialized);
    const int8_t err = uavcan_pnp_NodeIDAllocationData_1_0_serialize_(&msg, &serialized[0], &serialized_size);
    assert(err >= 0);
    if (err >= 0)
    {
        const CanardTransfer transfer = {
                .timestamp_usec = getMonotonicMicroseconds() + MEGA,
                .priority       = CanardPrioritySlow,
                .transfer_kind  = CanardTransferKindMessage,
                .port_id        = uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_,
                .remote_node_id = CANARD_NODE_ID_UNSET,
                .transfer_id    = (CanardTransferID)(state.transfer_ids.uavcan_pnp_allocation++),
                .payload_size   = serialized_size,
                .payload        = &serialized[0],
        };
        (void) canardTxPush(state.canard, &transfer);  // The response will arrive asynchronously eventually.
    }
}

