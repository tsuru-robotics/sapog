/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <zubax_chibios/config/config.hpp>
#include <libcanard/canard.h>

#define CONFIGURABLE_ID_IN_ESC_GROUP 0xFFFF
#define CONFIGURABLE_SUBJECT_ID 0xFFFF
namespace node::state
{
struct Timing
{
    CanardMicrosecond next_pnp_request;
    CanardMicrosecond started_at;
    CanardMicrosecond current_time;
};
struct TransferIds
{
    uint64_t uavcan_node_heartbeat;
    uint64_t uavcan_node_port_list;
    uint64_t uavcan_pnp_allocation;
};
enum class PNPStatus
{
    Subscribing,
    TryingToSend,
    SentRequest,
    ReceivedResponse,
    Done
};
enum class Readiness
{
    SLEEP = 0,
    STANDBY = 2,
    ENGAGED = 3
};
enum class Health
{
    NOMINAL = 0,
    ADVISORY = 1,
    CAUTION = 2,
    WARNING = 3
};
enum class ControlMode
{
    RPM,
    DUTYCYCLE
};
struct PlugAndPlay
{
    int request_count = 0;
    uint64_t unique_id_hash;
    PNPStatus status = PNPStatus::Subscribing;
    bool anonymous = true;
};
struct State
{
    bool is_restart_required = false;
    Timing timing;
    TransferIds transfer_ids;
    PlugAndPlay plug_and_play;
    CanardInstance canard;
    bool is_save_requested = false;
    CanardTxQueue queues[BXCAN_MAX_IFACE_INDEX + 1];
    Readiness readiness;
    Health health;
    uint16_t id_in_esc_group;
    uint16_t esc_heartbeat_publish_port;
    uint16_t esc_feedback_publish_port;
    ControlMode control_mode;
    uint16_t ttl_milliseconds;
};
}
