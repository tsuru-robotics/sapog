#ifndef FIRMWARE_UAVCAN_TYPE_CONVERSION_H
#define FIRMWARE_UAVCAN_TYPE_CONVERSION_H

#include <uavcan/_register/Value_1_0.h>
#include <optional>

namespace conversion
{
std::optional<float> extract(const uavcan_primitive_array_Bit_1_0 &bit);

std::optional<float> extract(const uavcan_primitive_array_Integer64_1_0 &integer);

std::optional<float> extract(const uavcan_primitive_array_Real64_1_0 &real);

template<typename T = uavcan_primitive_array_Real64_1_0>
std::optional<T> pack(const float input);

//std::optional<uavcan_primitive_array_Bit_1_0> pack(const float input);
}

#endif //FIRMWARE_UAVCAN_TYPE_CONVERSION_H
