/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#define NUNAVUT_ASSERT assert

#include "node.hpp"
#include <cstddef>
#include <ch.h>
#include "bxcan/bxcan.h"
#include "reception.hpp"
#include "uavcan/node/Heartbeat_1_0.h"
#include "uavcan/_register/Access_1_0.h"
#include "libcanard/canard.h"
#include "state.hpp"
#include "units.hpp"
#include "time.h"
#include "loops.hpp"
#include <node/loops/loop.hpp>
#include "board/board.hpp"
#include "node/conf/conf.hpp"
#include "reg/udral/physics/acoustics/Note_0_1.h"
#include "node/commands/commands.hpp"

#include <reg/udral/service/common/Readiness_0_1.h>
#include <reg/udral/service/actuator/common/__0_1.h>
#include <reg/udral/service/actuator/common/Feedback_0_1.h>
#include <reg/udral/service/actuator/common/Status_0_1.h>
#include <reg/udral/physics/dynamics/translation/LinearTs_0_1.h>
#include <reg/udral/physics/electricity/PowerTs_0_1.h>
#include <reg/udral/service/actuator/common/sp/Scalar_0_1.h>
#include <uavcan/node/ExecuteCommand_1_1.h>
#include <node/essential/access.hpp>
#include <node/essential/get_info.hpp>
#include <motor/motor.hpp>
#include <node/esc/esc.hpp>

#define CONFIGURABLE_SUBJECT_ID 0xFFFF

static void *canardAllocate(CanardInstance *const ins, const size_t amount)
{
    (void) ins;
    return board::allocate(amount);
}

static void canardFree(CanardInstance *const ins, void *const pointer)
{
    (void) ins;
    board::deallocate(pointer);
}


extern void board::die(int error);

extern void *const ConfigStorageAddress;
constexpr unsigned ConfigStorageSize = 1024;

using namespace uavcan_node_1_0;
using namespace board;

static void init_canard();

static State state{};
// This defines _wa_control_thread
static THD_WORKING_AREA(_wa_control_thread,
                        1024 * 4);

[[noreturn]] static void control_thread(void *arg)
{
    using namespace node::loops;
    (void) arg;
    init_canard();
    chRegSetThreadName("uavcan_thread");
    // Plug and play feature
    state.plug_and_play.anonymous = state.canard.node_id > CANARD_NODE_ID_MAX;
    node::pnp::plug_and_play_loop(state);
    // Loops are created
    static Loop loops[]{Loop{&handle_1hz_loop, SECOND_IN_MICROSECONDS, get_monotonic_microseconds()},
                        Loop{&handle_fast_loop, QUEUE_TIME_FRAME, get_monotonic_microseconds()},
                        Loop{&handle_5_second_loop, SECOND_IN_MICROSECONDS * 5, get_monotonic_microseconds()}
    };
    printf("Has this node_id after pnp: %d\n", state.canard.node_id);
    // Loops begin running
    while (true)
    {
        if (state.is_restart_required && !os::isRebootRequested())
        {
            printf("Sent %d remaining frames before restarting\n", transmit(state));
            os::requestReboot(); // This actually runs multiple times, like 7 usually, just puts up a flag
        }
        CanardMicrosecond current_time = get_monotonic_microseconds();
        for (Loop &loop: loops)
        {
            if (loop.do_execute(current_time))
            {
                loop.execution_function(state);
                loop.increment_next_execution();
            } else
            {
            }
        }
        chThdSleep(1);
    }
}

