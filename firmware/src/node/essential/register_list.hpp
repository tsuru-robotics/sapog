/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "libcanard/canard.h"
#include "node/interfaces/IHandler.hpp"
#include "uavcan/_register/List_1_0.h"

#include "node/interfaces/IHandler.hpp"
#include <string_view>
#include <node/units.hpp>
#include "uavcan/_register/List_1_0.h"
#include <node/time.h>
#include <node/stop_gap.hpp>
#include "heartbeat.hpp"
#include "board/board.hpp"

std::string_view all_register_names[] = {
  "uavcan.sub.note_response.id", "uavcan.sub.note_response.type",
  "uavcan.sub.setpoint.id", "uavcan.sub.setpoint.type",
  "id_in_esc_group",
  "uavcan.sub.readiness.id", "uavcan.sub.readiness.type",
  "ttl_milliseconds",
  "uavcan.pub.esc_heartbeat.id", "uavcan.pub.esc_heartbeat.type",
  "uavcan.pub.feedback.id", "uavcan.pub.feedback.type",
  "uavcan.pub.power.id", "uavcan.pub.power.type",
  "uavcan.pub.status.id", "uavcan.pub.status.type",
  "uavcan.pub.dynamics.id", "uavcan.pub.dynamics.type",
  "control_mode_rpm", "mot_v_min", "mot_v_spinup",
  "mot_spup_vramp_t", "mot_dc_accel", "mot_dc_slope",
  "mot_num_poles", "ctl_dir", "mot_rpm_min",
  "mot_i_max", "mot_i_max_p", "mot_lpf_freq",
  "mot_stop_thres", "uavcan.node.id"
};

UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_register_List,
                            1, 0);
namespace node::essential
{
struct RegisterListHandlerType : IHandler
{
  void operator()(node::state::State &state, CanardRxTransfer *transfer);
} uavcan_register_List_1_0_handler;

void RegisterListHandlerType::operator()(node::state::State &state, CanardRxTransfer *transfer)
{
  auto request =
    uavcan_l6::DSDL<uavcan_register_List_Request_1_0>
    ::deserialize(transfer->payload_size,
                  static_cast<const uint8_t *>(transfer->payload));
  if (request.has_value())
  {
    auto serializer = uavcan_l6::DSDL<uavcan_register_List_Response_1_0>::Serializer();
    auto response_value = uavcan_register_List_Response_1_0{};
    if (sizeof(all_register_names) / sizeof(all_register_names[0]) > 0)
    {
      std::copy(std::begin(all_register_names[request->index]),
                std::end(all_register_names[request->index]),
                std::begin(response_value.name.name.elements));
      response_value.name.name.count = all_register_names[request->index].size();
    }
    auto res = serializer.serialize(response_value);
    CanardTransferMetadata rtm = transfer->metadata;  // Response transfers are similar to their requests.
    rtm.transfer_kind = CanardTransferKindResponse;
    for (int i = 0; i <= board::detect_hardware_version().minor; ++i)
    {
      int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                       const_cast<CanardInstance *>(&state.canard),
                                                       get_monotonic_microseconds() +
                                                       ONE_SECOND_DEADLINE_usec,
                                                       &rtm,
                                                       res.value(),
                                                       serializer.getBuffer());
      (void) number_of_frames_enqueued;
    }
  }
  return;
}
}


