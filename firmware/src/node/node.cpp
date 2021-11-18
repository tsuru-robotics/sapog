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
#include <uavcan/si/unit/angular_velocity/Scalar_1_0.h>
#include <bxcan/bxcan_registers.h>
#include "stop_gap.hpp"

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

    static Loop loops[]{//Loop{&handle_1hz_loop, SECOND_IN_MICROSECONDS, get_monotonic_microseconds()},
        Loop{handle_fast_loop, QUEUE_TIME_FRAME, get_monotonic_microseconds()},
        //Loop{&handle_5_second_loop, SECOND_IN_MICROSECONDS * 5, get_monotonic_microseconds()}
    };
    printf("Has this node_id after pnp: %d\n", state.canard.node_id);
    // Loops begin running
    while (true)
    {
//        uint32_t error_code = ((volatile BxCANType *) 0x40006400U)->ESR;
//        if (error_code != 0)
//        {
//            printf("%ld\n", error_code);
//        }
        if (state.is_save_requested)
        {
            state.is_save_requested = false;
            configSave();
        }
        if (state.is_restart_required && !os::isRebootRequested())
        {
            printf("Sent %d remaining frames before restarting\n", transmit(state));
            os::requestReboot(); // This actually runs multiple times, like 7 usually, just puts up a flag
        }
        CanardMicrosecond current_time = get_monotonic_microseconds();
        for (Loop &loop: loops)
        {
            if (loop.is_time_to_execute(current_time))
            {
                loop.handler(state);
                loop.increment_next_execution();
            } else
            {
            }
        }
    }
}


// Not all subscriptions come from here, allocation comes from pnp.cpp file and is used there only
/*
 {
     CONFIGURABLE_SUBJECT_ID,
     "uavcan.sub.esc_rpm_direct.id",
     CanardTransferKindRequest,
     uavcan_si_unit_angular_velocity_Scalar_1_0_EXTENT_BYTES_,
     CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
     &sub_esc_rpm_handler},
 {
     CONFIGURABLE_SUBJECT_ID,
     "sub.esc.power",
     CanardTransferKindRequest,
     reg_udral_service_actuator_common_sp_Scalar_0_1_EXTENT_BYTES_,
     CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
     &reg_udral_physics_electricity_PowerTs_0_1_handler},
 {
     CONFIGURABLE_SUBJECT_ID,
     "sub.esc.duty_cycle",
     CanardTransferKindRequest,
     reg_udral_service_actuator_common_sp_Scalar_0_1_EXTENT_BYTES_,
     CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC, {},
     &sub_esc_duty_cycle_handler},
};*/


#define str(x) #x

#define FIXED_ID_SERVICE_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler) \
{.id = nunavut_type##_##version_major##_##version_minor##_FIXED_PORT_ID_,                  \
.type=str(nunavut_type##_Request_##version_major##_##version_minor),                       \
.name=str(nunavut_type##_##version_major##_##version_minor##_FULL_NAME_),                  \
                                                                                           \
                                                                                           \
.transfer_kind=CanardTransferKindRequest,                                                  \
.subscription = {.user_reference=(void *) handler,                                         \
._transfer_id_timeout_usec = CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC,                      \
._extent = nunavut_type##_Request_##version_major##_##version_minor##_EXTENT_BYTES_}}

#define FIXED_ID_MESSAGE_SUBSCRIPTION(nunavut_type, version_major, version_minor, handler) \
{.id = nunavut_type##_##version_major##_##version_minor##_FIXED_PORT_ID_,                  \
.type=str(nunavut_type##_Request_##version_major##_##version_minor),                                                                                  \
.name=str(nunavut_type##_##version_major##_##version_minor##_FULL_NAME_),                                                                                  \
.transfer_kind=CanardTransferKindMessage,                                                  \
.subscription = {.user_reference=(void *) handler,                                         \
._transfer_id_timeout_usec = CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC,                      \
._extent = nunavut_type##_##version_major##_##version_minor##_EXTENT_BYTES_}}


#define REGISTER_ID_SERVICE_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler) \
{.id = CONFIGURABLE_SUBJECT_ID,                                                                          \
.type=str(nunavut_type),                                                                                 \
.name=str(uavcan.sub.port_name.id),                                                                                    \
.transfer_kind=CanardTransferKindRequest,                                                                \
.subscription = {.user_reference=(void *) handler,                                                       \
._transfer_id_timeout_usec = CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC,                                    \
._extent = nunavut_type##_##version_major##_##version_minor##_EXTENT_BYTES_}}


#define REGISTER_ID_MESSAGE_SUBSCRIPTION(port_name, nunavut_type, version_major, version_minor, handler) \
{.id = CONFIGURABLE_SUBJECT_ID,                                                                          \
.type=str(nunavut_type),                                                                                 \
.name=str(uavcan.sub.port_name.id),                                                                                    \
.transfer_kind=CanardTransferKindMessage,                                                                \
.subscription = {.user_reference=(void *) handler,                                                       \
._transfer_id_timeout_usec = CANARD_DEFAULT_TRANSFER_ID_TIMEOUT_USEC,                                    \
._extent = nunavut_type##_##version_major##_##version_minor##_EXTENT_BYTES_}}

RegisteredPort registered_ports[] =
    {
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_GetInfo, 1, 0, node::essential::uavcan_node_GetInfo_1_0_handler),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_ExecuteCommand, 1, 1, uavcan_node_ExecuteCommand_Request_1_1_handler),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_register_Access, 1, 0,
                                      node::essential::uavcan_register_Access_1_0_handler),
        REGISTER_ID_MESSAGE_SUBSCRIPTION(note_response, reg_udral_physics_acoustics_Note,
                                         0, 1,
                                         reg_udral_physics_acoustics_Note_0_1_handler)
    };

// Get a pair of iterators, one points to the start of the subscriptions array and the other points to the end of it.
std::pair<RegisteredPort *, RegisteredPort *>
get_ports_info_iterators()
{
    return {std::begin(registered_ports), std::end(registered_ports)};
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
    for (auto &registered_port: registered_ports)
    {
        if (registered_port.id == CONFIGURABLE_SUBJECT_ID)
        {
            if (configGetDescr(registered_port.name, &_) != -ENOENT)
            {
                subscription.second.id = configGet(subscription.first);
            } else
            {
                printf("Subscription for %s had no subject port id configured\n", subscription.first);
                continue;
            }
        }
        const int8_t res =  //
            canardRxSubscribe(&state.canard,
                              CanardTransferKindRequest,
                              registered_port.id,
                              registered_port.subscription._extent,
                              registered_port.subscription._transfer_id_timeout_usec,
                              &registered_port.subscription);

        if (registered_port.subscription.user_reference == nullptr)
        {
            printf("Subscription %s had no handler set.\n", registered_port.name);
            continue;
        }
        (void) res;
        assert(res > 0); // This is to make sure that the subscription was successful.
        printf("Created a subscription for %s\n", registered_port.name);
    }
    printf("Canard initialized\n");
}


int UAVCANNode::init()
{
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), NORMALPRIO, control_thread, nullptr))
    {
        return -1;
    }
    return 0;
}
