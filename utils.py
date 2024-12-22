import time
import random
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

################################################################################
# Utility Functions
################################################################################

def load_vocabulary(csv_path):
    """
    Load possible guesses from a CSV file that has a 'Word' column.
    Shuffle them to introduce randomness each run.
    """
    df = pd.read_csv(csv_path)
    words = df['Noun'].tolist()
    random.shuffle(words)
    return words

def init_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.whatbeatsrock.com/")
    driver.maximize_window()
    time.sleep(2)
    return driver

def query_game(driver, current_word, candidate_word):
    """
    Queries the game to see if 'current_word' -> 'candidate_word' is correct.
    Returns True if current_word beats candidate_word,
    or False if candidate_word beats current_word.
    
    If True, the page should show the 'next' button.
    If False, the game ends or shows an error => we refresh.
    """
    try:
        # Enter candidate_word
        input_box = driver.find_element(By.TAG_NAME, "input")
        input_box.clear()
        input_box.send_keys(candidate_word)

        go_button = driver.find_element(By.XPATH, "//button[contains(text(), 'GO')]")
        go_button.click()
        time.sleep(4)

        # If we see the 'next' button => current_word -> candidate_word is correct
        next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'next')]")
        next_button.click()
        time.sleep(0.5)
        return True
    except:
        # candidate_word beats current_word => refresh
        try:
            error_message = driver.find_element(By.XPATH, "//h2").text
            print(f"'{candidate_word}' beats '{current_word}': {error_message}")
        except:
            print(f"Unknown error testing {current_word} -> {candidate_word}")

        driver.refresh()
        time.sleep(2)
        return False

################################################################################
# Main Algorithm - Single-Chain Approach (with Fixes)
################################################################################

def build_long_chain(driver, words, threshold=200):
    """
    1. Start from 'rock'.
    2. Pick a random candidate - if success, chain extends. If fail, fallback logic.
    3. Fallback logic:
       - If chain has > 1 node, move backward to find a node w where w->rock is True.
       - If found, truncate chain at w. If not found, try a new candidate (don't crash).
    4. Keep track of the chain, skipping used words.
    5. Continue building until no extension or threshold is reached.
    """

    # A record of which nodes definitely beat rock, or rock definitely beats them
    # Key: node, Value: True = node->rock, False = rock->node
    rock_relations = dict()

    # The chain (path) we maintain. Start with 'rock'.
    chain = ["rock"]

    # Set of used nodes (can't repeat)
    used = set(["rock"])

    def node_beats_rock(node):
        """
        Checks if node->rock. Uses rock_relations for cache if available.
        If not in cache, queries the game: node->rock?
        """
        # !!IF we cache the simulation will not cuaght up with the real game
        # if node in rock_relations:
        #     return rock_relations[node]  # True => node->rock, False => rock->node

        success = query_game(driver, "rock", node)
        rock_relations[node] = success
        return success

    # Candidates pool: everything except "rock"
    candidates = [w for w in words if w.lower() != "rock"]

    # Keep track of the longest chain we've seen so far
    longest_chain = list(chain)

    while True:
        # If we have reached or exceeded threshold, we stop
        if len(chain) >= threshold:
            print(f"Reached threshold of {threshold} with chain length {len(chain)}.")
            longest_chain = chain[:]
            break

        # Randomly pick a new candidate that hasn't been used
        candidate_pool = [c for c in candidates if c not in used]
        if not candidate_pool:
            print("No more candidates available.")
            longest_chain = chain[:]
            break

        next_candidate = random.choice(candidate_pool)

        current = chain[-1]  # The last node in the chain
        success = query_game(driver, current, next_candidate)

        if success:
            # current -> next_candidate
            chain.append(next_candidate)
            used.add(next_candidate)
            print(f"Chain extended: {' -> '.join(chain)}")

            # Update longest chain
            if len(chain) > len(longest_chain):
                longest_chain = chain[:]
        else:
            # next_candidate -> current
            print(f"Chain failed at '{current}' with '{next_candidate}' winning.")

            # If the chain is just ["rock"], don't attempt fallback—just pick another candidate
            if len(chain) == 1:
                print("Chain has only 'rock'. Trying another candidate...")
                continue
            print(f"Current chain: {' -> '.join(chain)}")
            # Otherwise, try fallback from the end of the chain backward
            fallback_index = len(chain) - 1
            found_fallback = False

            while fallback_index >= 0:
                w = chain[fallback_index]
                print(f"Trying to fallback to node '{w}'...")
                # Skip checking 'rock' => not useful to see if rock->rock
                if w.lower() == "rock":
                    fallback_index -= 1
                    continue

                # Check if w->rock
                if node_beats_rock(w):
                    # w->rock means we can start from w again
                    chain = chain[:fallback_index + 1]
                    print(f"Falling back to node '{w}' that can beat rock.")
                    found_fallback = True
                    break
                else:
                    # rock->w => not a fallback
                    fallback_index -= 1

            # If no fallback node found, we won't end the entire loop yet:
            # we just continue to pick another candidate
            if not found_fallback:
                print("No valid fallback node found. Will try a new candidate.")
                continue

    return longest_chain