/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <hal.h>
#include "reception.hpp"
#include "can_interrupt_handler.hpp"

UAVCAN_STM32_IRQ_HANDLER(CAN2_RX0_IRQHandler)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  receive_and_queue_for_processing(2);
  UAVCAN_STM32_IRQ_EPILOGUE();
}


UAVCAN_STM32_IRQ_HANDLER(CAN2_RX1_IRQHandler)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  receive_and_queue_for_processing(2);
  UAVCAN_STM32_IRQ_EPILOGUE();
}


UAVCAN_STM32_IRQ_HANDLER(CAN1_RX0_IRQHandler)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  receive_and_queue_for_processing(1);
  UAVCAN_STM32_IRQ_EPILOGUE();
}


UAVCAN_STM32_IRQ_HANDLER(CAN1_RX1_IRQHandler)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  receive_and_queue_for_processing(1);
  UAVCAN_STM32_IRQ_EPILOGUE();
}