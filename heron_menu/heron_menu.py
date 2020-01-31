# coding: utf-8
#!/usr/bin/python2.7

import roslaunch
import rospy
import curses
import gpio

menu = ['Controle par manette', 'Navigation', 'Mapping', 'Prise de positions', 'Exit']

gpio.setup(396,gpio.IN)


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
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

def start_launch(launch_name, stdscr):
    val_gpio = gpio.read(396)
    val_gpio = 1
    emergency = False
    echap = False
    while emergency == False:
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid, ['/home/sly/catkin_ws/src/heron_software/src/launch/'+launch_name+'.launch'])
        launch.start()
        while echap == False and emergency == False:
            val_gpio = gpio.read(396) 
            if stdscr.getch() == 27:
                echap = True
            elif val_gpio == 0:
                emergency = True
            else:
                pass
        launch.shutdown()
        if echap == True:
            break
        else:
            while emergency == True:
                val_gpio = gpio.read(396)
                if val_gpio == 1:  
                    emergency = False
                else:
                    pass

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
                start_launch('heronController', stdscr)
            if current_row == 1:
                start_launch('bringUp', stdscr)
            if current_row == 2:
               start_launch('gmapping', stdscr)
            if current_row == 3:
                start_launch('take_pos', stdscr)
            # if user selected last row, exit the program
            if current_row == len(menu)-1:
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)

