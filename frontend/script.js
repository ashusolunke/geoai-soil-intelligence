const analyzeBtn = document.querySelector(".analyze-btn");

if(analyzeBtn){

analyzeBtn.addEventListener("click", async () => {

let file = document.getElementById("fileInput").files[0];

if(!file){
alert("Please upload soil image first");
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

}
catch(err){

alert("AI server not responding");

}

});

}
document.getElementById("soilType").innerText = result.soil_type.replace("_", " ");