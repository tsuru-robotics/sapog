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

#include <board/board.hpp>
#include <cstring>
#include <unistd.h>
#include <zubax_chibios/util/software_i2c.hpp>
#include <zubax_chibios/platform/stm32/flash_writer.hpp>
#include <zubax_chibios/platform/stm32/config_storage.hpp>
#include <board/unique_id.h>
#include <cstdio>
#include "o1heap/o1heap.h"
#include "motor/realtime/adc.h"

extern "C" void _unhandled_exception()
{
    os::applicationHaltHook();
}
// Clock config validation
#if STM32_PREDIV1_VALUE != 2
# error STM32_PREDIV1_VALUE
#endif
#if STM32_SYSCLK != 72000000
# error STM32_SYSCLK
#endif
#if STM32_PCLK2 != 72000000
# error STM32_PCLK2
#endif

// Defines GPIO configuration after boot up; see os_config/board.h
const PALConfig pal_default_config = {
    {VAL_GPIOAODR, VAL_GPIOACRL, VAL_GPIOACRH},
    {VAL_GPIOBODR, VAL_GPIOBCRL, VAL_GPIOBCRH},
    {VAL_GPIOCODR, VAL_GPIOCCRL, VAL_GPIOCCRH},
    {VAL_GPIODODR, VAL_GPIODCRL, VAL_GPIODCRH},
    {VAL_GPIOEODR, VAL_GPIOECRL, VAL_GPIOECRH}
};

/// Provided by linker
const extern std::uint8_t DeviceSignatureStorage[];
static O1HeapInstance *o1_heap_instance;
namespace board
{

static syssts_t g_heap_irq_status_{};  // NOLINT

void heapLock()
{
    g_heap_irq_status_ = chSysGetStatusAndLockX();
}

void heapUnlock()
{
    chSysRestoreStatusX(g_heap_irq_status_);
}

void *allocate(std::size_t sz)
{
    return o1heapAllocate(o1_heap_instance, sz);
}

void deallocate(const void *ptr)
{
    o1heapFree(o1_heap_instance, const_cast<void *>(ptr));
}

// This can't be constexpr because of reinterpret_cast<>
static void *const ConfigStorageAddress = reinterpret_cast<void *>(0x08000000 + (256 * 1024) - 1024);
constexpr unsigned ConfigStorageSize = 1024;

extern void init_led();

std::optional<os::stm32::ConfigStorageBackend> config_storage_backend;
CONFIG_PARAM_INT("uavcan.node.id", 127, 0, 127)

os::watchdog::Timer init(unsigned watchdog_timeout_ms)
{
    // OS
    halInit();
    chSysInit();
    // Watchdog - initializing as soon as possible
    os::watchdog::init();
    os::watchdog::Timer wdt;
    wdt.startMSec(watchdog_timeout_ms);

    // CLI
    sdStart(&STDOUT_SD, NULL);

    // LED
    init_led();

    // Config
    config_storage_backend.emplace(os::stm32::ConfigStorageBackend(ConfigStorageAddress, ConfigStorageSize));
    const int config_init_res = os::config::init(&config_storage_backend.value());
    if (config_init_res < 0)
    {
        die(config_init_res);
    }
    // Heap init
    // Banner
//    const auto hw_version = detect_hardware_version();
//    os::lowsyslog("%s %u.%u %u.%u / %d %s\n",
//                  NODE_NAME,
//                  hw_version.major, hw_version.minor,
//                  FW_VERSION_MAJOR, FW_VERSION_MINOR, config_init_res,
//                  os::watchdog::wasLastResetTriggeredByWatchdog() ? "WDTRESET" : "OK");
    o1_heap_instance = o1heapInit(&::board::__heap_base__,
                                  reinterpret_cast<std::size_t>(&__heap_end__) -
                                  reinterpret_cast<std::size_t>(&__heap_base__),  // NOLINT
                                  &heapLock,
                                  &heapUnlock);
    if (o1_heap_instance == nullptr)
    {
        printf("o1heap failed to initialize\n");
        chibios_rt::System::halt("o1heap");
    }


    return wdt;
}


int i2c_exchange(std::uint8_t address,
                 const void *tx_data, const std::uint16_t tx_size,
                 void *rx_data, const std::uint16_t rx_size)
{
    static chibios_rt::Mutex mutex;
    os::MutexLocker mlock(mutex);
    return -int(os::software_i2c::Master(GPIO_PORT_I2C_SCL, GPIO_PIN_I2C_SCL,
                                         GPIO_PORT_I2C_SDA, GPIO_PIN_I2C_SDA)\
.exchange(address, tx_data, tx_size,
          rx_data, rx_size));
}

void i2c_reset()
{
    static chibios_rt::Mutex mutex;
    os::MutexLocker mlock(mutex);
    os::software_i2c::Master(GPIO_PORT_I2C_SCL, GPIO_PIN_I2C_SCL,
                             GPIO_PORT_I2C_SDA, GPIO_PIN_I2C_SDA).reset();
}

void die(int error)
{
    os::lowsyslog("FATAL ERROR %d\n", error);
    while (1)
    {
        led_emergency_override(LEDColor::RED);
        ::sleep(1);
    }
}

void reboot()
{
    NVIC_SystemReset();
}

HardwareVersion detect_hardware_version()
{
    auto v = HardwareVersion();

    v.major = HW_VERSION_MAJOR;
    v.minor = std::uint8_t(GPIOC->IDR & 0x0F);

    return v;
}

int get_max_can_interface_index()
{
    switch (detect_hardware_version().minor)
    {
        case 0:
            return 0;
        case 1:
            return 1;
        case 2:
            return 0;
        case 3:
            return 1;
    }
    assert(false);
    return 0;
}

float get_current_shunt_resistance()
{
    switch (detect_hardware_version().minor)
    {
        case 0:                // Sapog Reference Hardware
        case 1:                // Zubax Orel
        {
            return 5e-3F;
        }
        case 2:                // Kotleta
        {
            return 1e-3F;
        }
        case 3:
        {
            return 2e-4F; // 200 micro Ohms
        }
        default:
        {
            die(0);
            return 0.0F;
        }
    }
}

bool try_read_device_signature(DeviceSignature &out_sign)
{
    std::memcpy(out_sign.data(), &DeviceSignatureStorage[0], std::tuple_size<DeviceSignature>::value);

    return std::any_of(out_sign.begin(), out_sign.end(), [](auto x) { return x != 0xFF && x != 0x00; });
}

bool try_write_device_signature(const DeviceSignature &sign)
{
    {
        DeviceSignature dummy;
        if (try_read_device_signature(dummy))
        {
            return false;               // Already written
        }
    }

    // Before flash can be written, the source must be aligned.
    alignas(4) std::uint8_t aligned_buffer[std::tuple_size<DeviceSignature>::value];
    std::copy(std::begin(sign), std::end(sign), std::begin(aligned_buffer));

    os::stm32::FlashWriter writer;

    return writer.write(&DeviceSignatureStorage[0], &aligned_buffer[0], sizeof(aligned_buffer));
}

}

