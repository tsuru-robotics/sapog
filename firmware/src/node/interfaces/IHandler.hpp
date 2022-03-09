/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "src/node/state/state.hpp"

/*!
 * ILoopMethod is an interface that is used by handlers that are being called in the main loop of this firmware.
 * These handlers handle different loops. Each loop has its own delay for when it runs. The delays of the loops can be
 * modified.
 */
class ILoopMethod
{
public:
    ILoopMethod()
    {}

    virtual ~ILoopMethod()
    {}

    virtual void operator()(node::state::State &state) = 0;
};

class IStateAwareHandler
{
public:
    node::state::State *state;

    IStateAwareHandler()
    {}

    virtual ~IStateAwareHandler()
    {}

    virtual void operator()(node::state::State *state) = 0;
};

class IHandler
{
public:
    IHandler()
    {}

    virtual ~IHandler()
    {}

    virtual void operator()(node::state::State &state, CanardRxTransfer *transfer) = 0;
};
