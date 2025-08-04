import os
import json

class Pokemon:
    def __init__(self):
        self.nickname = None
        self.species = None
        self.level = None
        self.ability = None
        self.gender = None
        self.item = None
        self.nature = None
        self.ivs = None
        self.teraType = None
        self.status = None
        self.index = None
        self.moves = []


class Trainer:
    def __init__(self):
        self.name = None
        self.double_battle = None
        self.party = []


def write_file(content, file):
    with open(file, 'a') as file:
        file.write(str(content) + '\n')


def get_mon_suffix(mon):
    if mon.status is not None and mon.teraType is None:
        return f'{mon.ability}|{mon.nature}|{mon.status}'
    elif mon.status is None and mon.teraType is not None:
        return f'{mon.ability}|{mon.nature}|{mon.teraType}'
    if mon.status is not None and mon.teraType is not None:
        return f'{mon.ability}|{mon.nature}|{mon.teraType}|{mon.status}'
    else:
        return f'{mon.ability}|{mon.nature}'

"""
def generate_mastersheet(trainers):
    str = ""
    for trainer in trainers:
        if trainer.double_battle == "Yes":
            str += f'## {trainer.name} [Double Battle]\n'
        else:
            str += '## ' + trainer.name + '\n'
        for mon in trainer.party:
            suffix = get_mon_suffix(mon)
            str += f'{mon.species} Lv.{mon.level} @{mon.item}: {', '.join(mon.moves)} [{suffix}]  \n'
        str += '\n'
    return str
"""

def generate_calc_sets(trainers):
    data = {}
    for trainer in trainers:
        trainer_name = (trainer.name + '\n')
        trainer_name = {} 
        for mon in trainer.party:
            species = mon.species
            if species not in data:
                data[species] = {}
            data[species].update({trainer.name: {"level": mon.level, \
                                                 "ivs": mon.ivs, \
                                                 "item": mon.item, \
                                                 "ability": mon.ability, \
                                                 "nature": mon.nature, \
                                                 "teraType": mon.teraType, \
                                                 "status": mon.status, \
                                                 "moves": mon.moves, \
                                                 "index": mon.index}})

    return "var SETDEX_SV = " + json.dumps(data, indent=2)


def get_html_header():
    with open('site/header.html', 'r') as f:
        return f.readlines()


def generate_webpage(trainers):
    site_str = "".join(get_html_header())
    site_str += '\n'
    trainers = trainers[1:]

    for trainer in trainers:
        site_str += f'<table class="content-table">\n'
        if trainer.double_battle == "Yes":
            site_str += f'<caption class="caption-content">{trainer.name} [Double Battle]</caption>\n'
        else:
            site_str += f'<caption class="caption-content">{trainer.name}</caption>\n'
        site_str += f'<tbody>\n'

        # images
        site_str += f'<tr>\n'
        for i in range(0, 6):
            if i >= len(trainer.party):
                site_str += f'<td><img src="https://play.pokemonshowdown.com/sprites/gen5/.png" alt=""></img></td>\n'
            else:
                mon = trainer.party[i]
                site_str += f'<td><img src="https://play.pokemonshowdown.com/sprites/gen5/{mon.species.lower()}.png" alt=""></img></td>\n'
        site_str += f'</tr>\n'

        # names
        lst_names = ["<tr>\n", "<th></th>\n", "<th></th>\n", "<th></th>\n", "<th></th>\n", "<th></th>\n", "<th></th>\n", "</tr>\n"]
        counter = 1
        for mon in trainer.party:
            lst_names[counter] = f'<th>{mon.species}</th>\n'
            counter += 1
        site_str += "".join(lst_names)

        lst_other = ["<tr>\n", "<td></td>\n", "<td></td>\n", "<td></td>\n", "<td></td>\n", "<td></td>\n", "<td></td>\n", "</tr>\n"]

        # levels
        counter = 1
        for mon in trainer.party:
            lst_other[counter] = f'<td>{mon.level}</td>\n'
            counter += 1
        site_str += "".join(lst_other)

        # items
        counter = 1
        for mon in trainer.party:
            lst_other[counter] = f'<td>{mon.item}</td>\n'
            counter += 1
        site_str += "".join(lst_other)

        # ability
        counter = 1
        for mon in trainer.party:
            lst_other[counter] = f'<td>{mon.ability}</td>\n'
            counter += 1
        site_str += "".join(lst_other)

        # first move
        counter = 1
        move_row_present = False
        for mon in trainer.party:
            try:
                lst_other[counter] = f'<td>{mon.moves[0]}</td>\n'
                move_row_present = True
            except:
                pass
            counter += 1
        if move_row_present:
            site_str += "".join(lst_other)

        # second move
        counter = 1
        move_row_present = False
        for mon in trainer.party:
            try:
                lst_other[counter] = f'<td>{mon.moves[1]}</td>\n'
                move_row_present = True
            except:
                lst_other[counter] = f'<td></td>\n'
            counter += 1
        if move_row_present:
            site_str += "".join(lst_other)

        # third move
        counter = 1
        move_row_present = False
        for mon in trainer.party:
            try:
                lst_other[counter] = f'<td>{mon.moves[2]}</td>\n'
                move_row_present = True
            except:
                lst_other[counter] = f'<td></td>\n'
            counter += 1
        if move_row_present:
            site_str += "".join(lst_other)

        # fourth move
        counter = 1
        move_row_present = False
        for mon in trainer.party:
            try:
                lst_other[counter] = f'<td>{mon.moves[3]}</td>\n'
                move_row_present = True
            except:
                lst_other[counter] = f'<td></td>\n'
            counter += 1
        if move_row_present:
            site_str += "".join(lst_other)

    site_str += "</body>\n</html>\n"
    return site_str

