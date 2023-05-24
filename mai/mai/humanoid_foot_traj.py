#!/usr/bin/env python3

# node class
import rclpy
from rclpy.node import Node

# imports the built-in string message type that the node uses to structure the data that it passes on the topic
from std_msgs.msg import Float32MultiArray

import numpy as np
from humanoid_inv import leg

# x_start,x_stop,y_start,y_stop,z_start,z_mid,z_stop,time_middle,time_walking,isRight
# foot_input = [0,7,15,15,0,2,0,2,4,True]
# x_start,x_mid,x_stop,vx_start,vx_mid,vx_stop,accx_start,y_start,y_stop,z_start,z_stop,vz_start,vz_stop,time_middle,time_walking
# hip_input = [0,1,3,0,1,0,0,0,0,25,30,0,0,2,4]

class FootTrajPublisher(Node):
    def __init__(self, hip_input,foot_input):
        super().__init__('foot_traj_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'foot_traj_topic', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.timestamp_foot = self.get_clock().now().nanoseconds # loop control (ns)
        self.initial_foot = 1 # flag
        self.foot_x_traj = 0 # start x trajectory
        self.foot_y_traj = 0 # start y trajectory
        self.foot_z_traj = 0 # start z trajectory

        self.timestamp_hip = self.get_clock().now().nanoseconds # loop control (ns)
        self.initial_hip = 1 # flag
        self.hip_x_traj = 0 # start x trajectory
        self.hip_y_traj = 0 # start y trajectory
        self.hip_z_traj = 0 # start z trajectory

        self.foot_input = foot_input
        self.hip_input = hip_input
        
    # timer_callback creates a message with the counter value appended, 
    def timer_callback(self):
        
        msg = Float32MultiArray()
        msg.data = self.foot_joint_traj(self.foot_input,self.hip_input)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
    
    
    def foot_xyz_traj(self, foot_input):
        # x_start,x_stop,y_start,y_stop,z_start,z_mid,z_stop,time_middle,time_walking,isRight
        if (self.get_clock().now().nanoseconds - self.timestamp_foot >= 5000000): # 5 ms
            self.timestamp_foot = self.get_clock().now().nanoseconds
            if self.initial_foot:
                self.t_start_foot = self.get_clock().now().nanoseconds
                self.t_m_foot = foot_input[7] # s
                self.t_s_foot = foot_input[8] # s
                self.initial_foot = 0
                
            else:
                t_cont = (self.get_clock().now().nanoseconds - self.t_start_foot)*1e-9 # s
                self.foot_x_traj = foot_input[0]+3*(foot_input[1]-foot_input[0])*(t_cont**2)/(self.t_s_foot**2)-2*(foot_input[1]-foot_input[0])*(t_cont**3)/(self.t_s_foot**3)
                if int(foot_input[9]):
                    self.foot_y_traj = -foot_input[2]
                else:
                    self.foot_y_traj = foot_input[2]
                if (self.get_clock().now().nanoseconds - self.t_start_foot)*1e-9 <= self.t_m_foot:
                    self.foot_z_traj = foot_input[4]+3*(foot_input[5]-foot_input[4])*(t_cont**2)/(self.t_m_foot)**2-2*(foot_input[5]-foot_input[4])*(t_cont**3)/(self.t_m_foot)**3
                elif (self.get_clock().now().nanoseconds - self.t_start_foot)*1e-9 > self.t_m_foot and (self.get_clock().now().nanoseconds - self.t_start_foot)*1e-9 <= self.t_s_foot:
                    self.foot_z_traj = foot_input[5]+3*(foot_input[6]-foot_input[5])*(t_cont-self.t_m_foot)**2/(self.t_s_foot-self.t_m_foot)**2-2*(foot_input[6]-foot_input[5])*(t_cont-self.t_m_foot)**3/(self.t_s_foot-self.t_m_foot)**3
                elif ((self.get_clock().now().nanoseconds - self.t_start_foot)*1e-9 > self.t_s_foot) :
                    self.initial_foot = 1
        return [float(self.foot_x_traj), float(self.foot_y_traj), float(self.foot_z_traj)]
    
    def hip_xyz_traj(self, hip_input):
        # x_start,x_mid,x_stop,vx_start,vx_mid,vx_stop,accx_start,y_start,y_stop,z_start,z_stop,vz_start,vz_stop,time_middle,time_walking
        if (self.get_clock().now().nanoseconds - self.timestamp_hip >= 5000000): # 5 ms
            self.timestamp_hip = self.get_clock().now().nanoseconds
            if self.initial_hip:
                self.t_start_hip = self.get_clock().now().nanoseconds
                self.t_m_hip = hip_input[13] # s
                self.t_s_hip = hip_input[14] # s
                self.initial_hip = 0
                
            else:
                t_cont = (self.get_clock().now().nanoseconds - self.t_start_hip)*1e-9 # s
                self.hip_z_traj = hip_input[9]+hip_input[11]*t_cont+((3*(hip_input[10]-hip_input[9])-2*hip_input[11]*self.t_s_hip-hip_input[12]*self.t_s_hip)/(self.t_s_hip**2))*t_cont**2+((2*(hip_input[9]-hip_input[10])+(hip_input[11]+hip_input[12])*self.t_s_hip)/(self.t_s_hip**3))*t_cont**3
                self.hip_y_traj = hip_input[7]
                if (self.get_clock().now().nanoseconds - self.t_start_hip)*1e-9 <= self.t_m_hip:
                    self.hip_x_traj = hip_input[0]+hip_input[3]*t_cont+((hip_input[6]*t_cont**2)/2)+((hip_input[1]-hip_input[0]-hip_input[3]*self.t_m_hip-(1/2*hip_input[6]*self.t_m_hip**2))*t_cont**3/(self.t_m_hip**3))
                elif (self.get_clock().now().nanoseconds - self.t_start_hip)*1e-9 > self.t_m_hip and (self.get_clock().now().nanoseconds - self.t_start_hip)*1e-9 <= self.t_s_hip:
                    self.hip_x_traj = hip_input[1]+hip_input[4]*(t_cont-self.t_m_hip)+((3*(hip_input[2]-hip_input[1])-2*hip_input[4]*(self.t_s_hip-self.t_m_hip))*(t_cont-self.t_m_hip)**2/(self.t_s_hip-self.t_m_hip)**2)+(((2*(hip_input[1]-hip_input[2])+(hip_input[4]+hip_input[5])*(self.t_s_hip-self.t_m_hip))*(t_cont-self.t_m_hip)**3)/(self.t_s_hip-self.t_m_hip)**3)
                elif ((self.get_clock().now().nanoseconds - self.t_start_hip)*1e-9 > self.t_s_hip) :
                    self.initial_hip = 1
        return [float(self.hip_x_traj), float(self.hip_y_traj), float(self.hip_z_traj)]
    
    def foot_joint_traj(self, foot_input,hip_input):
        foot_xyz = self.foot_xyz_traj(foot_input)
        hip_xyz = self.hip_xyz_traj(hip_input)
        Hge = np.array([[0,0,1, foot_xyz[0]],[0,1,0,foot_xyz[1]],[-1,0,0,foot_xyz[2]],[0,0,0,1]])
        Hgb = np.array([[0,1,0, hip_xyz[0]],[-1,0,0,hip_xyz[1]],[0,0,1,hip_xyz[2]],[0,0,0,1]])
        Hbe = Hgb*np.linalg.inv(Hge)
        return leg(Hbe[0,3], Hbe[1,3], Hbe[2,3], foot_input[9]).inv_leg()

            
def main(args=None):
    # First the rclpy library is initialized, then the node is created, 
    rclpy.init(args=args)

    foot_traj_publisher = FootTrajPublisher()

    # and then it “spins” the node so its callbacks are called.
    rclpy.spin(foot_traj_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    foot_traj_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
  



