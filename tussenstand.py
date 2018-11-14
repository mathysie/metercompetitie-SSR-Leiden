import requests
import re
import sys

bestuur = 'Blijf Genieten'
website = 'https://metercompetitie.ssr-leiden.nl/'


def read_input_file():
    data = []

    f = open('input.txt', 'r')
    for line in f:
        data.append(line.rstrip().split(','))

    return data


def read_input_site():
    pattern = '<span class="dispuutsnaam">([a-zA-Z0-9.\- ]+)</span>[\r\n\s]+' \
        + '<span class="aantalMeters">([0-9]+)</span>'

    site = requests.get(website).text
    matches = re.findall(pattern, site, re.MULTILINE)

    return matches


def read_input():
    return read_input_site() if from_site else read_input_file()


def lootjes(meters):
    return (meters - meters % 5) / 5


def parse_disputen():
    disputen = {}
    data = read_input()

    for entry in data:
        if entry[0] != bestuur:
            disputen[entry[0]] = {
                'meters': int(entry[1]),
                'lootjes': lootjes(int(entry[1]))
            }

    disputen = sorted(
        disputen.items(),
        key=lambda kv: kv[1]['meters'],
        reverse=True
    )

    return disputen


def kansen_winnaar():
    kansen = {}
    kansen[disputen[0][0]] = 1.0

    for i in range(1, len(disputen)):
        kansen[disputen[i][0]] = 0.0

    return kansen


def kansen_top_5():
    kansen = {}
    kansen[disputen[0][0]] = 0.0

    for i in range(1, len(disputen)):
        kansen[disputen[i][0]] = 0.25 if i < 5 else 0.0

    return kansen


def kansen_lootjes():
    lootjes = 0.0
    for i in range(1, len(disputen)):
        lootjes += disputen[i][1]['lootjes']

    # Winnende dispuut mag niet meeloten
    kansen = {}
    kansen[disputen[0][0]] = 0.0

    for i in range(1, 5):
        l = range(1, 5)
        l.remove(i)
        kansen[disputen[i][0]] = 0.0
        for j in l:
            kansen[disputen[i][0]] += disputen[i][1]['lootjes'] \
                / (4 * (lootjes - disputen[j][1]['lootjes']))

    for i in range(5, len(disputen)):
        kansen[disputen[i][0]] = 0.0
        for j in range(1, 5):
            kansen[disputen[i][0]] += disputen[i][1]['lootjes'] \
                / (4 * (lootjes - disputen[j][1]['lootjes']))

    return kansen


def kansen_totaal():
    kansen = {}
    winnaar = kansen_winnaar()
    top_5 = kansen_top_5()
    lootjes = kansen_lootjes()

    for dispuut in disputen:
        kansen[dispuut[0]] = winnaar[dispuut[0]] + top_5[dispuut[0]] \
            + lootjes[dispuut[0]]

    return kansen


def output():
    string = 'De kans op een fust:\n'
    waarden = sorted(kansen.iteritems(), key=lambda k: k[1], reverse=True)

    for waarde in waarden:
        string += '\t{0}: {1:.1f}\n'.format(waarde[0], waarde[1] * 100)

    print(string)
    return


from_site = len(sys.argv) >= 2 and sys.argv[1] == '1'
disputen = parse_disputen()
kansen = kansen_totaal()
output()
