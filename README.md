# 📊 FinSight: Dashboard Analisis Keuangan Pribadi

## 📌 Deskripsi Proyek
Proyek ini adalah sistem analisis keuangan pribadi yang dibangun menggunakan Python dan Streamlit. Sistem ini menganalisis data transaksi keuangan pengguna untuk mengidentifikasi pola perilaku belanja dan mengklasifikasikan status keuangan ke dalam tiga kategori:
- Hemat
- Normal
- Boros

Dashboard ini dirancang dengan standar visual aplikasi keuangan modern dan menyediakan visualisasi interaktif untuk membantu pengguna memahami pendapatan, pengeluaran, tren belanja bulanan, serta segmentasi perilaku mereka.

---

## 🎯 Tujuan Proyek
Tujuan dari proyek ini adalah:
- Menganalisis kontribusi kategori pengeluaran terhadap status keuangan secara dinamis.
- Membandingkan total pemasukan dan total pengeluaran tanpa penumpukan angka pada grafik.
- Menganalisis tren pengeluaran bulanan dari waktu ke waktu untuk mendeteksi anomali musiman.
- Menerapkan rekayasa fitur (*Feature Engineering*) dan segmentasi berbasis perilaku (*Clustering*).
- Menyiapkan dataset keuangan yang realistis untuk kebutuhan pembelajaran mesin (*Machine Learning*) dan peramalan di masa depan.
- Membangun dan meluncurkan (*deploy*) visualisasi dashboard interaktif menggunakan Streamlit Cloud.

---

## 🧠 Rekayasa Fitur & Klaster Perilaku (Tugas Tambahan)
Untuk meningkatkan nilai analisis dari dataset, dua teknik rekayasa fitur (*Feature Engineering*) telah diterapkan:
1. **Ekstraksi Waktu:** Memecah kolom `tanggal` mentah menjadi fitur waktu mandiri yaitu `tahun` dan `bulan` untuk menggerakkan komponen filter interaktif pada panel samping secara real-time.
2. **Klaster Perilaku Berbasis Aturan:** Merekayasa fitur baru bernama `klaster_finansial` untuk mengelompokkan transaksi ke dalam 3 domain perilaku utama:
   * **Klaster 0: Pengeluaran Prioritas** (Kebutuhan pokok, operasional rutin, dan tagihan tetap).
   * **Klaster 1: Pengeluaran Impulsif** (Keinginan, gaya hidup konsumtif, dan kebocoran anggaran tak terencana).
   * **Klaster 2: Pengeluaran Masa Depan** (Alokasi tabungan, investasi jangka panjang, dan pos proteksi kekayaan).

---

## 🗂 Atribut Dataset
Dataset ini mengandung beberapa atribut sebagai berikut:

| Atribut | Deskripsi |
|---|---|
| tanggal | Tanggal transaksi |
| bulan | Bulan transaksi |
| nama_kategori | Kode kategori transaksi |
| nama_kategori_label | Nama kategori transaksi |
| deskripsi | Deskripsi detail transaksi |
| tipe | Kode tipe transaksi |
| tipe_label | Tipe transaksi (Masuk / Keluar) |
| saldo awal | Saldo sebelum transaksi |
| jumlah | Nominal jumlah transaksi |
| saldo akhir | Saldo setelah transaksi |
| status | Kode status keuangan |
| status_label | Label status keuangan (Hemat / Normal / Boros) |
| prediksi_pengeluaran | Nilai prediksi pengeluaran |
| klaster_finansial | Label klaster perilaku hasil rekayasa fitur *(Baru)* |

---

## 🛠️ Persyaratan Sistem & Dependensi
Pastikan Anda memiliki file `requirements.txt` di folder utama Anda. Pustaka Python yang dibutuhkan meliputi:
* `streamlit`
* `pandas`
* `numpy`
* `matplotlib`
* `seaborn`
* `openpyxl`

---

## 📂 Struktur Repositori
```text
├── dashboard.py                       # Kode utama aplikasi dashboard Streamlit
├── requirements.txt                   # Daftar instalasi pustaka otomatis untuk server
├── README.md                          # Dokumentasi lengkap proyek (File ini)
└── DATASET_KEUANGAN_CLUSTERED.xlsx   # Basis data keuangan yang telah dilengkapi fitur klaster
