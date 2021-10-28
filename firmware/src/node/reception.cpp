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
#include "zubax_chibios/zubax_chibios/config/config.h"
#include "transmit.hpp"
#include "node.hpp"
#include "reg/udral/physics/acoustics/Note_0_1.h"

std::pair<std::optional<CanardTransfer>, SubscriptionData*> receive_transfer(State &state, int if_index)
{
    CanardFrame frame{};
    frame.timestamp_usec = get_monotonic_microseconds();
    std::array<std::uint8_t, 8> payload_array{};
    frame.payload = &payload_array;
    for (uint16_t i = 0; i < max_frames_to_process_per_iteration; ++i)
    {
        bool bxCanQueueHadSomething = bxCANPop(if_index,
                                               &frame.extended_can_id,
                                               &frame.payload_size, payload_array.data());
        if (!bxCanQueueHadSomething)
        { return {}; }
        // The transfer is actually not stored here in this narrow scoped variable
        // Canard has an internal storage to make sure that it can receive frames in any order and assemble them into
        // transfers. If I now take a frame from bxCANPop and libcanard finds that it completes a transfer, it will
        // assign the transfer to the given CanardTransfer object. Not a bug!
        CanardTransfer transfer{};
        CanardRxSubscription *this_subscription;
        const int8_t canard_result = canardRxAcceptEx(&state.canard, &frame, if_index, &transfer, &this_subscription);
        //this_subscription->
        if (canard_result > 0)
        {
            return {transfer, static_cast<SubscriptionData*>(this_subscription->user_reference)};
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
    auto a = get_subscriptions();
    auto start = a.first;
    auto end = a.second;
    for (auto it = start; it!=end; ++it)
    {
        if (transfer->port_id == it->second.port_id)
        {
            it->second.handler(state, transfer);
            return;
        }
    }
}

template<std::size_t Size>
static void get_name_null_terminated_string(uavcan_register_Access_Request_1_0 &request,
                                            std::array<char, Size> &out_request_name)
{
    std::copy(std::begin(request.name.name.elements), std::end(request.name.name.elements),
              std::begin(out_request_name));
    out_request_name.at(request.name.name.count) = '\0';
}

void get_response_value(const char *const request_name, uavcan_register_Value_1_0 &out_value)
{
    ConfigParam param{};
    if (configGetDescr(request_name, &param) != 0)
    {
        uavcan_register_Value_1_0_select_empty_(&out_value);
    }
    float value = configGet(request_name);
    if (param.type == CONFIG_TYPE_FLOAT)
    {
        uavcan_register_Value_1_0_select_real64_(&out_value);
        out_value.real64.value.elements[0] = value;
        out_value.real64.value.count = 1;
    } else if (param.type == CONFIG_TYPE_INT)
    {
        uavcan_register_Value_1_0_select_integer64_(&out_value);
        out_value.integer64.value.elements[0] = value;
        out_value.integer64.value.count = 1;
    } else if (param.type == CONFIG_TYPE_BOOL)
    {
        uavcan_register_Value_1_0_select_bit_(&out_value);
        nunavutSetBit(out_value.bit.value.bitpacked, out_value.bit.value.count, 0, value != 0);
    }
}

bool respond_to_access(CanardInstance *canard, const char *request_name,
                       const CanardTransfer *const transfer)
{
    uavcan_register_Access_Response_1_0 response{};
    // Read the value and send it back to the client
    uavcan_register_Value_1_0 response_value{};
    get_response_value(request_name, response_value);
    response.value = response_value;
    uint8_t serialized[uavcan_register_Access_Response_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
    size_t serialized_size = sizeof(serialized);
    int8_t error = uavcan_register_Access_Response_1_0_serialize_(&response, &serialized[0], &serialized_size);
    assert(error >= 0);
    if (error < 0)
    { return false; }
    const CanardTransfer response_transfer = {
            .timestamp_usec = get_monotonic_microseconds() + SECOND_IN_MICROSECONDS * 2,
            .priority = transfer->priority,
            .transfer_kind = CanardTransferKindResponse,
            .port_id = uavcan_register_Access_1_0_FIXED_PORT_ID_,
            .remote_node_id = transfer->remote_node_id,
            .transfer_id = transfer->transfer_id,
            .payload_size = serialized_size,
            .payload = &serialized[0],
    };
    (void) canardTxPush(const_cast<CanardInstance *>(canard), &response_transfer);
    return true;
}

bool uavcan_node_GetInfo_1_0_handler(const State &state, const CanardTransfer *const transfer)
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
bool not_implemented_handler(const State &state, const CanardTransfer *const transfer)
{
    (void) transfer;
    (void) state;
    return true;
}
bool uavcan_register_Access_1_0_handler(const State &state, const CanardTransfer *const transfer)
{
    uavcan_register_Access_Request_1_0 request{};
    size_t temp_payload_size{transfer->payload_size};
    auto result = uavcan_register_Access_Request_1_0_deserialize_(&request,
                                                                  (const uint8_t *) transfer->payload,
                                                                  &temp_payload_size);
    assert(result >= 0);
    if (result < 0)
    { return false; } // maybe it is a damaged frame, could happen?
    if (request.name.name.count == 0)
    {
        return false;
    }
    std::array<char, uavcan_register_Name_1_0_name_ARRAY_CAPACITY_ + 1> request_name;
    get_name_null_terminated_string<uavcan_register_Name_1_0_name_ARRAY_CAPACITY_ + 1>(request, request_name);

    // Bounds checking
    bool does_request_provide_value = !uavcan_register_Value_1_0_is_empty_(&request.value);
    // Going to write a value to the register.
    if (does_request_provide_value)
    {
        float received_value = (float) request.value.integer64.value.elements[0];
        char *request_name_c = request_name.data();
        configSet(request_name_c, received_value);
        configSave();
    }
    // The client is going to get a response with the actual value of the register
    assert(request_name.data() != nullptr);
    // We are silently losing precision, but it shouldn't matter for this application
    respond_to_access(const_cast<CanardInstance *>(&state.canard), request_name.data(), transfer);
    return true;
}

bool reg_udral_physics_acoustics_Note_0_1_handler(const State &state, const CanardTransfer *const transfer)
{
    (void) transfer;
    (void) state;
    return true;
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
    resp.name.count = strlen(NODE_NAME); // QUESTION: Does this string include a null terminator? It mustn't include it.
    memcpy(&resp.name.elements, NODE_NAME, resp.name.count);

    // The software image CRC and the Certificate of Authenticity are optional so not populated in this demo.
    return resp;
}