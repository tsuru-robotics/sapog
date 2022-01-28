/****************************************************************************
 *
 *   Copyright (C) 2013 PX4 Development Team. All rights reserved.
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

// TODO: rewrite in C++

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ch.h>
#include <hal.h>
#include <shell.h>
#include <chprintf.h>
#include <unistd.h>
#include <board/board.hpp>
#include <motor/motor.hpp>

#include <zubax_chibios/util/base64.hpp>
#include "console.hpp"

#pragma GCC diagnostic ignored "-Wunused-parameter"

static void cmd_cfg(BaseSequentialStream *, int argc, char *argv[])
{
  // TODO: refuse to save/erase while the motor is running
  /*for (int x = 0; x < argc; x++)
  {
    printf("%d %s\n", x, argv[x]);
  }*/
  if (!motor_is_running()) // This needs to check for the actual use of save/erase, motor controls should still work
  {
    os::config::executeCLICommand(argc, argv);
  }
}

static void cmd_reboot(BaseSequentialStream *chp, int argc, char *argv[])
{
  os::requestReboot();
}

static void cmd_beep(BaseSequentialStream *chp, int argc, char *argv[])
{
  if (argc > 0 && !strcmp(argv[0], "help"))
  {
    puts("beep [freq_hz [duration_msec]]");
    return;
  }

  int freq = 500;
  if (argc > 0)
  {
    freq = atoi(argv[0]);
  }

  int duration = 300;
  if (argc > 1)
  {
    duration = atoi(argv[1]);
  }

  motor_beep(freq, duration);
}

static void cmd_stat(BaseSequentialStream *chp, int argc, char *argv[])
{
  float voltage = 0, current = 0;
  motor_get_input_voltage_current(&voltage, &current);

  std::printf("Power V/A     %-9f %f\n", voltage, current);
  std::printf("RPM/DC        %-9u %f\n", motor_get_rpm(), motor_get_duty_cycle());
  std::printf("Active limits %i\n", motor_get_limit_mask());
  std::printf("ZC failures   %lu\n", (unsigned long) motor_get_zc_failures_since_start());
}

static void cmd_test(BaseSequentialStream *chp, int argc, char *argv[])
{
  puts("Hardware test...");
  int res = motor_test_hardware();
  if (res)
  {
    std::printf("FAILED %i\n", res);
  } else
  {
    puts("OK");
  }

  puts("Motor test...");
  res = motor_test_motor();
  puts(res ? "Not connected" : "Connected");
}

static void cmd_dc(BaseSequentialStream *chp, int argc, char *argv[])
{
  static const int TTL_MS = 30000;

  if (argc == 0)
  {
    motor_stop();
    puts("Usage:\n"
         "  dc <duty cycle>\n"
         "  dc arm");
    return;
  }

  // Safety check
  static bool _armed = false;
  if (!strcmp(argv[0], "arm"))
  {
    _armed = true;
    puts("OK");
    return;
  }
  if (!_armed)
  {
    puts("Error: Not armed");
    return;
  }

  const float value = atoff(argv[0]);
  std::printf("Duty cycle %f\n", value);
  motor_set_duty_cycle(value, TTL_MS);
}

static void cmd_rpm(BaseSequentialStream *chp, int argc, char *argv[])
{
  static const int TTL_MS = 30000;

  if (argc == 0)
  {
    motor_stop();
    puts("Usage:\n"
         "  rpm <RPM>\n"
         "  rpm arm");
    return;
  }

  // Safety check
  static bool _armed = false;
  if (!strcmp(argv[0], "arm"))
  {
    _armed = true;
    puts("OK");
    return;
  }
  if (!_armed)
  {
    puts("Error: Not armed");
    return;
  }

  long value = (long) atoff(argv[0]);
  value = (value < 0) ? 0 : value;
  value = (value > 65535) ? 65535 : value;
  std::printf("RPM %li\n", value);
  motor_set_rpm((unsigned) value, TTL_MS);
}