def parse_parties(parties):
    trainer_parties = []
    trainer = None
    pokemon = None
    trainer_name = None
    trainer_class = None

    prev_line = None
    parsing_mon = False
    mon_index = 0

    for line in parties:
        if "REGULAR TRAINERS END" in line:
            break

        if "Name" in line:
            trainer_name = line.split(':')[1].strip()
        elif "Class" in line:
            trainer_class = line.split(':')[1].strip()
            trainer = Trainer()
            trainer.name = trainer_class + " " + trainer_name
        elif "Battle Type:" in line:
            trainer.double_battle = line.split(':')[1].strip()
        elif "=== TRAINER_" in line and prev_line == '\n':
            trainer_parties.append(trainer)
        elif "=== TRAINER_" not in line and prev_line == '\n':
            parsing_mon = True
            pokemon = Pokemon()
            if "@" in line and prev_line == '\n':
                pokemon.species = line.split('@')[0].strip() 
                pokemon.item = line.split('@')[1].strip()
            elif "@" not in line and prev_line == '\n':
                pokemon.species = line.split('\n')[0].strip()
        elif parsing_mon:
            if line == "\n":
                parsing_mon = False
                pokemon.index = mon_index
                mon_index += 1
                trainer.party.append(pokemon)
            elif "Ability:" in line:
                pokemon.ability = line.split(':')[1].strip()
            elif "Level:" in line:
                pokemon.level = line.split(':')[1].strip()
            elif "Tera Type:" in line:
                pokemon.teraType = line.split(':')[1].strip()
            elif "Status:" in line:
                pokemon.status = line.split(':')[1].strip()
            elif "Nature:" in line:
                pokemon.nature = line.split(':')[1].strip()
            elif "IVs:" in line:
                pokemon.ivs = line.split(':')[1].strip()
                ivs_str = []
                for i in pokemon.ivs.split(" / "):
                    ivs_str.append(i.split(" ")[0].strip())
                ivs = {"hp": int(ivs_str[0]),
                       "at": int(ivs_str[1]),
                       "df": int(ivs_str[2]),
                       "sa": int(ivs_str[3]),
                       "sd": int(ivs_str[4]),
                       "sp": int(ivs_str[5]),}
                pokemon.ivs = ivs
            elif "- " in line:
                pokemon.moves.append(line[1:].strip())

        prev_line = line

    return trainer_parties


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def get_party_contents(file):
    with open(file, 'r') as file:
        return file.readlines()


# TODO: Double Battles are not handled
if __name__ == "__main__":
    source = "../tag-game/src/data/trainers.party"
    """
    mastersheet = "mastersheet.md"
    """
    calc_sets = "src/js/data/sets/gen9.js"
    webpage = "site/index.html"

    parsed_trainers = parse_parties(get_party_contents(source))
    print("Num of trainers: " + str(len(parsed_trainers)))

    """
    delete_file(mastersheet)
    write_file(generate_mastersheet(parsed_trainers), mastersheet)
    """

    delete_file(calc_sets)
    write_file(generate_calc_sets(parsed_trainers), calc_sets)

    delete_file(webpage)
    write_file(generate_webpage(parsed_trainers), webpage)
