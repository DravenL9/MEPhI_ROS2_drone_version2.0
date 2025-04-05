#pragma once

namespace andino {

/// @brief команды для отладки прошивки
struct Commands {
  /// @brief Reads an analog GPIO.
  static constexpr const char* kReadAnalogGpio{"a"};
  /// @brief Reads a digital GPIO.
  static constexpr const char* kReadDigitalGpio{"d"};
  /// @brief Reads the encoders tick count values.
  static constexpr const char* kReadEncoders{"e"};
  /// @brief Sets the encoders ticks count to zero.
  static constexpr const char* kResetEncoders{"r"};
  /// @brief Sets the motors speed [ticks/s].
  static constexpr const char* kSetMotorsSpeed{"m"};
  /// @brief Sets the motors PWM value [duty range: 0-255].
  static constexpr const char* kSetMotorsPwm{"o"};
  /// @brief Sets the PIDs tuning gains [format: "kp:kd:ki:ko"].
  static constexpr const char* kSetPidsTuningGains{"u"};
  /// @brief Gets whether there is an IMU sensor connected.
  static constexpr const char* kGetIsImuConnected{"h"};
  /// @brief Reads the encoders tick count values and IMU sensor data.
  static constexpr const char* kReadEncodersAndImu{"i"};
};

}  // namespace andino
