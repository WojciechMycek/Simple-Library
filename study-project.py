import csv
import os
from datetime import datetime


class Ksiazka:
    def __init__(self, id, tytul, autor, rok_wydania, status):
        self.id = id
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
        self.status = status


class Wypozyczenie:
    def __init__(self, id_ksiazki, numer_czytacza, czy_udana, data_wypozyczenia, data_oddania):
        self.id_ksiazki = id_ksiazki
        self.numer_czytacza = numer_czytacza
        self.czy_udana = czy_udana
        self.data_wypozyczenia = data_wypozyczenia
        self.data_oddania = data_oddania


def dodaj_ksiazke(biblioteka):
    id = str(len(biblioteka) + 1)
    tytul = input("Podaj tytuł książki: ")
    autor = input("Podaj autora książki: ")
    rok_wydania = input("Podaj rok wydania książki: ")
    status = "W bibliotece"

    ksiazka = Ksiazka(id, tytul, autor, rok_wydania, status)
    biblioteka.append(ksiazka)

    zapisz_do_csv("biblioteka.csv", biblioteka)

    print("Książka została dodana do biblioteki.")


def wypozycz_ksiazke(biblioteka, historia, czytacze):
    tytul_lub_indeks = input("Podaj tytuł lub numer indeksu książki: ")

    ksiazki_do_wypozyczenia = []
    for ksiazka in biblioteka:
        if ksiazka.tytul == tytul_lub_indeks or ksiazka.id == tytul_lub_indeks:
            ksiazki_do_wypozyczenia.append(ksiazka)

    if not ksiazki_do_wypozyczenia:
        print("Nie znaleziono książki o podanym tytule lub numerze indeksu.")
        return

    numer_czytacza = input("Podaj numer czytacza: ")
    imie = input("Podaj imię czytacza: ")
    nazwisko = input("Podaj nazwisko czytacza: ")
    data_wypozyczenia = input("Podaj datę wypożyczenia książki (RRRR-MM-DD): ")
    data_wypozyczenia = datetime.strptime(data_wypozyczenia, "%Y-%m-%d").date()

    czytacz = [czytacz for czytacz in czytacze if czytacz["Numer czytacza"] == numer_czytacza]
    if czytacz:
        czytacz = czytacz[0]
        if czytacz["Imie"] != imie or czytacz["Nazwisko"] != nazwisko:
            print("Nieprawidłowe dane czytacza.")
            historia.append(["", numer_czytacza, "Nieudane", "", "", "Nieprawidłowe dane czytacza."])
            zapisz_do_csv("historia.csv", historia)
            return
    else:
        czytacz = {"Numer czytacza": numer_czytacza, "Imie": imie, "Nazwisko": nazwisko, "Ilosc ksiazek": "0"}
        czytacze.append(czytacz)

    ksiazki_do_wypozyczenia.sort(key=lambda k: k.id)

    ksiazka = ksiazki_do_wypozyczenia[0]
    id_ksiazki = ksiazka.id

    ksiazka.status = "Nie w bibliotece"
    zapisz_do_csv("biblioteka.csv", biblioteka)

    historia.append([id_ksiazki, numer_czytacza, "Udane", data_wypozyczenia.strftime("%Y-%m-%d"), "", ""])
    zapisz_do_csv("historia.csv", historia)

    czytacz["Ilosc ksiazek"] = str(int(czytacz["Ilosc ksiazek"]) + 1)
    zapisz_do_csv("czytacze.csv", czytacze)

    print("Książka została wypożyczona.")



def oddaj_ksiazke(biblioteka, historia, czytacze):
    numer_czytacza = input("Podaj numer czytacza: ")
    tytul = input("Podaj tytuł książki: ")

    wypozyczenia = [wypozyczenie for wypozyczenie in historia if wypozyczenie.numer_czytacza == numer_czytacza and wypozyczenie.czy_udana and not wypozyczenie.data_oddania]

    if not wypozyczenia:
        print("Brak wypożyczonych książek dla podanego numeru czytacza.")
        return

    if len(wypozyczenia) == 1:
        wypozyczenie = wypozyczenia[0]
        id_ksiazki = wypozyczenie.id_ksiazki
    else:
        print("Wypożyczone książki dla podanego numeru czytacza:")
        for wypozyczenie in wypozyczenia:
            ksiazka = [ksiazka for ksiazka in biblioteka if ksiazka.id == wypozyczenie.id_ksiazki]
            if ksiazka:
                ksiazka = ksiazka[0]
                print(f"ID: {ksiazka.id}, Tytuł: {ksiazka.tytul}, Autor: {ksiazka.autor}, Rok wydania: {ksiazka.rok_wydania}")

        id_ksiazki = input("Podaj ID książki, którą chcesz zwrócić: ")

        wypozyczenie = [wypozyczenie for wypozyczenie in wypozyczenia if wypozyczenie.id_ksiazki == id_ksiazki]
        if not wypozyczenie:
            print("Nieprawidłowy numer ID książki.")
            return
        wypozyczenie = wypozyczenie[0]

    wypozyczenie.data_oddania = datetime.now().strftime("%Y-%m-%d")
    zapisz_do_csv("historia.csv", historia)

    ksiazka = [ksiazka for ksiazka in biblioteka if ksiazka.id == id_ksiazki]
    if ksiazka:
        ksiazka = ksiazka[0]
        ksiazka.status = "W bibliotece"
        zapisz_do_csv("biblioteka.csv", biblioteka)

    czytacz = [czytacz for czytacz in czytacze if czytacz["Numer czytacza"] == numer_czytacza]
    if czytacz:
        czytacz[0]["Ilosc ksiazek"] = str(int(czytacz[0]["Ilosc ksiazek"]) - 1)
        zapisz_do_csv("czytacze.csv", czytacze)

    print("Książka została zwrócona.")


