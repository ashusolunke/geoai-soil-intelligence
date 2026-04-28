/* =========================================
   GeoAI — Frontend Script
   =========================================
   Uses API_BASE_URL from config.js
   ========================================= */


/* -------------------------------------------
   IMAGE UPLOAD & PREVIEW
   ------------------------------------------- */

const fileInput   = document.getElementById("fileInput");
const uploadBox   = document.getElementById("uploadBox");
const uploadText  = document.getElementById("uploadText");
const uploadBtn   = document.getElementById("uploadBtn");
const imgPreview  = document.getElementById("imagePreview");

// Click "Upload Image" → trigger file picker
if(uploadBtn){
uploadBtn.addEventListener("click", ()=> fileInput.click());
}

// Show preview when a file is selected
if(fileInput){
fileInput.addEventListener("change", ()=>{
  const file = fileInput.files[0];
  if(file){
    const reader = new FileReader();
    reader.onload = (e)=>{
      imgPreview.src = e.target.result;
      imgPreview.style.display = "block";
      uploadText.textContent = file.name;
    };
    reader.readAsDataURL(file);
  }
});
}

// Drag & drop support
if(uploadBox){
uploadBox.addEventListener("dragover",(e)=>{
  e.preventDefault();
  uploadBox.style.borderColor = "#3A7D44";
});
uploadBox.addEventListener("dragleave",()=>{
  uploadBox.style.borderColor = "rgba(255,255,255,0.2)";
});
uploadBox.addEventListener("drop",(e)=>{
  e.preventDefault();
  uploadBox.style.borderColor = "rgba(255,255,255,0.2)";
  const file = e.dataTransfer.files[0];
  if(file && file.type.startsWith("image/")){
    fileInput.files = e.dataTransfer.files;
    const reader = new FileReader();
    reader.onload = (ev)=>{
      imgPreview.src = ev.target.result;
      imgPreview.style.display = "block";
      uploadText.textContent = file.name;
    };
    reader.readAsDataURL(file);
  }
});
}


/* -------------------------------------------
   LOADING OVERLAY HELPERS
   ------------------------------------------- */

const loadingOverlay = document.getElementById("loadingOverlay");

function showLoading(){
  if(loadingOverlay) loadingOverlay.classList.add("active");
}
function hideLoading(){
  if(loadingOverlay) loadingOverlay.classList.remove("active");
}


/* -------------------------------------------
   ANALYZE SOIL — API CALL
   ------------------------------------------- */

const analyzeBtn = document.querySelector(".analyze-btn");

if(analyzeBtn){

analyzeBtn.addEventListener("click", async ()=>{

  const file = fileInput.files[0];

  if(!file){
    alert("Please upload a soil image first");
    return;
  }

  // Build FormData
  const formData = new FormData();
  formData.append("image", file);

  // Show loading state
  showLoading();
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "⏳ Analyzing…";

  try{

    const response = await fetch(API_BASE_URL + "/predict",{
      method:"POST",
      body:formData
    });

    if(!response.ok){
      const errBody = await response.json().catch(()=>({}));
      throw new Error(errBody.error || "Server returned " + response.status);
    }

    const result = await response.json();

    console.log("API response:", result);

    /* Update scanner result cards */

    document.getElementById("soilType").innerText   = result.soil_type.replace(/_/g," ");
    document.getElementById("moisture").innerText    = result.moisture;
    document.getElementById("strength").innerText    = result.strength;
    document.getElementById("crops").innerText       = result.crops.join(", ");
    document.getElementById("confidence").innerText  = result.confidence + "%";
    document.getElementById("healthScore").innerText = result.health_score + "/100";

    /* Update hero section */

    document.getElementById("heroSoil").innerText     = result.soil_type.replace(/_/g," ");
    document.getElementById("heroMoisture").innerText  = result.moisture;
    document.getElementById("heroStrength").innerText  = result.strength;

    /* Persist to localStorage */

    localStorage.setItem("soilType", result.soil_type);
    localStorage.setItem("moisture", result.moisture);
    localStorage.setItem("strength", result.strength);

    /* Update dashboard charts */

    updateDashboard(result.soil_type);

    /* Scroll to results */
    document.querySelector(".analysis-box").scrollIntoView({behavior:"smooth",block:"start"});

  }
  catch(error){
    console.error("Prediction error:", error);
    alert("⚠ Analysis Failed:\n\n" + error.message);
  }
  finally{
    hideLoading();
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "🔬 Analyze Soil";
  }

});

}


/* -------------------------------------------
   CAMERA FUNCTION
   ------------------------------------------- */

async function openCamera(){

const video = document.getElementById("camera");

video.style.display = "block";

try{
  const stream = await navigator.mediaDevices.getUserMedia({video:true});
  video.srcObject = stream;
}catch(err){
  alert("Camera access denied or not available.");
}

}


/* -------------------------------------------
   DOWNLOAD REPORT
   ------------------------------------------- */

