from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image
import numpy as np
import os
import tensorflow as tf
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load the model
MODEL_PATH = r'D:\DATA-DATA\Nicho\Bangkit\CAPSTONE\HeloTani_API\model\my_model_15.h5'
model = load_model(MODEL_PATH)

# Define categories
CATEGORIES = {
    0: 'american bollworm', 1: 'anthracnose', 2: 'armyworm',
    3: 'bacterial blight in rice', 4: 'brownspot', 5: 'common rust',
    6: 'cotton aphid', 7: 'cotton bollrot', 8: 'flag smut of wheat',
    9: 'gray leaf spot', 10: 'healthy cotton', 11: 'healthy maize',
    12: 'healthy sugarcane', 13: 'healthy wheat crops', 14: 'leaf curl',
    15: 'leaf smut', 16: 'maize ear rot', 17: 'maize fall armyworm',
    18: 'maize stem borer', 19: 'mealy bugs', 20: 'mosaic sugarcane',
    21: 'pink bollworm', 22: 'red cotton bugs', 23: 'redrot sugarcane',
    24: 'redrust sugarcane', 25: 'rice blast', 26: 'thirps',
    27: 'tungro', 28: 'wheat aphid', 29: 'wheat black rust',
    30: 'wheat brown rust', 31: 'wheat leaf blight', 32: 'wheat mite',
    33: 'wheat powdery mildew', 34: 'wheat scab', 35: 'wheat stem fly',
    36: 'wheat yellow rust', 37: 'whitefly cotton', 38: 'wilt',
    39: 'yellow rust sugarcane'
}

# Helper function to preprocess image
def preprocess_image(image_path):
    try:
        target_size = (224, 224)  # Adjust to your model's input size
        image = load_img(image_path, target_size=target_size, color_mode="rgb")
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)  # Use EfficientNet preprocess
        return image
    except Exception as e:
        raise ValueError(f"Error in preprocessing image: {e}")

# Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save file to uploads and image_uploaded
        file_path = os.path.join('uploads', file.filename)
        output_dir = r'D:\DATA-DATA\Nicho\Bangkit\CAPSTONE\HeloTani_API\image_uploaded'
        os.makedirs('uploads', exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        file.save(file_path)

        # Preprocess the image
        image = preprocess_image(file_path)

        # Make prediction
        start_time = datetime.now()
        logits = model.predict(image)
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        probabilities = tf.nn.softmax(logits[0]).numpy()
        predicted_class = np.argmax(probabilities)
        class_name = CATEGORIES.get(predicted_class, 'Unknown')

        # Save preprocessed image for debugging
        output_path = os.path.join(output_dir, f"processed_{file.filename}")
        preprocessed_image = (image[0] * 255).astype(np.uint8)  # Rescale back to [0,255]
        preprocessed_image = Image.fromarray(preprocessed_image)
        preprocessed_image.save(output_path.replace('.npy', '.jpg'))  # Save as .jpg

        # Clean up temporary file
        os.remove(file_path)

        # Return response
        return jsonify({
            'class_id': int(predicted_class),
            'class_name': class_name,
            'probabilities': probabilities.tolist(),
            'processing_time': processing_time,
            'saved_image': output_path.replace('.npy', '.jpg')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
