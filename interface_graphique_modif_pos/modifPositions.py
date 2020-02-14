# coding: utf-8
from tkinter import *


window = Tk()
window['bg']='white'
window.resizable(0, 0)

window.title("Edit Key Positions")

consigne = "Modifiez le nom des positions dans les champs puis cliquez sur modifier pour appliquer les changements."
Frame1 = Frame(window, borderwidth=1, relief=GROOVE)
Frame1.pack(side=TOP, padx=30, pady=10)
Label(Frame1, text = consigne).pack(padx=30, pady=30)


Frame2 = Frame(window, borderwidth=2, relief=GROOVE)
Frame2.pack(side=TOP, padx=30, pady=10)


Frame5 = Frame(Frame2,borderwidth=2, relief=GROOVE)
Frame5.pack(side=TOP, anchor=NE)
Label(Frame5, text="Position",width=32).pack(side=LEFT)
Label(Frame5, text="Orientation",width=32).pack(side=LEFT)
Label(Frame5, text="Hauteur",width=17).pack(side=LEFT)

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
    return open("MapKeyPos.txt", mode)

file = openFile("r")
content = file.readlines()
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


def modifier():
    for i in range(0,len(listOfTextbox)):
        print (textbox.get())
        var[i][0]=listOfTextbox[i].get()
    print(var)
    file = openFile("w")
    file.write(description)
    for line in var:
        file.write(line[0] + " :")
        for value in line[1:-1]:
            file.write(value + ";")
        file.write(str(line[len(line)-1]) + "\n")
    file.close()


boutonModifier = Button(Frame6, text='modifier',command=modifier, borderwidth=1).pack()
for ligne in range(nbPositions):
    value = StringVar()
    value.set(str(var[ligne][0]))
    textbox = Entry(Frame4, textvariable=value, width=20,selectborderwidth=4)
    textbox.grid(row=ligne,column=2)
    listOfTextbox.append(textbox)

    for colonne in range(6):
        labelx = Label(Frame4, text=var[ligne][1],width=16, bg="white").grid(row=ligne,column=3)
        labely = Label(Frame4, text=var[ligne][2],width=16, bg="white").grid(row=ligne,column=4)
        labelz = Label(Frame4, text=var[ligne][3],width=16, bg="white").grid(row=ligne,column=5)
        labelw = Label(Frame4, text=var[ligne][4],width=16, bg="white").grid(row=ligne,column=6)
        labelh = Label(Frame4, text=var[ligne][5],width=16, bg="white").grid(row=ligne,column=7)

closeButton = Button(window, text="close", command=window.destroy)
closeButton.pack(anchor=SE)


window.mainloop()
