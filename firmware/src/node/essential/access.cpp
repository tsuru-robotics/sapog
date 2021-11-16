/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <uavcan/_register/Access_1_0.h>
#include <node/units.hpp>
#include <node/time.h>
#include <cstdio>
#include <node/conf/wrapper.hpp>
#include "access.hpp"

template<std::size_t Size>
inline static void get_name_null_terminated_string(uavcan_register_Access_Request_1_0 &request,
                                                   std::array<char, Size> &out_request_name)
{
    std::copy(std::begin(request.name.name.elements), std::end(request.name.name.elements),
              std::begin(out_request_name));
    out_request_name.at(request.name.name.count) = '\0';
}

inline static void get_response_value(const char *const request_name, uavcan_register_Value_1_0 &out_value)
{
    ConfigParam param{};
    if (configGetDescr(request_name, &param) != 0)
    {
        uavcan_register_Value_1_0_select_empty_(&out_value);
        out_value.empty = uavcan_primitive_Empty_1_0{0};
        printf("Access returns with empty value\n");
        return;
    }
    printf("Response value is not empty\n");
    float value = configGet(request_name);
    if (param.type == CONFIG_TYPE_FLOAT)
    {
        printf("Response value is a float: %f\n", value);
        uavcan_register_Value_1_0_select_real64_(&out_value);
        out_value.real64.value.elements[0] = value;
        out_value.real64.value.count = 1;
    } else if (param.type == CONFIG_TYPE_INT)
    {
        printf("Response type is an int: %d\n", (uint16_t) value);
        uavcan_register_Value_1_0_select_integer64_(&out_value);
        out_value.integer64.value.elements[0] = value;
        out_value.integer64.value.count = 1;
    } else if (param.type == CONFIG_TYPE_BOOL)
    {
        printf("Response type is bool\n");
        uavcan_register_Value_1_0_select_bit_(&out_value);
        printf("The value that is being saved into a boolean: %d\n", (int) value);
        printf("nunavutSetBit %d", nunavutSetBit(out_value.bit.value.bitpacked, 1, 0, value != 0));
        out_value.bit.value.count = 1;
    }
}

inline static bool respond_to_access(CanardInstance *canard, const char *request_name,
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
    {
        printf("Failed to serialize access response with code %d\n", error);
        return false;
    }
    printf("Successfully serialized access response.\n");
    const CanardTransfer response_transfer = {
        .timestamp_usec = get_monotonic_microseconds() + SECOND_IN_MICROSECONDS * 1,
        .priority = transfer->priority,
        .transfer_kind = CanardTransferKindResponse,
        .port_id = uavcan_register_Access_1_0_FIXED_PORT_ID_,
        .remote_node_id = transfer->remote_node_id,
        .transfer_id = transfer->transfer_id,
        .payload_size = serialized_size,
        .payload = &serialized[0],
    };
    (void) canardTxPush(const_cast<CanardInstance *>(canard), &response_transfer);
    printf("Sent access response.\n");
    return true;
}

namespace node::essential
{
bool uavcan_register_Access_1_0_handler(const node::state::State &state, const CanardTransfer *const transfer)
{
    printf("Access handler\n");
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
    ConfigParam entry_config_params{};
    bool register_has_entry_for_name = configGetDescr(request_name.data(), &entry_config_params) == 0;
    if (register_has_entry_for_name)
    {
        std::optional<float> sapog_acceptable_value = ::conversion::extract_any_number(request.value,
                                                                                       entry_config_params.type);
        // Going to write a value to the register.
        if (sapog_acceptable_value.has_value())
        {
            printf("Request provides a value\n");
            float received_value = sapog_acceptable_value.value();
            char *request_name_c = request_name.data();
            printf("Request name: %s\n", request_name_c);
            printf("Received (int) value: %d\n", (int) received_value);
            configSet(request_name_c, received_value);
            configSave();
            printf("Saved configuration.\n");
        } else
        {
            printf("Received a value that cannot be stored in Sapog.\n");
        }
    }

    // The client is going to get a response with the actual value of the register
    assert(request_name.data() != nullptr);
    // We are silently losing precision, but it shouldn't matter for this application
    respond_to_access(const_cast<CanardInstance *>(&state.canard), request_name.data(), transfer);
    return true;
}
}