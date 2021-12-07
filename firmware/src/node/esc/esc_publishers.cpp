#include <reg/udral/service/common/Heartbeat_0_1.h>
#include <node/stop_gap.hpp>
#include <node/state.hpp>
#include <node/time.h>
#include <node/units.hpp>
#include <reg/udral/service/actuator/common/Feedback_0_1.h>
#include "esc_publishers.hpp"

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_service_common_Heartbeat,
                            0, 1);

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_service_actuator_common_Feedback,
                            0, 1);

void publish_esc_heartbeat(node::state::State &state)
{
  if (state.esc_heartbeat_publish_port == CONFIGURABLE_SUBJECT_ID)
  {
    return;
  }
  uavcan_l6::DSDL<reg_udral_service_common_Heartbeat_0_1>::Serializer serializer{};
  reg_udral_service_common_Heartbeat_0_1 hb{};
  hb.readiness = reg_udral_service_common_Readiness_0_1{};
  hb.readiness.value = static_cast<uint8_t>(state.readiness);
  hb.health = uavcan_node_Health_1_0{};
  hb.health.value = static_cast<uint8_t>(state.health);
  auto res = serializer.serialize(hb);
  if (res.has_value())
  {
    CanardTransferMetadata rtm{};  // Response transfers are similar to their requests.
    rtm.transfer_kind = CanardTransferKindMessage;
    for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
    {
      (void) canardTxPush(&state.queues[i], const_cast<CanardInstance *>(&state.canard),
                          get_monotonic_microseconds() + ONE_SECOND_DEADLINE_usec,
                          &rtm,
                          res.value(),
                          serializer.getBuffer());
    }
  } else
  {
    assert(false);
  }
}

void publish_esc_feedback(node::state::State &state)
{
  if (state.esc_feedback_publish_port != CONFIGURABLE_SUBJECT_ID)
  {
    uavcan_l6::DSDL<reg_udral_service_actuator_common_Feedback_0_1>::Serializer serializer{};
    reg_udral_service_actuator_common_Feedback_0_1 fb{};
    fb.heartbeat = reg_udral_service_common_Heartbeat_0_1{};
    fb.heartbeat.readiness.value = static_cast<uint8_t>(state.readiness);
    fb.heartbeat.health = uavcan_node_Health_1_0{};
    fb.heartbeat.health.value = static_cast<uint8_t>(state.health);
    auto res = serializer.serialize(fb);
    if (res.has_value())
    {
      CanardTransferMetadata rtm{};  // Response transfers are similar to their requests.
      rtm.transfer_kind = CanardTransferKindMessage;
      for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
      {
        (void) canardTxPush(&state.queues[i], const_cast<CanardInstance *>(&state.canard),
                            get_monotonic_microseconds() + ONE_SECOND_DEADLINE_usec,
                            &rtm,
                            res.value(),
                            serializer.getBuffer());
      }
    } else
    {
      assert(false);
    }
  }
}


void publish_esc_power(node::state::State &state)
{
  (void) state;
}

void publish_esc_dynamics(node::state::State &state)
{
  (void) state;
}