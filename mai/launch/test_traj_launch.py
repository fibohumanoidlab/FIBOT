#!/usr/bin/env python3

# These import statements pull in some Python launch modules.
from launch import LaunchDescription
from launch_ros.actions import Node

# Next, the launch description itself begins:
def generate_launch_description():
    return LaunchDescription([
        # The first two actions in the launch description launch the two turtlesim windows:
        Node(
            package='mai',
            # namespace='turtlesim1',
            executable='pub_test_traj.py',
            # name='sim'
        ),
        Node(
            package='mai',
            # namespace='turtlesim2',
            executable='sub_test_traj.py',
            # name='sim'
        ),
    ])