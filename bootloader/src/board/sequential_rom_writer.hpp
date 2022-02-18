/// Copyright (c) 2018  Zubax Robotics  <info@zubax.com>

#pragma once

#include <ch.hpp>
#include <cassert>
#include <cstring>
#include <cstdint>
#include <algorithm>

#if !defined(FLASH_SR_WRPRTERR)
#    define FLASH_SR_WRPRTERR FLASH_SR_WRPERR
#endif

namespace board
{
/// The code below assumes that the HSI oscillator running, otherwise the flash controller (FPEC) may misbehave.
/// Any FPEC issues will be detected at run time during write/erase verification.
class SequentialROMWriter
{
public:
    /// The address must be aligned at two bytes.
    explicit SequentialROMWriter(const std::size_t begin_address) : address_(begin_address), next_sector_to_erase_(0)
    {
        assert((address_ % 2U) == 0);
    }

    /// The source address and the length must be aligned at two bytes.
    /// The memory will be erased beforehand automatically as necessary.
    bool append(const void* const what, const std::size_t how_much)
    {
        if (((reinterpret_cast<std::size_t>(what)) % 2 != 0) || (what == nullptr))  // NOLINT
        {
            return false;
        }
        const std::size_t original_address = address_;
        // Erase the sectors that we're going to write into beforehand.
        // Advance the erase sector index as we go - we don't want to erase sectors more than once because
        // that would destroy data that we've written earlier.
        // Note that we use granular critical sections to reduce IRQ impact.
        for (std::size_t offset = 0; offset < how_much; offset++)
        {
            const auto sn = mapAddressToSectorNumber(address_);
            address_++;
            if (!sn)
            {
                return false;
            }
            if (*sn >= next_sector_to_erase_)
            {
                next_sector_to_erase_ = *sn;
                eraseSector(next_sector_to_erase_);
                next_sector_to_erase_++;
            }
        }
        // Now the memory is ready to be written. Run the write loop, two bytes per iteration.
        // We use a single big critical section to speed things up - writes are fast enough as they are.
        const std::size_t       num_half_words = (how_much + 1U) / 2U;
        volatile std::uint16_t* flashptr16     = reinterpret_cast<std::uint16_t*>(original_address);  // NOLINT
        const auto*             ramptr16       = static_cast<const std::uint16_t*>(what);
        {
            Prologuer prologuer;
            FLASH->CR = FLASH_CR_PG | FLASH_CR_PSIZE_0;
            for (std::size_t i = 0; i < num_half_words; i++)
            {
                *flashptr16++ = *ramptr16++;
                waitReady();
            }
            waitReady();
            FLASH->CR = 0;
        }
        // Final verification - compare the memory contents with the original data.
        return std::memcmp(what, reinterpret_cast<void*>(original_address), how_much) == 0;  // NOLINT
    }

    [[nodiscard]] auto getAddress() const { return address_; }

    void skip(const std::size_t how_much) { address_ += how_much; }

private:
    static void waitReady()
    {
        do
        {
            assert(!(FLASH->SR & FLASH_SR_WRPRTERR));
            assert(!(FLASH->SR & FLASH_SR_PGAERR));
        } while (FLASH->SR & FLASH_SR_BSY);
        FLASH->SR |= FLASH_SR_EOP;
    }

    struct Prologuer final
    {
        Prologuer()
        {
            waitReady();
            if (FLASH->CR & FLASH_CR_LOCK)
            {
                FLASH->KEYR = 0x45670123UL;
                FLASH->KEYR = 0xCDEF89ABUL;
            }
            FLASH->SR |= FLASH_SR_EOP | FLASH_SR_WRPRTERR | FLASH_SR_PGAERR;
            FLASH->CR = 0;
        }

        ~Prologuer()
        {
            FLASH->CR = FLASH_CR_LOCK;  // Reset the FPEC configuration and lock
        }

        Prologuer(const Prologuer&) = delete;
        Prologuer(Prologuer&&)      = delete;
        Prologuer& operator=(const Prologuer&) = delete;
        Prologuer& operator=(Prologuer&&) = delete;

    private:
        [[maybe_unused]] volatile const CriticalSectionLocker locker_;
    };

    static std::optional<std::uint8_t> mapAddressToSectorNumber(const std::size_t where)
    {
        // clang-format off
        if (where < 0x0800'0000U) { return {}; }
        if (where > 0x0803'FFFFU) { return {}; }
        return (where - 0x0800'0000U) / 2048U;
    }

    static void eraseSector(const std::uint8_t sector_index)
    {
        Prologuer prologuer;
        FLASH->CR |= FLASH_CR_PER_Msk;
        FLASH->AR = static_cast<std::uint32_t>(sector_index);
        FLASH->CR |= FLASH_CR_STRT;
        waitReady();
        FLASH->CR = 0;
    }

    std::size_t  address_;
    std::uint8_t next_sector_to_erase_;
};

}  // namespace board
