from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import os

def generate_launch_description():
    default_model_path = os.path.join(get_package_share_path('fibot_description'),'fibot001.urdf')
    default_rviz_config_path = os.path.join(get_package_share_path('fibot_description'),'urdf.rviz') 

    gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')

    # robot_description = ParameterValue(Command(['urdf', LaunchConfiguration('model')]),
    #                                    value_type=str)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # with open(default_model_path, 'r') as infp:
    #     robot_desc = infp.read()

    robot_state_publisher_node = Node(
        name='fibot_robot',
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[default_model_path],
        
    )

    # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    joint_state_publisher_node = Node(
        name='fibot_joint',
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui')),
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[default_model_path]
    )


    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return LaunchDescription([
        gui_arg,
        model_arg,
        rviz_arg,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])

# from ament_index_python.packages import get_package_share_path

# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.conditions import IfCondition, UnlessCondition
# from launch.substitutions import Command, LaunchConfiguration

# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue

# def generate_launch_description():
#     urdf_tutorial_path = get_package_share_path('fibot_description')
#     default_model_path = urdf_tutorial_path / 'urdf/fibot001.urdf.xacro'
#     default_rviz_config_path = urdf_tutorial_path / 'rviz/urdf.rviz'

#     gui_arg = DeclareLaunchArgument(name='gui', default_value='true', choices=['true', 'false'],
#                                     description='Flag to enable joint_state_publisher_gui')
#     model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
#                                       description='Absolute path to robot urdf file')
#     rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
#                                      description='Absolute path to rviz config file')

#     robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
#                                        value_type=str)

#     robot_state_publisher_node = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         parameters=[{'robot_description': robot_description}]
#     )

#     # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
#     joint_state_publisher_node = Node(
#         package='joint_state_publisher',
#         executable='joint_state_publisher',
#         condition=UnlessCondition(LaunchConfiguration('gui'))
#     )

#     joint_state_publisher_gui_node = Node(
#         package='joint_state_publisher_gui',
#         executable='joint_state_publisher_gui',
#         condition=IfCondition(LaunchConfiguration('gui'))
#     )

#     rviz_node = Node(
#         package='rviz2',
#         executable='rviz2',
#         name='rviz2',
#         output='screen',
#         arguments=['-d', LaunchConfiguration('rvizconfig')],
#     )

#     return LaunchDescription([
#         gui_arg,
#         model_arg,
#         rviz_arg,
#         # joint_state_publisher_node,
#         joint_state_publisher_gui_node,
#         robot_state_publisher_node,
#         rviz_node
#     ])