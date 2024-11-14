import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random

# Google araması yapmak ve sonuçlarını almak için fonksiyon
def search_google_selenium(query):
  chrome_driver_path = "./chromedriver"
  options = webdriver.ChromeOptions()
  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
  options.add_argument("--headless")
  options.add_argument("--disable-gpu")

  driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

  try:
    # Google'ı açma
    driver.get("https://www.google.com")

    # Arama kutusuna query (konu) yazma
    search_box = WebDriverWait(driver, 2).until(
          EC.presence_of_element_located((By.NAME, "q"))
      )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN) 

    search_results = WebDriverWait(driver, 2).until(
      EC.presence_of_all_elements_located((By.XPATH, '//h3/ancestor::a'))
    )


    if search_results:
      random_site = random.choice(search_results)
      random_site.click()

      html = driver.page_source

      current_url = driver.current_url
      return current_url, html
    else:
      print("Arama sonucu bulunumadı.")
      return None, None
  except Exception as e:
    print(f"Hata oluştu: {e}")
    return None, None
  finally:
    driver.quit()