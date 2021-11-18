/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include "node/state.hpp"
#include <node/stop_gap.hpp>
#include <cstdio>
#include <uavcan/node/GetInfo_1_0.h>
#include <board/unique_id.h>
#include <node/units.hpp>
#include <node/interfaces/IHandler.hpp>

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

UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_node_GetInfo, 1, 0);
namespace node::essential
{
struct : IHandler
{
    void operator()(node::state::State &state, CanardTransfer *transfer)
    {
        uavcan_l6::DSDL<uavcan_node_GetInfo_Response_1_0>::Serializer serializer{};
        auto res = serializer.serialize(process_request_node_get_info());
        if (res.has_value())
        {
            CanardTransfer rt = *transfer;  // Response transfers are similar to their requests.
            if (transfer->timestamp_usec > 0)
            {
                rt.timestamp_usec = transfer->timestamp_usec + ONE_SECOND_DEADLINE_usec;
            }
            rt.transfer_kind = CanardTransferKindResponse;
            rt.payload_size = res.value();
            rt.payload = serializer.getBuffer();
            (void) canardTxPush(const_cast<CanardInstance *>(&state.canard), &rt);
        } else
        {
            assert(false);
        }
        return;
    }
} uavcan_node_GetInfo_1_0_handler;
}

