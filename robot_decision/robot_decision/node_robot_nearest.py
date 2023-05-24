import rclpy
import py_trees_ros
from humanoid_interfaces.msg import Robot
import py_trees.console as console
import random,time


class Robot_class(object):

    def __init__(self):
        self.node = rclpy.create_node(node_name="robot",)
        self.publisher_nearest = py_trees_ros.utilities.Publishers(
            self.node,
            [("robot","robot/nearest_id", Robot, False),] )
        
        self.publisher_distance= py_trees_ros.utilities.Publishers(
            self.node,
            [("robot","robot/distance_robot_ball", Robot, False),] )
        
        timer_period = 0.2  # seconds
        self.robot = Robot()
 
        self.timer = self.node.create_timer(
            timer_period_sec=timer_period,
            callback=self.timer_callback
        )
        self.i = 0



    def timer_callback(self):
        if self.i>=5 :
            self.robot.id_robot_nearest_ball = random.randint(1,4)
            # self.robot.id_robot_nearest_ball = 0
            # self.robot.id_robot_nearest_ball = 3
            # console.info(f'The Robot Id which nearest to the ball is : {self.robot.id_robot_nearest_ball} ')
            self.i=0
        else:
            
            self.i+=1

        self.robot.distance_robot_ball = 15.0
        self.publisher_nearest.robot.publish(self.robot)
        self.publisher_distance.robot.publish(self.robot)


    def shutdown(self):
        """
        Cleanup ROS components.
        """
        self.node.destroy_node()


def main():

    rclpy.init()  
    robot_class = Robot_class()
    try:
        rclpy.spin(robot_class.node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        robot_class.shutdown()
        rclpy.try_shutdown()

if __name__ == '__main__':
    
    main()