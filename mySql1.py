import mysql.connector

def veritabani_baglanti():
    try:
        print("🔌 MySQL bağlantısı deneniyor...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Baris3642.",
            database="denemedb"  # GÜNCELLENDİ
        )
        print("✅ MySQL bağlantısı kuruldu.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Veritabanı bağlantı hatası: {err}")
        return None

if __name__ == "__main__":
    conn = veritabani_baglanti()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stoklar (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stok_no VARCHAR(100),
                stok_adi VARCHAR(255),
                stok_miktari INT,
                stok_mensei VARCHAR(255),
                stok_cinsi VARCHAR(255),
                stok_durumu VARCHAR(255)
            )
            """)
            conn.commit()
            print("🟢 Tablo başarıyla oluşturuldu.")
        except Exception as e:
            print("❌ Tablo oluşturulurken hata:", e)
        finally:
            cursor.close()
            conn.close()
