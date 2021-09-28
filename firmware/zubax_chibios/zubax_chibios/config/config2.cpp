#include <cstddef>
#include <zubax_chibios/sys/sys.hpp>
#include "config2.hpp"
#include <cerrno>


namespace config::registers
{
static chibios_rt::Mutex _mutex;

uavcan_register_Access_Response_1_0 Storage::getValue(uavcan_register_Access_Request_1_0 access_request)
{
    (void) access_request;

    return uavcan_register_Access_Response_1_0{};
}

int Storage::writeValue(uavcan_register_Access_Request_1_0 access_request)
{
    (void) access_request;
    auto& name = access_request.name;
    int retval = 0;
    ASSERT_ALWAYS(_frozen);
    os::MutexLocker locker(_mutex);

    const int index = _storage.getIndexFromName(name);
    if (index < 0)
    {
        retval = -ENOENT;
        goto leave;
    }

    if (!isValid(_descr_pool[index], value))
    {
        retval = -EINVAL;
        goto leave;
    }

    _modification_count += 1;
    _value_pool[index] = value;

    leave:
    return retval;
    return false;
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
        // Write CRC
        const int pool_len = _num_params * sizeof(_value_pool[0]);
        const std::uint32_t true_crc = crc32(_value_pool, pool_len);
        flash_res = _storage_backend.write(OFFSET_CRC, &true_crc, 4);
        if (flash_res)
        {
            goto flash_error;
        }

        // Write Values
        flash_res = _storage_backend.write(OFFSET_VALUES, _value_pool, pool_len);
        if (flash_res)
        {
            goto flash_error;
        }
    }

    return 0;

    flash_error:
    assert(flash_res);
    return flash_res;
}
};
