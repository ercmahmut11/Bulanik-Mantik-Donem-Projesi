 Otonom Çamaşır Makinesi Bulanık Kontrol Sistemi

Bu proje, Bulanık Mantık dersi dönem ödevi kapsamında **Mahmut** tarafından geliştirilmiştir. Geleneksel makinelerin aksine, çamaşırların kirlilik durumunu, kumaş hassasiyetini ve ağırlığını analiz ederek su, enerji ve deterjan tasarrufu sağlayan otonom bir sistem simüle eder.

  Proje Yapısı

 1. Giriş ve Çıkış Değişkenleri
* **Girişler:** Kirlilik Derecesi (%0-100), Kumaş Hassasiyeti (%0-100), Çamaşır Ağırlığı (0-10 kg)
* **Çıkışlar:** Yıkama Süresi (15-120 dk), Sıkma Devri (400-1400 rpm), Deterjan Miktarı (30-150 ml)

 2. Dilsel Terimler
* Kirlilik: Az, Orta, Çok
* Hassasiyet: Düşük, Orta, Yüksek
* Ağırlık: Hafif, Normal, Ağır
* Çıkışlar: Kısa/Düşük/Az, Normal/Standart/Orta, Uzun/Yüksek/Çok (Tümü için Üçgen Üyelik Fonksiyonları kullanılmıştır).

 3. Çıkarım ve Durulaştırma
Sistemde Mamdani tipi çıkarım mekanizması kullanılmış ve en az 15 adet aktif kural kurgulanmıştır. Nihai sayısal çıktıları elde etmek için **Ağırlık Merkezi (Centroid)** durulaştırma yöntemi uygulanmıştır.



 Kurulum ve Çalıştırma

1. Gerekli kütüphaneleri yükleyin:
 bash
   pip install -r requirements.txt

   Uygulamayı başlatın:

2.Uygulamayı Başlatın 
Bash
streamlit run app.py


 Değerlendirme
* Güçlü Yönleri: Sistem lineer olmayan insan kararlarını başarıyla modeller ve kaynak israfını önler.
* Zayıf Yönleri: Kurallar el ile yazılmıştır. Güncel yaklaşımlarda bu kurallar yapay sini
