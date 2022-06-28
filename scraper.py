import os
import time
import json
import signal
import inspect
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from colorama import init, Fore

login_url = "https://www.olx.pl/konto/"
saved_searches_url = "https://www.olx.pl/obserwowane/wyszukiwania/"
profile_url = "https://www.olx.pl/d/mojolx/#login"
non_search_buttons = 4

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='OLX deals watcher build with Selenium')
parser.add_argument('browser', nargs='?', default="chrome",
                    help='Browser that should be used for this session (default: chrome)')
parser.add_argument('-dh', '--disable_headless', action='store_true',
                    help='Disables headless mode')
parser.add_argument('-v', '--verbose',
                    help='Disables headless mode')
parser.add_argument('-o', '--output', type=str, required=False, default="data", 
                    help='Specify the output file filename')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Shows debug messages like refresh information')

args = parser.parse_args()

# Cosmetic
init(autoreset=True)        # initialise Colorama
if (args.verbose): os.system('cls||clear')     # clear terminal before executing

if (args.debug == True):
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
        if (args.disable_headless == True):
            options.add_argument("window-size=900,900")
        else:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if (args.verbose): print(Fore.GREEN + "WebDriver started")

    case "firefox":      # Firefox
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager

        options = webdriver.FirefoxOptions()
        options.add_argument("--mute-audio")
        if (args.disable_headless == True):
            options.add_argument("window-size=900,900")
        else:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        if (args.verbose): print(Fore.GREEN + "WebDriver started")

# Log into to OLX
if (args.verbose): print(Fore.CYAN + "Attempting a login...")
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

time.sleep(2)   # Wait for login to finish, good enough
# while expected_conditions.url_to_be(profile_url) != True: 
#     time.sleep(0.5)
if (args.verbose): print(Fore.CYAN + "Login complete")

driver.get(saved_searches_url)
MEGA_AD = {
    "num_of_observed_ads": len(driver.find_elements(By.CLASS_NAME, "observedsearch")),
}

if (args.verbose): print(Fore.LIGHTMAGENTA_EX + "Observed searches (" + str(MEGA_AD["num_of_observed_ads"]) + "): ")
for i in range(MEGA_AD["num_of_observed_ads"]):
    num_of_ads_full = driver.find_elements(By.CLASS_NAME, "fleft")[non_search_buttons + 2*i + 1].get_attribute("innerText")
    ad = {
        "query": driver.find_elements(By.CLASS_NAME, "is-query")[i].get_attribute("innerText"),
        "number_of_ads": num_of_ads_full[num_of_ads_full.find(':') + 2:num_of_ads_full.find(':') + 3],
        "url": driver.find_elements(By.CLASS_NAME, "searchLink")[i].get_attribute("href")
    }

    if (args.verbose): print(ad["query"] + ": " + ad["number_of_ads"])
    MEGA_AD[i] = ad

if (args.verbose): print(MEGA_AD)
file = open(f"{args.output}.json", 'w')
file.write(json.dumps(MEGA_AD))
file.close()