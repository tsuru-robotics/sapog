/****************************************************************************
 *
 *   Copyright (C) 2014 PX4 Development Team. All rights reserved.
 *   Author: Pavel Kirienko <pavel.kirienko@gmail.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name PX4 nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************/

#include "esc_controller.hpp"
#include <uavcan/equipment/esc/RawCommand.hpp>
#include <uavcan/equipment/esc/RPMCommand.hpp>
#include <uavcan/equipment/esc/Status.hpp>
#include <zubax_chibios/os.hpp>
#include <motor/motor.h>
#include <temperature_sensor.hpp>
#include <uavcan/protocol/node_status_monitor.hpp>
#include <arming_status_monitor.hpp>
#include "zubax_chibios/chibios/os/hal/include/serial.h"
#include "mavlink/common/mavlink.h"

#define MAVLINK_BUFFER_SIZE MAVLINK_MSG_ID_DEBUG_LEN + MAVLINK_NUM_NON_PAYLOAD_BYTES
#define MAV_SYS_ID 10

namespace uavcan_node
{
namespace
{

uavcan::Publisher<uavcan::equipment::esc::Status>* pub_status;
uavcan::Publisher<uavcan::equipment::esc::RawCommand>* pub_rawcommand;

unsigned self_index;
unsigned command_ttl_ms;
float max_dc_to_start;
uavcan::LazyConstructor<uavcan::NodeStatusMonitor> node_status_monitor;
uavcan::LazyConstructor<uavcan::ArmingStatusMonitor> arming_status_monitor;


os::config::Param<unsigned> param_esc_index("esc_index",           0,      0,    15);
os::config::Param<unsigned> param_cmd_ttl_ms("cmd_ttl_ms",       200,    100,  5000);
os::config::Param<float> param_cmd_start_dc("cmd_start_dc",      1.0,   0.01,   1.0);


void cb_raw_command(const uavcan::ReceivedDataStructure<uavcan::equipment::esc::RawCommand>& msg)
{
	if (msg.cmd.size() <= self_index) {
		motor_stop();
		return;
	}

    // Ignore RawCommand message from secondary FMU if primary FMU is healthy
    if (msg.getSrcNodeID() == 2)
    {
        uavcan::NodeStatusMonitor::NodeStatus fmu1_status = node_status_monitor->getNodeStatus(1);
        if (fmu1_status.health == uavcan::protocol::NodeStatus::HEALTH_OK &&
                fmu1_status.mode == uavcan::protocol::NodeStatus::MODE_OPERATIONAL) {
            //printf("Ignore RawCommand received from FMU2.\n");
            return;
        } else {
            //printf("Accept RawCommand received from FMU2.\n");
        }
    } else {
        //printf("RawCommand received from FMU1!\n");
    }

    // If system is DISARMED, output controls  to serial,
    // else output controls to motor
    if (arming_status_monitor->getArmingStatus() == uavcan::equipment::safety::ArmingStatus::STATUS_DISARMED) {
        // Encode MAVLink message
        mavlink_message_t mav_msg;
        mavlink_msg_debug_pack(MAV_SYS_ID,
                               self_index,
                               &mav_msg,
                               msg.getUtcTimestamp().toMSec(),
                               self_index,
                               (float)msg.cmd[self_index]);

        // Convert encoded message to buffer
        uint8_t msg_buff[MAVLINK_BUFFER_SIZE];
        uint8_t n_bytes = mavlink_msg_to_send_buffer(msg_buff, &mav_msg);

        // Send buffer to serial port
        sdWrite(&STDOUT_SD, msg_buff, n_bytes);

//        // Encode Dronecan message
//        uavcan::StaticTransferBuffer<28> msg_buff;
//        uavcan::BitStream bitstream(msg_buff);
//        uavcan::ScalarCodec codec(bitstream);
//        int encode_res = uavcan::equipment::esc::RawCommand::encode(msg, codec, uavcan::TailArrayOptEnabled);
//        if (encode_res <= 0)
//        {
//            printf("Encode ERROR!\n");
//        }
//        const uint8_t *buf = (const uint8_t *) &msg_buff;

        return;
    }

	const float scaled_dc =
		msg.cmd[self_index] / float(uavcan::equipment::esc::RawCommand::FieldTypes::cmd::RawValueType::max());

	const bool idle = motor_is_idle();
	const bool accept = (!idle) || (idle && (scaled_dc <= max_dc_to_start));

	if (accept && (scaled_dc > 0)) {
		motor_set_duty_cycle(scaled_dc, command_ttl_ms);
	} else {
		motor_stop();
	}
}

void cb_rpm_command(const uavcan::ReceivedDataStructure<uavcan::equipment::esc::RPMCommand>& msg)
{
	if (msg.rpm.size() <= self_index) {
		motor_stop();
		return;
	}

	const int rpm = msg.rpm[self_index];

	if (rpm > 0) {
		motor_set_rpm(rpm, command_ttl_ms);
	} else {
		motor_stop();
	}
}

void cb_10Hz(const uavcan::TimerEvent& event)
{
	uavcan::equipment::esc::Status msg;

	msg.esc_index = self_index;
	msg.rpm = motor_get_rpm();
	motor_get_input_voltage_current(&msg.voltage, &msg.current);
	msg.power_rating_pct = static_cast<unsigned>(motor_get_duty_cycle() * 100 + 0.5F);
	msg.error_count = motor_get_zc_failures_since_start();

	msg.temperature = float(temperature_sensor::get_temperature_K());
	if (msg.temperature < 0) {
		msg.temperature = std::numeric_limits<float>::quiet_NaN();
	}

	if (motor_is_idle()) {
		// Lower the publish rate to 1Hz if the motor is not running
		static uavcan::MonotonicTime prev_pub_ts;
		if ((event.scheduled_time - prev_pub_ts).toMSec() >= 990) {
			prev_pub_ts = event.scheduled_time;
			pub_status->broadcast(msg);
		}
	} else {
		pub_status->broadcast(msg);
	}
}

}

int init_esc_controller(uavcan::INode& node)
{
	static uavcan::Subscriber<uavcan::equipment::esc::RawCommand> sub_raw_command(node);
	static uavcan::Subscriber<uavcan::equipment::esc::RPMCommand> sub_rpm_command(node);
	static uavcan::Timer timer_10hz(node);

	self_index = param_esc_index.get();
	command_ttl_ms = param_cmd_ttl_ms.get();
	max_dc_to_start = param_cmd_start_dc.get();

	int res = 0;

	res = sub_raw_command.start(cb_raw_command);
	if (res != 0) {
		return res;
	}

	res = sub_rpm_command.start(cb_rpm_command);
	if (res != 0) {
		return res;
	}

	pub_status = new uavcan::Publisher<uavcan::equipment::esc::Status>(node);
	res = pub_status->init();
	if (res != 0) {
		return res;
	}

    pub_rawcommand = new uavcan::Publisher<uavcan::equipment::esc::RawCommand>(node);
    res = pub_rawcommand->init();
    if (res != 0) {
        return res;
    }

	timer_10hz.setCallback(&cb_10Hz);
	timer_10hz.startPeriodic(uavcan::MonotonicDuration::fromMSec(100));


    node_status_monitor.construct<uavcan::INode&>(node);
    res = node_status_monitor->start();
    if (res < 0) {
        return res;
    }

    arming_status_monitor.construct<uavcan::INode&>(node);
    res = arming_status_monitor->start();
    if (res < 0) {
        return res;
    }

	return 0;
}

}
