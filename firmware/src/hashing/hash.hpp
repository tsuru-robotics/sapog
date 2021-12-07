#ifndef FIRMWARE_HASH_HPP
#define FIRMWARE_HASH_HPP

#include <cstdint>

class CRC64
{
private:
  static constexpr auto Poly = static_cast<std::uint64_t>(0x42F0'E1EB'A9EA'3693ULL);
  static constexpr auto Mask = static_cast<std::uint64_t>(1) << 63U;
  static constexpr auto Xor = static_cast<std::uint64_t>(0xFFFF'FFFF'FFFF'FFFFULL);
  static constexpr auto Residue = static_cast<std::uint64_t>(0xFCAC'BEBD'5931'A992ULL);

  static constexpr auto InputShift = 56U;

  std::uint64_t crc_ = Xor;
public:
  static constexpr std::size_t Size = 8U;

  void update(const std::uint8_t *const data, const std::size_t len);

  /// The current CRC value.
  [[nodiscard]] std::uint64_t get() const;

  /// The current CRC value represented as a big-endian sequence of bytes.
  /// This method is designed for inserting the computed CRC value after the data.
  [[nodiscard]] auto getBytes() const -> std::array<std::uint8_t, Size>;

  /// True if the current CRC value is a correct residue (i.e., CRC verification successful).
  [[nodiscard]] auto isResidueCorrect() const;

};

#endif //FIRMWARE_HASH_HPP
