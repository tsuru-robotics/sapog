/// Copyright (c) 2018  Zubax Robotics  <info@zubax.com>

#pragma once

#include <ch.hpp>
#include <cassert>
#include <optional>
#include <hal.h>
#include <cstdint>
#include <chrono>
#include <array>

#if !defined(DEBUG_BUILD) && !defined(RELEASE_BUILD)
#    error Either DEBUG_BUILD or RELEASE_BUILD must be defined
#endif

namespace board
{
/// Can't use chrono because this is used during early-stage initialization.
static constexpr std::uint16_t WatchdogTimeout_ms = 10'000U;

/// Simple monotonic clock used for timestamping; measures the time since boot, never overflows.
/// Implementation of the TrivialClock trait from std.
///
/// Note that this implementation requires that the clock is sampled regularly,
/// otherwise the base timer may overflow and shift the epoch backwards!
///
/// http://en.cppreference.com/w/cpp/concept/TrivialClock
/// http://en.cppreference.com/w/cpp/concept/Clock
struct Clock
{
    using rep        = std::int64_t;
    using period     = std::ratio<1, CH_CFG_ST_FREQUENCY>;
    using duration   = std::chrono::duration<rep, period>;
    using time_point = std::chrono::time_point<Clock>;

    [[maybe_unused]] static constexpr bool is_steady = true;

    static time_point now() noexcept;
};

/// Encodes the reason of the latest (current) reset
enum class ResetCause : std::uint8_t
{
    Watchdog,
    Other
};

using RGB = std::array<std::uint8_t, 3>;
static constexpr RGB Red{{255, 0, 0}};
static constexpr RGB Green{{0, 255, 0}};
static constexpr RGB Blue{{0, 0, 255}};
static constexpr RGB Yellow{{255, 255, 0}};
static constexpr RGB Cyan{{0, 255, 255}};

/// This function should be invoked immediately from main().
/// It initializes the watchdog timer ASAP, which ensures that the application will not be stuck forever if init fails.
/// Note that this function erases the reset cause flags from the RCC CSR register!
ResetCause init(const RGB& initial_color);

/// Resets the hardware watchdog.
void kickWatchdog();

/// Starts the application normally. No validity checks of any kind are guaranteed.
[[noreturn]] void bootApplication();

/// Resets the MCU via NVIC, no additional actions are performed.
[[noreturn]] void restart();

/// Returns the 128-bit hardware UID, where only the first 96 bit are used, and the rest is
/// filled with zeros.
using UniqueID = std::array<std::uint8_t, 16>;
UniqueID readUniqueID();

/// RSA-1776 Signature of Authenticity management.
/// The signature can be written only once and it is typically done by the hardware manufacturer.
/// Read will fail if there is no signature installed.
using DeviceSignature = std::array<std::uint8_t, 222>;
std::optional<DeviceSignature> tryReadDeviceSignature();

/// The major code can be specified either by the hardware ID pins or at compile time.
/// The minor code is specified only by the hardware ID pins.
std::array<std::uint8_t, 2> detectHardwareVersion();

/// Returns the flash size on this particular microcontroller.
inline std::uint32_t getFlashSize()
{
    const std::uint32_t out = 1024U * *reinterpret_cast<std::uint16_t*>(0x1FFFF7E0);  // NOLINT
    assert(out >= 128 * 1024);
    assert(out <= 2048 * 1024);
    return out;
}

/// Pointer to SRAM where the arguments from the application may be stored.
std::uint8_t* getAppSharedStructLocation();

/// Sets the LED color.
void setRGBLED(const RGB& rgb);

/// Controls the CAN activity LED, per interface.
void setCANActivityLED(const int interface_index, const bool state);

/// Testpoint control.
/// The functions are made inline to ensure minimal runtime overhead even with LTO disabled.
/// Note that testpoint mapping depends on the hardware revision. Refer to the hardware design documentation for more
/// information.
/// @{
template <unsigned TestPointIndex>
void setTestPoint(bool level);

template <>
inline void setTestPoint<0>(bool level)
{
    palWritePad(GPIOC, GPIOC_TEST_1, unsigned(level));
}

template <>
inline void setTestPoint<1>(bool level)
{
    palWritePad(GPIOC, GPIOC_TEST_2, unsigned(level));
}

/// Use this helper to toggle testpoints:
///      RAIITestPointToggler<0> toggler;
template <unsigned TestPointIndex>
struct RAIITestPointTogglerImpl_
{
    RAIITestPointTogglerImpl_() { setTestPoint<TestPointIndex>(true); }
    ~RAIITestPointTogglerImpl_() { setTestPoint<TestPointIndex>(false); }

    RAIITestPointTogglerImpl_(const RAIITestPointTogglerImpl_&) = delete;
    RAIITestPointTogglerImpl_(RAIITestPointTogglerImpl_&&)      = delete;
    RAIITestPointTogglerImpl_& operator=(const RAIITestPointTogglerImpl_&) = delete;
    RAIITestPointTogglerImpl_& operator=(RAIITestPointTogglerImpl_&&) = delete;
};

template <unsigned TestPointIndex>
using RAIITestPointToggler = volatile RAIITestPointTogglerImpl_<TestPointIndex>;

/// RAII critical section locker.
using CriticalSectionLocker = volatile struct _cs final
{
    _cs() = default;
    ~_cs() { chSysRestoreStatusX(st_); }
    _cs(const _cs&) = delete;
    _cs(_cs&&)      = delete;
    _cs& operator=(const _cs&) = delete;
    _cs& operator=(_cs&&) = delete;

private:
    volatile const syssts_t st_ = chSysGetStatusAndLockX();
};

}  // namespace board
