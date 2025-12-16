from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, DECIMAL, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TypTransferuEnum(enum.Enum):
    transfer = "transfer"
    wypozyczenie = "wypozyczenie"
    wolny_agent = "wolny_agent"

class Pozycje(Base):
    __tablename__ = "Pozycje"
    
    id_pozycji = Column(Integer, primary_key=True, autoincrement=True)
    nazwa_pozycji = Column(String(50), nullable=False)
    skrot = Column(String(10), nullable=False)
    
    zawodnicy = relationship("Zawodnicy", back_populates="pozycja")

class Menedzerowie(Base):
    __tablename__ = "Menedzerowie"
    
    id_menedzera = Column(Integer, primary_key=True, autoincrement=True)
    imie = Column(String(50), nullable=False)
    nazwisko = Column(String(50), nullable=False)
    narodowosc = Column(String(50))
    data_urodzenia = Column(Date)
    
    kluby = relationship("Kluby", back_populates="menedzer")

class Stadiony(Base):
    __tablename__ = "Stadiony"
    
    id_stadionu = Column(Integer, primary_key=True, autoincrement=True)
    nazwa_stadionu = Column(String(100), nullable=False)
    pojemnosc = Column(Integer)
    miasto = Column(String(50))
    rok_otwarcia = Column(Integer)
    
    kluby = relationship("Kluby", back_populates="stadion")

class Kluby(Base):
    __tablename__ = "Kluby"
    
    id_klubu = Column(Integer, primary_key=True, autoincrement=True)
    nazwa_klubu = Column(String(100), nullable=False, unique=True)
    rok_zalozenia = Column(Integer)
    id_stadionu = Column(Integer, ForeignKey("Stadiony.id_stadionu", ondelete="SET NULL"))
    id_menedzera = Column(Integer, ForeignKey("Menedzerowie.id_menedzera", ondelete="SET NULL"))
    punkty = Column(Integer, default=0)
    mecze_rozegrane = Column(Integer, default=0)
    wygrane = Column(Integer, default=0)
    remisy = Column(Integer, default=0)
    przegrane = Column(Integer, default=0)
    bramki_strzelone = Column(Integer, default=0)
    bramki_stracone = Column(Integer, default=0)
    roznica_bramek = Column(Integer, default=0)
    
    stadion = relationship("Stadiony", back_populates="kluby")
    menedzer = relationship("Menedzerowie", back_populates="kluby")
    zawodnicy = relationship("Zawodnicy", back_populates="klub")
    mecze_gospodarze = relationship("Mecze", foreign_keys="[Mecze.id_klubu_gospodarze]", back_populates="klub_gospodarze")
    mecze_goscie = relationship("Mecze", foreign_keys="[Mecze.id_klubu_goscie]", back_populates="klub_goscie")

class Zawodnicy(Base):
    __tablename__ = "Zawodnicy"
    
    id_zawodnika = Column(Integer, primary_key=True, autoincrement=True)
    imie = Column(String(50), nullable=False)
    nazwisko = Column(String(50), nullable=False)
    data_urodzenia = Column(Date)
    narodowosc = Column(String(50))
    wzrost = Column(Integer)
    id_klubu = Column(Integer, ForeignKey("Kluby.id_klubu", ondelete="SET NULL"))
    id_pozycji = Column(Integer, ForeignKey("Pozycje.id_pozycji", ondelete="SET NULL"))
    wartosc_rynkowa = Column(DECIMAL(10, 2))
    numer_koszulki = Column(Integer)
    
    klub = relationship("Kluby", back_populates="zawodnicy")
    pozycja = relationship("Pozycje", back_populates="zawodnicy")
    statystyki = relationship("StatystykiIndywidualne", back_populates="zawodnik")
    transfery = relationship("Transfery", back_populates="zawodnik")

class Mecze(Base):
    __tablename__ = "Mecze"
    
    id_meczu = Column(Integer, primary_key=True, autoincrement=True)
    data_meczu = Column(DateTime, nullable=False)
    id_klubu_gospodarze = Column(Integer, ForeignKey("Kluby.id_klubu", ondelete="CASCADE"), nullable=False)
    id_klubu_goscie = Column(Integer, ForeignKey("Kluby.id_klubu", ondelete="CASCADE"), nullable=False)
    bramki_gospodarze = Column(Integer, default=0)
    bramki_goscie = Column(Integer, default=0)
    sezon = Column(String(20), nullable=False)
    kolejka = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint('id_klubu_gospodarze != id_klubu_goscie', name='check_different_clubs'),
    )
    
    klub_gospodarze = relationship("Kluby", foreign_keys=[id_klubu_gospodarze], back_populates="mecze_gospodarze")
    klub_goscie = relationship("Kluby", foreign_keys=[id_klubu_goscie], back_populates="mecze_goscie")
    statystyki = relationship("StatystykiIndywidualne", back_populates="mecz")
    sklady = relationship("SkladyMeczowe", back_populates="mecz")

class SkladyMeczowe(Base):
    __tablename__ = "SkladyMeczowe"
    
    id_skladu = Column(Integer, primary_key=True, autoincrement=True)
    id_meczu = Column(Integer, ForeignKey("Mecze.id_meczu", ondelete="CASCADE"), nullable=False)
    id_zawodnika = Column(Integer, ForeignKey("Zawodnicy.id_zawodnika", ondelete="CASCADE"), nullable=False)
    id_klubu = Column(Integer, ForeignKey("Kluby.id_klubu", ondelete="CASCADE"), nullable=False)
    w_podstawowym_skladzie = Column(Boolean, default=True)
    minuty_rozegrane = Column(Integer, default=0)
    
    mecz = relationship("Mecze", back_populates="sklady")
    zawodnik = relationship("Zawodnicy")
    klub = relationship("Kluby")

class StatystykiIndywidualne(Base):
    __tablename__ = "StatystykiIndywidualne"
    
    id_statystyki = Column(Integer, primary_key=True, autoincrement=True)
    id_zawodnika = Column(Integer, ForeignKey("Zawodnicy.id_zawodnika", ondelete="CASCADE"), nullable=False)
    id_meczu = Column(Integer, ForeignKey("Mecze.id_meczu", ondelete="CASCADE"), nullable=False)
    gole = Column(Integer, default=0)
    asysty = Column(Integer, default=0)
    zolte_kartki = Column(Integer, default=0)
    czerwone_kartki = Column(Integer, default=0)
    czyste_konto = Column(Boolean, default=False)
    minuty_rozegrane = Column(Integer, default=0)
    
    zawodnik = relationship("Zawodnicy", back_populates="statystyki")
    mecz = relationship("Mecze", back_populates="statystyki")

class Transfery(Base):
    __tablename__ = "Transfery"
    
    id_transferu = Column(Integer, primary_key=True, autoincrement=True)
    id_zawodnika = Column(Integer, ForeignKey("Zawodnicy.id_zawodnika", ondelete="CASCADE"), nullable=False)
    id_klubu_z = Column(Integer, ForeignKey("Kluby.id_klubu", ondelete="SET NULL"))
    id_klubu_do = Column(Integer, ForeignKey("Kluby.id_klubu", ondelete="CASCADE"), nullable=False)
    data_transferu = Column(Date, nullable=False)
    kwota_transferu = Column(DECIMAL(10, 2))
    typ_transferu = Column(Enum(TypTransferuEnum), nullable=False)
    
    zawodnik = relationship("Zawodnicy", back_populates="transfery")
    klub_z = relationship("Kluby", foreign_keys=[id_klubu_z])
    klub_do = relationship("Kluby", foreign_keys=[id_klubu_do])