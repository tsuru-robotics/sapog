/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "node/state/state.hpp"
#include "libcanard/canard.h"
#include "uavcan/_register/Access_1_0.h"
#include "access.hpp"

namespace node::essential
{
struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        (void) state;
        uavcan_register_Access_Request_1_0 request{};
        size_t temp_payload_size{transfer->payload_size};
        auto result = uavcan_register_Access_Request_1_0_deserialize_(&request,
                                                                      (const uint8_t *) transfer->payload,
                                                                      &temp_payload_size);
        assert(result >= 0);
        if (result < 0)
        { return; } // maybe it is a damaged frame, could happen?
        if (request.name.name.count == 0)
        {
            return;
        }
        request.name.name.elements[request.name.name.count] = 0;
        std::string_view request_name = reinterpret_cast<const char *>(request.name.name.elements);
        ConfigParam entry_config_params{};
        printf("\n\nAccess handler: %s\n", request.name.name.elements);
        bool register_has_entry_for_name =
            configGetDescr(request_name.data(), &entry_config_params) == 0;
        if (register_has_entry_for_name)
        {
            conversion::ConversionResponse conversion_response = ::conversion::extract_any_number(request.value,
                                                                                                  {entry_config_params.type});
            // Going to write a value to the register.
            switch (conversion_response.conversion_status)
            {
                case conversion::ConversionStatus::SUCCESS:
                {
                    float received_value = conversion_response.value;
                    const char *request_name_c = request_name.data();
                    printf("(int) value: %d\n", (int) received_value);
                    configSet(request_name_c, received_value);
                    break;
                }
                case conversion::ConversionStatus::NOT_SUPPORTED:
                    if (uavcan_register_Value_1_0_is_empty_(&request.value))
                    {
                        printf("Read requested.\n");
                    } else
                    {
                        printf(
                            "Value that cannot be stored in any register. This device doesn't support string register values btw.\n");
                    }
                    break;
                case conversion::ConversionStatus::WRONG_TYPE:
                    printf("Value of this type that cannot be stored in this register.\n");
                    break;
            }
        }
        // The client is going to get a response with the actual value of the register
        respond_to_access(state, request_name.data(), transfer);
        return;
    }
} uavcan_register_Access_1_0_handler;
}
