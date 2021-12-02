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
#include <node/esc/readiness.hpp>
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

bool is_port_configurable(RegisteredPort &reg)
{
    return reg.subscription.port_id == CONFIGURABLE_SUBJECT_ID;
}


CONFIG_PARAM_INT("uavcan.sub.note_response.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.sub.setpoint.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("id_in_esc_group", CONFIGURABLE_ID_IN_ESC_GROUP, 0, CONFIGURABLE_ID_IN_ESC_GROUP)

CONFIG_PARAM_INT("uavcan.sub.readiness.id", CONFIGURABLE_ID_IN_ESC_GROUP, 0, CONFIGURABLE_ID_IN_ESC_GROUP)

CONFIG_PARAM_INT("ttl_milliseconds", 500, 4, 500)

CONFIG_PARAM_INT("uavcan.pub.esc_heartbeat.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.esc_feedback.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.esc_power.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_INT("uavcan.pub.esc_dynamics.id", CONFIGURABLE_SUBJECT_ID, 0, CONFIGURABLE_SUBJECT_ID)

CONFIG_PARAM_BOOL("control_mode_rpm", true)

struct : IHandler
{
    void operator()(node::state::State &_state, CanardRxTransfer *transfer)
    {
        (void) _state;
        (void) transfer;
    }
} empty_handler;

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
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(setpoint, reg_udral_service_actuator_common_sp_Scalar,
                                             0, 1,
                                             &setpoint_handler),
        CONFIGURABLE_ID_MESSAGE_SUBSCRIPTION(readiness, reg_udral_service_common_Readiness,
                                             0, 1,
                                             &sub_readiness_handler)
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
#if BXCAN_MAX_IFACE_INDEX > 0
        RCC->APB1ENR |= RCC_APB1ENR_CAN2EN;
        RCC->APB1RSTR |= RCC_APB1RSTR_CAN2RST;
        RCC->APB1RSTR &= ~RCC_APB1RSTR_CAN2RST;
#endif
    }
    BxCANTimings timings{};
    bxCANComputeTimings(STM32_PCLK1, 1'000'000, &timings); // uavcan.can.bitrate
    for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
    {
        printf("%d\n", bxCANConfigure(i, timings, false));
    }
    state.canard = canardInit(&canardAllocate, &canardFree);
    for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
    {
        state.queues[i] = canardTxInit(100, 8);
    }
    ConfigParam _{};
    bool value_exists = false;//configGetDescr("uavcan.node.id", &_) != -ENOENT;
    float stored_node_id = CANARD_NODE_ID_UNSET;
    if (value_exists)
    {
        stored_node_id = configGet("uavcan.node.id");
    }
    if (stored_node_id == NAN)
    {
        state.canard.node_id = CANARD_NODE_ID_UNSET;
    } else
    {
        state.canard.node_id = stored_node_id;
    }

    if (configGetDescr("id_in_esc_group", &_) != -ENOENT)
    {
        state.id_in_esc_group = configGet("id_in_esc_group");
        if (state.id_in_esc_group == CONFIGURABLE_ID_IN_ESC_GROUP)
        {
            printf("no id_in_esc_group\n");

        }
    }
    if (configGetDescr("ttl_milliseconds", &_) != -ENOENT)
    {
        state.ttl_milliseconds = configGet("ttl_milliseconds");
    }

    if (configGetDescr("control_mode_rpm", &_) != -ENOENT)
    {
        state.control_mode = configGet("control_mode_rpm") == true ? ControlMode::RPM : ControlMode::DUTYCYCLE;
    }
    if (configGetDescr("uavcan.pub.esc_heartbeat.id", &_) != -ENOENT)
    {
        state.esc_heartbeat_publish_port = configGet("uavcan.pub.esc_heartbeat.id");
        if (state.esc_heartbeat_publish_port == CONFIGURABLE_SUBJECT_ID)
        {
            printf("no uavcan.pub.esc_heartbeat.id\n");

        }
    }
    if (configGetDescr("uavcan.pub.esc_feedback.id", &_) != -ENOENT)
    {
        state.esc_feedback_publish_port = configGet("uavcan.pub.esc_feedback.id");
        if (state.esc_feedback_publish_port == CONFIGURABLE_SUBJECT_ID)
        {
            printf("no uavcan.pub.esc_feedback.id\n");
        }
    }
    state.timing.started_at = get_monotonic_microseconds();
    for (auto &registered_port: registered_ports)
    {
        if (registered_port.subscription.port_id == CONFIGURABLE_SUBJECT_ID)
        {
            if (configGetDescr(registered_port.name, &_) != -ENOENT)
            {
                float new_port = configGet(registered_port.name);
                if ((int) new_port == CONFIGURABLE_SUBJECT_ID)
                {
                    printf("no %s\n", registered_port.name);
                    continue;
                }
                registered_port.subscription.port_id = new_port;
            } else
            {
                printf("no %s\n", registered_port.type);
                continue;
            }
        }
        const int8_t res =  //
            canardRxSubscribe(&state.canard,
                              registered_port.transfer_kind,
                              registered_port.subscription.port_id,
                              registered_port.subscription.extent,
                              registered_port.subscription.transfer_id_timeout_usec,
                              &registered_port.subscription);

        if (registered_port.subscription.user_reference == nullptr)
        {
            printf("no handler %s\n", registered_port.name);
            continue;
        }
        if (res < 0)
        {
            printf("canardRxSubscribe error: %d\n", res);
        }
        chThdSleepMicroseconds(400);
        assert(res >= 0); // This is to make sure that the subscription was successful.
        printf("New sub %s: %d, res=%d\n", registered_port.name, registered_port.subscription.port_id, res);
    }
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
