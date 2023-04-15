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

    ### world ###
    package_dir=get_package_share_directory('fibot_gazebo')

    world_file = os.path.join(package_dir,'worlds','soccer_field.world')
    ###

    ### URDF ###
    # urdf_file_name = 'fibot_robot_demo.urdf'
    urdf_file_name = 'fibot_robot_demo_joint_test.urdf'
    urdf = os.path.join(
        get_package_share_directory('fibot_description'),
        'urdf',
        urdf_file_name)
    ###

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_broad"],
    )

    forward_command_controller = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["forward_command_controller"],
    )

    joint_state_controller = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_state_controller"],
    )

    joint_trajectory_controller = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_trajectory_controller"],
    )
    

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    rviz_file_path = os.path.join(package_dir,'rviz','rviz_config.rviz')


    return LaunchDescription([

    # DeclareLaunchArgument(
    #         'use_sim_time',
    #         default_value='true',
    #         description='Use simulation (Gazebo) clock if true'),

    ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
            output='screen'),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_file}.items(),
    ),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
    ),

    Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[urdf]),
    
    Node(
        package='fibot_gazebo',
        executable='publisher_trajectory.py',
        name='publisher_trajectory',
        parameters=[{'use_sim_time': True}],
        ),

    # Node(
    #     package='localization_pkg',
    #     executable='ball_localization.py',
    #     name='ball_localization',
    #     parameters=[{'use_sim_time': True}],
    #     ),
        
    
    # Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     ),

    # Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     # parameters=[{'use_sim_time': use_sim_time}],
    #     arguments=[urdf]
    #     ),
    
    joint_broad_spawner,
    # forward_command_controller,
    # joint_state_controller,
    joint_trajectory_controller,

    Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner',
        output='screen',
        arguments=["-topic", "/robot_description", "-entity", "FIBOT","-x=-1.0", "-y=-3.5", "-Y=1.57"]
        ), 

    Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', rviz_file_path],
        output='screen'),

])
