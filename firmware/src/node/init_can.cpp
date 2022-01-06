/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <cerrno>
#include "init_can.hpp"
#include "libcanard/canard.h"
#include "board/board.hpp"
#include "reception.hpp"
#include "node/register_values/register_variables.hpp"
#include "node_config_macros/node_config.hpp"
#include "node/register_values/parameters.hpp"
#include "node/node_config_macros/node_config.hpp"
#include "board/board.hpp"

static void *canardAllocate(CanardInstance *const ins, const size_t amount)
{
  (void) ins;
  return board::allocate(amount);
}

static void canardFree(CanardInstance *const ins, void *const pointer)
{
  (void) ins;
  board::deallocate(pointer);
}

void init_canard()
{
  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  {
    /* https://www.st.com/resource/en/reference_manual/rm0008-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
    AHB/APB bridges (APB) page 49
    Turning on the clocks for the peripherals that are going to be used
    */
    RCC->APB1ENR |= RCC_APB1ENR_CAN1EN;
    RCC->APB1RSTR |= RCC_APB1RSTR_CAN1RST;
    RCC->APB1RSTR &= ~RCC_APB1RSTR_CAN1RST;
    printf("Current minor version is %d\n", board::detect_hardware_version().minor);
#if BXCAN_MAX_IFACE_INDEX > 0
    if (board::get_max_can_interface_index() > 0)
    {
      RCC->APB1ENR |= RCC_APB1ENR_CAN2EN;
      RCC->APB1RSTR |= RCC_APB1RSTR_CAN2RST;
      RCC->APB1RSTR &= ~RCC_APB1RSTR_CAN2RST;
    }
#endif
  }
  for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
  {
    for (int j = 0; j < 3; ++j)
    {
      receive_and_queue_for_processing(i);
    }
  }
  accept_transfers(state);

  BxCANTimings timings{};
  bxCANComputeTimings(STM32_PCLK1, 1'000'000, &timings); // uavcan.can.bitrate
  for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
  {
    printf("%d\n", bxCANConfigure(i, timings, false));
  }

  state.canard = canardInit(&canardAllocate, &canardFree);
  for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
  {
    state.queues[i] = canardTxInit(100, 8);
  }
  ConfigParam _{};
#ifdef FORGET_NODE_ID
  bool value_exists = false;
#else
  bool value_exists = configGetDescr("uavcan.node.id", &_) != -ENOENT;
#endif
  float stored_node_id = CANARD_NODE_ID_UNSET;
  if (value_exists)
  {
    stored_node_id = configGet("uavcan.node.id");
  }
  if (stored_node_id == NAN)
  {
    state.canard.node_id = CANARD_NODE_ID_UNSET;
  } else
  {
    state.canard.node_id = stored_node_id;
  }

  if (configGetDescr("control_mode_rpm", &_) != -ENOENT)
  {
    state.control_mode = configGet("control_mode_rpm") == true ? ControlMode::RPM : ControlMode::DUTYCYCLE;
  }
  auto it_pair = get_publish_port_iterators();

  for (auto &publish_port = it_pair.first; publish_port != it_pair.second; publish_port++)
  {
    if (configGetDescr(publish_port->name.data(), &_) != -ENOENT)
    {
      *publish_port->state_variable = configGet(publish_port->name.data());
      if (*publish_port->state_variable == CONFIGURABLE_SUBJECT_ID)
      {
        printf("no %s\n", publish_port->name.data());
      } else
      {
        printf("has %s\n", publish_port->name.data());
      }
    }
  }
  auto it_pair3 = get_state_variables_in_registers();
  for (auto &svir = it_pair3.first; svir != it_pair3.second; svir++)
  {
    if (configGetDescr(svir->name.data(), &_) != -ENOENT)
    {
      *svir->state_variable = configGet(svir->name.data());
      printf("has %s\n", svir->name.data());
    } else
    {
      printf("no %s\n", svir->name.data());
    }
  }
  if (state.id_in_esc_group != 255)
  {
    printf("id_in_esc_group=%d\n", state.id_in_esc_group);
  }
  state.timing.started_at = get_monotonic_microseconds();
  auto it_pair2 = get_dyn_subscription_iterators();
  for (auto subscription = it_pair2.first; subscription != it_pair2.second; subscription++)
  {
    if (subscription->subscription.port_id == CONFIGURABLE_SUBJECT_ID)
    {
      if (configGetDescr(subscription->name, &_) != -ENOENT)
      {
        float new_port = configGet(subscription->name);
        if ((int) new_port == CONFIGURABLE_SUBJECT_ID)
        {
          printf("no %s\n", subscription->name);
          continue;
        }
        subscription->subscription.port_id = new_port;
      } else
      {
        printf("no %s\n", subscription->type);
        continue;
      }
    }
    const int8_t res =
      canardRxSubscribe(&state.canard,
                        subscription->transfer_kind,
                        subscription->subscription.port_id,
                        subscription->subscription.extent,
                        subscription->subscription.transfer_id_timeout_usec,
                        &subscription->subscription);

    if (subscription->subscription.user_reference == nullptr)
    {
      printf("no handler %s\n", subscription->name);
      continue;
    }
    if (res < 0)
    {
      printf("canardRxSubscribe error: %d\n", res);
    }
    chThdSleepMicroseconds(400);
    assert(res >= 0); // This is to make sure that the subscription was successful.
    printf("New sub %s: %d, res=%d\n", subscription->name, subscription->subscription.port_id, res);
  }
}
