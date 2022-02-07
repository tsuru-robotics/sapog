/*
 * Copyright (c) 2016 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Pavel Kirienko <pavel.kirienko@zubax.com>
 */

#pragma once

#include <cstdint>
#include <cassert>
#include <tuple>
#include <type_traits>
#include <cstring>
#include "util.hpp"

struct AppShared
{
    std::uint32_t can_bus_speed = 0;
    std::uint8_t uavcan_node_id = 0;
    std::uint8_t uavcan_fw_server_node_id = 0;
    std::uint8_t uavcan_file_name[256] = {};
    // std::uint64_t crc; this is not in the struct itself but will be stored after it
};
// --------------------------------------------------------------------------------------------------------------------

/// This is used to verify integrity of the application and other data.
/// Note that the firmware CRC verification is a computationally expensive process that needs to be completed
/// in a limited time interval, which should be minimized. This class has been carefully manually optimized to
/// achieve the optimal balance between speed and ROM footprint.
/// The function is CRC-64/WE, see http://reveng.sourceforge.net/crc-catalogue/17plus.htm#crc.cat-bits.64.
class CRC64
{
public:
    static constexpr std::size_t Size = 8U;

    void update(const std::uint8_t* const data, const std::size_t len)
    {
        const auto* bytes = data;
        for (auto remaining = len; remaining > 0; remaining--)
        {
            crc_ ^= static_cast<std::uint64_t>(*bytes) << InputShift;
            ++bytes;
            // Unrolled for performance reasons. This path directly affects the boot-up time, so it is very
            // important to keep it optimized for speed. Rolling this into a loop causes a significant performance
            // degradation at least with GCC since the compiler refuses to unroll the loop when size optimization
            // is selected (which is normally used for bootloaders).
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
            crc_ = ((crc_ & Mask) != 0) ? ((crc_ << 1U) ^ Poly) : (crc_ << 1U);
        }
    }

    /// The current CRC value.
    [[nodiscard]] auto get() const { return crc_ ^ Xor; }

    /// The current CRC value represented as a big-endian sequence of bytes.
    /// This method is designed for inserting the computed CRC value after the data.
    [[nodiscard]] auto getBytes() const -> std::array<std::uint8_t, Size>
    {
        auto                           x = get();
        std::array<std::uint8_t, Size> out{};
        const auto                     rend = std::rend(out);
        for (auto it = std::rbegin(out); it != rend; ++it)
        {
            *it = static_cast<std::uint8_t>(x);
            x >>= 8U;
        }
        return out;
    }

    /// True if the current CRC value is a correct residue (i.e., CRC verification successful).
    [[nodiscard]] auto isResidueCorrect() const { return crc_ == Residue; }

private:
    static constexpr auto Poly    = static_cast<std::uint64_t>(0x42F0'E1EB'A9EA'3693ULL);
    static constexpr auto Mask    = static_cast<std::uint64_t>(1) << 63U;
    static constexpr auto Xor     = static_cast<std::uint64_t>(0xFFFF'FFFF'FFFF'FFFFULL);
    static constexpr auto Residue = static_cast<std::uint64_t>(0xFCAC'BEBD'5931'A992ULL);

    static constexpr auto InputShift = 56U;

    std::uint64_t crc_ = Xor;
};

// --------------------------------------------------------------------------------------------------------------------

/// This helper class allows the bootloader and the application to exchange arbitrary data in a robust way.
/// The data is stored in the specified memory location (usually it is a small dedicated area a few hundred bytes
/// large at the very end of the slowest RAM segment) together with a strong CRC64 hash to ensure its validity.
/// When one component (either the bootloader or the application) needs to pass data to another (e.g., when commencing
/// the update process, the application needs to reboot into the bootloader and pass specific parameters to it),
/// the data is prepared in a particular application-specific data structure which is then passed into this class.
/// The class writes the data structure into the provided memory region and appends the CRC64 hash immediately
/// afterwards (no padding inserted). The other component then checks the memory region where the data is expected to
/// be found and validates its CRC; if the CRC matches, the data is reported to be found, otherwise it is reported
/// that there is no data to read (the latter occurs when the bootloader is started after power-on reset,
/// a power loss, or a hard reset).
///
/// The stored data type shall be a trivial type (see https://en.cppreference.com/w/cpp/named_req/TrivialType).
/// The storage space shall be large enough to accommodate an instance of the stored data type plus eight bytes
/// for the CRC (no padding inserted).
///
/// Here is a usage example. Initialization:
///
///     struct MyData;
///     VolatileStorage<MyData> storage(my_memory_location);
///
/// Reading the data from the storage (the storage is always erased when reading to prevent deja-vu after restart):
///
///     if (auto data = storage.take())
///     {
///         // Process the data...
///     }
///     else
///     {
///         // Data is not available (not stored)
///     }
///
/// Writing the data into the storage: storage.store(data).
template <typename Container>
class VolatileStorage
{
public:
    /// The amount of memory required to store the data. This is the size of the container plus 8 bytes for the CRC.
    static constexpr auto StorageSize = sizeof(Container) + CRC64::Size;  // NOLINT

    explicit VolatileStorage(std::uint8_t* const location) : ptr_(location) {}

    /// Checks if the data is available and reads it, then erases the storage to prevent deja-vu.
    /// Returns an empty option if no data is available (in that case the storage is not erased).
    [[nodiscard]] auto take() -> std::optional<Container>
    {
        CRC64 crc;
        crc.update(ptr_, StorageSize);
        if (crc.isResidueCorrect())
        {
            Container out{};
            (void) std::memmove(&out, ptr_, sizeof(Container));
            (void) std::memset(ptr_, EraseFillValue, StorageSize);
            return out;
        }
        return {};
    }

    /// Writes the data into the storage with CRC64 protection.
    void store(const Container& data)
    {
        (void) std::memmove(ptr_, &data, sizeof(Container));
        CRC64 crc;
        crc.update(ptr_, sizeof(Container));
        const auto crc_ptr = ptr_ + sizeof(Container);  // NOLINT NOSONAR pointer arithmetic
        (void) std::memmove(crc_ptr, crc.getBytes().data(), CRC64::Size);
    }

protected:
    static constexpr std::uint8_t EraseFillValue = 0xCA;

    std::uint8_t* const ptr_;
};

