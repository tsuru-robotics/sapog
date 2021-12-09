/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once
/**
 * IRQ handler macros
 */
# define UAVCAN_STM32_IRQ_HANDLER(id)  CH_IRQ_HANDLER(id)
# define UAVCAN_STM32_IRQ_PROLOGUE()    CH_IRQ_PROLOGUE()
# define UAVCAN_STM32_IRQ_EPILOGUE()    CH_IRQ_EPILOGUE()

/**
 * Priority mask for timer and CAN interrupts.
 */
# ifndef UAVCAN_STM32_IRQ_PRIORITY_MASK
#  if (CH_KERNEL_MAJOR == 2)
#   define UAVCAN_STM32_IRQ_PRIORITY_MASK  CORTEX_PRIORITY_MASK(CORTEX_MAX_KERNEL_PRIORITY)
#  else // ChibiOS 3+
#   define UAVCAN_STM32_IRQ_PRIORITY_MASK  CORTEX_MAX_KERNEL_PRIORITY
#  endif
# endif

UAVCAN_STM32_IRQ_HANDLER(CAN2_RX0_IRQHandler);

UAVCAN_STM32_IRQ_HANDLER(CAN2_RX1_IRQHandler);

UAVCAN_STM32_IRQ_HANDLER(CAN1_RX0_IRQHandler);

UAVCAN_STM32_IRQ_HANDLER(CAN1_RX1_IRQHandler);
