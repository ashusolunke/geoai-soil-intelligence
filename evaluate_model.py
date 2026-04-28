import os
import cv2
import numpy as np
from tensorflow import lite as tflite

# Define classes
classes = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Black_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil",
]

# Load TFLite model
model_path = os.path.join("backend", "model.tflite")
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

dataset_dir = "dataset"
correct = 0
total = 0

print("Evaluating model accuracy on the dataset...")

for class_idx, class_name in enumerate(classes):
    class_dir = os.path.join(dataset_dir, class_name)
    if not os.path.exists(class_dir):
        continue
    
    for filename in os.listdir(class_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue
            
        filepath = os.path.join(class_dir, filename)
        
        # Read and preprocess image
        img = cv2.imread(filepath)
        if img is None:
            continue
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))
        img_array = img.astype(np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Prediction
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])
        
        predicted_class_idx = int(np.argmax(prediction))
        
        if predicted_class_idx == class_idx:
            correct += 1
        total += 1

if total > 0:
    accuracy = (correct / total) * 100
    print(f"\nTotal Images: {total}")
    print(f"Correct Predictions: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")
else:
    print("No images found in the dataset.")
