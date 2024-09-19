from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd

url = 'https://oldschool.runescape.wiki/w/Quests/List'

options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options) 
driver.get(url)

complete_quests_list = []

all_page_tables = driver.find_elements(by=By.TAG_NAME, value='table')
filtered_tables: list[WebElement] = []
# filtra apenas as 3 tabelas necessarias
for table in all_page_tables:
    if table.get_dom_attribute('class') == 'wikitable floatright align-center-1 align-left-2':
        continue
    filtered_tables.append(table)

# encontra os headers da tabela
quest_table_headers = filtered_tables[0].find_elements(by=By.TAG_NAME, value='th')
header_names = []
for header in quest_table_headers:
    if header.text != '':
        header_names.append(header.text)
    else:
        header_names.append('Quest Points')

filtered_header_names = header_names[1:-1]

# encontra lista com todas as linhas da tabela
for table in filtered_tables:
    all_table_rows = table.find_elements(by=By.TAG_NAME, value='tr')
    # itera cada linha da tabela
    for row_index, row in enumerate(all_table_rows):
        quest = {}
        if row_index == 0 or row_index == (len(all_table_rows) - 1):
            continue
        row_tds = row.find_elements(by=By.TAG_NAME, value='td')
        # itera cada td
        for td_index, td in enumerate(row_tds):
            if td_index == 0 and td.text.isdigit():
                continue

            if table.get_dom_attribute('class') == 'wikitable lighttable sortable qc-active oqg-table sticky-header align-center-4 autosort=1,a jquery-tablesorter':
                if td_index == 2:
                    print('antes', quest)
                    quest[filtered_header_names[td_index]] = td.text
                    quest['Quest Points'] = 0
                    print('deopis', quest)
                    continue
                quest[filtered_header_names[td_index]] = td.text
                print('finalzin', quest)
                continue
                
            if '#' in td.text:
                quest[filtered_header_names[td_index-1]] = td.text.split(',')[0]
                continue
            quest[filtered_header_names[td_index-1]] = td.text
            
        complete_quests_list.append(quest)
            
df = pd.DataFrame(complete_quests_list)
df.to_excel('osrs_quests.xlsx', index=False, engine='openpyxl')
    

                