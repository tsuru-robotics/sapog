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
  CanardFrame frame{};
  std::array<std::uint8_t, CANARD_MTU_CAN_CLASSIC> payload{};

  fifo_queue_item() noexcept
  {
    frame.payload = payload.data();
  }

  ~fifo_queue_item() noexcept = default;

  fifo_queue_item(const fifo_queue_item &other) noexcept: frame(other.frame), payload(other.payload)
  {
    frame.payload = payload.data();
  }

  auto operator=(
    const fifo_queue_item &other
  ) noexcept -> fifo_queue_item &
  {
    frame = other.frame;
    payload = other.payload;
    frame.payload = payload.data();
    return *this;
  }

  fifo_queue_item(const fifo_queue_item &&other) = delete;

  auto operator=(
    const fifo_queue_item &&other
  ) noexcept -> fifo_queue_item & = delete;
};
namespace can_interrupt
{
using frame = fifo_queue_item;
extern std::array<silver_template_library::Queue<frame, REQUIRED_FRAME_BUFFERS + 70>, BXCAN_MAX_IFACE_INDEX + 1>
  fifo_queues;
}
