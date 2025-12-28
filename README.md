# Buku-Tamu-Digital-Menggunakan-QR-Check-In
DESKRIPSI SINGKAT: Buku Tamu Digital adalah aplikasi berbasis web yang dikembangkan menggunakan Python dan Streamlit untuk mencatat dan mengelola data tamu secara digital. Aplikasi ini menyediakan fitur pengolahan data tamu (CRUD) serta mendukung penggunaan QR Code/Barcode guna mempermudah proses pencatatan, pencarian, dan pengelolaan data secara cepat dan efisien
# Penjelasan Fitur CRUD+QR SCAN
Mode Tamu 📝Isi Buku Tamu: Input Nama dan Alamat Validasi input (tidak boleh) Data disimpan ke file CSV Sistem membuat ID tamu otomatis QR Code dibuat otomatis untuk setiap tamu QR Code dapat diunduh (download) 
📷 Scan QR Code Scan QR Code untuk: Mencatat menghadiri tamu waktu kunjungan otomatis Data disimpan ke file kunjungan kosong.csv 
🔐 Mode Admin 📊 Dashboard Seperti: Total tamu Total kunjungan kosong hari ini Grafik kunjungan berdasarkan jam (real-time) 
📋 Manajemen Data Tamu (CRUD) Read → Menampilkan seluruh data tamu Update → Mengubah nama dan alamat tamu berdasarkan ID Delete → Menghapus data tamu berdasarkan ID 
📑 Laporan Kunjungan Menampilkan data kunjungan dalam bentuk tabel Filter laporan berdasarkan: Tanggal mulai Tanggal akhir Grafik kunjungan harian Ekspor laporan ke file Excel
ℹ️ Halaman Tentang Menampilkan informasi singkat aplikasi: Teknologi yang digunakan Fitur utama Tujuan aplikasi
# Struktur Folder
│
├── main.py # File utama aplikasi Streamlit
├── utils.py # Fungsi bantu (QR, simpan data, backup)
├── style.css # Styling tampilan aplikasi
├── requirements.txt # Daftar library Python
│
├── data/ # Data utama aplikasi
│ ├── tamu.csv
│ └── kunjungan.csv
│
├── qr/ # Penyimpanan QR Code
├── backup/ # Backup otomatis data
└── README.md
screnshot buku tamu digital



