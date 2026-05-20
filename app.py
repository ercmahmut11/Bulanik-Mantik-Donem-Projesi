import streamlit as st
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Sayfa Genişlik Ayarı
st.set_page_config(layout="wide", page_title="Bulanık Mantık Çamaşır Asistanı")

st.title(" Otonom Çamaşır Makinesi Bulanık Kontrol Sistemi")
st.write("Kirlilik, hassasiyet ve ağırlığa göre optimum yıkama parametrelerini hesaplar.")

# ---------------------------------------------------------
# 1. EVRENSEL KÜMELERİN (UNIVERSE) TANIMLANMASI
# ---------------------------------------------------------
x_kirlilik = np.arange(0, 101, 1)
x_hassasiyet = np.arange(0, 101, 1)
x_agirlik = np.arange(0, 11, 1)

x_sure = np.arange(15, 121, 1)
x_devir = np.arange(400, 1401, 1)
x_deterjan = np.arange(30, 151, 1)

# ---------------------------------------------------------
# 2. ÜYELİK FONKSİYONLARININ OLUŞTURULMASI
# ---------------------------------------------------------
# Girişler
kir_az = fuzz.trimf(x_kirlilik, [0, 0, 50])
kir_orta = fuzz.trimf(x_kirlilik, [20, 50, 80])
kir_cok = fuzz.trimf(x_kirlilik, [50, 100, 100])

has_dusuk = fuzz.trimf(x_hassasiyet, [0, 0, 50])
has_orta = fuzz.trimf(x_hassasiyet, [20, 50, 80])
has_yuksek = fuzz.trimf(x_hassasiyet, [50, 100, 100])

agr_hafif = fuzz.trimf(x_agirlik, [0, 0, 4])
agr_normal = fuzz.trimf(x_agirlik, [2, 5, 8])
agr_agir = fuzz.trimf(x_agirlik, [6, 10, 10])

# Çıkışlar
sure_kisa = fuzz.trimf(x_sure, [15, 15, 60])
sure_normal = fuzz.trimf(x_sure, [40, 70, 100])
sure_uzun = fuzz.trimf(x_sure, [80, 120, 120])

devir_dusuk = fuzz.trimf(x_devir, [400, 400, 800])
devir_standart = fuzz.trimf(x_devir, [600, 900, 1200])
devir_yuksek = fuzz.trimf(x_devir, [1000, 1400, 1400])

det_az = fuzz.trimf(x_deterjan, [30, 30, 70])
det_orta = fuzz.trimf(x_deterjan, [50, 90, 120])
det_cok = fuzz.trimf(x_deterjan, [100, 150, 150])

# ---------------------------------------------------------
# ARAYÜZ SOL PANEL: SLIDER GİRİŞLERİ
# ---------------------------------------------------------
st.sidebar.header(" Giriş Parametreleri")
input_kir = st.sidebar.slider("Kirlilik Derecesi (%)", 0, 100, 45)
input_has = st.sidebar.slider("Kumaş Hassasiyeti (%)", 0, 100, 30)
input_agr = st.sidebar.slider("Çamaşır Ağırlığı (kg)", 0.0, 10.0, 5.5)

# ---------------------------------------------------------
# 3. BULANIKLAŞTIRMA (FUZZIFICATION)
# ---------------------------------------------------------
val_kir_az = fuzz.interp_membership(x_kirlilik, kir_az, input_kir)
val_kir_orta = fuzz.interp_membership(x_kirlilik, kir_orta, input_kir)
val_kir_cok = fuzz.interp_membership(x_kirlilik, kir_cok, input_kir)

val_has_dusuk = fuzz.interp_membership(x_hassasiyet, has_dusuk, input_has)
val_has_orta = fuzz.interp_membership(x_hassasiyet, has_orta, input_has)
val_has_yuksek = fuzz.interp_membership(x_hassasiyet, has_yuksek, input_has)

val_agr_hafif = fuzz.interp_membership(x_agirlik, agr_hafif, input_agr)
val_agr_normal = fuzz.interp_membership(x_agirlik, agr_normal, input_agr)
val_agr_agir = fuzz.interp_membership(x_agirlik, agr_agir, input_agr)

