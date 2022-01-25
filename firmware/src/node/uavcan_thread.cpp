/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#define NUNAVUT_ASSERT assert

#include "uavcan_thread.hpp"
#include "loops.hpp"
#include "src/node/state/state.hpp"
#include "units.hpp"
#include <node/loops/loop.hpp>
#include "board/board.hpp"
#include <ch.h>
#include "time.h"
#include <cstddef>
#include "libcanard/canard.h"
#include <bxcan/bxcan_registers.h>
#include "print_can_error.hpp"
#include "node/register_values/subscriptions.hpp"
#include "init_can.hpp"


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

static THD_WORKING_AREA(_wa_uavcan_thread,
                        1024 * 4);

[[noreturn]] static void uavcan_thread(void *arg)
{
  (void) arg;
  init_canard();
  chRegSetThreadName("uavcan_thread");
  state.plug_and_play.anonymous = state.canard.node_id > CANARD_NODE_ID_MAX;
  node::pnp::plug_and_play_loop(state);
  enable_interrupt_handlers();
  printf("Has this node_id after pnp: %d\n", state.canard.node_id);
  // This is the main loop of the uavcan_thread
  while (true)
  {
    print_can_error_if_exists();
    if (state.is_save_requested)
    {
      configSave();
      state.is_save_requested = false;
    }
    if (!state.is_save_requested && state.is_restart_required && !os::isRebootRequested())
    {
      printf("Sent %d remaining frames before restarting\n", transmit(state));
      os::requestReboot(); // This actually runs multiple times, like 7 usually, just puts up a flag
    }
    CanardMicrosecond current_time = get_monotonic_microseconds();
    // These are loops because they are run in repeatedly according to their run delays.
    // A neat feature is that a loop can change its delay when needed but this hasn't been used.
    for (Loop &loop: node::loops::loops)
    {
      if (loop.is_time_to_execute(current_time))
      {
        loop.handler(state);
        loop.increment_next_execution();
      }
    }
    chThdSleepMicroseconds(100);
  }
}




/// Get a pair of iterators, one points to the start of the subscriptions array and the other points to the end of it.

int uavcan_node_1_0::init()
{
  if (!chThdCreateStatic(_wa_uavcan_thread, sizeof(_wa_uavcan_thread), NORMALPRIO, uavcan_thread,
                         nullptr))
  {
    return -1;
  }
  return 0;
}
