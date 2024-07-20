from requests import get
from json import dump
from bs4 import BeautifulSoup
from enum import Enum

WIKI_URL: str = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'


class RoleLookup(Enum):
    NAME = 0
    TOP = 1
    JUNGLE = 2
    MID = 3
    BOT = 4
    SUPPORT = 5
    UNPLAYED = 6


def main() -> None:
    soup = BeautifulSoup(get(WIKI_URL).text, 'html.parser')
    champ_table = soup.findAll('table')[1]

    role_info = []
    for row in champ_table.findAll('tr'):
        champ_cell = row.find('span')

        if 'data-champion' not in champ_cell.attrs:
            continue

        champ_name = champ_cell['data-champion']

        champ_roles = []
        columns = row.findAll('td')
        for i, col in enumerate(columns):
            if i == 0:
                continue

            if 'data-sort-value' not in col.attrs:
                continue

            champ_roles.append(RoleLookup(i).name)

        role_info.append({"Name": champ_name,
                          "Role": champ_roles})

    with open('champions.json', 'w') as f:
        dump(role_info, f, indent=2)


if __name__ == '__main__':
    main()
