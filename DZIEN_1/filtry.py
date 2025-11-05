def filtruj_dluzsze(lista, min_dlugosc):
    wynik = []
    for slowo in lista:
        if len(slowo) >= min_dlugosc:
            wynik.append(slowo)

    return wynik


miasta = ["Kraków","Lublin","Płock","Wrocław","Katowice"]
print(filtruj_dluzsze(miasta,3))
print(filtruj_dluzsze(miasta,7))

def filtruj(lista, min_dlugosc):
    return [x for x in lista if len(x)>=min_dlugosc]

print(filtruj_dluzsze(miasta,4))
print(filtruj_dluzsze(miasta,8))
