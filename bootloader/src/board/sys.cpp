/// Copyright (c) 2018  Zubax Robotics  <info@zubax.com>

#include "sys.hpp"
#include "chibios/os/various/cpp_wrappers/ch.hpp"
#include <unistd.h>
#include <cassert>
#include "board.hpp"

namespace os
{
/// Last-resort printing - bypasses all stdout logic and prints directly into the default CLI UART.
/// Can be used ONLY for panic reports.
static void emergencyPrint(const char* const str)
{
    for (const char* p = str; bool(*p); p++)
    {
        while (!bool(STDOUT_SD.usart->SR & USART_SR_TXE))
        {}
        STDOUT_SD.usart->DR = *p;
    }
}

}  // namespace os

extern "C" {

[[maybe_unused]] __attribute__((weak)) void* __dso_handle;

[[maybe_unused]] __attribute__((weak)) int* __errno()
{
    static int en;
    return &en;
}

void systemHaltHook(const char* msg)
{
    board::setRGBLED(board::Red);
    port_disable();
    os::emergencyPrint("\r\nPANIC: ");
    if (msg != nullptr)
    {
        os::emergencyPrint(msg);
    }
    os::emergencyPrint("\r\n");
#if defined(DEBUG_BUILD) && DEBUG_BUILD
    if (CoreDebug->DHCSR & CoreDebug_DHCSR_C_DEBUGEN_Msk)
    {
        __asm volatile("bkpt #0\n");  // NOLINT Break into the debugger
    }
#endif
}

/// Overrides the weak handler defined in the OS.
/// This is required because the weak handler doesn't halt the OS, which is very dangerous!
/// More context: http://www.chibios.com/forum/viewtopic.php?f=35&t=3819&p=28555#p28555
[[maybe_unused]] void _unhandled_exception()
{
    chSysHalt("UNDEFINED IRQ");
}

[[maybe_unused]] void __assert_func(const char* file, int line, const char* func, const char* expr)
{
    (void) line;
    (void) func;
    (void) expr;
    port_disable();
    chSysHalt(file);
    while (true)
    {}
}

[[maybe_unused]] void* malloc(size_t sz)
{
    (void) sz;
    assert(sz == 0);  // We want debug builds to fail loudly; release builds are given a pass
    return nullptr;
}

[[maybe_unused]] void* calloc(size_t num, size_t sz)
{
    (void) num;
    (void) sz;
    assert((num == 0) || (sz == 0));  // We want debug builds to fail loudly; release builds are given a pass
    return nullptr;
}

[[maybe_unused]] void* realloc(void* p, size_t sz)
{
    (void) p;
    (void) sz;
    assert(sz == 0);  // We want debug builds to fail loudly; release builds are given a pass
    return nullptr;
}

[[maybe_unused]] void free(void* p)
{
    // Certain stdlib functions, like mktime(), may call free() with zero argument, which can be safely ignored.
    if (p != nullptr)
    {
        chSysHalt("free");
    }
}

[[maybe_unused]] int printf(const char* format, ...)
{
    (void) format;
    assert(false);
    return -1;
}

[[maybe_unused]] int puts(const char* str)
{
    (void) str;
    assert(false);
    return -1;
}

[[maybe_unused]] void NMI_Handler(void)
{
    chibios_rt::System::halt("NMI");
}
[[maybe_unused]] void HardFault_Handler(void)
{
    chibios_rt::System::halt("HardFault");
}
[[maybe_unused]] void MemManage_Handler(void)
{
    chibios_rt::System::halt("MemManage");
}
[[maybe_unused]] void BusFault_Handler(void)
{
    chibios_rt::System::halt("BusFault");
}
[[maybe_unused]] void UsageFault_Handler(void)
{
    chibios_rt::System::halt("UsageFault");
}

}  // extern "C"
