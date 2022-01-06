/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <bxcan/bxcan.h>
#include <assert.h>
#include <cstdio>
#include <stm32f105xc.h>
#include <hal.h>
#include "transmit.hpp"
#include "src/node/state/state.hpp"
#include "libcanard/canard.h"
#include "time.h"
#include "board/board.hpp"

using namespace node::state;

/// Uses bxCAN to send all frames that have been queued in canard, returns the amount of frames that were sent
int transmit(State &state)
{
  int count_sent_frames = 0;
  for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
  {
    for (const CanardTxQueueItem *txf = NULL;
         (txf = canardTxPeek(&state.queues[i])) != nullptr;)  // Look at the top of the TX queue.
    {
      bool is_driver_busy = !bxCANPush(i, get_monotonic_microseconds(), (*txf).tx_deadline_usec,
                                       (*txf).frame.extended_can_id, (*txf).frame.payload_size,
                                       (*txf).frame.payload);
      if (!is_driver_busy)
      {
        assert(txf != nullptr);
        count_sent_frames++;
        state.canard.memory_free(&state.canard, canardTxPop(&state.queues[i], txf));
      } else
      { break; }
    }
  }
  return count_sent_frames;
}
