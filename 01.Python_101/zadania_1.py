# ZADANIE 1
# Stwórz listę liczb od 0 do 999.
# Liczby podzielne przez 5 zastąp słowem '❤️'.
# Liczby podzielne przez 7 zastąp słowem '🐍'.
# Liczby podzielne przez 11 zastąp słowem '🐕'.
# Liczby podzielne jednocześnie przez 11 i 5 zastąp słowem '🐕❤️'.
# Liczby podzielne jednocześnie przez 5 i 7 zastąp słowem '❤️🐍'.
# Liczby podzielne jednocześnie przez 11 i 7 zastąp słowem '🐕🐍'.
# Liczby podzielne jednocześnie przez 11,5,7 zastąp słowem '🐕❤️🐍'.
# Wynikową listę przypisz zmiennej result.
result = None


start = [x for x in range(1000)]
result = []
assert type(start) is list, "result is not a list"
assert len(start) == 1000, "result list is too small"
for x in start:
    if x % 11 == 0 and x % 5 == 0 and x % 7 == 0:
        result.append("🐕❤️🐍")
    elif x % 11 == 0 and x % 5 == 0:
        result.append("🐕❤️")
    elif x % 11 == 0 and x % 7 == 0:
        result.append("🐕🐍")
    elif x % 5 == 0 and x % 7 == 0:
        result.append("❤️🐍")
    elif x % 11 == 0:
        result.append("🐕")
    elif x % 5 == 0:
        result.append("❤️")
    elif x % 7 == 0:
        result.append("🐍")
    else:
        result.append(x)

# print("ZAD1:", result)
assert result[11 * 5 * 7 * 2] == "🐕❤️🐍"


# ZADANIE 2
# Napisać kod tworzący listę krotek kolejnych elementów nieparzystych < 100 według
# schematu: [(1,), (3,), ... , (99,)]. Wynikową listę przypisz do zmiennej result.
result = None

result = [(x,) for x in range(100) if x % 2 == 0]
assert type(result) is list
assert len(result) == 50
assert result[1] == (2,)
for x in result:
    assert type(x) is tuple, f"{x} is not a tuple!"
    assert len(x) == 1, f"Tuple is too small: {x}"
    assert x[0] % 2 == 0, f"This value is even: {x[0]}"
# print("ZAD2", result)

# ZADANIE 3
# Napisz kod transformujący podany słownik:
# {
#     1: 'Mateusz',
#     2: 'Marcin',
#     3: 'Wojciech',
#     4: 'Marcin',
#     5: 'Michał',
#     6: 'Antonii',
#     7: 'Katarzyna',
#     8: 'Agata'
# }
# do postaci:
# {
#     'Mateusz': 1,
#     'Marcin': 2,
#     ...
#     'Agata': 8
# }
# (Zamiana klucza z wartością).
# Wynik przypisz do zmiennej result


names = {
    1: "Mateusz",
    2: "Marcin",
    3: "Wojciech",
    4: "Marcin",
    5: "Michał",
    6: "Antonii",
    7: "Katarzyna",
    8: "Agata",
}
result = {v: k for k, v in names.items()}

assert type(result) is dict, f"{result} is not a dict!"
assert len(result) == len(names) - 1, f"{result} is too big!"
assert "Mateusz" in result, f"There is not Mateusz in your result: {result}"
# print("ZAD3", result)

# ZADANIE 4
# Napisz program tworzący ze zbioru U = {'👻', '🕵', '🔺', '🐉', '🐍', '🦂', '🔥', '🌻', '🐙', '🌌'}
# zbiór zawierający wszystkie podzbiory U (włącznie z pustym i U).
# UWAGA: w python zbiory (set) nie mogą być elementami innych zbiorów,
# proszę użyć frozenset jako zbiorów wewnętrznych.
# Wynik przypisz do zmienej result
import itertools

result = None
U = {"👻", "🕵", "🔺", "🐉", "🐍", "🦂", "🔥", "🌻", "🐙", "🌌"}
result = [()]
for i in range(len(U)):
    result += itertools.combinations(U, i + 1)
result = set([frozenset(x) for x in result])

assert type(result) is set, "Your results is not a set"
assert len(result) == 1024, "Your results are too short"
assert (
    frozenset(("👻", "🕵", "🔺", "🐉", "🐍", "🦂", "🔥", "🌻", "🐙", "🌌")) in result
), "You could not omit any set!"
assert frozenset() in result, "You could not omit any set!"
# print("ZAD4", result)
