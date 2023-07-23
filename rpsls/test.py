import tkinter as tk

def _lbl_init(master):
    label = tk.Label(master, text="sup")
    label["text"] = "hi"
    return label
    

root = tk.Tk()
label = _lbl_init(root).pack()
print(label)
root.mainloop()
