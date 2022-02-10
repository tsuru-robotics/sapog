/****************************************************************************
 *
 *   Copyright (C) 2013 PX4 Development Team. All rights reserved.
 *   Author: Pavel Kirienko <pavel.kirienko@gmail.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name PX4 nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************/

#include "rpmctl.h"
#include <zubax_chibios/config/config.h>
#include <math.h>
#include <assert.h>


static struct state
{
    float integrated;
    float prev_error;
} _state;

static struct params
{
    float p;
    float d;
    float i;
} _params;


CONFIG_PARAM_FLOAT("rpmctl_p", 0.0001, 0.0, 1.0)

CONFIG_PARAM_FLOAT("rpmctl_d", 0.0, 0.0, 1.0)

CONFIG_PARAM_FLOAT("rpmctl_i", 0.001, 0.0, 10.0)


int rpmctl_init(void)
{
    _params.p = configGet("rpmctl_p");
    _params.d = configGet("rpmctl_d");
    _params.i = configGet("rpmctl_i");
    return 0;
}

void rpmctl_reset(void)
{
    _state.integrated = 0.0;
    _state.prev_error = nan("");
}

float rpmctl_update(const struct rpmctl_input *input)
{
    const float error = input->sp - input->pv;
    assert(isfinite(error));

    if (!isfinite(_state.prev_error))
    {
        _state.prev_error = error;
    }

    const float p = error * _params.p;
    const float i = _state.integrated + error * input->dt * _params.i;
    const float d = ((error - _state.prev_error) / input->dt) * _params.d;

    _state.prev_error = error;

    float output = p + i + d;
    if (output > 1.0)
    {
        output = 1.0;
    } else if (output < -1.0)
    {
        output = -1.0;
    } else if (input->limit_mask == 0)
    {
        _state.integrated = i;
    }
    return output;
}
