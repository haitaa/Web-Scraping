import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import os 
import re
import nltk
import zeyrek
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# İlgili nltk kaynaklarını indiriyoruz
nltk.download('punkt_tab')
nltk.download('stopwords')

# Türkçe için stopwords ve Zeyrek kök bulucuyu ayarlıyoruz
stop_words = set(stopwords.words("turkish"))
analyzer = zeyrek.MorphAnalyzer()

zodiac_signs = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]

def scrape_website(website):
  print("Launching chrome browser...")

  chrome_driver_path = "./chromedriver"
  options = webdriver.ChromeOptions()
  driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

  try: 
    driver.get(website)
    print("Page loaded... ")
    html = driver.page_source

    return html
  finally:
    driver.quit()

def extract_body_content(html_content):
  soup = BeautifulSoup(html_content, "html.parser")
  body_content = soup.body
  if body_content:
    return str(body_content)
  return ""

# dosya ismini belirmeye yarayan fonksiyon
def detect_zodiac(html_content):
  pattern = re.compile(rf"({'|'.join(zodiac_signs)}) Günlük Burç Yorumu", re.IGNORECASE)
  matches = pattern.findall(html_content)

  if matches:
    return matches[0]
  return "Genel"

def clean_and_process_text(html_content):
  soup = BeautifulSoup(html_content, "html.parser")
  for script in soup(["script", "style"]):
    script.extract()


  cleaned_content = soup.get_text(separator="\n")
  cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

  # Tokenizasyon ve stopwords temizleme
  words = word_tokenize(cleaned_content)
  filtered_words = [word for word in words if word.lower() not in stop_words]

  # Zeyrek ile kök bulma işlemi
  processed_words = []
  for word in filtered_words:
    analysis = analyzer.analyze(word)
    if analysis:
      lemma = analysis[0][0].lemma
      processed_words.append(lemma)
    else:
      processed_words.append(word) # Köken bulunamazsa orjinal kelimeyi kullanıyoruz.

  # İşlenmiş kelimleri birleştirip bütünlüğü koruyoruz.
  processed_content = " ".join(processed_words)

  zodiac_name = detect_zodiac(cleaned_content)
  filename = get_unique_filename(zodiac_name)

  save_to_csv(processed_content, filename)

  return processed_content

# def clean_body_content(body_content):
#   soup = BeautifulSoup(body_content, "html.parser")

#   for script in soup(["script", "style"]):
#     script.extract()

#   cleaned_content = soup.get_text(separator="\n")
#   cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

#   zodiac_name = detect_zodiac(cleaned_content)
#   filename = get_unique_filename(zodiac_name)

#   save_to_csv(cleaned_content, filename)
#   return cleaned_content

def get_unique_filename(zodiac_name):
  count = 1
  filename = f"{zodiac_name}.csv"

  while os.path.exists(filename):
    filename = f"{zodiac_name}_{count}.csv"
    count += 1

  return filename

def split_dom_content(dom_content, max_length=6000):
  return [
    dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
  ]

def save_to_csv(content, filename="output.csv"):
  documents_path = os.path.expanduser("/Users/mustafahaita/Documents/AI Webscraper/documents")

  if not os.path.exists(documents_path):
        print("Documents klasörü bulunamadı!")
        return

  # Dosyanın tam yolunu oluştur
  file_path = os.path.join(documents_path, filename)

  with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Content"])

    for line in content.splitlines():
      writer.writerow([line])
