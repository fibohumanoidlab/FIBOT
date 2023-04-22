#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math as m
from math import pi 
from std_msgs.msg import Float32

import rclpy
from std_msgs.msg import Float64MultiArray

# def main(args=None):
#     rclpy.init(args=args)
#     node = rclpy.create_node('publisher')
#     publisher = node.create_publisher(Float64MultiArray, '/forward_command_controller/commands', 10)

#     msg = Float64MultiArray()
#     msg.data = [3.0]

#     while rclpy.ok():
#         publisher.publish(msg)
#         node.get_logger().info('Published: "%s"' % msg.data)
#         rclpy.spin_once(node)

#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        # self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 2)
        self.publisher_ = self.create_publisher(Float64MultiArray, '/forward_command_controller/commands', 1)
        self.publisher2 = self.create_publisher(Float32, 'traj_test', 10)
        self.timer_ = self.create_timer(0.01, self.publish_trajectory)
        # self.joint_names_ = ['yaw_camera_joint','camera_joint']
        self.joint_names_ = ['camera_joint']
        self.position = 0.75
        self.invert = 1
        # self.finalposition = 1.57

        # initial traj
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
    def trajectory(self,stop_angle1,stop_angle2,velo_max,acc_max):
        if (self.get_clock().now().nanoseconds - self.timestamp >= 50000):
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
  
    def publish_trajectory(self):
        #run traj
        self.trajectory(0.85,0.5,0.05,0.05) #stop_angle1,stop_angle2,velo_max,acc_max

        msg2 = Float32()
        msg2.data = float(self.desire_angle)
        self.publisher2.publish(msg2)

        msg = Float64MultiArray()
        msg.data = [float(self.desire_angle)]

        
        # point.velocities = [0.0, 0.0]
        # # point.velocities = [0.0]
        # point.time_from_start = rclpy.duration.Duration(seconds=1.0).to_msg()

        # msg.points = [point]
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
#################################################################################
# class TrajectoryPublisher(Node):
#     def __init__(self):
#         super().__init__('trajectory_publisher')
#         self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 2)
#         # self.publisher_ = self.create_publisher(Float64MultiArray, '/forward_command_controller/commands', 10)
#         self.publisher2 = self.create_publisher(Float32, 'traj_test', 10)
#         self.timer_ = self.create_timer(1.0, self.publish_trajectory)
#         self.joint_names_ = ['yaw_camera_joint','camera_joint']
#         # self.joint_names_ = ['camera_joint']
#         self.position = 0.75
#         self.invert = 1
#         # self.finalposition = 1.57

#         # initial traj
#         self.initial = 1
#         self.desire_angle = 0
#         self.time_initial = 0
#         self.tau_max = 0
#         self.c0 = 0
#         self.c1 = 0
#         self.c2 = 0
#         self.c3 = 0
#         self.c4 = 0
#         self.c5 = 0
#         self.start_angle = 0
#         self.stop_angle = 0
#         self.velo_max = 0
#         self.acc_max = 0
#         self.param_set = 1
#         self.timestamp = self.get_clock().now().nanoseconds
#     def trajectory(self,stop_angle1,stop_angle2,velo_max,acc_max):
#         if (self.get_clock().now().nanoseconds - self.timestamp >= 50000):
#             # nanosecond
#             self.timestamp = self.get_clock().now().nanoseconds
#             if self.param_set == 1 and self.initial == 1:
#                 self.stop_angle = stop_angle1
#                 self.velo_max = velo_max
#                 self.acc_max = acc_max
#                 self.param_set = 0
#                 self.get_logger().info('param set1')
#             elif self.param_set == 0 and self.initial == 1:
#                 self.stop_angle = stop_angle2
#                 self.velo_max = velo_max
#                 self.acc_max = acc_max
#                 self.param_set = 1
#                 self.get_logger().info('param set2')

#             if (self.initial == 1 and self.stop_angle - self.start_angle != 0):
#                 if 15/8*(self.stop_angle - self.start_angle)/self.velo_max >= m.sqrt(abs(((10*m.pow(3+m.sqrt(3),1))-(5*m.pow(3+m.sqrt(3),2))+(5*m.pow(3+m.sqrt(3),3)/9))*(self.stop_angle-self.start_angle)/self.acc_max)) :
#                     # second
#                     self.tau_max = 15/8*(self.stop_angle - self.start_angle)/self.velo_max
#                 else :
#                     # second
#                     self.tau_max = m.sqrt(abs(((10*m.pow(3+m.sqrt(3),1))-(5*m.pow(3+m.sqrt(3),2))+(5*m.pow(3+m.sqrt(3),3)/9))*(self.stop_angle-self.start_angle)/self.acc_max)) 
#                 self.c0 = self.start_angle
#                 self.c1 = 0
#                 self.c2 = 0
#                 self.c3 = 10*((self.stop_angle-self.start_angle)/(m.pow(self.tau_max,3)))
#                 self.c4 = 15*((self.start_angle-self.stop_angle)/(m.pow(self.tau_max,4)))
#                 self.c5 = 6*((self.stop_angle-self.start_angle)/(m.pow(self.tau_max,5)))

