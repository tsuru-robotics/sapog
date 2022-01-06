#include <reg/udral/service/common/Heartbeat_0_1.h>
#include <node/stop_gap.hpp>
#include "src/node/state/state.hpp"
#include <node/time.h>
#include <node/units.hpp>
#include <reg/udral/service/actuator/common/Feedback_0_1.h>
#include "reg/udral/service/actuator/common/Status_0_1.h"
#include "reg/udral/physics/electricity/PowerTs_0_1.h"
#include "reg/udral/physics/dynamics/rotation/PlanarTs_0_1.h"
#include "esc_publishers.hpp"
#include "motor/motor.hpp"
#include "temperature_sensor.hpp"
#include "node/transmit.hpp"
#include "board/board.hpp"
#include "node/node_config_macros/node_config.hpp"
#include "motor/motor.hpp"

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_service_common_Heartbeat,
                            0, 1);

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_service_actuator_common_Feedback,
                            0, 1);

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_service_actuator_common_Status,
                            0, 1);

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_physics_electricity_PowerTs,
                            0, 1);

UAVCAN_L6_NUNAVUT_C_MESSAGE(reg_udral_physics_dynamics_rotation_PlanarTs,
                            0, 1);


void publish_esc_feedback(node::state::State &state)
{

  if (state.readiness != node::state::Readiness::SLEEP)
  {

    if (state.publish_ports.esc_feedback != CONFIGURABLE_SUBJECT_ID)
    {
      uavcan_l6::DSDL<reg_udral_service_actuator_common_Feedback_0_1>::Serializer serializer{};
      reg_udral_service_actuator_common_Feedback_0_1 fb{};
      fb.heartbeat = reg_udral_service_common_Heartbeat_0_1{};
      fb.heartbeat.readiness.value = static_cast<uint8_t>(state.readiness);
      fb.heartbeat.health = uavcan_node_Health_1_0{};
      fb.heartbeat.health.value = static_cast<uint8_t>(state.health);
      fb.demand_factor_pct = static_cast<unsigned>(motor_get_duty_cycle() * 100 + 0.5F);
      auto res = serializer.serialize(fb);
      if (res.has_value())
      {
        CanardTransferMetadata rtm{};
        rtm.transfer_id = state.transfer_ids.reg_udral_service_actuator_common_Feedback_0_1++;
        rtm.priority = CanardPriorityNominal;
        rtm.port_id = state.publish_ports.esc_feedback;
        rtm.remote_node_id = CANARD_NODE_ID_UNSET;
        rtm.transfer_kind = CanardTransferKindMessage;
        for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
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
    if (get_monotonic_microseconds() > state.next_send_power_dynamics_time)
    {
      state.next_send_power_dynamics_time = get_monotonic_microseconds() + 20'000;  // 50 Hz, 0.02 seconds, 20k us delay
      if (state.publish_ports.esc_dynamics != CONFIGURABLE_SUBJECT_ID)
      {
        publish_esc_dynamics(state);
      }
      if (state.publish_ports.esc_power != CONFIGURABLE_SUBJECT_ID)
      {
        publish_esc_power(state);
      }
    }
    transmit(state);
  }
}


void publish_esc_status(node::state::State &state)
{
  uavcan_l6::DSDL<reg_udral_service_actuator_common_Status_0_1>::Serializer serializer{};
  reg_udral_service_actuator_common_Status_0_1 status{};
  status.error_count = motor_get_zc_failures_since_start();
  status.fault_flags = state.fault_flags;
  status.motor_temperature = uavcan_si_unit_temperature_Scalar_1_0{};
  status.motor_temperature.kelvin = NAN;
  status.controller_temperature = uavcan_si_unit_temperature_Scalar_1_0{};
  status.controller_temperature.kelvin = temperature_sensor::get_temperature_K();
  auto size = serializer.serialize(status);
  if (size.has_value())
  {
    CanardTransferMetadata rtm{};
    rtm.transfer_kind = CanardTransferKindMessage;
    rtm.priority = CanardPriorityNominal;
    rtm.port_id = state.publish_ports.esc_status;
    rtm.remote_node_id = CANARD_NODE_ID_UNSET;
    rtm.transfer_id = state.transfer_ids.reg_udral_service_actuator_common_Status_0_1++;
    for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
    {
      (void) canardTxPush(&state.queues[i], const_cast<CanardInstance *>(&state.canard),
                          get_monotonic_microseconds() + ONE_SECOND_DEADLINE_usec,
                          &rtm,
                          size.value(),
                          serializer.getBuffer());
    }
  } else
  {
    assert(false);
  }
}

void publish_esc_power(node::state::State &state)
{
  uavcan_l6::DSDL<reg_udral_physics_electricity_PowerTs_0_1>::Serializer serializer{};
  reg_udral_physics_electricity_PowerTs_0_1 power{};
  uavcan_si_unit_voltage_Scalar_1_0 voltage{};
  uavcan_si_unit_electric_current_Scalar_1_0 current{};
  motor_get_input_voltage_current(&voltage.volt, &current.ampere);
  power.value.voltage = voltage;
  power.value.current = current;
  auto size = serializer.serialize(power);
  if (size.has_value())
  {
    CanardTransferMetadata rtm{};
    rtm.transfer_kind = CanardTransferKindMessage;
    rtm.priority = CanardPriorityNominal;
    rtm.port_id = state.publish_ports.esc_power;
    rtm.remote_node_id = CANARD_NODE_ID_UNSET;
    rtm.transfer_id = state.transfer_ids.reg_udral_physics_electricity_PowerTs_0_1++;
    for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
    {
      (void) canardTxPush(&state.queues[i], const_cast<CanardInstance *>(&state.canard),
                          get_monotonic_microseconds() + ONE_SECOND_DEADLINE_usec,
                          &rtm,
                          size.value(),
                          serializer.getBuffer());
    }
  } else
  {
    assert(false);
  }
}

double rpm_to_radians_per_second(unsigned int rpm)
{
  unsigned int rotations_per_second = rpm / 60;
  return rotations_per_second * 2 * 3.14159265359;
}

void publish_esc_dynamics(node::state::State &state)
{
  reg_udral_physics_dynamics_rotation_PlanarTs_0_1 rotation{};
  rotation.value = reg_udral_physics_dynamics_rotation_Planar_0_1{};
  uavcan_time_SynchronizedTimestamp_1_0 timestamp01{};
  rotation.value.kinematics.angular_velocity = uavcan_si_unit_angular_velocity_Scalar_1_0{};
  rotation.value.kinematics.angular_position = uavcan_si_unit_angle_Scalar_1_0{};
  rotation.value.kinematics.angular_position.radian = NAN;
  rotation.value._torque = uavcan_si_unit_torque_Scalar_1_0{};
  rotation.value._torque.newton_meter = NAN;
  rotation.value.kinematics.angular_velocity.radian_per_second = rpm_to_radians_per_second(motor_get_rpm());
  CanardMicrosecond current_time_stamp = get_monotonic_microseconds();
  if (state.previous_esc_dynamics_message_timestamp > 0)
  {
    rotation.value.kinematics.angular_acceleration.radian_per_second_per_second =
      (rotation.value.kinematics.angular_velocity.radian_per_second - state.previous_esc_dynamics_angular_velocity)
      / (current_time_stamp - state.previous_esc_dynamics_message_timestamp);
  } else
  {
    rotation.value.kinematics.angular_acceleration.radian_per_second_per_second = NAN;
  }
  state.previous_esc_dynamics_message_timestamp = current_time_stamp;
  state.previous_esc_dynamics_angular_velocity = rotation.value.kinematics.angular_velocity.radian_per_second;
  timestamp01.microsecond = get_monotonic_microseconds();

  rotation.timestamp = timestamp01;

  uavcan_l6::DSDL<reg_udral_physics_dynamics_rotation_PlanarTs_0_1>::Serializer serializer{};
  auto size = serializer.serialize(rotation);
  if (size.has_value())
  {
    CanardTransferMetadata rtm{};
    rtm.transfer_kind = CanardTransferKindMessage;
    rtm.priority = CanardPriorityNominal;
    rtm.port_id = state.publish_ports.esc_dynamics;
    rtm.remote_node_id = CANARD_NODE_ID_UNSET;
    rtm.transfer_id = state.transfer_ids.reg_udral_physics_dynamics_rotation_PlanarTs_0_1++;
    for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
    {
      (void) canardTxPush(&state.queues[i], const_cast<CanardInstance *>(&state.canard),
                          get_monotonic_microseconds() + ONE_SECOND_DEADLINE_usec,
                          &rtm,
                          size.value(),
                          serializer.getBuffer());
    }
  } else
  {
    assert(false);
  }
}