# ---------------------------------------------------------
# 4. KURAL TABANI VE ÇIKARIM MOTORU
# ---------------------------------------------------------
aktivasyonlar = []
kurallar_metni = []

def kural_ekle(g1, g2, g3, c_sure, c_devir, c_det, text):
    akt = np.fmin(g1, np.fmin(g2, g3))
    if akt > 0:
        aktivasyonlar.append((akt, c_sure, c_devir, c_det))
        kurallar_metni.append(f"• [AKTİF] {text} (Aktivasyon: {akt:.2f})")
    else:
        kurallar_metni.append(f"• [Pasif] {text}")

# 15 Adet Kuralların Tanımlanması
kural_ekle(val_kir_az, val_has_yuksek, val_agr_hafif, sure_kisa, devir_dusuk, det_az, "EĞER Kirlilik Az VE Hassasiyet Yüksek VE Ağırlık Hafif İSE Süre Kısa, Devir Düşük, Deterjan Az")
kural_ekle(val_kir_az, val_has_orta, val_agr_normal, sure_kisa, devir_standart, det_az, "EĞER Kirlilik Az VE Hassasiyet Orta VE Ağırlık Normal İSE Süre Kısa, Devir Standart, Deterjan Az")
kural_ekle(val_kir_orta, val_has_orta, val_agr_normal, sure_normal, devir_standart, det_orta, "EĞER Kirlilik Orta VE Hassasiyet Orta VE Ağırlık Normal İSE Süre Normal, Devir Standart, Deterjan Orta")
kural_ekle(val_kir_cok, val_has_dusuk, val_agr_agir, sure_uzun, devir_yuksek, det_cok, "EĞER Kirlilik Çok VE Hassasiyet Düşük VE Ağırlık Ağır İSE Süre Uzun, Devir Yüksek, Deterjan Çok")
kural_ekle(val_kir_cok, val_has_yuksek, val_agr_hafif, sure_normal, devir_dusuk, det_orta, "EĞER Kirlilik Çok VE Hassasiyet Yüksek VE Ağırlık Hafif İSE Süre Normal, Devir Düşük, Deterjan Orta")
kural_ekle(val_kir_orta, val_has_yuksek, val_agr_agir, sure_normal, devir_dusuk, det_orta, "EĞER Kirlilik Orta VE Hassasiyet Yüksek VE Ağırlık Ağır İSE Süre Normal, Devir Düşük, Deterjan Orta")
kural_ekle(val_kir_az, val_has_dusuk, val_agr_agir, sure_kisa, devir_yuksek, det_orta, "EĞER Kirlilik Az VE Hassasiyet Düşük VE Ağırlık Ağır İSE Süre Kısa, Devir Yüksek, Deterjan Orta")
kural_ekle(val_kir_cok, val_has_orta, val_agr_normal, sure_uzun, devir_standart, det_cok, "EĞER Kirlilik Çok VE Hassasiyet Orta VE Ağırlık Normal İSE Süre Uzun, Devir Standart, Deterjan Çok")
kural_ekle(val_kir_orta, val_has_dusuk, val_agr_hafif, sure_kisa, devir_yuksek, det_az, "EĞER Kirlilik Orta VE Hassasiyet Düşük VE Ağırlık Hafif İSE Süre Kısa, Devir Yüksek, Deterjan Az")
kural_ekle(val_kir_cok, val_has_dusuk, val_agr_normal, sure_uzun, devir_yuksek, det_cok, "EĞER Kirlilik Çok VE Hassasiyet Düşük VE Ağırlık Normal İSE Süre Uzun, Devir Yüksek, Deterjan Çok")
kural_ekle(val_kir_az, val_has_orta, val_agr_hafif, sure_kisa, devir_standart, det_az, "EĞER Kirlilik Az VE Hassasiyet Orta VE Ağırlık Hafif İSE Süre Kısa, Devir Standart, Deterjan Az")
kural_ekle(val_kir_orta, val_has_orta, val_agr_hafif, sure_normal, devir_standart, det_az, "EĞER Kirlilik Orta VE Hassasiyet Orta VE Ağırlık Hafif İSE Süre Normal, Devir Standart, Deterjan Az")
kural_ekle(val_kir_orta, val_has_yuksek, val_agr_normal, sure_normal, devir_dusuk, det_orta, "EĞER Kirlilik Orta VE Hassasiyet Yüksek VE Ağırlık Normal İSE Süre Normal, Devir Düşük, Deterjan Orta")
kural_ekle(val_kir_cok, val_has_yuksek, val_agr_agir, sure_uzun, devir_dusuk, det_cok, "EĞER Kirlilik Çok VE Hassasiyet Yüksek VE Ağırlık Ağır İSE Süre Uzun, Devir Düşük, Deterjan Çok")
kural_ekle(val_kir_az, val_has_dusuk, val_agr_hafif, sure_kisa, devir_yuksek, det_az, "EĞER Kirlilik Az VE Hassasiyet Düşük VE Ağırlık Hafif İSE Süre Kısa, Devir Yüksek, Deterjan Az")

