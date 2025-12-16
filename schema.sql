-- 1. First create the database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS premier_league CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Select/Use the database
USE premier_league;

-- 3. Now drop existing tables (if they exist)
DROP TABLE IF EXISTS StatystykiIndywidualne;
DROP TABLE IF EXISTS SkladyMeczowe;
DROP TABLE IF EXISTS Transfery;
DROP TABLE IF EXISTS Mecze;
DROP TABLE IF EXISTS Zawodnicy;
DROP TABLE IF EXISTS Kluby;
DROP TABLE IF EXISTS Stadiony;
DROP TABLE IF EXISTS Menedzerowie;
DROP TABLE IF EXISTS Pozycje;

-- Tabela Pozycje
CREATE TABLE Pozycje (
    id_pozycji INT AUTO_INCREMENT PRIMARY KEY,
    nazwa_pozycji VARCHAR(50) NOT NULL,
    skrot VARCHAR(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Menedzerowie
CREATE TABLE Menedzerowie (
    id_menedzera INT AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    narodowosc VARCHAR(50),
    data_urodzenia DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Stadiony
CREATE TABLE Stadiony (
    id_stadionu INT AUTO_INCREMENT PRIMARY KEY,
    nazwa_stadionu VARCHAR(100) NOT NULL,
    pojemnosc INT,
    miasto VARCHAR(50),
    rok_otwarcia INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Kluby
CREATE TABLE Kluby (
    id_klubu INT AUTO_INCREMENT PRIMARY KEY,
    nazwa_klubu VARCHAR(100) NOT NULL UNIQUE,
    rok_zalozenia INT,
    id_stadionu INT,
    id_menedzera INT,
    punkty INT DEFAULT 0,
    mecze_rozegrane INT DEFAULT 0,
    wygrane INT DEFAULT 0,
    remisy INT DEFAULT 0,
    przegrane INT DEFAULT 0,
    bramki_strzelone INT DEFAULT 0,
    bramki_stracone INT DEFAULT 0,
    roznica_bramek INT DEFAULT 0,
    FOREIGN KEY (id_stadionu) REFERENCES Stadiony(id_stadionu) ON DELETE SET NULL,
    FOREIGN KEY (id_menedzera) REFERENCES Menedzerowie(id_menedzera) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Zawodnicy
CREATE TABLE Zawodnicy (
    id_zawodnika INT AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    data_urodzenia DATE,
    narodowosc VARCHAR(50),
    wzrost INT,
    id_klubu INT,
    id_pozycji INT,
    wartosc_rynkowa DECIMAL(10, 2),
    numer_koszulki INT,
    FOREIGN KEY (id_klubu) REFERENCES Kluby(id_klubu) ON DELETE SET NULL,
    FOREIGN KEY (id_pozycji) REFERENCES Pozycje(id_pozycji) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Mecze
CREATE TABLE Mecze (
    id_meczu INT AUTO_INCREMENT PRIMARY KEY,
    data_meczu DATETIME NOT NULL,
    id_klubu_gospodarze INT NOT NULL,
    id_klubu_goscie INT NOT NULL,
    bramki_gospodarze INT DEFAULT 0,
    bramki_goscie INT DEFAULT 0,
    sezon VARCHAR(20) NOT NULL,
    kolejka INT NOT NULL,
    FOREIGN KEY (id_klubu_gospodarze) REFERENCES Kluby(id_klubu) ON DELETE CASCADE,
    FOREIGN KEY (id_klubu_goscie) REFERENCES Kluby(id_klubu) ON DELETE CASCADE,
    CHECK (id_klubu_gospodarze != id_klubu_goscie)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela SkladyMeczowe
CREATE TABLE SkladyMeczowe (
    id_skladu INT AUTO_INCREMENT PRIMARY KEY,
    id_meczu INT NOT NULL,
    id_zawodnika INT NOT NULL,
    id_klubu INT NOT NULL,
    w_podstawowym_skladzie BOOLEAN DEFAULT TRUE,
    minuty_rozegrane INT DEFAULT 0,
    FOREIGN KEY (id_meczu) REFERENCES Mecze(id_meczu) ON DELETE CASCADE,
    FOREIGN KEY (id_zawodnika) REFERENCES Zawodnicy(id_zawodnika) ON DELETE CASCADE,
    FOREIGN KEY (id_klubu) REFERENCES Kluby(id_klubu) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela StatystykiIndywidualne
CREATE TABLE StatystykiIndywidualne (
    id_statystyki INT AUTO_INCREMENT PRIMARY KEY,
    id_zawodnika INT NOT NULL,
    id_meczu INT NOT NULL,
    gole INT DEFAULT 0,
    asysty INT DEFAULT 0,
    zolte_kartki INT DEFAULT 0,
    czerwone_kartki INT DEFAULT 0,
    czyste_konto BOOLEAN DEFAULT FALSE,
    minuty_rozegrane INT DEFAULT 0,
    FOREIGN KEY (id_zawodnika) REFERENCES Zawodnicy(id_zawodnika) ON DELETE CASCADE,
    FOREIGN KEY (id_meczu) REFERENCES Mecze(id_meczu) ON DELETE CASCADE,
    UNIQUE KEY unique_player_match (id_zawodnika, id_meczu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela Transfery
CREATE TABLE Transfery (
    id_transferu INT AUTO_INCREMENT PRIMARY KEY,
    id_zawodnika INT NOT NULL,
    id_klubu_z INT,
    id_klubu_do INT NOT NULL,
    data_transferu DATE NOT NULL,
    kwota_transferu DECIMAL(10, 2),
    typ_transferu ENUM('transfer', 'wypozyczenie', 'wolny_agent') NOT NULL,
    FOREIGN KEY (id_zawodnika) REFERENCES Zawodnicy(id_zawodnika) ON DELETE CASCADE,
    FOREIGN KEY (id_klubu_z) REFERENCES Kluby(id_klubu) ON DELETE SET NULL,
    FOREIGN KEY (id_klubu_do) REFERENCES Kluby(id_klubu) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Indeksy dla optymalizacji zapytań
CREATE INDEX idx_zawodnicy_klub ON Zawodnicy(id_klubu);
CREATE INDEX idx_zawodnicy_pozycja ON Zawodnicy(id_pozycji);
CREATE INDEX idx_mecze_sezon ON Mecze(sezon);
CREATE INDEX idx_mecze_data ON Mecze(data_meczu);
CREATE INDEX idx_statystyki_zawodnik ON StatystykiIndywidualne(id_zawodnika);
CREATE INDEX idx_statystyki_mecz ON StatystykiIndywidualne(id_meczu);
CREATE INDEX idx_sklady_mecz ON SkladyMeczowe(id_meczu);
CREATE INDEX idx_transfery_zawodnik ON Transfery(id_zawodnika);

-- Show confirmation
SELECT 'Database and tables created successfully!' as Message;