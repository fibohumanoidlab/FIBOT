#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('traj_subscriber')
        # the topic name and message type used by the publisher and subscriber must match to allow them to communicate.
        self.subscription = self.create_subscription(
            Float32,
            'traj_test',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    # The callback definition simply prints an info message to the console, along with the data it received. 
    # Recall that the publisher defines msg.data = 'Hello World: %d' % self.i
    def listener_callback(self, msg):
        self.get_logger().info('Recieve Angle: "%f"' % msg.data)

# The main definition is almost exactly the same, replacing the creation 
# and spinning of the publisher with the subscriber
def main(args=None):
    rclpy.init(args=args)

    sub_subscriber = MinimalSubscriber()

    rclpy.spin(sub_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    sub_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
