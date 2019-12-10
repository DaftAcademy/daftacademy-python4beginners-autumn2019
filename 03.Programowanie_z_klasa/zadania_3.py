"""
W tym zadaniu zawsze będą poprawne dane.
Nie ma potrzeby obsługiwania sytuacji wyjątkowych.
Napisz klasę MyPolynomial → https://pl.wikipedia.org/wiki/Wielomian
Ta klasa ma reprezentować wielomian.
Ta klasa ma być mutowalna.
Ta klasa ma mieć jedno pole `prywatne`(prywatne przez konwencję). Nazwa pola - dowolna


1. Instancję klasy MyPolynomial powinno dać się utworzyć na następujące sposoby
(Po znaku komentarza jest opis, jak należy interpretować wartości wewnątrz):
    MyPolynomial()  # 0
    MyPolynomial(1)  # 1
    MyPolynomial(1, 2)  # 1 + 2x
    MyPolynomial(1, 2, 3)  # 1 + 2x + 3x^2


2. Instancje klasy MyPolynomial powinno dać się rzutować na string, zaimplementuj odpowiednie metody,
w taki sposób, żeby polecenie str na obiekcie MyPolynomial(1,2,3) zwracało '1 + 2x + 3x^2'. Metoda reprezentacyjna(repr) dla MyPolynomial, powina zwracać strig w takiej postaci, żeby przeklejony do konsoli interpretera (bez '') mógł stworzyć obiekt o identycznej strukturze.

Przyklady:

    '1 + 2x^1' == str(MyPolynomial(1, 2))
    '1 + 1x^1 + 2x^2' == str(MyPolynomial(1, 1, 2))
    'MyPolynomial(1, 2)' == repr(MyPolynomial(1, 2))


3. Instancję obiektu klasy MyPolynomial powinniśmy móc wywołać z argumentem x.
Podobnie jak w matematyce piszemy:
w(x) = 1 + 2x  + 2x^2, kiedy podstawimy za x 2 mamy w(2), chcielibyśmy otrzymać wynik:
w(2) = 1 + 2*2 + 2*2^2 = 13

Przykład:

w = MyPolynomial(1, 2, 2)
w(2) == 13  # powinno zwrócić True



4. Nasze wielomiany powinno dać się porównywać, tak jak w przykładzie:

    MyPolynomial(5) == MyPolynomial(5, 1)  # powinno zwrócić False
    MyPolynomial() == MyPolynomial(0)  # powinno zwrócić True



5. Tworzenie obiektu MyPolynomial metodą from_iterable(iterable)

Przykłady:

    MyPolynomial.from_iterable([0, 1, 2]) == MyPolynomial(0, 1, 2)
    MyPolynomial.from_iterable((0, 1, 2)) == MyPolynomial(0, 1, 2)



6. Klasa MyPolynomial powinna mieć zaimplementowaną metodę degree, która zwraca stopień wielomianu.

Przykłady:

    MyPolynomial(5, 4).degree() == 1  # powinna zwrócić True
    MyPolynomial().degree() == 0  # powinna zwrócić True


7. Wielomiany powinno dać się do siebie dodać.

Przykłady:

    MyPolynomial(5, 8) == MyPolynomial(2, 4) + MyPolynomial(3, 4)
    mp1 = MyPolynomial(2, 4)
    mp2 = MyPolynomial(3, 4)
    mp3 = MyPolynomial(5, 8)
    mp1 += mp2
    mp3 == mp1



8. Wielomiany powinno dać się pomnożyć(*, *=), zarówno przez wielomian, jak i przez liczbę.
    MyPolynomial(6, 14, 8) == MyPolynomial(2, 2) * MyPolynomial(3, 4)
    MyPolynomial(6, 14, 8) == MyPolynomial(3, 7, 4) * 2
    MyPolynomial(6, 14, 8) == 2 * MyPolynomial(3, 7, 4)

"""


from itertools import zip_longest


