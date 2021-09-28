#ifndef FIRMWARE_CONFIG2_HPP
#include "IStorageBackend.hpp"
#include "uavcan/_register/Access_1_0.h"
#include "uavcan/_register/Value_1_0.h"
#include "static_map.hpp"
#include <unordered_map>
static constexpr int InitCodeRestored       = 1;
static constexpr int InitCodeLayoutMismatch = 2;
static constexpr int InitCodeCRCMismatch    = 3;
static constexpr int OFFSET_LAYOUT_HASH     = 0;
static constexpr int OFFSET_CRC             = 4;
static constexpr int OFFSET_VALUES          = 8;
static constexpr size_t storage_size = 100;
using namespace ::os::config;
namespace config::registers{
class Storage {
protected:
    IStorageBackend& _storage_backend;

    mtl::StaticMap<uavcan_register_Name_1_0, uavcan_register_Value_1_0, storage_size> _storage;
    int _modification_count;
    std::uint32_t _layout_hash = 0;
    bool _frozen;
    int _num_params;
public:
    explicit Storage(IStorageBackend& _storage_backend);
    void init();
    std::optional<uavcan_register_Access_Response_1_0> getValue(uavcan_register_Access_Request_1_0 access_request);
    bool writeValue(uavcan_register_Access_Request_1_0 access_request);
    bool save();

    bool load();
};
}


#endif //FIRMWARE_CONFIG2_HPP
