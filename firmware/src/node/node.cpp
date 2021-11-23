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
#include "reg/udral/physics/acoustics/Note_0_1.h"
#include "node/commands/commands.hpp"
#include <uavcan/node/ExecuteCommand_1_1.h>
#include <node/essential/access.hpp>
#include <node/essential/get_info.hpp>
#include <node/esc/esc.hpp>
#include <uavcan/si/unit/angular_velocity/Scalar_1_0.h>
#include <bxcan/bxcan_registers.h>
#include "node/essential/note.hpp"
#include "node/subscription_macros.hpp"

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

void print_can_error_if_exists()
{
    uint32_t error_code = ((volatile BxCANType *) 0x40006400U)->ESR;
    if (error_code != 0)
    {
        printf("%ld\n", error_code);
    }
}

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

    static Loop loops[]{Loop{handle_1hz_loop, SECOND_IN_MICROSECONDS, get_monotonic_microseconds()},
                        Loop{handle_fast_loop, QUEUE_TIME_FRAME, get_monotonic_microseconds()},
                        Loop{handle_5_second_loop, SECOND_IN_MICROSECONDS * 5, get_monotonic_microseconds()}
    };
    printf("Has this node_id after pnp: %d\n", state.canard.node_id);
    // Loops begin running
    while (true)
    {
//        print_can_error_if_exists()
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

bool is_port_configurable(RegisteredPort &reg)
{
    return reg.subscription.port_id == CONFIGURABLE_SUBJECT_ID;
}

#define CONFIGURABLE_SUBJECT_ID 0xFFFF
CONFIG_PARAM_INT("uavcan.sub.note_response.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.sub.radians_in_second_velocity.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

RegisteredPort registered_ports[] =
    {
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_GetInfo, 1, 0, &node::essential::uavcan_node_GetInfo_1_0_handler),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_node_ExecuteCommand, 1, 1,
                                      &uavcan_node_ExecuteCommand_Request_1_1_handler),
        FIXED_ID_SERVICE_SUBSCRIPTION(uavcan_register_Access, 1, 0,
                                      &node::essential::uavcan_register_Access_1_0_handler),
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(note_response, reg_udral_physics_acoustics_Note,
                                             0, 1,
                                             &reg_udral_physics_acoustics_Note_0_1_handler),
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(radians_in_second_velocity, uavcan_si_unit_angular_velocity_Scalar,
                                             1, 0,
                                             &sub_esc_rpm_handler)
    };


/// Get a pair of iterators, one points to the start of the subscriptions array and the other points to the end of it.


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
    for (int i = 0; i < AMOUNT_OF_QUEUES; ++i)
    {
        CanardTxQueue new_queue = canardTxInit(100, 8);
        state.queues[i] = new_queue;
    }
    ConfigParam _{};
    bool value_exists = false;//configGetDescr("uavcan_node_id", &_) != -ENOENT;
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
        if (registered_port.subscription.port_id == CONFIGURABLE_SUBJECT_ID)
        {
            if (configGetDescr(registered_port.name, &_) != -ENOENT)
            {
                registered_port.subscription.port_id = configGet(registered_port.name);
            } else
            {
                printf("Subscription for %s had no subject port id configured\n", registered_port.type);
                continue;
            }
        }
        const int8_t res =  //
            canardRxSubscribe(&state.canard,
                              CanardTransferKindRequest,
                              registered_port.subscription.port_id,
                              registered_port.subscription.extent,
                              registered_port.subscription.transfer_id_timeout_usec,
                              &registered_port.subscription);

        if (registered_port.subscription.user_reference == nullptr)
        {
            printf("Subscription %s had no handler set.\n", registered_port.name);
            continue;
        }
        if (res < 0)
        {
            printf("The error with canardRxSubscribe was: %d\n", res);
        }
        chThdSleepMicroseconds(400);
        assert(res >= 0); // This is to make sure that the subscription was successful.
        printf("Created a subscription for %s\n", registered_port.name);
    }
    printf("Canard initialized\n");
}

std::pair<RegisteredPort *, RegisteredPort *> get_ports_info_iterators()
{
    return {
        std::begin(registered_ports), std::end(registered_ports)
    };
}


int UAVCANNode::init()
{
    if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), NORMALPRIO, control_thread, nullptr))
    {
        return -1;
    }
    return 0;
}
