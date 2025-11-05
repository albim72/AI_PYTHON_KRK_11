#generator liczb
def licz_do(n):
    i=1
    while i<=n:
        yield i
        i+=1


print(list(licz_do(100)))
for licz in licz_do(100):
    print(licz)

#generator przetwarzający dane w strumieniu

def dlugie_slowa(lista, min_dlugosc):
    for slowo in lista:
        if len(slowo)>=min_dlugosc:
            yield slowo

miasta = ["Kraków","Lublin","Płock","Wrocław","Katowice","Poznań","Jelenia Góra"]

for slowo in dlugie_slowa(miasta, 8):
    print(slowo)
