# tithi.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
#for streamlit cloud 
#for streamlit cloud 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# Path to Chromium on Streamlit Cloud
CHROME_PATH = "/usr/bin/chromium"


def get_today_tithi():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    service = Service("chromedriver.exe")
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--headless")  # ✅ headless mode = background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    #service = Service("chromedriver.exe")
    #driver = webdriver.Chrome(service=service, options=options)
    # for streamlit cloud 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    

    try:
        driver.get("https://www.drikpanchang.com/")
        time.sleep(4)

        tithi = None
        try:
            tithi = driver.find_element(By.XPATH, "//div[contains(text(),'Tithi')]/following-sibling::div").text
        except NoSuchElementException:
            all_text = driver.find_element(By.TAG_NAME, "body").text
            for line in all_text.split('\n'):
                if "Tithi" in line:
                    tithi = line
                    break

        return f"🗓️ आज की तिथि:\n{tithi}" if tithi else "⚠ Could not extract Tithi."
    finally:
        driver.quit()
