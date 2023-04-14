#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

# from std_msgs.msg import Int32MultiArray
# import cv2
# import numpy as np
# import time

from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
 






class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(LaserScan, '/scan2', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

        # self.subscription = self.create_subscription(
        #     Int32MultiArray,
        #     '/cv',
        #     self.timer_callback,
        #     10)
        # self.subscription  # prevent unused variable warnin

        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/cv',
            self.get_data2,
            10)
        self.subscription

        self.data2 = []
    
    def get_data2(self, msg):
        
        self.data2 = msg.data
        # print(self.data2)

        # return self.data2
    
    def get_data(self):
        return self.data2

       

    def timer_callback(self):
        scan_msg = LaserScan()
        
        scan_msg.header.frame_id = 'camera'
        scan_msg.angle_min = -3.14
        scan_msg.angle_max = 3.14
        scan_msg.angle_increment = 0.01
        scan_msg.time_increment = 0.0001
        scan_msg.scan_time = 0.1
        scan_msg.range_min = 0.0
        scan_msg.range_max = 100.0

        # scan_msg.ranges = [0.5,0.4,0.3,0.2,0.1]
        data = self.get_data()
        # print(data)
        if data is not None:
            # lst = [float(i) for i in data]
            lst = [1.125, 1.1250110864639282, 1.1250444650650024, 1.125100016593933, 1.1251777410507202, 1.1252777576446533, 1.1253999471664429]
            lst = [[0.1,0.2],1.2,1.3,1.4]
            print(lst)
            scan_msg.ranges = lst

        
        
        

        scan_data = [0.5] * int((scan_msg.angle_max - scan_msg.angle_min) / scan_msg.angle_increment)



        self.publisher_.publish(scan_msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    # minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()