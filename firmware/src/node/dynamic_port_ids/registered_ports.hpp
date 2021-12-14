/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "libcanard/canard.h"

struct RegisteredPort
{
  // uavcan.pub.PORT_NAME.id
  const char *type;  // uavcan.pub.PORT_NAME.type
  const char *name;
  CanardTransferKind transfer_kind;
  CanardRxSubscription subscription;
};

template<size_t N>
extern inline std::pair<RegisteredPort *, RegisteredPort *> get_ports_info_iterators();