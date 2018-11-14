import requests
import re

bestuur = 'Blijf Genieten'
website = 'https://metercompetitie.ssr-leiden.nl/'


def lootjes(meters):
    return (meters - meters % 5) / 5


def parse_disputen():
    pattern = '<span class="dispuutsnaam">([a-zA-Z0-9.\- ]+)</span>[\r\n\s]+' \
        + '<span class="aantalMeters">([0-9]+)</span>'
    disputen = {}

    site = requests.get(website).text
    matches = re.findall(pattern, site, re.MULTILINE)

    for match in matches:
        if match[0] != bestuur:
            disputen[match[0]] = {
                'meters': int(match[1]),
                'lootjes': lootjes(int(match[1]))
            }

    disputen = sorted(
        disputen.items(),
        key=lambda kv: kv[1]['meters'],
        reverse=True
    )

    return disputen
