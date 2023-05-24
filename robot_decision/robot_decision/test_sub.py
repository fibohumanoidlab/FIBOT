#!/usr/bin python3
import py_trees
import py_trees_ros
import rcl_interfaces.msg as rcl_msgs
import rcl_interfaces.srv as rcl_srvs
import rclpy
from rclpy.node import Node
from humanoid_interfaces.msg import Ball,Robot
import std_msgs.msg as std_msgs
import py_trees.console as console

# class Nearest_Robot(py_trees.behaviour.Behaviour):
#     def __init__(self):
#         super(Nearest_Robot, self).__init__(name=name)
#         self.robot = Robot()
#         self.topic_name = topic_name
#         self.subscribe_topic ='/robot/nearest_id'
#         self.subscriber = self.node.create_subscription(msg_type=Robot,topic=self.subscribe_topic ,callback =self.callback_msg,qos_profile=1)
        
#     def callback_msg(self,msg):
#         self.msg_callback = msg.id_robot_nearest_ball
#         return  self.msg_callback



class Nearest_Robot(Node,py_trees.behaviour.Behaviour):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Robot,
            '/robot/nearest_id',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # self.get_logger().info('I heard: "%s"' % msg)
        console.info(str(msg.id_robot_nearest_ball))


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Nearest_Robot()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()