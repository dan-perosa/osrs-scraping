import requests
import json
import pandas as pd

# 3943

url = 'http://services.runescape.com/m=itemdb_rs/bestiary/beastData.json?beastid=1'

# res = requests.get(url)

# print(res.text)

monsters_data_list = []

# names_list = []

# max = 0

for i in range(3943):
    res = requests.get(url + str(i + 1))
    if res.text == '':
        continue
    try:
        loaded = json.loads(res.text)
        monster = {
            'name': loaded.get('name', ''),
            'id': loaded.get('id', ''),
            'members': loaded.get('members', ''),
            'weakness': loaded.get('weakness', ''),
            'level': loaded.get('level', ''),
            'lifepoints': loaded.get('lifepoints', ''),
            'defence': loaded.get('defence', ''),
            'attack': loaded.get('attack', ''),
            'magic': loaded.get('magic', ''),
            'ranged': loaded.get('ranged', ''),
            'xp': loaded.get('xp', ''),
            'slayerlevel': loaded.get('slayerlevel', ''),
            'slayercat': loaded.get('slayercat', ''),
            'size': loaded.get('size', ''),
            'attackable': loaded.get('attackable', ''),
            'aggressive': loaded.get('aggressive', ''),
            'poisonous': loaded.get('poisonous', ''),
            'description': loaded.get('description', ''),
            'areas': ', '.join(loaded.get('areas', [])),  # Converte lista para string
            'animations': ', '.join(f"{key}: {value}" for key, value in loaded.get('animations', {}).items())  # Converte dict para string
        }
        
        for monster_data in monsters_data_list:
            if monster['name'] in monster_data['name']:
                break
        else:
            monsters_data_list.append(monster)
            
    except json.JSONDecodeError:
        continue

df = pd.DataFrame(monsters_data_list)
        
df.to_excel('osrs_monsters.xlsx', index=False, engine='openpyxl')
