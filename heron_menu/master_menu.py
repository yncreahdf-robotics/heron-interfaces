#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslaunch
import rospy
import curses
import subprocess
import os
import time
import sys

#Mode du menu
menu = ['Navigation', 'Mapping', 'Take Key Positions', 'Edit Key Positions', 'IP Config (Restart after)', 'Exit']

#Fonction pour modifier les IP aux lignes ROS_MASTER_URI et ROS_HOSTNAME du .zshrc
#Modifie aussi le fichier HeronMasterStartup.desktop pour lancer le menu en ssh sur le robot 
def modifIP(stdscr):
    stdscr.clear()
    curses.echo()  #Affiche les caractères que l'on tape sur le clavier
    stdscr.addstr("Adresse IP PC Central ? (Enter to continue, NO SPACES)\nExample : 10.224.0.52\n")
    ip_master = stdscr.getstr() #Récupère l'IP master
    stdscr.clear()
    stdscr.addstr("Adresse IP Heron ? (Enter to continue, NO SPACES)\nExample : 10.224.0.51\n")
    ip_heron = stdscr.getstr() #Récupère l'IP heron
    curses.noecho() #Désactive le fait d'afficher les caractères

    file = open("/home/centralheron/.zshrc", "r")
    content=file.readlines()
    file.close()
    for i in range(len(content)):
        if ("ROS_MASTER") in content[i]:
            content[i] = "export ROS_MASTER_URI=http://"+ip_master+":11311"
        if ("ROS_HOSTNAME") in content[i]:
            content[i] = "\nexport ROS_HOSTNAME="+ip_master+"\n"

    file2 = open("/home/centralheron/.zshrc", "w")
    for line in content:
        file2.write(line)   #Ecrit la totalité du fichier .zshrc avec les IP changées
    file2.close()

    file3 = open("/home/centralheron/Desktop/HeronMasterStartup.desktop", "r")
    content=file3.readlines()
    file3.close()
    for i in range(len(content)):
        if "Exec" in content[i]:
            content[i] = 'Exec=zsh -c "ssh -t nvidia@'+ip_heron+' \'source .zshrc && python /home/nvidia/heron-interfaces/heron_menu/heron_menu.py\'"\n'
    file4 = open("/home/centralheron/Desktop/HeronMasterStartup.desktop", "w")

    for line in content:
        file4.write(line)  #Ecrit la totalité du fichier HeronMasterStartup.desktop en changeant l'IP en ssh

    file4.close()



#Permet d'afficher le menu en récupérant la hauteur de l'écran et la largeur pour écrire les textes de manière centrée
def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h//2 - len(menu)//2 - 7,w//2 - len("MENU MASTER")//2,"MENU MASTER")
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

#Affiche les textes de manière centrée 
def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()

#Permet de lancer un roscore en parallèle, de lancer un launch également
def start_launch(launch_name, stdscr, current_row):
    roscore = subprocess.Popen('roscore') #Roscore lancé en threading
    time.sleep(1)
    stdscr.nodelay(1) 
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ['/home/centralheron/catkin_ws/src/heron_software/src/launch/'+launch_name+'.launch'])
    launch.start() #Lance le launch
    while stdscr.getch() != 27: #Attend que "Echap" soit appuyé 
        pass
    launch.shutdown() #Arrête le launch
    if current_row == 1: #Si le mode est "mapping"
        rosrun = "rosrun map_server map_saver map:=/"+os.getenv("HERON_ID")+"/map -f /home/centralheron/catkin_ws/src/heron_software/map/demo"
        subprocess.check_call(rosrun.split()) #Lance la commande pour sauvegarder la map
    roscore.terminate() #Arrête le roscore
    time.sleep(1)

#Permet de lancer le programme pour éditer les positions 
def start_program1(stdscr):
    command = "python3 /home/centralheron/heron-interfaces/interface_graphique_modif_pos/modifPositions.py"
    program = subprocess.Popen(command.split())
    print_center(stdscr, "Click on [close] to get back to the menu.")
    while program.poll() == None: #Attend que le programme se termine
        pass

#Permet de lancer le programme pour envoyer des positions au robot
def start_program2():
    command = "python3 /home/centralheron/heron-interfaces/navigation/navigationGoal.py"
    return subprocess.Popen(command.split())
    


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
        stdscr.nodelay(0)
        if key == curses.KEY_UP and current_row > 0: #Permet de monter dans les modes
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1: #Permet de descendre dans les modes
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]: #Permet de sélectionner un mode
            stdscr.clear()
            stdscr.refresh()
            if current_row == 0: #Mode Navigation
                prog = start_program2() #Lance le programme d'envoi de positions
                start_launch('master_navigation', stdscr,current_row) #Lance le launch
                prog.terminate() #Coupe le programme d'envoi de positions
            if current_row == 1: #Mode Mapping
                stdscr.addstr("Are you sure ? \nPress ENTER and it will delete the old map.\nPress any other key to go back to menu.")
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]: #Appui Entrée
                    stdscr.clear()
                    start_launch('display_mapping', stdscr,current_row)
                else: #Si appui sur une autre touche
                    pass #Revient au menu
            if current_row == 2: #Mode Prise de positions
                stdscr.addstr("Are you sure ? \nPress ENTER and it will delete the old positions.\nPress any other key to go back to menu.")
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]: #Si appui sur entrée
                    stdscr.clear()
                    start_launch('take_key_position',stdscr,current_row)
                else: #Si appui sur une autre touche
                    pass #Revient au menu
                
            if current_row == 3: #Mode Edition de positions
                start_program1(stdscr) #Lance le programme pour éditer les positions

            if current_row == 4: #Mode config IP
                stdscr.addstr("Are you sure ? Press ENTER and it will delete the old IP\nRestart the menu when finished to save the changes")
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]: #Si appui sur entrée
                    modifIP(stdscr)
                else: #Si appui sur une autre touche
                    pass #Revient au menu
            if current_row == len(menu)-1: #Ferme le menu
                break

        print_menu(stdscr, current_row)
curses.wrapper(main)
