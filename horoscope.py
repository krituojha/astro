# horoscope.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

def get_daily_horoscope(sign="aries"):
    url = f"https://www.astrosage.com/horoscope/daily-{sign.lower()}-horoscope.asp"

    options = Options()
    options.add_argument("--headless")  # ✅ headless mode = background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)

        prediction = None
        try:
            # ✅ Get all elements with this class
            elems = driver.find_elements(By.CSS_SELECTOR, "div.ui-large-content.text-justify")
            if elems:
                prediction = elems[0].text.strip()  # First block is main prediction
        except NoSuchElementException:
            prediction = "⚠ Prediction block not found."

        return prediction if prediction else "⚠ Could not extract horoscope."
    finally:
        driver.quit