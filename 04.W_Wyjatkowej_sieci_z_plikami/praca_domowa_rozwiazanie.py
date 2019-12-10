u"""Praca domowa.

Zadanie 1:
Rozszerzyć modelową lub własną implementację klasy MyPolynomial.
Dodać:
    obsługę liczb ujemnych
    odejmowanie z liczbą
    odejmowanie wielomianów klasy MyPolynomial

    '-1 - 2x' == str(MyPolynomial(-1, -2))
    '1x - 2x^2' == str(MyPolynomial(0, 1, -2))
    'MyPolynomial(-1, -2)' == repr(MyPolynomial(-1, -2))

    MyPolynomial(2, 4) == MyPolynomial(5, 8) - MyPolynomial(3, 4)
    MyPolynomial(-1) == MyPolynomial(2, 4) -= MyPolynomial(3, 4)
    MyPolynomial(0, 2, 3) == MyPolynomial(0, 2, 3) - 1


Zadanie 2:
Klasa MyPolynomial powinna też obsługiwać dzielenie przez liczbę
    MyPolynomial(6, 14, 8) == MyPolynomial(12, 28, 16) / 2

Zadanie 3:
Dane wejściowe Tworzenia klasy MyPolynomial mogą nie być poprawne.
Z tego powodu klasa MyPolynomial powinna walidować wejściowe parametry i ich poprawność.
By to osiągnąć zaimplementuj następujące wyjątki:
    InvalidOperandError
    InvalidInputOperandError
    OperationNotSupportedError

Przykład:
    MyPolynomial(5, 4) + "10" #  <- ten test ma rzucić wyjątkiem InvalidOperand
    MyPolynomial(5, [12])     #  <- ten test ma rzucić wyjątkiem InvalidInputOperand
    MyPolynomial(99, 100)**2  #  <- ten test ma rzucić wyjątkiem OperationNotSupported


Pamiętaj jednak że wszystkie dotychczasowej operacje na MyFraction z Zadań 3.1 - 3.8
powinny wciąż działać.
"""

from itertools import zip_longest
from collections import defaultdict
import unittest


class GenericPolynomialError(Exception):
    """Base exception for all Polynomial exceptions."""

    pass


class InvalidOperandError(GenericPolynomialError):
    """Trhow this exception when Invalid Operand."""

    pass


class InvalidInputOperandError(GenericPolynomialError):
    """Trhow this exception when Invalid Input."""

    pass


class OperationNotSupportedError(GenericPolynomialError):
    """Trhow this exception when Invalid Operation on object."""

    pass


