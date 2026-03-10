const analyzeBtn = document.querySelector(".analyze-btn");

if(analyzeBtn){

analyzeBtn.addEventListener("click", async ()=>{

let file = document.getElementById("fileInput").files[0];

if(!file){
alert("Upload soil image first");
return;
}

const progress = document.getElementById("progress");
let width = 0;

let scan = setInterval(()=>{
if(width>=100){
clearInterval(scan);
}
else{
width++;
progress.style.width = width + "%";
}
},20);

let formData = new FormData();
formData.append("image", file);

try{

let response = await fetch("http://127.0.0.1:5000/predict",{
method:"POST",
body:formData
});

let result = await response.json();

/* dashboard report */

document.getElementById("soilType").innerText =
result.soil_type.replace("_"," ");

document.getElementById("moisture").innerText =
result.moisture;

document.getElementById("strength").innerText =
result.strength;

/* hero live card */

document.getElementById("heroSoil").innerText =
result.soil_type.replace("_"," ");

document.getElementById("heroMoisture").innerText =
result.moisture;

document.getElementById("heroStrength").innerText =
result.strength;

}catch(err){

alert("AI server not responding");
console.error(err);

}

});

}
document.getElementById("soilType").innerText = result.soil_type.replace("_", " ");