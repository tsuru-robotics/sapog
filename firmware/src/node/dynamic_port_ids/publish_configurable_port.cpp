/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include "publish_configurable_port.hpp"

PublishConfigurablePort publish_ports[] = {
  {"uavcan.pub.esc_heartbeat.id", &state.publish_ports.esc_heartbeat},
  {"uavcan.pub.feedback.id",      &state.publish_ports.esc_feedback},
  {"uavcan.pub.status.id",        &state.publish_ports.esc_status},
  {"uavcan.pub.power.id",         &state.publish_ports.esc_power},
  {"uavcan.pub.dynamics.id",      &state.publish_ports.esc_dynamics},
  {"id_in_esc_group",             &state.id_in_esc_group},
  {"ttl_milliseconds",            &state.ttl_milliseconds}
};

inline std::pair<PublishConfigurablePort *, PublishConfigurablePort *> get_publish_port_iterators()
{
  return {std::begin(publish_ports), std::end(publish_ports)};
}