#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
from std_msgs.msg import Float32
from math import sin,cos
from geometry_msgs.msg import Quaternion

class StatePublisher(Node):
    def __init__(self):
        super().__init__('state_subscriber')
        self.subscription = self.create_subscription(
            Float32,
            'traj_test',
            self.listener_callback,
            10)
        self.subscription

        self.odom_trans = TransformStamped()
        # self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.header.frame_id = 'base_link'
        self.odom_trans.child_frame_id = 'camera_link'

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)

        self.joint_state = JointState()

    def listener_callback(self, msg):
        # t = TransformStamped()
        # t.header.stamp = self.get_clock().now().to_msg()
        # t.header.frame_id = 'base_link'
        # t.child_frame_id = 'camera_link'
        # t.transform.rotation = euler_to_quaternion(0, 0, msg.data)

        # Send the transformation
        # self.broadcaster.sendTransform(t)
        

        now = self.get_clock().now()
        self.joint_state.header.stamp = now.to_msg()

        self.odom_trans.header.stamp = now.to_msg()
        self.odom_trans.transform.rotation = euler_to_quaternion(0, 0, msg.data) # roll,pitch,yaw 

        self.joint_pub.publish(self.joint_state)
        self.broadcaster.sendTransform(self.odom_trans)

def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main(args=None):
    rclpy.init(args=args)
    node = StatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    