"""
Convert model.h5 → model.tflite
================================
Run this ONCE locally to generate a TFLite model (~1MB vs ~85MB).
After conversion, you can switch app.py to use tflite-runtime
for drastically faster deployments.

Usage:
    pip install tensorflow-cpu numpy
    python convert_to_tflite.py
"""

import tensorflow as tf
import os

MODEL_DIR = os.path.dirname(__file__)
H5_PATH = os.path.join(MODEL_DIR, "model.h5")
TFLITE_PATH = os.path.join(MODEL_DIR, "model.tflite")

print(f"Loading {H5_PATH} ...")
model = tf.keras.models.load_model(H5_PATH)

print("Converting to TFLite ...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]        # quantise for size
tflite_model = converter.convert()

with open(TFLITE_PATH, "wb") as f:
    f.write(tflite_model)

h5_size = os.path.getsize(H5_PATH) / (1024 * 1024)
tflite_size = os.path.getsize(TFLITE_PATH) / (1024 * 1024)
print(f"Done!  {H5_PATH} ({h5_size:.1f} MB) → {TFLITE_PATH} ({tflite_size:.2f} MB)")
print(f"Size reduction: {(1 - tflite_size/h5_size)*100:.0f}%")
