import mysql.connector

from db_utils import connect_to_server, disconnect_from_server

# MySQL'e bağlan
conn, cursor = connect_to_server()

if conn and cursor:
  try:
    # Yıl Tablosu Oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Years (
        year_id INT AUTO_INCREMENT PRIMARY KEY,
        year INT NOT NULL
    );
    """)

    # Aylar Tablosu Oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Months (
        month_id INT AUTO_INCREMENT PRIMARY KEY,
        year_id INT NOT NULL,
        month_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (year_id) REFERENCES Years(year_id)
    );
    """)

    # Günler Tablosu Oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Days (
        day_id INT AUTO_INCREMENT PRIMARY KEY,
        month_id INT NOT NULL,
        day_number INT NOT NULL,
        day_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (month_id) REFERENCES Months(month_id)
    );
    """)

    # Burç Yorumları Tablosu Oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS HoroscopeComments (
        comment_id INT AUTO_INCREMENT PRIMARY KEY,
        day_id INT NOT NULL,
        zodiac_sign VARCHAR(255) NOT NULL,
        comment_text TEXT NOT NULL,
        FOREIGN KEY (day_id) REFERENCES Days(day_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) UNIQUE NOT NULL
    );
    """)

    # Değişiklikleri kaydet
    conn.commit()
  except mysql.connector.Error as error:
    print(f"Tablolar oluşturulurken hata oluştu: {error}")
  finally:
    print("Tablolar başarıyla oluşturuldu!")
    disconnect_from_server(conn, cursor)

