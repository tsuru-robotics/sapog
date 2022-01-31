/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <uavcan/node/ExecuteCommand_1_1.h>
#include <cstdio>
#include <node/units.hpp>
#include <node/time.h>
#include <motor/motor.hpp>
#include "src/node/state/state.hpp"
#include "node/commands/commands.hpp"
#include "board/board.hpp"
#include "node/interfaces/IHandler.hpp"
#include "software_update/util.hpp"
#include <node/stop_gap.hpp>
#include <cstring>
#include <string_view>
#include "software_update/app_shared.hpp"

UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_node_ExecuteCommand,
                            1, 1);

struct : IHandler
{
  void operator()(node::state::State &state, CanardRxTransfer *transfer)
  {
    (void) state;
    auto request = uavcan_l6::DSDL<uavcan_node_ExecuteCommand_Request_1_1>::deserialize(transfer->payload_size,
                                                                                        static_cast<const uint8_t *>(transfer->payload));
    if (request.has_value())
    {
      uavcan_node_ExecuteCommand_Response_1_1 response{};
//            printf("Commanded: %d\n", request.value().command);
      os::bootloader::AppShared *app_shared = reinterpret_cast<os::bootloader::AppShared *>(0x20000000);
      switch (request.value().command)
      {
        case uavcan_node_ExecuteCommand_Request_1_1_COMMAND_RESTART:
          if (app_shared->stay_in_bootloader)
          {
            printf("Stay in bootloader was set, so resetting it.\n");
            app_shared->stay_in_bootloader = false;
          }
          state.is_restart_required = true;
          response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_SUCCESS;
          printf("Restart is requested.\n");
          break;
        case uavcan_node_ExecuteCommand_Request_1_1_COMMAND_STORE_PERSISTENT_STATES:
          if (motor_is_idle())
          {
            state.is_save_requested = true;
            response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_SUCCESS;
          } else
          {
            response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_BAD_STATE;
          }
          break;
        case uavcan_node_ExecuteCommand_Request_1_1_COMMAND_BEGIN_SOFTWARE_UPDATE:
          if (request->parameter.count == 0)
          {
            response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_BAD_PARAMETER;
            printf("Bad parameter\n");
            break;
          }
          os::bootloader::AppShared my_app_shared{};
          std::memcpy(my_app_shared.uavcan_file_name, request->parameter.elements, request->parameter.count);
          my_app_shared.can_bus_speed = 1'000'000;
          my_app_shared.uavcan_node_id = state.canard.node_id;
          my_app_shared.uavcan_fw_server_node_id = transfer->metadata.remote_node_id;
          my_app_shared.stay_in_bootloader = true;
          auto x = os::bootloader::app_shared::makeAppSharedMarshaller<os::bootloader::AppShared>(
            reinterpret_cast<void *>(0x20000000));
          x.write(my_app_shared);
          __asm volatile("bkpt #0\n");  // NOLINT Break into the debugger
//          std::memcpy(reinterpret_cast<void *>(0x20000000), &my_app_shared, sizeof(my_app_shared));
//          state.is_restart_required = true;
          response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_SUCCESS;
      }
      uavcan_l6::DSDL<uavcan_node_ExecuteCommand_Response_1_1>::Serializer serializer{};
      auto res = serializer.serialize(response);
      assert(res.has_value());
      if (res.has_value())
      {
        CanardTransferMetadata rtm = transfer->metadata;  // Response transfers are similar to their requests.
        rtm.transfer_kind = CanardTransferKindResponse;
        for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
        {
          int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                           const_cast<CanardInstance *>(&state.canard),
                                                           transfer->timestamp_usec +
                                                           ONE_SECOND_DEADLINE_usec,
                                                           &rtm,
                                                           res.value(),
                                                           serializer.getBuffer());
          (void) number_of_frames_enqueued;
        }

      }
      return;
    }
    return;
  }
} uavcan_node_ExecuteCommand_Request_1_1_handler;
