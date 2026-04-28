"""
GeoAI Soil Intelligence — FastAPI Backend
==========================================
Converted from Flask to FastAPI for deployment on Hugging Face Spaces / Railway.

Endpoints:
  POST /predict   — Upload soil image → returns prediction JSON
  GET  /history   — Last 10 predictions
  GET  /health    — Liveness check
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from tensorflow import lite as tflite
import numpy as np
import cv2
import os
import sqlite3
import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geoai")

# ---------------------------------------------------------------------------
# Global model reference (loaded once at startup)
# ---------------------------------------------------------------------------

interpreter = None
input_details = None
output_details = None

# ---------------------------------------------------------------------------
# Soil domain data  (identical to original Flask app)
# ---------------------------------------------------------------------------

classes = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil",
]

soil_data = {
    "Alluvial_Soil":  {"moisture": "High",   "strength": "Medium"},
    "Arid_Soil":      {"moisture": "Low",    "strength": "Medium"},
    "Black_Soil":     {"moisture": "High",   "strength": "High"},
    "Laterite_Soil":  {"moisture": "Medium", "strength": "Medium"},
    "Mountain_Soil":  {"moisture": "Medium", "strength": "High"},
    "Red_Soil":       {"moisture": "Low",    "strength": "Medium"},
    "Yellow_Soil":    {"moisture": "Low",    "strength": "Low"},
}

crop_data = {
    "Alluvial_Soil":  ["Rice", "Wheat", "Sugarcane"],
    "Arid_Soil":      ["Millet", "Barley", "Cotton"],
    "Black_Soil":     ["Cotton", "Soybean", "Sunflower"],
    "Laterite_Soil":  ["Cashew", "Tea", "Coffee"],
    "Mountain_Soil":  ["Apple", "Potato", "Maize"],
    "Red_Soil":       ["Groundnut", "Millet", "Pulses"],
    "Yellow_Soil":    ["Maize", "Potato", "Oilseeds"],
}

# ---------------------------------------------------------------------------
# Database helper
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(os.path.dirname(__file__), "soil_history.db")


def get_db():
    """Return a new SQLite connection (thread-safe for read/write)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create the history table if it doesn't exist."""
    conn = get_db()
    conn.execute("""
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
    logger.info("Database initialised: %s", DB_PATH)


# ---------------------------------------------------------------------------
# Lifespan: load model + init DB once at startup
# ---------------------------------------------------------------------------

def load_model():
    global interpreter, input_details, output_details
    if interpreter is None:
        logger.info("Loading TFLite model (lazy loading)…")
        model_path = os.path.join(os.path.dirname(__file__), "model.tflite")
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        logger.info("Model loaded successfully from %s", model_path)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    init_db()

    yield  # app is running

    # --- Shutdown ---
    logger.info("Shutting down GeoAI backend")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="GeoAI Soil Intelligence API",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins so the Vercel frontend can call this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/")
@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": interpreter is not None}


# ---------------------------------------------------------------------------
# POST /predict  — core prediction endpoint
# ---------------------------------------------------------------------------

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    """
    Accept a soil image, run the CNN model, return prediction.
    Identical prediction logic to the original Flask endpoint.
    """

    # --- Validate file type ---
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    try:
        # --- Lazy Load Model ---
        load_model()

        # --- Read & preprocess (same as original) ---
        contents = await image.read()
        img_array = np.frombuffer(contents, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))
        img_array = img.astype(np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # --- Prediction (using TFLite) ---
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

        soil_index = int(np.argmax(prediction))
        soil = classes[soil_index]
        confidence = float(np.max(prediction)) * 100

        # --- Health score calculation (same as original) ---
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

        # --- Save to database ---
        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO history (soil_type, moisture, strength, confidence, health_score) VALUES (?, ?, ?, ?, ?)",
                (soil, soil_data[soil]["moisture"], soil_data[soil]["strength"], confidence, health_score),
            )
            conn.commit()
            conn.close()
        except Exception as db_err:
            logger.warning("DB write failed (non-fatal): %s", db_err)

        # --- Return JSON (same shape as original) ---
        return {
            "soil_type": soil,
            "confidence": round(confidence, 2),
            "moisture": soil_data[soil]["moisture"],
            "strength": soil_data[soil]["strength"],
            "crops": crop_data[soil],
            "health_score": health_score,
        }

    except Exception as e:
        logger.error("Prediction error: %s", e)
        return JSONResponse(status_code=500, content={"error": str(e), "status": "failed"})


# ---------------------------------------------------------------------------
# GET /history  — last 10 predictions
# ---------------------------------------------------------------------------

@app.get("/history")
async def history():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "soil_type": row[1],
                "moisture": row[2],
                "strength": row[3],
                "confidence": row[4],
                "health_score": row[5],
            }
            for row in rows
        ]
    except Exception as e:
        logger.error("History error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Local development entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)