/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "node/state/state.hpp"
#include <string_view>

struct PublishConfigurablePort
{
  std::string_view name;
  uint16_t *state_variable;
};

extern inline std::pair<PublishConfigurablePort *, PublishConfigurablePort *> get_publish_port_iterators();