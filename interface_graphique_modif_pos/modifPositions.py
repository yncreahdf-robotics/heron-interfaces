# coding: utf-8
from tkinter import *
import sys


window = Tk()
window['bg']='white'
window.resizable(0, 0)

window.title("Edit Key Positions")

consigne = "Rename key positions and Delete unwanted ones.\nThen click on [Save and Close] to save your changes OR close the window to discard changes (upper corner red cross)."
Frame1 = Frame(window, borderwidth=1, relief=GROOVE)
Frame1.pack(side=TOP, padx=30, pady=10)
Label(Frame1, text = consigne).pack(padx=15, pady=15)


Frame2 = Frame(window, borderwidth=2, relief=GROOVE)
Frame2.pack(side=TOP, padx=30, pady=10)


Frame5 = Frame(Frame2,borderwidth=2, relief=GROOVE)
Frame5.pack(side=TOP, anchor=NE)
Label(Frame5, text="Position",width=32).pack(side=LEFT)
Label(Frame5, text="Orientation",width=32).pack(side=LEFT)
Label(Frame5, text="Height",width=17).pack(side=LEFT)

Frame3 = Frame(Frame2, borderwidth=2, relief=GROOVE)
Frame3.pack(side=TOP, anchor=NE)
Label(Frame3, text="x",width=16).pack(side=LEFT)
Label(Frame3, text="y",width=16).pack(side=LEFT)
Label(Frame3, text="z",width=16).pack(side=LEFT)
Label(Frame3, text="w",width=16).pack(side=LEFT)
Label(Frame3, text="h",width=16).pack(side=LEFT)

Frame4 = Frame(Frame2, borderwidth=2, relief=GROOVE)
Frame4.pack(side=TOP)

Frame6 = Frame(window,borderwidth=1, relief=GROOVE)
Frame6.pack(side=TOP, pady=10)

var=[]

def openFile(mode):
    return open("/home/centralheron/MapKeyPos.txt", mode)

file = openFile("r")
content = file.readlines()
if(len(content) == 0):
    sys.exit()
description = content[0]
lines = content[1::]
positions=[]
nbPositions = len(lines)

listOfTextbox=list()

for line in lines:
    pos = line.split(":")[0]
    x = line.split(":")[1].split(";")[0]
    y = line.split(":")[1].split(";")[1]
    z = line.split(":")[1].split(";")[2]
    w = line.split(":")[1].split(";")[3]
    h = line.split(":")[1].split(";")[4].split("\n")[0]
    var.append([pos, x, y, z, w, h])


def fermerSauvegarder():
    global listOfTextbox

    for i in range(len(var)):
        var[i][0]=listOfTextbox[i].get()

    file = openFile("w")
    file.write(description)
    for line in var:
        file.write(line[0] + ":")
        for value in line[1:-1]:
            file.write(value + ";")
        file.write(str(line[len(line)-1]) + "\n")
    file.close()
    window.destroy()


def supprimer(ligne):
    global listOfTextbox
    global nbPositions
    
    var.pop(ligne)
    listOfTextbox.pop(ligne)
    nbPositions = nbPositions - 1

    update()



def update():    
    global Frame4
    Frame4.destroy()
    Frame4 = Frame(Frame2, borderwidth=2, relief=GROOVE)
    Frame4.pack(side=TOP)
    listOfTextbox.clear()

    for ligne in range(nbPositions):
        value = StringVar()
        value.set(str(var[ligne][0]))
        textbox = Entry(Frame4, textvariable=value, width=20, selectborderwidth=4, justify="right")
        textbox.grid(row=ligne,column=2)
        listOfTextbox.append(textbox)

        for colonne in range(6):

            labelx = Label(Frame4, text=var[ligne][1],width=16, bg="white").grid(row=ligne,column=3)
            labely = Label(Frame4, text=var[ligne][2],width=16, bg="white").grid(row=ligne,column=4)
            labelz = Label(Frame4, text=var[ligne][3],width=16, bg="white").grid(row=ligne,column=5)
            labelw = Label(Frame4, text=var[ligne][4],width=16, bg="white").grid(row=ligne,column=6)
            labelh = Label(Frame4, text=var[ligne][5],width=16, bg="white").grid(row=ligne,column=7)
            
            
            suppr = Button(Frame4, text='Delete',command= lambda l=ligne : supprimer(l), borderwidth=1)
            suppr.grid(row=ligne,column=1)
            suppr.config(padx=10, pady=-1, bg="#E84E48")


closeButton = Button(window, text="Save and Close", command=fermerSauvegarder)
closeButton.pack(anchor=SE, padx=5, pady=5)
closeButton.config(bg="#6EFF6E")

update()
window.mainloop()
