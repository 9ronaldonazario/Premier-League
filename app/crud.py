from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, text
from typing import List, Optional
from app import models, schemas
from datetime import datetime

#kluby
def get_kluby(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kluby).offset(skip).limit(limit).all()

def get_klub(db: Session, klub_id: int):
    return db.query(models.Kluby).filter(models.Kluby.id_klubu == klub_id).first()

def create_klub(db: Session, klub: schemas.KlubCreate):
    db_klub = models.Kluby(**klub.dict())
    db.add(db_klub)
    db.commit()
    db.refresh(db_klub)
    return db_klub

def update_klub(db: Session, klub_id: int, klub: schemas.KlubUpdate):
    db_klub = get_klub(db, klub_id)
    if db_klub:
        for key, value in klub.dict(exclude_unset=True).items():
            setattr(db_klub, key, value)
        db.commit()
        db.refresh(db_klub)
    return db_klub

#zawodnicy
def get_zawodnicy(db: Session, skip: int = 0, limit: int = 100, 
                  klub_id: Optional[int] = None, pozycja_id: Optional[int] = None,
                  narodowosc: Optional[str] = None):
    query = db.query(models.Zawodnicy)
    
    if klub_id:
        query = query.filter(models.Zawodnicy.id_klubu == klub_id)
    if pozycja_id:
        query = query.filter(models.Zawodnicy.id_pozycji == pozycja_id)
    if narodowosc:
        query = query.filter(models.Zawodnicy.narodowosc == narodowosc)
    
    return query.offset(skip).limit(limit).all()

def get_zawodnik(db: Session, zawodnik_id: int):
    return db.query(models.Zawodnicy).filter(
        models.Zawodnicy.id_zawodnika == zawodnik_id
    ).first()

def create_zawodnik(db: Session, zawodnik: schemas.ZawodnikCreate):
    db_zawodnik = models.Zawodnicy(**zawodnik.dict())
    db.add(db_zawodnik)
    db.commit()
    db.refresh(db_zawodnik)
    return db_zawodnik

def update_zawodnik(db: Session, zawodnik_id: int, zawodnik: schemas.ZawodnikUpdate):
    db_zawodnik = get_zawodnik(db, zawodnik_id)
    if db_zawodnik:
        for key, value in zawodnik.dict(exclude_unset=True).items():
            setattr(db_zawodnik, key, value)
        db.commit()
        db.refresh(db_zawodnik)
    return db_zawodnik

def search_zawodnicy(db: Session, search: str):
    return db.query(models.Zawodnicy).filter(
        (models.Zawodnicy.imie.contains(search)) |
        (models.Zawodnicy.nazwisko.contains(search))
    ).all()

#mecze
def get_mecze(db: Session, sezon: Optional[str] = None, kolejka: Optional[int] = None):
    query = db.query(models.Mecze)
    
    if sezon:
        query = query.filter(models.Mecze.sezon == sezon)
    if kolejka:
        query = query.filter(models.Mecze.kolejka == kolejka)
    
    return query.order_by(models.Mecze.data_meczu.desc()).all()

def get_mecz(db: Session, mecz_id: int):
    return db.query(models.Mecze).filter(models.Mecze.id_meczu == mecz_id).first()

#T1: dodanie wyniku meczu
def create_mecz_z_aktualizacja_statystyk(db: Session, mecz: schemas.MeczCreate):
    """
    T1: Dodaje wynik meczu i automatycznie aktualizuje statystyki klubow
    """
    try:
        db_mecz = models.Mecze(**mecz.dict())
        db.add(db_mecz)
        db.flush()
        
        #home club
        klub_gospodarze = db.query(models.Kluby).filter(
            models.Kluby.id_klubu == mecz.id_klubu_gospodarze
        ).first()
        
        if klub_gospodarze:
            klub_gospodarze.mecze_rozegrane += 1
            klub_gospodarze.bramki_strzelone += mecz.bramki_gospodarze
            klub_gospodarze.bramki_stracone += mecz.bramki_goscie
            klub_gospodarze.roznica_bramek += (mecz.bramki_gospodarze - mecz.bramki_goscie)
            
            if mecz.bramki_gospodarze > mecz.bramki_goscie:
                klub_gospodarze.wygrane += 1
                klub_gospodarze.punkty += 3
            elif mecz.bramki_gospodarze == mecz.bramki_goscie:
                klub_gospodarze.remisy += 1
                klub_gospodarze.punkty += 1
            else:
                klub_gospodarze.przegrane += 1
        
        #away club
        klub_goscie = db.query(models.Kluby).filter(
            models.Kluby.id_klubu == mecz.id_klubu_goscie
        ).first()
        
        if klub_goscie:
            klub_goscie.mecze_rozegrane += 1
            klub_goscie.bramki_strzelone += mecz.bramki_goscie
            klub_goscie.bramki_stracone += mecz.bramki_gospodarze
            klub_goscie.roznica_bramek += (mecz.bramki_goscie - mecz.bramki_gospodarze)
            
            if mecz.bramki_goscie > mecz.bramki_gospodarze:
                klub_goscie.wygrane += 1
                klub_goscie.punkty += 3
            elif mecz.bramki_goscie == mecz.bramki_gospodarze:
                klub_goscie.remisy += 1
                klub_goscie.punkty += 1
            else:
                klub_goscie.przegrane += 1
        
        db.commit()
        db.refresh(db_mecz)
        return db_mecz
        
    except Exception as e:
        db.rollback()
        raise e

