
# About this meta package
* **Author** : Tanach Chinbutarnont (Mark)
* **Package** : mark
* **Detail** : Ubuntu 20.04 Lts, ROS2 (Foxy) , Ubuntu 22.04 Lts, ROS2 (Humble)
* **Joined** : FIBOT Team, Thavida Lab (Humanoid Soccer RoboCup), FIBO, KMUTT, Thailand
* **Contact** : tanach.fibo@mail.kmutt.ac.th

# Branch is contain
1. c2cpp script for compair tranfer .c to .cpp Because of fixing the IOC to change the peripheral configuration. It migrates the user code from.c to create a new.c, but most libraries, including Xicro, are written in C++. Also moved, so after generating from ioc, run this script to make this vulnerability disappear.
2. Imu library base on hardware
3. Dynamixel_protocol_2.0_pipeline_library



# C2CPP 
1. create folder for script and log file
```
cd {your_path}
mkdir -p c2cpp/.log
cd {your_path}/c2cpp
```
2. drop script here
3. config path in script

<img
  src="pic/Screenshot from 2023-05-29 14-45-24.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">

4. run script in folder c2cpp
```
python3 cpp_c_to_cpp.py -project_name {project_name} -remove 1
```
The scripts are regenerated again and the pre-generated files are stored in the .log folder.







# Imu library
use on I2C interrupt mode
1. install library as static library c++
2. include 
<img
  src="pic/Screenshot from 2023-05-29 15-46-22.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">
3.imu begin

<img
  src="pic/Screenshot from 2023-05-29 15-46-56.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">

4. setup I2C IT call back
<img
  src="pic/Screenshot from 2023-05-29 15-47-39.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">


5. get value

<img
  src="pic/Screenshot from 2023-05-29 15-47-25.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">



# Dynamixel_protocol_2.0_pipeline
1. include 

<img
  src="pic/Screenshot from 2023-05-29 16-07-37.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">

2. dynamixel begin 

<img
  src="pic/Screenshot from 2023-05-29 16-08-32.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">

3. Spin_computation_pipeline

<img
  src="pic/Screenshot from 2023-05-29 16-08-59.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 800px">

The library handles the order of receiving and sending data according to the Dynamixel protocol 2.0 RS485 format and receives feedback automatically. which can be executed according to the.h of the library.