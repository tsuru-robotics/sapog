/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "node/state/state.hpp"

CONFIG_PARAM_INT("uavcan.pub.feedback.id", CONFIGURABLE_SUBJECT_ID, -1, 6143)

CONFIG_PARAM_INT("uavcan.pub.power.id", CONFIGURABLE_SUBJECT_ID, -1, 6143)

CONFIG_PARAM_INT("uavcan.pub.dynamics.id", CONFIGURABLE_SUBJECT_ID, -1, 6143)

CONFIG_PARAM_INT("uavcan.pub.status.id", CONFIGURABLE_SUBJECT_ID, -1, 6143)

CONFIG_PARAM_INT("uavcan.sub.readiness.id", CONFIGURABLE_ID_IN_ESC_GROUP, -1, 6143)

CONFIG_PARAM_INT("uavcan.sub.note_response.id", CONFIGURABLE_SUBJECT_ID, -1, 6143)

CONFIG_PARAM_INT("uavcan.sub.setpoint.id", CONFIGURABLE_SUBJECT_ID, -1, 6143)

CONFIG_PARAM_BOOL("control_mode_rpm", true)

CONFIG_PARAM_INT("id_in_esc_group", 255, 0, 255)

CONFIG_PARAM_INT("ttl_milliseconds", 10, 0, 500)