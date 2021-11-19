/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

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
#include <uavcan/si/unit/angular_velocity/Scalar_1_0.h>
#include <motor/motor.hpp>
#include <node/interfaces/IHandler.hpp>

struct : IHandler
{
    void operator()(node::state::State &state, CanardTransfer *transfer)
    {
        (void) state;
        uavcan_si_unit_angular_velocity_Scalar_1_0 angular_velocity{};
        size_t size = transfer->payload_size;
        if (uavcan_si_unit_angular_velocity_Scalar_1_0_deserialize_(&angular_velocity,
                                                                    (const uint8_t *) transfer->payload,
                                                                    &size) >= 0)
        {
            float rotations_per_second = angular_velocity.radian_per_second / 2.0 / 3.14159265358979f;
            unsigned int rpm = rotations_per_second * 60;
            motor_set_rpm(rpm, 100);
        }
        (void) transfer;
        return;
    }
} sub_esc_rpm_handler;


struct : IHandler
{
    void operator()(node::state::State &state, CanardTransfer *transfer)
    {
        (void) state;
        (void) transfer;
        return;
    }
} sub_esc_duty_cycle_handler;

struct : IHandler
{
    void operator()(node::state::State &state, CanardTransfer *transfer)
    {
        (void) state;
        (void) transfer;
        return;
    }
} sub_esc_power_handler;

struct : IHandler
{
    void operator()(node::state::State &state, CanardTransfer *transfer)
    {
        reg_udral_physics_electricity_PowerTs_0_1 power_ts{};
        printf("ESC handler\n");
        size_t temp_payload_size{transfer->payload_size};
        auto result = reg_udral_physics_electricity_PowerTs_0_1_deserialize_(&power_ts,
                                                                             (const uint8_t *) transfer->payload,
                                                                             &temp_payload_size);
        (void) state;
        (void) result;
        return;
    }
} reg_udral_physics_electricity_PowerTs_0_1_handler;
