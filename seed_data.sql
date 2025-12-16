-- Dane testowe dla systemu Premier League
USE premier_league;

-- Pozycje
INSERT INTO Pozycje (nazwa_pozycji, skrot) VALUES
('Bramkarz', 'GK'),
('Lewy stoper', 'RCB'),
('Prawy stoper', 'LCB'),
('Prawy obronca', 'RB'),
('Lewy obronca', 'LB'),
('Pomocnik defensywny', 'CDM'),
('Srodkowy pomocnik', 'CM'),
('Pomocnik ofensywny', 'CAM'),
('Prawy skrzydlowy', 'RW'),
('Lewy skrzydlowy', 'LW'),
('Falszywa 9', 'CF'),
('Napastnik', 'ST');

-- Menedżerowie
INSERT INTO Menedzerowie (imie, nazwisko, narodowosc, data_urodzenia) VALUES
('Pep', 'Guardiola', 'Hiszpania', '1971-01-18'),
('Jurgen', 'Klopp', 'Niemcy', '1967-06-16'),
('Mikel', 'Arteta', 'Hiszpania', '1982-03-26'),
('Erik', 'ten Hag', 'Holandia', '1970-02-02'),
('Mauricio', 'Pochettino', 'Argentyna', '1972-03-02');

-- Stadiony
INSERT INTO Stadiony (nazwa_stadionu, pojemnosc, miasto, rok_otwarcia) VALUES
('Etihad Stadium', 53400, 'Manchester', 2002),
('Anfield', 53394, 'Liverpool', 1884),
('Emirates Stadium', 60704, 'Londyn', 2006),
('Old Trafford', 74310, 'Manchester', 1910),
('Stamford Bridge', 40834, 'Londyn', 1877),
('Tottenham Hotspur Stadium', 62850, 'Londyn', 2019),
('St James Park', 52305, 'Newcastle', 1892),
('Villa Park', 42785, 'Birmingham', 1897);

-- Kluby
INSERT INTO Kluby (nazwa_klubu, rok_zalozenia, id_stadionu, id_menedzera, punkty, mecze_rozegrane, wygrane, remisy, przegrane, bramki_strzelone, bramki_stracone, roznica_bramek) VALUES
('Manchester City', 1880, 1, 1, 45, 18, 14, 3, 1, 52, 18, 34),
('Liverpool FC', 1892, 2, 2, 42, 18, 13, 3, 2, 48, 22, 26),
('Arsenal FC', 1886, 3, 3, 40, 18, 12, 4, 2, 45, 20, 25),
('Manchester United', 1878, 4, 4, 35, 18, 10, 5, 3, 38, 25, 13),
('Chelsea FC', 1905, 5, 5, 33, 18, 10, 3, 5, 36, 28, 8),
('Tottenham Hotspur', 1882, 6, NULL, 30, 18, 9, 3, 6, 35, 30, 5),
('Newcastle United', 1892, 7, NULL, 28, 18, 8, 4, 6, 32, 28, 4),
('Aston Villa', 1874, 8, NULL, 25, 18, 7, 4, 7, 30, 32, -2);

