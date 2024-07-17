import requests
import json
from bs4 import BeautifulSoup
from enum import Enum


class RoleLookup(Enum):
    NAME = 0
    TOP = 1
    JUNGLE = 2
    MID = 3
    BOT = 4
    SUPPORT = 5
    UNPLAYED = 6


if __name__ == '__main__':
    wiki_url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'
    soup = BeautifulSoup(requests.get(wiki_url).text, 'html.parser')
    champ_table = soup.findAll('table')[1]

    role_info = []
    for row in champ_table.findAll('tr'):
        try:
            champ_name = row.find('span', {'data-game': 'lol'})['data-champion']
        except KeyError:
            continue

        champ_roles = []
        columns = row.findAll('td')
        for i, col in enumerate(columns):
            if i == 0:
                continue

            try:
                sort_value = col['data-sort-value']
            except KeyError:
                continue

            champ_roles.append(RoleLookup(i).name)

        role_info.append({"Name": champ_name,
                          "Role": champ_roles})

    with open('champions.json', 'w') as f:
        json.dump(role_info, f, indent=2)
