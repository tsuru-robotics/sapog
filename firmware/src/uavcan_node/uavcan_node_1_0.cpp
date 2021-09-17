/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#define NUNAVUT_ASSERT assert

#include "uavcan_node_1_0.hpp"
#include <cstddef>
#include "zubax_chibios/config/config.hpp"
#include <ch.h>
#include <uavcan/node/port/List_0_1.h>
#include "bxcan/bxcan.h"
#include "reception.hpp"


#include "uavcan/node/Heartbeat_1_0.h"
#include "uavcan/_register/Access_1_0.h"
#include "libcanard/canard.h"
#include "o1heap/o1heap.h"
#include "state.hpp"
#include "units.hpp"
#include "time.h"
#include "loops.hpp"
#include <thread>
#include <sys/unistd.h>

static void *canardAllocate(CanardInstance *const ins, const size_t amount)
{
    (void) ins;
    return o1heapAllocate(static_cast<O1HeapInstance *>(ins->user_reference), amount);
}

static void canardFree(CanardInstance *const ins, void *const pointer)
{
    (void) ins;
    o1heapFree(static_cast<O1HeapInstance *>(ins->user_reference), pointer);
}


namespace board
{
extern void die(int error);

extern void *const ConfigStorageAddress;
constexpr unsigned ConfigStorageSize = 1024;
}

using namespace uavcan_node_1_0;
using namespace board;
static THD_WORKING_AREA(_wa_control_thread, 1024 * 2); // This defines _wa_control_thread


static void initCanard();

extern "C"
{
extern char __heap_base__;  // NOLINT
extern char __heap_end__;   // NOLINT
}
using node::state::State;


static State state{};
namespace platform
{
syssts_t g_heap_irq_status_{};  // NOLINT

void heapLock()
{
    g_heap_irq_status_ = chSysGetStatusAndLockX();
}

void heapUnlock()
{
    chSysRestoreStatusX(g_heap_irq_status_);
}
}

[[noreturn]] static void control_thread(void *arg)
{
    using namespace node::loops;
    (void) arg;
    initCanard();
    chRegSetThreadName("uavcan_thread");
    state.timing.next_fast_iter_at = state.timing.started_at + QUEUE_TIME_FRAME;
    state.timing.next_1_hz_iter_at = state.timing.started_at + MEGA;
    state.timing.next_01_hz_iter_at = state.timing.started_at + MEGA * 10;
    // Plug and play feature
    while (state.flags.anonymous)
    {
        state.flags.anonymous = !node::config::plug_and_play(state);
        int sleep_time = 500 + rand() % 2000;
        printf("Plug and play is sleeping for %d", sleep_time);
        chThdSleep(sleep_time);  // 1 tick is 100 microseconds in our case, so 1000 is one second
    }
    while(true)
    {
        // Run a trivial scheduler polling the loops that run the business logic.
        state.timing.current_time = getMonotonicMicroseconds();
        if (state.timing.current_time >= state.timing.next_fast_iter_at)
        {
            state.timing.next_fast_iter_at += QUEUE_TIME_FRAME;;
            node::loops::handleFastLoop(state);
        }
        if (state.timing.current_time >= state.timing.next_1_hz_iter_at)
        {
            state.timing.next_1_hz_iter_at += MEGA;
            handle1HzLoop(state);
        }
        if (state.timing.current_time >= state.timing.next_01_hz_iter_at)
        {
            state.timing.next_01_hz_iter_at += MEGA * 10;
            handle01HzLoop(state);
        }
        chThdSleep(1);
        //publish_port_list(canard, monotonic_time); // TODO: When we have subscriptions, enable this.
    }
}

static void initCanard()
{
    {
        // https://www.st.com/resource/en/reference_manual/rm0008-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
        // AHB/APB bridges (APB) page 49
        // Turning on the clocks for the peripherals that are going to be used
        RCC->APB1ENR |= RCC_APB1ENR_CAN1EN;
        RCC->APB1RSTR |= RCC_APB1RSTR_CAN1RST;
        RCC->APB1RSTR &= ~RCC_APB1RSTR_CAN1RST;
    }
    BxCANTimings timings{};
    bxCANComputeTimings(36'000'000, 1'000'000, &timings); // TODO: should be taken from macro
    bxCANConfigure(0, timings, false);
    state.canard = canardInit(&canardAllocate, &canardFree);
    state.canard.user_reference =
            o1heapInit(&__heap_base__,
                       reinterpret_cast<std::size_t>(&__heap_end__) -
                       reinterpret_cast<std::size_t>(&__heap_base__),  // NOLINT
                       &platform::heapLock,
                       &platform::heapUnlock);
    state.canard.mtu_bytes = CANARD_MTU_CAN_CLASSIC; // 8 bytes in MTU
    state.canard.node_id = state.param_node_id.get();
    // Service servers:
    {
        static CanardRxSubscription rx;
        const int8_t res =  //
                canardRxSubscribe(&state.canard,
                                  CanardTransferKindRequest,
                                  uavcan_node_GetInfo_1_0_FIXED_PORT_ID_,
                                  uavcan_node_GetInfo_Request_1_0_EXTENT_BYTES_,
                                  CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC,
                                  &rx);
        assert(res > 0); // This is to make sure that the subscription was successful.
    }
}


int UAVCANNode::init()
{
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), HIGHPRIO - 1, control_thread, nullptr))
    {
        return -1;
    }
    return 0;
}
