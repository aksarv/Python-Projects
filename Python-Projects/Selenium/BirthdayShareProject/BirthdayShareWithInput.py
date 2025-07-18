"""
Made this since if you choose 23 people it's more likely than not that at least two will share a birthday
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import random
import time

names = []

print("You need to enter 23 names for this to work. Please be accurate with celebrity names for best results.")
for i in range(23):
    get_name = input(f"Enter a name ({23 - i} remaining): ")
    names.append(get_name)

service = Service(executable_path="path/to/chromedriver")
driver = webdriver.Chrome(service=service)

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

dob = []

disabled_cookies = False

try:
    for j, name in enumerate(names):
        time.sleep(random.uniform(3, 7))

        print(f"Person {j + 1} out of {len(names)} ({name})...")
        url = "https://www.famousbirthdays.com"
        driver.get(url)
        
        if not disabled_cookies:
            try:
                # Switch to iframe if necessary
                WebDriverWait(driver, 20).until(
                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='SP Consent Message']"))
                )

                # Dismiss the cookies popup
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".message-button.sp_choice_type_11"))
                ).click()

                print("Cookies popup dismissed.")

                disabled_cookies = True
                
                # Switch back to the main content
                driver.switch_to.default_content()

            except Exception as e:
                print("Cookies popup not found or already dismissed:", e)

        # Interact with the search box
        search_box = driver.find_element(By.ID, "main-search")
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".type-16-18"))
        )

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')

        links = soup.find_all('a')
        month1 = ""
        day = ""
        year = ""
        found_d_m = False
        for link in links:
            href = link.get('href')
            for month in months:
                if href.startswith("/" + month) and not found_d_m:
                    month1, day = link.text.strip().split(" ")
                    day = int(day)
                    found_d_m = True
            if href.startswith("/year/"):
                try:
                    year = int(link.text.strip())
                except ValueError:
                    year = int(link.text.strip().split(" ")[2][:4])

        dob.append([day, month1, year, name, random.randint(1, 10000000000)])

    flag = False
    first_name_dob = []
    second_name_dob = []
    for d in dob:
        for e in dob:
            if d[4] != e[4]:
                if d[0] == e[0] and d[1] == e[1]:
                    flag = True
                    first_name_dob = [d[3], d[0], d[1], d[2]]
                    second_name_dob = [e[3], e[0], e[1], e[2]]
    if flag:
        print(f"Two people do share a birthday: {first_name_dob[0]} (born {first_name_dob[1]} {first_name_dob[2]}, {first_name_dob[3]}) and {second_name_dob[0]} (born {second_name_dob[1]} {second_name_dob[2]}, {second_name_dob[3]}).")
    else:
        print("None of these people share a birthday.")
    
finally:
    driver.quit()
