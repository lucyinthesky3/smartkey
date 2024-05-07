class FrameManager:

    paneli = {}

    @staticmethod  # slicno kao i classmethod dekorator ali se ne prenosi instanca klase (nema cls kao parametar)
    def dodaj_panel(naziv, panel):
        FrameManager.paneli.update({naziv: panel})

    @staticmethod
    def prikazi_panel(naziv_panela):
        panel = FrameManager.paneli.get(naziv_panela)
        panel.tkraise()
