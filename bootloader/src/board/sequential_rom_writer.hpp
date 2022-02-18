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

    [[nodiscard]] auto getAddress() const { return address_; }

    void skip(const std::size_t how_much) { address_ += how_much; }

private:

    static void waitReady()
    {
        do
        {
            assert(!(FLASH->SR & FLASH_SR_WRPRTERR));
#ifdef FLASH_SR_PGERR
            assert(!(FLASH->SR & FLASH_SR_PGERR));
#else
            assert(!(FLASH->SR & FLASH_SR_PGAERR));
            assert(!(FLASH->SR & FLASH_SR_PGPERR));
            assert(!(FLASH->SR & FLASH_SR_PGSERR));
#endif
        }
        while (FLASH->SR & FLASH_SR_BSY);
        FLASH->SR |= FLASH_SR_EOP;
    }

    struct Prologuer
    {
        const CriticalSectionLocker locker_;

        Prologuer()
        {
            waitReady();
            if (FLASH->CR & FLASH_CR_LOCK)
            {
                FLASH->KEYR = 0x45670123UL;
                FLASH->KEYR = 0xCDEF89ABUL;
            }
            FLASH->SR |= FLASH_SR_EOP | FLASH_SR_WRPRTERR |
#ifdef FLASH_SR_PGERR
                FLASH_SR_PGERR
#else
                FLASH_SR_PGAERR | FLASH_SR_PGPERR | FLASH_SR_PGSERR
#endif
                ;
            FLASH->CR = 0;
        }

        ~Prologuer()
        {
            FLASH->CR = FLASH_CR_LOCK;  // Reset the FPEC configuration and lock
        }
    };

    /**
     * This function maps an arbitrary address onto a flash sector number.
     * It need not be implemented for MCU which do not require sector numbers for operations on flash.
     * Returns negative if there's no match.
     */

public:
    /**
     * Source and destination must be aligned at two bytes.
     */
    bool write(const void* const what,
               const std::size_t how_much)
    {
        if (((reinterpret_cast<std::size_t>(address_)) % 2 != 0) ||
            ((reinterpret_cast<std::size_t>(what)) % 2 != 0) ||
            (reinterpret_cast<const void *>(address_) == nullptr) || (what == nullptr))
        {
            assert(false);
            return false;
        }

        const unsigned num_halfwords = (how_much + 1U) / 2U;

        volatile std::uint16_t* flashptr16 = reinterpret_cast<std::uint16_t*>(address_);
        const std::uint16_t* ramptr16 = static_cast<const std::uint16_t*>(what);

        {
            Prologuer prologuer;

#ifdef FLASH_CR_PSIZE_0
            FLASH->CR = FLASH_CR_PG | FLASH_CR_PSIZE_0;
#else
            FLASH->CR = FLASH_CR_PG;
#endif

            for (unsigned i = 0; i < num_halfwords; i++)
            {
                *flashptr16++ = *ramptr16++;
                waitReady();
            }

            waitReady();
            FLASH->CR = 0;
        }

        return std::memcmp(what, reinterpret_cast<const void *>(address_), how_much) == 0;
    }

    /**
     * Erases the specified region, possibly more if the region does not exactly match with the page/sector boundaries.
     */
    bool erase(const void* const where,
               const std::size_t how_much)
    {
#if defined(FLASH_CR_PER)
        for (std::size_t blank_check_pos = reinterpret_cast<std::size_t>(where);
            blank_check_pos < (reinterpret_cast<std::size_t>(where) + how_much);
            blank_check_pos++)
        {
            if (*reinterpret_cast<const std::uint8_t*>(blank_check_pos) != 0xFF)
            {

                // Erase operation
                {
                    Prologuer prologuer;
                    FLASH->CR = FLASH_CR_PER;
                    FLASH->AR = blank_check_pos;
                    FLASH->CR = FLASH_CR_PER | FLASH_CR_STRT;
                    waitReady();
                    FLASH->CR = 0;
                }

                // Immediate blank check
                if (*reinterpret_cast<const std::uint8_t*>(blank_check_pos) != 0xFF)
                {
                    // Interrupt immediately, otherwise we'll be stuck here erasing each byte unsuccessfully
                    return false;
                }

            }
        }
#else
        constexpr unsigned SmallestSectorSize = 1024;

        int sector_number = -1;

        for (std::size_t location = reinterpret_cast<std::size_t>(where);
             location < (reinterpret_cast<std::size_t>(where) + how_much);
             location += SmallestSectorSize)
        {
            const int new_sector_number = mapAddressToSectorNumber(location);
            if (new_sector_number < 0)
            {
                return false;
            }
            if (new_sector_number == sector_number)
            {
                continue;
            }
            sector_number = new_sector_number;
            DEBUG_LOG("Erasing at 0x%08x, sector %d\n", unsigned(location), sector_number);

            Prologuer prologuer;
            FLASH->CR = FLASH_CR_SER | (sector_number << 3);
            FLASH->CR |= FLASH_CR_STRT;
            waitReady();
            FLASH->CR = 0;
        }
#endif

        return std::all_of(reinterpret_cast<const std::uint8_t*>(where),
                           reinterpret_cast<const std::uint8_t*>(where) + how_much,
                           [](std::uint8_t x) { return x == 0xFF; });
    }

    std::size_t  address_;
    std::uint8_t next_sector_to_erase_;
};

}  // namespace board
