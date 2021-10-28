/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "esc.hpp"
#include "src/settings/registers.hpp"
#include <reg/udral/service/common/Readiness_0_1.h>
#include <reg/udral/service/actuator/common/__0_1.h>
#include <reg/udral/service/actuator/common/Feedback_0_1.h>
#include <reg/udral/service/actuator/common/Status_0_1.h>
#include <reg/udral/physics/dynamics/translation/LinearTs_0_1.h>
#include <reg/udral/physics/electricity/PowerTs_0_1.h>
#include <cstdio>

bool
reg_udral_physics_electricity_PowerTs_0_1_handler(const node::state::State &state, const CanardTransfer *const transfer)
{
    reg_udral_physics_electricity_PowerTs_0_1 power_ts{};
    printf("ESC handler\n");
    size_t temp_payload_size{transfer->payload_size};
    auto result = reg_udral_physics_electricity_PowerTs_0_1_deserialize_(&power_ts, (const uint8_t *) transfer->payload,
                                                                         &temp_payload_size);
    (void) state;
    (void) result;
    return true;
}
