# Detection

yolov5s + custom train dataset for detection and publish as ros2 publisher node
* ball (ball publisher)
* robot (robot publisher)
* goal post

**[Detection model]** yolov5s : https://github.com/ultralytics/yolov5

**[Dataset]** torso21: https://github.com/bit-bots/TORSO_21_dataset

## working steps
* **[training phase]** training yolov5s on custom dataset (on ubuntu pc with gpus)
  * clone yolov5 github
    * install all requirement pakage
    * install nvidia driver and cuda
  * colne torso21 github
    *  download dataset as show in torso21 github
  * data prepairation
    *  dataset labeled in .yaml file
    *  convert .yaml format to yolov5 format(.txt)
  * training yolov5s on ubuntu pc
    * wait for training to finish
    * [result weight] : "yolov5s_torso.pt" 
* **[testing phase]** test model on nvidia jetson xavier
  * create custom python script to run custom model
  * test custom model on jetson
* **[ros2 phase]** detection publisher node form nvidia jetson xavier
  * create publisher node
    * run detection model
    * publish custom ball message
    * publish custom robot message  
  

# System requirement
* **[SBC]** nvidia bjetson xavier
  * ubuntu 20.04
  * ROS2 (Foxy)
  * all requirement package for yolov5 are pre-install on jetson xavier
* **[Webcam]** logitech c920

# Quickstart
```
ros2 run obj_detect obj_det.py
```

# custom yolov5s result
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/jeM1RRcv-zo/0.jpg)](https://www.youtube.com/watch?v=jeM1RRcv-zo)

# Suggestion
* change from yolov5 to yolov8
* stream webcam via rtsp so camera can be call by multiple python script
* **[Custom train yolov5s]** : https://github.com/nosegit/yolov5s-torso21.git
