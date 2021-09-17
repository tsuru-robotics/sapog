#include "zubax_chibios/zubax_chibios/platform/stm32/config_storage.hpp"
#include "uavcan/_register/Value_1_0.h"
#ifndef FIRMWARE_REGISTERS_HPP
#define FIRMWARE_REGISTERS_HPP
namespace config::registers
{
class StorageManager
{
public:
    os::stm32::ConfigStorageBackend config_storage_backend;
    StorageManager() noexcept;
    std::optional<uavcan_register_Value_1_0> registerRead(const char *const register_name);
    void registerWrite(const char *const register_name, const uavcan_register_Value_1_0 *const input_value);
};
}

#endif //FIRMWARE_REGISTERS_HPP
