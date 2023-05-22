# FIBOT
"""sudo apt install ros-<ros2-distro>-robot-localization"""
  https://navigation.ros.org/setup_guides/odom/setup_odom.html
  
  อย่าลืมเพิ่ม <exec_depend>robot_localization</exec_depend>
  
  sudo apt install ros-foxy-ros2-control ros-foxy-ros2-controllers ros-foxy-gazebo-ros2-control

# About this package

* **Author** : Patcharapon Thaweepanyayos && 
* **Package** : robot_decision
* **detail** : Ubuntu 20.04 Lts, ROS2 (Foxy)
* **Provider** : FIBO Humanoid Lab, KMUTT, Thailand
* **Contact** : 
  
# Document
this document be a part of FRA506 humanoid. In this document including of introduction content conclusion and suggestion

# Installation

This package use extends py_trees package with behaviours, idioms, a tree manager and command line tools that suited for ROS2 ecosystem.
To enable the package, first, we must install following package.
  
## Install pip install opencv-python
```
pip3 install opencv-python
```
## Install navigation2
```
sudo apt install ros-foxy-navigation2
```
## install ros2-control
```
sudo apt install ros-foxy-ros2-control ros-foxy-ros2-controllers ros-foxy-gazebo-ros2-control
```
