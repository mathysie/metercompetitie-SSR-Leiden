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


from_site = len(sys.argv) >= 2 and sys.argv[1] == '1'
