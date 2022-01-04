/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "node/state/state.hpp"

CONFIG_PARAM_INT("uavcan.pub.esc_heartbeat.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.feedback.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.power.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.dynamics.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.status.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.sub.readiness.id", CONFIGURABLE_ID_IN_ESC_GROUP, 0, CONFIGURABLE_ID_IN_ESC_GROUP)

CONFIG_PARAM_INT("uavcan.sub.note_response.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.sub.setpoint.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("control_mode_rpm", 1, 0, 1)

CONFIG_PARAM_INT("id_in_esc_group", 255, 0, 255)

CONFIG_PARAM_INT("ttl_milliseconds", 10, 0, 500)