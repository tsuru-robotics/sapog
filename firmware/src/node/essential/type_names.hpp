/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "node/register_values/type_name_association.hpp"

type_name_association types_names[] = {
  {"uavcan.sub.note_response.type", "reg.udral.physics.acoustics.Note.0.1"},
  {"uavcan.sub.readiness.type",     "reg.udral.service.common.Readiness.0.1"},
  {"uavcan.sub.setpoint.type",      "reg.udral.service.actuator.common.sp.Scalar.0.1"},
  {"uavcan.sub.note_response.type", "reg.udral.physics.acoustics.Note.0.1"},
  {"id_in_esc_group.type",          "uavcan.primitive.scalar.Natural16.1.0"},
};