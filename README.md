# About this package

* **Author** : Russapat Leelawattanakiet && Nattasit Phaisalrittiwong 
* **Package** : robot_decision
* **detail** : Ubuntu 20.04 Lts, ROS2 (Foxy)
* **Provider** : FIBO Humanoid Lab, KMUTT, Thailand
* **Contact** : russapat@gmail.com

# Introduction
The decision of the player is an important part of the match that can lead to victory. A good decision can measure the intelligence of the robot. In 2022, our team uses a state machine to create an algorithm. However, a state machine has some disadvantages compared to a behavior tree. For example, the behavior tree can be coded in a node and connected with other nodes like a tree. it’s able to overwrite the behavior node or recreate the tree with the same behavior node. Moreover, our system is developed using ROS2 which has a behavior tree extension.

# Installation
This package use extends the py_trees package with behaviors, idioms, a tree manager, and command line tools that are suited for the ROS2 ecosystem.
To enable the package, first, we must install the following package.

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
Now, we can learn py_tree tutorials from this website [py_tree_tutorial](https://py-trees-ros-tutorials.readthedocs.io/en/release-2.1.x/index.html).

## Optional
if you want some visualization, you can install the py_trees_ros_viewer package
```
git clone https://github.com/splintered-reality/py_trees_ros_viewer.git
```
For more information about installing, can check on this git [ splintered-reality /py_trees_ros ](https://github.com/splintered-reality/py_trees_ros).

# Quickstart
This package have a launch file that launches all node include of Ball_node Root_node and robot_id node
```
ros2 launch robot_decision node.launch.py
```
The ball node is a node that provides a topic when the robot detects the ball.
The root node is a node that creates the behavior tree as it was designed.
robot_id_node is a node that provide a topic robot id to simulate which robot is stay nearest to the ball.
Use this command line to visualize the result and the behavior.
```
py-trees-tree-viewer
```

