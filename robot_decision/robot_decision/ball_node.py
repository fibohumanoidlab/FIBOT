import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import py_trees_ros
# from py_trees_ros_interfaces.msg import Ball
from humanoid_interfaces.msg import Ball

class Ball_class(Node):

    def __init__(self):
        super().__init__('ball_class')
        self.node = rclpy.create_node(node_name="ball",)
        self.publisher_ = self.create_publisher(Ball, 'ball/detection', 10)
        # self.publishers = py_trees_ros.utilities.Publishers(
        #     self.node,
        #     [
        #         ("ball","ball/detection", Ball, False),
        #     ]
        # )
        timer_period = 0.5  # seconds
 
        self.timer = self.create_timer(timer_period_sec = timer_period, callback=self.timer_callback)
        self.i = 0
        self.ball = Ball()
        print('starting node')

    def timer_callback(self):
        print('call back')
        if self.i >= 10 : 
            self.ball.is_detected = True
            print(self.ball)
        else :
            self.ball.is_detected = False
            print(self.ball)
            self.i += 1

        self.publisher_.publish(self.ball)


    def shutdown(self):
        """
        Cleanup ROS components.
        """
        self.node.destroy_node()


def main():

    rclpy.init()  

    ball_class = Ball_class()

    # ball_class.destroy_node()
    # rclpy.shutdown()
    try:
        rclpy.spin(ball_class)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        ball_class.shutdown()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()

