from tkinter import *


def donothing():
    x = 0


root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_cascade(label="Save", command=donothing)
shart = Menu(filemenu, tearoff=0)
shart.add_command(label="hello")
shart.add_command(label="hehe")
shart.add_command(
    label="holy mackerel", command=lambda: print("HOLY MACKEREL")
)
filemenu.add_cascade(label="shart", menu=shart)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()
