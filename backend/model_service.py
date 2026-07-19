"""
====================================================
Nama File    : model_service.py

Deskripsi:
Mengelola integrasi model machine learning
untuk prediksi dan explainability SHAP.

Project:
Sistem Deteksi Dini Diabetes Mellitus Menggunakan
XGBoost dengan Pendekatan Explainable Artificial
Intelligence.
====================================================
"""


import joblib
import pandas as pd
import shap


from config import MODEL_PATH



# ====================================================
# Load Pipeline Model
# ====================================================

model_pipeline = None
xgb_model = None
explainer = None

def get_model_pipeline():
    global model_pipeline, xgb_model

    if model_pipeline is None:
        model_pipeline = joblib.load(MODEL_PATH)
        xgb_model = model_pipeline.named_steps["model"]

    return model_pipeline

def get_explainer():
    global explainer

    if explainer is None:
        get_model_pipeline()
        explainer = shap.TreeExplainer(xgb_model)

    return explainer

# ====================================================
# Membuat input dataframe
# ====================================================

def create_input(
    age,
    bmi,
    family_history
):

    return pd.DataFrame(
        [
            [
                age,
                bmi,
                family_history
            ]
        ],
        columns=[
            "Age",
            "BMI",
            "FamilyHistory_binary"
        ]
    )



# ====================================================
# Prediksi Risiko
# ====================================================

def predict_risk(age, bmi, family_history):
    input_data = create_input(age, bmi, family_history)

    pipeline = get_model_pipeline()

    probability = pipeline.predict_proba(
        input_data
    )[0][1]

    return probability



# ====================================================
# SHAP Explanation
# ====================================================

def explain_risk(
    age,
    bmi,
    family_history
):


    input_data = create_input(
        age,
        bmi,
        family_history
    )


    # preprocessing sesuai pipeline
    pipeline = get_model_pipeline()

    transformed_data = (
        pipeline
        .named_steps["scaler"]
        .transform(input_data)
    )


    shap_values = get_explainer().shap_values(transformed_data)


    values = shap_values[0]


    explanation = {

        "Age":
        float(values[0]),

        "BMI":
        float(values[1]),

        "FamilyHistory_binary":
        float(values[2])

    }


    return explanation

# ====================================================
# Generator Interpretasi SHAP
#
# Mengubah nilai kontribusi model menjadi
# penjelasan yang mudah dipahami pengguna.
#
# Input:
# shap_values dictionary
#
# Output:
# ranking faktor + narasi interpretasi
# ====================================================


def generate_shap_interpretation(shap_values, probability, risk_category):


    # Mapping nama fitur agar lebih manusiawi

    feature_names = {

        "BMI": "BMI",

        "Age": "usia",

        "FamilyHistory_binary": "riwayat keluarga diabetes"

    }



    # Mengurutkan berdasarkan nilai absolut SHAP
    #
    # Semakin besar nilai absolut,
    # semakin besar kontribusinya terhadap model.

    ranked_features = sorted(
        shap_values.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )



    # Mengambil urutan faktor

    first_factor = feature_names[
        ranked_features[0][0]
    ]

    second_factor = feature_names[
        ranked_features[1][0]
    ]

    third_factor = feature_names[
        ranked_features[2][0]
    ]



    # Menentukan arah pengaruh fitur dalam perhitungan model

    contributions = []



    for feature, value in ranked_features:


        name = feature_names[feature]


        if value > 0:

            direction = (
                "cenderung menaikkan estimasi risiko menurut model"
            )

        else:

            direction = (
                "cenderung menurunkan estimasi risiko menurut model"
            )


        contributions.append(
            f"{name} {direction}"
        )



    narrative = (

        f"Hasil skrining menunjukkan estimasi risiko sebesar "
        f"{probability * 100:.1f}% "
        f"dengan kategori {risk_category.lower()}. "

        f"Berdasarkan data yang dimasukkan, "
        f"faktor yang memiliki kontribusi terbesar terhadap hasil estimasi model adalah "
        f"{first_factor}, diikuti oleh {second_factor}, dan {third_factor}. "

        f"Menurut interpretasi model, "
        f"{contributions[0]}, "
        f"{contributions[1]}, dan "
        f"{contributions[2]}. "

        f"Interpretasi faktor risiko menunjukkan kontribusi masing-masing variabel "
        f"terhadap hasil prediksi berdasarkan pola yang dipelajari model, "
        f"bukan menunjukkan hubungan sebab-akibat secara langsung. "

        f"Hasil ini bersifat skrining awal dan bukan diagnosis medis."
    )



    return {

        "ranking": [

            first_factor,
            second_factor,
            third_factor

        ],

        "contributions": contributions,

        "narrative": narrative

    }
