import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import io
import os
import pandas as pd

# Load model and taxonomy within same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "INatVision_Small_2_fact256_8bit.tflite")
TAXONOMY_PATH = os.path.join(BASE_DIR, "taxonomy.csv")

# Load model
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load taxonomy
taxonomy_df = pd.read_csv(TAXONOMY_PATH)

def predict_species(file_content: bytes):
    img = Image.open(io.BytesIO(file_content)).convert("RGB")

    input_shape = input_details[0]['shape']
    img = img.resize((input_shape[1], input_shape[2]))

    input_data = np.expand_dims(img, axis=0)

    if input_details[0]['dtype'] == np.float32:
        input_data = input_data.astype(np.float32) / 255.0
    else:
        input_data = input_data.astype(np.uint8)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    best_index = int(np.argmax(output_data))
    confidence = float(np.max(output_data))

    # Find best matching taxonomy column
    columns = taxonomy_df.columns
    candidate_column = ("scientific_name" if "scientific_name" in columns 
                        else "name" if "name" in columns 
                        else columns[1])  # fallback

    species_name = taxonomy_df.iloc[best_index][candidate_column]

    return {
        "species": species_name,
        "confidence": round(confidence, 4),
        "class_index": best_index
    }
