/****************************************************************************
 *
 *   Copyright (C) 2016 PX4 Development Team. All rights reserved.
 *   Author: Pavel Kirienko <pavel.kirienko@gmail.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name PX4 nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************/

#include <cstdint>
#include <array>

namespace uavcan_node
{
/**
 * This is the Brickproof Bootloader's app descriptor.
 * Details: https://github.com/PX4/Firmware/tree/nuttx_next/src/drivers/bootloaders/src/uavcan
 */
alignas(8) struct AppDescriptor
{
    struct Flags
    {
        static constexpr std::uint16_t ReleaseBuild = 1U;
        static constexpr std::uint16_t DirtyBuild = 2U;
    };

    [[maybe_unused]] std::uint64_t magic = 0x5E44'1514'6FC0'C4C7ULL;  ///< Identification and byte order detection.
    [[maybe_unused]] std::array<std::uint8_t, 8> signature{{'A', 'P', 'D', 'e', 's', 'c', '0', '0'}};

    std::uint64_t image_crc = 0;  ///< CRC-64-WE of the firmware padded to 8 bytes computed with this field =0.
    [[maybe_unused]] std::uint32_t image_size = 0;  ///< Size of the application image in bytes padded to 8.

    /// Deprecated in favor of the larger, 64-bit VCS commit field. Eventually it may be reused for other purposes.
    [[maybe_unused]] std::uint32_t _legacy_vcs_revision_id = static_cast<std::uint32_t>(VCS_REVISION_ID >> 32U);

    std::uint8_t version[2] = {FW_VERSION_MAJOR, FW_VERSION_MINOR};  // NOLINT std::array<>
    std::uint8_t flags = Flags::ReleaseBuild | (DIRTY_BUILD ? Flags::DirtyBuild : 0U);
    [[maybe_unused]] std::uint8_t _reserved_a{};

    std::uint32_t build_timestamp_utc = BUILD_TIMESTAMP_UTC;  ///< Wraps every ~136 years. Unwrap when reading.
    std::uint64_t vcs_revision_id = VCS_REVISION_ID;

    [[maybe_unused]] std::array<std::byte, 16> _reserved_b{};
} const volatile _app_descriptor __attribute__((used, section(".app_descriptor")));

}
