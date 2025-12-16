README - System statystyk zawodników i klubów Premier League zbudowany w FastAPI z bazą danych MySQL.
Opis systemu

Instalacja i uruchomienie
1. Instalacja zależności
bash:	pip install -r requirements.txt
2. Konfiguracja bazy danych

Stwórz bazę danych MySQL
Edytuj plik .env zgodnie z .env.example:

DATABASE_URL=mysql+pymysql://bartek:0000@localhost:3306/premier_league
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=bartek
DATABASE_PASSWORD=0000
DATABASE_NAME=premier_league

3. Inicjalizacja bazy danych
bash:   mysql -u bartek -p < schema.sql
	mysql -u bartek -p < seed_data.sql
4. Uruchomienie aplikacji
bash:	python main.py

5. Dostęp do dokumentacji API
Po uruchomieniu aplikacji, w konsoli pojawi się link (np. http://127.0.0.1:8000)
Kliknij CTRL + Click na link
Dopisz na końcu URL: /docs
Otworzy się interaktywna dokumentacja OpenAPI (Swagger UI)


Jak korzystać z API (OpenAPI/Swagger)
Testowanie endpointów:

Wybierz interesujący endpoint (GET, POST, PUT)
Kliknij na niego, aby rozwinąć szczegóły
Kliknij przycisk "Try it out"
Wypełnij wymagane pola wartościami zgodnymi z typami danych
Kliknij "Execute"
Sprawdź odpowiedź w sekcji "Response"


Walidacje danych w systemie

1. Walidacje w schemas.py (Pydantic)
Zawodnicy (ZawodnikCreate):

			numer_koszulki: Musi być między 1 a 99

python  @validator('numer_koszulki')
  def validate_numer(cls, v):
      if v is not None and (v < 1 or v > 99):
          raise ValueError('Numer koszulki musi być między 1 a 99')
      return v
Mecze (MeczCreate):

id_klubu_goscie: Klub nie może grać sam ze sobą

python  @validator('id_klubu_goscie')
  def validate_kluby(cls, v, values):
      if 'id_klubu_gospodarze' in values and v == values['id_klubu_gospodarze']:
          raise ValueError('Klub nie może grać sam ze sobą')
      return v
Statystyki indywidualne (StatystykiIndywidualneCreate):

			minuty_rozegrane: Muszą być między 0 a 120 (z dogrywką)

python  @validator('minuty_rozegrane')
  def validate_minuty(cls, v):
      if v < 0 or v > 120:
          raise ValueError('Minuty muszą być między 0 a 120')
      return v

gole, asysty, żółte_kartki, czerwone_kartki: Nie mogą być ujemne

python  @validator('gole', 'asysty', 'zolte_kartki', 'czerwone_kartki')
  def validate_non_negative(cls, v):
      if v < 0:
          raise ValueError('Wartość nie może być ujemna')
      return v
Transfery (TransferCreate):

			typ_transferu: Musi być jednym z: 'transfer', 'wypożyczenie', 'wolny_agent'

python  @validator('typ_transferu')
  def validate_typ(cls, v):
      if v not in ['transfer', 'wypozyczenie', 'wolny_agent']:
          raise ValueError('Nieprawidłowy typ transferu')
      return v
2. Walidacje w bazie danych (schema.sql)
Kluby:

			nazwa_klubu: UNIQUE - każdy klub musi mieć unikalną nazwę
			Wartości domyślne dla statystyk: punkty, mecze_rozegrane, wygrane, remisy, przegrane, bramki = 0

Mecze:

CHECK constraint: id_klubu_gospodarze != id_klubu_goscie

Uniemożliwia stworzenie meczu, gdzie klub gra sam ze sobą


NOT NULL: data_meczu, id_klubu_gospodarze, id_klubu_goscie, sezon, kolejka

Zawodnicy:

Foreign Keys:

id_klubu → Kluby (ON DELETE SET NULL)
id_pozycji → Pozycje (ON DELETE SET NULL)



StatystykiIndywidualne:

UNIQUE KEY: unique_player_match (id_zawodnika, id_meczu)

			Każdy zawodnik może mieć tylko jeden wpis statystyk na mecz



Transfery:

ENUM: typ_transferu ∈ {'transfer', 'wypozyczenie', 'wolny_agent'}
NOT NULL: id_zawodnika, id_klubu_do, data_transferu, typ_transferu

3. Walidacje kaskadowe (Foreign Keys)
ON DELETE CASCADE:

Usunięcie meczu → usuwa wszystkie powiązane statystyki i składy
Usunięcie zawodnika → usuwa wszystkie jego statystyki i transfery
Usunięcie klubu → usuwa wszystkie mecze gdzie występował

ON DELETE SET NULL:

Usunięcie stadionu/menedżera → ustawia NULL w klubie
Usunięcie klubu źródłowego w transferze → ustawia NULL


Główne funkcjonalności API
Transakcje (automatyczne aktualizacje):
T1: Dodanie wyniku meczu z automatyczną aktualizacją statystyk
Endpoint: POST /mecze/

Dodaje wynik meczu
Automatycznie aktualizuje punkty, wygrane/remisy/przegrane
Przelicza różnicę bramek dla obu klubów
Transakcja atomowa - wszystko albo nic

T2: Ranking strzelców
Endpoint: GET /raporty/ranking-strzelcow?sezon=2024/25

Zwraca najlepszych strzelców w sezonie
Agreguje gole, asysty, minuty z wielu meczów

T3: Forma drużyny
Endpoint: GET /raporty/forma-druzyny/{klub_id}?limit=5

Pokazuje ostatnie 5 meczów klubu
Wyniki (W/R/P), bramki za/przeciw

T4: Porównanie zawodników
Endpoint: GET /raporty/porownanie-zawodnikow?pozycja_id=12&sezon=2024/25

Porównuje zawodników na tej samej pozycji
Statystyki per 90 minut

T5: Historia transferów
Endpoint: GET /transfery/zawodnik/{zawodnik_id}

Pełna historia transferów zawodnika
Chronologicznie od najnowszych

T6: Skuteczność klubów
Endpoint: GET /raporty/skutecznosc-klubow

Ranking skuteczności ofensywnej i defensywnej
Średnie gole/stracone/punkty na mecz


Przykłady użycia
Przykład 1: Dodanie nowego meczu
jsonPOST /mecze/
{
  "data_meczu": "2024-12-16T20:00:00",
  "id_klubu_gospodarze": 1,
  "id_klubu_goscie": 2,
  "bramki_gospodarze": 3,
  "bramki_goscie": 1,
  "sezon": "2024/25",
  "kolejka": 10
}
System automatycznie zaktualizuje statystyki obu klubów!

Przykład 2: Dodanie zawodnika
jsonPOST /zawodnicy/
{
  "imie": "Jan",
  "nazwisko": "Kowalski",
  "data_urodzenia": "2000-01-15",
  "narodowosc": "Polska",
  "wzrost": 185,
  "id_klubu": 1,
  "id_pozycji": 12,
  "wartosc_rynkowa": 25.00,
  "numer_koszulki": 10
}
Przykład 3: Transfer zawodnika
jsonPOST /transfery/
{
  "id_zawodnika": 25,
  "id_klubu_z": 1,
  "id_klubu_do": 2,
  "data_transferu": "2024-09-01",
  "kwota_transferu": 50.00,
  "typ_transferu": "transfer"
}
System automatycznie zmieni klub zawodnika.

Struktura projektu
.
├── app/
│   ├── __init__.py
│   ├── config.py          # Konfiguracja bazy danych
│   ├── database.py        # Połączenie z bazą
│   ├── models.py          # Modele SQLAlchemy
│   ├── schemas.py         # Schematy Pydantic (+ walidacje)
│   └── crud.py            # Operacje na bazie danych
├── main.py                # Główny plik aplikacji
├── schema.sql             # Schema bazy danych
├── seed_data.sql          # Dane testowe
├── requirements.txt       # Zależności Python
├── .env.example           # Przykład konfiguracji
└── README.txt             # Ten plik

Wsparcie techniczne
W razie problemów sprawdź:

Czy baza danych jest uruchomiona
Czy dane w .env są poprawne
Czy wszystkie tabele zostały utworzone (schema.sql)
Logi w konsoli aplikacji FastAPI


Technologie

FastAPI 0.109.0
SQLAlchemy 2.0.25
PyMySQL 1.1.0
Pydantic 2.5.3
MySQL 8.0+

