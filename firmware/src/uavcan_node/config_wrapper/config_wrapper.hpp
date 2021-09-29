#ifndef FIRMWARE_CONFIG_WRAPPER_HPP
#define FIRMWARE_CONFIG_WRAPPER_HPP

#include <utility>
#include <cstdint>
#include <functional>
#include <uavcan/_register/Value_1_0.h>

std::pair<const char *,  std::function<uavcan_register_Value_1_0(float)>> reference[2]{
        {"uavcan.pub.esc.status.id",
         [](float in){
            uavcan_register_Value_1_0 value{};
            uavcan_register_Value_1_0_select_natural16_(&value);
            value.natural16.value.elements[0] = static_cast<std::uint16_t>(in);
            value.natural16.value.count = 1;
            return value;
        }},
        std::make_pair("uavcan.node.id", [](float in){
            uavcan_register_Value_1_0 value{};
            uavcan_register_Value_1_0_select_natural16_(&value);
            value.natural16.value.elements[0] = in;
            return value;
        }),
};
#endif //FIRMWARE_CONFIG_WRAPPER_HPP
