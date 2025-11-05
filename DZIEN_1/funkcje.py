#podstawowy schemat funkcji

def pole_kwadratu(bok):
    if bok <=0:
        return "taki kwadrat nie istnieje"
    wynik = bok**2
    return wynik


print(pole_kwadratu(3))
print(pole_kwadratu(6.84))
print(pole_kwadratu(0))
print(pole_kwadratu(-3))

#funkcja bez parametrów
def przywitaj():
    print("witaj na szkoleniu z Pythona i AI!")

przywitaj()


#funkcja z wieloma argumentami
def suma(a,b,c,d):
    return a+b+c+d

print(suma(3,4,5,6))
print(suma(-3,0,11,9.34))
print(suma(d=3,b=2.3,c=7,a=0.3))

#funkcja z wartością domyślną

def poiwtanie(imie,jezyk="PL"):
    if jezyk=="PL":
        return f"Cześć {imie}!"
    elif jezyk == "EN":
        return f"Hello {imie}!"
    else:
        return f"Hi {imie}!"

print(poiwtanie("Marcin"))
print(poiwtanie("Marcin","PL"))
print(poiwtanie("Ewa","EN"))
print(poiwtanie("Ewa","FR"))