class MyPolynomial:
    """MyPolynomial class definition."""

    def __init__(self, *args):
        """Init."""
        for arg in args:
            self._supported_input(arg)

        if not args:
            self.__coefs = [0]
        elif any(map(lambda x: isinstance(x, MyPolynomial), args)):
            new_args = defaultdict(int)
            for i, x in enumerate(args):
                if isinstance(x, MyPolynomial):
                    for j, y in enumerate(x):
                        new_args[i + j] += y
                else:
                    new_args[i] += x
            self.__coefs = self._truncate_zeros(*new_args.values())
        else:
            self.__coefs = self._truncate_zeros(*args) if len(args) else args

    def _supported_operand(self, other):
        if not isinstance(other, (int, float, MyPolynomial)) or isinstance(other, bool):
            raise InvalidOperandError

    def _supported_digit_operand(self, other):
        if not isinstance(other, (int, float)) or isinstance(other, bool):
            raise InvalidOperandError

    def _supported_input(self, other):
        if not isinstance(other, (int, float, MyPolynomial)) or isinstance(other, bool):
            raise InvalidInputOperandError

    def _truncate_zeros(self, *args):
        i = len(args)

        while i > 1 and args[i - 1] == 0:
            i -= 1

        return list(args[:i])

    @classmethod
    def from_iterable(cls, iterable):
        """Create MyPolynomial Object from given iterable object."""
        return cls(*iterable)

    def __repr__(self):
        """Return stringified repr of a MyPolynomial class object."""
        return "MyPolynomial{})".format(str(tuple(self.__coefs)).rstrip(',)'))

    def __floordiv__(self, other):
        """Operation not yet supported for MyPolynomial."""
        raise OperationNotSupportedError("Operator // is not yet supported")

    def __pow__(self, other):
        """Operation not yet supported for MyPolynomial."""
        raise OperationNotSupportedError("Operator ** is not yet supported")

    def __lshift__(self, other):
        """Operation not yet supported for MyPolynomial."""
        raise OperationNotSupportedError("Operator << is not yet supported")

    def __rshift__(self, other):
        """Operation not yet supported for MyPolynomial."""
        raise OperationNotSupportedError("Operator >> is not yet supported")

    def __str__(self):
        """Return stringified MyPolynomial object represention."""
        printable = list()
        for i, x in enumerate(self):
            if x > 0:
                if i == 0:
                    printable.append(str(x))
                else:
                    printable.append(" + {x}x^{i}".format(x=x if x != 1 else '', i=i))
            if x < 0:
                if i == 0:
                    printable.append(str(x))
                else:
                    printable.append(" - {x}x^{i}".format(x=abs(x) if abs(x) != 1 else '', i=i))
            if x == 0 and len(self) == 1:
                printable.append('0')

        return "".join(printable)

    def degree(self):
        """Retrurn a degree of a MyPolynomial polynomainal."""
        return len(self) - 1

    def _inner_mul(self, other):
        new_len = len(self) + len(other) - 1
        new_coefs = [0] * new_len
        computaion_matrix = [[0] * len(self) for _ in range(len(other))]

        for o_i, o in enumerate(other):
            for s_i, s in enumerate(self):
                computaion_matrix[o_i][s_i] = o * s

        for o_i in range(len(other)):
            for s_i in range(len(self)):
                new_coefs[o_i + s_i] += computaion_matrix[o_i][s_i]

        coefs = self._truncate_zeros(*new_coefs)
        return coefs

    def __getitem__(self, idx):
        """Return item by index from MyPolynomial coeficients - list like."""
        return self.__coefs[idx]

    def __len__(self):
        """Return lenght of MyPolynomial coeficients."""
        return len(self.__coefs)

    def __eq__(self, other):
        """Return boolean value for comparing polymonals and digits."""
        if type(other) != type(self):
            raise InvalidOperandError

        if len(self) != len(other):
            return False
        return all(i == j for i, j in zip(self, other))

    def __call__(self, x):
        """Return calculated value of a polynomainal."""
        self._supported_digit_operand(x)
        return sum([x ** exp * coef for exp, coef in enumerate(self)])

    def __neg__(self):
        """Return negated self."""
        new_coefs = [-x for x in self.__coefs]
        for i, x in enumerate(new_coefs):
            self.__coefs[i] = x
        return self

    def __add__(self, other):
        """Retrurn new MyPolynomial object added with annother one."""
        self._supported_operand(other)
        if type(other) == type(self):
            res = [sum(t) for t in zip_longest(self, other, fillvalue=0)]
            return MyPolynomial(*res)

        return MyPolynomial(other) + self

    def __iadd__(self, other):
        """Add other to self."""
        self._supported_operand(other)
        if type(other) == type(self):
            res = [sum(t) for t in zip_longest(self, other, fillvalue=0)]
            self.__coefs = self._truncate_zeros(*res)
        else:
            self[0] += other
        return self

    def __radd__(self, other):
        """Retrurn new MyPolynomial object added with other as r operand."""
        return self + other

    def __mul__(self, other):
        """Retrurn new MyPolynomial object multipied by other."""
        self._supported_operand(other)
        if type(other) != type(self):
            new_coefs = [x * other for x in self.__coefs]
            return MyPolynomial(*new_coefs)

        new_coefs = self._inner_mul(other)
        return MyPolynomial(*new_coefs)

    def __imul__(self, other):
        """Multiply self by other."""
        self._supported_operand(other)
        if type(other) != type(self):
            new_coefs = [x * other for x in self.__coefs]
            self.__coefs = self._truncate_zeros(*new_coefs)
            return self

        self.__coefs = self._inner_mul(other)
        return self

    def __rmul__(self, other):
        """Retrurn new MyPolynomial object multipied by other as r operand."""
        return self * other

    def __coef(self, idx):
        if idx < len(self):
            return self.__coefs[idx]
        return 0

    def __sub__(self, other):
        """Retrurn new MyPolynomial object substracting other from self."""
        self._supported_operand(other)
        if type(other) == type(self):
            max_len = max(len(self), len(other))
            return MyPolynomial.from_iterable(
                list([self.__coef(i) - other.__coef(i) for i in range(max_len)]))

        return (self - MyPolynomial(other))

    def __isub__(self, other):
        """Substract other from self."""
        self._supported_operand(other)
        if type(other) == type(self):
            max_len = max(len(self), len(other))
            self.__coefs = list([self.__coef(i) - other.__coef(i) for i in range(max_len)])

        self[0] -= other

        return self

    def __rsub__(self, other):
        """Retrurn new MyPolynomial object substracting self from other."""
        self._supported_operand(other)
        if type(other) == type(self):
            max_len = max(len(self), len(other))
            return MyPolynomial.from_iterable(
                [self.__coef(i) - other.__coef(i) for i in range(max_len)])._truncate_zeros()

        return (MyPolynomial(other) + MyPolynomial(self))._truncate_zeros()

    def __truediv__(self, other):
        """Retrurn new MyPolynomial object divided by a number."""
        self._supported_digit_operand(other)

        new_coefs = [x / other for x in self.__coefs]
        return MyPolynomial(*new_coefs)

    def __itruediv__(self, other):
        """Retrurn this MyPolynomial object divided by a number."""
        new_coefs = [x / other for x in self.__coefs]
        for i, x in enumerate(new_coefs):
            self.__coefs[i] = x
        return self

    def __rtruediv__(self, other):
        """Operation not yet supported."""
        raise OperationNotSupportedError("Operator / is not yet supported")


