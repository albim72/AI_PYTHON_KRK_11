#dekorator logujący wywołania
def loguj(funkcja):
    def wrapper():
        print(f"wywołuję funkcję: {funkcja.__name__}")
        wynik = funkcja()
        print(f"zakończono działanie")
        return wynik
    return wrapper

@loguj
def przywitaj():
    print("Cześć!!!")

przywitaj()

#dekorator pomiaru czasu
import time

def czas(funkcja):
    def wrapper(*args, **kwargs):
        start = time.time()
        wynik = funkcja(*args, **kwargs)
        stop = time.time()
        print(f"{funkcja.__name__}: {stop-start}")
        return wynik
    return wrapper


@czas
def oblicz():
    suma=0
    for i in range(20_000_000):
        suma += i
    return suma

oblicz()
