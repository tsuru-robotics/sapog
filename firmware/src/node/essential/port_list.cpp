/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <uavcan/node/port/List_0_1.h>
#include <uavcan/node/Heartbeat_1_0.h>
#include <node/units.hpp>
#include "src/node/uavcan_thread.hpp"
#include <cstdio>
#include <node/time.h>
#include "port_list.hpp"
#include "board/board.hpp"

void publish_port_list(CanardInstance &canard, node::state::State &state)
{
  (void) canard;
  uavcan_node_port_List_0_1 m{};
  uavcan_node_port_List_0_1_initialize_(&m);
  uavcan_node_port_SubjectIDList_0_1_select_sparse_list_(&m.publishers);
  uavcan_node_port_SubjectIDList_0_1_select_sparse_list_(&m.subscribers);
  // Indicate which subjects we publish to. Don't forget to keep this updated if you add new publications!
  {
    size_t *const cnt = &m.publishers.sparse_list.count;
    m.publishers.sparse_list.elements[(*cnt)++].value = uavcan_node_Heartbeat_1_0_FIXED_PORT_ID_;
    m.publishers.sparse_list.elements[(*cnt)++].value = uavcan_node_port_List_0_1_FIXED_PORT_ID_;
  }

  auto iterators = get_dyn_subscription_iterators();
  for (auto iter = iterators.first; iter < iterators.second; iter++)
  {
    if (iter->transfer_kind == CanardTransferKindRequest)
    {
      nunavutSetBit(&m.servers.mask_bitpacked_[0], sizeof(m.servers.mask_bitpacked_), iter->subscription.port_id,
                    true);
    } else
    {
      m.subscribers.sparse_list.elements[m.subscribers.sparse_list.count++].value = iter->subscription.port_id;
    }
  }
  // Notice that we don't check the clients because our application doesn't invoke any services.

  // Serialize and publish the message. Use a small buffer because we know that our message is always small.
  uint8_t serialized[512] = {0};  // https://github.com/UAVCAN/nunavut/issues/191
  size_t serialized_size = uavcan_node_port_List_0_1_SERIALIZATION_BUFFER_SIZE_BYTES_;
  if (uavcan_node_port_List_0_1_serialize_(&m, &serialized[0], &serialized_size) >= 0)
  {
    CanardTransferMetadata rtm{};
    rtm.transfer_kind = CanardTransferKindMessage;
    rtm.port_id = uavcan_node_port_List_0_1_FIXED_PORT_ID_;
    rtm.remote_node_id = CANARD_NODE_ID_UNSET;
    rtm.priority = CanardPriorityOptional;
    rtm.transfer_id = (CanardTransferID) (state.transfer_ids.uavcan_node_port_list++);
    for (int i = 0; i <= board::detect_hardware_version().minor; ++i)
    {
      int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                       const_cast<CanardInstance *>(&state.canard),
                                                       get_monotonic_microseconds() +
                                                       ONE_SECOND_DEADLINE_usec,
                                                       &rtm,
                                                       serialized_size,
                                                       serialized);
      (void) number_of_frames_enqueued;
    }
  }
}
