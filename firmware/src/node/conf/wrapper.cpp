/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "wrapper.hpp"

namespace node::conf::wrapper
{

convert_pair converters[] = {
    {"uavcan.node.id",
     [](float in) {
         value_type value{};
         uavcan_register_Value_1_0_select_natural16_(&value);
         value.natural16.value.elements[0] = in; // NOLINT(cppcoreguidelines-narrowing-conversions)
         return ConverterReturnType{.value = value, ._mutable = true, .persistent = true};
     }},
}; // NOLINT(bugprone-dynamic-static-initializers)
}

using converter_type = node::conf::wrapper::converter_type;

std::optional<converter_type> node::conf::wrapper::find_converter(const char *name)
{
    using namespace node::conf::wrapper;
    for (auto &pair: converters)
    {
        const char *current_name = pair.first;
        if (strcmp(current_name, name) == 0)
        {
            converter_type *converter = &(pair.second);
            return *converter;
        }
    }
    // In case there isn't a matching converter, return one that returns an empty value.
    // the returned value is basically selected to be uavcan.primitive.Empty.1.0
    return {};
}

#define CHECK_PARAM_IF_GIVEN(type) \
!param.has_value() || param.value() == type


namespace conversion
{
ConversionResponse extract_any_number(const uavcan_register_Value_1_0 &value, std::optional<ConfigDataType> param)
{
    if (uavcan_register_Value_1_0_is_integer16_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_INT))
        {
            return {ConversionStatus::SUCCESS, (float) value.integer16.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_integer32_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_INT))
        {
            return {ConversionStatus::SUCCESS, (float) value.integer32.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_integer64_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_INT))
        {
            return {ConversionStatus::SUCCESS, (float) value.integer64.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_natural16_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_INT))
        {
            return {ConversionStatus::SUCCESS, (float) value.natural16.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_natural32_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_INT))
        {
            return {ConversionStatus::SUCCESS, (float) value.natural32.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_natural64_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_INT))
        {
            return {ConversionStatus::SUCCESS, (float) value.natural64.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_real16_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_FLOAT))
        {
            return {ConversionStatus::SUCCESS, (float) value.real16.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_real32_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_FLOAT))
        {
            return {ConversionStatus::SUCCESS, (float) value.real32.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_real64_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_FLOAT))
        {
            return {ConversionStatus::SUCCESS, (float) value.real64.value.elements[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};

    } else if (uavcan_register_Value_1_0_is_bit_(&value))
    {
        if (CHECK_PARAM_IF_GIVEN(CONFIG_TYPE_BOOL))
        {
            return {ConversionStatus::SUCCESS, (float) value.bit.value.bitpacked[0]};
        }
        return {ConversionStatus::WRONG_TYPE, 0};
    }
    return {ConversionStatus::NOT_SUPPORTED, 0};
}

std::optional<float> extract(const uavcan_primitive_array_Integer64_1_0 &integer)
{
    if (integer.value.count == 0)
    {
        return {};
    }
    return integer.value.elements[0];
}

std::optional<float> extract(const uavcan_primitive_array_Bit_1_0 &bit)
{
    if (bit.value.count == 0)
    {
        return {};
    }
    return nunavutGetBit(bit.value.bitpacked, sizeof(bit.value.bitpacked), 0);
}

std::optional<float> extract(const uavcan_primitive_array_Real64_1_0 &real)
{
    if (real.value.count == 0)
    { return {}; }
    return real.value.elements[0];
}


template<typename T>
std::optional<T> pack(const float input)
{
    T return_value{};
    return_value.value.elements[0] = input;
    return return_value;
}

std::optional<uavcan_primitive_array_Bit_1_0> pack(const float input)
{
    uavcan_primitive_array_Bit_1_0 return_value{};
    return_value.value.bitpacked[0] = input;
    return return_value;
}
}