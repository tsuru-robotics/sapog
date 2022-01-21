// Copyright (c) 2021  Zubax Robotics  <info@zubax.com>

#pragma once

#include <board/board.hpp>
#include <board/sequential_rom_writer.hpp>
#include <kocherga.hpp>

namespace sapog_bootloader
{
class ROMBackend final : public kocherga::IROMBackend
{
public:
    explicit ROMBackend(const std::size_t base_address) : base_(FLASH_BASE + base_address) {}

    void beginWrite() override { writer_.emplace(base_); }

    void endWrite() override { writer_.reset(); }

    [[nodiscard]] auto write(const std::size_t offset, const std::byte* const data, const std::size_t size)
        -> std::optional<std::size_t> override
    {
        if (!writer_)
        {
            return {};
        }
        auto adj_offset = offset;
        auto adj_size   = size;
        if (!adjustOffsetAndSize(adj_offset, adj_size))
        {
            return {};
        }
        if (adj_offset < writer_->getAddress())
        {
            return {};
        }
        if (adj_offset > writer_->getAddress())
        {
            writer_->skip(adj_offset - writer_->getAddress());
        }
        assert(adj_offset == writer_->getAddress());
        if (writer_->append(data, adj_size))
        {
            return adj_size;
        }
        return {};
    }

    [[nodiscard]] auto read(const std::size_t offset, std::byte* const out_data, const std::size_t size) const
        -> std::size_t override
    {
        auto adj_offset = offset;
        auto adj_size   = size;
        if (adjustOffsetAndSize(adj_offset, adj_size))
        {
            std::memcpy(out_data, reinterpret_cast<const void*>(adj_offset), adj_size);  // NOLINT
            return adj_size;
        }
        return 0;
    }

private:
    bool adjustOffsetAndSize(std::size_t& offset, std::size_t& size) const
    {
        offset += base_;
        if (offset >= end_)
        {
            return false;
        }
        if ((offset + size) >= end_)
        {
            size = end_ - offset;
        }
        return true;
    }

    const std::size_t base_;
    const std::size_t end_ = FLASH_BASE + board::getFlashSize();

    std::optional<board::SequentialROMWriter> writer_;
};

}  // namespace sapog_bootloader
