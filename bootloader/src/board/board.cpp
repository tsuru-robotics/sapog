/// Copyright (c) 2018  Zubax Robotics  <info@zubax.com>

#include "board.hpp"
#include <ch.hpp>
#include <cstring>
#include <unistd.h>
#include "led.hpp"

/// Provided by the linker
const extern std::uint8_t DeviceSignatureStorage[];  // NOLINT std::array<>
extern std::uint8_t       AppSharedStruct[];         // NOLINT std::array<>


const PALConfig pal_default_config = {
  {VAL_GPIOAODR, VAL_GPIOACRL, VAL_GPIOACRH},
  {VAL_GPIOBODR, VAL_GPIOBCRL, VAL_GPIOBCRH},
  {VAL_GPIOCODR, VAL_GPIOCCRL, VAL_GPIOCCRH},
  {VAL_GPIODODR, VAL_GPIODCRL, VAL_GPIODCRH},
  {VAL_GPIOEODR, VAL_GPIOECRL, VAL_GPIOECRH}
};
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
namespace board
{
namespace
{

/// This data is used to decide whether the reset handler should jump to the application.
std::uint8_t g_boot_magic[1024] __attribute__((section(".noinit")));  // NOLINT std::array<>

}  // namespace

Clock::time_point Clock::now() noexcept
{
    static ::systime_t   prev_sample = 0;
    static std::uint64_t base        = 0;

    CriticalSectionLocker locker;

#ifndef NDEBUG
    const auto old_base = base;
#endif

    // Computing increment since last invocation
    const ::systime_t   ts        = chVTGetSystemTimeX();
    const std::uint64_t increment = ::systime_t(ts - prev_sample);
    prev_sample                   = ts;

    // Add the increment to the absolute time estimate
    base += increment;

    // Check correctness by making sure the time doesn't go backwards
    assert(old_base <= base);

    return time_point(duration(base));
}

ResetCause init(const RGB& initial_color)
{
    halInit();
    chibios_rt::System::init();
    std::fill(std::begin(g_boot_magic), std::end(g_boot_magic), 0);

//    initLEDPWM();
    board::init_led();
    board::setRGBLED(initial_color);

    ResetCause          reset_cause = ResetCause::Other;
    const std::uint32_t rcc_csr     = RCC->CSR;
    RCC->CSR |= RCC_CSR_RMVF;                                    // Clear reset cause flags
    if ((rcc_csr & (RCC_CSR_IWDGRSTF | RCC_CSR_WWDGRSTF)) != 0)  // Check for either watchdog
    {
        reset_cause = ResetCause::Watchdog;
    }

    sdStart(&STDOUT_SD, nullptr);

    RCC->APB1ENR |= RCC_APB1ENR_CAN1EN;  // CAN2 is not used.

    kickWatchdog();
    return reset_cause;
}

void kickWatchdog()
{
    IWDG->KR = 0xAAAA;
}

[[noreturn]] void bootApplication()
{
    // Loading and validating the application entry point
    const unsigned stacktop   = *reinterpret_cast<unsigned*>(FLASH_BASE + APPLICATION_OFFSET);      // NOLINT
    const unsigned entrypoint = *reinterpret_cast<unsigned*>(FLASH_BASE + APPLICATION_OFFSET + 4);  // NOLINT
    if ((stacktop <= SRAM_BASE) || (stacktop > (SRAM_BASE + 2 * 1024 * 1024)))
    {
        chibios_rt::System::halt("STACKTOP");
    }
    if ((entrypoint < (FLASH_BASE + APPLICATION_OFFSET)) || (entrypoint >= (FLASH_BASE + getFlashSize())))
    {
        chibios_rt::System::halt("ENTRYPOINT");
    }
    std::memcpy(g_boot_magic,
                reinterpret_cast<unsigned*>(FLASH_BASE + APPLICATION_OFFSET),  // NOLINT
                sizeof(g_boot_magic));
    while (true)
    {
        NVIC_SystemReset();
    }
}

[[noreturn]] void restart()
{
    NVIC_SystemReset();
    while (true)
    {
        chibios_rt::System::halt("UNREACHABLE");
    }
}

UniqueID readUniqueID()
{
    UniqueID out;
      std::memcpy(out.data(), reinterpret_cast<const void *>(0x1FFFF7E8), std::tuple_size<UniqueID>::value);
      return out;
}

std::optional<DeviceSignature> tryReadDeviceSignature()
{
    // Read from the designated storage in ROM
    DeviceSignature out_sign{};
    std::memcpy(out_sign.data(), DeviceSignatureStorage, out_sign.size());
    // Verify if it looks valid
    for (auto x : out_sign)
    {
        if ((x != 0xFF) && (x != 0x00))  // All 0xFF/0x00 is not a valid signature, it's empty storage
        {
            return out_sign;
        }
    }
    return {};
}

std::array<std::uint8_t, 2> detectHardwareVersion()
{
    static const std::array<std::uint8_t, 2> v{{HW_VERSION_MAJOR, std::uint8_t(GPIOC->IDR & 0x0F)}};
    return v;
}

std::uint8_t* getAppSharedStructLocation()
{
    return &AppSharedStruct[0];
}

void setRGBLED(const RGB& rgb)
{
    (void)rgb;
    TIM3->CCR1 = rgb[0] * 257U;
    TIM3->CCR2 = rgb[1] * 257U;
    TIM3->CCR3 = rgb[2] * 257U;
}

void setCANActivityLED(const int interface_index, const bool state)
{
    (void) state;
    (void) interface_index;

}

}  // namespace board

