from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import os
import time

def mount_equipment_data():
    if os.path.isfile('osrs_equipments.xlsx'):
        df_to_find_existents = pd.read_excel('osrs_equipments.xlsx', engine='openpyxl')
        if (len(df_to_find_existents) > 0):
            to_json_on_existents = df_to_find_existents.to_json(orient='records')
            parsed_existents = json.loads(to_json_on_existents)
            return parsed_existents
    return []

def find_total_equipments_in_xlsx():
    find_last_equipment_index = pd.read_excel('osrs_equipments.xlsx', engine='openpyxl')
    return len(find_last_equipment_index)

def check_if_equipment_in_xlsx(equipment):
    if os.path.isfile('osrs_equipments.xlsx'):
        df_to_find_is_equipment_already_in_xlsx = pd.read_excel('osrs_equipments.xlsx', engine='openpyxl')
        if 'Eqipment name' in df_to_find_is_equipment_already_in_xlsx.columns:
            return equipment in df_to_find_is_equipment_already_in_xlsx['Monster name'].values
    return False


url = 'https://oldschool.runescape.wiki/w/Worn_Equipment'

options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome() 
driver.get(url)
driver.implicitly_wait(2)

outside_div = driver.find_element(by=By.CLASS_NAME, value='mw-parser-output')
all_a_tags = outside_div.find_elements(by=By.TAG_NAME, value='a')
equipment_types_to_click: list[WebElement] = []

for a_tag in all_a_tags:
    if a_tag.text != None:
      if 'slot table' in a_tag.text:
          equipment_types_to_click.append(a_tag)
          
all_equipment_data = mount_equipment_data()

summed_all_number_of_equipments_in_wiki_tables = 0
    
for equipment_type in equipment_types_to_click:
    
    # clica em cada tipo de equipamento na pagina inicial
    time.sleep(5)
    equipment_type.click()
    time.sleep(5)
    
    # encontra os headers da tabela após clicar no range de lvl
    both_tables = driver.find_elements(by=By.TAG_NAME, value='table')
    complete_equipment_table = both_tables[1]
    complete_equipment_table_headers = complete_equipment_table.find_elements(by=By.TAG_NAME, value='th') 
    header_names = ['Image', 'Equipment Name']
    
    for header in complete_equipment_table_headers:
        if header.text != '':
            continue
        title = header.find_element(by=By.TAG_NAME, value='img')
        header_names.append(title.get_dom_attribute('alt'))
    if 'Speed' not in header_names:
        header_names.append('Speed')
    # termina os headers
    
    # começa checagem para ver aonde começar na wiki
    # checa quantidade de linhas na tabela pra comparar com xlsx
    rows_in_equipments_table = complete_equipment_table.find_elements(by=By.TAG_NAME, value='tr')
    number_of_equipments_in_wiki_table = len(rows_in_equipments_table)
    print('number of rows: ', number_of_equipments_in_wiki_table)
    summed_all_number_of_equipments_in_wiki_tables += number_of_equipments_in_wiki_table
    
    if (len(all_equipment_data) > 0):
        total_equipments_in_xlsx = find_total_equipments_in_xlsx()
    
    # caso o numero de equipamentos no xlsx seja maior ou igual que todos os vistos já na wiki
    if total_equipments_in_xlsx >= summed_all_number_of_equipments_in_wiki_tables:
        print('total_eq in xlsx maior ou igual que a soma das table')
        already_in_xlsx_equipments = number_of_equipments_in_wiki_table
    
    # caso o numero de equipamentos no xlsx seja menor que todos os vistos já na wiki
    if total_equipments_in_xlsx < summed_all_number_of_equipments_in_wiki_tables:
        print('total_eq in xlsx menor que a soma das table')
        already_in_xlsx_equipments = number_of_equipments_in_wiki_table - (summed_all_number_of_equipments_in_wiki_tables - total_equipments_in_xlsx)

    # procura a lista com todas as linhas da tabela 
    find_tbody = complete_equipment_table.find_element(by=By.TAG_NAME, value='tbody')
    list_with_all_tr_tags = find_tbody.find_elements(by=By.TAG_NAME, value='tr')
    # termina de procurar lista com linhas
    
    # começa iterar cada linha pra pegar o td
    for tr_index, tr in enumerate(list_with_all_tr_tags):
        if tr_index < already_in_xlsx_equipments:
            print('pulando linha ', tr_index)
            continue
        equipment_row_data = {}
        all_td_in_tr = tr.find_elements(by=By.TAG_NAME, value='td')
        # itera em cada td do tr atual
        for td_index, td in enumerate(all_td_in_tr):
            # procura imagem para o caso da imagem e members
            images = td.find_elements(by=By.TAG_NAME, value='img')
            if len(images) > 0:
                image_src = images[0].get_dom_attribute('src')
                if image_src == '/images/Free-to-play_icon.png?628ce' or \
                    image_src == '/images/Member_icon.png?1de0c':
                        check_star_image = td.find_element(by=By.TAG_NAME, value='img')
                        is_member = check_star_image.get_dom_attribute('alt')
                        equipment_row_data['Members'] = is_member
                        continue
                else:
                    equipment_row_data['Image'] = 'https://oldschool.runescape.wiki' + image_src
                    continue
            # checa se é a coluna de nome
            if td_index == 1:
                check_if_equipment_in_xlsx(td.text)
                equipment_row_data['Equipment Name'] = td.text
                continue
            # pega as outras colunas
            equipment_row_data[header_names[td_index]] = td.text
            
        if 'Speed' not in list(equipment_row_data.keys()):
            equipment_row_data['Speed'] = 'N/A'
        all_equipment_data.append(equipment_row_data)
        df = pd.DataFrame(all_equipment_data)
        df.to_excel('osrs_equipments.xlsx', index=False, engine='openpyxl')
    driver.back()

driver.quit()