from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException

#Method used to scrape the statistics from the tables inside each match link
def scrape_data(driver, player_name, url):
    driver.get(url)
    print(f"Accessing URL: {url}")
    wait = WebDriverWait(driver, 1)
    player_stats = []

    # Extract the match date
    try:
        date_element = driver.find_element(By.CLASS_NAME, 'moment-tz-convert')
        match_date = date_element.get_attribute('data-utc-ts')
        print(f"Match date extracted: {match_date}")
    except NoSuchElementException:
        print("Match date not found.")
        match_date = None
    
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

                # Find the abbreviation element within the player's row
                team_abbr_element = player_row.find_element(By.CSS_SELECTOR, 'div.ge-text-light')
                player_team_abbr = team_abbr_element.text.strip()

                # Find the agent's image element within the player's row
                agent_img_element = player_row.find_element(By.CSS_SELECTOR, 'td.mod-agents img')
                agent_name = agent_img_element.get_attribute('alt').strip()  # Extract the agent's name from the alt attribute

                # In your main scrape_data function:
                player_team = match_team(player_team_abbr, [first_team_name, second_team_name])
                opposite_team = first_team_name if player_team == second_team_name else second_team_name

                # Extracting specific data
                stats = {
                'Agent' : agent_name,
                'Player team': player_team,
                'Opposite team': opposite_team,
                'Winning team': winning_team,
                'Winning team score': first_team_score if first_team_score > second_team_score else second_team_score,
                'Losing team': losing_team,
                'Losing team score': second_team_score if first_team_score > second_team_score else first_team_score,
                'Map': map_name, 
                'Player': player_name,
                'Date': match_date 
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



#Function used to identify which team is the opposite
def match_team(abbreviation, team_names):
    abbreviation = abbreviation.lower().replace(' ', '')
    best_match = team_names[0]  # Initialize to the first team name by default
    best_score = -float('inf')  # Initialize to negative infinity
    
    for team in team_names:
        clean_team_name = team.lower().replace(' ', '')
        score = 0
        j = 0
        
        # Check if each character in the abbreviation appears in sequence in the team name
        for char in abbreviation:
            if char in clean_team_name[j:]:
                j = clean_team_name.index(char, j) + 1
                score += 1
            else:
                score -= 1
        
        # Update the best match if this score is higher than the previous best
        if score > best_score:
            best_match = team
            best_score = score
        elif score == best_score and len(team) < len(best_match):
            best_match = team
    
    return best_match
