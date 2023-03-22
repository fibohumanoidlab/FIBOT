from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
        package= 'robot_decision',
        executable= 'root',
        name= 'root'
        ),
        Node(
        package= 'robot_decision',
        executable= 'ball',
        ),
    ])