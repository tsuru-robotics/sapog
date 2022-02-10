/****************************************************************************
 *
 *   Copyright (C) 2014 PX4 Development Team. All rights reserved.
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

// TODO: rewrite in C++

#include "pwm_input.hpp"
#include <ch.h>
#include <hal.h>
#include <stdio.h>
#include <stdlib.h>
#include <zubax_chibios/os.hpp>
#include <motor/motor.hpp>
#include <assert.h>

static const unsigned MIN_VALID_PULSE_WIDTH_USEC = 500;
static const unsigned MAX_VALID_PULSE_WIDTH_USEC = 3000;

static const float STOP_DUTY_CYCLE = 0.03;
static const float START_MIN_DUTY_CYCLE = 0.06;
static const float START_MAX_DUTY_CYCLE = 0.40;

static const unsigned COMMAND_TTL_MS = 100;


chibios_rt::EvtSource _update_event;

static volatile unsigned _last_pulse_width_usec;

static os::Logger g_logger{"RCPWM"};

CONFIG_PARAM_BOOL("pwm_enable", false)

CONFIG_PARAM_INT("pwm_min_usec", 1000, 800, 1200)

CONFIG_PARAM_INT("pwm_max_usec", 2000, 1800, 2200)


static void icu_pulse_width_callback(ICUDriver *icup)
{
    const unsigned new_width = icuGetWidthX(icup);

    if ((new_width >= MIN_VALID_PULSE_WIDTH_USEC) && (new_width <= MAX_VALID_PULSE_WIDTH_USEC))
    {
        _last_pulse_width_usec = new_width;

        chSysLockFromISR();
        chEvtBroadcastFlagsI(&_update_event.ev_source, ALL_EVENTS);      // TODO: use C++ API
        chSysUnlockFromISR();
    }
}

static void icu_period_callback(ICUDriver *icup)
{
    (void) icup;
    /*
     * Nothing to do here.
     * This handler is required by the ICU driver, see the link:
     * http://forum.chibios.org/phpbb/viewtopic.php?f=3&t=2078
     */
}

static void thread(void *)
{
    event_listener_t listener;
    chEvtRegisterMask(&_update_event.ev_source, &listener, ALL_EVENTS);  // TODO: use C++ API

    const unsigned min_pulse_width_usec = configGet("pwm_min_usec");
    const unsigned max_pulse_width_usec = configGet("pwm_max_usec");

    g_logger.println("Started");

    while (!os::isRebootRequested())
    {
        if (chEvtWaitAnyTimeout(ALL_EVENTS, US2ST(65536)) == 0)
        {
            if (_last_pulse_width_usec > 0)
            {
                g_logger.println("Timeout");
                // We don't stop the motor here - it will be stopped automatically when TTL has expired
            }
            _last_pulse_width_usec = 0;
            continue;
        }

        /*
         * Scale the input signal into [0, 1]
         */
        unsigned local_copy = _last_pulse_width_usec;
        if (local_copy < min_pulse_width_usec)
        {
            local_copy = min_pulse_width_usec;
        }
        if (local_copy > max_pulse_width_usec)
        {
            local_copy = max_pulse_width_usec;
        }

        float dc = (local_copy - min_pulse_width_usec) / (float) (max_pulse_width_usec - min_pulse_width_usec);
        assert(dc >= 0);
        assert(dc <= 1);

        /*
         * Handle start/stop corner cases
         */
        if (motor_is_idle() && ((dc < START_MIN_DUTY_CYCLE) || (dc > START_MAX_DUTY_CYCLE)))
        {
            dc = 0;
        } else if (dc < STOP_DUTY_CYCLE)
        {
            dc = 0;
        } else
        { ; // Nothing to do
        }

        /*
         * Pass the new command into the motor controller
         */
        if (dc > 0)
        {
            motor_set_duty_cycle(dc, COMMAND_TTL_MS);
        } else
        {
            motor_stop();
        }
    }

    g_logger.println("Going down");
}

void pwm_input_init(void)
{
    assert(STOP_DUTY_CYCLE < START_MIN_DUTY_CYCLE);
    assert(START_MIN_DUTY_CYCLE < START_MAX_DUTY_CYCLE);

    if (!configGet("pwm_enable"))
    {
//		g_logger.println("Disabled");
        return;
    }

    static THD_WORKING_AREA(_wa_thread, 1024);
    if (!chThdCreateStatic(_wa_thread, sizeof(_wa_thread), NORMALPRIO, thread, NULL))
    {
        abort();
    }

    static ICUConfig icucfg = {
        ICU_INPUT_ACTIVE_HIGH,
        1000000,
        icu_pulse_width_callback,
        icu_period_callback,       // Required even if not used
        NULL,
        ICU_CHANNEL_1,
        0
    };

    icuStart(&ICUD5, &icucfg);
    icuStartCapture(&ICUD5);
    icuEnableNotifications(&ICUD5);
}
