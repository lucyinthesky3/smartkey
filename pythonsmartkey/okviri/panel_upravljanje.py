import tkinter as tk
from sqlalchemy.orm import sessionmaker
from okviri.pin_panel import PinPanel

from db.dbmanager import Admini, db_engine
Session = sessionmaker(bind=db_engine)
session = Session()


class PanelUpravljanje(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.pin_panel = None
        self.original_positions = []
        self.listbox = None
        self.checkbox_active = None
        self.entry_ime = None
        self.entry_prezime = None
        self.entry_pin = None
        self.grid(sticky="nsew")
        self.create_widgets()
        self.bind_pin_entered_event()

    def set_pin_panel(self, pin_panel):
        self.pin_panel = pin_panel

    def create_widgets(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        naslovni_label = tk.Label(self, text="Upravljanje dodijeljenim kljucevima")
        naslovni_label.grid(row=0, column=0, pady=10, padx=200, columnspan=2)

        lista_imena = tk.Frame(self, bd=2, highlightthickness=2, highlightbackground="orange", relief="ridge")
        lista_imena.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        lista_imena_naslov = tk.Label(lista_imena, text="Lista imena i prezimena osoba koje imaju digitalni ključ")
        lista_imena_naslov.grid(row=0, column=0, pady=10, padx=10)

        self.listbox = tk.Listbox(lista_imena, selectmode=tk.SINGLE)
        self.listbox.grid(row=1, column=0, sticky="nsew")

        # imena_i_prezimena = session.query(Admini.ime, Admini.prezime).all()
        #
        # for ime, prezime in imena_i_prezimena:
        #     self.listbox.insert(tk.END, f"{ime} {prezime}")

        frame_za_unos = tk.Frame(self, bd=2, highlightthickness=2, highlightbackground="orange", relief="ridge")
        frame_za_unos.grid(row=1, column=1, columnspan=4, pady=10, padx=10, sticky="nsew")

        label_names = ["Ime", "Prezime", "PIN", "Aktivan"]
        labels = [tk.Label(frame_za_unos, text=label_text) for label_text in label_names]

        for i, label in enumerate(labels):
            label.grid(row=i, column=1, padx=5, pady=5)

        entry_ime = tk.Entry(frame_za_unos)
        self.entry_ime = entry_ime

        entry_prezime = tk.Entry(frame_za_unos)
        self.entry_prezime = entry_prezime

        entry_pin = tk.Entry(frame_za_unos)
        self.entry_pin = entry_pin

        checkbox_active = tk.Checkbutton(frame_za_unos)

        entry_ime.grid(row=0, column=2, padx=5, pady=5)
        entry_prezime.grid(row=1, column=2, padx=5, pady=5)
        entry_pin.grid(row=2, column=2, padx=5, pady=5)
        checkbox_active.grid(row=3, column=2, padx=5, pady=5)

        self.checkbox_active = checkbox_active

        button_okvir = tk.Frame(self, bd=2, highlightthickness=2, highlightbackground="orange", relief="ridge")
        button_okvir.grid(row=2, column=1, columnspan=4, pady=10, padx=10, sticky="nsew")


        spremi_button = tk.Button(button_okvir, text="Save", command=self.save_changes)
        izbrisi_button = tk.Button(button_okvir, text="Delete", command=self.delete_user)
        odustani_button = tk.Button(button_okvir, text="Cancel", command=self.cancel_changes)

        spremi_button.grid(row=2, column=0, padx=5, pady=5)
        izbrisi_button.grid(row=2, column=1, padx=5, pady=5)
        odustani_button.grid(row=2, column=2, padx=5, pady=5)

        for widget in self.winfo_children():
            self.original_positions.append((widget, widget.grid_info()))

        for widget in self.winfo_children():
            widget.grid_forget()

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        self.initialize_listbox()

    def initialize_listbox(self):
        self.listbox.delete(0, tk.END)  # Clear the listbox
        imena_i_prezimena = session.query(Admini.ime, Admini.prezime).all()
        for ime, prezime in imena_i_prezimena:
            self.listbox.insert(tk.END, f"{ime} {prezime}")


    def is_admin_logged_in(self):
        return self.pin_panel and self.pin_panel.is_admin_logged_in()

    def show_all_widgets(self):
        for widget, position in self.original_positions:
            widget.grid(row=position['row'], column=position['column'])
        self.update_idletasks()

    def hide_all_widgets(self):
        self.original_positions = []
        for i, widget in enumerate(self.winfo_children()):
            position = widget.grid_info()
            self.original_positions.append((widget, position))
            widget.grid_forget()
        self.update_idletasks()

    def set_pin_panel(self, pin_panel):
        self.pin_panel = pin_panel
        self.bind_pin_entered_event()

    def bind_pin_entered_event(self):
        if self.pin_panel:
            self.pin_panel.bind(PinPanel.PIN_ENTERED_EVENT, self.handle_pin_entered)

    def handle_pin_entered(self, event):
        self.show_all_widgets()
        self.initialize_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)  # Clear the listbox

        imena_i_prezimena = session.query(Admini.ime, Admini.prezime).all()
        for ime, prezime in imena_i_prezimena:
            self.listbox.insert(tk.END, f"{ime} {prezime}")

    def save_changes(self):
        selected_index = self.listbox.curselection()
        ime = self.entry_ime.get()
        prezime = self.entry_prezime.get()
        pin = self.entry_pin.get()
        admin = ""

        if selected_index:
            selected_name = self.listbox.get(selected_index[0])  # Use selected_index[0]
            selected_admin = Admini.get_admin_by_pin(pin)
            selected_admin.ime = ime
            selected_admin.prezime = prezime
            selected_admin.admin = admin
            selected_admin.toggle_active_status()
        else:
            new_admin = Admini(ime=ime, prezime=prezime, pin=pin, admin=admin)
            new_admin.toggle_active_status()
            new_admin.update_or_add_admin()

            self.listbox.insert(tk.END, f"{ime} {prezime}")

        self.update_listbox()



    def delete_user(self):
        selected_item = self.listbox.curselection()

        if not selected_item:
            self.display_message("Error: Ispravno odaberi korisnika.")
            return

        selected_name = self.listbox.get(selected_item)
        first_name, last_name = selected_name.split()
        user_to_delete = session.query(Admini).filter_by(ime=first_name, prezime=last_name).first()

        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            self.update_listbox()
            self.display_message(f"Korisnik {selected_name} uspješno izbrisan.")
        else:
            self.display_message(f"Error: Korisnik {selected_name} nije pronađen u bazi podataka.")

    def cancel_changes(self):
        self.clear_input_fields()

    def clear_input_fields(self):
        self.entry_ime.delete(0, tk.END)
        self.entry_prezime.delete(0, tk.END)
        self.entry_pin.delete(0, tk.END)
        self.checkbox_active.deselect()

    def display_message(self, message):
        print(f"Status: {message}")


