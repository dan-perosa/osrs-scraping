from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pandas as pd

# def check_monster_in_xlsx(monster_name):
#     print(monster_name)
#     try:
#         test_df = pd.read_excel('osrs_monsters.xlsx', engine='openpyxl')
#     except:
#         return False
    
#     print(test_df['Monster name'].values)
#     return monster_name in test_df['Monster name'].values

def open_url_in_chrome(url):
    
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options) 
    driver.get(url)
    
    # entra em cada range de lvl
    bestiary_list = driver.find_element(by=By.CLASS_NAME, value='div-col')
    ul_bestiary_list = bestiary_list.find_element(By.TAG_NAME, value='ul')
    li_bestiary_list = ul_bestiary_list.find_elements(By.TAG_NAME, value='a')
    li_bestiary_list[0].click()
    driver.implicitly_wait(5)
    
    # encontra os headers da tabela
    complete_monster_table = driver.find_element(by=By.TAG_NAME, value='table')
    complete_monster_table_headers = complete_monster_table.find_elements(by=By.TAG_NAME, value='th')
    
    header_names = []
    monster_row_data = {}
    all_monsters_data = []
    
    for header in complete_monster_table_headers:
        if header.text != '':
            header_names.append(header.text)
        else:
            title = header.find_element(by=By.TAG_NAME, value='img')
            header_names.append(title.get_dom_attribute('alt'))

            
    # encontra os valores
    table_rows = complete_monster_table.find_elements(by=By.TAG_NAME, value='tr')

    for index, table_row in enumerate(table_rows):
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
                    found_i_tag = data.find_element(by=By.TAG_NAME, value='i')
                except:
                    ...
                if found_i_tag.text != '':
                    found_i = found_i_tag.text
                    monster_name = monster_name + f' ({found_i})'
                    found_i = ''
                
                # if check_monster_in_xlsx(monster_name):
                #     break

                monster_row_data['Monster name'] = monster_name
            # finaliza checagem de tipo de coluna

        if monster_row_data == {}:
            continue
        all_monsters_data.append(monster_row_data)
        print(monster_row_data)
        df = pd.DataFrame(all_monsters_data)
        df.to_excel('osrs_monsters.xlsx', index=False, engine='openpyxl')

    driver.quit()

if __name__ == "__main__":
    url = 'https://oldschool.runescape.wiki/w/Bestiary'
    open_url_in_chrome(url)