/****************************************************************************
 *
 *   Copyright (C) 2016 PX4 Development Team. All rights reserved.
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

#include <temperature_sensor.hpp>
#include <zubax_chibios/os.hpp>
#include <board/board.hpp>
#include <motor/motor.hpp>
#include <unistd.h>
#include <limits>
#include <algorithm>
#include <cstdio>

namespace temperature_sensor
{
namespace
{
static constexpr auto max_number_of_sensors = 3;
std::array<std::optional<unsigned>, max_number_of_sensors> sensor_addresses;
std::array<std::optional<std::int16_t>, max_number_of_sensors> temperatures;
static constexpr std::int16_t KELVIN_OFFSET = 273;
int available_temperature_sensors;


bool functional = false;

std::int16_t convert_lm75b_to_kelvin(const std::array<std::uint8_t, 2> &raw)
{
    auto x = std::int16_t((std::uint16_t(raw[0]) << 8) | raw[1]) >> 5;
    if (x & (1U << 10))
    {
        x |= 0xFC00;
    }
    return x / 8 + KELVIN_OFFSET;
}

std::array<std::optional<std::int16_t>, max_number_of_sensors> try_read()
{
    std::array<std::optional<std::int16_t>, max_number_of_sensors> result{};
    int count = 0;
    for (auto &sensor_address: sensor_addresses)
    {
        const std::array<std::uint8_t, 1> tx = {0};
        std::array<std::uint8_t, 2> rx;
        if (sensor_address.has_value())
        {
            int retry_count = 0;
            while (retry_count < 3)
            {
                if (board::i2c_exchange(sensor_address.value(), tx, rx) == 0)
                {
                    result[count] = convert_lm75b_to_kelvin(rx);
                    break;
                } else
                {
                    retry_count++;
                }
            }

        } else
        {
            result[count] = {};
        }
        count++;
    }
    return result;
}


std::optional<std::int16_t> read_maximum_temperature()
{
    std::int16_t current_maximum = -32768;
    for (auto &temperature: try_read())
    {
        if (temperature.has_value() && temperature > current_maximum)
        {
            current_maximum = temperature.value();
        }
    }
    if (current_maximum <= 0)
    {
        return {};
    } else
    {
        return current_maximum;
    }
}

class : public chibios_rt::BaseStaticThread<128>
{
    void main() override
    {
        os::watchdog::Timer wdt;
        wdt.startMSec(2000);
        setName("tempsens");

        while (!os::isRebootRequested())
        {
            wdt.reset();
            ::usleep(500 * 1000);

            if (!motor_is_running() && !motor_is_idle())
            {
                // When the motor is starting, I2C goes bananas
                continue;
            }
            for (auto &new_temp: try_read())
            {
                if (new_temp.has_value() && new_temp.value() >= 0)
                {
//                    temperature = std::int16_t((std::int32_t(temperature) * 7 + new_temp.value() + 7) / 8);
                    functional = true;
                } else
                {
                    functional = false;
                }
            }

        }
    }
} thread_;

}

int init()
{
    printf("\nHardware minor version: %d\n", board::detect_hardware_version().minor);
    switch (board::detect_hardware_version().minor)
    {
        case 0:
        case 1:
        case 2: // Sapog Reference, Sapog, Kotleta
            sensor_addresses[0] = 0b1001000;
            sensor_addresses[1] = {};
            sensor_addresses[2] = {};
            available_temperature_sensors = 1;
            printf("Kotleta detected.\n");
            break;
        case 3: // Valenok
            sensor_addresses[0] = 0b1001000;
            sensor_addresses[1] = 0b1001001;
            sensor_addresses[2] = 0b1001011;
            available_temperature_sensors = 3;
            break;
        default:
            board::die(0);
    }
    temperatures = try_read();
    int counted_functioning_temperature_sensors = 0;
    for (auto &temperature: temperatures)
    {
        if (temperature.has_value())
        {
            counted_functioning_temperature_sensors++;
        }
    }
    if (counted_functioning_temperature_sensors != available_temperature_sensors)
    {
        return -1;
    }
    assert(counted_functioning_temperature_sensors == available_temperature_sensors);
    thread_.start(LOWPRIO);
    return 0;
}

bool is_ok()
{
    return functional;
}

std::int16_t get_temperature_K()
{
    return read_maximum_temperature().value_or(0);
}

}
