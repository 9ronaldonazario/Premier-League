from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

#pozycje
class PozycjaBase(BaseModel):
    nazwa_pozycji: str
    skrot: str

class PozycjaCreate(PozycjaBase):
    pass

class Pozycja(PozycjaBase):
    id_pozycji: int
    
    class Config:
        from_attributes = True

#menedzerowie
class MenedzerBase(BaseModel):
    imie: str
    nazwisko: str
    narodowosc: Optional[str] = None
    data_urodzenia: Optional[date] = None

class MenedzerCreate(MenedzerBase):
    pass

class Menedzer(MenedzerBase):
    id_menedzera: int
    
    class Config:
        from_attributes = True

#stadiony
class StadionBase(BaseModel):
    nazwa_stadionu: str
    pojemnosc: Optional[int] = None
    miasto: Optional[str] = None
    rok_otwarcia: Optional[int] = None

class StadionCreate(StadionBase):
    pass

class Stadion(StadionBase):
    id_stadionu: int
    
    class Config:
        from_attributes = True

#kluby
class KlubBase(BaseModel):
    nazwa_klubu: str
    rok_zalozenia: Optional[int] = None
    id_stadionu: Optional[int] = None
    id_menedzera: Optional[int] = None

class KlubCreate(KlubBase):
    pass

class KlubUpdate(BaseModel):
    nazwa_klubu: Optional[str] = None
    id_stadionu: Optional[int] = None
    id_menedzera: Optional[int] = None

class Klub(KlubBase):
    id_klubu: int
    punkty: int = 0
    mecze_rozegrane: int = 0
    wygrane: int = 0
    remisy: int = 0
    przegrane: int = 0
    bramki_strzelone: int = 0
    bramki_stracone: int = 0
    roznica_bramek: int = 0
    
    class Config:
        from_attributes = True

class KlubDetale(Klub):
    stadion: Optional[Stadion] = None
    menedzer: Optional[Menedzer] = None

#zawodnicy
class ZawodnikBase(BaseModel):
    imie: str
    nazwisko: str
    data_urodzenia: Optional[date] = None
    narodowosc: Optional[str] = None
    wzrost: Optional[int] = None
    id_klubu: Optional[int] = None
    id_pozycji: Optional[int] = None
    wartosc_rynkowa: Optional[Decimal] = None
    numer_koszulki: Optional[int] = None

class ZawodnikCreate(ZawodnikBase):
    @validator('numer_koszulki')
    def validate_numer(cls, v):
        if v is not None and (v < 1 or v > 99):
            raise ValueError('Numer koszulki musi być między 1 a 99')
        return v

class ZawodnikUpdate(BaseModel):
    imie: Optional[str] = None
    nazwisko: Optional[str] = None
    id_klubu: Optional[int] = None
    id_pozycji: Optional[int] = None
    wartosc_rynkowa: Optional[Decimal] = None
    numer_koszulki: Optional[int] = None

class Zawodnik(ZawodnikBase):
    id_zawodnika: int
    
    class Config:
        from_attributes = True

class ZawodnikDetale(Zawodnik):
    klub: Optional[Klub] = None
    pozycja: Optional[Pozycja] = None

#mecze
class MeczBase(BaseModel):
    data_meczu: datetime
    id_klubu_gospodarze: int
    id_klubu_goscie: int
    sezon: str
    kolejka: int
    bramki_gospodarze: int = 0
    bramki_goscie: int = 0

class MeczCreate(MeczBase):
    @validator('id_klubu_goscie')
    def validate_kluby(cls, v, values):
        if 'id_klubu_gospodarze' in values and v == values['id_klubu_gospodarze']:
            raise ValueError('Klub nie może grać sam ze sobą')
        return v

class MeczUpdate(BaseModel):
    bramki_gospodarze: int
    bramki_goscie: int

class Mecz(MeczBase):
    id_meczu: int
    
    class Config:
        from_attributes = True

class MeczDetale(Mecz):
    klub_gospodarze: Optional[Klub] = None
    klub_goscie: Optional[Klub] = None

#statystyki indywidualne
class StatystykiIndywidualneBase(BaseModel):
    id_zawodnika: int
    id_meczu: int
    gole: int = 0
    asysty: int = 0
    zolte_kartki: int = 0
    czerwone_kartki: int = 0
    czyste_konto: bool = False
    minuty_rozegrane: int = 0

class StatystykiIndywidualneCreate(StatystykiIndywidualneBase):
    @validator('minuty_rozegrane')
    def validate_minuty(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Minuty muszą być między 0 a 120')
        return v
    
    @validator('gole', 'asysty', 'zolte_kartki', 'czerwone_kartki')
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError('Wartość nie może być ujemna')
        return v

class StatystykiIndywidualne(StatystykiIndywidualneBase):
    id_statystyki: int
    
    class Config:
        from_attributes = True

#transfery
class TransferBase(BaseModel):
    id_zawodnika: int
    id_klubu_z: Optional[int] = None
    id_klubu_do: int
    data_transferu: date
    kwota_transferu: Optional[Decimal] = None
    typ_transferu: str

class TransferCreate(TransferBase):
    @validator('typ_transferu')
    def validate_typ(cls, v):
        if v not in ['transfer', 'wypozyczenie', 'wolny_agent']:
            raise ValueError('Nieprawidłowy typ transferu')
        return v

class Transfer(TransferBase):
    id_transferu: int
    
    class Config:
        from_attributes = True

class TransferDetale(Transfer):
    zawodnik: Optional[Zawodnik] = None
    klub_z: Optional[Klub] = None
    klub_do: Optional[Klub] = None

#ranking strzelców
class RankingStrzelcow(BaseModel):
    imie: str
    nazwisko: str
    nazwa_klubu: str
    suma_goli: int
    suma_asyst: int
    suma_minut: int
    liczba_meczy: int

#forma drużyny
class FormaDruzyny(BaseModel):
    id_meczu: int
    data_meczu: datetime
    typ_meczu: str
    przeciwnik: str
    bramki_za: int
    bramki_przeciw: int
    wynik: str

#porownanie zawodników
class PorownanieZawodnikow(BaseModel):
    imie: str
    nazwisko: str
    nazwa_klubu: str
    wartosc_rynkowa: Optional[Decimal]
    mecze: int
    gole: int
    asysty: int
    minuty: int
    gole_na_90min: Optional[float]
    asysty_na_90min: Optional[float]

#skuteczność klubów
class SkutecznoscKlubu(BaseModel):
    nazwa_klubu: str
    punkty: int
    mecze_rozegrane: int
    bramki_strzelone: int
    bramki_stracone: int
    roznica_bramek: int
    srednia_goli: Optional[float]
    srednia_straconych: Optional[float]
    srednia_punktow: Optional[float]