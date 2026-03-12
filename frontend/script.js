/* ===============================
   AI SOIL ANALYSIS
================================ */

const analyzeBtn = document.querySelector(".analyze-btn");

if (analyzeBtn) {

analyzeBtn.addEventListener("click", async () => {

let file = document.getElementById("fileInput").files[0];

if (!file) {
alert("Please upload a soil image first");
return;
}

let formData = new FormData();
formData.append("image", file);

try {

let response = await fetch("https://geoai-backend.onrender.com/predict", {
method: "POST",
body: formData
});

let result = await response.json();

/* Update Report */

document.getElementById("soilType").innerText = result.soil_type.replace("_"," ");
document.getElementById("moisture").innerText = result.moisture;
document.getElementById("strength").innerText = result.strength;
document.getElementById("crops").innerText = result.crops.join(", ");

/* Update Hero Section */

document.getElementById("heroSoil").innerText = result.soil_type.replace("_"," ");
document.getElementById("heroMoisture").innerText = result.moisture;
document.getElementById("heroStrength").innerText = result.strength;

/* Save for dashboard */

localStorage.setItem("soilType", result.soil_type);
localStorage.setItem("moisture", result.moisture);
localStorage.setItem("strength", result.strength);

/* Update Dashboard */

updateDashboard(result.soil_type);

} catch (error) {

console.error(error);
alert("AI server not responding");

}

});

}


/* ===============================
   DASHBOARD UPDATE
================================ */

function updateDashboard(soil){

let phData = {
"Alluvial_Soil":[6,7,5],
"Arid_Soil":[8,6,4],
"Black_Soil":[7,8,6],
"Laterite_Soil":[5,6,4],
"Mountain_Soil":[6,7,6],
"Red_Soil":[5,6,5],
"Yellow_Soil":[5,5,4]
};

let moistureData = {
"Alluvial_Soil":70,
"Arid_Soil":30,
"Black_Soil":80,
"Laterite_Soil":50,
"Mountain_Soil":60,
"Red_Soil":40,
"Yellow_Soil":35
};

let fertilityData = {
"Alluvial_Soil":[7,6,7,6],
"Arid_Soil":[3,4,3,2],
"Black_Soil":[8,7,8,7],
"Laterite_Soil":[5,5,4,4],
"Mountain_Soil":[6,6,5,5],
"Red_Soil":[4,5,4,4],
"Yellow_Soil":[3,4,3,3]
};

/* Update Charts */

phChart.data.datasets[0].data = phData[soil];
moistureChart.data.datasets[0].data = [moistureData[soil],100-moistureData[soil]];
fertilityChart.data.datasets[0].data = fertilityData[soil];

phChart.update();
moistureChart.update();
fertilityChart.update();

}


/* ===============================
   LOAD DASHBOARD DATA
================================ */

window.addEventListener("load",()=>{

let soil = localStorage.getItem("soilType");

if(soil){
updateDashboard(soil);
}

});


/* ===============================
   CAMERA SCAN
================================ */

async function openCamera(){

const video = document.getElementById("camera");

video.style.display="block";

let stream = await navigator.mediaDevices.getUserMedia({
video:true
});

video.srcObject = stream;

}