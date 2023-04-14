#!/usr/bin/env python3

# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np

from std_msgs.msg import Float32MultiArray

import math



# ===================================== #
# camera calibration matrix K
fx = 1360.3838
fy = 1360.38386
px = 960.5
py = 540.5

# rotation matrix R (in deg)
yaw =    0.0
pitch =  19.42
# pitch =  45.0
roll =   0.0 #right hand

# vehicle coords of camera origin
XCam = 0.0
YCam = 0.0
ZCam = 0.63


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
    self.publisher_2 = self.create_publisher(Float32MultiArray, '/cv', 10)



      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """

   

    # Display the message on the console
    self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)

    mynode = Topview()
    # result = cv2.warpPerspective(current_frame, mynode.IPMs, (mynode.outputRes[1]+200, mynode.outputRes[0]), flags=cv2.INTER_LINEAR)
    result = cv2.warpPerspective(current_frame, mynode.IPMs, (mynode.outputRes[1], mynode.outputRes[0]), flags=cv2.INTER_LINEAR)

    result2 = result.copy()
    result3 = result.copy()
    
    # result2 = cv2.line(result2, (0,225), (450,225), (0,0,0), 1)
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
        cv2.line(result2, (0, 256), (x2, 256+y2), (0, 0, 0), 1)

    
    result = abs(result-result2)
    result3 = result.copy()
    cv2.imshow("camera", result)
    #################### sua #####################
    # img_array = np.array(result)

    # # Create boolean mask of white pixels
    # white_mask = np.all(img_array == [255, 255, 255], axis=-1)

    # # Find indices of True values in mask
    # white_indices = np.where(white_mask)
    # x = np.stack((white_indices[0],white_indices[1]),axis=-1)
    #########################################
    # Display image
    
    # cv2.waitKey(0)


    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # apply Canny edge detector
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # apply Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
    
    # draw detected lines on original image
    # print(lines)
    
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 10000*(-b))
            y1 = int(y0 + 10000*(a))
            x2 = int(x0 - 10000*(-b))
            y2 = int(y0 - 10000*(a))
            cv2.line(result, (x1, y1), (x2, y2), (255, 0, 0), 1)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # Threshold the image to create a binary image
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    white_pixels = cv2.findNonZero(thresh)
    b=np.array([[100, 100]])
    # print(b)
    # print(b.shape)
    m=np.array([[100, 100]])
    # print((white_pixels).shape)
    if white_pixels is not None:
        for row0 in white_pixels:
        
            # m=[[0,0]]
            # print(row0)
            # print(type(row0))
            # matrix =[1, 2, 3]
            # b=[[0, 0]]
            c=row0-np.array([225, 0])
            # print(c)
            # print(c.shape)
            m=np.append(m,c,axis = 0)
        # print(m)
    # print(m[1:])
    d=m[1:]
    # print(d)
        # print(type(m))
    # matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    list=[]
    for row1 in d:
        # print(row1)
        cc = math.sqrt(row1[0]**2 + row1[1]**2)
        list.append((cc)/200)
        # print(list)
    for row in list:
        # print(row)
        msg = Float32MultiArray()
        msg.data = (np.array(list).flatten().tolist())
        self.publisher_2.publish(msg)
    
   

    self.publisher_.publish(self.br.cv2_to_imgmsg(result3, encoding='rgb8'))
    
    cv2.waitKey(1)



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
        M = np.array([[1.0 / pxPerM[1], 0.0, 0.0], [0.0, -1.0 / pxPerM[0], shift[0] / pxPerM[0]], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        # find IPM as inverse of P*M
        # self.IPMs = {}
        self.IPMs = np.linalg.inv((cams.project).dot(M))
  
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