class MyPolynomial:
    def __init__(self, *args):
        if not args:
            args = [0]

        self.__coefs = self._truncate_zeros(*args)

    def _truncate_zeros(self, *args):
        i = len(args)

        while i > 1 and args[i - 1] == 0:
            i -= 1

        return list(args[:i])

    @classmethod
    def from_iterable(cls, iterable):
        return cls(*iterable)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(repr(x) for x in self)})"

    def __str__(self):
        st = ""
        for exp, coef in enumerate(self):
            if exp == 0:
                st += repr(coef)
                continue
            if coef == 0:
                continue
            # a co z ujemnymi?
            st += f" + {coef}x^{exp}"
        return st

    def __getitem__(self, idx):
        return self.__coefs[idx]

    def __len__(self):
        return len(self.__coefs)

    def __eq__(self, other):
        if len(self) != len(other):
            if len(other) == 0 and self[0] == 0:
                return True
            return False
        return all(i == j for i, j in zip(self, other))

    def __call__(self, x):
        return sum([x ** exp * coef for exp, coef in enumerate(self)])

    def __add__(self, other):
        res = [sum(t) for t in zip_longest(self, other, fillvalue=0)]
        return MyPolynomial(*res)

    def __iadd__(self, other):
        res = [sum(t) for t in zip_longest(self, other, fillvalue=0)]
        self.__coefs = self._truncate_zeros(*res)
        return self

    def __radd__(self, other):
        return self + other

    def _inner_mul(self, other):
        new_len = len(self) + len(other) - 1
        new_coefs = [0] * new_len
        computation_matrix = [[0] * len(self) for _ in range(len(other))]

        for o_i, o in enumerate(other):
            for s_i, s in enumerate(self):
                computation_matrix[o_i][s_i] = o * s

        for o_i in range(len(other)):
            for s_i in range(len(self)):
                new_coefs[o_i + s_i] += computation_matrix[o_i][s_i]

        coefs = self._truncate_zeros(*new_coefs)
        return coefs

    def __mul__(self, other):
        if type(other) != type(self):
            new_coefs = [x * other for x in self.__coefs]
            return MyPolynomial(*new_coefs)

        new_coefs = self._inner_mul(other)
        return MyPolynomial(*new_coefs)

    def __imul__(self, other):
        if type(other) != type(self):
            new_coefs = [x * other for x in self.__coefs]
            self.__coefs = self._truncate_zeros(*new_coefs)
            return self

        self.__coefs = self._inner_mul(other)
        return self

    def __rmul__(self, other):
        return self * other

    def degree(self):
        return len(self) - 1


print("Zadanie 1")
assert type(MyPolynomial()) is MyPolynomial
assert type(MyPolynomial(1)) is MyPolynomial
assert type(MyPolynomial(1, 2)) is MyPolynomial
assert type(MyPolynomial(0, 0)) is MyPolynomial
assert any(
    name.startswith("_") and not callable(name)
    for name in MyPolynomial().__dict__.keys()
)
import ipdb  # Warto zobaczyć co to i jak używać

ipdb.sset_trace()

print("Zadanie 2")
assert "1 + 2x^1" == str(MyPolynomial(1, 2))
assert "MyPolynomial(1, 2)" == repr(MyPolynomial(1, 2))
assert "MyPolynomial(0)" == repr(MyPolynomial())
assert "MyPolynomial(0)" == repr(MyPolynomial(0, 0, 0))
assert "0" == str(MyPolynomial(0, 0, 0))


print("Zadanie 3")
assert MyPolynomial(1, 2, 2)(0) == 1
assert MyPolynomial(1, 2, 2)(1) == 5
assert MyPolynomial(1, 2, 2)(2) == 13
assert MyPolynomial(1, 2, 2)(3) == 25
assert MyPolynomial(1, 2, 2)(4) == 41

print("Zadanie 4")
assert MyPolynomial(1, 2, 2) == MyPolynomial(1, 2, 2)
assert (MyPolynomial(1, 2, 2) == MyPolynomial(1, 2)) is False
assert MyPolynomial(0) == MyPolynomial()
assert MyPolynomial(0, 0) == MyPolynomial(0)
assert MyPolynomial(0, 0, 0) == MyPolynomial(0)
assert MyPolynomial(1, 0, 0) == MyPolynomial(1)
assert MyPolynomial(0, 1, 0) == MyPolynomial(0, 1)
assert MyPolynomial(0, 1, 1) == MyPolynomial(0, 1, 1)


