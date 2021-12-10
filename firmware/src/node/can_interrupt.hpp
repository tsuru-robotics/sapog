/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include "fifo_queue.hpp"
#include "libcanard/canard.h"

#define DEVICE_MAX_QUEUES (3)
#define DEVICE_QUEUE_FULL_TIME_us (192)
// This is just the number I remember from looking at the logic analyzer showing signals from test points toggled by
// reception
#define PROCESSING_DELAY_us (700)
#define REQUIRED_FRAME_BUFFERS ((std::uint8_t)(PROCESSING_DELAY_us / DEVICE_QUEUE_FULL_TIME_us * DEVICE_MAX_QUEUES)+1)
struct fifo_queue_item
{
  CanardFrame frame;
  std::array<std::uint8_t, 8> payload;
  size_t payload_size;
  uint32_t extended_can_id;
};
namespace can_interrupt
{
using frame = fifo_queue_item;
extern std::array<silver_template_library::Queue<frame, REQUIRED_FRAME_BUFFERS>, BXCAN_MAX_IFACE_INDEX>
  fifo_queues;
}
