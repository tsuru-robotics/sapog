/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <cstdint>
#include <cstdio>
#include "print_can_error.hpp"

//#define SHOW_PENDING_MESSAGE_COUNT
//#define SHOW_IF_QUEUE_FULL
//#define SHOW_IF_QUEUE_OVERRUN
//#define SHOW_INTERRUPT_ENABLE_REGISTER_STATUS

void print_can_error_if_exists()
{
  uint32_t CAN1_RF0R = BXCAN1->RF0R;
  uint32_t CAN1_RF1R = BXCAN1->RF1R;
  uint32_t CAN2_RF0R = BXCAN2->RF0R;
  uint32_t CAN2_RF1R = BXCAN2->RF1R;
  (void) CAN1_RF0R;
  (void) CAN1_RF1R;
  (void) CAN2_RF0R;
  (void) CAN2_RF1R;
#ifdef SHOW_PENDING_MESSAGE_COUNT
  // Page 680 beginning: FMP0[1:0]
  printf("CAN1 FIF0 has %d pending messages.", (uint8_t) (0b11 & CAN1_RF0R));
  printf("CAN1 FIF1 has %d pending messages.", (uint8_t) (0b11 & CAN1_RF1R));
  printf("CAN2 FIF0 has %d pending messages.", (uint8_t) (0b11 & CAN2_RF0R));
  printf("CAN2 FIF1 has %d pending messages.", (uint8_t) (0b11 & CAN2_RF1R));
#endif
#ifdef SHOW_IF_QUEUE_FULL
  if ((CAN1_RF0R & 0b100) > 0)
  {
    printf("CAN1 FIFO0 full\n");
  }
  if ((CAN1_RF1R & 0b100) > 0)
  {
    printf("CAN1 FIFO1 full\n");
  }
  if ((CAN1_RF0R & 0b100) > 0)
  {
    printf("CAN2 FIFO0 full\n");
  }
  if ((CAN1_RF1R & 0b100) > 0)
  {
    printf("CAN2 FIFO1 full\n");
  }
#endif
#ifdef SHOW_IF_QUEUE_OVERRUN
  if (CAN1_RF0R & 0b1000)
  {
    printf("CAN1 FIFO0 overrun\n");
  }
  if (CAN1_RF1R & 0b1000)
  {
    printf("CAN1 FIFO1 overrun\n");
  }
  if (CAN1_RF0R & 0b1000)
  {
    printf("CAN2 FIFO0 overrun\n");
  }
  if (CAN1_RF1R & 0b1000)
  {
    printf("CAN2 FIFO1 overrun\n");
  }
#endif
#ifdef SHOW_INTERRUPT_ENABLE_REGISTER_STATUS
  // Bit 0: TMEIE
  if (BXCAN1->IER & 0b1)
  {
    printf("CAN1 Transmit mailbox empty interrupt enabled\n");
  }
  // Bit 1: FMPIE0
  if (BXCAN1->IER & 0b10)
  {
    printf("CAN1 FIFO0 message pending interrupt enabled\n");
  }
  // Bit 2: FFIE0
  if (BXCAN1->IER & 0b100)
  {
    // Interrupt generated when FULL bit is set.
    printf("CAN1 FIFO0 full interrupt enabled\n");
  }
  // Bit 3: FOVIE0
  if (BXCAN1->IER & 0b1000)
  {
    // Interrupt generated when FOVR bit is set.
    printf("CAN1 FIFO0 overrun interrupt enable\n");
  }
  // Bit 4: FMPIE1
  if (BXCAN1->IER & 0b10000)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN1 FIFO1 message pending interrupt enabled\n");
  }
  // Bit 5: FFIE1
  if (BXCAN1->IER & 0b10000'0)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN1 FIFO1 full interrupt enabled\n");
  }
  // Bit 6: FOVIE1
  if (BXCAN1->IER & 0b1'0000'00)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN1 FIFO overrun interrupt enable\n");
  }
  // Bit 7 is reserved
  // Bit 8: EWGIE
  if (BXCAN1->IER & 0b1'0000'0000)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN1 Error warning interrupt enabled\n");
  }
  // Bit 9: EPVIE
  if (BXCAN1->IER & (1U << 9U))
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN1 Error passive interrupt enabled\n");
  }
  // Bit 10: BOFIE
  if (BXCAN1->IER & (1U << 10U))
  {
    // ERRI bit will be set when BOFF is set.
    printf("CAN1 Bus-off interrupt enabled\n");
  }
  // Bit 11: LECIE
  if (BXCAN1->IER & (1U << 11U))
  {
    // ERRI bit will be set when the error code in LEC[2:0]
    // is set by hardware on error detection.
    printf("CAN1 Last error code interrupt enabled\n");
  }
  // Bits 14:12 are reserved
  // Bit 15: ERRIE
  if (BXCAN1->IER & (1U << 15U))
  {
    // An interrupt will be generated when an error condition is pending
    // in the CAN_ESR
    printf("CAN1 Error interrupt enabled\n");
  }
  // Bit 16: WKUIE
  if (BXCAN1->IER & (1U << 16U))
  {
    // Interrupt generated when WKUI bit is set.
    printf("CAN1 Wakeup interrupt enabled\n");
  }
  // Bit 17: SLKIE
  if (BXCAN1->IER & (1U << 16U))
  {
    // Interrupt generated when SLAKI bit is set
    printf("CAN1 Sleep interrupt enabled\n");
  }



  // Bit 0: TMEIE
  if (BXCAN2->IER & 0b1)
  {
    printf("CAN2 Transmit mailbox empty interrupt enabled\n");
  }
  // Bit 1: FMPIE0
  if (BXCAN2->IER & 0b10)
  {
    printf("CAN2 FIFO0 message pending interrupt enabled\n");
  }
  // Bit 2: FFIE0
  if (BXCAN2->IER & 0b100)
  {
    // Interrupt generated when FULL bit is set.
    printf("CAN2 FIFO0 full interrupt enabled\n");
  }
  // Bit 3: FOVIE0
  if (BXCAN2->IER & 0b1000)
  {
    // Interrupt generated when FOVR bit is set.
    printf("CAN2 FIFO0 overrun interrupt enable\n");
  }
  // Bit 4: FMPIE1
  if (BXCAN2->IER & 0b10000)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN2 FIFO1 message pending interrupt enabled\n");
  }
  // Bit 5: FFIE1
  if (BXCAN2->IER & 0b10000'0)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN2 FIFO1 full interrupt enabled\n");
  }
  // Bit 6: FOVIE1
  if (BXCAN2->IER & 0b1'0000'00)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN2 FIFO overrun interrupt enable\n");
  }
  // Bit 7 is reserved
  // Bit 8: EWGIE
  if (BXCAN2->IER & 0b1'0000'0000)
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN2 Error warning interrupt enabled\n");
  }
  // Bit 9: EPVIE
  if (BXCAN2->IER & (1U << 9U))
  {
    // Interrupt generated when state of FMP[1:0] bits are not 00b
    printf("CAN2 Error passive interrupt enabled\n");
  }
  // Bit 10: BOFIE
  if (BXCAN2->IER & (1U << 10U))
  {
    // ERRI bit will be set when BOFF is set.
    printf("CAN2 Bus-off interrupt enabled\n");
  }
  // Bit 11: LECIE
  if (BXCAN2->IER & (1U << 11U))
  {
    // ERRI bit will be set when the error code in LEC[2:0]
    // is set by hardware on error detection.
    printf("CAN2 Last error code interrupt enabled\n");
  }
  // Bits 14:12 are reserved
  // Bit 15: ERRIE
  if (BXCAN2->IER & (1U << 15U))
  {
    // An interrupt will be generated when an error condition is pending
    // in the CAN_ESR
    printf("CAN2 Error interrupt enabled\n");
  }
  // Bit 16: WKUIE
  if (BXCAN2->IER & (1U << 16U))
  {
    // Interrupt generated when WKUI bit is set.
    printf("CAN2 Wakeup interrupt enabled\n");
  }
  // Bit 17: SLKIE
  if (BXCAN2->IER & (1U << 16U))
  {
    // Interrupt generated when SLAKI bit is set
    printf("CAN2 Sleep interrupt enabled\n");
  }

#endif
}
