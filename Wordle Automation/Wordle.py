from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/games/wordle/index.html")

button_rejectAll = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid = "Reject all-btn"]')))
button_rejectAll.click()
button_continue = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.purr-blocker-card__button')))
button_continue.click()
button_play = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid = "Play"]')))
button_play.click()
button_close = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.Modal-module_closeIcon__TcEKb')))
button_close.click()

start_word = ["o","u","i","j","a", "↵"]
random_word = ""
for word in start_word:

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[data-key = "{word}"]')))
    button.click()
    time.sleep(0.5)

checkRow1 = ["1st letter", "2nd letter", "3rd letter", "4th letter", "5th letter"]
resultsRow1 = {}
position = 1
for check in checkRow1:    
    outer_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Row 1"]'))
    )
    inner_div = WebDriverWait(outer_div, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//div[contains(@aria-label, "{check}")]'))
    )
    value = inner_div.get_attribute("data-state") 
    text = inner_div.text  
    resultsRow1[check] = {"text": text, "value": value, "position": position}
    position = position + 1
    time.sleep(0.5)

absent_list = []
correct_dict = {}
present_dict = {}
def row1_lists(resultsRow1):
    global absent_list
    global correct_dict
    global present_dict
    for key, value in resultsRow1.items():
        letter = value["text"]
        state = value["value"]  
        position = value["position"]
        if state == "absent":
            absent_list.append(letter.lower())
        if state == "correct":
            correct_dict[key] = {"letter": letter.lower(), "position": position}
        if state == "present":
            present_dict[key] = {"letter": letter.lower(), "position": position}
            

row1_lists(resultsRow1)
# print(f"Absent: {absent_list}")
# print(f"Correct: {correct_dict}")
# print(f"Present: {present_dict}")

def filteredWords():
    global random_word           
    with open('words.txt', 'r') as file:
        words = file.readlines()
        filtered_words = []
        letter_values = {
            'a': 1, 'e': 1, 'i': 1, 'l': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1, 'u': 1,  # 1 point letters
            'd': 2, 'g': 2,  # 2 points letters
            'b': 3, 'c': 3, 'm': 3, 'p': 3,  # 3 points letters
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,  # 4 points letters
            'k': 5,  # 5 points letter
            'j': 8, 'x': 8,  # 8 points letters
            'q': 10, 'z': 10  # 10 points letters
        }
        for word in words:
            word = word.strip()             
            if any(letter in word for letter in absent_list):                
                continue
            if any(word[info["position"] - 1] != info["letter"] for info in correct_dict.values()):
                continue  
            if any(letter not in word for letter, info in present_dict.items()) or any(word[info["position"] - 1] == letter for letter, info in present_dict.items()):
                continue
            filtered_words.append(word)

        word_scores = {}

        for word in filtered_words:
            word_score = sum(letter_values[letter] for letter in word)
            word_scores[word] = word_score
        least_value = min(word_scores.values())
        least_score_words = [word for word, score in word_scores.items() if score == least_value]

        random_word = random.choice(least_score_words)
        # print(f"Words with the least scores ({least_value}):")
        # for word in least_score_words:
        #     print(word)
        
filteredWords()

second_word = list(random_word)
second_word.append("↵")
for word in second_word:

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[data-key = "{word}"]')))
    button.click()
    time.sleep(0.5)
time.sleep(2)

checkRow2 = ["1st letter", "2nd letter", "3rd letter", "4th letter", "5th letter"]
resultsRow2 = {}
position = 1
for check in checkRow2:    
    outer_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Row 2"]'))
    )
    inner_div = WebDriverWait(outer_div, 10).until(
    EC.presence_of_element_located((By.XPATH, f'.//div[contains(@aria-label, "{check}")]'))
    )
    value = inner_div.get_attribute("data-state") 
    text = inner_div.text
    resultsRow2[check] = {"text": text, "value": value, "position": position}
    position = position + 1
    time.sleep(0.5)

def row2_lists(resultsRow2):
    global absent_list
    global correct_dict
    global present_dict
    for key, value in resultsRow2.items():
        letter = value["text"]
        state = value["value"]  
        position = value["position"]
        if state == "absent":
            absent_list.append(letter.lower())
        if state == "correct":
            correct_dict[key] = {"letter": letter.lower(), "position": position}
        if state == "present":
            present_dict[key] = {"letter": letter.lower(), "position": position}
            

row2_lists(resultsRow1)

input("Press Enter to stop the program...")

# time.sleep(5)
# driver.quit()

#If absent = remove letter from alphabet
#If correct = add position in dictionary
#If present = make a word with that letter compulsorily next round