# Agregasyon (Birleştirme)
out_sure = np.zeros_like(x_sure)
out_devir = np.zeros_like(x_devir)
out_deterjan = np.zeros_like(x_deterjan)

for akt, c_sure, c_devir, c_det in aktivasyonlar:
    out_sure = np.fmax(out_sure, np.fmin(akt, c_sure))
    out_devir = np.fmax(out_devir, np.fmin(akt, c_devir))
    out_deterjan = np.fmax(out_deterjan, np.fmin(akt, c_det))

# ---------------------------------------------------------
# 5. DURULAŞTIRMA (DEFUZZIFICATION - Centroid)
# ---------------------------------------------------------
try:
    res_sure = fuzz.defuzz(x_sure, out_sure, 'centroid')
    res_devir = fuzz.defuzz(x_devir, out_devir, 'centroid')
    res_deterjan = fuzz.defuzz(x_deterjan, out_deterjan, 'centroid')
except AssertionError:
    res_sure, res_devir, res_deterjan = 67.5, 900, 90

# ---------------------------------------------------------
# ARAYÜZ PANEL GÖRSELLEŞTİRME
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(" Sayısal Çıktılar (Durulaştırılmış)")
    st.metric(" Yıkama Süresi", f"{res_sure:.1f} Dakika")
    st.metric(" Sıkma Devri", f"{res_devir:.0f} RPM")
    st.metric(" Deterjan Miktarı", f"{res_deterjan:.1f} ml")

    st.subheader(" Kural Aktivasyon Listesi")
    with st.expander("Tüm Kuralları ve Durumları Gör"):
        for k in kurallar_metni:
            st.write(k)

with col2:
    st.subheader(" Üyelik Fonksiyonları ve Çıkış Grafikleri")
    
    fig, axs = plt.subplots(3, 1, figsize=(6, 8))
    
    axs[0].plot(x_sure, sure_kisa, 'b', label='Kısa')
    axs[0].plot(x_sure, sure_normal, 'g', label='Normal')
    axs[0].plot(x_sure, sure_uzun, 'r', label='Uzun')
    axs[0].fill_between(x_sure, 0, out_sure, facecolor='Orange', alpha=0.4)
    axs[0].axvline(res_sure, color='black', linestyle='--')
    axs[0].set_title(f"Yıkama Süresi Sonuç: {res_sure:.1f} dk")
    axs[0].legend()

    axs[1].plot(x_devir, devir_dusuk, 'b', label='Düşük')
    axs[1].plot(x_devir, devir_standart, 'g', label='Standart')
    axs[1].plot(x_devir, devir_yuksek, 'r', label='Yüksek')
    axs[1].fill_between(x_devir, 0, out_devir, facecolor='Orange', alpha=0.4)
    axs[1].axvline(res_devir, color='black', linestyle='--')
    axs[1].set_title(f"Sıkma Devri Sonuç: {res_devir:.0f} rpm")
    axs[1].legend()

    axs[2].plot(x_deterjan, det_az, 'b', label='Az')
    axs[2].plot(x_deterjan, det_orta, 'g', label='Orta')
    axs[2].plot(x_deterjan, det_cok, 'r', label='Çok')
    axs[2].fill_between(x_deterjan, 0, out_deterjan, facecolor='Orange', alpha=0.4)
    axs[2].axvline(res_deterjan, color='black', linestyle='--')
    axs[2].set_title(f"Deterjan Miktarı Sonuç: {res_deterjan:.1f} ml")
    axs[2].legend()

    plt.tight_layout()
    st.pyplot(fig)