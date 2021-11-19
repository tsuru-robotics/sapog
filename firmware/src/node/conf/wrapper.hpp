/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <utility>
#include <cstdint>
#include <functional>
#include <uavcan/_register/Value_1_0.h>
#include <cstring>
#include <zubax_chibios/config/config.h>

namespace
{
using function_type = uavcan_register_Value_1_0(float);
using converter_type = std::function<function_type>;
using convert_pair = std::pair<const char *, converter_type>;
using value_type = uavcan_register_Value_1_0;
convert_pair converters[2]{ // NOLINT(bugprone-dynamic-static-initializers)
    {"uavcan.pub.esc.status.id",
        [](float in) {
            value_type value{};
            uavcan_register_Value_1_0_select_natural16_(&value);
            value.natural16.value.elements[0] = static_cast<std::uint16_t>(in);
            value.natural16.value.count = 1;
            return value;
        }},
    {"uavcan.node.id",
        [](float in) {
            value_type value{};
            uavcan_register_Value_1_0_select_natural16_(&value);
            value.natural16.value.elements[0] = in; // NOLINT(cppcoreguidelines-narrowing-conversions)
            return value;
        }}
};
}

converter_type find_converter(const char *name);


namespace conversion
{
enum class ConversionStatus
{
    NOT_SUPPORTED,
    WRONG_TYPE,
    SUCCESS
};
struct ConversionResponse
{
    ConversionStatus conversion_status;
    float value;
};

ConversionResponse extract_any_number(const uavcan_register_Value_1_0 &value, std::optional<ConfigDataType> param);

std::optional<float> extract(const uavcan_primitive_array_Bit_1_0 &bit);

std::optional<float> extract(const uavcan_primitive_array_Integer64_1_0 &integer);

std::optional<float> extract(const uavcan_primitive_array_Real64_1_0 &real);

template<typename T = uavcan_primitive_array_Real64_1_0>
std::optional<T> pack(float input);

//std::optional<uavcan_primitive_array_Bit_1_0> pack(const float input);
}

