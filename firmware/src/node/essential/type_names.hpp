/*
 * Copyright (c) 2022 Zubax, zubax.com
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
  {"uavcan.pub.feedback.type",      "reg.udral.service.actuator.common.Feedback.0.1"},
  {"uavcan.pub.power.type",         "reg.udral.physics.electricity.PowerTs.0.1"},
  {"uavcan.pub.status.type",        "reg.udral.service.actuator.common.Status.0.1"},
  {"uavcan.pub.dynamics.type",      "reg.udral.physics.dynamics.rotation.PlanarTs.0.1"},
  {"uavcan.pub.esc_heartbeat.type", "reg.udral.service.common.Heartbeat.0.1"},
};