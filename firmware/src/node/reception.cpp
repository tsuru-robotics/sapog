/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "node/reception.hpp"
#include "uavcan/_register/Access_1_0.h"
#include "uavcan/_register/List_1_0.h"
#include "uavcan/_register/Name_1_0.h"
#include "uavcan/_register/Value_1_0.h"
#include "node/conf/wrapper.hpp"
#include "zubax_chibios/zubax_chibios/config/config.h"

std::optional<CanardTransfer> receive_transfer(State &state, int if_index)
{
    CanardFrame frame{};
    frame.timestamp_usec = get_monotonic_microseconds();
    std::array<std::uint8_t, 8> payload_array{};
    frame.payload = &payload_array;
    for (uint16_t i = 0; i < max_frames_to_process_per_iteration; ++i)
    {
        bool bxCanQueueHadSomething = bxCANPop(if_index,
                                               &frame.extended_can_id,
                                               &frame.payload_size, const_cast<void *>(frame.payload));
        if (!bxCanQueueHadSomething)
        { return {}; }
        // The transfer is actually not stored here in this narrow scoped variable
        // Canard has an internal storage to make sure that it can receive frames in any order and assemble them into
        // transfers. If I now take a frame from bxCANPop and libcanard finds that it completes a transfer, it will
        // assign the transfer to the given CanardTransfer object. Not a bug!
        CanardTransfer transfer{};
        CanardRxSubscription subscription{};
        const int8_t canard_result = canardRxAcceptEx(&state.canard, &frame, if_index, &transfer,
                                                      reinterpret_cast<CanardRxSubscription **>(&subscription));
        if (canard_result > 0)
        {
            //printf("I have received a transfer\n");
            return transfer;
            //state.canard.memory_free(&state.canard, (void *) transfer.payload);
        } else if ((canard_result == 0) || (canard_result == -CANARD_ERROR_OUT_OF_MEMORY))
        { ;  // Zero means that the frame did not complete a transfer so there is nothing to do.
            // OOM should never occur if the heap is sized correctly. We track OOM errors via heap API.
        } else
        {
            assert(false);  // No other error can possibly occur at runtime.
        }
    }
    return {};
}

void process_received_transfer(const State &state, const CanardTransfer *const transfer)
{
    if (transfer->transfer_kind == CanardTransferKindMessage)
    {
        process_received_message(state, transfer);
    } else if (transfer->transfer_kind == CanardTransferKindRequest)
    {
        process_received_request(state, transfer);
    } else
    {
        assert(false); // This can only happen when received transfer is a response.
    }
}

std::pair<unsigned int, std::function<bool(const State &, const CanardTransfer *const)>> receivers[3] = {
        {uavcan_node_GetInfo_1_0_FIXED_PORT_ID_,    [](const State &state, const CanardTransfer *const transfer) {
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
        }},
        {uavcan_register_Access_1_0_FIXED_PORT_ID_, [](const State &state, const CanardTransfer *const transfer) {
            uavcan_register_Access_Request_1_0 request{};
            size_t temp_payload_size{transfer->payload_size};
            auto result = uavcan_register_Access_Request_1_0_deserialize_(&request,
                                                                          (const uint8_t *) transfer->payload,
                                                                          &temp_payload_size);
            if (result >= 0)
            {
                if (request.name.name.count == 0)
                {
                    printf("Discarding empty name register access request.\n");
                    return false;
                }
                auto request_name = (const char *) request.name.name.elements;
                assert(request_name != nullptr);
                auto converter = find_converter(request_name);
                float register_value = configGet(request_name);
                auto value = converter(register_value);
                if (uavcan_register_Value_1_0_is_empty_(&value))
                {
                    std::printf("Didn't find a converter for %s\n", request_name);
                    return false;
                }
                uavcan_register_Access_Response_1_0 response{};
                uint8_t serialized[uavcan_register_Access_Response_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
                size_t serialized_size = sizeof(serialized);
                const int8_t error = uavcan_register_Access_Response_1_0_serialize_(&response,
                                                                                    &serialized[0],
                                                                                    &serialized_size);
                assert(error >= 0);
                if (error >= 0)
                {
                    const CanardTransfer response_transfer = {
                            .timestamp_usec = get_monotonic_microseconds() + SECOND_IN_MICROSECONDS,
                            .priority = CanardPriorityNominal,
                            .transfer_kind = CanardTransferKindMessage,
                            .port_id = uavcan_register_Access_1_0_FIXED_PORT_ID_,
                            .remote_node_id = transfer->remote_node_id,
                            .transfer_id = transfer->transfer_id,
                            .payload_size = serialized_size,
                            .payload = &serialized[0],
                    };
                    (void) canardTxPush(const_cast<CanardInstance *>(&state.canard), &response_transfer);
                }
            }
            return true;
        }},
        {uavcan_register_List_1_0_FIXED_PORT_ID_,   [](const State &state, const CanardTransfer *const transfer) {
            (void) state;
            (void) transfer;
            return true;
        }}
};

void process_received_request(const State &state, const CanardTransfer *const transfer)
{
    // Finds a handler and calls it
    for (auto &pair: receivers)
    {
        if (transfer->port_id == pair.first)
        {
            pair.second(state, transfer);
            return;
        }
    }
}


uavcan_node_GetInfo_Response_1_0 process_request_node_get_info()
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

void process_received_message(const State &state, const CanardTransfer *const transfer)
{
    if (transfer->port_id == uavcan_register_Access_1_0_FIXED_PORT_ID_)
    {
        // The transfer could be deserialized to a uavcan_register_Access_Response_1_0
    }
    (void) state;
    (void) transfer;
}