class Tests(unittest.TestCase):
    """Manin Test class."""

    def test_3_1(self):
        assert type(MyPolynomial()) is MyPolynomial
        assert type(MyPolynomial(1)) is MyPolynomial
        assert type(MyPolynomial(1, 2)) is MyPolynomial
        assert type(MyPolynomial(0, 0)) is MyPolynomial
        assert any(["_MyPolynomial__" in name for name in MyPolynomial().__dict__.keys()])

    def test_3_2(self):
        assert "1 + 2x^1" == str(MyPolynomial(1, 2))
        assert "MyPolynomial(1, 2)" == repr(MyPolynomial(1, 2))
        assert "MyPolynomial(0)" == repr(MyPolynomial())
        assert "MyPolynomial(0)" == repr(MyPolynomial(0, 0, 0))
        assert "0" == str(MyPolynomial(0, 0, 0))

    def test_3_3(self):
        assert MyPolynomial(1, 2, 2)(0) == 1
        assert MyPolynomial(1, 2, 2)(1) == 5
        assert MyPolynomial(1, 2, 2)(2) == 13
        assert MyPolynomial(1, 2, 2)(3) == 25
        assert MyPolynomial(1, 2, 2)(4) == 41

    def test_3_4(self):
        assert MyPolynomial(1, 2, 2) == MyPolynomial(1, 2, 2)
        assert (MyPolynomial(1, 2, 2) == MyPolynomial(1, 2)) is False
        assert MyPolynomial(0) == MyPolynomial()
        assert MyPolynomial(0, 0) == MyPolynomial(0)
        assert MyPolynomial(0, 0, 0) == MyPolynomial(0)
        assert MyPolynomial(1, 0, 0) == MyPolynomial(1)
        assert MyPolynomial(0, 1, 0) == MyPolynomial(0, 1)
        assert MyPolynomial(0, 1, 1) == MyPolynomial(0, 1, 1)

    def test_3_5(self):
        assert MyPolynomial.from_iterable([0, 1, 2]) == MyPolynomial(0, 1, 2)
        assert MyPolynomial.from_iterable((0, 1, 2)) == MyPolynomial(0, 1, 2)
        assert MyPolynomial.from_iterable([1, 2, 2]) == MyPolynomial(1, 2, 2)
        assert (MyPolynomial.from_iterable((1, 2, 2)) == MyPolynomial(1, 2)) is False
        assert MyPolynomial.from_iterable([0]) == MyPolynomial()
        assert MyPolynomial.from_iterable([0, 0]) == MyPolynomial(0)
        assert MyPolynomial.from_iterable(set([0, 0, 0])) == MyPolynomial(0)

    def test_3_6(self):
        assert MyPolynomial(5, 4).degree() == 1
        assert MyPolynomial().degree() == 0
        assert MyPolynomial(0, 0, 0).degree() == 0
        assert MyPolynomial(0, 1, 0).degree() == 1
        assert MyPolynomial(0, 0, 1).degree() == 2
        assert MyPolynomial.from_iterable([0, 1, 0]).degree() == 1

    def test_3_7(self):
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

    def test_3_8(self):
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

    def test_4_1_1(self):
        assert '1 - 2x^1' == str(MyPolynomial(1, -2))
        assert '-1 + x^1 - 2x^2' == str(MyPolynomial(-1, 1, -2))
        assert '1 + 2x^2' == str(MyPolynomial(1, 0, 2))
        assert '-1 - 2x^2' == str(-MyPolynomial(1, 0, 2))
        assert '-1 - 2x^2 + x^7' == str(-MyPolynomial(1, 0, 2, 0, 0, 0, 0, -1))
        assert 'MyPolynomial(-1, -2)' == repr(MyPolynomial(-1, -2))
        assert 'MyPolynomial(-1, -2)' == repr(-MyPolynomial(1, 2))

    def test_4_1_2(self):
        assert MyPolynomial(2, 4) == MyPolynomial(5, 4) - 3
        assert MyPolynomial(0, 4, 1, 4) == (MyPolynomial(0, 4, 1, 4) - 2) + 2

    def test_4_1_3(self):
        assert MyPolynomial(2, 4) == MyPolynomial(5, 8) - MyPolynomial(3, 4)
        assert MyPolynomial(1, 1, 2, 2) == MyPolynomial(2, 2, 2, 2) - MyPolynomial(1, 1)
        assert MyPolynomial(3, 3, 2, 2) == MyPolynomial(2, 2, 2, 2) - -MyPolynomial(1, 1)

    def test_4_1_4(self):
        assert MyPolynomial(-2, -4) == -MyPolynomial(2, 4)
        assert MyPolynomial(-2, 4) == -MyPolynomial(2, -4)

    def test_4_2_1(self):
        assert MyPolynomial(1, 1) == MyPolynomial(2, 2) / 2
        assert MyPolynomial(3, 5, 6) == MyPolynomial(6, 10, 12) / 2
        assert MyPolynomial(3, -5, 6) == MyPolynomial(6, -10, 12) / 2
        assert MyPolynomial(3, -5, 6) == -MyPolynomial(6, -10, 12) / -2

    def test_4_3_1(self):
        data = [(1,), (1, 2, 3, 4), (MyPolynomial(1, 2), ), (100, ), ('yolo', ),
                (None, ), (True, ), ({}, ), (dict(), ),
                ]
        expect_exceptions = [False, False, False, False, True, True, True, True, True]
        params = zip(data, expect_exceptions)
        for args, expect_exception in params:
            if expect_exception:
                with self.assertRaises(InvalidInputOperandError):
                    MyPolynomial(*args)
            else:
                MyPolynomial(*args)

    def test_4_3_2(self):
        a = MyPolynomial(21, 37)
        b = MyPolynomial(14, 88)

        with self.assertRaises(OperationNotSupportedError):
            c = a ** b

        with self.assertRaises(OperationNotSupportedError):
            c = a // b

        with self.assertRaises(OperationNotSupportedError):
            c = a << b

        with self.assertRaises(OperationNotSupportedError):
            c = b >> a

        with self.assertRaises(OperationNotSupportedError):
            c = a ** 5

        with self.assertRaises(OperationNotSupportedError):
            c = a // 6

        with self.assertRaises(OperationNotSupportedError):
            c = a >> 1

        with self.assertRaises(OperationNotSupportedError):
            c = b << 9

        with self.assertRaises(OperationNotSupportedError):
            c = 9 / b

        with self.assertRaises(OperationNotSupportedError):
            x = 9
            x /= b

    def test_4_3_3(self):
        polynomianl = MyPolynomial(2)
        operands = ['yolo', [], {}, dict(), None, False, True, '', {1, 2}]
        for operand in operands:
            with self.assertRaises(InvalidOperandError):
                a = polynomianl + operand
            with self.assertRaises(InvalidOperandError):
                a = operand + polynomianl
            with self.assertRaises(InvalidOperandError):
                a = polynomianl * operand
            with self.assertRaises(InvalidOperandError):
                a = operand * polynomianl
            with self.assertRaises(InvalidOperandError):
                a = polynomianl / operand
            with self.assertRaises(InvalidOperandError):
                a = polynomianl - operand
            with self.assertRaises(InvalidOperandError):
                a = operand - polynomianl

    def test_4_4_1(self):

        with self.assertRaises(InvalidInputOperandError):
            MyPolynomial(MyPolynomial(1, MyPolynomial(1, 2, 3), "1"))

        assert MyPolynomial(MyPolynomial(1, 2, 3)) == MyPolynomial(1, 2, 3)
        assert MyPolynomial(MyPolynomial(-1, -2)) == -MyPolynomial(1, 2)
        assert MyPolynomial(1, MyPolynomial(-1, -2)) == MyPolynomial(1, -1, -2)

    def test_4_4_2(self):
        assert MyPolynomial(
            MyPolynomial(1, 2, 3),
            MyPolynomial(1, 2, 3),
            MyPolynomial(1, 2, 3)) == MyPolynomial(1, 3, 6, 5, 3)
        assert MyPolynomial(
            MyPolynomial(1, 2, 3),
            MyPolynomial(1, -2, 3),
            MyPolynomial(1, 2, -3)) == MyPolynomial(1, 3, 2, 5, -3)

    def test_4_4_3(self):
        x = MyPolynomial(MyPolynomial(1, 2, 3),
                         -MyPolynomial(2, MyPolynomial(1, 2, 3), 3, 4, MyPolynomial(1, 2, 3)),
                         MyPolynomial(1),
                         -5,
                         MyPolynomial(1),
                         MyPolynomial(1, 2, 3))

        assert x == MyPolynomial(1, 0, 3, -10, -6)


if __name__ == '__main__':
    unittest.main()
