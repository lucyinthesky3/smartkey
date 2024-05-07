import tkinter as tk
from okviri.panel_s_gumbima import PanelGumbi
from okviri.framemanager import FrameManager
from okviri.pin_panel import PinPanel
from okviri.panel_upravljanje import PanelUpravljanje

root = tk.Tk()
root.geometry("600x900+100+100")
root.title("Smart Key")

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=2)
root.grid_columnconfigure(0, weight=1)

pin_panel = PinPanel(root, height=100, highlightthickness=2, highlightbackground="orange")
pin_panel.grid(row=1, column=0, sticky="nsew")
FrameManager.dodaj_panel("pin_panel", pin_panel)


panel_upravljanje = PanelUpravljanje(root, height=200, highlightthickness=2, highlightbackground="orange")
panel_upravljanje.grid(row=2, column=0, sticky="nsew")
FrameManager.dodaj_panel("panel_upravljanje", panel_upravljanje)


panel_gumbi = PanelGumbi(root, pin_panel=pin_panel, highlightthickness=2, highlightbackground="orange", padx=120)
panel_gumbi.grid(row=0, column=0, sticky="nsew")
FrameManager.dodaj_panel("panel_s_gumbima", panel_gumbi)

pin_panel.set_panel_upravljanje(panel_upravljanje)
panel_upravljanje.set_pin_panel(pin_panel)



root.mainloop()


