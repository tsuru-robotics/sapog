/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <hal.h>
#include "reception.hpp"

extern "C" {
/**
* IRQ handler macros
*/
# define UAVCAN_STM32_IRQ_HANDLER(id)  CH_IRQ_HANDLER(id)
# define UAVCAN_STM32_IRQ_PROLOGUE()    CH_IRQ_PROLOGUE()
# define UAVCAN_STM32_IRQ_EPILOGUE()    CH_IRQ_EPILOGUE()

/**
 * Priority mask for timer and CAN interrupts.
 */


UAVCAN_STM32_IRQ_HANDLER(STM32_CAN2_RX0_HANDLER);

UAVCAN_STM32_IRQ_HANDLER(STM32_CAN2_RX1_HANDLER);

UAVCAN_STM32_IRQ_HANDLER(STM32_CAN1_RX0_HANDLER);

UAVCAN_STM32_IRQ_HANDLER(STM32_CAN1_RX1_HANDLER);

UAVCAN_STM32_IRQ_HANDLER(STM32_CAN2_RX0_HANDLER)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  //UAVCAN_STM32_IRQ_PROLOGUE();
  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  receive_and_queue_for_processing(1);
  UAVCAN_STM32_IRQ_EPILOGUE();
}


UAVCAN_STM32_IRQ_HANDLER(STM32_CAN2_RX1_HANDLER)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  receive_and_queue_for_processing(1);
  UAVCAN_STM32_IRQ_EPILOGUE();
}


UAVCAN_STM32_IRQ_HANDLER(STM32_CAN1_RX0_HANDLER)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  receive_and_queue_for_processing(0);
  UAVCAN_STM32_IRQ_EPILOGUE();
}


UAVCAN_STM32_IRQ_HANDLER(STM32_CAN1_RX1_HANDLER)
{
  UAVCAN_STM32_IRQ_PROLOGUE();
  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  receive_and_queue_for_processing(0);
  UAVCAN_STM32_IRQ_EPILOGUE();
}
}
