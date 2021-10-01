#include <libcanard/canard.h>
#include <motor/realtime/api.h>
#include "time.h"
/// A deeply embedded system should sample a microsecond-resolution non-overflowing 64-bit timer.
/// Here is a simple non-blocking implementation as an example:
/// https://github.com/PX4/sapog/blob/601f4580b71c3c4da65cc52237e62a/firmware/src/motor/realtime/motor_timer.c#L233-L274
/// Mind the difference between monotonic time and wall time. Monotonic time never changes rate or makes leaps,
/// it is therefore impossible to synchronize with an external reference. Wall time can be synchronized and therefore
/// it may change rate or make leap adjustments. The two kinds of time serve completely different purposes.
CanardMicrosecond get_monotonic_microseconds()
{
    uint64_t currentTimeStamp{motor_rtctl_timestamp_hnsec()};
    return currentTimeStamp / 10;
}
