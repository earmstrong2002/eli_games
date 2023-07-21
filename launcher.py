# This program acts as a launcher for all the games I have made
import importlib
import tkinter as tk

# Import all games
import counter.counter as counter
import rpsls.rpsls as rpsls


def create_window():
    top = tk.Tk()

    # Configure grid. REMEMBER TO UPDATE WHEN YOU ADD A NEW GAME
    top.columnconfigure([0, 1], weight=1, minsize=100)
    top.rowconfigure(0, weight=1, minsize=100)

    # Create the buttons that launch each game.
    def create_widgets():
        btn_counter = tk.Button(text="Counter", command=counter.main)
        btn_counter.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        btn_rpsls = tk.Button(text="RPSLS", command=rpsls.main)
        btn_rpsls.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    create_widgets()
    top.mainloop()


def main():
    create_window()


if __name__ == "__main__":
    main()
