from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node


def generate_launch_description():

    # node_ball = Node(package='robot_decision',executable='ball_node')
    # node_nearest_robot = Node(package='robot_decision',executable='nearest_robot_node')
    # node_root = Node(package='robot_decision',executable='root')
 


    return LaunchDescription([   
        Node(package='robot_decision',executable='ball_node'),
        Node(package='robot_decision',executable='nearest_robot_node'),
        Node(package='robot_decision',executable='root',name='root',output='screen'),
    ])