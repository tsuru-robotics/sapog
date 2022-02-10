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

#include "led.hpp"
#include <hal.h>
#include <assert.h>
#include <zubax_chibios/os.hpp>
#include <algorithm>

#undef TIM1
#undef TIM2
#undef TIM4
#undef TIM5
#undef TIM6
#undef TIM7

#define GLUE2_(A, B)     A##B
#define GLUE2(A, B)      GLUE2_(A, B)
#define GLUE3_(A, B, C)  A##B##C
#define GLUE3(A, B, C)   GLUE3_(A, B, C)

/**
 * Timer declaration
 */
#define TIMER_NUMBER   3

#define TIMX            GLUE2(TIM, TIMER_NUMBER)

#if TIMER_NUMBER < 2 || TIMER_NUMBER > 7
#  error "Invalid timer number"
#else
#  define TIMX_RCC_ENR          RCC->APB1ENR
#  define TIMX_RCC_RSTR         RCC->APB1RSTR
#  define TIMX_RCC_ENR_MASK     GLUE3(RCC_APB1ENR_TIM,  TIMER_NUMBER, EN)
#  define TIMX_RCC_RSTR_MASK    GLUE3(RCC_APB1RSTR_TIM, TIMER_NUMBER, RST)
#  define TIMX_INPUT_CLOCK      STM32_TIMCLK1
#endif

namespace board
{

/*
 * Static functions
 */
void init_led()
{
    chSysDisable();

    // Power-on and reset
    TIMX_RCC_ENR |= TIMX_RCC_ENR_MASK;
    TIMX_RCC_RSTR |= TIMX_RCC_RSTR_MASK;
    TIMX_RCC_RSTR &= ~TIMX_RCC_RSTR_MASK;

    chSysEnable();

    TIMX->ARR = 0xFFFF;
    TIMX->CR1 = 0;
    TIMX->CR2 = 0;

    // CC1, CC2, CC3 are R, G, B. Inverted mode.
    TIMX->CCMR1 =
        TIM_CCMR1_OC1M_2 | TIM_CCMR1_OC1M_1 |
        TIM_CCMR1_OC2M_2 | TIM_CCMR1_OC2M_1;

    TIMX->CCMR2 =
        TIM_CCMR2_OC3M_2 | TIM_CCMR2_OC3M_1;

    // All enabled, all inverted.
    // TODO: Pixhawk ESC v1.4b reqiuires non-inverted outputs; make it optional depending on the HW version?
    TIMX->CCER =
        TIM_CCER_CC3E | TIM_CCER_CC2E | TIM_CCER_CC1E |
        TIM_CCER_CC3P | TIM_CCER_CC2P | TIM_CCER_CC1P;

    // Start
    TIMX->EGR = TIM_EGR_UG | TIM_EGR_COMG;
    TIMX->CR1 |= TIM_CR1_CEN;
}

static void set_hex_impl(std::uint32_t hex_rgb)
{
    hex_rgb &= 0xFFFFFFU;
    const unsigned pwm_red = ((hex_rgb & 0xFF0000U) >> 16) * 257U;
    const unsigned pwm_green = ((hex_rgb & 0x00FF00U) >> 8) * 257U;
    const unsigned pwm_blue = ((hex_rgb & 0x0000FFU) >> 0) * 257U;

    TIMX->CCR1 = pwm_red;
    TIMX->CCR2 = pwm_green;    // On Pixhawk ESC v1.4b this is BLUE
    TIMX->CCR3 = pwm_blue;     // On Pixhawk ESC v1.4b this is GREEN
}

void led_emergency_override(LEDColor color)
{
    set_hex_impl(unsigned(color));
}

/*
 * LEDOverlay
 */
LEDOverlay *LEDOverlay::layers[MAX_LAYERS] = {};
chibios_rt::Mutex LEDOverlay::mutex;

void LEDOverlay::set_hex_rgb(std::uint32_t hex_rgb)
{
    os::MutexLocker mlock(mutex);

    color = hex_rgb;

    // Checking if this layer is registered
    int position = -1;
    for (int i = 0; i < MAX_LAYERS; i++)
    {
        if (layers[i] == this)
        {
            position = i;
            break;
        }
    }

    // Not registered - fixing
    if (position < 0)
    {
        for (int i = 0; i < MAX_LAYERS; i++)
        {
            if (layers[i] == nullptr)
            {
                position = i;
                layers[i] = this;
//				os::lowsyslog("LED: 0x%08x registered at pos %d\n",
//				            reinterpret_cast<unsigned>(this), position);
                break;
            }
        }
    }

    // Failed to register - ignore the command
    if (position < 0)
    {
        os::lowsyslog("LED: 0x%08x failed to register\n", reinterpret_cast<unsigned>(this));
        return;
    }

    // Checking if we're at the top
    if ((position >= (MAX_LAYERS - 1)) || (layers[position + 1] == nullptr))
    {
        set_hex_impl(color);
    }
}

void LEDOverlay::unset()
{
    os::MutexLocker mlock(mutex);

    // Removing ourselves from the list
    for (int i = 0; i < MAX_LAYERS; i++)
    {
        if (layers[i] == this)
        {
            layers[i] = nullptr;
            os::lowsyslog("LED: 0x%08x unregistered from pos %d\n", reinterpret_cast<unsigned>(this), i);
            break;
        }
    }

    // Defragmenting the list
    LEDOverlay *new_layers[MAX_LAYERS] = {};
    for (int src = 0, dst = 0; src < MAX_LAYERS; src++)
    {
        if (layers[src] != nullptr)
        {
            new_layers[dst++] = layers[src];
        }
    }
    std::copy_n(new_layers, MAX_LAYERS, layers);

    // Activating the last item
    for (int i = (MAX_LAYERS - 1); i >= 0; i--)
    {
        if (layers[i] != nullptr)
        {
            os::lowsyslog("LED: 0x%08x reactivated at pos %d\n", reinterpret_cast<unsigned>(layers[i]), i);
            set_hex_impl(layers[i]->color);
            break;
        }
    }
}

}