static void cmd_startstop(BaseSequentialStream *chp, int argc, char *argv[])
{
  static const int TTL_MS = 5000;

  if (argc == 0)
  {
    motor_stop();
    puts("Usage:\n"
         "  startstop <number of cycles> [duty cycle = 0.1]");
    return;
  }

  motor_stop();

  const int num_cycles = (int) atoff(argv[0]);
  const float dc = (argc > 1) ? atoff(argv[1]) : 0.1;

  int current_cycle = 0;

  for (; current_cycle < num_cycles; current_cycle++)
  {
    printf("Cycle %d of %d, dc %f...\n", current_cycle + 1, num_cycles, dc);

    // Waiting for the motor to spin down
    sleep(5);
    if (!motor_is_idle())
    {
      puts("NOT STOPPED");
      break;
    }

    // Starting with the specified duty cycle
    motor_set_duty_cycle(dc, TTL_MS);

    // Checking if started and stopping
    sleep(3);
    if (!motor_is_running())
    {
      puts("NOT RUNNING");
      break;
    }

    motor_stop();
  }

  printf("Finished %d cycles of %d\n", current_cycle, num_cycles);
}

static void cmd_md(BaseSequentialStream *chp, int argc, char *argv[])
{
  motor_print_debug_info();
}

static void cmd_m(BaseSequentialStream *chp, int argc, char *argv[])
{
  motor_execute_cli_command(argc, (const char **) argv);
}

static void cmd_zubax_id(BaseSequentialStream *chp, int argc, char *argv[])
{
  if (argc == 0)
  {
    // Product identification
    printf("product_id   : '%s'\n", NODE_NAME);
    printf("product_name : 'PX4 Sapog'\n");

    // SW version
    printf("sw_version   : '%u.%u'\n", FW_VERSION_MAJOR, FW_VERSION_MINOR);
    printf("sw_vcs_commit: %u\n", unsigned(GIT_HASH));
    printf("sw_build_date: %s\n", __DATE__);

    // HW version
    const auto hw_version = board::detect_hardware_version();
    printf("hw_version   : '%u.%u'\n", hw_version.major, hw_version.minor);

    // Unique ID and signature
    char base64_buf[os::base64::predictEncodedDataLength(std::tuple_size<board::DeviceSignature>::value) + 1];
    std::array<std::uint8_t, 16> uid_128;
    std::fill(std::begin(uid_128), std::end(uid_128), 0);
    {
      const auto uid = board::read_unique_id();
      std::copy(std::begin(uid), std::end(uid), std::begin(uid_128));
    }
    printf("hw_unique_id : '%s'\n", os::base64::encode(uid_128, base64_buf));
    board::DeviceSignature signature;
    if (board::try_read_device_signature(signature))
    {
      printf("hw_signature : '%s'\n", os::base64::encode(signature, base64_buf));

      std::memset(&base64_buf[0], 0, sizeof(base64_buf));
      for (unsigned i = 0; i < 16; i++)
      {
        chsnprintf(&base64_buf[i * 2], 3, "%02x", uid_128[i]);
      }
      printf("hw_info_url  : http://device.zubax.com/device_info?uid=%s\n", &base64_buf[0]);
    }
  } else if (argc == 1)
  {
    const char *const encoded = argv[0];
    board::DeviceSignature sign;

    if (!os::base64::decode(sign, encoded))
    {
      std::puts("Error: Invalid base64");
      return;
    }

    if (!board::try_write_device_signature(sign))
    {
      std::puts("Error: Write failed");
      return;
    }
  } else
  {
    std::puts("Error: Invalid usage. Format: zubax_id [base64 signature]");
  }
}

#define COMMAND(cmd)    {#cmd, cmd_##cmd},
static const ShellCommand _commands[] =
  {
    COMMAND(cfg)
    COMMAND(reboot)
    COMMAND(beep)
    COMMAND(stat)
    COMMAND(test)
    COMMAND(dc)
    COMMAND(rpm)
    COMMAND(startstop)
    COMMAND(md)
    COMMAND(m)
    COMMAND(zubax_id)
    {NULL, NULL}
  };

// --------------------------

static const ShellConfig _config = {(BaseSequentialStream *) &STDOUT_SD, _commands};

static THD_WORKING_AREA(_wa_shell, 1024);

void console_init(void)
{
  shellInit();
  ASSERT_ALWAYS(shellCreateStatic(&_config, _wa_shell, sizeof(_wa_shell), LOWPRIO));
}
