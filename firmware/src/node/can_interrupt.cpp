/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <cstdint>
#include "can_interrupt.hpp"
#include "fifo_queue.hpp"

namespace can_interrupt
{
// 3 queues get filled in 192 microseconds, 5 * 192 microseconds is more than the time it takes for something to process
// the queue while the motor is running on a higher priority thread (approximately 700 microseconds)
std::array<silver_template_library::Queue<frame, REQUIRED_FRAME_BUFFERS + 100>, BXCAN_MAX_IFACE_INDEX>
  fifo_queues{};
}
