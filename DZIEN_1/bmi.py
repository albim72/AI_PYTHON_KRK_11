def bmi(wzrost,waga):
    """
    funkcja licząca bmi
    :param wzrost: w m
    :param waga: w kg
    :return: bmi
    """

    wynik = waga / (wzrost**2)

    if wynik < 18.5:
        return f"{wynik} -> niedowaga"
    elif wynik < 25:
        return f"{wynik} -> waga prawidłowa"
    elif wynik < 30:
        return f"{wynik} -> nadwaga"
    elif wynik < 35:
        return f"{wynik} -> otyłość I stopnia"
    elif wynik < 40:
        return f"{wynik} -> otyłość II stopnia"
    else:
        return f"{wynik} -> otyłość III stopnia"

wartosc = bmi(1.72,87)
print(wartosc)

wartosc2 = bmi(1.68, 122)
print(wartosc2)

wartosc3 = bmi(1.88, 82)
print(wartosc3)
