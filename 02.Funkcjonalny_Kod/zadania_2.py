import collections
import ipdb
import re
import string

from collections import Counter

pan_tadeusz = ""  # do pobrania z projektu Gutenberg

# Zadanie 1
# Napisz funkcję power, która dla danego n i p zwraca w wyniku n podniesione do
# potęgi p.
# Domyślna wartość argumentu p to 3.
# Niech n i p będą liczbami całkowitymi >= 0.


def power(n, p=3):
    return n ** p


assert power(5) == 125
assert power(5, 3) == 125
assert power(0, 0) == 1
assert power(0) == 0


# Zadanie 2
# Napisz funkcję fold.
# Funkcja ma na celu mnożenie kolejnych par elementów zadanej listy i
# zwrócenie listy iloczynów kolejnych par.
# Jeżeli listy wejściowe są nierówne, na ostatnich pozycjach listy wyjściowej
# powinny znaleźć się 0. Tyle 0, ile jest różnicy między listami.


# Tego jak obsłużyć niepoprawny dane, czy to z wejścia, czy też powstawe
# podczas ich przetwarzania, dowiecie się na wykładzie 4
def fold(a=None, b=None):
    if not a:
        a = []
    if not b:
        b = []
    res = [_a * _b for _a, _b in zip(a, b)]
    diff = abs(len(a) - len(b))
    res.extend([0] * diff)
    return res


assert fold(None, None) == []
assert fold([1, 2, 3], [1, 2, 3]) == [1, 4, 9]
assert fold([1, 2], [1, 2, 3]) == [1, 4, 0]
assert fold(None, [1, 2, 3]) == [0, 0, 0]
assert fold([1, 2, 3], None) == [0, 0, 0]


# Zadanie 3
# Napisz funkcję word_frequency, która przyjmuje jako argument string.
# Dla podanego stringa funkcja musi zliczyć ile razy wystąpił każdy wyraz.
# Zwróc wynik jako słownik wartości ile razy wystąpił każdy wyraz, gdzie klucz
# to występujący wyraz a wartścią jest liczba wystąpień tego wyrazu.


# Poniżej zbiór różnych rozwiązań, pierwsze z góry poprawne,
# ale do słów zalicza takie_słowa.
# Niektóre rozwiązania są nieefektywne oblliczeniowo,
# ale generalnie rozwiązują problem.
def word_frequency(text=None):
    if not text:
        return {}
    return dict(Counter(re.sub(r"[\W]", " ", text).split()))


def word_frequency2(s=""):
    for c in string.punctuation:
        s = s.replace(c, " ")
    wordlist = s.split()
    wordfreq = [wordlist.count(w) for w in wordlist]
    return dict(zip(wordlist, wordfreq))


def word_frequency3(words=""):
    lista = re.split(r"\W", words)
    slownik = {}
    for x in lista:
        slownik[x] = lista.count(x)
        continue
    return slownik


def word_frequency4(stri=""):
    result = {}
    for word in stri.split(" "):
        if word.isalnum():
            if word not in result:
                result[word] = 0
            result[word] += 1
    return result


def word_frequency5(string=""):
    if string == "":
        return {}
    else:
        string1 = re.split("\W+", string)
        cnt = dict(collections.Counter(string1))
        return cnt


def word_frequency6(txt=""):
    print(txt)
    print(len(txt))
    if txt[len(txt) - 1] == " ":
        txt = txt[0 : len(txt) - 1]
    txt_bez_znakow_specjalnych = re.sub(r"[^\w]", "_", txt)
    txt_bez_znakow_specjalnych = re.sub(r"(_+)", " ", re.sub(r"[^\w]", "_", txt))
    txt_lista = re.split(" ", txt_bez_znakow_specjalnych)
    slownik = dict(collections.Counter(txt_lista))
    return slownik


def word_frequency7(string=""):
    string = replacer(
        string, [".", ",", "-", ";", ":", "'", "\\", "?", "!", '"', "\n", "(", ")"], " "
    )
    s_arr = string.split(" ")
    result = {}
    for el in s_arr:
        if el not in result.keys():
            result[el] = 1
        else:
            result[el] += 1
    if "" in result.keys():
        del result[""]
    return result


def word_frequency8(twoje_wyrazy=None):
    twoje_wyrazy = twoje_wyrazy if twoje_wyrazy else ""
    z = twoje_wyrazy
    delimiters = [" ", "-", "\n", "–", "'", ":", ";", "!", ".", ","]

    regexPattern = "|".join(map(re.escape, delimiters))
    z = re.split(regexPattern, z)
    i = 0
    while i < len(z):
        z[i] = re.sub("[^A-Za-z0-9ęćąółżźńśĘĆĄÓŁŻŹŃŚÉ]", "", z[i])
        i = i + 1
    z = list(filter(("").__ne__, z))

    slownik = {}
    for wyraz in z:
        slownik[wyraz] = slownik.get(wyraz, 0) + 1
    return slownik


result = word_frequency(pan_tadeusz)
result2 = word_frequency2(pan_tadeusz)
result3 = word_frequency3(pan_tadeusz)
result4 = word_frequency4(pan_tadeusz)
result5 = word_frequency5(pan_tadeusz)
result6 = word_frequency6(pan_tadeusz)
try:
    result7 = word_frequency7(pan_tadeusz)
except:
    result7 = {}
result8 = word_frequency8(pan_tadeusz)

ipdb.sset_trace()

# Zadanie 4
# Napisz funkcję hexagonal_list, która dla danego n obliczy n liczb ciągu
# hexagonal number series → https://edublognss.wordpress.com/2013/04/16/famous-mathematical-sequences-and-series/
# Załóż, że n >= 1 i jest liczbą całkowitą


def hexagonal_list(n):
    result = []
    for i in range(1, n + 1):
        result.append((2 * i * (2 * i - 1)) // 2)
    return result


# ZADANIE 5
# Napisz funkcję doskonale, ktora zwraca listę wszystich liczb doskonałych
# mniejszych bądź równych zadanemu n
# Wewnątrz, stwórz funkcję suma_dzielnikow, która zwraca sumę
# dzielników właściwych zadanej liczby


# To rozwiązanie nawiązuje swoją budową (funkcją suma_dzielników w funkcji doskonale)
# do struktury dekoratora:
# https://realpython.com/primer-on-python-decorators/
# Dekoratory są omawiane na drugiej edycji kursu


def doskonale(n):
    def suma_dzielnikow(k):
        suma = 0
        for i in range(1, k // 2 + 1):
            if k % i == 0:
                suma += i
        return suma

    result = []
    for k in range(1, n + 1):
        suma = suma_dzielnikow(k)
        if k == suma:
            result.append(k)
    return result
