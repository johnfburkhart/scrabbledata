import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def setup_driver() -> webdriver.Firefox:
    """Set up the Firefox WebDriver."""
    options = Options()
    options.headless = True  # Run in headless mode for efficiency
    driver = webdriver.Firefox(options=options)
    return driver

def load_games(filename: str) -> list[str]:
    """Load game URLs from a text file."""
    with open(filename, 'r') as f:
        games = f.read().splitlines()
    return games

def click_last_game(driver: webdriver.Firefox) -> None:
    """Navigate to the last game by clicking the final anchor."""
    final_anchor_text = "final"
    anchor = driver.find_element(By.XPATH, f"//a[text()='{final_anchor_text}']")
    anchor.click()

def extract_names_scores(driver: webdriver.Firefox) -> tuple[list[str], list[str]]:
    """Extract player names and scores from the current game."""
    situation_div = driver.find_element(By.CLASS_NAME, "cursituation")
    situation_table = situation_div.find_element(By.TAG_NAME, 'table')
    rows = situation_table.find_elements(By.TAG_NAME, "tr")
    
    names, scores = [], []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        cell_texts = [cell.text for cell in cells]
        names.append(cell_texts[0])
        scores.append(cell_texts[-1])
    
    return names, scores

def extract_dictionary(driver: webdriver.Firefox) -> str:
    """Extract the dictionary type used in the game."""
    p_text = "Dictionary:"
    p_tag = driver.find_element(By.XPATH, f"//p[contains(text(), '{p_text}')]")
    b_tag = p_tag.find_element(By.TAG_NAME, "b")
    return b_tag.text

def extract_num_turns(driver: webdriver.Firefox) -> str:
    """Extract the number of turns from the game."""
    try:
        final_anchor_text = "final"
        final_anchor = driver.find_element(By.XPATH, f"//a[text()='{final_anchor_text}']")
        previous_anchor = final_anchor.find_element(By.XPATH, "preceding-sibling::a[1]")
        return previous_anchor.text
    except Exception as e:
        print(f'An error occurred: {e}')
        return ""
    
def score_extractor(moves_list: list[str]) -> list[int]:
    """Extract scores from the moves list."""
    return [int(move[1:]) for move in moves_list if move and move[0] == "+"]

def extract_scores(driver: webdriver.Firefox) -> list[int]:
    """Extract all scores from the game."""
    click_last_game(driver)
    div = driver.find_element(By.CLASS_NAME, "movessofar")
    table = div.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    cleaned_scores = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        cell_text = [cell.text for cell in cells]
        cleaned_scores.extend(score_extractor(cell_text))
    
    return cleaned_scores

def extract_game_metadata(driver: webdriver.Firefox, game_url: str, meta_data: dict) -> None:
    """Extract metadata for a single game and update the meta_data dictionary."""
    driver.get(game_url)
    click_last_game(driver)

    names, scores = extract_names_scores(driver)
    meta_data["PlayerOne"].append(names[0])
    meta_data["PlayerTwo"].append(names[1])
    meta_data["ScorePlayerOne"].append(scores[0])
    meta_data["ScorePlayerTwo"].append(scores[1])

    meta_data["Dictionary"].append(extract_dictionary(driver))
    meta_data["NumTurns"].append(extract_num_turns(driver))

    scores = extract_scores(driver)
    meta_data["MaxScore"].append(max(scores))
    meta_data["MinScore"].append(min(scores))
    meta_data["MeanScore"].append(round(np.mean(scores),2))

def scrape_games(games: list[str], limit: int = 50) -> pd.DataFrame:
    """Scrape metadata for a list of games and return as a DataFrame."""
    meta_data = {
        "PlayerOne": [],
        "PlayerTwo": [], 
        "Dictionary": [],
        "ScorePlayerOne": [],
        "ScorePlayerTwo": [],
        "NumTurns": [],
        "MaxScore": [],
        "MinScore": [],
        "MeanScore": []
    }

    driver = setup_driver()
    try:
        for game in games[:limit]:
            extract_game_metadata(driver, game, meta_data)
    finally:
        driver.quit()

    return pd.DataFrame(meta_data)

def save_metadata_to_csv(data: pd.DataFrame, filename: str) -> None:
    """Save the metadata DataFrame to a CSV file."""
    data.to_csv(filename, index=False)

if __name__ == "__main__":
    games = load_games("game_list.txt")
    game_metadata = scrape_games(games, limit=1000)
    save_metadata_to_csv(game_metadata, "games_metadata.csv")
    print("Scraping complete and data saved to games_metadata.csv.")
