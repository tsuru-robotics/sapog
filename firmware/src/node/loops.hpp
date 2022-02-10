/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include <node/interfaces/IHandler.hpp>
#include <node/esc/esc_publishers.hpp>
#include "node/pnp.hpp"
#include "node/time.h"
#include "src/node/state/state.hpp"
#include "publishers.hpp"
#include "reception.hpp"
#include "node/essential/heartbeat.hpp"
#include "node/essential/port_list.hpp"
#include "node/esc/esc_publishers.hpp"
#include "node/esc/esc_publishers.hpp"
#include "node/loops/loop.hpp"


namespace node::loops
{


struct : ILoopMethod
{
    void operator()(node::state::State &state)
    {
        node::essential::publish_heartbeat(state.canard, state);
        publish_esc_feedback(state);
        transmit(state);
    }
} handle_1hz_loop;

struct : ILoopMethod
{
    void operator()(node::state::State &state)
    {
        publish_port_list(state.canard, state);
        transmit(state);
    }
} handle_5_second_loop;

struct : ILoopMethod
{
    void operator()(node::state::State &state)
    {
        publish_esc_status(state);
        transmit(state);
    }
} handle_esc_status_loop;

struct : ILoopMethod
{
    void operator()(node::state::State &state)
    {
        accept_transfers(state);
        transmit(state);
    }
} handle_fast_loop;

Loop loops[]{Loop{handle_1hz_loop, SECOND_IN_MICROSECONDS},
             Loop{handle_fast_loop, QUEUE_TIME_FRAME},
             Loop{handle_5_second_loop, SECOND_IN_MICROSECONDS * 5},
             Loop{handle_esc_status_loop, SECOND_IN_MICROSECONDS / 10}
};
}