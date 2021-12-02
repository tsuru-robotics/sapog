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
#include <uavcan/primitive/scalar/Natural16_1_0.h>
#include "access.hpp"

struct type_name_association
{
    const char *name;
    const char *type_name;
};

template<std::size_t Size>
inline static void get_name_null_terminated_string(uavcan_register_Access_Request_1_0 &request,
                                                   std::array<char, Size> &out_request_name)
{
    std::copy(std::begin(request.name.name.elements), std::end(request.name.name.elements),
              std::begin(out_request_name));
    out_request_name.at(request.name.name.count) = '\0';
}

type_name_association types_names[] = {
    {"uavcan.sub.note_response.type", "reg.udral.physics.acoustics.Note.0.1"},
    {"uavcan.sub.readiness.type",     "reg.udral.service.common.Readiness.0.1"},
    {"uavcan.sub.setpoint.type",      "reg.udral.service.actuator.common.sp.Scalar.0.1"},
    {"uavcan.sub.note_response.type", "reg.udral.physics.acoustics.Note.0.1"},
};

std::string_view find_type_name(const char *const request_name)
{
    std::string_view found_type_name{};
    for (auto &iter: types_names)
    {
        if (std::string_view(iter.name) == std::string_view(request_name))
        {
            found_type_name = iter.type_name;
        }
    }
    return found_type_name;
}

struct RegisterCriteria
{
    bool _mutable;
    bool persistent;
};

inline static RegisterCriteria get_response_value(std::string_view
                                                  request_name,
                                                  uavcan_register_Value_1_0 &out_value
)
{
    ConfigParam param{};
    if (configGetDescr(request_name.data(), &param) != 0)
    {
        std::string_view type_string = find_type_name(request_name.data());
        bool endsWithId =
            request_name.at(request_name.size() - 1) == 'd' && request_name.at(request_name.size() - 2) == 'i' &&
            request_name.at(request_name.size() - 3) == '.';
        if (type_string != "")
        {
            uavcan_register_Value_1_0_select_string_(&out_value);
            uavcan_primitive_String_1_0 return_value{};
            return_value.value.count = type_string.size();
            memcpy(&return_value.value.elements, type_string.data(), return_value.value.count);
            out_value._string = return_value;
            return RegisterCriteria{._mutable=true, .persistent = true};
        } else if (endsWithId)
        {
            uavcan_register_Value_1_0_select_string_(&out_value);
            uavcan_primitive_String_1_0 return_value{};
            constexpr
            std::string_view natural16_string = "uavcan.primitive.scalar.Natural16.1.0\0";
            return_value.value.count = natural16_string.size();
            std::copy(natural16_string.begin(), natural16_string.end(), std::begin(return_value.value.elements));
            out_value._string = return_value;
        } else
        {
            uavcan_register_Value_1_0_select_empty_(&out_value);
            out_value.empty = uavcan_primitive_Empty_1_0{0};
            printf("Access returns with empty value\n");
            return RegisterCriteria{._mutable=true, .persistent = true};
        }
    }
    float value = configGet(request_name.data());
    std::optional <node::conf::wrapper::converter_type> converter = node::conf::wrapper::find_converter(
        request_name.data());
    std::string_view request_name_sw(request_name.data());
    if (converter.has_value())
    {
        auto converter_response = converter.value()(value);
        out_value = converter_response.value;
        return RegisterCriteria{._mutable = converter_response._mutable, .persistent = converter_response.persistent};
    } else
    {
        if (param.type == CONFIG_TYPE_FLOAT)
        {
            printf("Response value: float: %f\n", value);
            uavcan_register_Value_1_0_select_real64_(&out_value);
            out_value.real64.value.elements[0] = value;
            out_value.real64.value.
                count = 1;
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
            printf("nunavutSetBit %d\n",
                   nunavutSetBit(out_value
                                     .bit.value.bitpacked, 1, 0, value != 0));
            out_value.bit.value.
                count = 1;
        }
    }
    return RegisterCriteria{};
}

inline static bool respond_to_access(node::state::State &state, std::basic_string_view<char> request_name,
                                     const CanardRxTransfer *const transfer)
{
    uavcan_register_Access_Response_1_0 response{};
    // Read the value and send it back to the client
    uavcan_register_Value_1_0 response_value{};
    auto register_criteria = get_response_value(request_name, response_value);
    response.value = response_value;
    response.persistent = register_criteria.persistent;
    response._mutable = register_criteria._mutable;
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
    for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
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
        std::array < char, uavcan_register_Name_1_0_name_ARRAY_CAPACITY_ + 1 > request_name;
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
        respond_to_access(state, std::string_view(request_name.data()), transfer);
        return;
    }
} uavcan_register_Access_1_0_handler;
}

