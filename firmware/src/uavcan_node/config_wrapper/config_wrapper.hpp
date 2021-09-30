#ifndef FIRMWARE_CONFIG_WRAPPER_HPP
#define FIRMWARE_CONFIG_WRAPPER_HPP

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


converter_type find_converter(const char *name)
{
    int name_length{static_cast<int>(std::strlen(name))};
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
    return [](float input){
        return value_type{};
    };
}

#endif //FIRMWARE_CONFIG_WRAPPER_HPP
