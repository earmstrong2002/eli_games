import tkinter as tk

INCREMENT = 1

def create_window():
    # root window
    win = tk.Tk()
    win.title('Counter')
    win.resizable(True, True)

    # grid config
    win.columnconfigure([0, 1, 2], weight=1, pad=5, minsize=50)
    win.rowconfigure([0, 1,], weight=1, pad=5, minsize=50)

    def create_widgets():
        # value display
        lbl_value = tk.Label(win, text='0')
        lbl_value.grid(
            column=1, row=0,
            sticky='nsew',
            padx=5, pady=5
        )
        
        # decrement button
        def decrement():
            inc = int(ent_increment.get())
            value = int(lbl_value['text'])
            lbl_value['text'] = f'{value - inc}'
        btn_decrement = tk.Button(win, text = '-', command=decrement)
        btn_decrement.grid(
            column=0, row=0,
            sticky='nsew',
            padx=5, pady=5
        )
        
        # increment button
        def increment():
            inc = int(ent_increment.get())
            value = int(lbl_value['text'])
            lbl_value['text'] = f'{value + inc}'
        btn_increment = tk.Button(win, text = '+', command=increment)
        btn_increment.grid(
            column=2, row=0,
            sticky='nsew',
            padx=5, pady=5
        )
        
        # increment picker
        ent_increment = tk.Entry(win, justify='center')
        ent_increment.insert(0, '1')
        ent_increment.grid(
            column=0, row=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky='nsew'
        )
        #increment = int(ent_increment.get())
        
    create_widgets()
    win.mainloop()
    
def main():
    create_window()

    print('Finished!')
main()