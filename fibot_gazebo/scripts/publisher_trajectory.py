#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.timer_ = self.create_timer(3, self.publish_trajectory)
        self.joint_names_ = ['yaw_camera_joint','camera_joint']
        self.position = 0.1
        # self.finalposition = 1.57
  
    def publish_trajectory(self):
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        # msg.header.stamp = rospy.Time.now()
        msg.joint_names = self.joint_names_
        # points=[]
        point = JointTrajectoryPoint()

        self.position = self.position * -1.0

        # print(self.position)

        point.positions = [0.0, self.position]
        point.velocities = [0.0, 0.0]
        point.time_from_start = rclpy.duration.Duration(seconds=3).to_msg()

        msg.points = [point]
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

    
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
#         msg.name = ['yaw_camera_joint']
#         msg.position = [3.0]
#         self.publisher_.publish(msg)

# def main(args=None):
#     rclpy.init(args=args)
#     node = JointStatePublisher()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


































