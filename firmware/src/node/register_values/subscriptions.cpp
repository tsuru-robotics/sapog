/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <utility>
#include "subscriptions.hpp"
#include "node/subscription_macros.hpp"
#include "node/commands/commands.hpp"
#include <node/essential/get_info.hpp>
#include <uavcan/node/ExecuteCommand_1_1.h>
#include "node/essential/register_list.hpp"
#include "node/essential/note.hpp"
#include "node/esc/esc.hpp"
#include "node/esc/readiness.hpp"
#include "node/essential/access_handler.hpp"
#include "node/node_config_macros/node_config.hpp"


AnySubscription registered_ports[] =
    {
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_GetInfo, 1, 0, &node::essential::uavcan_node_GetInfo_1_0_handler,
                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_ExecuteCommand, 1, 1,
                                      &uavcan_node_ExecuteCommand_Request_1_1_handler,
                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_register_Access, 1, 0,
                                      &node::essential::uavcan_register_Access_1_0_handler,
                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_register_List, 1, 0,
                                      &node::essential::uavcan_register_List_1_0_handler,
                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC),
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(note_response, reg_udral_physics_acoustics_Note,
                                             0, 1,
                                             &reg_udral_physics_acoustics_Note_0_1_handler,
                                             CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC),
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(setpoint, reg_udral_service_actuator_common_sp_Vector31,
                                             0, 1,
                                             &setpoint_handler, 90000),
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(readiness, reg_udral_service_common_Readiness,
                                             0, 1,
                                             &sub_readiness_handler, CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC)
    };

// A pointer can be considered an iterator
std::pair<AnySubscription *, AnySubscription *> get_subscription_iterators()
{
    return {
        std::begin(registered_ports), std::end(registered_ports)
    };
}


bool is_port_configurable(AnySubscription &reg)
{
    return reg.subscription.port_id == CONFIGURABLE_SUBJECT_ID;
}
