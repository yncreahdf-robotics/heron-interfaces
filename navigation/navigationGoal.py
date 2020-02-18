# coding: utf-8
from tkinter import *
import sys
import subprocess
import time

window = Tk()
window['bg']='white'

window.title("Navigation Goal")
window.resizable(0, 0)

goals=[]

def sendGoal(x,y,z,w,h):
    print("sending")
    command = ["rostopic", "pub", "-1", "/Heron01/move_to", "heron/Motion", '{position_x: '+str(x)+', position_y: '+str(y)+', orientation_z: '+str(z)+', orientation_w: '+str(w)+', plate_height: '+str(h)+'}']
    subprocess.Popen(command)
    time.sleep(2)

def openFile(mode):
    return open("/home/centralheron/MapKeyPos.txt", mode)

def load():
    file = openFile("r")
    content = file.readlines()
    file.close()
    if(len(content) == 0):
        sys.exit()

    lines = content[1::]

    for line in lines:
        name = line.split(":")[0]
        x = float(line.split(":")[1].split(";")[0])
        y = float(line.split(":")[1].split(";")[1])
        z = float(line.split(":")[1].split(";")[2])
        w = float(line.split(":")[1].split(";")[3])
        h = float(line.split(":")[1].split(";")[4].split("\n")[0])

        GoalButton = Button(window, text=name, command= lambda: sendGoal(x,y,z,w,h))
        GoalButton.pack(side=TOP)


    # file = openFile("w")
    # for line in content:
    #     file.write(line)
    # file.close()
    



# closeButton = Button(window, text="close", command=window.destroy)
# closeButton.pack(side=RIGHT)


load()
window.mainloop()