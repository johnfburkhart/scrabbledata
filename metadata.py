from selenium import webdriver
from selenium.webdriver.common.by import By


# Load the games
games = []
with open("game_list.txt", 'r') as f:
    for line in f:
        games.append(line)
    f.close()

meta_data = {
    "PlayerOne": [],
    "PlayerTwo": [], 
    "Dictionary":[],
    "ScorePlayerOne":[],
    "ScorePlayerTwo":[]
}

driver = webdriver.Firefox()

def last_anchor() -> None:
    # Click to last game
    final_anchor_text = "final"
    anchor = driver.find_element(By.XPATH, f"//a[text()='{final_anchor_text}']")
    anchor.click()

    return None


def names_score() -> tuple:

    # Select 'situation table' and all rows from that table
    situation_div = driver.find_element(By.CLASS_NAME, "cursituation")
    situation_table = situation_div.find_element(By.TAG_NAME, 'table')
    rows = situation_table.find_elements(By.TAG_NAME, "tr")

    # Find all names and scores in rows 
    names = []
    scores = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        # Extract text from each cell and print
        cell_texts = [cell.text for cell in cells]
        name = cell_texts[0]
        score = cell_texts[-1]
        names.append(name)
        scores.append(score)
    
    return((names,scores))


def get_dictionary() -> str:

    # Define the text to look for in the <p> tag
    p_text = "Dictionary:"  # Replace with the actual text you are looking for

    # Locate the <p> tag containing the specified text
    p_tag = driver.find_element(By.XPATH, f"//p[contains(text(), '{p_text}')]")

    # Locate the <b> tag within the located <p> tag
    b_tag = p_tag.find_element(By.TAG_NAME, "b")

    # Extract the text from the <b> tag
    b_text = b_tag.text
    return(b_text)


for game in games[:3]:
    driver.get(game)
    last_anchor()
    names, scores = names_score()
    dictionary_type = get_dictionary()
    meta_data["Dictionary"].append(dictionary_type)
    meta_data["PlayerOne"].append(names[0])
    meta_data["PlayerTwo"].append(names[1])
    meta_data["ScorePlayerOne"].append(scores[0])
    meta_data["ScorePlayerTwo"].append(scores[1])

# Meta data fields
# identifer: self explanatory
# Player 1 name: player who played first
# player 2 name: player who played second
# dictionary type: nwlxx or cswxx
# num turns: number of plays
# score player 1: player 1's score
# score player 2: 
# mean play: average score of each play
# min play: lowest point play
# max player: yep