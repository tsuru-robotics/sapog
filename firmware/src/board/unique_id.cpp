#include <uavcan/node/GetInfo_1_0.h>
#include <src/settings/registers.hpp>
#include "unique_id.h"

namespace board
{
UniqueID read_unique_id()
{
  UniqueID out;
  std::memcpy(out.data(), reinterpret_cast<const void *>(0x1FFFF7E8), std::tuple_size<UniqueID>::value);
  return out;
}
}
