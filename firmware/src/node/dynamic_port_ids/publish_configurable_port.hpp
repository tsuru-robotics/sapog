/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include <string_view>

struct PublishConfigurablePort
{
  std::string_view name;
  uint16_t *state_variable;
};

PublishConfigurablePort publish_ports[] = {
  {"uavcan.pub.esc_heartbeat.id", &state.esc_heartbeat_publish_port},
  {"uavcan.pub.feedback.id",      &state.esc_feedback_publish_port},
  {"uavcan.pub.status.id",        &state.esc_status_publish_port},
  {"uavcan.pub.power.id",         &state.esc_power_publish_port},
  {"uavcan.pub.dynamics.id",      &state.esc_dynamics_publish_port},
  {"id_in_esc_group",             &state.id_in_esc_group},
  {"ttl_milliseconds",            &state.ttl_milliseconds}
};