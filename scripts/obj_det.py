#!/usr/bin/python3

import torch
import cv2
import os
import numpy
from ament_index_python.packages import get_package_share_directory




pkg_name = get_package_share_directory("obj_detect")

yolo_path = os.path.join(pkg_name,'yolov5')


# print(yolo_path)
# model = torch.hub.load(yolo_path, 'custom', path=yolo_path+"/yolov5s_tosro.pt", source='local') 
# # # Image
# # img = '../data/images/bus.jpg'

# #vid
# vid = cv2.VideoCapture(0)

# while(True) :

# 	ret,frame = vid.read()
# 	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# 	# Inference
# 	results = model(frame)
# 	# Results, change the flowing to: results.show()
# 	results.print()  # or .show(), .save(), .crop(), .pandas(), etc


# print("hello wrold")


import rclpy
from rclpy.node import Node
from humanoid_interfaces.msg import Ball,Robot



class ObjPublisher(Node):

    def __init__(self):
        super().__init__('object_detection')
        self.ball_publisher = self.create_publisher(Ball, 'detection/ball', 10)
        self.robot_publisher = self.create_publisher(Robot, 'detection/robot', 10)
        timer_period = 1/30  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        #define model
        self.pkg_name = get_package_share_directory("obj_detect")
        self.yolo_path = os.path.join(pkg_name,'yolov5')
        self.model = torch.hub.load(self.yolo_path, 'custom', path=self.yolo_path+"/yolov5s_tosro.pt", source='local') 

        #define camera
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    def timer_callback(self):
        msg_ball = Ball()
        msg_robot = Robot()

        ret,frame = self.vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	    # Inference
        results = self.model(frame)
        
        # type_detect = list(results.pandas().xyxy[0]['class_index'])
        # for type in type_detect:
        #     if type == 'ball':
        #         msg.is_detected = True
        #         msg.x_min = list(results.pandas().xyxy[0]['x_min'])
        #         msg.y_min = list(results.pandas().xyxy[0]['y_min'])
        #         msg.x_max = list(results.pandas().xyxy[0]['x_max'])
        #         msg.y_max = list(results.pandas().xyxy[0]['y_max'])
        #         msg.confidence = list(results.pandas().xyxy[0]['confidence'])
        #         msg.class_index = list(results.pandas().xyxy[0]['class_index'])

        # print(results.pandas().xyxy[2,:].cpu().numpy())
        
        dfresult = results.pandas().xyxy[0]
        for i in range(len(dfresult)):
            msg = None
            publisher = None
            classsss = dfresult.loc[i,"class"]
            if classsss == 0 :
                # print("ball")
                msg = msg_ball
            elif classsss == 1 :
                # print('robot') 
                msg = msg_robot

            if msg :
                msg.is_detected = True
                msg.x_min.append(dfresult.loc[i,'xmin'])
                msg.y_min.append(dfresult.loc[i,'ymin'])
                msg.x_max.append(dfresult.loc[i,'xmax'])
                msg.y_max.append(dfresult.loc[i,'ymax'])
                msg.confidence.append(dfresult.loc[i,'confidence'])
                msg.id.append(int(i))

            msg_ball.id = list(range(len(msg_ball.id)))
            msg_robot.id = list(range(len(msg_robot.id)))

        self.ball_publisher.publish(msg_ball)
        self.robot_publisher.publish(msg_robot)
        
        # for obj in results.pandas().xyxyn[0]:
        #     print (obj)

        # cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)

    obj_publisher = ObjPublisher()

    rclpy.spin(obj_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    obj_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
