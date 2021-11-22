// Copyright (c) 2021  Zubax Robotics  <info@zubax.com>
// Distributed under the MIT License, available in the file LICENSE.

#pragma once

#include <cstdint>
#include <optional>
#include <array>
#include <chrono>
#include <memory>
#include <cassert>

namespace uavcan_l6
{
/// This template shall be instantiable for each data type used by the application.
template<typename D>
struct DSDL final
{
    static constexpr std::size_t getExtent();

    struct Serializer
    {
        /// Returns pointer to the internal buffer where serialized data is stored.
        [[nodiscard]] const std::uint8_t *getBuffer() const;

        /// Returns the number of bytes stored in the internal buffer; empty option if the object is invalid.
        [[nodiscard]] std::optional<std::size_t> serialize(const D &obj);
    };

    /// Returns the deserialized object; empty option if the serialized representation is invalid.
    [[nodiscard]] static std::optional<D> deserialize(const std::size_t size, const std::uint8_t *const buffer);

    /// This type is not instantiable.
    DSDL() = delete;
};

}  // namespace uavcan_l6

/// This is used as a stop-gap solution until C++ code generation is implemented.
/// Use it like this with Nunavut-generated C code, once for every message type used in the application:
///     UAVCAN_L6_NUNAVUT_C_MESSAGE(uavcan_node_Heartbeat, 1, 0);
// NOLINTNEXTLINE
#define UAVCAN_L6_NUNAVUT_C_MESSAGE(nunavut_type_without_version, version_major, version_minor) \
    UAVCAN_L6_NUNAVUT_C(nunavut_type_without_version##_##version_major##_##version_minor)

/// Likewise, but for service types:
///     UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_node_GetInfo, 1, 0);
// NOLINTNEXTLINE
#define UAVCAN_L6_NUNAVUT_C_SERVICE(nunavut_type_without_version, version_major, version_minor)        \
    UAVCAN_L6_NUNAVUT_C_MESSAGE(nunavut_type_without_version##_Request, version_major, version_minor); \
    UAVCAN_L6_NUNAVUT_C_MESSAGE(nunavut_type_without_version##_Response, version_major, version_minor)
// The buffer that is left uninitialized always gets overridden during serialization anyway.
/// Implementation detail. Do not use this directly.
// NOLINTNEXTLINE
#define UAVCAN_L6_NUNAVUT_C(nunavut_type)                                                              \
    template <>                                                                                        \
    struct uavcan_l6::DSDL<nunavut_type> final                                                         \
    {                                                                                                  \
        static constexpr std::size_t getExtent() { return nunavut_type##_EXTENT_BYTES_; }              \
        struct Serializer            final                                                             \
        {                                                                                              \
            Serializer() { buffer_[0] = 0; } /* NOLINT buffer uninitialized intentionally */           \
            [[nodiscard]] const std::uint8_t*        getBuffer() const { return buffer_.data(); }      \
            [[nodiscard]] std::optional<std::size_t> serialize(const nunavut_type& obj)                \
            {                                                                                          \
                std::size_t sz = buffer_.size();                                                       \
                const bool  ok = nunavut_type##_serialize_(&obj, buffer_.data(), &sz) >= 0;            \
                assert(sz <= buffer_.size());                                                          \
                return ok ? sz : std::optional<std::size_t>{};                                         \
            }                                                                                          \
                                                                                                       \
        private:                                                                                       \
            std::array<std::uint8_t, nunavut_type##_SERIALIZATION_BUFFER_SIZE_BYTES_> buffer_;         \
        };                                                                                             \
        [[nodiscard]] static std::optional<nunavut_type> deserialize(const std::size_t         size,   \
                                                                     const std::uint8_t* const buffer) \
        {                                                                                              \
            nunavut_type obj{};                                                                        \
            std::size_t  sz = size;                                                                    \
            const bool   ok = nunavut_type##_deserialize_(&obj, buffer, &sz) >= 0;                     \
            return ok ? obj : std::optional<nunavut_type>{};                                           \
        }                                                                                              \
        DSDL() = delete;                                                                               \
    }

