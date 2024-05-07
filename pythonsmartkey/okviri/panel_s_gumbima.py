import tkinter as tk
from okviri.pin_panel import PinPanel

class PanelGumbi(tk.Frame):

    def __init__(self, master, pin_panel, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pin_panel = pin_panel
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):

        self.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        naslovni_label = tk.Label(self, text="Panel s gumbima")
        naslovni_label.grid(row=0, column=0, pady=10, columnspan=2)

        button1_frame = tk.Frame(self, highlightthickness=2, highlightbackground="orange")
        button1_frame.grid(row=1, column=0, padx=(0, 100), pady=30)
        button2_frame = tk.Frame(self, highlightthickness=2, highlightbackground="orange")
        button2_frame.grid(row=1, column=1, padx=(100, 0))

        self.pozvoni_button = tk.Button(button1_frame, text="POZVONI", command=self.show_status_frame)
        self.pozvoni_button.grid(row=0, column=0)
        self.otkljucaj_button = tk.Button(button2_frame, text="OTKLJUČAJ", command=self.show_pin_frame)
        self.otkljucaj_button.grid(row=0, column=0)

    def show_pin_frame(self):
        self.pin_panel.show_pin_frame()

    def show_status_frame(self):
        self.pin_panel.show_status_frame()





