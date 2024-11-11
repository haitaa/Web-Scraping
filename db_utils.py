import mysql.connector
import pandas as pd

def connect_to_server():
  """MySQL veritabanına bağlanır ve bir cursor döner."""
  try:
    conn = mysql.connector.connect(
      host="localhost",         # Veritabanı hostu (genellikle localhost)
      user="root",         # Kullanıcı adı
      password="rootpassword", # Şifre
      database="horoscope_db"   # Veritabanı adı
    )

    cursor = conn.cursor()
    print("Veritabanına başarıyla bağlanıldı.")
    return conn, cursor
  except mysql.connector.Error as error:
    print(f"Bağlantı hatası: {error}")
    return None, None


def disconnect_from_server(conn, cursor):
  """Veritabanı bağlantısını kapatır."""
  try:
    cursor.close()
    conn.close()
    print("Veritabanı bağlantısı kapatıldı.")
  except mysql.connector.Error as error:
    print(f"Bağlantı kapatılırken hata oluştu: {error}")

def save_words_to_sql(word_list):
  conn, cursor = connect_to_server()

  if conn is None or cursor is None:
    print("Veritabanına bağlanılamadı. İşlem iptal ediliyor.")
    return

  for word in word_list:
    try:
      cursor.execute("INSERT IGNORE INTO words (word) VALUES (%s)", (word,))
    except mysql.connector.Error as error:
      print(f"Kelime kaydedilirken hata oluştu: {error}")
      continue
  
  conn.commit()
  disconnect_from_server(conn, cursor)

  print("Kelimeler başarıyla kaydedildi.")


def fetch_data_from_db(query):
  conn, cursor = connect_to_server()

  cursor.execute(query)
  result = cursor.fetchall()

  # Kolon isimlerini almak
  column_names = [desc[0] for desc in cursor.description]

  # Veriyi Pandas DataFrame'e dönüştürme
  df = pd.DataFrame(result, columns=column_names)

  disconnect_from_server(conn, cursor)
  return df

def fetch_table_names():
  conn, cursor = connect_to_server()
  cursor.execute("SHOW TABLES")
  tables = cursor.fetchall()
  disconnect_from_server(conn, cursor)
  return [table[0] for table in tables]
  
  