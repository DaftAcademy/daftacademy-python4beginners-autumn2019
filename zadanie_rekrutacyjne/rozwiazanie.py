"""DaftAcademy Python4Beginers recrutment assignment resolve script."""
from collections import defaultdict
from statistics import mean
from math import ceil


def get_data(filename):
    """Data file parser."""
    rows = list()
    data = list()
    with open(filename, "r") as f:
        headers = f.readline().strip('\n').split(";")
        for i in range(len(headers)):
            x = headers[i].split(' ')
            headers[i] = {
                "no": int(x[0].strip(':')),
                "name": x[1],
                "class": x[2].strip('()')
            }
        for line in f:
            rows.append(line.strip(') \n').split(";"))

        for i in range(len(headers)):
            # list(filter(lambda g: len(g), [y[i] for y in rows]))})
            # is list from filter wchich is a generator
            # filter accepts only non empty strings and is processed
            # by lambda function doing len(teu)
            # and is iterating it by column for all rows in data structure
            cargo = list(filter(lambda teu: len(teu), [y[i] for y in rows]))
            for j, teu in enumerate(cargo):
                # aa-bb-cccccccc/yyyy/xx@ddddddddd.ee/pp
                aabbcc, yyyy, xxdee, pp = teu.split('/')
                aa, bb, cc = aabbcc.split('-')
                xx, dee = xxdee.split('@')
                d, ee = dee.split('.')

                cargo[j] = {'aa': aa,
                            'bb': bb,
                            'cc': cc,
                            'yyyy': int(yyyy),
                            'xx': xx,
                            'd': d,
                            'ee': ee,
                            'pp': int(pp)}
            ship_data = {'cargo_size': len(cargo),
                         'cargo': cargo}
            ship_data.update(headers[i])
            data.append(ship_data)

    return data


def assignment_1(data):
    jp = 0
    for ship in data:
        for teu in ship['cargo']:
            if teu['bb'] == 'JP':
                jp += 1
    return jp


def assignment_2(data):
    teu_counter = defaultdict(list)
    for ship in data:
        teu_counter[ship['class']].append(ship['cargo_size'])
    return max(teu_counter.keys(), key=(lambda key: mean(teu_counter[key])))


def assignment_3(data):
    x1_teus = list()
    for ship in data:
        x1_teus.extend(x['yyyy'] for x in ship['cargo'] if x['xx'] == 'X1')
    return ceil(mean(x1_teus))


def assignment_4(data):
    teu_counter = defaultdict(int)
    for ship in data:
        for teu in ship['cargo']:
            if teu['ee'] == 'pl':
                teu_counter[teu['d']] += 1
    return max(teu_counter.keys(), key=(lambda key: teu_counter[key]))


def assignment_5(data):
    cargo_type = defaultdict(list)
    for ship in data:
        for teu in ship['cargo']:
            if teu['bb'] == 'DE' and teu['ee'] == 'de':
                cargo_type[teu['xx']].append(teu['pp'] / teu['yyyy'])

    return max(cargo_type.keys(), key=(lambda key: max(cargo_type[key])))


data = get_data("./dane.csv")
print("1:", assignment_1(data))
print("2:", assignment_2(data))
print("3:", assignment_3(data))
print("4:", assignment_4(data))
print("5:", assignment_5(data))
