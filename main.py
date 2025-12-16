from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Premier League Statistics API",
    description="System statystyk zawodników i klubów Premier League",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Premier League Statistics API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

#kluby
@app.get("/kluby/", response_model=List[schemas.Klub], tags=["Kluby"])
def read_kluby(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Pobiera listę wszystkich klubów"""
    kluby = crud.get_kluby(db, skip=skip, limit=limit)
    return kluby

@app.get("/kluby/{klub_id}", response_model=schemas.KlubDetale, tags=["Kluby"])
def read_klub(klub_id: int, db: Session = Depends(get_db)):
    """Pobiera szczegóły klubu (WF.05)"""
    klub = crud.get_klub(db, klub_id=klub_id)
    if klub is None:
        raise HTTPException(status_code=404, detail="Klub nie znaleziony")
    return klub

@app.post("/kluby/", response_model=schemas.Klub, tags=["Kluby"])
def create_klub(klub: schemas.KlubCreate, db: Session = Depends(get_db)):
    """Dodaje nowy klub (WF.13)"""
    return crud.create_klub(db=db, klub=klub)

@app.put("/kluby/{klub_id}", response_model=schemas.Klub, tags=["Kluby"])
def update_klub(klub_id: int, klub: schemas.KlubUpdate, db: Session = Depends(get_db)):
    """Edytuje dane klubu (WF.13)"""
    updated = crud.update_klub(db, klub_id=klub_id, klub=klub)
    if updated is None:
        raise HTTPException(status_code=404, detail="Klub nie znaleziony")
    return updated

@app.get("/kluby/tabela/ligowa", response_model=List[schemas.Klub], tags=["Kluby"])
def read_tabela_ligowa(db: Session = Depends(get_db)):
    """Pobiera aktualną tabelę ligową posortowaną według punktów (WF.04)"""
    return crud.get_kluby(db, skip=0, limit=100)

#zawodnicy
@app.get("/zawodnicy/", response_model=List[schemas.Zawodnik], tags=["Zawodnicy"])
def read_zawodnicy(
    skip: int = 0, 
    limit: int = 100,
    klub_id: Optional[int] = Query(None, description="Filtruj według klubu"),
    pozycja_id: Optional[int] = Query(None, description="Filtruj według pozycji"),
    narodowosc: Optional[str] = Query(None, description="Filtruj według narodowości"),
    db: Session = Depends(get_db)
):
    """
    Pobiera listę zawodników z możliwością filtrowania (WF.06, WF.07)
    - klub_id: ID klubu
    - pozycja_id: ID pozycji
    - narodowosc: narodowość zawodnika
    """
    zawodnicy = crud.get_zawodnicy(
        db, 
        skip=skip, 
        limit=limit,
        klub_id=klub_id,
        pozycja_id=pozycja_id,
        narodowosc=narodowosc
    )
    return zawodnicy

@app.get("/zawodnicy/search/", response_model=List[schemas.Zawodnik], tags=["Zawodnicy"])
def search_zawodnicy(
    q: str = Query(..., description="Szukaj po imieniu lub nazwisku"),
    db: Session = Depends(get_db)
):
    """Wyszukuje zawodników po imieniu lub nazwisku (WF.07)"""
    return crud.search_zawodnicy(db, search=q)

@app.get("/zawodnicy/{zawodnik_id}", response_model=schemas.ZawodnikDetale, tags=["Zawodnicy"])
def read_zawodnik(zawodnik_id: int, db: Session = Depends(get_db)):
    """Pobiera szczegółowy profil zawodnika (WF.01)"""
    zawodnik = crud.get_zawodnik(db, zawodnik_id=zawodnik_id)
    if zawodnik is None:
        raise HTTPException(status_code=404, detail="Zawodnik nie znaleziony")
    return zawodnik

@app.post("/zawodnicy/", response_model=schemas.Zawodnik, tags=["Zawodnicy"])
def create_zawodnik(zawodnik: schemas.ZawodnikCreate, db: Session = Depends(get_db)):
    """Dodaje nowego zawodnika (WF.12)"""
    return crud.create_zawodnik(db=db, zawodnik=zawodnik)

@app.put("/zawodnicy/{zawodnik_id}", response_model=schemas.Zawodnik, tags=["Zawodnicy"])
def update_zawodnik(
    zawodnik_id: int, 
    zawodnik: schemas.ZawodnikUpdate, 
    db: Session = Depends(get_db)
):
    """Edytuje dane zawodnika (WF.12)"""
    updated = crud.update_zawodnik(db, zawodnik_id=zawodnik_id, zawodnik=zawodnik)
    if updated is None:
        raise HTTPException(status_code=404, detail="Zawodnik nie znaleziony")
    return updated

#mecze
@app.get("/mecze/", response_model=List[schemas.Mecz], tags=["Mecze"])
def read_mecze(
    sezon: Optional[str] = Query(None, description="Filtruj według sezonu"),
    kolejka: Optional[int] = Query(None, description="Filtruj według kolejki"),
    db: Session = Depends(get_db)
):
    """
    Pobiera listę meczów z możliwością filtrowania (WF.08)
    - sezon: np. "2024/25"
    - kolejka: numer kolejki
    """
    return crud.get_mecze(db, sezon=sezon, kolejka=kolejka)

@app.get("/mecze/{mecz_id}", response_model=schemas.MeczDetale, tags=["Mecze"])
def read_mecz(mecz_id: int, db: Session = Depends(get_db)):
    """Pobiera szczegóły meczu (WF.09)"""
    mecz = crud.get_mecz(db, mecz_id=mecz_id)
    if mecz is None:
        raise HTTPException(status_code=404, detail="Mecz nie znaleziony")
    return mecz

@app.post("/mecze/", response_model=schemas.Mecz, tags=["Mecze"])
def create_mecz(mecz: schemas.MeczCreate, db: Session = Depends(get_db)):
    """
    T1: Dodaje wynik meczu i automatycznie aktualizuje statystyki klubów (WF.10, WF.11)
    
    Transakcja atomowa która:
    1. Zapisuje mecz
    2. Aktualizuje punkty, wygrane, remisy, przegrane
    3. Aktualizuje bramki strzelone/stracone
    4. Przelicza różnicę bramek
    """
    return crud.create_mecz_z_aktualizacja_statystyk(db=db, mecz=mecz)

#transakcje/raporty
@app.get("/raporty/ranking-strzelcow", tags=["Raporty"])
def read_ranking_strzelcow(
    sezon: str = Query(..., description="Sezon np. '2024/25'"),
    limit: int = Query(20, description="Liczba wyników"),
    db: Session = Depends(get_db)
):
    """
    T2: Ranking najlepszych strzelców w sezonie (WF.15)
    
    Zwraca:
    - Imię i nazwisko
    - Klub
    - Suma goli
    - Suma asyst
    - Liczba meczów
    - Suma minut
    """
    results = crud.get_ranking_strzelcow(db, sezon=sezon, limit=limit)
    return [
        {
            "imie": r.imie,
            "nazwisko": r.nazwisko,
            "nazwa_klubu": r.nazwa_klubu,
            "suma_goli": r.suma_goli,
            "suma_asyst": r.suma_asyst,
            "suma_minut": r.suma_minut,
            "liczba_meczy": r.liczba_meczy
        }
        for r in results
    ]

@app.get("/raporty/forma-druzyny/{klub_id}", tags=["Raporty"])
def read_forma_druzyny(
    klub_id: int,
    limit: int = Query(5, description="Liczba ostatnich meczów"),
    db: Session = Depends(get_db)
):
    """
    T3: Forma drużyny na podstawie ostatnich meczów
    
    Zwraca:
    - Dane meczu
    - Przeciwnik
    - Wynik (W/R/P)
    - Bramki za/przeciw
    """
    results = crud.get_forma_druzyny(db, klub_id=klub_id, limit=limit)
    return [
        {
            "id_meczu": r[0],
            "data_meczu": r[1],
            "typ_meczu": r[2],
            "przeciwnik": r[3],
            "bramki_za": r[4],
            "bramki_przeciw": r[5],
            "wynik": r[6]
        }
        for r in results
    ]

@app.get("/raporty/porownanie-zawodnikow", tags=["Raporty"])
def read_porownanie_zawodnikow(
    pozycja_id: int = Query(..., description="ID pozycji"),
    sezon: str = Query(..., description="Sezon np. '2024/25'"),
    db: Session = Depends(get_db)
):
    """
    T4: Porównanie zawodników na tej samej pozycji
    
    Zwraca:
    - Imię i nazwisko
    - Klub
    - Wartość rynkowa
    - Statystyki (gole, asysty, minuty)
    - Średnie per 90 minut
    """
    results = crud.get_porownanie_zawodnikow(db, pozycja_id=pozycja_id, sezon=sezon)
    return [
        {
            "imie": r[0],
            "nazwisko": r[1],
            "nazwa_klubu": r[2],
            "wartosc_rynkowa": float(r[3]) if r[3] else None,
            "mecze": r[4],
            "gole": r[5],
            "asysty": r[6],
            "minuty": r[7],
            "gole_na_90min": float(r[8]) if r[8] else 0.0,
            "asysty_na_90min": float(r[9]) if r[9] else 0.0
        }
        for r in results
    ]

@app.get("/raporty/skutecznosc-klubow", tags=["Raporty"])
def read_skutecznosc_klubow(db: Session = Depends(get_db)):
    """
    T6: Ranking klubów pod względem skuteczności ofensywnej i defensywnej
    
    Zwraca:
    - Nazwa klubu
    - Punkty i statystyki meczowe
    - Średnie (gole, stracone, punkty na mecz)
    """
    results = crud.get_skutecznosc_klubow(db)
    return [
        {
            "nazwa_klubu": r[0],
            "punkty": r[1],
            "mecze_rozegrane": r[2],
            "bramki_strzelone": r[3],
            "bramki_stracone": r[4],
            "roznica_bramek": r[5],
            "srednia_goli": float(r[6]) if r[6] else 0.0,
            "srednia_straconych": float(r[7]) if r[7] else 0.0,
            "srednia_punktow": float(r[8]) if r[8] else 0.0
        }
        for r in results
    ]

#staty indywidualne
@app.post("/statystyki/", response_model=schemas.StatystykiIndywidualne, tags=["Statystyki"])
def create_statystyki(
    statystyki: schemas.StatystykiIndywidualneCreate, 
    db: Session = Depends(get_db)
):
    """Dodaje statystyki zawodnika z meczu"""
    return crud.create_statystyki(db=db, statystyki=statystyki)

@app.get("/statystyki/zawodnik/{zawodnik_id}", tags=["Statystyki"])
def read_statystyki_zawodnika(
    zawodnik_id: int,
    sezon: Optional[str] = Query(None, description="Filtruj według sezonu"),
    db: Session = Depends(get_db)
):
    """Pobiera statystyki zawodnika z podziałem na sezony (WF.02)"""
    return crud.get_statystyki_zawodnika(db, zawodnik_id=zawodnik_id, sezon=sezon)

#transfery
@app.post("/transfery/", response_model=schemas.Transfer, tags=["Transfery"])
def create_transfer(transfer: schemas.TransferCreate, db: Session = Depends(get_db)):
    """
    Rejestruje transfer zawodnika (WF.14, WF.18)
    Automatycznie aktualizuje klub zawodnika
    """
    return crud.create_transfer(db=db, transfer=transfer)

@app.get("/transfery/zawodnik/{zawodnik_id}", tags=["Transfery"])
def read_historia_transferow(zawodnik_id: int, db: Session = Depends(get_db)):
    """
    T5: Historia transferów zawodnika (WF.03, WF.19)
    
    Zwraca pełną historię transferów z:
    - Daty transferu
    - Klub źródłowy i docelowy
    - Kwota transferu
    - Typ transferu
    """
    results = crud.get_historia_transferow(db, zawodnik_id=zawodnik_id)
    return results

#slowniki
@app.get("/pozycje/", response_model=List[schemas.Pozycja], tags=["Słowniki"])
def read_pozycje(db: Session = Depends(get_db)):
    """Pobiera listę wszystkich pozycji"""
    return crud.get_pozycje(db)

@app.get("/menedzerowie/", response_model=List[schemas.Menedzer], tags=["Słowniki"])
def read_menedzerowie(db: Session = Depends(get_db)):
    """Pobiera listę wszystkich menedżerów"""
    return crud.get_menedzerowie(db)

@app.get("/stadiony/", response_model=List[schemas.Stadion], tags=["Słowniki"])
def read_stadiony(db: Session = Depends(get_db)):
    """Pobiera listę wszystkich stadionów"""
    return crud.get_stadiony(db)

#health check
@app.get("/health", tags=["Health"])
def health_check():
    """Sprawdza status aplikacji"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)