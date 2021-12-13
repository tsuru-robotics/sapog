/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "fifo_queue.hpp"
#include "libcanard/canard.h"

#define DEVICE_MAX_QUEUES (3U)
#define DEVICE_QUEUE_FULL_TIME_us (192U)
// This is just the number I remember from looking at the logic analyzer showing signals from test points toggled by
// reception
#define PROCESSING_DELAY_us (700U)
#define REQUIRED_FRAME_BUFFERS ((std::uint8_t)(PROCESSING_DELAY_us / DEVICE_QUEUE_FULL_TIME_us * DEVICE_MAX_QUEUES*2)+1U)
struct fifo_queue_item
{
  CanardFrame frame;
};
namespace can_interrupt
{
using frame = fifo_queue_item;
extern std::array<silver_template_library::Queue<frame, REQUIRED_FRAME_BUFFERS + 100>, BXCAN_MAX_IFACE_INDEX>
  fifo_queues;
}
