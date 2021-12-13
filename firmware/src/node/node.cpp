/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#define NUNAVUT_ASSERT assert

#include "node.hpp"
#include "loops.hpp"
#include "src/node/state/state.hpp"
#include "units.hpp"
#include <node/loops/loop.hpp>
#include "board/board.hpp"
#include <ch.h>
#include "time.h"
#include <cstddef>
#include "bxcan/bxcan.h"
#include "libcanard/canard.h"
#include "uavcan/_register/Access_1_0.h"
#include "reg/udral/physics/acoustics/Note_0_1.h"
#include <uavcan/si/unit/angular_velocity/Scalar_1_0.h>
#include "node/commands/commands.hpp"
#include <uavcan/node/ExecuteCommand_1_1.h>
#include <node/essential/access.hpp>
#include <node/essential/get_info.hpp>
#include "node/essential/note.hpp"
#include "node/essential/register_list.hpp"
#include <node/esc/esc.hpp>
#include <bxcan/bxcan_registers.h>
#include <node/esc/readiness.hpp>
#include "src/node/can_interrupt/can_interrupt_handler.hpp"
#include "print_can_error.hpp"
#include "node_config_macros/node_config.hpp"
#include "node/dynamic_port_ids/registered_ports.hpp"
#include "node/dynamic_port_ids/publish_configurable_port.hpp"

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
  {
    nvicEnableVector(CAN1_RX0_IRQn, CORTEX_MINIMUM_PRIORITY);
    nvicEnableVector(CAN1_RX1_IRQn, CORTEX_MINIMUM_PRIORITY);
# if BXCAN_MAX_IFACE_INDEX > 0
    nvicEnableVector(CAN2_RX0_IRQn, CORTEX_MINIMUM_PRIORITY);
    nvicEnableVector(CAN2_RX1_IRQn, CORTEX_MINIMUM_PRIORITY);
# endif
  }
  // Loops are created

  static Loop loops[]{Loop{handle_1hz_loop, SECOND_IN_MICROSECONDS, get_monotonic_microseconds()},
                      Loop{handle_fast_loop, QUEUE_TIME_FRAME, get_monotonic_microseconds()},
                      Loop{handle_5_second_loop, SECOND_IN_MICROSECONDS * 5, get_monotonic_microseconds()},
                      Loop{handle_esc_status_loop, SECOND_IN_MICROSECONDS / 10, get_monotonic_microseconds()}
  };
  printf("Has this node_id after pnp: %d\n", state.canard.node_id);
  // Loops begin running
  while (true)
  {
    print_can_error_if_exists();
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


CONFIG_PARAM_INT("id_in_esc_group", CONFIGURABLE_ID_IN_ESC_GROUP, 0, CONFIGURABLE_ID_IN_ESC_GROUP)


CONFIG_PARAM_INT("ttl_milliseconds", 500, 4, 500)


CONFIG_PARAM_BOOL("control_mode_rpm", true)

struct : IHandler
{
  void operator()(node::state::State &_state, CanardRxTransfer *transfer)
  {
    (void) _state;
    (void) transfer;
  }
} empty_handler;



/// Get a pair of iterators, one points to the start of the subscriptions array and the other points to the end of it.


static void init_canard()
{
  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));

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
  for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
  {
    for (int j = 0; j < 3; ++j)
    {
      receive_and_queue_for_processing(i);
    }
  }
  accept_transfers(state);
//  {
//    os::CriticalSectionLocker lock;
//    BXCAN1->IER = BXCAN_IER_TMEIE | BXCAN_IER_FMPIE0 | BXCAN_IER_FFIE0 | BXCAN_IER_FOVIE0 |
//                  BXCAN_IER_FMPIE1 | BXCAN_IER_FFIE1 | BXCAN_IER_FOVIE1 | BXCAN_IER_EWGIE |
//                  BXCAN_IER_EPVIE | BXCAN_IER_BOFIE | BXCAN_IER_LECIE | BXCAN_IER_ERRIE |
//                  BXCAN_IER_WKUIE | BXCAN_IER_SLKIE;
//# if BXCAN_MAX_IFACE_INDEX > 0
//    BXCAN2->IER = BXCAN_IER_TMEIE | BXCAN_IER_FMPIE0 | BXCAN_IER_FFIE0 | BXCAN_IER_FOVIE0 |
//                  BXCAN_IER_FMPIE1 | BXCAN_IER_FFIE1 | BXCAN_IER_FOVIE1 | BXCAN_IER_EWGIE |
//                  BXCAN_IER_EPVIE | BXCAN_IER_BOFIE | BXCAN_IER_LECIE | BXCAN_IER_ERRIE |
//                  BXCAN_IER_WKUIE | BXCAN_IER_SLKIE;
//#endif
//  }

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
#ifdef FORGET_NODE_ID
  bool value_exists = false;
#else
  bool value_exists = configGetDescr("uavcan.node.id", &_) != -ENOENT;
#endif
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

  if (configGetDescr("control_mode_rpm", &_) != -ENOENT)
  {
    state.control_mode = configGet("control_mode_rpm") == true ? ControlMode::RPM : ControlMode::DUTYCYCLE;
  }
  for (auto &publish_port: publish_ports)
  {
    if (configGetDescr(publish_port.name.data(), &_) != -ENOENT)
    {
      *publish_port.state_variable = configGet(publish_port.name.data());
      if (*publish_port.state_variable == CONFIGURABLE_SUBJECT_ID)
      {
        printf("no %s\n", publish_port.name.data());
      } else
      {
        printf("has %s\n", publish_port.name.data());
      }
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

int UAVCANNode::init()
{
  if (!chThdCreateStatic(_wa_control_thread, sizeof(_wa_control_thread), NORMALPRIO, control_thread, nullptr))
  {
    return -1;
  }
  return 0;
}