#T2: top strzelcy
def get_ranking_strzelcow(db: Session, sezon: str, limit: int = 20):
    """
    T2: Zwraca ranking najlepszych strzelcow w sezonie
    """
    query = db.query(
        models.Zawodnicy.imie,
        models.Zawodnicy.nazwisko,
        models.Kluby.nazwa_klubu,
        func.sum(models.StatystykiIndywidualne.gole).label('suma_goli'),
        func.sum(models.StatystykiIndywidualne.asysty).label('suma_asyst'),
        func.sum(models.StatystykiIndywidualne.minuty_rozegrane).label('suma_minut'),
        func.count(func.distinct(models.StatystykiIndywidualne.id_meczu)).label('liczba_meczy')
    ).join(
        models.StatystykiIndywidualne,
        models.Zawodnicy.id_zawodnika == models.StatystykiIndywidualne.id_zawodnika
    ).join(
        models.Mecze,
        models.StatystykiIndywidualne.id_meczu == models.Mecze.id_meczu
    ).join(
        models.Kluby,
        models.Zawodnicy.id_klubu == models.Kluby.id_klubu
    ).filter(
        models.Mecze.sezon == sezon
    ).group_by(
        models.Zawodnicy.id_zawodnika,
        models.Zawodnicy.imie,
        models.Zawodnicy.nazwisko,
        models.Kluby.nazwa_klubu
    ).having(
        func.sum(models.StatystykiIndywidualne.gole) > 0
    ).order_by(
        desc('suma_goli'),
        desc('suma_asyst')
    ).limit(limit)
    
    return query.all()

#T3: forma druzyny
def get_forma_druzyny(db: Session, klub_id: int, limit: int = 5):
    """
    T3: Analizuje forme druzyny na podstawie ostatnich meczow
    """
    query = text("""
        SELECT 
            m.id_meczu,
            m.data_meczu,
            CASE
                WHEN m.id_klubu_gospodarze = :klub_id THEN 'gospodarze'
                ELSE 'goscie'
            END AS typ_meczu,
            CASE
                WHEN m.id_klubu_gospodarze = :klub_id THEN k2.nazwa_klubu
                ELSE k1.nazwa_klubu
            END AS przeciwnik,
            CASE
                WHEN m.id_klubu_gospodarze = :klub_id THEN m.bramki_gospodarze
                ELSE m.bramki_goscie
            END AS bramki_za,
            CASE
                WHEN m.id_klubu_gospodarze = :klub_id THEN m.bramki_goscie
                ELSE m.bramki_gospodarze
            END AS bramki_przeciw,
            CASE
                WHEN (m.id_klubu_gospodarze = :klub_id AND m.bramki_gospodarze > m.bramki_goscie) OR
                     (m.id_klubu_goscie = :klub_id AND m.bramki_goscie > m.bramki_gospodarze)
                THEN 'W'
                WHEN m.bramki_gospodarze = m.bramki_goscie THEN 'R'
                ELSE 'P'
            END AS wynik
        FROM Mecze m
        JOIN Kluby k1 ON m.id_klubu_gospodarze = k1.id_klubu
        JOIN Kluby k2 ON m.id_klubu_goscie = k2.id_klubu
        WHERE m.id_klubu_gospodarze = :klub_id OR m.id_klubu_goscie = :klub_id
        ORDER BY m.data_meczu DESC
        LIMIT :limit
    """)
    
    result = db.execute(query, {"klub_id": klub_id, "limit": limit})
    return result.fetchall()

