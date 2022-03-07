/// Copyright (c) 2018  Zubax Robotics  <info@zubax.com>

#include "can.hpp"
#include "rom.hpp"
#include "app_shared.hpp"
#include <ch.hpp>
#include <cstdio>
#include "board/sys.hpp"

namespace sapog_bootloader
{
namespace
{
constexpr std::chrono::seconds BootDelayAfterWatchdogTimedOut(20);

[[nodiscard]] inline board::RGB mapStateToColor(const kocherga::State s)
{
    using kocherga::State;
    if (s == State::NoAppToBoot)
    {
        return board::Yellow;
    }
    if (s == State::AppUpdateInProgress)
    {
        return board::Blue;
    }
    assert((s == State::BootCanceled) || (s == State::BootDelay));
    return board::Green;
}

[[noreturn]] void finalize(const kocherga::Final fin)
{
    board::kickWatchdog();
    if (fin == kocherga::Final::BootApp)
    {
        board::bootApplication();
    }
    assert(fin == kocherga::Final::Restart);
    board::restart();
}

[[nodiscard]] kocherga::SystemInfo initSystemInfo()
{
    static auto coa = board::tryReadDeviceSignature();
    if (coa)
    {
        (void) coa;  // TODO: validate the RSA-1776 signature
    }
    kocherga::SystemInfo out{};
    out.hardware_version = board::detectHardwareVersion();
    out.unique_id = board::readUniqueID();
    out.node_name = "io.px4.sapog";
    if (coa)
    {
        out.certificate_of_authenticity_len = coa->size();
        out.certificate_of_authenticity = coa->data();
    }
    return out;
}

}  // namespace
}  // namespace sapog_bootloader

int main()
{
    const auto reset_cause = board::init(board::Cyan);
    static const auto system_info = sapog_bootloader::initSystemInfo();
    // ----------------------------------------------------------------------------------------------------------------
    // Initialize the bootloader. Boot immediately if everything is okay before adding the nodes/transports.
    // If we reset due to watchdog, add an extra delay to allow for intervention.
    const auto args = sapog_bootloader::takeAppShared();
    std::chrono::seconds boot_delay(1);

    if (reset_cause == board::ResetCause::Watchdog)
    {
        boot_delay = sapog_bootloader::BootDelayAfterWatchdogTimedOut;
    }
    static sapog_bootloader::ROMBackend rom_backend(APPLICATION_OFFSET);
    // Delaying to wait for print to work, which doesn't help actually
    static kocherga::Bootloader boot(rom_backend, system_info, board::getFlashSize(), bool(args), boot_delay, true);
    static const auto poll = []() {
        board::kickWatchdog();
        const auto now = board::Clock::now().time_since_epoch();
        const auto result = boot.poll(now);
        board::setRGBLED(sapog_bootloader::mapStateToColor(boot.getState()));
        return result;
    };
    if (const auto fin = poll())
    {
        sapog_bootloader::finalize(fin.value());
    }

    // ----------------------------------------------------------------------------------------------------------------
    // Fast boot is not possible -- initialize the interfaces.

    std::optional<kocherga::can::ICANDriver::Bitrate> can_bitrate{
        kocherga::can::ICANDriver::Bitrate{.arbitration=1000000, .data=1000000}};
    std::optional<std::uint8_t> uavcan_can_version = 1;
    std::optional<kocherga::NodeID> uavcan_can_node_id;
    if (args)
    {
        can_bitrate.emplace();
        can_bitrate->arbitration = args->can_bus_speed;
        uavcan_can_node_id = args->uavcan_node_id;
    }
    static sapog_bootloader::CANDriver<8192> can_driver;
    //
    static kocherga::can::CANNode can_node(can_driver,
                                           system_info.unique_id,
                                           can_bitrate,
                                           uavcan_can_version,
                                           uavcan_can_node_id);
    (void) boot.addNode(&can_node);

    // ------------------------------w----------------------------------------------------------------------------------
    // Commence the update process if requested by the application.
    if (args &&                                                                        //
        (args->uavcan_fw_server_node_id < std::numeric_limits<kocherga::NodeID>::max()))
    {
        const auto path_len = std::strlen(reinterpret_cast<const char *>(args->uavcan_file_name));  // NOLINT
        (void) boot.trigger(&can_node, args->uavcan_fw_server_node_id, path_len,
                            args->uavcan_file_name);
    }

    // ----------------------------------------------------------------------------------------------------------------
    // Run until either app boot or self-reboot.
    auto next_poll_at = chVTGetSystemTimeX();
    std::optional<kocherga::Final> fin;
    do
    {
        {
            board::RAIITestPointToggler<0> tp_toggler;
            fin = poll();
        }
        {
            board::RAIITestPointToggler<1> tp_toggler;
            next_poll_at = chThdSleepUntilWindowed(next_poll_at, next_poll_at + chTimeUS2I(10));
        }
    } while (!fin);
    sapog_bootloader::finalize(fin.value());
}