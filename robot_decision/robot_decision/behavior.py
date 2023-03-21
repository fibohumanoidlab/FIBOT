import py_trees
import py_trees_ros
import rcl_interfaces.msg as rcl_msgs
import rcl_interfaces.srv as rcl_srvs
from py_trees_ros_interfaces.msg import Ball
import std_msgs.msg as std_msgs


class find_ball_behavior(py_trees.behaviour.Behaviour):

    def __init__(self, name: str, topic_name: str="/find_ball/behavior"):
        super(find_ball_behavior, self).__init__(name=name)
        self.topic_name= topic_name
        self.msg = Ball()
        
        # self.status = py_trees.common.Status.RUNNING

    def subscriber_callback(self,msg):
        self.msg = msg
        print(self.msg)
        self.msg2 = msg.is_detected
        print(self.msg2)
        # print('callback')

    def setup(self, **kwargs):

        self.logger.debug('find ball behavior setup')
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
        self.subscriber = self.node.create_subscription(
            msg_type=Ball, topic='/ball/detection', 
            callback = self.subscriber_callback, 
            qos_profile=10
        )

    def update(self):

        self.publisher.publish(std_msgs.String(data="Find Ball"))

        try:
            if self.msg.is_detected == True:
                self.status = py_trees.common.Status.SUCCESS

            else :
                self.status = py_trees.common.Status.RUNNING

            return self.status
        except KeyError as e:
            print('No Topic Receive')
        
        
    def terminate(self, new_status):

        new_status = self.status
        return new_status 
    
