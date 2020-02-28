#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslaunch
import rospy
import curses
import gpio
import subprocess
import os
import time

#Mode du menu
menu = ['Remote Control', 'Navigation', 'Mapping', 'Take Key Positions', 'IP Config (Restart after)', 'Exit']

#Fonction pour modifier les IP aux lignes ROS_MASTER_URI et ROS_HOSTNAME du .zshrc
def modifIP(stdscr):
    stdscr.clear()
    curses.echo()  #Affiche les caractères que l'on tape sur le clavier
    stdscr.addstr("Adresse IP PC Central ? (Enter to continue, NO SPACES)\nExample : 10.224.0.52\n")
    ip_master = stdscr.getstr() #Récupère l'IP master
    stdscr.clear()
    stdscr.addstr("Adresse IP Heron ? (Enter to continue, NO SPACES)\nExample : 10.224.0.51\n")
    ip_heron = stdscr.getstr() #Récupère l'IP heron
    curses.noecho() #Désactive le fait d'afficher les caractères

    file = open("/home/nvidia/.zshrc", "r")
    content=file.readlines()
    file.close()
    for i in range(len(content)):
        if ("ROS_MASTER") in content[i]:
            content[i] = "export ROS_MASTER_URI=http://"+ip_master+":11311"
        if ("ROS_HOSTNAME") in content[i]:
            content[i] = "\nexport ROS_HOSTNAME="+ip_heron+"\n"

    file2 = open("/home/nvidia/.zshrc", "w")
    for line in content:
        file2.write(line)
    file2.close()


#Permet d'afficher le menu en récupérant la hauteur de l'écran et la largeur pour écrire les textes de manière centrée
def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h//2 - len(menu)//2 - 7,w//2 - len("MENU HERON")//2,"MENU HERON")
    consigne = "Use arrows to navigate and then ENTER :(ESC to leave mode)"
    stdscr.addstr(h//2 - len(menu)//2 - 2,w//2 - len(consigne)//2,consigne)
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx: #Met en blanc le fond du mode sur lequel on se trouve
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

#Change les variables d'environnement de ROS_MASTER_URI et ROS_HOSTNAME
def set_environment(master, ip):
    os.environ['ROS_MASTER_URI']=master
    os.environ['ROS_HOSTNAME']=ip

#Récupère les variables d'environnement de ROS_MASTER_URI et ROS_HOSTNAME 
def get_environment():
    return os.environ['ROS_MASTER_URI'], os.environ['ROS_HOSTNAME']

#Affiche les textes de manière centrée 
def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

#Permet de lancer un launch
def start_launch(launch_name, stdscr):
    stdscr.nodelay(1)
    gpio.setup(396,gpio.IN)
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ['/home/nvidia/catkin_ws/src/heron_software/src/launch/'+launch_name+'.launch'])
    launch.start() #Lance le launch
    while stdscr.getch() != 27 and gpio.read(396) != 0: #Attend que "Echap" ou le bouton d'arrêt d'urgence soit appuyé
        pass
    launch.shutdown() #Arrête le launch

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

        if key == curses.KEY_UP and current_row > 0: #Permet de monter dans les modes
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1: #Permet de descendre dans les modes
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]: #Permet de sélectionner un mode
            stdscr.clear()
            stdscr.refresh()
            if current_row == 0: #Mode manette
                master, ip = get_environment() #Récupère les IP actuelles du master et du robot
                set_environment("http://localhost:11311","localhost") #Définit le master et le hostname en local
                roscore = subprocess.Popen('roscore') #Lance un roscore
                time.sleep(1)
                start_launch('heronController', stdscr) #Lance le launch manette
                time.sleep(1)
                roscore.terminate() #Quitte le roscore
                time.sleep(1)
                set_environment(master,ip) #Remet les anciennes IP du master et du hostname
            if current_row == 1: #Mode Navigation
                start_launch('bringUp', stdscr)
            if current_row == 2: #Mode mapping
               start_launch('gmapping', stdscr)
            if current_row == 3: #Mode prise de positions
                start_launch('take_pos', stdscr)
            # if user selected last row, exit the program
            if current_row == 4: #Mode config IP
                stdscr.addstr("Are you sure ? Press ENTER and it will delete the old IP\nRestart the menu when finished to save the changes")
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]: #Si appui sur entrée
                    modifIP(stdscr)
                else: #Si appui sur autre touche
                    pass #Revient au menu
            if current_row == len(menu)-1: #Ferme le menu
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)
