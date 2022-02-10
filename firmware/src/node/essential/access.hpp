/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include "src/node/state/state.hpp"
#include "../../../generated/nunavut_out/uavcan/_register/Access_1_0.h"

/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <uavcan/_register/Access_1_0.h>
#include <node/units.hpp>
#include <node/time.h>
#include <cstdio>
#include <node/conf/wrapper.hpp>
#include <node/interfaces/IHandler.hpp>
#include <uavcan/primitive/scalar/Natural16_1_0.h>
#include <string_view>

#pragma once

std::string_view find_type_name(std::string_view request_name);

struct RegisterCriteria
{
    bool _mutable;
    bool persistent;
};

RegisterCriteria get_response_value(std::string_view
                                    request_name,
                                    uavcan_register_Value_1_0 &out_value);


bool respond_to_access(node::state::State &state, std::basic_string_view<char> request_name,
                       const CanardRxTransfer *const transfer);



