/*
 * Copyright (c) 2022 Zubax, zubax.com
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
#include "reg/udral/service/common/Readiness_0_1.h"
#include <cstdio>
#include <uavcan/si/unit/angular_velocity/Scalar_1_0.h>
#include <motor/motor.hpp>
#include <node/interfaces/IHandler.hpp>

struct : IHandler
{
  void operator()(node::state::State &state, CanardRxTransfer *transfer)
  {
    // ID in esc group needs to be set before readiness is set.
    if (state.id_in_esc_group != CONFIGURABLE_ID_IN_ESC_GROUP)
    {
      (void) state;
      reg_udral_service_common_Readiness_0_1 readiness{};
      size_t size = transfer->payload_size;
      if (reg_udral_service_common_Readiness_0_1_deserialize_(&readiness,
                                                              (const uint8_t *) transfer->payload,
                                                              &size) >= 0)
      {
        state.readiness = node::state::Readiness(readiness.value);
      }
      (void) transfer;
      return;
    }
  }
} sub_readiness_handler;
