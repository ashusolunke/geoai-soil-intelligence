from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import sqlite3

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "model.h5")
model = tf.keras.models.load_model(model_path)

# Create database if not exists
conn = sqlite3.connect("soil_history.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
soil_type TEXT,
moisture TEXT,
strength TEXT,
confidence REAL,
health_score INTEGER
)
""")

conn.commit()
conn.close()

# Soil classes
classes = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil"
]

# Soil properties
soil_data = {
    "Alluvial_Soil": {"moisture": "High", "strength": "Medium"},
    "Arid_Soil": {"moisture": "Low", "strength": "Medium"},
    "Black_Soil": {"moisture": "High", "strength": "High"},
    "Laterite_Soil": {"moisture": "Medium", "strength": "Medium"},
    "Mountain_Soil": {"moisture": "Medium", "strength": "High"},
    "Red_Soil": {"moisture": "Low", "strength": "Medium"},
    "Yellow_Soil": {"moisture": "Low", "strength": "Low"}
}

# Crop recommendations
crop_data = {
    "Alluvial_Soil": ["Rice", "Wheat", "Sugarcane"],
    "Arid_Soil": ["Millet", "Barley", "Cotton"],
    "Black_Soil": ["Cotton", "Soybean", "Sunflower"],
    "Laterite_Soil": ["Cashew", "Tea", "Coffee"],
    "Mountain_Soil": ["Apple", "Potato", "Maize"],
    "Red_Soil": ["Groundnut", "Millet", "Pulses"],
    "Yellow_Soil": ["Maize", "Potato", "Oilseeds"]
}


@app.route("/predict", methods=["POST"])
def predict():
    try:

        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]

        # Preprocess image
        img = Image.open(file).convert("RGB")
        img = img.resize((128, 128))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Prediction
        prediction = model.predict(img)

        soil_index = np.argmax(prediction)
        soil = classes[soil_index]

        confidence = float(np.max(prediction)) * 100

        # Calculate Soil Health Score
        health_score = 0

        if soil_data[soil]["moisture"] == "High":
            health_score += 40
        elif soil_data[soil]["moisture"] == "Medium":
            health_score += 30
        else:
            health_score += 20

        if soil_data[soil]["strength"] == "High":
            health_score += 40
        elif soil_data[soil]["strength"] == "Medium":
            health_score += 30
        else:
            health_score += 20

        health_score += 20

        # Save prediction to database
        conn = sqlite3.connect("soil_history.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO history (soil_type, moisture, strength, confidence, health_score)
        VALUES (?, ?, ?, ?, ?)
        """, (
            soil,
            soil_data[soil]["moisture"],
            soil_data[soil]["strength"],
            confidence,
            health_score
        ))

        conn.commit()
        conn.close()

        # Return response
        return jsonify({
            "soil_type": soil,
            "confidence": round(confidence, 2),
            "moisture": soil_data[soil]["moisture"],
            "strength": soil_data[soil]["strength"],
            "crops": crop_data[soil],
            "health_score": health_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history", methods=["GET"])
def history():

    conn = sqlite3.connect("soil_history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()

    conn.close()

    history_data = []

    for row in rows:
        history_data.append({
            "soil_type": row[1],
            "moisture": row[2],
            "strength": row[3],
            "confidence": row[4],
            "health_score": row[5]
        })

    return jsonify(history_data)


if __name__ == "__main__":
    app.run(debug=True)