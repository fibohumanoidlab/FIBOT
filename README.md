<h1 align="center">Localization </h1>

Repository นี้คือ implementation ของระบบ localization สำหรับ Humanoid robot ด้วยข้อมูลจากกล้อง(ใช้ Lidar ไม่ได้) และเซนเซอร์ต่าง ๆ เช่น IMU รวมถึงข้อมูลจาก odom estimation เพื่อให้หุ่นยนต์รับรู้ข้อมูลตำแหน่งและทิศทางของตัวเอง และสามารถวางแผนกลยุทธ์การบุกและการรับของทีมได้

![test](image/localization_sim.png)

โดยแนวคิดการออกแบบ

เริ่มต้นเเปลงภาพที่ได้จากกล้อง web camera ซึ่งภาพที่ได้มาเป็น perspective ให้เป็นภาพ Top view โดยใช้ IPM  

<!-- ROADMAP -->
# Roadmap
- [x] Setup gazebo environment
- [x] Camera to topview 
- [x] topview to laserscan msg in simulation
- [x] camera move in pitch and yaw (simulation) # note not good in simulation!!!
- [x] Localize with AMCL(Nav2) in simulation
  - [x] by only camera to laserscan
  - [ ] by sensor fusion (IMU + odom + camera to laserscan) 
- [ ] topview to laserscan msg in real world (waiting segmentation node from AI team)
- [ ] implement Localization in real world

# Table of Contents

1. [System requirements](#System-requirements)
2. [Built With](#Built-With)
3. [Installation](#Installation)
4. [Contact](#Contact)
5. [Acknowledgments](#Acknowledgments)

<a name="System-requirements"></a>
# System requirements
  
* Ubuntu 20.04 
* ROS2 (Foxy)
  




<a name="Built-With"></a>
# Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![docs][docs.ros]][https://docs.ros.org/en/foxy/index.html]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
# Document
this document be a part of FRA506 humanoid. In this document including of introduction content conclusion and suggestion

<a name="Installation"></a>
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
  
<a name=Contact"></a>
## Contact

Patcharapon Thaweepanyayos - https://www.facebook.com/profile.php?id=100007441359573e - patcharaponthaweepanyayos@gmail.com

Project Link: [https://github.com/fibohumanoidlab/FIBOT_Github/tree/localization](https://github.com/fibohumanoidlab/FIBOT_Github/tree/localization)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
  
  <!-- ACKNOWLEDGMENTS -->
                                       
<a name="Acknowledgments"></a>
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


### Note for Sua
"""sudo apt install ros-<ros2-distro>-robot-localization"""
  https://navigation.ros.org/setup_guides/odom/setup_odom.html
  
  อย่าลืมเพิ่ม <exec_depend>robot_localization</exec_depend>
  
  sudo apt install ros-foxy-ros2-control ros-foxy-ros2-controllers ros-foxy-gazebo-ros2-control
