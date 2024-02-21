from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_data(driver, player_name, url):
    driver.get(url)
    print(f"Accessing URL: {url}")
    wait = WebDriverWait(driver, 1)
    player_stats = []

    # Extract the team names
    team_names_elements = driver.find_elements(By.CLASS_NAME, 'wf-title-med')
    if len(team_names_elements) >= 2:
        first_team_name = team_names_elements[0].text
        second_team_name = team_names_elements[1].text

    # Extract the scores
    team_scores_elements = driver.find_elements(By.CLASS_NAME, 'match-header-vs-score')
    if len(team_scores_elements) >= 1:
        score_spans = team_scores_elements[0].find_elements(By.TAG_NAME, 'span')
        if len(score_spans) >= 3:
        # Extract scores from the first and third span elements
            first_team_score = int(score_spans[0].text)
            second_team_score = int(score_spans[2].text)

        # Determine winner and loser based on scores
            if first_team_score > second_team_score:
                winning_team = first_team_name
                losing_team = second_team_name
            else:
                winning_team = second_team_name
                losing_team = first_team_name

    try:
        all_map_boxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.vm-stats-gamesnav-item:not([data-game-id="all"])')))
        print(f"Found {len(all_map_boxes)} map boxes to click through.")
    except TimeoutException:
        print(f"Timeout occurred while trying to find map boxes on {url}")
        return player_stats

    for box in all_map_boxes:
        map_name = box.text.strip()
        print(f"Processing map: {map_name}")

        driver.execute_script("arguments[0].click();", box)

        specific_table_selector = f"div.vm-stats-game[data-game-id='{box.get_attribute('data-game-id')}'][style*='display: block']"
        try:
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, specific_table_selector)))
            print(f"Stats section found for map: {map_name}")
            stats_section = driver.find_element(By.CSS_SELECTOR, specific_table_selector)

            player_selector = f".//div[contains(@class, 'text-of') and contains(text(), '{player_name}')]/ancestor::tr"
            try:
                player_row = stats_section.find_element(By.XPATH, player_selector)

                # Extracting specific data
                stats = {
                'Winning team': winning_team,
                'Winning team score': first_team_score if first_team_score > second_team_score else second_team_score,
                'Losing team': losing_team,
                'Losing team score': second_team_score if first_team_score > second_team_score else first_team_score,
                'Map': map_name,  # This should be set from your current loop iterating over maps
                'Player': player_name  # Set this to the player's name you are currently processing
                }
     

                stats_data = player_row.find_elements(By.CSS_SELECTOR, 'td.mod-stat')
                if len(stats_data) >= 7:
                    stats['ACS'] = stats_data[1].text.strip()
                    stats['Kills'] = stats_data[2].text.strip()
                    stats['Deaths'] = stats_data[3].text.strip()
                    stats['Assists'] = stats_data[4].text.strip()
                    stats['KAST'] = stats_data[6].text.strip()
                    stats['ADR'] = stats_data[7].text.strip()

                player_stats.append(stats)
                print(f"Stats collected for {player_name} on map: {map_name}")

            except NoSuchElementException:
                print(f"{player_name} cannot be found in this map {map_name}.")
                continue

        except TimeoutException:
            print(f"Timeout or data not found for map {map_name}.")

    return player_stats