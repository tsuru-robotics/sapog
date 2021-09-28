#include <uavcan/_register/Value_1_0.h>
#include "registers.hpp"
#include <optional>
#include <cstdio>
#include "zubax_chibios/zubax_chibios/config/config.h"
#include "src/uavcan_node/type_conversion/uavcan_type_conversion.h"
#include <variant>
#include <motor/realtime/api.h>
#include "motor/motor.hpp"

namespace board
{
extern std::optional<os::stm32::ConfigStorageBackend> config_storage_backend;
}
static void *const ConfigStorageAddress = reinterpret_cast<void *>(0x08000000 + (256 * 1024) - 1024);
constexpr unsigned ConfigStorageSize = 1024;

namespace config::registers
{

StorageManager &getInstance()
{
    static StorageManager storage_manager;
    return storage_manager;
}

StorageManager::StorageManager() noexcept:
        config_storage_backend{ConfigStorageAddress, ConfigStorageSize}
{

};


bool StorageManager::registerWrite([[maybe_unused]] const char *const register_name,
                                   const uavcan_register_Value_1_0 *const input_value)
{
    if (input_value == nullptr)
    { return false; }
    if (uavcan_register_Value_1_0_is_bit_(input_value))
    {
        std::optional<float> value;
        value = conversion::extract(input_value->bit);
        if (value.has_value())
        {
            configSet(register_name, value.value());
        } else
        {
            return false;
        }
    } else if (uavcan_register_Value_1_0_is_integer64_(input_value))
    {
        std::optional<float> value;
        value = conversion::extract(input_value->integer64);
        if (value.has_value())
        {
            configSet(register_name, value.value());
        } else
        {
            return false;
        }
    } else if (uavcan_register_Value_1_0_is_real64_(input_value))
    {
        std::optional<float> value;
        value = conversion::extract(input_value->real64);
        if (value.has_value())
        {
            configSet(register_name, value.value());
        } else
        {
            return false;
        }
    }
    return false;
}

std::optional<uavcan_register_Value_1_0> StorageManager::registerRead(const char *const register_name)
{
    printf("Reading register: %s\n", register_name);
    ConfigParam in{};
    int result = configGetDescr(register_name, &in);
    if (result <= 0)
    { return {}; }
    switch (in.type)
    {
        case CONFIG_TYPE_FLOAT:
        {
            std::optional<uavcan_primitive_array_Real64_1_0> conversion = conversion::pack<uavcan_primitive_array_Real64_1_0>(
                    configGet(register_name));
            if (conversion.has_value())
            {
                uavcan_register_Value_1_0 value{};
                value.real64 = conversion.value();
                return value;
            }
            break;
        }

        case CONFIG_TYPE_INT:
        {
            std::optional<uavcan_primitive_array_Integer64_1_0> conversion = conversion::pack<uavcan_primitive_array_Integer64_1_0>(
                    configGet(register_name));
            if (conversion.has_value())
            {
                uavcan_register_Value_1_0 value{};
                value.integer64 = conversion.value();
                return value;
            }
            break;
        }
        case CONFIG_TYPE_BOOL:
        {
            std::optional<uavcan_primitive_array_Bit_1_0> conversion = conversion::pack<uavcan_primitive_array_Bit_1_0>(
                    configGet(register_name));
            if (conversion.has_value())
            {
                uavcan_register_Value_1_0 value{};
                value.bit = conversion.value();
                return value;
            }
            break;
        }
        default:
            return {};
    }
    return std::optional<uavcan_register_Value_1_0>();
}
}