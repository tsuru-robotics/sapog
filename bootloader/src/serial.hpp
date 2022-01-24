// Copyright (c) 2021  Zubax Robotics  <info@zubax.com>

#pragma once

#include <kocherga_serial.hpp>
#include "ch.h"
#include "hal.h"

namespace sapog_bootloader
{
class SerialPort final : public kocherga::serial::ISerialPort
{
public:
    [[nodiscard]] auto receive() -> std::optional<std::uint8_t> override
    {
        const auto res = chnGetTimeout(getChannel(), TIME_IMMEDIATE);
        return (res < 0) ? std::optional<std::uint8_t>{} : static_cast<std::uint8_t>(res);
    }

    [[nodiscard]] auto send(const std::uint8_t b) -> bool override
    {
        return STM_OK == chnPutTimeout(getChannel(), b, TIME_IMMEDIATE);
    }
private:


    [[nodiscard]] static auto getChannel() -> ::BaseChannel*
    {return reinterpret_cast<::BaseChannel*>(&STDOUT_SD);  // NOLINT
    }
};

}  // namespace sapog_bootloader
