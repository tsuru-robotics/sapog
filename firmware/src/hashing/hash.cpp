#include <array>
#include "hash.hpp"

// https://github.com/Zubax/kocherga/blob/94b7365be1e2418113d6bc433cbd50fe67c27664/kocherga/kocherga.hpp#L234-L291
/// This is used to verify integrity of the application and other data.
/// Note that the firmware CRC verification is a computationally expensive process that needs to be completed
/// in a limited time interval, which should be minimized. This class has been carefully manually optimized to
/// achieve the optimal balance between speed and ROM footprint.
/// The function is CRC-64/WE, see http://reveng.sourceforge.net/crc-catalogue/17plus.htm#crc.cat-bits.64.
void CRC64::update(const std::uint8_t *const data, const std::size_t len)
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

std::uint64_t CRC64::get() const
{ return crc_ ^ Xor; }

auto CRC64::getBytes() const -> std::array<uint8_t, Size>
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

auto CRC64::isResidueCorrect() const
{ return crc_ == Residue; }
