#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import py_trees
import py_trees_ros.trees
import py_trees.console as console
# from py_trees_ros import subscribers
import rclpy
import sys
from . import behavior
from . import to_blackboard



def create_root():

    main_root = py_trees.composites.Parallel(
        name = "Main_Root", 
        policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=True)
    )

    topics2bb = py_trees.composites.Sequence(name="Topics2BB",memory=True)
    ball2bb = to_blackboard.BallToBlackBoard(name="Ball2BB", 
                                             topic_name="/ball/detection",
                                             qos_profile=py_trees_ros.utilities.qos_profile_unlatched()
                                             )
    
    task_ball = py_trees.composites.Sequence("Task_Ball")
    is_ball_detected = py_trees.composites.Sequence(name="Is_Ball_Detected", 
                                                    memory=True)
    finding_ball = behavior.find_ball_behavior(name="Finding_Ball")
    is_nearest = behavior.nearest(name='Nearest_Robot')

    # add root 
    main_root.add_children([topics2bb, task_ball])
    topics2bb.add_child(ball2bb)
    task_ball.add_child(is_ball_detected)
    is_ball_detected.add_child(finding_ball)
    is_ball_detected.add_child(is_nearest)
    

    return main_root


def main(): # run root

    rclpy.init(args=None)
    root = create_root()
    tree = py_trees_ros.trees.BehaviourTree(
        root=root,
        unicode_tree_debug=True
    )
    try:
        tree.setup(node_name="root_node", timeout=15.0)
    except py_trees_ros.exceptions.TimedOutError as e:
        console.logerror(console.red + "failed to setup the tree, aborting [{}]".format(str(e)) + console.reset)
        tree.shutdown()
        rclpy.try_shutdown()
        sys.exit(1)
    except KeyboardInterrupt:
        # not a warning, nor error, usually a user-initiated shutdown
        console.logerror("tree setup interrupted")
        tree.shutdown()
        rclpy.try_shutdown()
        sys.exit(1)

    tree.tick_tock(period_ms=1000.0)

    try:
        rclpy.spin(tree.node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        tree.shutdown()
        rclpy.try_shutdown()

# if __name__ == '__main__':
#     main()