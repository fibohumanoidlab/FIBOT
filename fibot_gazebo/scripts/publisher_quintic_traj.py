#!/usr/bin/env python3

import math as m
from math import pi 

# node class
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from math import sin,cos
from geometry_msgs.msg import Quaternion

# imports the built-in string message type that the node uses to structure the data that it passes on the topic
from std_msgs.msg import Float32, String
from tf2_ros import TransformBroadcaster, TransformStamped
# the MinimalPublisher class is created, which inherits from (or is a subclass of) Node
class Publisher_quintic_traj(Node):

    def __init__(self):
        # super().__init__ calls the Node class’s constructor and gives it your node name, 
        # in this case minimal_publisher
        super().__init__('publisher_quintic_traj')

        ###
        # qos_profile = QoSProfile(depth=10)
        # self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        ###
        # create_publisher declares that the node publishes messages of type String (imported from the std_msgs.msg module), 
        # over a topic named topic, and that the “queue size” is 10
        self.publisher_ = self.create_publisher(Float32, 'traj_test', 10)
        # a timer is created with a callback to execute every 0.5 seconds
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i is a counter used in the callback
        # self.i = 0
        self.initial = 1
        self.desire_angle = 0
        self.time_initial = 0
        self.tau_max = 0
        self.c0 = 0
        self.c1 = 0
        self.c2 = 0
        self.c3 = 0
        self.c4 = 0
        self.c5 = 0
        self.start_angle = 0
        self.stop_angle = 0
        self.velo_max = 0
        self.acc_max = 0
        self.param_set = 1
        self.timestamp = self.get_clock().now().nanoseconds


    # timer_callback creates a message with the counter value appended, 
    def timer_callback(self):
        self.trajectory(pi,0.0,0.5,0.2)
        msg = Float32()
        msg.data = float(self.desire_angle)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'camera_link_fixed'
        t.child_frame_id = 'camera'
        t.transform.rotation = self.euler_to_quaternion(0,  msg.data,0)
        # self.broadcaster.sendTransform(t)

        # print("RRR")


        # self.publisher_.publish(msg)
        # publishes it to the console with get_logger().info
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1
    def euler_to_quaternion(self,roll, pitch, yaw):
        qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
        qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
        qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
        qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)
    
    def trajectory(self,stop_angle1,stop_angle2,velo_max,acc_max):
        if (self.get_clock().now().nanoseconds - self.timestamp >= 500000):
            # nanosecond
            self.timestamp = self.get_clock().now().nanoseconds
            if self.param_set == 1 and self.initial == 1:
                self.stop_angle = stop_angle1
                self.velo_max = velo_max
                self.acc_max = acc_max
                self.param_set = 0
                self.get_logger().info('param set1')
            elif self.param_set == 0 and self.initial == 1:
                self.stop_angle = stop_angle2
                self.velo_max = velo_max
                self.acc_max = acc_max
                self.param_set = 1
                self.get_logger().info('param set2')

            if (self.initial == 1 and self.stop_angle - self.start_angle != 0):
                if 15/8*(self.stop_angle - self.start_angle)/self.velo_max >= m.sqrt(abs(((10*m.pow(3+m.sqrt(3),1))-(5*m.pow(3+m.sqrt(3),2))+(5*m.pow(3+m.sqrt(3),3)/9))*(self.stop_angle-self.start_angle)/self.acc_max)) :
                    # second
                    self.tau_max = 15/8*(self.stop_angle - self.start_angle)/self.velo_max
                else :
                    # second
                    self.tau_max = m.sqrt(abs(((10*m.pow(3+m.sqrt(3),1))-(5*m.pow(3+m.sqrt(3),2))+(5*m.pow(3+m.sqrt(3),3)/9))*(self.stop_angle-self.start_angle)/self.acc_max)) 
                self.c0 = self.start_angle
                self.c1 = 0
                self.c2 = 0
                self.c3 = 10*((self.stop_angle-self.start_angle)/(m.pow(self.tau_max,3)))
                self.c4 = 15*((self.start_angle-self.stop_angle)/(m.pow(self.tau_max,4)))
                self.c5 = 6*((self.stop_angle-self.start_angle)/(m.pow(self.tau_max,5)))

                self.time_initial = self.get_clock().now().nanoseconds*1e-9 # second

                self.initial = 0
                self.get_logger().info('initial set')

            elif (self.initial == 0 and self.stop_angle - self.start_angle != 0):

                self.get_logger().info('check condition')
                if (self.get_clock().now().nanoseconds*1e-9 -self.time_initial>= self.tau_max):
                    
                    self.initial = 1
                    self.start_angle = self.desire_angle
                    self.get_logger().info('finish')

                else:
                    self.get_logger().info('calculating')
                    tau = self.get_clock().now().nanoseconds*1e-9-self.time_initial # second
                    self.desire_angle = self.c0*m.pow(tau,0)+self.c1*m.pow(tau,1)+self.c2*m.pow(tau,2)+self.c3*m.pow(tau,3)+self.c4*m.pow(tau,4)+self.c5*m.pow(tau,5)

def main(args=None):
    # First the rclpy library is initialized, then the node is created, 
    rclpy.init(args=args)

    traj_publisher = Publisher_quintic_traj()

    # and then it “spins” the node so its callbacks are called.
    rclpy.spin(traj_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    traj_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()