from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pandas as pd
import json
import os


# options = ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome() 
driver.get('https://oldschool.runescape.wiki/w/Bestiary')

# entra em cada range de lvl
bestiary_list = driver.find_element(by=By.CLASS_NAME, value='div-col')
ul_bestiary_list = bestiary_list.find_element(By.TAG_NAME, value='ul')
li_bestiary_list = ul_bestiary_list.find_elements(By.TAG_NAME, value='a')
print(len(li_bestiary_list))

for index, level_range in enumerate(li_bestiary_list):
    bestiary_list = driver.find_element(by=By.CLASS_NAME, value='div-col')
    ul_bestiary_list = bestiary_list.find_element(By.TAG_NAME, value='ul')
    li_bestiary_list = ul_bestiary_list.find_elements(By.TAG_NAME, value='a')
    print(li_bestiary_list[index].text)
    li_bestiary_list[index].click()

    # encontra os headers da tabela após clicar no range de lvl
    complete_monster_table = driver.find_element(by=By.TAG_NAME, value='table')
    complete_monster_table_headers = complete_monster_table.find_elements(by=By.TAG_NAME, value='th')
    driver.back()