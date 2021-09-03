/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include "uavcan_node_1_0.hpp"
#include "zubax_chibios/sys/sys.hpp"
#include <cstddef>
#include "zubax_chibios/config/config.hpp"
#include "zubax_chibios/platform/stm32/config_storage.hpp"
#include <ch.h>
#include <sys/timespec.h>
#include <cstdio>

#define NUNAVUT_ASSERT assert

#include "uavcan/node/Heartbeat_1_0.h"
#include "uavcan/_register/Access_1_0.h"
#include "libcanard/canard.h"

# define CLOCK_MONOTONIC        1
#define KILO 1000L
#define MEGA ((int64_t) KILO * KILO)

static void *canardAllocate(CanardInstance *const ins, const size_t amount)
{
    (void) ins;
    return malloc(amount);
}

static void canardFree(CanardInstance *const ins, void *const pointer)
{
    (void) ins;
    free(pointer);
}

/* Get current value of clock CLOCK_ID and store it in TP.  */
extern int clock_gettime(clockid_t __clock_id, struct timespec *__tp) __THROW;

/// A deeply embedded system should sample a microsecond-resolution non-overflowing 64-bit timer.
/// Here is a simple non-blocking implementation as an example:
/// https://github.com/PX4/sapog/blob/601f4580b71c3c4da65cc52237e62a/firmware/src/motor/realtime/motor_timer.c#L233-L274
/// Mind the difference between monotonic time and wall time. Monotonic time never changes rate or makes leaps,
/// it is therefore impossible to synchronize with an external reference. Wall time can be synchronized and therefore
/// it may change rate or make leap adjustments. The two kinds of time serve completely different purposes.
static CanardMicrosecond getMonotonicMicroseconds()
{
    timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) {
        abort();
    }
    return (uint64_t) (ts.tv_sec * 1000000 + ts.tv_nsec / 1000);
}

namespace board
{
    extern void die(int error);

    extern void *const ConfigStorageAddress;
    constexpr unsigned ConfigStorageSize = 1024;
}

using namespace uavcan_node_1_0;
using namespace board;
static os::config::Param<unsigned> param_node_id("uavcan.node.id", 0, 0, 128);
static THD_WORKING_AREA(_wa_control_thread, 1024 * 2); // This defines _wa_control_thread
static CanardMicrosecond started_at;

static void control_thread(void *arg)
{
    CanardInstance canard = canardInit(&canardAllocate, &canardFree);
    canard.mtu_bytes = CANARD_MTU_CAN_CLASSIC; // 8 bytes in MTU
    canard.node_id = param_node_id.get();

    (void) canard;
    (void) arg;
    chRegSetThreadName("heartbeat_control_thread");
    //event_listener_t listener;
    //chEvtRegisterMask(&_setpoint_update_event, &listener, ALL_EVENTS);

    //uint64_t timestamp_hnsec = motor_rtctl_timestamp_hnsec();
    do {
        CanardMicrosecond monotonic_time = getMonotonicMicroseconds();
        uavcan_node_Heartbeat_1_0 heartbeat{};
        heartbeat.uptime = (uint32_t) ((monotonic_time - started_at) / MEGA);
        heartbeat.mode.value = uavcan_node_Mode_1_0_OPERATIONAL;
/*        if (heap_diag.oom_count > 0)
        {
            heartbeat.health.value = uavcan_node_Health_1_0_CAUTION;
        }
        else
        {*/
        heartbeat.health.value = uavcan_node_Health_1_0_NOMINAL;
        (void) heartbeat;
//        }
    } while (1);
}

int UAVCANNode::init()
{
    static os::stm32::ConfigStorageBackend config_storage_backend(ConfigStorageAddress, ConfigStorageSize);
    const int config_init_res = os::config::init(&config_storage_backend);
    if (config_init_res < 0) {
        die(config_init_res);
    }
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), HIGHPRIO - 1, control_thread,
                           NULL)) { // HIGHPRIO from #include "chschd.h"
        return -1;
    }
    return 0;
}
