import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_path = os.path.join(get_package_share_directory('fibot_description'))
    default_rviz_config_path = os.path.join(get_package_share_directory('fibot_description'),'urdf.rviz') 
    xacro_file = os.path.join(package_path,'fibot_xacro.urdf.xacro')
    # xacro_file = os.path.join(package_path,'fibot001.urdf.xacro')

    
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml()}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    joint_state_publisher_node = Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
            )
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )
    

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     condition=IfCondition(LaunchConfiguration('gui'))
    # )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', default_rviz_config_path],
    )

    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',),
            # description='Use simulation (Gazebo) clock if true'),
        node_robot_state_publisher,
        rviz_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,

    ])