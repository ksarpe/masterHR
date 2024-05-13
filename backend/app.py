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
  try:
    response_dict = image_processor.process(file)
    return jsonify(response_dict), 200
  except Exception as e:
    return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500
  
if __name__ == '__main__':
    app.run(debug=True)


