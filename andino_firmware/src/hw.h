#pragma once

namespace andino {

/// @brief
struct Hw {
  /// @brief Энкодер левого мотора канал A (digital pin 2)
  static constexpr int kLeftEncoderChannelAGpioPin{2};
  /// @brief Энкодер левого мотора канал B (digital pin 3)
  static constexpr int kLeftEncoderChannelBGpioPin{3};

  /// @brief Энкодер правого мотора канал A (analog pin A2)
  static constexpr int kRightEncoderChannelAGpioPin{16};
  /// @brief Энкодер правого мотора канал B (analog pin A3)
  static constexpr int kRightEncoderChannelBGpioPin{17};

  /// @brief Левый мотор IN1 (digital pin 6)
  static constexpr int kLeftMotorBackwardGpioPin{6};
  /// @brief Левый мотор IN2 (digital pin 10)
  static constexpr int kLeftMotorForwardGpioPin{10};
  /// @brief
  /// @note
  /// Левый мотор ENA (digital pin 13)
  static constexpr int kLeftMotorEnableGpioPin{13};

  /// @brief Правый мотор IN3 (digital pin 5)
  static constexpr int kRightMotorBackwardGpioPin{5};
  /// @brief Правый мотор IN4 (digital pin 9)
  static constexpr int kRightMotorForwardGpioPin{9};
  /// @brief
  /// @note
  /// Правый мотор ENB (digital pin 12)
  static constexpr int kRightMotorEnableGpioPin{12};

  /// @brief IMU I2C SCL (analog pin A5).
  static constexpr int kImuI2cSclPin{19};
  /// @brief IMU I2C SDA (analog pin A4)
  static constexpr int kImuI2cSdaPin{18};
};

}
