#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math

class FakeLidar(Node):
    def __init__(self):
        super().__init__('fake_lidar')
        self.publisher = self.create_publisher(LaserScan, '/scan', 10)
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
        self.timer = self.create_timer(0.1, self.publish_scan)
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.get_logger().info('Fake LiDAR node started')

    def odom_callback(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

    def publish_scan(self):
        scan = LaserScan()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'base_link'
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = 2 * math.pi / 360
        scan.range_min = 0.12
        scan.range_max = 10.0

        # Simulate a circular wall around the robot at 2.0 metres
        ranges = []
        for i in range(360):
            angle = scan.angle_min + i * scan.angle_increment
            # Simulate walls at edges of a 4x4 room
            dist = min(
                abs(2.0 / math.cos(angle)) if math.cos(angle) != 0 else 10.0,
                abs(2.0 / math.sin(angle)) if math.sin(angle) != 0 else 10.0
            )
            dist = max(scan.range_min, min(dist, scan.range_max))
            ranges.append(dist)

        scan.ranges = ranges
        self.publisher.publish(scan)

def main(args=None):
    rclpy.init(args=args)
    node = FakeLidar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
