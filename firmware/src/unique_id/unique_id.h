#ifndef FIRMWARE_UNIQUE_ID_H
#define FIRMWARE_UNIQUE_ID_H

#include <array>
#include <cstdint>
// Returns the 128-bit unique-ID of the local node. This value is used in uavcan.node.GetInfo.Response and during the
// plug-and-play node-ID allocation by uavcan.pnp.NodeIDAllocationData. The function is infallible.
namespace board
{
typedef std::array<std::uint8_t, 12> UniqueID;

UniqueID read_unique_id();
}

#endif //FIRMWARE_UNIQUE_ID_H
