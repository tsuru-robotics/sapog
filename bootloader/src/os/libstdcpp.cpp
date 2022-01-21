// Copyright (c) 2018 Zubax, zubax.com
// Distributed under the MIT License, available in the file LICENSE.
// Author: Pavel Kirienko <pavel.kirienko@zubax.com>

#include <ch.hpp>
#include <cstdint>
#include <new>

static std::uint8_t g_operator_new_returns_pointer_to_this;

[[noreturn]] static void _libstdcpp_panic(const char* msg)
{
    chSysHalt(msg);
    for (;;)
    {}
}

void* operator new(std::size_t x)
{
    (void) x;
    _libstdcpp_panic("operator new()");
    return &g_operator_new_returns_pointer_to_this;
}

void* operator new[](std::size_t x)
{
    (void) x;
    _libstdcpp_panic("operator new[]()");
    return &g_operator_new_returns_pointer_to_this;
}

void operator delete(void* x)
{
    (void) x;
    _libstdcpp_panic("delete");
}

void operator delete[](void* x)
{
    (void) x;
    _libstdcpp_panic("delete");
}

void operator delete(void* x, std::size_t sz)
{
    (void) x;
    (void) sz;
    _libstdcpp_panic("delete");
}

void operator delete[](void* x, std::size_t sz)
{
    (void) x;
    (void) sz;
    _libstdcpp_panic("delete");
}

#if __cpp_aligned_new
void operator delete(void* x, std::align_val_t sz)
{
    (void) x;
    (void) sz;
    _libstdcpp_panic("delete");
}

void operator delete[](void* x, std::align_val_t sz)
{
    (void) x;
    (void) sz;
    _libstdcpp_panic("delete");
}

void operator delete(void* x, std::size_t sz, std::align_val_t al)
{
    (void) x;
    (void) sz;
    (void) al;
    _libstdcpp_panic("delete");
}

void operator delete[](void* x, std::size_t sz, std::align_val_t al)
{
    (void) x;
    (void) sz;
    (void) al;
    _libstdcpp_panic("delete");
}
#endif

// stdlibc++ workaround.
// Default implementations will throw, which causes code size explosion.
// These definitions override the ones defined in the stdlibc+++.
namespace std  // NOLINT
{
[[maybe_unused]] void __throw_bad_exception()
{
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_bad_alloc()
{
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_bad_cast()
{
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_bad_typeid()
{
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_logic_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_domain_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_invalid_argument(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_length_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_out_of_range(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_out_of_range_fmt(const char* x, ...)  // NOLINT
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_runtime_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_range_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_overflow_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_underflow_error(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_ios_failure(const char* x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_system_error(int x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_future_error(int x)
{
    (void) x;
    _libstdcpp_panic("throw");
}

[[maybe_unused]] void __throw_bad_function_call()
{
    _libstdcpp_panic("throw");
}

}  // namespace std

namespace __gnu_cxx
{
[[maybe_unused]] void __verbose_terminate_handler()
{
    _libstdcpp_panic("terminate");
}

}  // namespace __gnu_cxx

extern "C" {

[[maybe_unused]] int __aeabi_atexit(void* x, void (*fun)(void*), void* y)  // NOLINT
{
    (void) x;
    (void) fun;
    (void) y;
    return 0;
}

/// Ref. "Run-time ABI for the ARM Architecture" page 23..24
/// http://infocenter.arm.com/help/topic/com.arm.doc.ihi0043d/IHI0043D_rtabi.pdf
///
/// ChibiOS issue: http://forum.chibios.org/phpbb/viewtopic.php?f=3&t=2404
///
/// A 32-bit, 4-byte-aligned static data value. The least significant 2 bits
/// must be statically initialized to 0.
using __guard = int;
static_assert(sizeof(__guard) == 4);

[[maybe_unused]] void __cxa_atexit(void (*x)(void*), void* y, void* z)
{
    (void) x;
    (void) y;
    (void) z;
}

[[maybe_unused]] int __cxa_guard_acquire(const __guard* g)
{
    return static_cast<int>(*g == 0);
}

[[maybe_unused]] void __cxa_guard_release(__guard* g)
{
    *g = 1;
}

[[maybe_unused]] void __cxa_guard_abort(const __guard* g)
{
    (void) g;
}

}  // namespace __gnu_cxx
