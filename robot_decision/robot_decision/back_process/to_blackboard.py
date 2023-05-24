#!/usr/bin/env python3

import py_trees
import rclpy.qos
import py_trees.console as console
from py_trees_ros import subscribers
from humanoid_interfaces.msg import Ball,Robot

class BallToBlackBoard(subscribers.ToBlackboard):

    def __init__(self,name: str,topic_name: str,qos_profile: rclpy.qos.QoSProfile):
        super().__init__(name=name,
                         topic_name=topic_name,
                         topic_type=Ball,
                         qos_profile=qos_profile,
                         blackboard_variables={"msg_ball": None},
                         clearing_policy=py_trees.common.ClearingPolicy.NEVER
                        )
        
        self.blackboard.register_key(key="is_ball_detected",access=py_trees.common.Access.WRITE)
        # self.blackboard.register_key(key="nearest_id", access=py_trees.common.Access.READ)
      
        self.blackboard.msg_ball = Ball()
        self.blackboard.msg_ball.is_detected  = False  # decision making

    def update(self):
        status = super(BallToBlackBoard, self).update()
        if status != py_trees.common.Status.RUNNING:
            self.blackboard.is_ball_detected = self.blackboard.msg_ball.is_detected
            console.info('BallToBlackBoard : ' + str(self.blackboard.msg_ball.is_detected))
        return status
    
class RobotToBlackBoard(subscribers.ToBlackboard):
    def __init__(self,name: str,topic_name: str,qos_profile: rclpy.qos.QoSProfile):
        super().__init__(name=name,
                         topic_name=topic_name,
                         topic_type=Robot,
                         qos_profile=qos_profile,
                         blackboard_variables={"msg_robot": None },
                         clearing_policy=py_trees.common.ClearingPolicy.NEVER
                        )

        self.blackboard.register_key(key="nearest_robot",access=py_trees.common.Access.WRITE)
        self.blackboard.msg_robot = Robot()
        self.blackboard.msg_robot.id_robot_nearest_ball = 0  #Initial

    
    def update(self):
        status = super(RobotToBlackBoard, self).update()
        # if status != py_trees.common.Status.RUNNING:
        self.blackboard.nearest_robot = self.blackboard.msg_robot.id_robot_nearest_ball
            # console.info('RobotToBlackBoard : ' + str(self.blackboard.nearest_robot))

        return status




        