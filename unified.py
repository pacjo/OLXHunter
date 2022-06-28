import os
import time
import json
import inspect
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions
from colorama import init, Fore

login_url = "https://www.olx.pl/konto/"
saved_searches_url = "https://www.olx.pl/obserwowane/wyszukiwania/"
profile_url = "https://www.olx.pl/d/mojolx/#login"
non_search_buttons = 4

def new_deal(query, number_of_deals, deal_url, notification, mqtt):
    print(Fore.LIGHTRED_EX + datetime.now().strftime("%H:%M:%S") + ": new listing found (" + number_of_deals + "): " + deal_url)
    if (notification):
        notification.notify(
            title="OLX watcher",
            message="New deal available: " + str(number_of_deals),
            # app_icon=f'{file_path}\\assets\\ut_icon.ico'
        )

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='OLX deals watcher built with Selenium')
parser.add_argument('browser', nargs='?', default="chrome",
                    help='Browser that should be used for this session (default: chrome)')
parser.add_argument('-dh', '--disable_headless', action='store_true',
                    help='Disables headless mode')
parser.add_argument('-t', type=int, default=60,
                    help='Change time between comparisons (in seconds)')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Disables headless mode')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Shows debug messages')

args = parser.parse_args()

# Cosmetic
init(autoreset=True)        # initialise Colorama
if (args.verbose and not args.debug): os.system('cls||clear')     # clear terminal before executing

if (args.debug):
    print(Fore.BLUE + "Debugging is enabled, remove \"--debug\" or \"-d\" to disable it")
else:
    os.environ['WDM_LOG_LEVEL'] = '0'

# WebDriver initialization
match args.browser:
    case "chrome":      # Chrome
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--mute-audio")
        if (args.disable_headless):
            options.add_argument("window-size=900,900")
        else:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if (args.verbose or args.debug): print(Fore.GREEN + "WebDriver started")

    case "firefox":      # Firefox
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager

        options = webdriver.FirefoxOptions()
        options.add_argument("--mute-audio")
        if (args.disable_headless):
            options.add_argument("window-size=900,900")
        else:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        if (args.verbose or args.debug): print(Fore.GREEN + "WebDriver started")

# Log into to OLX
if (args.verbose or args.debug): print(Fore.CYAN + "Attempting a login...")
driver.get(login_url)

file = open(f'credentials.json', 'r')
load = json.load(file)
username = load.get('user')
password = load.get('password')
file.close()

driver.find_elements(By.ID, "onetrust-accept-btn-handler")[0].click()
driver.find_elements(By.ID, "userEmail")[0].send_keys(username)
driver.find_elements(By.ID, "userPass")[0].send_keys(password)
driver.find_elements(By.ID, "se_userLogin")[0].click()

# Wait for login to finish
while (driver.current_url != profile_url): time.sleep(1)
if (args.verbose or args.debug): print(Fore.CYAN + "Login complete")

driver.get(saved_searches_url)

MEGA_AD_last = {
        "num_of_observed_ads": len(driver.find_elements(By.CLASS_NAME, "observedsearch")),
    }
MEGA_AD_current = {
        "num_of_observed_ads": len(driver.find_elements(By.CLASS_NAME, "observedsearch")),
    }

time.sleep(2)
while True:
    # Get number of new deals into ad dictionary
    MEGA_AD_last = MEGA_AD_current      # Save last data into another dict (for comparison)
    if (args.verbose or args.debug): print(Fore.MAGENTA + "Observed searches (" + str(MEGA_AD_current["num_of_observed_ads"]) + "): ")
    for i in range(MEGA_AD_current["num_of_observed_ads"]):
        num_of_ads_full = driver.find_elements(By.CLASS_NAME, "fleft")[non_search_buttons + 2*i + 1].get_attribute("innerText")
        ad = {
            "query": driver.find_elements(By.CLASS_NAME, "is-query")[i].get_attribute("innerText"),
            "number_of_ads": num_of_ads_full[num_of_ads_full.find(':') + 2:num_of_ads_full.find(':') + 3],
            "url": driver.find_elements(By.CLASS_NAME, "searchLink")[i].get_attribute("href")
        }

        if (args.verbose or args.debug): print(Fore.LIGHTMAGENTA_EX + ad["query"] + ": " + ad["number_of_ads"])
        MEGA_AD_current[i] = ad
    if (args.debug): print(MEGA_AD_current)

    # Check for changes (new deals)
    for i in range(min(MEGA_AD_last["num_of_observed_ads"], MEGA_AD_current["num_of_observed_ads"])):
        try:
            if (int(MEGA_AD_current[str(i)]["number_of_ads"]) > int(MEGA_AD_last[str(i)]["number_of_ads"])):    # New deal detected
                # print(Fore.GREEN + datetime.now().strftime("%H:%M:%S") + ": new listing found (" + MEGA_AD_current[str(i)]["number_of_ads"] + "): " + MEGA_AD_current[str(i)]["url"])
                new_deal(int(MEGA_AD_current[str(i)]["query"]), int(MEGA_AD_current[str(i)]["number_of_ads"]), int(MEGA_AD_current[str(i)]["url"]), True, True) # change True to argument
            else: print(Fore.LIGHTWHITE_EX + datetime.now().strftime("%H:%M:%S") + ": no new listings, keep looking")
        except KeyError:        # It's the first loop, should be safe to ignore
            pass

    driver.refresh()
    time.sleep(args.t)