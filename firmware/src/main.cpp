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

#include <ch.h>
#include <cmath>
#include <board/board.hpp>
#include <board/led.hpp>
#include <console.hpp>
#include <pwm_input.hpp>
#include <temperature_sensor.hpp>
#include <motor/motor.hpp>
#include <cstring>
#include <sys/unistd.h>
#include "node/uavcan_thread.hpp"
#include "node/BackgroundConfigManager.hpp"
#include <stdio.h>

namespace
{

static constexpr unsigned WATCHDOG_TIMEOUT = 10000;

board::LEDOverlay led_ctl;

os::watchdog::Timer init()
{
    auto wdt = board::init(WATCHDOG_TIMEOUT);

    led_ctl.set(board::LEDColor::PALE_WHITE);

    // Temperature sensor
    int res = temperature_sensor::init();
    if (res < 0)
    {
        os::lowsyslog("Failed to init temperature sensor\n");
        board::die(res);
    }

    // Motor control (must be initialized earlier than communicaton interfaces)
    res = motor_init(board::get_current_shunt_resistance());
    if (res < 0)
    {
        board::die(res);
    }

    // PWM input
    pwm_input_init();

    // Self test
    res = motor_test_hardware();
    if (res != 0)
    {
        board::die(res);
    }

    if (motor_test_motor())
    {
        os::lowsyslog("Motor is not connected or damaged\n");
    }

    // Initializing console after delay to ensure that CLI is flushed
    chThdSleepMilliseconds(300);
    console_init();

    return wdt;
}

[[maybe_unused]] void do_startup_beep()
{
    // Valenok should not do the startup beep, it is dangerous, apparently.
    if (board::detect_hardware_version().minor == 3)
    {
        return;
    }
    motor_beep(1000, 100);
    chThdSleepMilliseconds(200);
    motor_beep(1000, 100);
}


}

namespace os
{

void applicationHaltHook()
{
    motor_emergency();
    board::led_emergency_override(board::LEDColor::RED);
}

}

int main()
{
    auto wdt = init();
    chThdSetPriority(NORMALPRIO);

//    do_startup_beep();

    motor_confirm_initialization();
    printf("\n\n\n\nBooted\n");

    /*
     * Here we run some high-level self diagnostics, indicating the system health via UAVCAN and LED.
     * TODO: Refactor.
     * TODO: Report status flags via vendor-specific status field.
     */
    BackgroundConfigManager bg_config_manager;
    uavcan_node_1_0::init();
    while (!os::isRebootRequested())
    {
        wdt.reset();

        if (motor_is_blocked())
        {
            led_ctl.set(board::LEDColor::YELLOW);
            printf("Motor is blocked!\n");
        } else
        {
            led_ctl.set(board::LEDColor::DARK_GREEN);
        }

        //bg_config_manager.poll();
        chThdSleepMilliseconds(500);
    }
    chThdSleepMilliseconds(100);
    motor_stop();
    board::reboot();
    return 0;
}


#define MATCH_GCC_VERSION(major, minor)  \
    ((__GNUC__ == (major)) && (__GNUC_MINOR__ == (minor)))

#if !(MATCH_GCC_VERSION(10, 3))
# error "This compiler is not supported"
#endif
