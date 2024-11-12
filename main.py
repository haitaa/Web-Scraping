import streamlit as st
import pandas as pd
import io
import random
import mysql.connector

from scrape import scrape_website, split_dom_content, extract_body_content, clean_and_process_text
from parse import parse_with_ollama
from word_edit import metni_duzenle
from db_utils import save_words_to_sql
from db_utils import fetch_data_from_db, fetch_table_names
from crawler import search_google_selenium
from save_loc import save_to_csv
from utils import find_zodiac_in_topic

PAGES = {
  "Ana Sayfa": "home",
  "Online Crawler": "crawler",
  "Yapay Zeka Kullanarak Veri Çekme ve İşleme": "scraping",
  "Veri İndirme": "download",
}


# Navbar
st.sidebar.title("Navbar")
page = st.sidebar.radio("Sayfa Seçin", options=list(PAGES.keys()))

if page == "Ana Sayfa":
  st.title("Web Scraping...")
elif page == "Yapay Zeka Kullanarak Veri Çekme ve İşleme":
  st.title("AI Web Scraper")
  url = st.text_input("Enter a Website URL: ")

  json = {}

  if st.button("Scrape Site"):
    st.write("Scraping the website...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_and_process_text(body_content)

    st.session_state.dom_content = cleaned_content
    
    with st.expander("View DOM Content"):
      st.text_area("DOM Content", cleaned_content, height=300)

    words = metni_duzenle(cleaned_content)

    json = {"kelimeler": words}

  if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
      if parse_description:
        st.write("Parsing content...")

        dom_chunks = split_dom_content(st.session_state.dom_content)
        result = parse_with_ollama(dom_chunks, parse_description)
        st.write(result)
        st.success("Content parsed successfully!")

  st.markdown("----------------------------------------------------------------")
  st.subheader("JSON Kayıtları")

  if len(json) == 0: 
    st.json({"Hata": "Veri bulunamadı."})
  else: 
    st.json(json["kelimeler"])
    save_words_to_sql(list(json["kelimeler"]))

elif page == "Veri İndirme":
  st.title("Veri İndirme")
  st.markdown("### Veritabanından Veri Seçimi")

  # Kullanıcıya selectbox ile hangi tabloyu seçmek istediğini soralım
  tables = fetch_table_names()  # Burada veritabanındaki tabloları güncelleyebilirsiniz
  selected_table = st.selectbox("Veri Tablosu Seçin", tables)

  # SQL Sorgusu
  query = f"SELECT * FROM {selected_table}"

  # Veritabanından verileri çekme
  if selected_table:
    df = fetch_data_from_db(query)

    # Dataframe'i göster
    # st.write(f"{selected_table} Tablosu", df) # TODO: Tabloyu değiştir
    # Pandas styling
    if 'word' in df.columns:
      styled_df = df.style.applymap(lambda x: 'background-color: yellow' if isinstance(x, str) else '', subset=['word'])
      st.dataframe(styled_df)
    else:
      st.write(f"Veritabanında '{selected_table}' tablosunda veri bulunamadı.")


    if st.button("Dosyayı Dönüştür ve İndir"):
      # Excel dosyalasına dönüştürme
      towrite = io.BytesIO()
      with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
      towrite.seek(0)

      # CSV format
      towrite_csv = io.BytesIO()
      df.to_csv(towrite_csv, index=False)
      towrite_csv.seek(0)

      # JSON format
      json_data = df.to_json(orient="records")
      towrite_json = io.BytesIO(json_data.encode("utf-8"))

      with st.expander("Dosyayı Türünü Seç ve İndir"):
        st.download_button(
          label="Excel Dosyasını İndir",
          data=towrite,
          file_name="veri.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.download_button(
          label="CSV Dosyasını İndir",
          data=towrite_csv,
          file_name="veri.csv",
          mime="text/csv"
        )

        st.download_button(
          label="JSON Dosyasını İndir",
          data=towrite_json,
          file_name="veri.json",
          mime="application/json"
        )
elif page == "Online Crawler":
  st.title("Online Crawler")
  topic = st.text_input("Ne hakkında veri çekmek istiyorsun?")

  json = {}

  if st.button("Ara"):
    if topic:
      st.write(f"'{topic} hakkında Google'da arama yapılıyor...'")
      current_url, html_body = search_google_selenium(topic)
      body_content = extract_body_content(html_body)
      cleaned_content = clean_and_process_text(body_content)

      burclar = [
        "Koç", "Boğa", "Ikizler", "Yengeç", "Aslan", "Başak",
        "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"
      ]

      zodiac = find_zodiac_in_topic(topic, burclar)


      # Temizlenmiş içerik ve kelimeleri session_state'e kaydediyoruz
      st.session_state.dom_content = cleaned_content
      words = metni_duzenle(cleaned_content)

      st.subheader(f"zodiac: {zodiac.capitalize()}") 

      json = {"kelimeler": words}

      st.markdown("----------------------------------------------------------------")
      st.subheader("JSON Kayıtları")

      if len(json) == 0: 
        st.json({"Hata": "Veri bulunamadı."})
      else: 
        st.json(list(json["kelimeler"]))
        words = list(json["kelimeler"])

        st.subheader("Temizlenmiş İçerik")
        st.text_area("", cleaned_content, height=300)

        try:
          if zodiac != "":
            save_words_to_sql(list(json["kelimeler"]), zodiac_name=zodiac)
          else: 
            save_words_to_sql(list(json["kelimeler"]), zodiac_name="words")
        except mysql.connector.Error as error:
          print(f"Kelimeleri veritabanına kaydedilirken hata oluştu: {error}")
        

        # Kelimeleiri DataFrame'e dönüştür.
        df = pd.DataFrame(words, columns=["Tokenized Words"])

        with st.expander("Tokenize Edilmiş Kelimeleri İndirme Seçenekleri"):
          # CSV indirme butonu
          csv = df.to_csv(index=False).encode("utf8")
          st.download_button(
            label="CSV Dosyasını İndir",
            data=csv,
            file_name="tokenized_words.csv",
            mime="text/csv"
          )

          # Excel indirme butonu   
          towrite = io.BytesIO()
          with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Tokenized Words")
          towrite.seek(0)
          st.download_button(
            label="Excel olarak indir",
            data=towrite,
            file_name="tokenized_words.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          )

          # JSON indirme butonu
          json_data = df.to_json(orient="records", force_ascii=False)
          st.download_button(
            label="JSON olarak indir",
            data=json_data,
            file_name="tokenized_words.json",
            mime="application/json"
          )
      
      with st.expander("Temizlenmiş İçerikleri İndirme Seçenekleri"):
        cleaned_content_list = cleaned_content.split("\n")

        df_cleaned_content = pd.DataFrame(cleaned_content_list, columns=["Cleaned Content"])

        csv = df_cleaned_content.to_csv(index=False).encode("utf-8")
        st.download_button(
          label="CSV Dosyasını Bilgisayara İndir",
          data=csv,
          file_name="cleaned_content.csv",
          mime="text/csv"
        )

        # TODO: Düzelt çalışmıyor
        # if st.button("Geliştirme Dosyasına Kaydet (Henüz Çalışmıyor)"):
        #   save_to_csv(cleaned_content_list)

        #   st.success("Temizlenmiş içerikler geliştirme dosyasına kaydedildi.")


else:
  st.warning("Lütfen bir konu girin.")