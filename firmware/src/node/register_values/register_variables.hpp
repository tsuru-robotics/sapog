/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "node/state/state.hpp"
#include <string_view>

// An integer only state variable that is stored in a register and retrieved at startup
struct IntStateVariableInRegister
{
  std::string_view name;
  uint16_t *state_variable;
};

extern std::pair<IntStateVariableInRegister *, IntStateVariableInRegister *> get_publish_port_iterators();

extern std::pair<IntStateVariableInRegister *, IntStateVariableInRegister *> get_state_variables_in_registers();
