/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include <node/interfaces/IHandler.hpp>
#include "node/pnp.hpp"
#include "node/time.h"
#include "state.hpp"
#include "publishers.hpp"
#include "reception.hpp"
#include "node/essential/heartbeat.hpp"
#include "node/essential/port_list.hpp"


namespace node::loops
{
struct : ILoopMethod
{
    void operator()(node::state::State &state)
    {
        node::essential::publish_heartbeat(state.canard, state);
        transmit(state);
        // Before code below is uncommented, make sure that the node has an id.
        // communications::publish_port_list(state.canard, state);
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

        auto transfer = receive_transfer(state, 0);
        if (transfer.first.has_value())
        {
            palWritePad(GPIOC, 11, 0);
            static_cast<IHandler *>(transfer.second->subscription.user_reference)->operator()(state,
                                                                                              &transfer.first.value());
            palWritePad(GPIOC, 11, 1);
            //process_received_transfer(state, &transfer.value());
        }
        transmit(state);
    }
} handle_fast_loop;
}