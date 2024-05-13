from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.image_processor import ImageProcessor

app = Flask(__name__)
CORS(app)

@app.route('/process_frame', methods=['POST'])
def process_frame():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400
  
  file = request.files['file']

  image_processor = ImageProcessor()
  image_processor.process(file)
  return jsonify({'message': 'Image received and processed'}), 200
  



