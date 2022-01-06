//
// Created by silver on 14.12.21.
//

#include <cstddef>
#include <array>
#include <string_view>
#include "uavcan/_register/Access_1_0.h"
#include "type_names.hpp"
#include "access.hpp"
#include "board/board.hpp"

std::string_view find_type_name(std::string_view request_name)
{
  std::string_view found_type_name{};
  for (auto &iter: types_names)
  {
    if (iter.name == request_name)
    {
      found_type_name = iter.type_name;
    }
  }
  return found_type_name;
}

RegisterCriteria
handle_possible_imaginary_register_access(std::string_view request_name, uavcan_register_Value_1_0 &out_value)
{

  // Now what happens if the size of the incoming string is less than 3 or 5
  bool endsWithType = request_name.size() >= 5 &&
                      request_name.at(request_name.size() - 1) == 'e' &&
                      request_name.at(request_name.size() - 2) == 'p' &&
                      request_name.at(request_name.size() - 3) == 'y' &&
                      request_name.at(request_name.size() - 4) == 't'
                      && request_name.at(request_name.size() - 5) == '.';

  if (endsWithType)
  {
    std::string_view type_string = find_type_name(request_name.data());
    if (!type_string.empty())
    {
      uavcan_register_Value_1_0_select_string_(&out_value);
      uavcan_primitive_String_1_0 return_value{};
      return_value.value.count = type_string.size();
      memcpy(&return_value.value.elements, type_string.data(), return_value.value.count);
      out_value._string = return_value;
      return RegisterCriteria{._mutable=true, .persistent = true};
    }
    bool alsoEndsWithId =
      request_name.size() >= 3 && request_name.at(request_name.size() - 6) == 'd' &&
      request_name.at(request_name.size() - 7) == 'i' &&
      request_name.at(request_name.size() - 8) == '.';
    if (alsoEndsWithId)
    {
      uavcan_register_Value_1_0_select_string_(&out_value);
      uavcan_primitive_String_1_0 return_value{};
      constexpr std::string_view natural16_string = "uavcan.primitive.scalar.Natural16.1.0\0";
      return_value.value.count = natural16_string.size();
      std::copy(natural16_string.begin(), natural16_string.end(), std::begin(return_value.value.elements));
      out_value._string = return_value;
      return RegisterCriteria{._mutable=false, .persistent = true};
    }

    uavcan_register_Value_1_0_select_empty_(&out_value);
    out_value.empty = uavcan_primitive_Empty_1_0{0};
    printf("Access returns with empty value\n");
    return RegisterCriteria{._mutable=true, .persistent = true};
  }
  return RegisterCriteria{};
}

RegisterCriteria handle_real_register_access(std::string_view request_name, uavcan_register_Value_1_0 &out_value,
                                             ConfigParam &param)
{
  bool endsWithId =
    request_name.size() >= 3 && request_name.at(request_name.size() - 1) == 'd' &&
    request_name.at(request_name.size() - 2) == 'i' &&
    request_name.at(request_name.size() - 3) == '.';
  float value = configGet(request_name.data());
  std::optional<node::conf::wrapper::converter_type> converter = node::conf::wrapper::find_converter(
    request_name.data());
  std::string_view request_name_sw(request_name.data());
  if (converter.has_value())
  {
    auto converter_response = converter.value()(value, out_value);
    return RegisterCriteria{._mutable = converter_response._mutable, .persistent = converter_response.persistent};
  } else
  {
    if (param.type == CONFIG_TYPE_FLOAT)
    {
      printf("Response value: float: %f\n", value);
      uavcan_register_Value_1_0_select_real64_(&out_value);
      out_value.real64.value.elements[0] = value;
      out_value.real64.value.
        count = 1;
    } else if (param.type == CONFIG_TYPE_INT)
    {
      printf("Response type: int: %d\n", (uint16_t) value);

      if (endsWithId)
      {
        uavcan_register_Value_1_0_select_natural16_(&out_value);
        out_value.natural16.value.elements[0] = value;
        out_value.natural16.value.count = 1;
      } else
      {
        uavcan_register_Value_1_0_select_integer64_(&out_value);
        out_value.integer64.value.elements[0] = value;
        out_value.integer64.value.count = 1;
      }
    } else if (param.type == CONFIG_TYPE_BOOL)
    {
      printf("Response type: bool\n");
      uavcan_register_Value_1_0_select_bit_(&out_value);
      printf("The value that is being saved into a boolean: %d\n", (int) value);
      printf("nunavutSetBit %d\n", nunavutSetBit(out_value.bit.value.bitpacked, 1, 0, value != 0));
      out_value.bit.value.count = 1;
    }
  }
  if (endsWithId)
  {
    return RegisterCriteria{true, true};
  }
  return RegisterCriteria{};
}

RegisterCriteria get_response_value(std::string_view request_name, uavcan_register_Value_1_0 &out_value)
{
  ConfigParam param{};
  auto register_access_status_number = configGetDescr(request_name.data(), &param);
  bool was_register_access_successful = register_access_status_number == 0;
  if (was_register_access_successful)
  {
    return handle_real_register_access(request_name, out_value, param);
  } else
  {
    return handle_possible_imaginary_register_access(request_name, out_value);
  }
}

bool respond_to_access(node::state::State &state, std::basic_string_view<char> request_name,
                       const CanardRxTransfer *const transfer)
{
  uavcan_register_Access_Response_1_0 response{};
  // Read the value and send it back to the client
  uavcan_register_Value_1_0 response_value{};
  auto register_criteria = get_response_value(request_name, response_value);
  response.value = response_value;
  response.persistent = register_criteria.persistent;
  response._mutable = register_criteria._mutable;
  uint8_t serialized[uavcan_register_Access_Response_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
  size_t serialized_size = sizeof(serialized);
  int8_t error = uavcan_register_Access_Response_1_0_serialize_(&response, &serialized[0], &serialized_size);
  assert(error >= 0);
  if (error < 0)
  {
    printf("Failed to serialize access response with code %d\n", error);
    return false;
  }
  printf("Serialized.\n");
  CanardTransferMetadata rtm = transfer->metadata;  // Response transfers are similar to their requests.
  rtm.transfer_kind = CanardTransferKindResponse;
  for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
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
  printf("Responded.\n");
  return true;
}
