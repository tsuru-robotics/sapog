/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "esc.hpp"
#include "src/settings/registers.hpp"
#include <reg/udral/service/common/Readiness_0_1.h>
#include <reg/udral/service/actuator/common/Feedback_0_1.h>
#include <reg/udral/service/actuator/common/Status_0_1.h>
#include <reg/udral/physics/dynamics/translation/LinearTs_0_1.h>
#include <reg/udral/physics/electricity/PowerTs_0_1.h>
#include <cstdio>
#include <uavcan/si/unit/angular_velocity/Scalar_1_0.h>
#include "reg/udral/service/actuator/common/sp/Vector31_0_1.h"
#include <motor/motor.hpp>
#include <node/interfaces/IHandler.hpp>
#include "node/esc/esc_publishers.hpp"
#include "node/transmit.hpp"
#include <algorithm>
#include <motor/motor_ttl_expiry_handler.hpp>

using Readiness = node::state::Readiness;
using ControlMode = node::state::ControlMode;

struct : IStateAwareHandler
{
    void operator()(node::state::State *state)
    {
        assert(state != nullptr);
        printf("Readiness expired!!!\n");
        if (state != nullptr)
        {
            state->readiness = Readiness::STANDBY;
        }
    }
} ttl_expiry_handler;

struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        if (state.readiness == Readiness::ENGAGED && state.id_in_esc_group != 255)
        {
            reg_udral_service_actuator_common_sp_Vector31_0_1 setpoint{};
            size_t size = transfer->payload_size;
            if (reg_udral_service_actuator_common_sp_Vector31_0_1_deserialize_(&setpoint,
                                                                               (const uint8_t *) transfer->payload,
                                                                               &size) >= 0)
            {
                if (state.control_mode == ControlMode::RPM)
                {
                    float rotations_per_second = setpoint.value[state.id_in_esc_group] / 2.0f / 3.14159265358979f;
                    unsigned int rpm = rotations_per_second * 60;
                    motor_set_rpm(rpm, state.ttl_milliseconds);
                    ttl_expiry_handler.state = &state;
                    motor_set_current_ttl_expiry_handler(&ttl_expiry_handler);
                    publish_esc_feedback(state);
                    transmit(state);
                    return;
                } else if (state.control_mode == ControlMode::DUTYCYCLE)
                {
                    float dc = setpoint.value[state.id_in_esc_group];
                    // the range is clipped in here
                    motor_set_duty_cycle(dc, state.ttl_milliseconds);
                    ttl_expiry_handler.state = &state;
                    motor_set_current_ttl_expiry_handler(&ttl_expiry_handler);
                    publish_esc_feedback(state);
                    transmit(state);
                    return;
                }
            }
        }
    }
} setpoint_handler;