/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <utility>
#include "registered_ports.hpp"
#include "node/subscription_macros.hpp"


RegisteredPort registered_ports[] =
  {
    FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_GetInfo, 1, 0, &node::essential::uavcan_node_GetInfo_1_0_handler),
    FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_ExecuteCommand, 1, 1,
                                  &uavcan_node_ExecuteCommand_Request_1_1_handler),
    FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_register_Access, 1, 0,
                                  &node::essential::uavcan_register_Access_1_0_handler),
    FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_register_List, 1, 0,
                                  &node::essential::uavcan_register_List_1_0_handler),
    CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(note_response, reg_udral_physics_acoustics_Note,
                                         0, 1,
                                         &reg_udral_physics_acoustics_Note_0_1_handler),
    CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(setpoint, reg_udral_service_actuator_common_sp_Scalar,
                                         0, 1,
                                         &setpoint_handler),
    CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(readiness, reg_udral_service_common_Readiness,
                                         0, 1,
                                         &sub_readiness_handler)
  };

std::pair<RegisteredPort *, RegisteredPort *> get_ports_info_iterators()
{
  return {
    std::begin(registered_ports), std::end(registered_ports)
  };
}
