import tkinter as tk

def button_click():
    print("Button clicked!")
    tk.Tk().title("Test Window")

    button = tk.Button(tk.Tk(), text="Click Me", command=button_click)
    button.pack(padx=20, pady=10)

    tk.Tk().mainloop()
