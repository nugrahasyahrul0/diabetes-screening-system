"""
====================================================
Nama File    : app.py

Deskripsi:
Backend API Flask untuk sistem deteksi dini
risiko diabetes mellitus menggunakan XGBoost
dengan pendekatan Explainable Artificial
Intelligence.

Tanggung jawab:
- Menerima input frontend
- Memanggil model_service
- Mengirim response JSON

Catatan:
- Tidak ada preprocessing model di sini.
- Seluruh proses model berada di model_service.py.
====================================================
"""


from flask import Flask, request, jsonify
from flask_cors import CORS


from model_service import (
    predict_risk,
    explain_risk,
    generate_shap_interpretation
)


from config import MODEL_THRESHOLD



# ====================================================
# Flask Application
# ====================================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

@app.route("/predict", methods=["OPTIONS"])
def predict_options():
    return jsonify({"status": "ok"}), 200

# ====================================================
# Endpoint Prediction
# ====================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():


    data = request.get_json()


    if not data:

        return jsonify(
            {
                "error":
                "Input tidak ditemukan"
            }
        ),400



    try:

        age = data["age"]

        bmi = data["bmi"]

        family_history = data["family_history"]



        probability = predict_risk(
            age,
            bmi,
            family_history
        )



        if probability >= MODEL_THRESHOLD:


            risk_category = (
                "Risiko lebih tinggi"
            )


            recommendation = (
                "Disarankan melakukan pemeriksaan "
                "kesehatan lanjutan ke tenaga kesehatan."
            )


        else:


            risk_category = (
                "Risiko lebih rendah"
            )


            recommendation = (
                "Tetap menjaga pola hidup sehat "
                "dan melakukan pemeriksaan berkala."
            )



        return jsonify(
            {
                "probability":
                    float(probability),

                "risk_category":
                    risk_category,

                "recommendation":
                    recommendation
            }
        )



    except Exception as error:


        return jsonify(
            {
                "error":
                str(error)
            }
        ),500





# ====================================================
# Endpoint SHAP Explanation
# ====================================================

@app.route("/explain", methods=["POST"])
def explain():

    data = request.get_json()

    if not data:
        return jsonify(
            {
                "error": "Input tidak ditemukan"
            }
        ),400

    try:

        age = data["age"]
        bmi = data["bmi"]
        family_history = data["family_history"]


    # Hitung ulang probabilitas
    # agar endpoint explain tetap independen

        probability = predict_risk(
            age,
            bmi,
            family_history
        )


    # Tentukan kategori berdasarkan threshold penelitian

        if probability >= MODEL_THRESHOLD:

            risk_category = "Risiko lebih tinggi"

        else:

            risk_category = "Risiko lebih rendah"



    # Ambil nilai kontribusi SHAP

        shap_values = explain_risk(
            age,
            bmi,
            family_history
        )



    # Buat interpretasi manusia

        interpretation = generate_shap_interpretation(
            shap_values,
            probability,
            risk_category
        )

        return jsonify({

            "shap_values": shap_values,

            "ranking": interpretation["ranking"],

            "contributions": interpretation["contributions"],

            "narrative": interpretation["narrative"]

        })

    except Exception as error:
        return jsonify(
            {
                "error": str(error)
            }
        ),500


    

    





# ====================================================
# Run Server
# ====================================================
import os

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000)),
        debug=False
    )