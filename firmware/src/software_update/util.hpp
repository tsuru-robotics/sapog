/*
 * Copyright (c) 2016 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Pavel Kirienko <pavel.kirienko@zubax.com>
 */

#pragma once

#include <cstdint>
#include <cassert>


namespace os
{
namespace bootloader
{
struct AppShared
{
  std::uint32_t can_bus_speed = 0;
  std::uint8_t uavcan_node_id = 0;
  std::uint8_t uavcan_fw_server_node_id = 0;
  std::uint8_t uavcan_file_name[256] = {};
  // std::uint64_t crc; this is not in the struct itself but will be stored after it
};
/**
 * Error codes.
 * These are returned from functions in negated form, i.e. -10000 means error code 10000.
 */
static constexpr std::int16_t ErrOK = 0;
static constexpr std::int16_t ErrInvalidState = 10001;
static constexpr std::int16_t ErrAppImageTooLarge = 10002;
static constexpr std::int16_t ErrAppStorageWriteFailure = 10003;

/**
 * This is used to verify integrity of the application and other data.
 * Note that firmware CRC verification is a very computationally intensive process that needs to be completed
 * in a limited time interval, which should be minimized. Therefore, this class has been carefully manually
 * optimized to achieve the optimal balance between speed and ROM footprint.
 *
 * CRC-64-WE
 * Description: http://reveng.sourceforge.net/crc-catalogue/17plus.htm#crc.cat-bits.64
 * Initial value: 0xFFFFFFFFFFFFFFFF
 * Poly: 0x42F0E1EBA9EA3693
 * Reverse: no
 * Output xor: 0xFFFFFFFFFFFFFFFF
 * Check: 0x62EC59E3F1A4F00A
 */
/// This is used to verify integrity of the application and other data.
/// Note that the firmware CRC verification is a computationally expensive process that needs to be completed
/// in a limited time interval, which should be minimized. This class has been carefully manually optimized to
/// achieve the optimal balance between speed and ROM footprint.
/// The function is CRC-64/WE, see http://reveng.sourceforge.net/crc-catalogue/17plus.htm#crc.cat-bits.64.
class CRC64
{
public:
  static constexpr std::size_t Size = 8U;

  void update(const std::uint8_t *const data, const std::size_t len)
  {
    const auto *bytes = data;
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
  [[nodiscard]] auto get() const
  { return crc_ ^ Xor; }

  /// The current CRC value represented as a big-endian sequence of bytes.
  /// This method is designed for inserting the computed CRC value after the data.
  [[nodiscard]] auto getBytes() const -> std::array<std::uint8_t, Size>
  {
    auto x = get();
    std::array<std::uint8_t, Size> out{};
    const auto rend = std::rend(out);
    for (auto it = std::rbegin(out); it != rend; ++it)
    {
      *it = static_cast<std::uint8_t>(x);
      x >>= 8U;
    }
    return out;
  }

  /// True if the current CRC value is a correct residue (i.e., CRC verification successful).
  [[nodiscard]] auto isResidueCorrect() const
  { return crc_ == Residue; }

private:
  static constexpr auto Poly = static_cast<std::uint64_t>(0x42F0'E1EB'A9EA'3693ULL);
  static constexpr auto Mask = static_cast<std::uint64_t>(1) << 63U;
  static constexpr auto Xor = static_cast<std::uint64_t>(0xFFFF'FFFF'FFFF'FFFFULL);
  static constexpr auto Residue = static_cast<std::uint64_t>(0xFCAC'BEBD'5931'A992ULL);

  static constexpr auto InputShift = 56U;

  std::uint64_t crc_ = Xor;
};


}
}
