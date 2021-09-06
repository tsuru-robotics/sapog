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
#include "bxcan/bxcan.h"
#include <time.h>
#include "motor/realtime/api.h"
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

/* Get current value of clock CLOCK_ID and store it in TP.  *//*
extern int clock_gettime(clockid_t __clock_id, struct timespec *__tp) __THROW;*/

/// A deeply embedded system should sample a microsecond-resolution non-overflowing 64-bit timer.
/// Here is a simple non-blocking implementation as an example:
/// https://github.com/PX4/sapog/blob/601f4580b71c3c4da65cc52237e62a/firmware/src/motor/realtime/motor_timer.c#L233-L274
/// Mind the difference between monotonic time and wall time. Monotonic time never changes rate or makes leaps,
/// it is therefore impossible to synchronize with an external reference. Wall time can be synchronized and therefore
/// it may change rate or make leap adjustments. The two kinds of time serve completely different purposes.
static CanardMicrosecond getMonotonicMicroseconds()
{
    uint64_t currentTimeStamp{motor_rtctl_timestamp_hnsec()};
    return currentTimeStamp * 0.1;
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
static uint64_t next_transfer_id_uavcan_node_heartbeat;

bool pleaseTransmit(const CanardFrame txf)
{
    return bxCANPush(0, getMonotonicMicroseconds(), txf.timestamp_usec, txf.extended_can_id, txf.payload_size,
                     txf.payload);
}

static void control_thread(void *arg)
{
    CanardInstance canard = canardInit(&canardAllocate, &canardFree);
    canard.mtu_bytes = CANARD_MTU_CAN_CLASSIC; // 8 bytes in MTU
    canard.node_id = param_node_id.get();
    (void) arg;
    chRegSetThreadName("heartbeat_control_thread");
    CanardMicrosecond next_1_hz_iter_at = started_at + MEGA;

    // provide an implementation of a CAN driver for this node
    do {
        CanardMicrosecond monotonic_time = getMonotonicMicroseconds();
        if (monotonic_time < next_1_hz_iter_at) { continue; }
        next_1_hz_iter_at += MEGA;
        uavcan_node_Heartbeat_1_0 heartbeat{};
        heartbeat.uptime = (uint32_t) ((monotonic_time - started_at) / MEGA);
        heartbeat.mode.value = uavcan_node_Mode_1_0_OPERATIONAL;
        heartbeat.health.value = uavcan_node_Health_1_0_NOMINAL;
        uint8_t serialized[uavcan_node_Heartbeat_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
        size_t serialized_size = sizeof(serialized);
        const int8_t err = uavcan_node_Heartbeat_1_0_serialize_(&heartbeat, &serialized[0], &serialized_size);
        assert(err >= 0);
        if (err >= 0) {
            const CanardTransfer transfer = {
                    .timestamp_usec = monotonic_time + MEGA, // transmission deadline 1 second, optimal for heartbeat
                    .priority       = CanardPriorityNominal,
                    .transfer_kind  = CanardTransferKindMessage,
                    .port_id        = uavcan_node_Heartbeat_1_0_FIXED_PORT_ID_,
                    .remote_node_id = CANARD_NODE_ID_UNSET,
                    .transfer_id    = (CanardTransferID) (next_transfer_id_uavcan_node_heartbeat++),
                    .payload_size   = serialized_size,
                    .payload        = &serialized[0],
            };
            (void) canardTxPush(&canard, &transfer);
        }
        for (const CanardFrame *txf = NULL; (txf = canardTxPeek(&canard)) != NULL;)  // Look at the top of the TX queue.
        {
            if ((0U == txf->timestamp_usec) ||
                (txf->timestamp_usec > getMonotonicMicroseconds()))  // Check the deadline.
            {
                if (!pleaseTransmit(*txf))              // Send the frame. Redundant interfaces may be used here.
                {
                    break;                             // If the driver is busy, break and retry later.
                }
            }
            canardTxPop(&canard);                         // Remove the frame from the queue after it's transmitted.
            canard.memory_free(&canard, (CanardFrame *) txf);  // Deallocate the dynamic memory afterwards.
        }
    } while (1);
}
/*struct BxCANTimings {
    uint16_t bit_rate_prescaler;     /// [1, 1024]
    uint8_t  bit_segment_1;          /// [1, 16]
    uint8_t  bit_segment_2;          /// [1, 8]
    uint8_t  max_resync_jump_width;  /// [1, 4] (recommended value is 1)
};*/
int UAVCANNode::init()
{
//    static os::stm32::ConfigStorageBackend config_storage_backend(ConfigStorageAddress, ConfigStorageSize);
    /*const int config_init_res = os::config::init(&config_storage_backend);
    if (config_init_res < 0) {
        die(config_init_res);
    }*/
    BxCANTimings timings{};
    bxCANComputeTimings(72'000'000, 1'000'000, &timings); // TODO: should be taken from macro
    bxCANConfigure(0, timings, false);
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), HIGHPRIO - 1, control_thread, NULL)) {
        return -1;
    }
    return 0;
}
