#!/usr/bin/env python3

# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
import math

from sensor_msgs.msg import JointState

from std_msgs.msg import Float32

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('Image_Subcriber')
        self.joint_sub_ = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_sub_callback,10
        )
        
        self.publisher_ = self.create_publisher(
          #  String,
           Float32,
           'sua_test',
           10
        )

    def joint_sub_callback(self, msg):
      self.m = msg 
      #  print(self.m.position[0]/math.pi * 180)
      
      # print(self.get_clock().now().to_msg())
      print(float(self.get_clock().now().to_msg().sec))

      msg_str = Float32()
      msg_str.data = float(self.get_clock().now().to_msg().sec)
      # msg_str.data = 0.32
      self.publisher_.publish(msg_str)




  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()




