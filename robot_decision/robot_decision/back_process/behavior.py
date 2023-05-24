#!/usr/bin python3

import py_trees
import py_trees_ros

from humanoid_interfaces.msg import Ball,Robot
import std_msgs.msg as std_msgs
import py_trees.console as console



class Ball_Check_Success(py_trees.behaviour.Behaviour):

    def __init__(
            self,
            name: str,
            topic_name: str="/behavior/ball_check_success",

    ):
        super(Ball_Check_Success, self).__init__(name=name)
        self.ball_behavior = Ball()
        self.topic_name = topic_name


    def setup(self, **kwargs):

        self.logger.debug("{}.setup()".format(self.qualified_name))
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability

        self.publisher = self.node.create_publisher(
            msg_type=std_msgs.String,
            topic=self.topic_name,
            qos_profile=py_trees_ros.utilities.qos_profile_latched()
        )
        # self.feedback_message = "publisher created"

    def update(self) -> py_trees.common.Status:

        self.logger.debug("%s.update()" % self.__class__.__name__)
        self.publisher.publish(std_msgs.String(data=str(self.ball_behavior.is_detected)))
        # self.feedback_message = "flashing {0}".format(self.colour)
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status: py_trees.common.Status):

        self.logger.debug(
            "{}.terminate({})".format(
                self.qualified_name,
                "{}->{}".format(self.status, new_status) if self.status != new_status else "{}".format(new_status)
            )
        )
        self.publisher.publish(std_msgs.String(data=""))
        self.feedback_message = "cleared"


class Finding_Ball(py_trees.behaviour.Behaviour):
    def __init__(self,name: str,topic_name: str="/behavior/finding_ball",):
        super(Finding_Ball, self).__init__(name=name)
        self.ball_behavior = Ball()
        self.topic_name = topic_name
        self.subscribe_topic = 'ball/detection'
        
    def callback_msg(self,msg):
        self.msg_callback = msg.is_detected
        return  self.msg_callback

    def setup(self, **kwargs):

        self.logger.debug("{}.setup()".format(self.qualified_name))
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability

        self.publisher = self.node.create_publisher(
            msg_type=std_msgs.String,
            topic=self.topic_name,
            qos_profile=py_trees_ros.utilities.qos_profile_latched()
        )
        self.subscriber = self.node.create_subscription(msg_type=Ball,topic=self.subscribe_topic ,callback =self.callback_msg,qos_profile=1)

    
    def update(self) -> py_trees.common.Status:
        self.logger.debug("%s.update()" % self.__class__.__name__)
        
        try:
            ball_detected = self.msg_callback
        except:
            ball_detected = False
        if not ball_detected:
            return py_trees.common.Status.RUNNING
        else:
            return py_trees.common.Status.SUCCESS

    def terminate(self, new_status: py_trees.common.Status):

        self.logger.debug(
            "{}.terminate({})".format(
                self.qualified_name,
                "{}->{}".format(self.status, new_status) if self.status != new_status else "{}".format(new_status)
            )
        )
        self.publisher.publish(std_msgs.String(data=""))
        self.feedback_message = "cleared"


class Nearest_Robot(py_trees.behaviour.Behaviour):
    def __init__(
            self,
            name: str,
            threshold_distance : float,
            topic_name: str="/behavior/nearest_robot",):
        super(Nearest_Robot, self).__init__(name=name)
        self.robot = Robot()
        self.topic_name = topic_name
        self.threshold_distance = threshold_distance
        self.subscribe_topic ='robot/nearest_id'
        
    def callback_msg(self,msg):
        self.msg_callback = msg
        return  self.msg_callback


    def setup(self, **kwargs):
        self.logger.debug("{}.setup()".format(self.qualified_name))
        try:
            self.node = kwargs['node']
        except KeyError as e:
            error_message = "didn't find 'node' in setup's kwargs [{}][{}]".format(self.qualified_name)
            raise KeyError(error_message) from e  # 'direct cause' traceability
        self.publisher = self.node.create_publisher(
            msg_type=Robot,
            topic=self.topic_name,
            qos_profile=py_trees_ros.utilities.qos_profile_latched()
        )
        self.subscriber = self.node.create_subscription(msg_type=Robot,topic=self.subscribe_topic ,callback =self.callback_msg,qos_profile=1)
        
        
    def update(self) -> py_trees.common.Status:
        self.logger.debug("%s.update()" % self.__class__.__name__)
        print('-------------------------------------------------------------')
        try:
            if self.msg_callback!=0:
                msg = Robot()
                console.info(f'The Robot Id which nearest to the ball is : { self.msg_callback.id_robot_nearest_ball} ')
                self.publish_bhv = msg
                self.publish_bhv.id_robot_nearest_ball = self.msg_callback.id_robot_nearest_ball
                self.publish_bhv.distance_robot_ball = self.msg_callback.distance_robot_ball
                self.publisher.publish(self.publish_bhv)
                if self.msg_callback.distance_robot_ball <= self.threshold_distance:
                    console.info('KICK')
                else:
                    console.info('WALK')
                return py_trees.common.Status.SUCCESS
            else:
                return py_trees.common.Status.RUNNING
        except:
                return py_trees.common.Status.RUNNING

    def terminate(self, new_status: py_trees.common.Status):
        self.logger.debug( "{}.terminate({})".format(self.qualified_name, "{}->{}".format(self.status, new_status) if self.status != new_status else "{}".format(new_status)) )
        self.feedback_message = "cleared"
    