extern "C"
{
float motor_adc_convert_input_voltage(int raw)
{
    static float top_resistance = 10.0F;
    static float bottom_resistance = 1.3F;
    switch (board::detect_hardware_version().minor)
    {
        case 0:                // Sapog Reference Hardware
        case 1:                // Zubax Orel
        case 2:                // Kotleta
        {
            top_resistance = 10.0F * 1000;
            bottom_resistance = 1.3F * 1000;
            break;
        }
        case 3:                // Valenok
        {
            top_resistance = 110.0F * 1000;
            bottom_resistance = 3.3F * 1000;
            break;
        }
        default:
        {
            board::die(0);
        }
    }
    static const float SCALE = (top_resistance + bottom_resistance) / bottom_resistance;
    const float unscaled = raw * (ADC_REF_VOLTAGE / (float) (1 << ADC_RESOLUTION));
    return unscaled * SCALE;
}

float motor_adc_convert_input_current(int raw)
{
    // http://www.diodes.com/datasheets/ZXCT1051.pdf
    int gain = 10;
    switch (board::detect_hardware_version().minor)
    {
        case 0:                // Sapog Reference Hardware
        case 1:                // Zubax Orel
        case 2:                // Kotleta
        {
            gain = 10;
            break;
        }
        case 3:                // Valenok
        {
            gain = 50;
            break;
        }
        default:
        {
            board::die(0);
        }
    }
    const float vout = raw * (ADC_REF_VOLTAGE / (float) (1 << ADC_RESOLUTION));
    const float vsense = vout / gain;
    const float iload = vsense / board::get_current_shunt_resistance();
    return iload;
}

/// Called from ChibiOS init
void __early_init()
{
    stm32_clock_init();
    // Making sure LSI is up and running
    while ((RCC->CSR & RCC_CSR_LSIRDY) == 0);
}

/// Called from ChibiOS init
void boardInit()
{
    uint32_t mapr = AFIO->MAPR;
    mapr &= ~AFIO_MAPR_SWJ_CFG; // these bits are write-only

    // Enable SWJ only, JTAG is not needed at all:
    mapr |= AFIO_MAPR_SWJ_CFG_JTAGDISABLE;

    // TIM1 - motor control
    mapr |= AFIO_MAPR_TIM1_REMAP_0;

    // Serial CLI
    mapr |= AFIO_MAPR_USART1_REMAP;

    // TIM3 - RGB LED PWM
    mapr |= AFIO_MAPR_TIM3_REMAP_FULLREMAP;

    AFIO->MAPR = mapr;
}

} // extern "C"
