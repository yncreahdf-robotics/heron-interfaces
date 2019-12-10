#!/usr/bin/env python

import rospy
import time
from geometry_msgs.msg import Twist

HERON_ID='HeronFirst'

def Circle():
    # Starts a new node
    rospy.init_node('centralheron', anonymous=True)
    velocity_publisher = rospy.Publisher('/'+HERON_ID+'/cmd_vel', Twist, queue_size=10)
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
        #Calculates distancePoseStamped
        #current_distance= speed*(t1-t0)
        #After the loop, stops the robot
        #vel_msg.linear.x = 0
        #Force the robot to stop
        #velocity_publisher.publish(vel_msg)
        time.sleep(0.01)

#circle()
