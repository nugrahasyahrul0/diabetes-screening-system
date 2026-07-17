/*
====================================================
Nama File    : script.js

Deskripsi:
Menghubungkan frontend screening diabetes dengan
backend Flask API.

Alur:
Form Input
    ↓
POST /predict
    ↓
XGBoost Prediction

    ↓
POST /explain
    ↓
SHAP Explanation

    ↓
Update UI

====================================================
*/


const screeningForm = document.getElementById(
    "screening-form"
);



if (screeningForm) {


screeningForm.addEventListener(
"submit",
async function(event){


event.preventDefault();



const age =
Number(
document.getElementById("age").value
);



const bmi =
Number(
document.getElementById("bmi").value
);



const familyHistoryInput =
document.getElementById("family-history").value;


if (familyHistoryInput === "") {

    alert(
        "Silakan pilih riwayat keluarga diabetes terlebih dahulu."
    );

    return;

}


const familyHistory =
Number(familyHistoryInput);

// ===============================
// VALIDASI INPUT
// ===============================

// Validasi usia
if (
    !Number.isInteger(age) ||
    age <= 0 ||
    age > 120
){

    alert(
        "Usia harus berupa angka bulat antara 1 sampai 120 tahun."
    );

    return;

}


// Validasi BMI
if (
    bmi <= 0 ||
    bmi > 100
){

    alert(
        "Nilai BMI tidak valid."
    );

    return;

}


// Validasi family history
if (
    familyHistory !== 0 &&
    familyHistory !== 1
){

    alert(
        "Silakan pilih riwayat keluarga diabetes."
    );

    return;

}


// ===============================
// RESET HASIL SEBELUM ANALISIS BARU
// ===============================

resetResultDisplay();


// Payload dikirim ke kedua endpoint

const payload = {

    age: age,

    bmi: bmi,

    family_history: familyHistory

};



try{


// =================================
// PREDICT
// =================================


const response =
await fetch(
"http://127.0.0.1:5000/predict",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:
JSON.stringify(payload)

}
);



if(!response.ok){

throw new Error(
"Predict API gagal"
);

}



const result =
await response.json();



console.log(
"Prediction Response:",
result
);




// Update hasil prediksi


document.getElementById(
"risk-category"
).textContent =
result.risk_category;



document.getElementById(
"risk-probability"
).textContent =
`${(
result.probability * 100
).toFixed(1)}%`;



document.getElementById(
"recommendation"
).textContent =
result.recommendation;





// =================================
// SHAP EXPLANATION
// =================================


const shapResponse =
await fetch(
"http://127.0.0.1:5000/explain",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:
JSON.stringify(payload)

}
);



if(!shapResponse.ok){

throw new Error(
"Explain API gagal"
);

}



const shapResult =
await shapResponse.json();



console.log(
"SHAP Response:",
shapResult
);



// Update faktor risiko

updateExplanation(
shapResult.shap_values
);

document.getElementById(
    "shap-narrative"
).textContent =
shapResult.narrative;



}

catch(error){


console.error(
"ERROR:",
error
);


alert(
"Gagal memproses prediksi."
);


}



}
);


}




function updateExplanation(data){


    const factors = {


        BMI: {

            bar:"bmi-bar",
            text:"bmi-text",
            direction:"bmi-direction"

        },


        Age: {

            bar:"age-bar",
            text:"age-text",
            direction:"age-direction"

        },


        FamilyHistory_binary: {

            bar:"family-bar",
            text:"family-text",
            direction:"family-direction"

        }


    };



    Object.keys(factors).forEach(feature => {


        const value = data[feature];


        const absValue = Math.min(
            Math.abs(value) / 3 * 100,
            100
        );



        document.getElementById(
            factors[feature].bar
        ).style.width =
        `${absValue}%`;



        if(value > 0){


            document.getElementById(
                factors[feature].direction
            ).textContent =
            "↑";


            document.getElementById(
                factors[feature].text
            ).textContent =
            "Meningkatkan kontribusi risiko";


        }

        else {


            document.getElementById(
                factors[feature].direction
            ).textContent =
            "↓";


            document.getElementById(
                factors[feature].text
            ).textContent =
            "Menurunkan kontribusi risiko";


        }


    });



}

//reset screening
function resetScreening(){

    // Reset form input
    document.getElementById("screening-form").reset();


    // Reset hasil analisis

    document.getElementById(
        "risk-category"
    ).textContent =
    "Belum ada hasil analisis";


    document.getElementById(
        "risk-probability"
    ).textContent =
    "-";


    document.getElementById(
        "recommendation"
    ).textContent =
    "Menunggu hasil skrining.";



    // Reset SHAP

    const shapDefault = {

        "bmi-bar": "0%",
        "age-bar": "0%",
        "family-bar": "0%"

    };


    Object.keys(shapDefault).forEach(id => {

        const element = document.getElementById(id);

        if(element){
            element.style.width = shapDefault[id];
        }

    });



    // Reset arah dan teks SHAP

    document.getElementById(
        "bmi-direction"
    ).textContent = "—";


    document.getElementById(
        "age-direction"
    ).textContent = "—";


    document.getElementById(
        "family-direction"
    ).textContent = "—";



    document.getElementById(
        "bmi-text"
    ).textContent =
    "Menunggu analisis";


    document.getElementById(
        "age-text"
    ).textContent =
    "Menunggu analisis";


    document.getElementById(
        "family-text"
    ).textContent =
    "Menunggu analisis";



    document.getElementById(
        "shap-narrative"
    ).textContent =
    "Menunggu hasil analisis faktor risiko.";



    // Kembali ke posisi form

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}

//reset display

function resetResultDisplay(){

    document.getElementById(
        "risk-category"
    ).textContent =
    "Menunggu hasil analisis";


    document.getElementById(
        "risk-probability"
    ).textContent =
    "-";


    document.getElementById(
        "recommendation"
    ).textContent =
    "Menunggu hasil skrining.";


    document.getElementById(
        "shap-narrative"
    ).textContent =
    "Menunggu hasil analisis faktor risiko.";


    document.querySelectorAll(
        ".shap-bar"
    ).forEach(bar => {
        bar.style.width = "0%";
    });

}