#T4: porownanie zawodnikow
def get_porownanie_zawodnikow(db: Session, pozycja_id: int, sezon: str):
    """
    T4: Porownuje statystyki zawodnikow na tej samej pozycji
    """
    query = text("""
        SELECT 
            z.imie,
            z.nazwisko,
            k.nazwa_klubu,
            z.wartosc_rynkowa,
            COUNT(DISTINCT si.id_meczu) AS mecze,
            COALESCE(SUM(si.gole), 0) AS gole,
            COALESCE(SUM(si.asysty), 0) AS asysty,
            COALESCE(SUM(si.minuty_rozegrane), 0) AS minuty,
            ROUND(COALESCE(SUM(si.gole), 0) / NULLIF(SUM(si.minuty_rozegrane), 0) * 90, 2) AS gole_na_90min,
            ROUND(COALESCE(SUM(si.asysty), 0) / NULLIF(SUM(si.minuty_rozegrane), 0) * 90, 2) AS asysty_na_90min
        FROM Zawodnicy z
        JOIN Kluby k ON z.id_klubu = k.id_klubu
        LEFT JOIN StatystykiIndywidualne si ON z.id_zawodnika = si.id_zawodnika
        LEFT JOIN Mecze m ON si.id_meczu = m.id_meczu
        WHERE z.id_pozycji = :pozycja_id
        AND (m.sezon = :sezon OR m.sezon IS NULL)
        GROUP BY z.id_zawodnika, z.imie, z.nazwisko, k.nazwa_klubu, z.wartosc_rynkowa
        ORDER BY gole DESC, asysty DESC
    """)
    
    result = db.execute(query, {"pozycja_id": pozycja_id, "sezon": sezon})
    return result.fetchall()

#T5: historia transferow
def get_historia_transferow(db: Session, zawodnik_id: int):
    """
    T5: Wyswietla pelna historie transferow zawodnika
    """
    return db.query(
        models.Transfery.data_transferu,
        models.Kluby.nazwa_klubu.label('klub_z'),
        models.Kluby.nazwa_klubu.label('klub_do'),
        models.Transfery.kwota_transferu,
        models.Transfery.typ_transferu
    ).outerjoin(
        models.Kluby,
        models.Transfery.id_klubu_z == models.Kluby.id_klubu
    ).join(
        models.Kluby,
        models.Transfery.id_klubu_do == models.Kluby.id_klubu
    ).filter(
        models.Transfery.id_zawodnika == zawodnik_id
    ).order_by(
        models.Transfery.data_transferu.desc()
    ).all()

#T6: skutecznosc klubow
def get_skutecznosc_klubow(db: Session):
    """
    T6: Ranking klubow pod wzgledem skutecznosci ofensywnej i defensywnej
    """
    query = text("""
        SELECT 
            k.nazwa_klubu,
            k.punkty,
            k.mecze_rozegrane,
            k.bramki_strzelone,
            k.bramki_stracone,
            k.roznica_bramek,
            ROUND(k.bramki_strzelone / NULLIF(k.mecze_rozegrane, 0), 2) AS srednia_goli,
            ROUND(k.bramki_stracone / NULLIF(k.mecze_rozegrane, 0), 2) AS srednia_straconych,
            ROUND(k.punkty / NULLIF(k.mecze_rozegrane, 0), 2) AS srednia_punktow
        FROM Kluby k
        WHERE k.mecze_rozegrane > 0
        ORDER BY k.punkty DESC, k.roznica_bramek DESC
    """)
    
    result = db.execute(query)
    return result.fetchall()

#staty indywidualne
def create_statystyki(db: Session, statystyki: schemas.StatystykiIndywidualneCreate):
    db_stat = models.StatystykiIndywidualne(**statystyki.dict())
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

def get_statystyki_zawodnika(db: Session, zawodnik_id: int, sezon: Optional[str] = None):
    query = db.query(models.StatystykiIndywidualne).filter(
        models.StatystykiIndywidualne.id_zawodnika == zawodnik_id
    )
    
    if sezon:
        query = query.join(models.Mecze).filter(models.Mecze.sezon == sezon)
    
    return query.all()

#transfery
def create_transfer(db: Session, transfer: schemas.TransferCreate):
    db_transfer = models.Transfery(**transfer.dict())
    db.add(db_transfer)
    
    # Aktualizacja klubu zawodnika
    zawodnik = get_zawodnik(db, transfer.id_zawodnika)
    if zawodnik:
        zawodnik.id_klubu = transfer.id_klubu_do
    
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

#pozycje
def get_pozycje(db: Session):
    return db.query(models.Pozycje).all()

#menedzerowie
def get_menedzerowie(db: Session):
    return db.query(models.Menedzerowie).all()

#stadiony
def get_stadiony(db: Session):
    return db.query(models.Stadiony).all()