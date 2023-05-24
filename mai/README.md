# About this package
* **Author** : Natanan Tirasukvongsa (Mai)
* **Package** : mai
* **Detail** : Ubuntu 20.04 Lts, ROS2 (Foxy)
* **Joined** : FIBOT Team, Thavida Lab (Humanoid Soccer RoboCup), FIBO, KMUTT, Thailand
* **Contact** : tnatanan@gmail.com

# Document
* **Independent Study Document** : [รายงานความคืบหน้า_ณัฐนันท์.pdf](https://github.com/Natanan-Tirasukvongsa/mai/files/11497313/_.pdf)
* **Inverse Kinematics** : 
  - **Neck and Arms** : [Neck_Arm_inv.pdf](https://github.com/Natanan-Tirasukvongsa/mai/files/11523844/Neck_Arm_inv.pdf)
  - **Legs (Ref.5)** : [Leg_inv.pdf](https://github.com/Natanan-Tirasukvongsa/mai/files/11523846/Leg_inv.pdf)
* **Trajectory (Ref.2)** : [Dynamic_control_algorithm_for_a_biped_robot.pdf](https://github.com/Natanan-Tirasukvongsa/mai/files/11523865/Dynamic_control_algorithm_for_a_biped_robot.1.pdf)


# Installation
1. Install ROS2 Foxy by following this [tutorial](https://docs.ros.org/en/foxy/Installation.html)
2. Open terminal (Ctrl+Alt+t)
3. Install Colcon and create workspace by following this [tutorial](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html)
```
sudo apt install python3-colcon-common-extensions
mkdir -p ~/ros2_ws/src
```
4. Clone mai package
```
cd ~/ros2_ws/src
git clone https://github.com/Natanan-Tirasukvongsa/mai.git 
```
5. Build the workspace with colcon
```
cd ..
colcon build --packages-select mai
```
6. Source the setup file
```
source install/local_setup.bash
```

# Launch File
## Launch URDF file
1. Open New terminal
2. Launch command line 
```
ros2 launch mai display.launch.py
```

| ![Screenshot from 2023-05-17 18-29-40](https://github.com/Natanan-Tirasukvongsa/mai/assets/78638430/951df0da-461f-4135-9c1b-5da69374ba81) | 
|  :---: | 
| URDF - Cylinder  | 

## Launch trajectory and display axis 
1. Open New terminal
2. Launch command line  
```
ros2 launch mai test_display.launch.py 
```
|![Screenshot from 2023-05-17 18-32-49](https://github.com/Natanan-Tirasukvongsa/mai/assets/78638430/d3b1557d-4e8d-4ce4-9a72-e6d7f9f3925c) | 
|  :---: | 
| Axis moves by following trajectory  | 

## Launch only trajectory
1. Open New terminal
2. Launch command line  
```
ros2 launch mai test_traj_launch.py 
```
3. Open another terminal
```
rqt
```
|![Screenshot from 2023-05-17 18-43-00](https://github.com/Natanan-Tirasukvongsa/mai/assets/78638430/f7f921f2-68af-4d4e-9d64-cd9b22261ecc)| 
|  :---: | 
| rqt default window  | 

4. Plugins -> Introspection -> Node Graph

|![Screenshot from 2023-05-17 18-39-39](https://github.com/Natanan-Tirasukvongsa/mai/assets/78638430/ac6c72d1-4a30-4bb6-840f-8d2801c0782d)| 
|  :---: | 
| rqt graph : Trajectory publish and subscribe node| 

5. Plugins -> Visualization -> Plot

|![Screenshot from 2023-05-17 18-52-13](https://github.com/Natanan-Tirasukvongsa/mai/assets/78638430/a375923f-0579-4c17-a558-b9efd885bfb3)| 
|  :---: | 
| rqt plot| 

6. Add Topic : /traj_test/data

|![Screenshot from 2023-05-17 18-54-48](https://github.com/Natanan-Tirasukvongsa/mai/assets/78638430/2d841e79-61cf-4a51-992c-3ce8eb089eb8)| 
|  :---: | 
| position trajectory| 

# Service File
## Server and Client Trajectory
1. copy config_inv.yaml path (${\color{lightblue}Name}$ is your computer name)

```
/home/Name/ros2_ws/src/mai/config/config_inv.yaml
```

2. Change yaml file directory in humanoid_inv.py (line 6)  
- humanoid_inv.py is in /home/**Name**/ros2_ws/src/mai/mai/humanoid_inv.py 
- Open this file 
```
cd ~/ros2_ws/src/mai/mai
gedit humanoid_inv.py
```
- Edit line 6 (paste new directory)
```
with open('/home/Name/ros2_ws/src/mai/config/config_inv.yaml', 'r') as file:
```
- Save file (Ctrl+s) 

3. Build the workspace with colcon
```
cd ~/ros2_ws
colcon build --packages-select mai
```
4. Source the setup file
```
source install/local_setup.bash
```
5. Run service node
```
ros2 run mai ser_fw_xyz_parent.py 
```
6. Open another terminal and run client node
```
ros2 run mai cli_inv_th.py 
```
# All Files
| File Name | Folder | Description |
|  --- | --- | --- | 
| config_inv.yaml  | config | Link Lenght Constant | 
| test_display.rviz | config | rviz config |
| display.launch.py | launch | show cylinder model |
| test_display.launch.py | launch | show axis moving by trajectory |
| test_traj_launch.py | launch | publish and subscribe trajectory |
| cli_inv_th.py | mai | cilent node |
| humanoid_foot_traj_inherit_ser.py | mai | publish joint node |
| humanoid_inv.py | mai | inverse kinemaics of legs, head, arms |
| pub_test_traj.py | mai | publish trajectory node |
| ser_fw_xyz_parent.py | mai | service node |
| sub_test_traj.py | mai | subscribe node |
| test_state_subscriber.py | mai | state publisher node |
| SendINV.srv| srv | structure your requests and responses |
| pr2.urdf.xacro| urdf | cylinder model |
| test_display.urdf.xml | urdf | base_link to camera_link |

# References
1. Ali, M.A., Park, H.A. and Lee, C.G., 2010, October. Closed-form inverse kinematic joint solution for humanoid robots. In 2010 IEEE/RSJ International Conference on Intelligent Robots and Systems (pp. 704-709). IEEE.
2. Cuevas, E.V., Zaldívar, D. and Rojas, R., 2005, May. Dynamic control algorithm for a biped robot. In 7th International Conference on Control and Applications, Cancún, Mexico.
3. Hashimoto, K., Hattori, K., Otani, T., Lim, H.O. and Takanishi, A., 2014. Foot placement modification for a biped humanoid robot with narrow feet. The Scientific World Journal, 2014.
4. Hong, Y.D., 2019. Capture point-based controller using real-time zero moment point manipulation for stable bipedal walking in human environment. Sensors, 19(15), p.3407.
5. Park, H.A., Ali, M.A. and Lee, C.G., 2012. Closed-form inverse kinematic position solution for humanoid robots. International Journal of Humanoid Robotics, 9(03), p.1250022.
6. Rouxel, Q., Passault, G., Hofer, L., N’Guyen, S. and Ly, O., 2015. Rhoban hardware and software open source contributions for robocup humanoids. In Proceedings of 10th Workshop on Humanoid Soccer Robots, IEEE-RAS Int. Conference on Humanoid Robots, Seoul, Korea.
7. Sugihara, T. and Yamamoto, T., 2017, September. Foot-guided agile control of a biped robot through ZMP manipulation. In 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) (pp. 4546-4551). IEEE.
