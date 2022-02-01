// Copyright (c) 2021  Zubax Robotics  <info@zubax.com>

#pragma once

#include <kocherga.hpp>
#include <array>
#include <type_traits>

namespace sapog_bootloader
{
struct AppShared
{
    std::uint32_t can_bus_speed = 0;
    std::uint8_t uavcan_node_id = 0;
    std::uint8_t uavcan_fw_server_node_id = 0;
    std::uint8_t uavcan_file_name[256] = {};
    // std::uint64_t crc; this is not in the struct itself but will be stored after it
};

namespace impl
{
template <typename Container>
std::optional<Container> takeLegacy(void* const ptr)
{
    class ContainerWrapper
    {
    public:
        Container container;

        [[nodiscard]] bool isValid() const
        {
            kocherga::CRC64 crc_computer;
            crc_computer.update(reinterpret_cast<const std::uint8_t*>(&container), sizeof(container));  // NOLINT
            return crc_ == crc_computer.get();
        }

    private:
        std::uint64_t crc_;
    };
    ContainerWrapper wrapper{};
    std::memmove(&wrapper, ptr, sizeof(ContainerWrapper));
    if (wrapper.isValid())
    {
        ContainerWrapper empty{};
        std::memset(&empty, 0, sizeof(empty));  // NOLINT
        std::memmove(ptr, &empty, sizeof(ContainerWrapper));
        return wrapper.container;
    }
    return {};
}


}  // namespace impl

/// Reads and destroys the AppShared struct from the app-bootloader exchange area, if there is one.
/// Returns an empty option otherwise.
/// This function supports all legacy versions and storage locations of the app shared struct to ensure maximum
/// binary compatibility; however, support for the old versions can be safely dropped after 2022.
/// Support for legacy versions was dropped 19th of January 2022.
inline std::optional<AppShared> takeAppShared()
{
    if (const auto x = kocherga::VolatileStorage<AppShared>(board::getAppSharedStructLocation()).take())
    {
        return x;
    }
    return {};
}

}  // namespace sapog_bootloader
