# Camera Calibration Script

import cv2
import yaml
import numpy as np

# Load the calibration parameters
def load_calibration(calib_file):
    with open(calib_file, 'r') as file:
        calib_data = yaml.safe_load(file)
        return calib_data['camera_matrix'], calib_data['distortion_coefficients']

# Save the calibration for future use
if __name__ == '__main__':
    camera_matrix, dist_coeffs = load_calibration('camera_calib.yml')
    print('Camera matrix:', camera_matrix)
    print('Distortion coefficients:', dist_coeffs)