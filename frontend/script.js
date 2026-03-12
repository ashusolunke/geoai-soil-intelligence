const analyzeBtn = document.querySelector(".analyze-btn");

if(analyzeBtn){

const analyzeBtn = document.querySelector(".analyze-btn");

analyzeBtn.addEventListener("click", async () => {

let file = document.getElementById("fileInput").files[0];

if(!file){
alert("Please upload a soil image first");
return;
}

let formData = new FormData();
formData.append("image", file);

try{

let response = await fetch("https://geoai-backend.onrender.com/predict",{
method:"POST",
body:formData
});

let result = await response.json();

document.getElementById("soilType").innerText = result.soil_type;
document.getElementById("moisture").innerText = result.moisture;
document.getElementById("strength").innerText = result.strength;

/* Save data for dashboard */

localStorage.setItem("soilType",result.soil_type);
localStorage.setItem("moisture",result.moisture);
localStorage.setItem("strength",result.strength);

}
catch(error){
console.error("Error analyzing image:", error);
alert("AI server not responding");
}

});

}
document.getElementById("soilType").innerText = result.soil_type.replace("_", " ");
window.addEventListener("load",()=>{

let soil = localStorage.getItem("soilType");
let moisture = localStorage.getItem("moisture");
let strength = localStorage.getItem("strength");

if(soil){

/* Update dashboard titles */

document.querySelector("#phChartTitle").innerText = soil;
document.querySelector("#moistureChartTitle").innerText = moisture;
document.querySelector("#fertilityChartTitle").innerText = strength;

}

});