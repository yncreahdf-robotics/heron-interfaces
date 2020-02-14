#!/usr/bin/env python

import roslaunch
import rospy
import curses
import subprocess
import os
import time

menu = ['Controle par manette', 'Navigation', 'Mapping', 'Prise de positions', 'Exit']





def print_center(stdscr, text):
    stdscr.clear()
    stdscr.nodelay(0)
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def start_launch(launch_name, stdscr):
    roscore = subprocess.Popen('roscore')
    time.sleep(1)
    stdscr.nodelay(1)
    rospy.init_node('heron')
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ['/home/nvidia/catkin_ws/src/heron_software/src/launch/'+launch_name+'.launch'])
    launch.start()
    while stdscr.getch() != 27:
        pass
    launch.shutdown()
    roscore.terminate()
    time.sleep(1)

def main(stdscr):
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    consigne = "Press ENTER to run master :(ESC to leave mode)"

    print_center(stdscr, consigne)

    while 1:
        key = stdscr.getch()

        if key == curses.KEY_ENTER or key in [10, 13]:
            start_launch('master',stdscr)

    print_center(stdscr, consigne)

curses.wrapper(main)
