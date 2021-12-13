/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "src/node/state/state.hpp"

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