function downloadReport(){

const soil       = document.getElementById("soilType").innerText;
const moisture   = document.getElementById("moisture").innerText;
const strength   = document.getElementById("strength").innerText;
const crops      = document.getElementById("crops").innerText;
const confidence = document.getElementById("confidence").innerText;
const health     = document.getElementById("healthScore").innerText;

if(soil === "--"){
  alert("Run a soil analysis first before downloading the report.");
  return;
}

const htmlReport = `
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GeoAI Soil Report</title>
<style>
  body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #333;
    background: #fff;
    margin: 0;
    padding: 40px;
  }
  .report-container {
    max-width: 800px;
    margin: 0 auto;
    border: 1px solid #ccc;
    padding: 40px;
  }
  .header {
    text-align: center;
    border-bottom: 2px solid #2e7d32;
    padding-bottom: 20px;
    margin-bottom: 30px;
  }
  .header h1 {
    margin: 0;
    color: #2e7d32;
    font-size: 28px;
    text-transform: uppercase;
  }
  .header p {
    margin: 5px 0 0;
    color: #666;
    font-size: 14px;
  }
  .section-title {
    font-size: 18px;
    color: #2e7d32;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
    margin-top: 30px;
    margin-bottom: 15px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  th, td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: left;
  }
  th {
    width: 40%;
    color: #555;
    font-weight: bold;
    background-color: #f9f9f9;
  }
  td {
    font-weight: 500;
  }
  .footer {
    margin-top: 50px;
    text-align: center;
    font-size: 12px;
    color: #999;
    border-top: 1px solid #eee;
    padding-top: 20px;
  }
  @media print {
    body { padding: 0; }
    .report-container { border: none; padding: 0; }
  }
</style>
</head>
<body>
  <div class="report-container">
    <div class="header">
      <h1>GeoAI Soil Intelligence</h1>
      <p>Official Soil Analysis Report</p>
    </div>
    
    <div class="section-title">Analysis Summary</div>
    <table>
      <tr>
        <th>Soil Type</th>
        <td>${soil}</td>
      </tr>
      <tr>
        <th>Moisture Level</th>
        <td>${moisture}</td>
      </tr>
      <tr>
        <th>Soil Strength</th>
        <td>${strength}</td>
      </tr>
      <tr>
        <th>Recommended Crops</th>
        <td>${crops}</td>
      </tr>
    </table>

    <div class="section-title">AI Prediction Metrics</div>
    <table>
      <tr>
        <th>Prediction Confidence</th>
        <td>${confidence}</td>
      </tr>
      <tr>
        <th>Soil Health Score</th>
        <td>${health}</td>
      </tr>
    </table>

    <div class="footer">
      Generated by GeoAI Platform • Industry-Grade Soil Analysis<br>
      Date: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}
    </div>
  </div>
  <script>
    window.onload = function() { window.print(); }
  </script>
</body>
</html>
`;

const blob = new Blob([htmlReport],{type:"text/html"});
const link = document.createElement("a");

link.href = URL.createObjectURL(blob);
link.download = "soil_report.html";
link.click();

}


/* -------------------------------------------
   CHARTS (Chart.js)
   ------------------------------------------- */

let phChart;
let moistureChart;
let fertilityChart;

window.addEventListener("load",()=>{

const phCtx        = document.getElementById("phChart");
const moistureCtx  = document.getElementById("moistureChart");
const fertilityCtx = document.getElementById("fertilityChart");

phChart = new Chart(phCtx,{
  type:"bar",
  data:{
    labels:["Nitrogen","Phosphorus","Potassium"],
    datasets:[{
      label:"Soil pH Composition",
      data:[5,6,7],
      backgroundColor:"#4CAF50"
    }]
  }
});

moistureChart = new Chart(moistureCtx,{
  type:"doughnut",
  data:{
    labels:["Moisture","Dry"],
    datasets:[{
      data:[50,50],
      backgroundColor:["#4CAF50","#222"]
    }]
  }
});

fertilityChart = new Chart(fertilityCtx,{
  type:"radar",
  data:{
    labels:["Organic","Minerals","Water","Structure"],
    datasets:[{
      label:"Fertility Score",
      data:[4,5,6,5],
      backgroundColor:"rgba(76,175,80,0.3)",
      borderColor:"#4CAF50"
    }]
  }
});

});


/* -------------------------------------------
   UPDATE DASHBOARD from prediction
   ------------------------------------------- */

function updateDashboard(soil){

const phData = {
  Alluvial_Soil:[6,7,5],
  Arid_Soil:[8,6,4],
  Black_Soil:[7,8,6],
  Laterite_Soil:[5,6,4],
  Mountain_Soil:[6,7,6],
  Red_Soil:[5,6,5],
  Yellow_Soil:[5,5,4]
};

const moistureData = {
  Alluvial_Soil:70,
  Arid_Soil:30,
  Black_Soil:80,
  Laterite_Soil:50,
  Mountain_Soil:60,
  Red_Soil:40,
  Yellow_Soil:35
};

const fertilityData = {
  Alluvial_Soil:[7,6,7,6],
  Arid_Soil:[3,4,3,2],
  Black_Soil:[8,7,8,7],
  Laterite_Soil:[5,5,4,4],
  Mountain_Soil:[6,6,5,5],
  Red_Soil:[4,5,4,4],
  Yellow_Soil:[3,4,3,3]
};

phChart.data.datasets[0].data = phData[soil];

moistureChart.data.datasets[0].data = [
  moistureData[soil],
  100-moistureData[soil]
];

fertilityChart.data.datasets[0].data = fertilityData[soil];

phChart.update();
moistureChart.update();
fertilityChart.update();

}


/* -------------------------------------------
   GEOAI MAP (Leaflet)
   ------------------------------------------- */

const map = L.map('soilMap').setView([20.5937, 78.9629], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:19
}).addTo(map);

map.on("click",function(e){

let lat = e.latlng.lat.toFixed(4);
let lon = e.latlng.lng.toFixed(4);

document.getElementById("mapLocation").innerText = lat + ", " + lon;

/* Dummy soil prediction for demo */

let soils = [
  "Alluvial Soil",
  "Black Soil",
  "Red Soil",
  "Laterite Soil",
  "Arid Soil"
];

let randomSoil = soils[Math.floor(Math.random()*soils.length)];

document.getElementById("mapSoil").innerText = randomSoil;

});