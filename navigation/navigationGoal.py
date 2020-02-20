# coding: utf-8
from tkinter import *
import sys
import subprocess
import time

window = Tk()
window['bg']='white'

window.title("Navigation Goal")
window.resizable(0, 0)

Frame1 = Frame(window, borderwidth=2, relief=GROOVE)
Frame1.pack(side=TOP, padx=10, pady=10)
Label(Frame1, text="WARNNING\nDon't press any button until the robot is not localized properly in the environment !").pack(side=TOP)
Frame1.config(bg="#E84E48")

Frame2 = Frame(window, borderwidth=2, relief=GROOVE)
Frame2.pack(side=TOP, padx=10, pady=10)

def sendGoal(pos):
    print("sending")
    command = ["rostopic", "pub", "-1", "/Heron01/move_to", "heron/Motion", '{position_x: '+str(pos[0])+', position_y: '+str(pos[1])+', orientation_z: '+str(pos[2])+', orientation_w: '+str(pos[3])+', plate_height: '+str(pos[4])+'}']
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

        GoalButton = Button(Frame2, text=name, height=2, width=50, command= lambda p=[x,y,z,w,h,name] : sendGoal(p))
        GoalButton.pack(side=TOP)

    



    # file = openFile("w")
    # for line in content:
    #     file.write(line)
    # file.close()
    



# closeButton = Button(window, text="close", command=window.destroy)
# closeButton.pack(side=RIGHT)


load()
window.mainloop()