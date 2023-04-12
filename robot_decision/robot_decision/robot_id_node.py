import rclpy
from rclpy.node import Node
from humanoid_interfaces.msg import Robot

class Robot_class(Node):

    def __init__(self):
        super().__init__('Robot_class')
        self.node = rclpy.create_node(node_name = 'Robot_id')
        self.publisher_ = self.create_publisher(Robot, 'robot/nearest_id', 10)
        self.call_back = self.create_timer(
            timer_period_sec= 0.5, 
            callback= self.timer_callback
        )
        self.Robot_msg = Robot()

    def timer_callback(self):
        print('call back')
        self.Robot_msg.id_robot_nearest_ball = 100
        self.publisher_.publish(self.Robot_msg)
        print(self.Robot_msg)

    def shutdown(self):
        """
        Cleanup ROS components.
        """
        self.node.destroy_node()


def main():

    rclpy.init()  

    robot_class = Robot_class()

    # ball_class.destroy_node()
    # rclpy.shutdown()
    try:
        rclpy.spin(robot_class)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        robot_class.shutdown()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()

 
        