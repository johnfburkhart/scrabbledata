import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


# Load the games
games = []
with open("game_list.txt", 'r') as f:
    for line in f:
        games.append(line)
    f.close()

# Dictionary for data
meta_data = {
    "PlayerOne": [],
    "PlayerTwo": [], 
    "Dictionary":[],
    "ScorePlayerOne":[],
    "ScorePlayerTwo":[],
    "NumTurns":[],
    "MaxScore":[],
    "MinScore": []
}

driver = webdriver.Firefox()

# Skip to the end of the game
def last_anchor() -> None:
    # Click to last game
    final_anchor_text = "final"
    anchor = driver.find_element(By.XPATH, f"//a[text()='{final_anchor_text}']")
    anchor.click()

    return None

# Extract the name and final score of players in a game
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


def get_num_turns() -> str:
    # Click to last game
    try:
        final_anchor_text = "final"
        final_anchor = driver.find_element(By.XPATH, f"//a[text()='{final_anchor_text}']")
        previous_anchor = final_anchor.find_element(By.XPATH, "preceding-sibling::a[1]")
        num_turns = previous_anchor.text

    except Exception as e:
        print(f'An error occured {e}')

    return(num_turns)

# Extract scores from 'movessofar' list
def score_extracter(moves_list) -> list[int]:
    scores = []
    for move in moves_list:
        if move != '': 
            if move[0] == "+":
                scores.append(int(move[1:]))
    return scores

def get_scores() -> list[int]:
    last_anchor()
    # Select 'movessofar' div
    div = driver.find_element(By.CLASS_NAME, "movessofar")
    # Find table within moves div
    table = div.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    cleaned_scores = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        cell_text = [cell.text for cell in cells]
        game_scores = score_extracter(cell_text)
        for turn in game_scores:
            cleaned_scores.append(turn)
    
    return(cleaned_scores) 


# Get the maximum scoring play 
def get_max_score() -> int:
    # Get all score
    scores = get_scores()
    return(max(scores))

def get_min_score() -> int:
    scores = get_scores()
    return(min(scores))

for game in games[:10]:
    driver.get(game)
    last_anchor()

    # Insert names and score
    names, scores = names_score()
    meta_data["PlayerOne"].append(names[0])
    meta_data["PlayerTwo"].append(names[1])
    meta_data["ScorePlayerOne"].append(scores[0])
    meta_data["ScorePlayerTwo"].append(scores[1])

    # Insert dictionary type 
    dictionary_type = get_dictionary()
    meta_data["Dictionary"].append(dictionary_type)

    # Insert num turns
    meta_data["NumTurns"].append(get_num_turns())

    # Insert max score
    meta_data["MaxScore"].append(get_max_score())

    # Insert min score
    meta_data["MinScore"].append(get_min_score())



data = pd.DataFrame(meta_data)
data.to_csv("games_metadata.csv", index = False)

# Meta data fields
# identifer: self explanatory
# mean play: average score of each play
# min play: lowest point play
# max player: yep