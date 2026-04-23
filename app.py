from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def detect_corrosion(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (300, 300))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_rust = np.array([5, 50, 50])
    upper_rust = np.array([20, 255, 255])

    mask = cv2.inRange(hsv, lower_rust, upper_rust)

    rust_pixels = np.sum(mask > 0)
    total_pixels = image.size / 3

    rust_percentage = (rust_pixels / total_pixels) * 100

    if rust_percentage > 5:
        return f"Corrosion Detected ({rust_percentage:.2f}%)"
    else:
        return f"No Corrosion ({rust_percentage:.2f}%)"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    image_file = None

    if request.method == 'POST':
        file = request.files['image']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        result = detect_corrosion(filepath)
        image_file = file.filename

    return render_template('index.html', result=result, image_file=image_file)

if __name__ == '__main__':
   app.run(debug=True, port=5001)