#!/usr/bin/env python3
import math
from nav_msgs.msg import Odometry

import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np

from sensor_msgs.msg import LaserScan

from collections import defaultdict


# ===================================== #
# camera calibration matrix K
fx = 1360.3838
fy = 1360.38386
px = 960.5
py = 540.5

# rotation matrix R (in deg)
yaw =    0.0
pitch =  30.0
roll =   0.0 #right hand

# vehicle coords of camera origin
XCam = 0.0
YCam = 0.0
ZCam = 0.635

class FrameListener(Node):
    def __init__(self):
        super().__init__('turtle_tf2_frame_listener')

        # Declare and acquire `target_frame` parameter
        # self.target_frame = self.declare_parameter(
        #   'target_frame', 'turtle1').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        

      

        # Create turtle2 velocity publisher
        self.publisher = self.create_publisher(Odometry, 'champ', 10)

        # Call on_timer function every second
        self.timer = self.create_timer(0.1, self.on_timer)
    def euler_from_quaternion(self,x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (clockwise)
        pitch is rotation around y in radians (clockwise)
        yaw is rotation around z in radians (clockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return [math.degrees(roll_x), math.degrees(pitch_y), math.degrees(yaw_z)]  # in degree

    def on_timer(self):
    
        # Store frame names in variables that will be used to
        # compute transformations
        from_frame_rel = 'camera'
        to_frame_rel = 'base_footprint'

        try:
            t = self.tf_buffer.lookup_transform(
                to_frame_rel,
                from_frame_rel,
                rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
            return
       
        msg = Odometry()
        msg.pose.pose.position.x = t.transform.translation.x  
        msg.pose.pose.position.y = t.transform.translation.y 
        msg.pose.pose.position.z = t.transform.translation.z 

        msg.pose.pose.orientation.w = t.transform.rotation.w
        msg.pose.pose.orientation.x = t.transform.rotation.x
        msg.pose.pose.orientation.y = t.transform.rotation.y
        msg.pose.pose.orientation.z = t.transform.rotation.z

        # print(t.transform.rotation.z)
        # a = self.euler_from_quaternion(1.0,1.0,1.0,1.0)
        # print(a)

        # print(self.euler_from_quaternion(1.0,1.0,1.0,1.0))
        camera_pose = self.euler_from_quaternion(
            t.transform.rotation.x,
            t.transform.rotation.y,
            t.transform.rotation.z,
            t.transform.rotation.w)
        camera_pose.append(t.transform.translation.z)   
        print(camera_pose)

        # print(self.euler_from_quaternion(
        #     t.transform.rotation.x,
        #     t.transform.rotation.y,
        #     t.transform.rotation.z,
        #     t.transform.rotation.w))
        
        return self.euler_from_quaternion(
            t.transform.rotation.x,
            t.transform.rotation.y,
            t.transform.rotation.z,
            t.transform.rotation.w)


        # self.publisher.publish(msg)


class Camera():
    K = np.zeros([3, 3])
    R = np.zeros([3, 3])
    t = np.zeros([3, 1])
    P = np.zeros([3, 4]) # projection matrix

    def setK(self, fx, fy, px, py):
        self.K[0, 0] = fx
        self.K[1, 1] = fy
        self.K[0, 2] = px
        self.K[1, 2] = py
        self.K[2, 2] = 1.0

    def setR(self, y, p, r):
        Rz = np.array([[np.cos(-y), -np.sin(-y), 0.0], [np.sin(-y), np.cos(-y), 0.0], [0.0, 0.0, 1.0]])
        Ry = np.array([[np.cos(-p), 0.0, np.sin(-p)], [0.0, 1.0, 0.0], [-np.sin(-p), 0.0, np.cos(-p)]])
        Rx = np.array([[1.0, 0.0, 0.0], [0.0, np.cos(-r), -np.sin(-r)], [0.0, np.sin(-r), np.cos(-r)]])
        Rs = np.array([[0.0, -1.0, 0.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0]]) # switch axes (x = -y, y = -z, z = x)
        self.R = Rs.dot(Rz.dot(Ry.dot(Rx)))
    
    def setT(self, XCam, YCam, ZCam):
        X = np.array([XCam, YCam, ZCam])
        self.t = -self.R.dot(X)

    def updateP(self):
        Rt = np.zeros([3, 4])
        Rt[0:3, 0:3] = self.R
        Rt[0:3, 3] = self.t
        self.P = self.K.dot(Rt)
        return self.P

    def __init__(self):
        self.setK(fx, fy, px, py)
        self.setR(np.deg2rad(yaw), np.deg2rad(pitch), np.deg2rad(roll))
        self.setT(XCam, YCam, ZCam)
        self.project = self.updateP()


class Topview(object):
    def __init__(self):
        # initialize camera objects
        cams = Camera()
        # calculate output shape
        pxPerM = (50,50) # 20 px/1 m => 1 px/0.05 m
        self.outputRes = (int(9*pxPerM[0]),int(9*pxPerM[1])) # output 5 m each direction (200 * 200 px)
        # setup mapping from street/top-image plane to world coords
        shift = (self.outputRes[0] / 2.0, self.outputRes[1] / 2.0)
        # shift = (480,640)
        # M = np.array([[1.0 / pxPerM[1], 0.0, -shift[1] / pxPerM[1]], [0.0, -1.0 / pxPerM[0], shift[0] / pxPerM[0]], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        # M = np.array([[1.0 / pxPerM[1], 0.0, -shift[1] / pxPerM[1]], [0.0, -1.0 / pxPerM[0], shift[0] / pxPerM[0]], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        M = np.array([[1.0 / pxPerM[1], 0.0, 0], [0.0, -1.0 / pxPerM[0], shift[0] / pxPerM[0]], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        # find IPM as inverse of P*M
        # self.IPMs = {}
        self.IPMs = np.linalg.inv((cams.project).dot(M))
    
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image, 
      '/camera1/image_raw', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning

    self.publisher_ = self.create_publisher(Image, 'line', 10)
   



      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()


   
    self.publisher_scan = self.create_publisher(LaserScan, '/scan', 10)
   
  def listener_callback(self, data):
    """
    Callback function.
    """

   

    # Display the message on the console
    self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)

    # print(current_frame[0][0])

    mynode = Topview()
    result = cv2.warpPerspective(current_frame, mynode.IPMs, (mynode.outputRes[1]+200, mynode.outputRes[0]), flags=cv2.INTER_LINEAR)

    # cv2.imshow("camera", result)
    
    result2 = result.copy()



   
#crate lidar line
    length = 600
    angles = []
    for i in range(-90,90,1):
        angles.append(i)
    # print(angles)

    # Draw lines with different angles
    for angle in angles:
        radians = angle * np.pi / 180
        x2 = int(length * np.cos(radians))
        y2 = int(length * np.sin(radians))
        resault2=cv2.line(result2, (0, 225), (x2, 225+y2), (0, 0, 0), 1)
    # result2 = cv2.line(result2, (0,700), (800,0), (0,0,0), 1)

    result = abs(result-result2)

    cv2.imshow("camera", result)
    
    cv2.waitKey(1)


def main():
    rclpy.init()
    node = FrameListener()
    # node = ImageSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()

if __name__ == '__main__':
    main()

# # Import the necessary libraries
# import rclpy # Python library for ROS 2
# from rclpy.node import Node # Handles the creation of nodes
# from sensor_msgs.msg import Image # Image is the message type
# from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
# import cv2 # OpenCV library
# import numpy as np
# import math

# from sensor_msgs.msg import JointState

# from std_msgs.msg import Float32

# class ImageSubscriber(Node):
#     def __init__(self):
#         super().__init__('Image_Subcriber')
#         self.joint_sub_ = self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.joint_sub_callback,10
#         )
        
#         self.publisher_ = self.create_publisher(
#           #  String,
#            Float32,
#            'sua_test',
#            10
#         )

#     def joint_sub_callback(self, msg):
#       self.m = msg 
#       #  print(self.m.position[0]/math.pi * 180)
      
#       # print(self.get_clock().now().to_msg())
#       print(float(self.get_clock().now().to_msg().sec))

#       msg_str = Float32()
#       msg_str.data = float(self.get_clock().now().to_msg().sec)
#       # msg_str.data = 0.32
#       self.publisher_.publish(msg_str)




  
# def main(args=None):
  
#   # Initialize the rclpy library
#   rclpy.init(args=args)
  
#   # Create the node
#   image_subscriber = ImageSubscriber()
  
#   # Spin the node so the callback function is called.
#   rclpy.spin(image_subscriber)
  
#   # Destroy the node explicitly
#   # (optional - otherwise it will be done automatically
#   # when the garbage collector destroys the node object)
#   image_subscriber.destroy_node()
  
#   # Shutdown the ROS client library for Python
#   rclpy.shutdown()
  
# if __name__ == '__main__':
#   main()




