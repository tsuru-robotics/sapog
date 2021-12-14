/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#define NUNAVUT_ASSERT assert

#include "node_control_thread.hpp"
#include "loops.hpp"
#include "src/node/state/state.hpp"
#include "units.hpp"
#include <node/loops/loop.hpp>
#include "board/board.hpp"
#include <ch.h>
#include "time.h"
#include <cstddef>
#include "libcanard/canard.h"
#include <node/essential/access.hpp>
#include <bxcan/bxcan_registers.h>
#include "print_can_error.hpp"
#include "node/dynamic_port_ids/registered_ports.hpp"
#include "init_can.hpp"


#define CONFIGURABLE_SUBJECT_ID 0xFFFF


extern void board::die(int error);

extern void *const ConfigStorageAddress;
constexpr unsigned ConfigStorageSize = 1024;

using namespace uavcan_node_1_0;
using namespace board;

void enable_interrupt_handlers()
{
  nvicEnableVector(CAN1_RX0_IRQn, CORTEX_MINIMUM_PRIORITY);
  nvicEnableVector(CAN1_RX1_IRQn, CORTEX_MINIMUM_PRIORITY);
# if BXCAN_MAX_IFACE_INDEX > 0
  nvicEnableVector(CAN2_RX0_IRQn, CORTEX_MINIMUM_PRIORITY);
  nvicEnableVector(CAN2_RX1_IRQn, CORTEX_MINIMUM_PRIORITY);
# endif
}

// This defines _wa_control_thread
static THD_WORKING_AREA(_wa_uavcan_thread,
                        1024 * 4);


[[noreturn]] static void uavcan_thread(void *arg)
{
  using namespace node::loops;
  (void) arg;
  init_canard();
  chRegSetThreadName("uavcan_thread");
  state.plug_and_play.anonymous = state.canard.node_id > CANARD_NODE_ID_MAX;
  node::pnp::plug_and_play_loop(state);
  enable_interrupt_handlers();
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

/// Get a pair of iterators, one points to the start of the subscriptions array and the other points to the end of it.

int UAVCANNode::init()
{
  if (!chThdCreateStatic(_wa_uavcan_thread, sizeof(_wa_uavcan_thread), NORMALPRIO, uavcan_thread,
                         nullptr))
  {
    return -1;
  }
  return 0;
}
