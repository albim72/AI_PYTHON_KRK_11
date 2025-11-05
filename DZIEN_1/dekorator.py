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
