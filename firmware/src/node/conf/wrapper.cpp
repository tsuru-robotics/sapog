/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "wrapper.hpp"

converter_type find_converter(const char *name)
{
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
    return [](float input) {
        (void) input;
        return value_type{};
    };
}
namespace conversion
{
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