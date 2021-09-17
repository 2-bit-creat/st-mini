#! /usr/bin/env python
import cv2
import serial
import time
import numpy as np
import ctypes
import rospy
from std_msgs.msg import Int32, Int16
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist #Twist is class

class CAN_com:
    print("hello")
    speed = rospy.get_param('~turtle_speed_x', 0.0) #private
    angular_speed = rospy.get_param('~turtle_ang_vel', 0.0) #private

    def __init__(self):
        rospy.init_node("main_node")
        
        self.CAN_pub = rospy.Publisher(
            "/cmd_vel",
            Twist,
            queue_size= 5
        )

        self.steering = 0
        self.flag_sub = rospy.Subscriber(
            "/flag",
            Int32,
            self.ch_flag
        )

        self.flag = 0
        self.steering_sub = rospy.Subscriber(
            "/steering",
            Float32,
            self.ch_steering
        )

        self.flag_aruco = 0
        self.steering_sub = rospy.Subscriber(
            "/aruco_flag",
            Int16,
            self.ch_flag_aruco
        )
   
    def ch_flag(self, _data):
        self.flag = _data.data

    def ch_steering(self, _data):
        self.steering = _data.data

    def ch_flag_aruco(self, _data):
        self.flag_aruco = _data.data

    def Twist_msg(self, steering):
        if steering > 0.95 or steering <-0.95:
            self.msg = Twist()
            self.msg.linear.x = 0.16
            self.msg.linear.y = 0.0
            self.msg.linear.z = 0.0
            self.msg.angular.x = 0.0
            self.msg.angular.y = 0.0
            self.msg.angular.z = steering*0.6
        else:
            self.msg = Twist()
            self.msg.linear.x = 0.22
            self.msg.linear.y = 0.0
            self.msg.linear.z = 0.0
            self.msg.angular.x = 0.0
            self.msg.angular.y = 0.0
            self.msg.angular.z = steering

    def run(self): 
        rate = rospy.Rate(40)
        #the while loop here can replace rospy.spin
        while not rospy.is_shutdown():
            if self.flag_aruco == 0:
                if self.flag == 0:
                    self.Twist_msg(self.steering )
                    self.CAN_pub.publish(self.msg)

                else:
                    self.msg.linear.x = 0.0
                    self.msg.linear.y = 0.0
                    self.msg.linear.z = 0.0
                    self.msg.angular.x = 0.0
                    self.msg.angular.y = 0.0
                    self.msg.angular.z = 0.0
                    self.CAN_pub.publish(self.msg) #emergency brake for 2 seconds
                    time.sleep(2)
                
            else:
                    self.msg.linear.x = 0.0
                    self.msg.linear.y = 0.0
                    self.msg.linear.z = 0.0
                    self.msg.angular.x = 0.0
                    self.msg.angular.y = 0.0
                    self.msg.angular.z = 0.0
                    time.sleep(0.5)
                    self.msg.angular.z = 1.0
                    time1 = time.time()
                    while True:      
                        time2 = time.time()           
                        if time2 > (time1 + 4): #turn for 4 seconds
                            break
                        self.CAN_pub.publish(self.msg) 
                        rate.sleep()
            rate.sleep()

if __name__ == "__main__":
    a = CAN_com()
    a.run()