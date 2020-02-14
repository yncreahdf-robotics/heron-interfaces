#!/usr/bin/env python

import roslaunch
import rospy
import curses
import subprocess
import os
import time

menu = ['Navigation', 'Mapping', 'Exit']


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    consigne = "Use arrows to navigate and then ENTER :(ESC to leave mode)"
    stdscr.addstr(h//2 - len(menu)//2 - 2,w//2 - len(consigne)//2,consigne)
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

def start_launch(launch_name, stdscr, current_row):
    roscore = subprocess.Popen('roscore')
    time.sleep(1)
    stdscr.nodelay(1)
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ['/home/centralheron/catkin_ws/src/heron_software/src/launch/'+launch_name+'.launch'])
    launch.start()
    while stdscr.getch() != 27:
        pass
    launch.shutdown()
    if current_row == 1:
        rosrun = "rosrun map_server map_saver map:=/"+os.getenv("HERON_ID")+"/map -f /home/centralheron/catkin_ws/src/heron_software/map/demo"
        subprocess.check_call(rosrun.split())
    roscore.terminate()
    time.sleep(1)

def main(stdscr):
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # specify the current selected row
    current_row = 0

    # print the menu
    print_menu(stdscr, current_row)

    while 1:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            #print_center(stdscr, "You selected '{}'".format(menu[current_row]))
            stdscr.clear()
            stdscr.refresh()
            if current_row == 0:
                start_launch('master', stdscr,current_row)
            if current_row == 1:
                start_launch('master', stdscr,current_row)
            # if user selected last row, exit the program
            if current_row == len(menu)-1:
                break

        print_menu(stdscr, current_row)
curses.wrapper(main)