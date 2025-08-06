from mySql1 import veritabani_baglanti
from PyQt6.QtWidgets import *
import traceback

class StokMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STOK MODÜLÜ")
        self.setFixedSize(800, 550)

        gicerik = QVBoxLayout()

        # 🆕 Arama Kutusu
        arama_layout = QHBoxLayout()
        arama_label = QLabel("Ara:")
        self.arama_kutusu = QLineEdit()
        self.arama_kutusu.setPlaceholderText("Stok No, Ad, Cins, Menşei...")
        self.arama_kutusu.textChanged.connect(self.filter_table)
        arama_layout.addWidget(arama_label)
        arama_layout.addWidget(self.arama_kutusu)
        gicerik.addLayout(arama_layout)

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

        btn_guncelle = QPushButton("Güncelle")
        btn_guncelle.clicked.connect(self.kayit_guncelle)

        btn_sil = QPushButton("Sil")
        btn_sil.clicked.connect(self.kayit_sil)

        btn_iptal = QPushButton("İptal")
        btn_iptal.clicked.connect(self.temizle)

        btn_cikis = QPushButton("Çıkış")
        btn_cikis.clicked.connect(self.close)

        dugmeler.addWidget(btn_kaydet)
        dugmeler.addWidget(btn_guncelle)
        dugmeler.addWidget(btn_sil)
        dugmeler.addWidget(btn_iptal)
        dugmeler.addWidget(btn_cikis)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["Stok No", "Adı", "Miktar", "Menşei", "Cinsi", "Durumu"])
        self.tablo.horizontalHeader().setStretchLastSection(True)
        self.tablo.cellClicked.connect(self.satir_secildi)

        gicerik.addLayout(yicerik1)
        gicerik.addLayout(yicerik2)
        gicerik.addLayout(dicerik1)
        gicerik.addLayout(dugmeler)
        gicerik.addWidget(self.tablo)

        araclar = QWidget()
        araclar.setLayout(gicerik)
        self.setCentralWidget(araclar)

        # 🆕 Stil Eklendi
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: Arial;
                font-size: 13px;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                background-color: white;
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1c5980;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #cce5ff;
            }
            QHeaderView::section {
                background-color: #dbe9f4;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #bbb;
            }
        """)

        self.tum_kayitlar = []
        self.kayitlari_yukle()

    def kayitlari_yukle(self):
        try:
            conn = veritabani_baglanti()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT stok_no, stok_adi, stok_miktari, stok_mensei, stok_cinsi, stok_durumu FROM stoklar")
                kayitlar = cursor.fetchall()
                self.tum_kayitlar = kayitlar

                self.tablo.setRowCount(len(kayitlar))
                for row_idx, satir in enumerate(kayitlar):
                    for col_idx, deger in enumerate(satir):
                        self.tablo.setItem(row_idx, col_idx, QTableWidgetItem(str(deger)))

                cursor.close()
                conn.close()
        except Exception as e:
            print("❌ Tablo yüklenirken hata:", e)
            print(traceback.format_exc())

    def filter_table(self):
        aranan = self.arama_kutusu.text().lower().strip()
        filtreli = [k for k in self.tum_kayitlar if any(aranan in str(d).lower() for d in k)]
        self.tablo.setRowCount(len(filtreli))
        for row_idx, satir in enumerate(filtreli):
            for col_idx, deger in enumerate(satir):
                self.tablo.setItem(row_idx, col_idx, QTableWidgetItem(str(deger)))

    def satir_secildi(self, row, column):
        self.stok_no.setText(self.tablo.item(row, 0).text())
        self.stok_adi.setText(self.tablo.item(row, 1).text())
        self.stok_miktari.setText(self.tablo.item(row, 2).text())
        self.stok_mensei.setText(self.tablo.item(row, 3).text())
        self.stok_cinsi.setText(self.tablo.item(row, 4).text())
        self.stok_durumu.setText(self.tablo.item(row, 5).text())

    def kaydet(self):
        try:
            stok_no = self.stok_no.text().strip()
            stok_adi = self.stok_adi.text().strip()
            miktar_text = self.stok_miktari.text().strip()
            stok_mensei = self.stok_mensei.text().strip()
            stok_cinsi = self.stok_cinsi.text().strip()
            stok_durumu = self.stok_durumu.text().strip()

            if not stok_no or not stok_adi or not miktar_text:
                QMessageBox.warning(self, "Eksik Bilgi", "Stok No, Adı ve Miktarı doldurulmalıdır.")
                return

            if not miktar_text.isdigit():
                QMessageBox.warning(self, "Hatalı Veri", "Stok miktarı sayı olmalıdır.")
                return

            stok_miktari = int(miktar_text)

            conn = veritabani_baglanti()
            cursor = conn.cursor()
            sql = """
                INSERT INTO stoklar (stok_no, stok_adi, stok_miktari, stok_mensei, stok_cinsi, stok_durumu)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (stok_no, stok_adi, stok_miktari, stok_mensei, stok_cinsi, stok_durumu)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Kayıt veritabanına eklendi.")
            self.temizle()
            self.kayitlari_yukle()

        except Exception as e:
            print("❌ HATA:", e)
            print(traceback.format_exc())

    def kayit_guncelle(self):
        try:
            stok_no = self.stok_no.text().strip()
            stok_adi = self.stok_adi.text().strip()
            miktar_text = self.stok_miktari.text().strip()
            stok_mensei = self.stok_mensei.text().strip()
            stok_cinsi = self.stok_cinsi.text().strip()
            stok_durumu = self.stok_durumu.text().strip()

            if not stok_no:
                QMessageBox.warning(self, "Hata", "Güncellenecek stok numarası boş olamaz.")
                return

            if not miktar_text.isdigit():
                QMessageBox.warning(self, "Hatalı Veri", "Stok miktarı sayı olmalıdır.")
                return

            stok_miktari = int(miktar_text)

            conn = veritabani_baglanti()
            cursor = conn.cursor()
            sql = """
                UPDATE stoklar
                SET stok_adi=%s, stok_miktari=%s, stok_mensei=%s, stok_cinsi=%s, stok_durumu=%s
                WHERE stok_no=%s
            """
            values = (stok_adi, stok_miktari, stok_mensei, stok_cinsi, stok_durumu, stok_no)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Kayıt güncellendi.")
            self.temizle()
            self.kayitlari_yukle()

        except Exception as e:
            QMessageBox.critical(self, "Hata", "Kayıt güncellenirken hata oluştu.")

    def kayit_sil(self):
        secilen_satir = self.tablo.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırı seçin.")
            return

        stok_no_item = self.tablo.item(secilen_satir, 0)
        if stok_no_item is None:
            QMessageBox.warning(self, "Uyarı", "Geçersiz kayıt.")
            return

        stok_no = stok_no_item.text()
        cevap = QMessageBox.question(self, "Silme Onayı", f"{stok_no} numaralı kaydı silmek istediğinize emin misiniz?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if cevap == QMessageBox.StandardButton.Yes:
            try:
                conn = veritabani_baglanti()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM stoklar WHERE stok_no = %s", (stok_no,))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Başarılı", "Kayıt silindi.")
                self.kayitlari_yukle()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kayıt silinemedi: {e}")

    def temizle(self):
        self.stok_no.clear()
        self.stok_adi.clear()
        self.stok_miktari.clear()
        self.stok_mensei.clear()
        self.stok_cinsi.clear()
        self.stok_durumu.clear()
        self.arama_kutusu.clear()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    pencere = StokMenu()
    pencere.show()
    sys.exit(app.exec())
