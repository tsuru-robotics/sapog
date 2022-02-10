/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "libcanard/canard.h"

struct AnySubscription
{
    const char *type;
    const char *name;
    CanardTransferKind transfer_kind;
    CanardRxSubscription subscription;
};

// This pair stores two pointers to iterators (an iterator is a pointer in implementation details), for start and end of
// the subscriptions array
extern std::pair<AnySubscription *, AnySubscription *> get_subscription_iterators();

bool is_port_configurable(AnySubscription &reg);
