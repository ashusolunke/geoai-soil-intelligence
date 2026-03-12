from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Load trained model
model_path = os.path.join(os.path.dirname(__file__), "model.h5")
model = tf.keras.models.load_model(model_path)

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

        # Model prediction
        prediction = model.predict(img)
        soil_index = np.argmax(prediction)
        soil = classes[soil_index]

        # Response
        return jsonify({
            "soil_type": soil,
            "moisture": soil_data[soil]["moisture"],
            "strength": soil_data[soil]["strength"],
            "crops": crop_data[soil]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)