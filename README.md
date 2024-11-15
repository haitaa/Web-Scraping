# Web-Scraping

# README

## Proje Özeti

Bu proje, web scraping (veri kazıma) işlemi yaparak internetten istenilen konularda veri toplamanızı sağlar. Kullanıcılar, bir anahtar kelime veya URL girerek, Google üzerinde rastgele bir web sitesinden bu konuya ait verileri çekebilirler.

## Kullanılan Teknolojiler

- **Python** (Sürüm 3.13.0)
- **Selenium**
- **Streamlit**
- **BeautifulSoup (bs4)**
- **Pandas**
- **Ollama**
- **NLTK**
- **Zeyrek**
- **MySQL** (Veritabanı)

## Projenin Genel İşleyişi

Bu proje, Streamlit üzerinden çalışır. Kullanıcılar, aradıkları konuya dair bir anahtar kelime veya URL girer. Sistem, bu bilgiyi alır ve Google'da rastgele bir web sitesi seçer. Seçilen site üzerinden veri çekilir ve kullanıcıya sunulur.

## Gereksinimler

- Python 3.13.0
- Selenium
- Streamlit
- BeautifulSoup
- Pandas
- Ollama
- NLTK
- Zeyrek
- MySQL

Yukarıdaki bağımlılıkları yükledikten sonra , terminal veya komut satırında şu komutu kullanabilirsiniz:

    pip install -r requirements.txt

Daha sonra projeyi çalıştırmak için aşağıdaki kodu yazmanız yeterli

    streamlit run main.py
