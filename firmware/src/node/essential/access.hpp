/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include "node/state.hpp"

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
#include <node/interfaces/IHandler.hpp>
#include "access.hpp"

struct type_name_association
{
    const char *name;
    const char *type_name;
};

type_name_association types_names[] = {
    {"uavcan.sub.note_response.type", "reg.udral.physics.acoustics.Note.0.1"},
    {"uavcan.sub.readiness.type",     "reg.udral.service.common.Readiness.0.1"},
    {"uavcan.sub.setpoint.type",      "reg.udral.service.actuator.common.sp.Scalar.0.1"},
    {"uavcan.sub.note_response.type", "reg.udral.physics.acoustics.Note.0.1"},
};

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
    float value = configGet(request_name);
    auto converter = node::conf::wrapper::find_converter(request_name);
    if (converter.has_value())
    {
        out_value = converter.value()(value);
    } else
    {
        if (param.type == CONFIG_TYPE_FLOAT)
        {
            printf("Response value: float: %f\n", value);
            uavcan_register_Value_1_0_select_real64_(&out_value);
            out_value.real64.value.elements[0] = value;
            out_value.real64.value.count = 1;
        } else if (param.type == CONFIG_TYPE_INT)
        {
            printf("Response type: int: %d\n", (uint16_t) value);
            uavcan_register_Value_1_0_select_integer64_(&out_value);
            out_value.integer64.value.elements[0] = value;
            out_value.integer64.value.count = 1;
        } else if (param.type == CONFIG_TYPE_BOOL)
        {
            printf("Response type: bool\n");
            uavcan_register_Value_1_0_select_bit_(&out_value);
            printf("The value that is being saved into a boolean: %d\n", (int) value);
            printf("nunavutSetBit %d\n", nunavutSetBit(out_value.bit.value.bitpacked, 1, 0, value != 0));
            out_value.bit.value.count = 1;
        }
    }
}

inline static bool respond_to_access(node::state::State &state, const char *request_name,
                                     const CanardRxTransfer *const transfer)
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
    printf("Serialized.\n");
    CanardTransferMetadata rtm = transfer->metadata;  // Response transfers are similar to their requests.
    rtm.transfer_kind = CanardTransferKindResponse;
    for (int i = 0; i < AMOUNT_OF_QUEUES; ++i)
    {
        int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                         const_cast<CanardInstance *>(&state.canard),
                                                         get_monotonic_microseconds() +
                                                         ONE_SECOND_DEADLINE_usec,
                                                         &rtm,
                                                         serialized_size,
                                                         serialized);

        (void) number_of_frames_enqueued;
        assert(number_of_frames_enqueued > 0);
    }
    printf("Responded.\n");
    return true;
}


namespace node::essential
{
struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        (void) state;
        uavcan_register_Access_Request_1_0 request{};
        size_t temp_payload_size{transfer->payload_size};
        auto result = uavcan_register_Access_Request_1_0_deserialize_(&request,
                                                                      (const uint8_t *) transfer->payload,
                                                                      &temp_payload_size);
        assert(result >= 0);
        if (result < 0)
        { return; } // maybe it is a damaged frame, could happen?
        if (request.name.name.count == 0)
        {
            return;
        }
        std::array<char, uavcan_register_Name_1_0_name_ARRAY_CAPACITY_ + 1> request_name;
        get_name_null_terminated_string<uavcan_register_Name_1_0_name_ARRAY_CAPACITY_ + 1>(request, request_name);
        ConfigParam entry_config_params{};
        printf("\n\nAccess handler: %s\n", request_name.data());
        bool register_has_entry_for_name = configGetDescr(request_name.data(), &entry_config_params) == 0;
        if (register_has_entry_for_name)
        {
            conversion::ConversionResponse conversion_response = ::conversion::extract_any_number(request.value,
                                                                                                  {entry_config_params.type});
            // Going to write a value to the register.
            switch (conversion_response.conversion_status)
            {
                case conversion::ConversionStatus::SUCCESS:
                {
                    float received_value = conversion_response.value;
                    char *request_name_c = request_name.data();
                    printf("(int) value: %d\n", (int) received_value);
                    configSet(request_name_c, received_value);
                    break;
                }
                case conversion::ConversionStatus::NOT_SUPPORTED:
                    if (uavcan_register_Value_1_0_is_empty_(&request.value))
                    {
                        printf("Read requested.\n");
                    } else
                    {
                        printf("Value that cannot be stored in any register.\n");
                    }
                    break;
                case conversion::ConversionStatus::WRONG_TYPE:
                    printf("Value of this type that cannot be stored in this register.\n");
                    break;
            }
        }
        // The client is going to get a response with the actual value of the register
        assert(request_name.data() != nullptr);
        // We are silently losing precision, but it shouldn't matter for this application
        respond_to_access(state, request_name.data(),
                          transfer);
        return;
    }
} uavcan_register_Access_1_0_handler;
}

