from setuptools import setup
import os
from glob import glob
package_name = 'robot_decision'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name),glob('launch/*launch.py')),
 
        # (os.path.join('share', package_name,'back_process'), glob('launch/*launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ty-humble',
    maintainer_email='teeteethewacko@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ball_node = robot_decision.node_ball:main',
            'nearest_robot_node = robot_decision.node_robot_nearest:main',
            'root = robot_decision.root:main',
        ],
    },
)
