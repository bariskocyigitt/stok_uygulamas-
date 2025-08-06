from mySql1 import veritabani_baglanti
from PyQt6.QtWidgets import *
import traceback

class StokMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STOK MODÜLÜ")
        self.setFixedSize(600, 300)

        gicerik = QVBoxLayout()

        yicerik1 = QHBoxLayout()
        yicerik1.addWidget(QLabel("Ürün Stok No"))
        yicerik1.addWidget(QLabel("Stok Adı"))
        yicerik1.addWidget(QLabel("Stok Miktarı"))

        yicerik2 = QHBoxLayout()
        self.stok_no = QLineEdit()
        self.stok_adi = QLineEdit()
        self.stok_miktari = QLineEdit()
        yicerik2.addWidget(self.stok_no)
        yicerik2.addWidget(self.stok_adi)
        yicerik2.addWidget(self.stok_miktari)

        dicerik1 = QVBoxLayout()

        yicerik3 = QHBoxLayout()
        self.stok_mensei = QLineEdit()
        yicerik3.addWidget(QLabel("Stok Menşei:"))
        yicerik3.addWidget(self.stok_mensei)

        yicerik4 = QHBoxLayout()
        self.stok_cinsi = QLineEdit()
        yicerik4.addWidget(QLabel("Stok Cinsi:"))
        yicerik4.addWidget(self.stok_cinsi)

        yicerik5 = QHBoxLayout()
        self.stok_durumu = QLineEdit()
        yicerik5.addWidget(QLabel("Stok Durumu:"))
        yicerik5.addWidget(self.stok_durumu)

        dicerik1.addLayout(yicerik3)
        dicerik1.addLayout(yicerik4)
        dicerik1.addLayout(yicerik5)

        dugmeler = QHBoxLayout()
        btn_kaydet = QPushButton("Kaydet")
        btn_kaydet.clicked.connect(self.kaydet)
        btn_iptal = QPushButton("İptal")
        btn_iptal.clicked.connect(self.temizle)
        btn_cikis = QPushButton("Çıkış")
        btn_cikis.clicked.connect(self.close)

        dugmeler.addWidget(btn_kaydet)
        dugmeler.addWidget(btn_iptal)
        dugmeler.addWidget(btn_cikis)

        gicerik.addLayout(yicerik1)
        gicerik.addLayout(yicerik2)
        gicerik.addLayout(dicerik1)
        gicerik.addLayout(dugmeler)

        araclar = QWidget()
        araclar.setLayout(gicerik)
        self.setCentralWidget(araclar)

    def kaydet(self):
        print("🟡 Kaydet fonksiyonu çağrıldı.")
        try:
            stok_no = self.stok_no.text().strip()
            stok_adi = self.stok_adi.text().strip()
            miktar_text = self.stok_miktari.text().strip()
            stok_mensei = self.stok_mensei.text().strip()
            stok_cinsi = self.stok_cinsi.text().strip()
            stok_durumu = self.stok_durumu.text().strip()

            print("📥 Girilen veriler:")
            print(f"Stok No: {stok_no}, Adı: {stok_adi}, Miktar: {miktar_text}")

            if not stok_no or not stok_adi or not miktar_text:
                print("❗ Eksik bilgi.")
                QMessageBox.warning(self, "Eksik Bilgi", "Stok No, Adı ve Miktarı doldurulmalıdır.")
                return

            if not miktar_text.isdigit():
                print("❗ Miktar geçersiz.")
                QMessageBox.warning(self, "Hatalı Veri", "Stok miktarı sayı olmalıdır.")
                return

            stok_miktari = int(miktar_text)

            print("🔗 Veritabanına bağlanılıyor...")
            conn = veritabani_baglanti()
            print("🧪 conn nesnesi:", conn)

            if conn is None:
                print("❌ Bağlantı başarısız.")
                QMessageBox.critical(self, "Hata", "Veritabanı bağlantısı sağlanamadı.")
                return

            print("🎯 Cursor alınıyor...")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            aktif_db = cursor.fetchone()
            print("📡 Bağlı veritabanı:", aktif_db)

            sql = """
                INSERT INTO stoklar (stok_no, stok_adi, stok_miktari, stok_mensei, stok_cinsi, stok_durumu)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (stok_no, stok_adi, stok_miktari, stok_mensei, stok_cinsi, stok_durumu)
            print("📦 Veriler:", values)

            cursor.execute(sql, values)
            conn.commit()
            print("✅ Veri başarıyla eklendi.")

            cursor.close()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Kayıt veritabanına eklendi.")
            self.temizle()

        except Exception as e:
            print("❌ HATA:", e)
            print("💥 Ayrıntılı traceback:")
            print(traceback.format_exc())
            raise  # HATA YUKARI FIRLATILACAK → terminalde net görülecek

    def temizle(self):
        self.stok_no.clear()
        self.stok_adi.clear()
        self.stok_miktari.clear()
        self.stok_mensei.clear()
        self.stok_cinsi.clear()
        self.stok_durumu.clear()
        print("🔄 Temizleme tamamlandı.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    pencere = StokMenu()
    pencere.show()
    sys.exit(app.exec())
