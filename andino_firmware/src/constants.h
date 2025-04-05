#pragma once

namespace andino {

/// @brief Common constants.
struct Constants {
  /// @brief Serial port baud rate.
  static constexpr long kBaudrate{57600};

  /// @brief Time window to automatically stop the robot if no command has been received [ms].
  static constexpr long kAutoStopWindow{3000};

  /// @brief Minimum PWM wave duty cycle (0%) (see
  /// https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/).
  static constexpr int kPwmMin{30};
  /// @brief Maximum PWM wave duty cycle (100%) (see
  /// https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/).
  static constexpr int kPwmMax{255};

  /// @brief PID computation rate [Hz].
  static constexpr int kPidRate{30};
  /// @brief PID computation period [ms].
  static constexpr double kPidPeriod{1000 / kPidRate};
  /// @brief PID default tuning proportional gain.
  static constexpr int kPidKp{10};
  /// @brief PID default tuning derivative gain.
  static constexpr int kPidKd{10};
  /// @brief PID default tuning integral gain.
  static constexpr int kPidKi{0};
  /// @brief PID default tuning output gain.
  static constexpr int kPidKo{10};
};

}  // namespace andino
