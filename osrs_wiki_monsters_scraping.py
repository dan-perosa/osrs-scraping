from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pandas as pd
import json
import os
import time


def check_monster_in_xlsx(monster_name):
    print(monster_name)
    try:
        test_df = pd.read_excel('osrs_monsters.xlsx', engine='openpyxl')
    except:
        return False
    
    if 'Monster name' in test_df.columns:
        print(test_df['Monster name'].values)
        return monster_name in test_df['Monster name'].values
    return False

def find_last_xlsx_monster():
    find_index_df = pd.read_excel('osrs_monsters.xlsx', engine='openpyxl')
    return len(find_index_df)

def find_all_xlsx_monsters():
    if os.path.isfile('osrs_monsters.xlsx'):
        print('ntrou')
        df_to_find_existents = pd.read_excel('osrs_monsters.xlsx', engine='openpyxl')
        if (len(df_to_find_existents) > 0):
            to_json_on_existents = df_to_find_existents.to_json(orient='records')
            parsed_existents = json.loads(to_json_on_existents)

            return parsed_existents
    return []

def open_url_in_chrome(url):
    
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options) 
    driver.get(url)
    driver.implicitly_wait(2)
    
    # entra em cada range de lvl
    bestiary_list = driver.find_element(by=By.CLASS_NAME, value='div-col')
    ul_bestiary_list = bestiary_list.find_element(By.TAG_NAME, value='ul')
    li_bestiary_list = ul_bestiary_list.find_elements(By.TAG_NAME, value='a')
    
    all_monsters_data = find_all_xlsx_monsters()
    
    summed_all_number_of_monsters_in_wiki_table = 0
    
    # itera cada range de lvl
    for index, level_range in enumerate(li_bestiary_list):
        
        bestiary_list = driver.find_element(by=By.CLASS_NAME, value='div-col')
        ul_bestiary_list = bestiary_list.find_element(By.TAG_NAME, value='ul')
        li_bestiary_list = ul_bestiary_list.find_elements(By.TAG_NAME, value='a')
        
        for item in li_bestiary_list:
            print(item.text)
        print('entrou na range: ', li_bestiary_list[index].text)

        li_bestiary_list[index].click()
        time.sleep(5)
    
        # encontra os headers da tabela após clicar no range de lvl
        complete_monster_table = driver.find_element(by=By.TAG_NAME, value='table')
        complete_monster_table_headers = complete_monster_table.find_elements(by=By.TAG_NAME, value='th')
        
        header_names = []
        monster_row_data = {}
        
        for header in complete_monster_table_headers:
            if header.text != '':
                header_names.append(header.text)
            else:
                title = header.find_element(by=By.TAG_NAME, value='img')
                header_names.append(title.get_dom_attribute('alt'))

                
        # encontra os valores
        table_rows = complete_monster_table.find_elements(by=By.TAG_NAME, value='tr')
        print(len(table_rows))
        
        number_of_monsters_in_wiki_table = len(table_rows)
        summed_all_number_of_monsters_in_wiki_table += number_of_monsters_in_wiki_table
        
        if (len(all_monsters_data) > 0):
            total_monsters_in_xlsx = find_last_xlsx_monster()
        
        if total_monsters_in_xlsx >= summed_all_number_of_monsters_in_wiki_table:
            print('total_monsters in xlsx maior ou igual que a soma das table')
            already_in_xlsx_monsters = number_of_monsters_in_wiki_table
        
        if total_monsters_in_xlsx < summed_all_number_of_monsters_in_wiki_table:
            print('total_monsters in xlsx menor que a soma das table')
            already_in_xlsx_monsters = number_of_monsters_in_wiki_table - (summed_all_number_of_monsters_in_wiki_table - total_monsters_in_xlsx)
        
        for index, table_row in enumerate(table_rows):
            if index < already_in_xlsx_monsters:
                print('pulando linha ', index)
                continue
            monster_exists = False
            print('fazendo a linha: ', index)
            monster_row_data = {}
            table_data = table_row.find_elements(by=By.TAG_NAME, value='td')
            index_counter = 2
            for data in table_data:
                # começa checagem de tipo de coluna: imagem, nome, member e resto
                images = data.find_elements(by=By.TAG_NAME, value='img')
                if images:
                    image_src = images[0].get_dom_attribute('src')
                    if image_src == '/images/Free-to-play_icon.png?628ce' or \
                    image_src == '/images/Member_icon.png?1de0c':
                        anchor = data.find_element(by=By.TAG_NAME, value='a')
                        is_member = anchor.get_dom_attribute('title')
                        monster_row_data['Members'] = is_member
                    else:
                        monster_row_data['Image'] = 'https://oldschool.runescape.wiki' + image_src

                elif not data.text or data.text == '':
                    monster_row_data[header_names[index_counter]] = 0
                    index_counter += 1
                    
                elif data.text.replace('-', '').isnumeric():
                    monster_row_data[header_names[index_counter]] = data.text
                    index_counter += 1
                    
                else:
                    monster_name_tag = data.find_element(by=By.TAG_NAME, value='a')
                    monster_name = monster_name_tag.text
                    try:
                        found_i_tag = data.find_elements(by=By.TAG_NAME, value='i')
                    except:
                        ...
                    if len(found_i_tag) > 0:
                        found_i = found_i_tag[0].text
                        monster_name = monster_name + f' ({found_i})'
                        found_i = ''
                    
                    if check_monster_in_xlsx(monster_name):
                        monster_exists = True
                        break

                    monster_row_data['Monster name'] = monster_name
                # finaliza checagem de tipo de coluna

            if monster_row_data == {}:
                continue
            if monster_exists:
                print('pulando monstro')
                continue
            
            all_monsters_data.append(monster_row_data)       
            print(monster_row_data)
            if not os.path.isfile('osrs_monsters.xlsx'):
                df = pd.read_excel('osrs_monsters.xlsx', engine='openpyxl')
            else:
                df = pd.DataFrame(all_monsters_data)
            df.to_excel('osrs_monsters.xlsx', index=False, engine='openpyxl')
        
        driver.back()

    driver.quit()

if __name__ == "__main__":
    url = 'https://oldschool.runescape.wiki/w/Bestiary'
    open_url_in_chrome(url)