print("Zadanie 5")
assert MyPolynomial.from_iterable([0, 1, 2]) == MyPolynomial(0, 1, 2)
assert MyPolynomial.from_iterable((0, 1, 2)) == MyPolynomial(0, 1, 2)
assert MyPolynomial.from_iterable([1, 2, 2]) == MyPolynomial(1, 2, 2)
assert (MyPolynomial.from_iterable((1, 2, 2)) == MyPolynomial(1, 2)) is False
assert MyPolynomial.from_iterable([0]) == MyPolynomial()
assert MyPolynomial.from_iterable([0, 0]) == MyPolynomial(0)
assert MyPolynomial.from_iterable(set([0, 0, 0])) == MyPolynomial(0)

print("Zadanie 6")
assert MyPolynomial(5, 4).degree() == 1
assert MyPolynomial().degree() == 0
assert MyPolynomial(0, 0, 0).degree() == 0
assert MyPolynomial(0, 1, 0).degree() == 1
assert MyPolynomial(0, 0, 1).degree() == 2
assert MyPolynomial.from_iterable([0, 1, 0]).degree() == 1


print("Zadanie 7")
assert MyPolynomial(5, 8) == MyPolynomial(2, 4) + MyPolynomial(3, 4)
assert MyPolynomial(5, 4) == MyPolynomial(2) + MyPolynomial(3, 4)
assert MyPolynomial(6, 4) == MyPolynomial(2, 4) + MyPolynomial(4)

mp1 = MyPolynomial(2, 4)
old_id = id(mp1)
mp2 = MyPolynomial(3, 4)
mp3 = MyPolynomial(5, 8)
mp1 += mp2
new_id = id(mp1)
assert mp3 == mp1
assert old_id == new_id, "After +=, you returned different object!"


print("Zadanie 8")
assert MyPolynomial(6, 14, 8) == MyPolynomial(2, 2) * MyPolynomial(3, 4)
assert MyPolynomial(9, 6, 13, 4, 4) == MyPolynomial(3, 1, 2) * MyPolynomial(3, 1, 2)
assert MyPolynomial(16, 24, 25, 20, 10, 4, 1) == MyPolynomial(
    4, 3, 2, 1
) * MyPolynomial(4, 3, 2, 1)
assert MyPolynomial(1, 4, 7, 10, 8) == MyPolynomial(1, 2) * MyPolynomial(1, 2, 3, 4)
assert MyPolynomial(1, 4, 7, 10, 8) == MyPolynomial(1, 2, 3, 4) * MyPolynomial(1, 2)
assert MyPolynomial(6, 14, 8) == MyPolynomial(3, 7, 4) * 2
assert MyPolynomial(9, 21, 12) == 3 * MyPolynomial(3, 7, 4)


mp1 = MyPolynomial(3, 7, 4)
mp1_old_id = id(mp1)
mp2 = MyPolynomial(0)
mp1 *= mp2
mp1_new_id = id(mp1)
assert mp1 == mp2, "Something went wrong with: MyPolynomial * MyPolynomial"
assert mp1_old_id == mp1_new_id, "After *=, you returned different object!"

mp1 = MyPolynomial(3, 7, 4)
mp1_old_id = id(mp1)
mp1 *= 0
mp1_new_id = id(mp1)
assert mp1 == MyPolynomial(0), "Something went wrong with: MyPolynomial *= number"
assert mp1_old_id == mp1_new_id, "After *=, you returned different object!"


print("TEST")
my = MyPolynomial(1, 2, 2)
print("{}:{}".format(id(my), my))
my2 = MyPolynomial(1, 2, 3, 4)
print("{}:{}".format(id(my2), my2))
my3 = my + my2
print("{}:{}".format(id(my3), my3))
my4 = my + [1, 2, 3, 4]
print("{}:{}".format(id(my4), my4))
my5 = [1, 2, 3, 4] + my
print("{}:{}".format(id(my5), my5))
my6 = MyPolynomial()
print("{}:{}".format(id(my6), my6))
my6 += my
print("{}:{}".format(id(my6), my6))
print(my(2))
my7 = MyPolynomial(-1, -2, -2)
print("{}:{}".format(id(my7), my7))
