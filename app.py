from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import cv2
import numpy as np

app = Flask(__name__)

def enhance_image_resolution(image_data):
    img_array = np.array(Image.open(io.BytesIO(image_data)))
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    upscaled = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    result = cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB)
    return Image.fromarray(result)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    image = enhance_image_resolution(file.read())
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/')
def index():
    return open('index.html').read()

if __name__ == '__main__':
    app.run(debug=True)