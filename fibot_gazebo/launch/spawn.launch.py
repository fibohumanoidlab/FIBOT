# Learn from https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/#important-launch-functionalities
# from launch import LaunchDescription

# def  generate_launch_descrioption():
#     return LaunchDescription([
#         # add your action here...
        
#     ])
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')


    return LaunchDescription([
    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        # launch_arguments={'world': world}.items(),
    ),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
    ),

    ExecuteProcess(
        cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
        output='screen'),

    
])