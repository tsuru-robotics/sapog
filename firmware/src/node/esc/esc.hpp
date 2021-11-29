/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

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
#include "reg/udral/service/actuator/common/sp/Scalar_0_1.h"
#include <motor/motor.hpp>
#include <node/interfaces/IHandler.hpp>
#include "node/esc/esc_publishers.hpp"
#include <algorithm>

struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        if (state.readiness == Readiness::ENGAGED && state.id_in_esc_group != CONFIGURABLE_ID_IN_ESC_GROUP)
        {
            reg_udral_service_actuator_common_sp_Scalar_0_1 setpoint{};
            size_t size = transfer->payload_size;
            if (reg_udral_service_actuator_common_sp_Scalar_0_1_deserialize_(&setpoint,
                                                                             (const uint8_t *) transfer->payload,
                                                                             &size) >= 0)
            {
                if (state.control_mode == ControlMode::RPM)
                {

                    float rotations_per_second = setpoint.value / 2.0 / 3.14159265358979f;
                    unsigned int rpm = rotations_per_second * 60;
                    printf("RPM: %d\n", rpm);
                    motor_set_rpm(rpm, state.ttl_milliseconds);
                    publish_esc_feedback(state);
                    (void) transfer;
                    return;
                } else if (state.control_mode == ControlMode::DUTYCYCLE)
                {
                    float dc = setpoint.value;
                    dc = std::min(dc, 1.0f);
                    printf("DC: %f\n", (float) dc);
                    motor_set_duty_cycle(dc, state.ttl_milliseconds);
                    publish_esc_feedback(state);
                    (void) transfer;
                    return;
                }
            }
        }
    }
} setpoint_handler;


struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        (void) state;
        (void) transfer;
        return;
    }
} sub_esc_duty_cycle_handler;

struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        (void) state;
        (void) transfer;
        return;
    }
} sub_esc_power_handler;

struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
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
