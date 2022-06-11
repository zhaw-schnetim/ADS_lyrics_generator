import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def scrape_song_artist(args):
    name = args.get("name")
    opts = webdriver.ChromeOptions()
    opts.headless = True
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opts)

    driver.get('https://hitparade.ch/search.asp?cat=s&search=' + name.replace("_", "+"))
    time.sleep(5)
    driver.find_element(by=By.XPATH, value='/html/body/div[10]/div[4]/div[3]/div/table/tbody[2]/tr[1]/td[1]/a').click()

    artist_song = driver.find_element(by=By.XPATH, value='/html/body/div[10]/div[3]/div/h1').text
    year = driver.find_element(by=By.XPATH, value='/html/body/div[10]/div[5]/div[2]/div/div[2]').text

    f = open('results/information/' + name + '/result.json')
    data = json.load(f)
    data["artist_song"] = artist_song.replace("\u2013", "-")
    data["year"] = year

    with open("results/information/" + name + "/result.json", "w") as fp:
        json.dump(data, fp)
