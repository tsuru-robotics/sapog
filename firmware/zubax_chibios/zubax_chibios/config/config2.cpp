#include <cstddef>
#include <zubax_chibios/sys/sys.hpp>
#include "config2.hpp"
#include <cerrno>
#include "uavcan_node/time.h"
#include <etl/crc32.h>

namespace config::registers
{
static chibios_rt::Mutex _mutex;

std::optional<uavcan_register_Access_Response_1_0> Storage::getValue(uavcan_register_Access_Request_1_0 access_request)
{
    auto &name = access_request.name;
    ASSERT_ALWAYS(_frozen);
    os::MutexLocker locker(_mutex);

    if (auto value = _storage.getValue(name); value.has_value())
    {
        uavcan_register_Access_Response_1_0 response{};
        response.value = value.value();
        uavcan_time_SynchronizedTimestamp_1_0 timestamp{};
        timestamp.microsecond = getMonotonicMicroseconds();
        response.timestamp = timestamp;
        return response;
    }
    return {};
}

bool Storage::writeValue(uavcan_register_Access_Request_1_0 access_request)
{
    _modification_count += 1;
    return _storage.setValue(access_request.name, access_request.value);
}

Storage::Storage(IStorageBackend &_storage_backend) :
        _storage_backend(_storage_backend)
{}

void Storage::init()
{

}

bool Storage::save()
{
    ASSERT_ALWAYS(_frozen);
    os::MutexLocker locker(_mutex);

    // Erase
    int flash_res = _storage_backend.erase();
    if (flash_res)
    {
        goto flash_error;
    }

    // Write Layout
    flash_res = _storage_backend.write(OFFSET_LAYOUT_HASH, &_layout_hash, 4);
    if (flash_res)
    {
        goto flash_error;
    }

    {
        // Serialize storage
        constexpr size_t pool_len = storage_size * uavcan_register_Value_1_0_EXTENT_BYTES_;
        uint8_t valuesSerialized[pool_len]{};
        auto start_serialized = etl::cbegin(valuesSerialized);
        for (int i = 0; i < _num_params; ++i)
        {
            uint8_t buffer[uavcan_register_Value_1_0_EXTENT_BYTES_];
            size_t size_of_buffer;
            uavcan_register_Value_1_0_serialize_(&_storage.value_array[i], buffer, &size_of_buffer);
            etl::copy(etl::cbegin(buffer), etl::cend(buffer), start_serialized++);
        }

        // Write CRC
        etl::crc32_t256 crc_value;
        crc_value = ::etl::crc32{};
        crc_value.add(etl::cbegin(valuesSerialized), etl::cend(valuesSerialized));
        const std::uint32_t true_crc = crc_value.value();// _storage.value_array, pool_len
        flash_res = _storage_backend.write(OFFSET_CRC, &true_crc, 4);
        if (flash_res)
        {
            goto flash_error;
        }

        // Write Values
        flash_res = _storage_backend.write(OFFSET_VALUES, valuesSerialized, pool_len);
        if (flash_res)
        {
            goto flash_error;
        }
    }


    flash_error:
    assert(flash_res);
    return flash_res;
}

bool Storage::load()
{
    return false;
}
};