// Not all subscriptions come from here, allocation comes from pnp.cpp file and is used there only
std::pair<const char *, SubscriptionData> subscriptions[] = {
    {uavcan_node_GetInfo_1_0_FULL_NAME_AND_VERSION_,              {CanardTransferKindRequest,
                                                                      uavcan_node_GetInfo_1_0_FIXED_PORT_ID_,
                                                                      uavcan_node_GetInfo_Request_1_0_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &node::essential::uavcan_node_GetInfo_1_0_handler}},
    {uavcan_register_Access_1_0_FULL_NAME_AND_VERSION_,           {CanardTransferKindRequest,
                                                                      uavcan_register_Access_1_0_FIXED_PORT_ID_,
                                                                      uavcan_register_Access_Request_1_0_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &node::essential::uavcan_register_Access_1_0_handler}},
    {reg_udral_physics_acoustics_Note_0_1_FULL_NAME_AND_VERSION_, {CanardTransferKindMessage,
                                                                      CONFIGURABLE_SUBJECT_ID,
                                                                      reg_udral_physics_acoustics_Note_0_1_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &reg_udral_physics_acoustics_Note_0_1_handler}},
    {uavcan_node_ExecuteCommand_1_1_FULL_NAME_AND_VERSION_,       {CanardTransferKindRequest,
                                                                      uavcan_node_ExecuteCommand_1_1_FIXED_PORT_ID_,
                                                                      uavcan_node_ExecuteCommand_Request_1_1_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &uavcan_node_ExecuteCommand_Request_1_1_handler}},
    {"sub.esc.rpm",                                               {CanardTransferKindRequest,
                                                                      CONFIGURABLE_SUBJECT_ID,
                                                                      reg_udral_service_actuator_common_sp_Scalar_0_1_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &sub_esc_rpm_handler}},
    {"sub.esc.power",                                             {CanardTransferKindRequest,
                                                                      CONFIGURABLE_SUBJECT_ID,
                                                                      reg_udral_service_actuator_common_sp_Scalar_0_1_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &sub_esc_rpm_handler}},
    {"sub.esc.duty_cycle",                                        {CanardTransferKindRequest,
                                                                      CONFIGURABLE_SUBJECT_ID,
                                                                      reg_udral_service_actuator_common_sp_Scalar_0_1_EXTENT_BYTES_,
                                                                      CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
                                                                      &sub_esc_rpm_handler}},

};

// Get a pair of iterators, one points to the start of the subscriptions array and the other points to the end of it.
std::pair<const std::pair<const char *, SubscriptionData> *, const std::pair<const char *, SubscriptionData> *>
get_subscriptions()
{
    return {std::begin(subscriptions), std::end(subscriptions)};
}

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
    state.canard.mtu_bytes = CANARD_MTU_CAN_CLASSIC; // 8 bytes in MTU
    ConfigParam _{};
    bool value_exists = configGetDescr("uavcan_node_id", &_) != -ENOENT;
    float stored_node_id = CANARD_NODE_ID_UNSET;
    if (value_exists)
    {
        stored_node_id = configGet("uavcan_node_id");
    }
    if (stored_node_id == NAN)
    {
        state.canard.node_id = CANARD_NODE_ID_UNSET;
    } else
    {
        state.canard.node_id = stored_node_id;
    }
    state.timing.started_at = get_monotonic_microseconds();
    for (auto &subscription: subscriptions)
    {
        if (subscription.second.port_id == 0xFFFF)
        {
            if (configGetDescr(subscription.first, &_) != -ENOENT)
            {
                subscription.second.port_id = configGet(subscription.first);
            } else
            {
                printf("Subscription for %s had no subject port id configured\n", subscription.first);
                continue;
            }
        }
        const int8_t res =  //
            canardRxSubscribe(&state.canard,
                              subscription.second.transfer_kind,
                              subscription.second.port_id,
                              subscription.second.extent_bytes,
                              subscription.second.time_out,
                              &subscription.second.subscription);
        if (subscription.second.handler != nullptr)
        {
            subscription.second.subscription.user_reference = &subscription.second;
        } else
        {
            printf("Subscription %s had no handler set.\n", subscription.first);
        }
        assert(res > 0); // This is to make sure that the subscription was successful.
    }
    printf("Canard initialized\n");
}


int UAVCANNode::init()
{
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), HIGHPRIO - 1, control_thread, nullptr))
    {
        return -1;
    }
    return 0;
}