-- Zawodnicy
INSERT INTO Zawodnicy (imie, nazwisko, data_urodzenia, narodowosc, wzrost, id_klubu, id_pozycji, wartosc_rynkowa, numer_koszulki) VALUES
-- Manchester City
('Ederson', 'Moraes', '1993-08-17', 'Brazylia', 188, 1, 1, 40.00, 31),
('Ruben', 'Dias', '1997-05-14', 'Portugalia', 187, 1, 3, 75.00, 3),
('Kevin', 'De Bruyne', '1991-06-28', 'Belgia', 181, 1, 8, 100.00, 17),
('Erling', 'Haaland', '2000-07-21', 'Norwegia', 194, 1, 12, 180.00, 9),
('Phil', 'Foden', '2000-05-28', 'Anglia', 171, 1, 8, 110.00, 47),
-- Liverpool
('Alisson', 'Becker', '1992-10-02', 'Brazylia', 193, 2, 1, 60.00, 1),
('Virgil', 'van Dijk', '1991-07-08', 'Holandia', 195, 2, 3, 50.00, 4),
('Mohamed', 'Salah', '1992-06-15', 'Egipt', 175, 2, 11, 65.00, 11),
('Darwin', 'Nunez', '1999-06-24', 'Urugwaj', 187, 2, 12, 70.00, 9),
('Trent', 'Alexander-Arnold', '1998-10-07', 'Anglia', 180, 2, 4, 80.00, 66),
-- Arsenal
('Aaron', 'Ramsdale', '1998-05-14', 'Anglia', 188, 3, 1, 30.00, 1),
('Gabriel', 'Magalhaes', '1997-12-19', 'Brazylia', 190, 3, 3, 50.00, 6),
('Martin', 'Odegaard', '1998-12-17', 'Norwegia', 178, 3, 8, 85.00, 8),
('Bukayo', 'Saka', '2001-09-05', 'Anglia', 178, 3, 11, 120.00, 7),
('Gabriel', 'Jesus', '1997-04-03', 'Brazylia', 175, 3, 12, 75.00, 9),
-- Manchester United
('Andre', 'Onana', '1996-04-02', 'Kamerun', 190, 4, 1, 45.00, 24),
('Raphael', 'Varane', '1993-04-25', 'Francja', 191, 4, 3, 40.00, 19),
('Bruno', 'Fernandes', '1994-09-08', 'Portugalia', 179, 4, 8, 80.00, 8),
('Marcus', 'Rashford', '1997-10-31', 'Anglia', 180, 4, 11, 85.00, 10),
('Rasmus', 'Hojlund', '2003-02-04', 'Dania', 191, 4, 12, 65.00, 11),
-- Chelsea
('Robert', 'Sanchez', '1997-11-18', 'Hiszpania', 197, 5, 1, 30.00, 1),
('Thiago', 'Silva', '1984-09-22', 'Brazylia', 183, 5, 3, 5.00, 6),
('Enzo', 'Fernandez', '2001-01-17', 'Argentyna', 178, 5, 7, 75.00, 5),
('Cole', 'Palmer', '2002-05-06', 'Anglia', 189, 5, 8, 80.00, 20),
('Nicolas', 'Jackson', '2001-06-20', 'Senegal', 185, 5, 12, 35.00, 15);

-- Mecze
INSERT INTO Mecze (data_meczu, id_klubu_gospodarze, id_klubu_goscie, bramki_gospodarze, bramki_goscie, sezon, kolejka) VALUES
('2024-08-16 20:00:00', 1, 5, 2, 0, '2024/25', 1),
('2024-08-17 17:30:00', 2, 3, 3, 1, '2024/25', 1),
('2024-08-17 15:00:00', 4, 6, 1, 0, '2024/25', 1),
('2024-08-24 20:00:00', 3, 7, 2, 0, '2024/25', 2),
('2024-08-24 17:30:00', 5, 2, 0, 2, '2024/25', 2),
('2024-08-25 16:30:00', 6, 1, 1, 2, '2024/25', 2),
('2024-08-31 15:00:00', 1, 3, 2, 2, '2024/25', 3),
('2024-08-31 17:30:00', 2, 4, 3, 0, '2024/25', 3),
('2024-09-01 14:00:00', 7, 6, 2, 1, '2024/25', 3);

-- StatystykiIndywidualne
INSERT INTO StatystykiIndywidualne (id_zawodnika, id_meczu, gole, asysty, zolte_kartki, czerwone_kartki, czyste_konto, minuty_rozegrane) VALUES
-- Mecz 1: Man City 2-0 Chelsea
(4, 1, 2, 0, 0, 0, FALSE, 90),
(3, 1, 0, 1, 0, 0, FALSE, 90),
(1, 1, 0, 0, 0, 0, TRUE, 90),
-- Mecz 2: Liverpool 3-1 Arsenal
(8, 2, 2, 0, 0, 0, FALSE, 90),
(9, 2, 1, 1, 0, 0, FALSE, 75),
(14, 2, 1, 0, 1, 0, FALSE, 90),
(6, 2, 0, 0, 0, 0, FALSE, 90),
-- Mecz 3: Man United 1-0 Tottenham
(19, 3, 1, 0, 0, 0, FALSE, 90),
(16, 3, 0, 0, 0, 0, TRUE, 90),
-- Mecz 4: Arsenal 2-0 Newcastle
(14, 4, 1, 1, 0, 0, FALSE, 90),
(15, 4, 1, 0, 0, 0, FALSE, 85),
-- Mecz 5: Chelsea 0-2 Liverpool
(8, 5, 1, 0, 0, 0, FALSE, 90),
(9, 5, 1, 1, 0, 0, FALSE, 90),
(6, 5, 0, 0, 0, 0, TRUE, 90);

-- Transfery
INSERT INTO Transfery (id_zawodnika, id_klubu_z, id_klubu_do, data_transferu, kwota_transferu, typ_transferu) VALUES
(4, NULL, 1, '2022-07-01', 60.00, 'transfer'),
(9, NULL, 2, '2022-06-14', 75.00, 'transfer'),
(20, 1, 4, '2023-07-01', 72.00, 'transfer'),
(15, 1, 3, '2022-07-01', 45.00, 'transfer'),
(25, NULL, 5, '2023-09-01', 30.00, 'transfer');