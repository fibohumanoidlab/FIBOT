import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = get_package_share_directory('localization_pkg')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # Load Map #
    map_dir = LaunchConfiguration(
        'map',
        default=os.path.join(pkg_path, 'map', 'field2.yaml'))
    # Load nav2 robot parameters #
    param_file_name = 'nav2_param.yaml'
    param_dir = LaunchConfiguration(
        'params_file',
        default=os.path.join( pkg_path, 'param', param_file_name))
    # Load nav2 bringup #
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')

    rviz_config_dir = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'rviz',
        'nav2_default_view.rviz')
    
    robot_localization_node = Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_path, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}],
    #    parameters=[os.path.join(pkg_path, 'config/ekf.yaml'), {'use_sim_time': use_sim_time }]
       remappings=[
            ('/imu/data_raw', 'imu_data_raw'),
            # ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),

        DeclareLaunchArgument(
            'map',
            default_value=map_dir,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value=param_dir,
            description='Full path to param file to load'),

        # DeclareLaunchArgument(
        #     'use_sim_time',
        #     default_value='false',
        #     description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': param_dir}.items(),
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
        
        robot_localization_node,
    ])
