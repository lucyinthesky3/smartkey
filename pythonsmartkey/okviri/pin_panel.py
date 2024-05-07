import tkinter as tk

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from db.dbmanager import Admini, db_engine
Session = sessionmaker(bind=db_engine)
session = Session()


class PinPanel(tk.Frame):
    PIN_ENTERED_EVENT = "<<PinEntered>>"

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.panel_upravljanje = None
        self.pin = ""
        self.pin_count = 0
        self.grid(sticky="nsew")
        self.create_widgets()

    def set_panel_upravljanje(self, panel_upravljanje):
        self.panel_upravljanje = panel_upravljanje

    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        naslovni_label = tk.Label(self, text="PIN panel")
        naslovni_label.grid(row=0, column=0, pady=10, padx=200, columnspan=2)

        self.pin_frame = tk.Frame(self, highlightthickness=2, highlightbackground="orange")
        self.pin_frame.grid(row=1, column=0, padx=(0, 100), pady=30)
        self.pin_frame.grid_forget()

        for i in range(4):
            self.lbl_prazni = tk.Label(self.pin_frame, width=3, height=2, bd=2, relief="ridge")
            self.lbl_prazni.grid(row=1, column=i, padx=5, pady=5)

        for i in range(1, 10):
            btn_brojevi = tk.Button(
                self.pin_frame, text=str(i), width=3, height=2, bd=2, relief="ridge",
                command=lambda num=i: self.handle_pin_button(num)
            )
            btn_brojevi.grid(row=(i - 1) // 3 + 2, column=(i - 1) % 3, padx=5, pady=5)


        self.lbl_blank = tk.Label(self.pin_frame, width=3, height=2, bd=2, relief="ridge")
        self.lbl_blank.grid(row=5, column=0, padx=5, pady=5)

        btn_nula = tk.Button(self.pin_frame, text="0", width=3, height=2, bd=2, relief="ridge",
                             command=lambda: self.handle_pin_button(0))
        btn_nula.grid(row=5, column=1, padx=5, pady=5)

        btn_c = tk.Button(self.pin_frame, text="C", width=3, height=2, bd=2, relief="ridge",
                          command=self.clear_status_frame)
        btn_c.grid(row=5, column=2, padx=5, pady=5)




        self.status_frame = tk.Frame(self, bd=2, highlightthickness=2, highlightbackground="orange", relief="ridge")
        self.status_frame.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.status_frame.grid_forget()
        self.status_label = tk.Label(self.status_frame, text="Status i poruke")
        self.status_label.grid(row=0, column=1, sticky="n", pady=10, padx=70)
        self.poruka_label = tk.Label(self.status_frame, text="Zvono je aktivirano! Uskoro će netko doći i otvoriti vrata.")
        self.poruka_label.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)


    def show_pin_frame(self):
        self.pin_frame.grid(row=1, column=0, padx=(0, 100), pady=30)
        self.status_frame.grid_forget()

    def show_status_frame(self):
        self.pin_frame.grid_forget()
        self.status_frame.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky="nsew")

    def update_status_frame(self, message):
        self.poruka_label.config(text=message)
        self.show_status_frame()

    def clear_status_frame(self):
        self.pin = ""
        self.poruka_label.config(text="")
        self.status_frame.grid_forget()

    def handle_pin_button(self, num):
        self.pin += str(num)
        if len(self.pin) == 4:
            user = Admini.get_admin_by_pin(self.pin)
            if user:
                self.update_status_frame(f"Unesen je admin pin! Dobrodošao {user.ime} {user.prezime}")

                if self.panel_upravljanje:
                    self.trigger_pin_entered_event()
                else:
                    print("Debug: panel_upravljanje is not set correctly")
            else:
                self.update_status_frame("Neispravan PIN")
                self.reset_pin_entry()


    def reset_pin_entry(self):
        self.pin = ""

    def is_admin_logged_in(self):
        user = Admini.get_admin_by_pin(self.pin)
        return user is not None

    def otvori_panel_za_upravljanje(self):
        if self.panel_upravljanje and self.panel_upravljanje.is_admin_logged_in():
            self.panel_upravljanje.show_all_widgets()

    def admin_logged_in(self):
        if self.panel_upravljanje:
            self.panel_upravljanje.show_all_widgets()
        else:
            print("Debug: PanelUpravljanje is not set correctly")

    def trigger_pin_entered_event(self):
        self.event_generate(self.PIN_ENTERED_EVENT, when="tail")

    def handle_pin_entered(self, event):
        self.show_pin_frame()
        self.otvori_panel_za_upravljanje()


