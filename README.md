# 🛡️ Safety Equipment Detection - Streamlit App

Aplikasi Streamlit untuk deteksi peralatan keselamatan (Helmet dan Vest) menggunakan model YOLOv12 yang sudah dilatih.

## 🚀 Fitur

- **📸 Deteksi Gambar**: Upload dan analisis gambar untuk deteksi helm dan vest
- **🎥 Deteksi Video**: Upload dan analisis video dengan visualisasi hasil
- **⚙️ Konfigurasi Model**: Pilih dari 3 model YOLOv12 (S, M, N)
- **🎚️ Threshold Control**: Atur confidence threshold untuk deteksi
- **📊 Statistik**: Informasi model dan perbandingan performa
- **📥 Download**: Download hasil video yang sudah diproses

## 📦 Instalasi

1. Clone repository ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Pastikan model `.pt` sudah ada di folder `model/`:
   - `BESTSModel.pt`
   - `BESTMModel.pt` 
   - `BESTNModel.pt`

## 🎯 Penggunaan

1. Jalankan aplikasi:
```bash
streamlit run app.py
```

2. Buka browser dan akses `http://localhost:8501`

3. Pilih tab yang sesuai:
   - **Deteksi Gambar**: Upload gambar untuk analisis
   - **Deteksi Video**: Upload video untuk analisis
   - **Statistik**: Informasi model dan tips penggunaan

## ⚙️ Konfigurasi

### Pilih Model
- **Model S**: BESTSModel.pt (18MB) - Fast, High Accuracy
- **Model M**: BESTMModel.pt (39MB) - Medium Speed, Very High Accuracy  
- **Model N**: BESTNModel.pt (5.2MB) - Very Fast, Medium Accuracy

### Threshold
- **Rendah (0.1-0.3)**: Deteksi lebih banyak, mungkin ada false positive
- **Menengah (0.4-0.6)**: Seimbang antara akurasi dan deteksi
- **Tinggi (0.7-0.9)**: Hanya deteksi yang sangat yakin

## 🏷️ Kelas Deteksi

- **Kelas 0**: Helmet (Helm)
- **Kelas 1**: Vest (Rompi)

## 📁 Struktur Proyek

```
├── app.py                 # Aplikasi Streamlit utama
├── requirements.txt       # Dependencies Python
├── README.md             # Dokumentasi
└── model/                # Folder model AI
    ├── BESTSModel.pt
    ├── BESTMModel.pt
    └── BESTNModel.pt
```

## 🛠️ Teknologi

- **Frontend**: Streamlit
- **AI Model**: YOLOv12 (Ultralytics)
- **Computer Vision**: OpenCV
- **Image Processing**: Pillow
- **Deep Learning**: PyTorch

## 📝 Lisensi

Proyek ini dibuat untuk tujuan edukasi dan pengembangan.
