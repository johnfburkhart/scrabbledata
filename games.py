from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def setup_driver() -> webdriver.Firefox:
    """Set up the Firefox WebDriver."""
    options = Options()
    options.headless = True 
    driver = webdriver.Firefox(options=options)
    return driver


def next_page(driver) -> None:
    """Click the 'next' button to navigate to new page"""
    next_button = driver.find_element(By.CLASS_NAME, 'next')
    next_button.click()


def extract_game_links(driver: webdriver.Firefox) -> list[str]:
    """Extract game links from the current page."""
    table = driver.find_element(By.ID, "xtdatatable")
    rows = table.find_elements(By.TAG_NAME, 'tr')
    games = []

    for row in rows[1:]:  # Skip the header row
        anchor = row.find_element(By.TAG_NAME, "a")
        href = anchor.get_attribute('href')
        games.append(href)

    return games

def save_to_file(filename: str, data: list[str]) -> None:
    """Save the list of data to a text file."""
    with open(filename, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

def game_scraper(num_games: int) -> list[str]:
    """
    This function scrapes the hrefs for each scrabble game listed
    on the website. It writes a text file containing each of these
    hrefs and also returns a list of the hrefs for the metadata 
    script to iterate over. 
    """
    driver = setup_driver()

    try:
        url = "https://www.cross-tables.com/annolistself.php"
        driver.get(url)
        driver.implicitly_wait(5)
        
        all_games = []
        while len(all_games) < num_games:
            games = extract_game_links(driver)
            all_games.extend(games)
            if len(all_games) >= num_games:
                break
            next_page(driver)
        
        all_games = all_games[:num_games]
        save_to_file("game_list.txt", all_games)
        return all_games
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    num_games = 1000  # Set the desired number of games to scrape
    game_links = game_scraper(num_games)
    print(f"Scraped {len(game_links)} game links.")