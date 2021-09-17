#! /usr/bin/env python
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
from std_msgs.msg import Float32
import rospy
import cv2
import serial
import time
import numpy as np
import ctypes


class rplidar_sub:
    initial_time=time.time()
    flag = 0
    
    def __init__(self):
        rospy.init_node("flag_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.callback3)
        self.pub = rospy.Publisher('/flag', Int32, queue_size= 5)
        rospy.spin() #if there is no rospy.spin the process will end right away. But in case there are other loops that enables the process keep going, you don't have to use rospy.spin

    def callback1(self, rp_data):
        for i in range(0, 29, 1):
            if (rp_data.ranges[29-i] < 0.7 and rp_data.ranges[29-i] != 0)  or (rp_data.ranges[330+i] < 0.7 and rp_data.ranges[330+i]  != 0): #publish 1 when the LiDAR detects something within 0.7m in the range of [0, 30] or [330, 360] degrees.
                self.pub.publish(1)
                return 
        self.pub.publish(0)
    
    def callback2(self, rp_data):
        print(360/(rp_data.angle_increment*180/3.141592))
        return 
    def callback3(self, rp_data):
        for i in range(300, 450, 2):
            if (rp_data.ranges[i] < 0.7 and rp_data.ranges[i] != 0):  #publish 1 when the LiDAR detects something within 0.7m in the range of [0, 30] or [330, 360] degrees.
                self.pub.publish(1)
                return 
        self.pub.publish(0)
        

if __name__ == "__main__":
    a = rplidar_sub()