def wyswietl_historie_ksiazki(historia, biblioteka):
    tytul = input("Podaj tytuł książki: ")

    ksiazki = [ksiazka for ksiazka in biblioteka if ksiazka.tytul == tytul]
    if not ksiazki:
        print("Brak książek o podanym tytule.")
        return

    for ksiazka in ksiazki:
        wypozyczenia = [wypozyczenie for wypozyczenie in historia if wypozyczenie.id_ksiazki == ksiazka.id]

        print(f"ID: {ksiazka.id}, Tytuł: {ksiazka.tytul}, Autor: {ksiazka.autor}, Rok wydania: {ksiazka.rok_wydania}")
        print("Historia wypożyczeń:")
        if wypozyczenia:
            for wypozyczenie in wypozyczenia:
                numer_czytacza = wypozyczenie.numer_czytacza
                czy_udana = "Tak" if wypozyczenie.czy_udana else "Nie"
                data_wypozyczenia = wypozyczenie.data_wypozyczenia
                data_oddania = wypozyczenie.data_oddania if wypozyczenie.data_oddania else "Nieoddana"

                print(f"Numer czytacza: {numer_czytacza}, Czy udana: {czy_udana}, "
                      f"Data wypożyczenia: {data_wypozyczenia}, Data oddania: {data_oddania}")
        else:
            print("Brak historii wypożyczeń dla tej książki.")

        print()


def zapisz_do_csv(nazwa_pliku, dane):
    try:
        with open(nazwa_pliku, mode="w", newline="", encoding="utf-8") as plik:
            writer = csv.writer(plik)
            if nazwa_pliku == "biblioteka.csv":
                writer.writerow(["ID", "Tytul", "Autor", "Rok wydania", "Status"])
            elif nazwa_pliku == "historia.csv":
                writer.writerow(["ID", "Numer czytacza", "Czy udana", "Data wypozyczenia", "Data oddania"])
            elif nazwa_pliku == "czytacze.csv":
                writer.writerow(["Numer czytacza", "Imie", "Nazwisko", "Ilosc ksiazek"])

            for rekord in dane:
                if nazwa_pliku == "historia.csv":
                    writer.writerow([rekord])
                elif isinstance(rekord, dict):
                    writer.writerow(rekord.values())
                else:
                    writer.writerow([getattr(rekord, pole) for pole in rekord.__dict__.keys()])
    except IOError:
        print(f"Błąd zapisu do pliku: {nazwa_pliku}")


def wczytaj_z_csv(nazwa_pliku):
    dane = []
    if os.path.isfile(nazwa_pliku):
        try:
            with open(nazwa_pliku, mode="r", encoding="utf-8") as plik:
                reader = csv.reader(plik)
                naglowek = next(reader)

                for wiersz in reader:
                    if nazwa_pliku == "biblioteka.csv":
                        ksiazka = Ksiazka(wiersz[0], wiersz[1], wiersz[2], wiersz[3], wiersz[4])
                        dane.append(ksiazka)
                    elif nazwa_pliku == "historia.csv":
                        wypozyczenie = Wypozyczenie(wiersz[0], wiersz[1], wiersz[2] == "True", wiersz[3], wiersz[4])
                        dane.append(wypozyczenie)
                    elif nazwa_pliku == "czytacze.csv":
                        czytacz = {
                            "Numer czytacza": wiersz[0],
                            "Imie": wiersz[1],
                            "Nazwisko": wiersz[2],
                            "Ilosc ksiazek": wiersz[3]
                        }
                        dane.append(czytacz)
        except IOError:
            print(f"Błąd odczytu pliku: {nazwa_pliku}")
    else:
        if nazwa_pliku == "biblioteka.csv":
            print("Plik biblioteka.csv nie istnieje. Tworzenie nowego pliku.")
        elif nazwa_pliku == "historia.csv":
            print("Plik historia.csv nie istnieje. Tworzenie nowego pliku.")
        elif nazwa_pliku == "czytacze.csv":
            print("Plik czytacze.csv nie istnieje. Tworzenie nowego pliku.")

    return dane


def menu():
    biblioteka = wczytaj_z_csv("biblioteka.csv")
    historia = wczytaj_z_csv("historia.csv")
    czytacze = wczytaj_z_csv("czytacze.csv")

    while True:
        print("========== MENU ==========")
        print("1. Dodaj książkę")
        print("2. Wypożycz książkę")
        print("3. Oddaj książkę")
        print("4. Wyświetl historię książki")
        print("5. Wyjście")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            dodaj_ksiazke(biblioteka)
        elif wybor == "2":
            wypozycz_ksiazke(biblioteka, historia, czytacze)
        elif wybor == "3":
            oddaj_ksiazke(biblioteka, historia, czytacze)
        elif wybor == "4":
            wyswietl_historie_ksiazki(historia, biblioteka)
        elif wybor == "5":
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


menu()
