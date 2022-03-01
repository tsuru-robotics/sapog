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

    virtual std::size_t getAbsoluteAddressFromOffset(const std::size_t offset) const {
        return base_ + offset;
    }

    virtual std::size_t getBaseAddress() const {
        return writer_->getAddress();
    }

    virtual void setNewBase(const std::size_t base_address) { base_ = base_address; }

    [[nodiscard]] auto write(const std::size_t offset, const std::byte* const data, const std::size_t size)
        -> std::optional<std::size_t> override
    {
        if (!writer_)
        {
            return {};
        }
        volatile auto adj_offset = offset;
        auto          adj_size   = size;
        if (!adjustOffsetAndSize(adj_offset, adj_size))
        {
            chSysHalt("It is not good!");
            return {};
        }
        if (adj_offset < writer_->getAddress())
        {
            chSysHalt("It is not good!");
            return {};
        }
        if (adj_offset > writer_->getAddress())
        {
            chSysHalt("It is not good!");
            writer_->skip(adj_offset - writer_->getAddress());
        }
        assert(adj_offset == writer_->getAddress());
        writer_->erase(reinterpret_cast<const void*>(writer_->getAddress()), adj_size);
        if (writer_->write(data, adj_size))
        {
            writer_->advance_address(adj_size);
            return adj_size;
        }
        else
        {
            chSysHalt("It is not good!");
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
    bool adjustOffsetAndSize(volatile std::size_t& offset, std::size_t& size) const
    {
        offset += base_;  // To make this a device specific address
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

    volatile std::size_t base_;
    const std::size_t    end_ = FLASH_BASE + board::getFlashSize();

    std::optional<board::SequentialROMWriter> writer_;
};

}  // namespace sapog_bootloader
