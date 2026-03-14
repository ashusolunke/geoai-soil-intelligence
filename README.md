# GeoAI Soil Intelligence Platform 🌍

![Project Demo](images/demo.gif)

AI-powered soil analysis platform that detects soil type from images and provides agricultural and construction insights.

This project combines **Machine Learning + Web Development + Data Visualization** to build an intelligent soil analysis system.

---

## 🚀 Features

- AI Soil Classification using Deep Learning
- Soil Moisture and Strength Prediction
- Crop Recommendation System
- Soil Health Score Calculation
- AI Confidence Score
- Interactive Analytics Dashboard
- Soil Scan History Tracking (SQLite Database)
- Camera-based Soil Scanning
- Downloadable Soil Analysis Report
- Construction & Agriculture Insights

---

## 🧠 How It Works

1. User uploads a soil image.
2. The Flask backend processes the image.
3. The trained deep learning model predicts the soil type.
4. The system generates insights including:

- Soil Type  
- Moisture Level  
- Soil Strength  
- Crop Recommendations  
- Confidence Score  
- Soil Health Score  

5. Results are displayed on an interactive dashboard.
6. Each prediction is saved in a **SQLite database** for history tracking.

---

## 🖼 Project UI Preview

### Home Page
![Home UI](assets/images/home.png)

### AI Soil Scanner
![Scanner UI](assets/images/scanner.png)

### Soil Analysis Dashboard
![Dashboard UI](assets/images/dashboard.png)

### Prediction Result
![Prediction UI](assets/images/report.png)

### Map 
![map UI](assets/images/map.png)

*(Place your screenshots inside the **images** folder)*

---

## 🏗 System Architecture
User Interface (HTML / CSS / JavaScript)
↓
Flask Backend API
↓
TensorFlow Soil Classification Model
↓
SQLite Database (Scan History)
↓
Analytics Dashboard (Chart.js)


---

## 🛠 Tech Stack

### Machine Learning
- Python
- TensorFlow / Keras
- NumPy
- PIL (Image Processing)

### Backend
- Flask
- Flask-CORS
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### Visualization
- Chart.js

---

## 📊 Soil Types Supported

- Alluvial Soil
- Arid Soil
- Black Soil
- Laterite Soil
- Mountain Soil
- Red Soil
- Yellow Soil

---

## 📂 Project Structure

geoai-soil-intelligence
│
├── backend
│ ├── app.py
│ ├── model.h5
│ └── requirements.txt
├── frontend
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── images
│ ├── home.png
│ ├── scanner.png
│ ├── dashboard.png
│ └── report.png
│ └── map.png
│
├── README.md
└── .gitignore

---

## 📌 Future Improvements

- Geospatial Soil Mapping
- AI Soil Comparison Tool
- Advanced Fertility Prediction
- Real PDF Report Generation
- Cloud Deployment

---

## 👨‍💻 Author

**Ashutosh Solunke**

B.Tech CSE  
IITM BS in Data Science

GitHub  
https://github.com/ashusolunke

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

