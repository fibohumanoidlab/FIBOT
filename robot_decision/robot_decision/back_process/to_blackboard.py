#!/usr/bin/env python3

import py_trees
import rclpy.qos
from std_msgs.msg import Bool

from py_trees_ros import subscribers
from py_trees_ros_interfaces.msg import Ball

class BallToBlackBoard(subscribers.ToBlackboard):

    def __init__(self, name: str, topic_name: str, 
                 qos_profile: rclpy.qos.QoSPresetProfiles):
        super().__init__(name=name,
                         topic_name=topic_name,
                         topic_type=Ball,
                         qos_profile=qos_profile,
                         blackboard_variables={"msg_ball": None},
                         clearing_policy=py_trees.common.ClearingPolicy.NEVER
                         )
        self.blackboard.register_key(key="is_ball_detected", 
                                     access=py_trees.common.Access.WRITE
                                     )
        self.blackboard.msg_ball = Ball()
        self.blackboard.msg_ball.is_detected = False

    def update(self):
        
        status = super(BallToBlackBoard, self).update()
        
        if status != py_trees.common.Status.RUNNING:
            
            # self.blackboard.is_ball_detected = False
            self.blackboard.is_ball_detected = self.blackboard.msg_ball.is_detected 
        return status