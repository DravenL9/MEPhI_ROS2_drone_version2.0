#!/usr/bin/env python3
"""
camera_undistort — ROS2-нода для исправления искажений камеры.
Подписка:  /camera/image_raw
Публикация: /camera/image_undistorted
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraUndistortNode(Node):
    def __init__(self):
        super().__init__('camera_undistort')

        self.declare_parameter('calib_file', 'camera_calib.yml')
        self.declare_parameter('input_topic', '/camera/image_raw')
        self.declare_parameter('output_topic', '/camera/image_undistorted')

        self.calib_file = self.get_parameter('calib_file').get_parameter_value().string_value
        self.input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        self.output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        self.bridge = CvBridge()

        self.map1 = None
        self.map2 = None
        self.calib_loaded = False

        self.load_calibration(self.calib_file)

        self.sub = self.create_subscription(
            Image, self.input_topic, self.image_callback, 10
        )
        self.pub = self.create_publisher(Image, self.output_topic, 10)

        self.get_logger().info(
            f'camera_undistort started. input={self.input_topic} output={self.output_topic}'
        )

    def load_calibration(self, path):
        fs = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
        if not fs.isOpened():
            self.get_logger().warn(f"Calibration file not found: {path}")
            return
        K = fs.getNode("camera_matrix").mat()
        D = fs.getNode("dist_coeffs").mat()
        w = int(fs.getNode("image_width").real())
        h = int(fs.getNode("image_height").real())
        fs.release()

        self.map1, self.map2 = cv2.initUndistortRectifyMap(
            K, D, None, K, (w, h), cv2.CV_16SC2
        )
        self.calib_loaded = True
        self.get_logger().info("Calibration loaded")

    def image_callback(self, msg: Image):
        if not self.calib_loaded:
            return
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        undistorted = cv2.remap(frame, self.map1, self.map2, interpolation=cv2.INTER_LINEAR)
        out_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8')
        out_msg.header = msg.header
        self.pub.publish(out_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CameraUndistortNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()