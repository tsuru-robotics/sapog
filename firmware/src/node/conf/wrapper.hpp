#pragma once

#include <utility>
#include <cstdint>
#include <functional>
#include <uavcan/_register/Value_1_0.h>
#include <cstring>

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

