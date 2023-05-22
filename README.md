# FIBOT
"""sudo apt install ros-<ros2-distro>-robot-localization"""
  https://navigation.ros.org/setup_guides/odom/setup_odom.html
  
  อย่าลืมเพิ่ม <exec_depend>robot_localization</exec_depend>
  
  sudo apt install ros-foxy-ros2-control ros-foxy-ros2-controllers ros-foxy-gazebo-ros2-control

  <!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.m)

There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template!

Use the `BLANK_README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

  
# System requirements
  
* Ubuntu 20.04 Lts
* ROS2 (Foxy)
  
### Table of Contents

1. [Built With](#Built-With)
2. [Installation](#Installation)



  <a name="Built-With"></a>
  ### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![docs][docs.ros]][https://docs.ros.org/en/foxy/index.html]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
# Document
this document be a part of FRA506 humanoid. In this document including of introduction content conclusion and suggestion

# Installation

This package use extends py_trees package with behaviours, idioms, a tree manager and command line tools that suited for ROS2 ecosystem.
To enable the package, first, we must install following package.
  
## Install opencv
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
# Quickstart
In this package have launch file that launch all node include of Ball_node Root_node and robot_id node
```
ros2 launch robot_decision decision.launch.py
```
  
  
  
  <!-- CONTACT -->
## Contact

Patcharapon Thaweepanyayos - https://www.facebook.com/profile.php?id=100007441359573e - patcharaponthaweepanyayos@gmail.com

Project Link: [https://github.com/fibohumanoidlab/FIBOT_Github/tree/localization](https://github.com/fibohumanoidlab/FIBOT_Github/tree/localization)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
  
  <!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [navigation2](https://navigation.ros.org/getting_started/index.html#getting-started)
* [ros2 control example](https://articulatedrobotics.xyz/mobile-robot-12-ros2-control/)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