// Early init from ChibiOS
extern "C" {

static void initGPIO()
{

}

[[maybe_unused]] void __early_init(void)  // NOLINT
{
    initGPIO();

    // Init the default clock configuration which is to use HSI --> PLL. The HSI is imprecise though, last resort only.
    stm32_clock_init();

}

[[noreturn]] extern void _crt0_entry() noexcept;

/// We have to override the reset handler in order to implement fast jump to the application.
/// Note that the RGB LED will be turned off upon reset.
[[noreturn]] void Reset_Handler() noexcept;
void              Reset_Handler() noexcept
{
    // The watchdog shall be enabled before the application is started to allow the bootloader to take control
    // if the application is faulty and unable to reset the watchdog timely.
    RCC->CSR |= RCC_CSR_LSION;  // Make sure LSI is enabled
    while (!bool(RCC->CSR & RCC_CSR_LSIRDY))
    {
        (void) 0;  // Wait for the LSI to start.
    }
//    IWDG->KR = 0xAAAA;
//    while (IWDG->SR != 0)
//    {
//        (void) 0;  // Wait until the IWDG is ready to accept the new parameters
//    }
//    IWDG->KR  = 0x5555;
//    IWDG->PR  = 6;  // Div 256 yields 6.4ms per clock period at 40kHz
//    IWDG->RLR = std::uint16_t(std::min<std::int64_t>(board::WatchdogTimeout_ms / 6, 0x0FFF));
//    IWDG->KR  = 0xAAAA;
//    IWDG->KR  = 0xCCCC;
    // In order to ensure clean, deterministic state at the time of the application launch, we jump
    // to the application immediately after reset without configuring anything.
    const auto app_adr = FLASH_BASE + APPLICATION_OFFSET;
    const auto app_ptr = reinterpret_cast<unsigned*>(app_adr);  // NOLINT
    if (0 == std::memcmp(board::g_boot_magic, app_ptr, sizeof(board::g_boot_magic)))
    {
        std::memset(board::g_boot_magic, 0, sizeof(board::g_boot_magic));  // Prevent deja vu.
        const unsigned stacktop   = *(app_ptr + 0U);                       // NOLINT
        const unsigned entrypoint = *(app_ptr + 1U);                       // NOLINT
        if ((stacktop > SRAM_BASE) && (entrypoint >= app_adr))
        {
            asm("dsb");  // NOLINT
            asm("isb");  // NOLINT
            SCB->VTOR = app_adr;
            asm volatile(                        // NOLINT
                "dsb                        \n"  //
                "isb                        \n"  //
                "msr msp, %[stacktop]       \n"  //
                "dsb                        \n"  //
                "isb                        \n"  //
                "bx       %[entrypoint]     \n"  //
                ::[stacktop] "r"(stacktop),
                [entrypoint] "r"(entrypoint)
                :);
        }
    }
    // If the app does not need to be launched or cannot be launched, jump to the ChibiOS entry point.
    _crt0_entry();
}
}
