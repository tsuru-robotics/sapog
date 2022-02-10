/*
 * Copyright (c) 2022 Zubax, zubax.com
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

namespace node::conf::wrapper
{
struct ConverterReturnType
{
    uavcan_register_Value_1_0 value;
    bool _mutable = true;
    bool persistent = true;
};
using value_type = uavcan_register_Value_1_0;
using function_type = ConverterReturnType(float in, uavcan_register_Value_1_0 &out_value);
using converter_type = std::function<function_type>;
using convert_pair = std::pair<const char *, converter_type>;

std::optional<converter_type> find_converter(const char *name);
}

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

