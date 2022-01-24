/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include "get_info.hpp"

uavcan_node_GetInfo_Response_1_0 process_request_node_get_info()
{
  uavcan_node_GetInfo_Response_1_0 resp{};
  resp.protocol_version.major = CANARD_UAVCAN_SPECIFICATION_VERSION_MAJOR;
  resp.protocol_version.minor = CANARD_UAVCAN_SPECIFICATION_VERSION_MINOR;

  auto hw_version = board::detect_hardware_version();
  resp.hardware_version.major = hw_version.major;
  resp.hardware_version.minor = hw_version.minor;

  resp.software_version.major = FW_VERSION_MAJOR;
  resp.software_version.minor = FW_VERSION_MINOR;

  resp.software_vcs_revision_id = GIT_HASH;
  // https://github.com/Zubax/sapog/blob/601f4580b71c3c4da65cc52237e62a163d6a6a16/firmware/src/uavcan_node/uavcan_node.cpp#L428
  memcpy(resp.unique_id, board::read_unique_id().data(), sizeof(uint8_t[16]));
  // The node name is the name of the product like a reversed Internet domain name (or like a Java package).
  resp.name.count = strlen(NODE_NAME); // QUESTION: Does this string include a null terminator? It mustn't include it.
  memcpy(&resp.name.elements, NODE_NAME, resp.name.count);

  // The software image CRC and the Certificate of Authenticity are optional so not populated in this demo.
  return resp;
}