#                 self.time_initial = self.get_clock().now().nanoseconds*1e-9 # second

#                 self.initial = 0
#                 self.get_logger().info('initial set')

#             elif (self.initial == 0 and self.stop_angle - self.start_angle != 0):

#                 self.get_logger().info('check condition')
#                 if (self.get_clock().now().nanoseconds*1e-9 -self.time_initial>= self.tau_max):
                    
#                     self.initial = 1
#                     self.start_angle = self.desire_angle
#                     self.get_logger().info('finish')

#                 else:
#                     self.get_logger().info('calculating')
#                     tau = self.get_clock().now().nanoseconds*1e-9-self.time_initial # second
#                     self.desire_angle = self.c0*m.pow(tau,0)+self.c1*m.pow(tau,1)+self.c2*m.pow(tau,2)+self.c3*m.pow(tau,3)+self.c4*m.pow(tau,4)+self.c5*m.pow(tau,5)
  
#     def publish_trajectory(self):
#         #run traj
#         self.trajectory(0.85,0.5,0.05,0.05) #stop_angle1,stop_angle2,velo_max,acc_max

#         msg2 = Float32()
#         msg2.data = float(self.desire_angle)
#         self.publisher2.publish(msg2)

#         msg = JointTrajectory()
#         msg.header.stamp = self.get_clock().now().to_msg()
#         # msg.header.stamp = rospy.Time.now()
#         msg.joint_names = self.joint_names_
#         # points=[]
#         point = JointTrajectoryPoint()

#         point.positions = [0.0, float(self.desire_angle)]
#         # point.positions = [float(self.desire_angle)]
        
#         msg = Float64MultiArray()
#         msg.data = [float(self.desire_angle)]

        
#         # point.velocities = [0.0, 0.0]
#         # # point.velocities = [0.0]
#         # point.time_from_start = rclpy.duration.Duration(seconds=1.0).to_msg()

#         # msg.points = [point]
#         self.publisher_.publish(msg)

# def main(args=None):
#     rclpy.init(args=args)
#     node = TrajectoryPublisher()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
###############################################################################################
# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

# class TrajectoryPublisher(Node):
#     def __init__(self):
#         super().__init__('trajectory_publisher')
#         self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 20)
#         self.timer_ = self.create_timer(15, self.publish_trajectory)
#         self.joint_names_ = ['yaw_camera_joint','camera_joint']
#         self.position = 0.75
#         self.invert = 1
#         # self.finalposition = 1.57
  
#     def publish_trajectory(self):
#         msg = JointTrajectory()
#         msg.header.stamp = self.get_clock().now().to_msg()
#         # msg.header.stamp = rospy.Time.now()
#         msg.joint_names = self.joint_names_
#         # points=[]
#         point = JointTrajectoryPoint()

#         point.positions = [0.0, self.position]
        
#         self.invert = -1 * self.invert

#         self.position = self.position  + (self.invert *0.75/3)

#         # print(self.position)

        
#         point.velocities = [0.0, 0.0]
#         point.time_from_start = rclpy.duration.Duration(seconds=15).to_msg()

#         msg.points = [point]
#         self.publisher_.publish(msg)

# def main(args=None):
#     rclpy.init(args=args)
#     node = TrajectoryPublisher()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
########################################################################################
    
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import JointState

# class JointStatePublisher(Node):
#     def __init__(self):
#         super().__init__('joint_state_publisher')
#         self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)
#         self.timer = self.create_timer(0.01, self.publish_joint_states)

#     def publish_joint_states(self):
#         msg = JointState()
#         msg.header.stamp = self.get_clock().now().to_msg()
#         # msg.header.stamp = rc
#         print(self.get_clock().now().to_msg())
#         msg.name = ['camera_joint']
#         msg.position = [1.0]
#         self.publisher_.publish(msg)

# def main(args=None):
#     rclpy.init(args=args)
#     node = JointStatePublisher()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


































