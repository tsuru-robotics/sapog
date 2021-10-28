/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <libcanard/canard.h>
#include <cstdio>
#include <uavcan/node/GetInfo_1_0.h>
#include <board/unique_id.h>
#include <node/units.hpp>
#include "get_info.hpp"


static uavcan_node_GetInfo_Response_1_0 process_request_node_get_info()
{
    uavcan_node_GetInfo_Response_1_0 resp{};
    resp.protocol_version.major = CANARD_UAVCAN_SPECIFICATION_VERSION_MAJOR;
    resp.protocol_version.minor = CANARD_UAVCAN_SPECIFICATION_VERSION_MINOR;

    // The hardware version is not populated in this demo because it runs on no specific hardware.
    // An embedded node like a servo would usually determine the version by querying the hardware.

    resp.software_version.major = FW_VERSION_MAJOR;
    resp.software_version.minor = FW_VERSION_MINOR;
    //resp.software_vcs_revision_id = FW_VERSION_MAJOR_MINOR_VCS_HASH;
    // https://github.com/Zubax/sapog/blob/601f4580b71c3c4da65cc52237e62a163d6a6a16/firmware/src/uavcan_node/uavcan_node.cpp#L428
    memcpy(resp.unique_id, board::read_unique_id().data(), sizeof(uint8_t[16]));
    // The node name is the name of the product like a reversed Internet domain name (or like a Java package).
    resp.name.count = strlen(NODE_NAME); // QUESTION: Does this string include a null terminator? It mustn't include it.
    memcpy(&resp.name.elements, NODE_NAME, resp.name.count);

    // The software image CRC and the Certificate of Authenticity are optional so not populated in this demo.
    return resp;
}


namespace node::essential
{
bool uavcan_node_GetInfo_1_0_handler(const node::state::State &state, const CanardTransfer *const transfer)
{
    printf("GetInfo handler responding\n");
    const uavcan_node_GetInfo_Response_1_0 resp = process_request_node_get_info();
    uint8_t serialized[uavcan_node_GetInfo_Response_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_] = {0};
    size_t serialized_size = sizeof(serialized);
    const int8_t res = uavcan_node_GetInfo_Response_1_0_serialize_(&resp, &serialized[0], &serialized_size);
    if (res >= 0)
    {
        CanardTransfer rt = *transfer;  // Response transfers are similar to their requests.
        if (transfer->timestamp_usec > 0)
        {
            rt.timestamp_usec = transfer->timestamp_usec + ONE_SECOND_DEADLINE_usec;
        }
        rt.transfer_kind = CanardTransferKindResponse;
        rt.payload_size = serialized_size;
        rt.payload = &serialized[0];
        (void) canardTxPush(const_cast<CanardInstance *>(&state.canard), &rt);
    } else
    {
        assert(false);
    }
    return true;
}

}

