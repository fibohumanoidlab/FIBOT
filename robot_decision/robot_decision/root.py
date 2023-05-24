#!/usr/bin python3
import py_trees
import py_trees_ros.trees
import py_trees.console as console
from py_trees_ros import subscribers
import robot_decision.behavior as behavior
import rclpy
import sys


from robot_decision.to_blackboard import BallToBlackBoard,RobotToBlackBoard


def check_is_ball_detected (blackboard: py_trees.blackboard.Blackboard):
    # Update register key via blackboard
    msg= f' msg : {blackboard.is_ball_detected}'
    return blackboard.is_ball_detected

def create_root():
    '''
    Main Root
    '''
    main_root = py_trees.composites.Parallel(
        name = "Main_Root", 
        policy=py_trees.common.ParallelPolicy.SuccessOnAll(synchronise=False))
    
    topics2bb = py_trees.composites.Sequence(name="Topics2BB", memory=False)


    # Creating branch
    ballToBB = BallToBlackBoard(
        name="Ball2BB",
        topic_name="/ball/detection",
        qos_profile=py_trees_ros.utilities.qos_profile_unlatched(), )
    
    # Creating Sub-branch
    ball_priorities = py_trees.composites.Sequence("Task_Ball",memory=False)
    finding_ball = py_trees.composites.Sequence("Finding Ball",memory=False)

   # Adding Behavior
    ball_check_success = behavior.Finding_Ball(name='Ball Deteteced')

    # Creating branch
    robotToBB =  RobotToBlackBoard(
        name="RobotToBB",
        topic_name="/behavior/nearest_robot",
        qos_profile=py_trees_ros.utilities.qos_profile_unlatched(), )
    
    # Creating Sub-branch
    robot_priorities =  py_trees.composites.Sequence(name="Task_Robot",memory=False)
    robot_nearest = py_trees.composites.Sequence("Finding Nearest Robot",memory=True)
    robot_nearest_check = behavior.Nearest_Robot(name='ID nearest',threshold_distance=10.0)
    
    # Connecting root
    main_root.add_children([topics2bb,ball_priorities,robot_priorities])
    topics2bb.add_children([ballToBB,robotToBB])
    ball_priorities.add_child(finding_ball)
    finding_ball.add_children([ball_check_success])
    robot_priorities.add_child(robot_nearest)
    robot_nearest.add_child(robot_nearest_check)    
    
    return main_root


def main():
    """
    Create pytree ros from create_root() function
    """
    rclpy.init(args=None)
    # root = create_root()
    tree = py_trees_ros.trees.BehaviourTree(
        root=create_root(),
        unicode_tree_debug=True
    )
    try:
        # Set Node name
        tree.setup(node_name="root_node", timeout=15.0)
    except py_trees_ros.exceptions.TimedOutError as e:
        console.logerror(console.red + "failed to setup the tree, aborting [{}]".format(str(e)) + console.reset)
        tree.shutdown()
        rclpy.try_shutdown()
        sys.exit(1)
    except KeyboardInterrupt:
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

if __name__ == '__main__':
   main()

  

    
