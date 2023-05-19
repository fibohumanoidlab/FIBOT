# About this package

* **Author** : Russapat Leelawattanakiet && Nattasit Phaisalrittiwong 
* **Package** : robot_decision
* **detail** : Ubuntu 20.04 Lts, ROS2 (Foxy)
* **Provider** : FIBO Humanoid Lab, KMUTT, Thailand
* **Contact** : russapat@gmail.com

# Document
this document be a part of FRA506 humanoid. In this document including of introduction content conclusion and suggestion

# Installation

This package use extends py_trees package with behaviours, idioms, a tree manager and command line tools that suited for ROS2 ecosystem.
To enable the package, first, we must install following package.
## Install py_trees_ros package
```
git clone https://github.com/splintered-reality/py_trees_ros.git
```
## Install py_tree_ros_tutorials
```
git clone https://github.com/splintered-reality/py_trees_ros_tutorials.git
```
## install py_tree_interface
```
git clone https://github.com/splintered-reality/py_trees_ros_interfaces.git
```
Now, we can learn py_tree tutorials from this web site [py_tree_tutorial](https://py-trees-ros-tutorials.readthedocs.io/en/release-2.1.x/index.html).

## Optional
if you want some visaulize, you can install py_trees_ros_viewer package
```
git clone https://github.com/splintered-reality/py_trees_ros_viewer.git
```
For more infomation about installing, can check on this git [ splintered-reality /py_trees_ros ](https://github.com/splintered-reality/py_trees_ros).

# Quickstart
In this package have launch file that launch all node include of Ball_node Root_node and robot_id node
```
ros2 launch robot_decision decision.launch.py
```
Ball node is a node that provide topic when robot detect the ball.
Root node is a node that create the behavior tree as it was designed.
robot_id_node is a node that provide topic robot id to simulate which robot is stay nearest the ball.
Use this command line to visualize the result and the behavior.
```
py-trees-tree-viewer
```

