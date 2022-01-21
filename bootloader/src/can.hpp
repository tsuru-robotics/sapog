// Copyright (c) 2021  Zubax Robotics  <info@zubax.com>

#pragma once

#include <kocherga_can.hpp>
#include <bxcan.h>
#include <ch.hpp>
#include <board/board.hpp>

namespace sapog_bootloader
{
template <std::size_t TxQueueMemoryFootprint>
class CANDriver : public kocherga::can::ICANDriver
{
public:
    CANDriver() : heap_area_{} { ::chHeapObjectInit(&heap_, heap_area_, sizeof(heap_area_)); }

private:
    [[nodiscard]] auto configure(const Bitrate&                                  bitrate,
                                 const bool                                      silent,
                                 const kocherga::can::CANAcceptanceFilterConfig& filter) -> std::optional<Mode> override
    {
        ::BxCANTimings timings{};
        if (!::bxCANComputeTimings(STM32_PCLK1, bitrate.arbitration, &timings))
        {
            return {};
        }
        if (!::bxCANConfigure(0, timings, silent))
        {
            return {};
        }
        assert(filter.extended_can_id != 0 || filter.mask != 0);  // Zero-zero is treated as reject all (special case).
        std::array<::BxCANFilterParams, BXCAN_NUM_ACCEPTANCE_FILTERS> filter_params{};
        filter_params.at(0).extended_id   = filter.extended_can_id;
        filter_params.at(0).extended_mask = filter.mask;
        ::bxCANConfigureFilters(0, filter_params.data());
        tx_queue_.clear();
        return Mode::Classic;
    }

    [[nodiscard]] auto push(const bool          force_classic_can,
                            const std::uint32_t extended_can_id,
                            const std::uint8_t  payload_size,
                            const void* const   payload) -> bool override
    {
        const std::chrono::microseconds now = board::Clock::now().time_since_epoch();
        const bool ok = tx_queue_.push(now, force_classic_can, extended_can_id, payload_size, payload);
        poll(now);
        return ok;
    }

    [[nodiscard]] auto pop(PayloadBuffer& payload_buffer)
        -> std::optional<std::pair<std::uint32_t, std::uint8_t>> override
    {
        const std::chrono::microseconds                       now             = board::Clock::now().time_since_epoch();
        std::uint32_t                                         extended_can_id = 0;
        std::size_t                                           payload_size    = payload_buffer.size();
        std::optional<std::pair<std::uint32_t, std::uint8_t>> out;
        if (::bxCANPop(0, &extended_can_id, &payload_size, payload_buffer.data()))
        {
            last_io_at_ = now;
            out.emplace(std::pair<std::uint32_t, std::uint8_t>{
                extended_can_id,
                static_cast<std::uint8_t>(payload_size),
            });
        }
        poll(now);
        return out;
    }

    void poll(const std::chrono::microseconds now)
    {
        if (const auto* const item = tx_queue_.peek())
        {
            if (::bxCANPush(0,
                            now.count(),
                            std::chrono::duration_cast<std::chrono::microseconds>(now + kocherga::can::SendTimeout)
                                .count(),
                            item->extended_can_id,
                            item->payload_size,
                            item->payload))
            {
                last_io_at_ = now;
                tx_queue_.pop();
            }
        }
        board::setCANActivityLED(0, (now - last_io_at_) <= IfaceActivityLEDAfterglow);
    }

    [[nodiscard]] static auto getAllocFun(::memory_heap_t* const heap)
    {
        return [heap](const std::size_t x) -> void* { return chHeapAllocAligned(heap, x, sizeof(std::max_align_t)); };
    }

    static constexpr std::chrono::milliseconds IfaceActivityLEDAfterglow{25};

    std::chrono::microseconds last_io_at_{};

    CH_HEAP_AREA(heap_area_, TxQueueMemoryFootprint);  // NOLINT std::array<>
    ::memory_heap_t heap_{};

    // Can't use std::function<> because it uses heap.
    kocherga::can::TxQueue<decltype(getAllocFun(nullptr)), void (*)(void*)> tx_queue_{
        getAllocFun(&heap_),
        &::chHeapFree,
    };
};

}  // namespace sapog_bootloader
