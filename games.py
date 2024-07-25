from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()

url = "https://www.cross-tables.com/annolistself.php"
driver.get(url)
driver.implicitly_wait(5)

# Locate the table and find all the rows 
table = driver.find_element(By.ID, "xtdatatable")
rows = table.find_elements(By.TAG_NAME, 'tr')

games = []
for row in rows[1:]:
    # Locate the anchor tag within the row
    anchor = row.find_element(By.TAG_NAME, "a")
    href = anchor.get_attribute('href') 
    games.append(href)

filename = "game_list.txt"
with open(filename, 'w') as f:
    for item in games:
        f.write(f"{item}\n")
