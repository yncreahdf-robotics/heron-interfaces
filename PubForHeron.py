#!/usr/bin/env python

import rospy
import time

#from std_msgs.msg import String

from geometry_msgs.msg import Twist
from heron.msg import Motion


def Circle(velocity_publisher):
    # Starts a new node
    vel_msg = Twist()

    #Receiveing the user's input

    speed = 0
    distance = 0
    isForward = 0

    #Checking if the movement is forward or backwards
    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 1.2


    for i in range(0,600):
        #Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        #Loop to move the turtle in an specified distance
        #Publish the velocity
        velocity_publisher.publish(vel_msg)
        #Takes actual time to velocity calculus
        t1=rospy.Time.now().to_sec()
        time.sleep(0.01)


#----------------------Zone()-------------------------





def Zone(position_x,position_y,orientation_z,orientation_w,plate_height,zone_publisher):

    msg_Zone=Motion()
    msg_Zone.position_x,msg_Zone.position_y,msg_Zone.orientation_z,msg_Zone.orientation_w,msg_Zone.plate_height=position_x,position_y,orientation_z,orientation_w,plate_height
    print(msg_Zone)
    zone_publisher.publish(msg_Zone)
