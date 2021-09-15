#ifndef FIRMWARE_RECEPTION_H
#define FIRMWARE_RECEPTION_H

static const int max_frames_to_process_per_iteration = 1000;
#define NUNAVUT_ASSERT assert

#include <libcanard/canard.h>
#include <uavcan/node/GetInfo_1_0.h>
#include <board/board.hpp>
#include "node_state.h"
#include "units.hpp"
#include <cstddef>
#include "node_time.h"

using namespace node::state;

void processReceivedMessage(const State &state, const CanardTransfer *const transfer)
{
    (void) state;
    (void) transfer;
}

static uavcan_node_GetInfo_Response_1_0 processRequestNodeGetInfo()
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
    resp.name.count = strlen(NODE_NAME);
    memcpy(&resp.name.elements, NODE_NAME, resp.name.count);

    // The software image CRC and the Certificate of Authenticity are optional so not populated in this demo.
    return resp;
}

void processReceivedRequest(const State &state, const CanardTransfer *const transfer)
{
    if (transfer->port_id == uavcan_node_GetInfo_1_0_FIXED_PORT_ID_)
    {
        // The request object is empty so we don't bother deserializing it. Just send the response.
        const uavcan_node_GetInfo_Response_1_0 resp = processRequestNodeGetInfo();
        uint8_t serialized[uavcan_node_GetInfo_Response_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_] = {0};
        size_t serialized_size = sizeof(serialized);
        const int8_t res = uavcan_node_GetInfo_Response_1_0_serialize_(&resp, &serialized[0], &serialized_size);
        if (res >= 0)
        {
            CanardTransfer rt = *transfer;  // Response transfers are similar to their requests.
            if(transfer->timestamp_usec > 0){
                rt.timestamp_usec = transfer->timestamp_usec + ONE_SECOND_DEADLINE;
            }
            rt.transfer_kind = CanardTransferKindResponse;
            rt.payload_size = serialized_size;
            rt.payload = &serialized[0];
            (void) canardTxPush(const_cast<CanardInstance *>(&state.canard), &rt);
        } else
        {
            assert(false);
        }
    }
}

void processReceivedTransfer(const State &state, const CanardTransfer *const transfer)
{
    if (transfer->transfer_kind == CanardTransferKindMessage)
    {
        processReceivedMessage(state, transfer);
    } else if (transfer->transfer_kind == CanardTransferKindRequest)
    {
        processReceivedRequest(state, transfer);
    } else
    {
        assert(false); // This can only happen when received transfer is a response.
    }
}

void receiveTransfer(State &state, int if_index)
{
    CanardFrame frame{};
    frame.timestamp_usec = getMonotonicMicroseconds();
    //TODO: Make sure that the timestamp is initialized
    //TODO: Also make sure that I check for the deadline of a request using my definition of ONE_SECOND_DEADLINE in units.hpp
    std::array<std::uint8_t, 8> payload_array{};
    frame.payload = &payload_array;
    for (uint16_t i = 0; i < max_frames_to_process_per_iteration; ++i)
    {
        bool bxCanQueueHadSomething = bxCANPop(if_index,
                                               &frame.extended_can_id,
                                               &frame.payload_size, const_cast<void *>(frame.payload));
        if (!bxCanQueueHadSomething)
        { return; }
        // The transfer is actually not stored here in this narrow scoped variable
        // Canard has an internal storage to make sure that it can receive frames in any order and assemble them into
        // transfers. If I now take a frame from bxCANPop and libcanard finds that it completes a transfer, it will
        // assign the transfer to the given CanardTransfer object. Not a bug!
        CanardTransfer transfer{};
        const int8_t canard_result = canardRxAccept(&state.canard, &frame, if_index, &transfer);
        if (canard_result > 0)
        {
            processReceivedTransfer(state, &transfer);
            state.canard.memory_free(&state.canard, (void *) transfer.payload);
        } else if ((canard_result == 0) || (canard_result == -CANARD_ERROR_OUT_OF_MEMORY))
        { ;  // Zero means that the frame did not complete a transfer so there is nothing to do.
            // OOM should never occur if the heap is sized correctly. We track OOM errors via heap API.
        } else
        {
            assert(false);  // No other error can possibly occur at runtime.
        }
    }
}

#endif //FIRMWARE_RECEPTION_H
