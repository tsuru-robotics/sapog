#include "uavcan_type_conversion.h"

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