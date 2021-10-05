/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#define NUNAVUT_ASSERT assert

#include "node.hpp"
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
#include <node/loops/loop.hpp>
#include "board/board.hpp"

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


extern void board::die(int error);

extern void *const ConfigStorageAddress;
constexpr unsigned ConfigStorageSize = 1024;

using namespace uavcan_node_1_0;
using namespace board;

static void init_canard();

static State state{};
// This defines _wa_control_thread
static THD_WORKING_AREA(_wa_control_thread, 1024 * 2);

[[noreturn]] static void control_thread(void *arg)
{
    using namespace node::loops;
    (void) arg;
    init_canard();
    chRegSetThreadName("uavcan_thread");
    // Plug and play feature
    state.plug_and_play.anonymous = state.canard.node_id > CANARD_NODE_ID_MAX;
    node::config::plug_and_play_loop(state);
    static Loop loops[]{Loop{&handle_1hz_loop, SECOND_IN_MICROSECONDS},
                         Loop{&handle_fast_loop, QUEUE_TIME_FRAME},
                         /*Loop{[](State &state_local) {
                             (void) state_local;
                         }, SECOND_IN_MICROSECONDS * 10},
                         Loop{
                                 [](State &state_local) {
                                     (void) state_local;
                                 }, QUEUE_TIME_FRAME
                         },*/
    };

    while (true)
    {
        state.timing.current_time = get_monotonic_microseconds();
        for (Loop loop: loops)
        {
            if (loop.do_execute(state.timing.current_time))
            {
                loop.execution_function(state);
                loop.increment_next_execution();
            }
        }
        chThdSleep(1);
    }
}

struct SubscriptionData
{
    CanardTransferKind transfer_kind;
    int port_id;
    unsigned long extent_bytes;
    unsigned long time_out;
    std::optional<CanardRxSubscription> subscription;
};
std::pair<const char *,  SubscriptionData> subscriptions[3] = {
        {"uavcan.node.getinfo", {CanardTransferKindRequest,
                                        uavcan_node_GetInfo_1_0_FIXED_PORT_ID_,
                                        uavcan_node_GetInfo_Request_1_0_EXTENT_BYTES_,
                                        CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {}}},
        {"uavcan.node.getinfo", {CanardTransferKindRequest, // TODO: fix strings uavcan.node.getinfo
                                        uavcan_pnp_NodeIDAllocationData_1_0_FIXED_PORT_ID_,
                                        uavcan_pnp_NodeIDAllocationData_1_0_EXTENT_BYTES_,
                                        CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {}}},
        {"uavcan.node.getinfo", {CanardTransferKindRequest,
                                        uavcan_register_Access_1_0_FIXED_PORT_ID_,
                                        uavcan_register_Access_Request_1_0_EXTENT_BYTES_,
                                        CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {}}},
};

static void init_canard()
{
    {
        /* https://www.st.com/resource/en/reference_manual/rm0008-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
        AHB/APB bridges (APB) page 49
        Turning on the clocks for the peripherals that are going to be used
        */
        RCC->APB1ENR |= RCC_APB1ENR_CAN1EN;
        RCC->APB1RSTR |= RCC_APB1RSTR_CAN1RST;
        RCC->APB1RSTR &= ~RCC_APB1RSTR_CAN1RST;
    }
    BxCANTimings timings{};
    bxCANComputeTimings(STM32_PCLK1, 1'000'000, &timings); // uavcan.can.bitrate
    bxCANConfigure(0, timings, false);
    state.canard = canardInit(&canardAllocate, &canardFree);
    state.canard.user_reference =
            o1heapInit(&::board::__heap_base__,
                       reinterpret_cast<std::size_t>(&__heap_end__) -
                       reinterpret_cast<std::size_t>(&__heap_base__),  // NOLINT
                       &::board::heapLock,
                       &::board::heapUnlock);
    if (state.canard.user_reference == nullptr)
    {
        chibios_rt::System::halt("o1heap");
    }
    state.canard.mtu_bytes = CANARD_MTU_CAN_CLASSIC; // 8 bytes in MTU
    state.canard.node_id = state.param_node_id.get();
    for (auto &subscription: subscriptions)
    {
        CanardRxSubscription rx;
        subscription.second.subscription = rx;
        const int8_t res =  //
                canardRxSubscribe(&state.canard,
                                  subscription.second.transfer_kind,
                                  subscription.second.port_id,
                                  subscription.second.extent_bytes,
                                  subscription.second.time_out,
                                  &subscription.second.subscription.value());
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
