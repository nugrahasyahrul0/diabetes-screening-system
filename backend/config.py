"""
====================================================
Nama File    : config.py

Deskripsi:
Menyimpan konfigurasi utama backend untuk sistem
deteksi dini risiko diabetes mellitus.

Project:
Sistem Deteksi Dini Diabetes Mellitus Menggunakan
XGBoost dengan Pendekatan Explainable Artificial
Intelligence.

Catatan Maintenance:
- Threshold model disimpan di satu tempat agar
  konsisten dengan hasil penelitian.
- Jangan mengubah nilai threshold tanpa merujuk
  kembali pada hasil eksperimen model final.
====================================================
"""


from pathlib import Path

# ====================================================
# Threshold klasifikasi model
#
# Nilai ini berasal dari hasil optimasi threshold
# model final XGBoost.
#
# Fungsi:
# Probabilitas >= threshold:
#     Risiko lebih tinggi
#
# Probabilitas < threshold:
#     Risiko lebih rendah
# ====================================================

MODEL_THRESHOLD = 0.3289475



# ====================================================
# Lokasi file model pipeline
#
# Pipeline berisi:
# - preprocessing/scaler
# - model XGBoost classifier
#
# Backend tidak melakukan scaling manual.
# Semua preprocessing dijalankan oleh pipeline.
# ====================================================

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "diabetes_xgb_pipeline.pkl"
)