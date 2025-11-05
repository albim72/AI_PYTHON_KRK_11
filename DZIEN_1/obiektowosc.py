class Biegacz:
    def __init__(self, imie, dystans):
        self.imie = imie
        self.dystans = dystans

    def __new__(cls, imie, dystans):
        # tu ewentualne wczesne walidacje / wzorce (singleton, immutables, cache)
        obj = super().__new__(cls)   # <- tworzy pusty obiekt
        return obj                   # MUSI zwrócić obiekt!


    def przedstaw_sie(self):
        print(f"Cześć, jestem {self.imie} i bignę {self.dystans} km.")


m = Biegacz("Marcin",67)
m.przedstaw_sie()

#modyfikacja stanu
class Licznik:
    def __init__(self):
        self.wartosc = 0

    def dodaj(self):
        self.wartosc += 1

    def pokaz(self):
        print(f"stan licznika: {self.wartosc}")

L = Licznik()
L.dodaj()
L.dodaj()
L.dodaj()
L.pokaz()
