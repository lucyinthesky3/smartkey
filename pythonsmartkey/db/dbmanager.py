import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base

from okviri.framemanager import FrameManager

Base = declarative_base()

db_engine = db.create_engine('sqlite:///Baza.db')
Session = sessionmaker(bind=db_engine)
session = Session()

class Admini(Base):
    __tablename__ = "admini"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String)
    prezime = db.Column(db.String)
    pin = db.Column(db.Integer)
    admin = db.Column(db.Text)
    aktivan = db.Column(db.Text)


    def __init__(self, ime, prezime, pin, admin):
        self.ime = ime
        self.prezime = prezime
        self.pin = pin
        self.admin = admin

    def __str__(self):
        return("OSOBA: " + " " + str(self.ime) + " " + self.prezime)


    @classmethod
    def get_admin_by_pin(cls, pin):
        return session.query(Admini).filter_by(pin=pin).first()

    def update_or_add_admin(self):
        # Check if an admin with the same pin exists in the database
        existing_admin = session.query(Admini).filter_by(pin=self.pin).first()

        if existing_admin:
            # Update the existing admin
            existing_admin.ime = self.ime
            existing_admin.prezime = self.prezime
            existing_admin.admin = self.admin
        else:
            # Add a new admin
            session.add(self)

        session.commit()

    def toggle_active_status(self):
        self.aktivan = not self.aktivan
        session.commit()
