from flask import Flask, request, jsonify
from flask_cors import CORS
import utils.image_processor as image_processor
from utils.logger import Logger
import utils.learn.word_generator as word_generator

app = Flask(__name__)
logger = Logger("app.py").get_logger()
CORS(app)

@app.route('/process_frame', methods=['POST'])
def process_frame():
  logger.info("Got request to process the image")
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400
  
  file = request.files['file']

  try:
    response_dict = image_processor.process(file)
    logger.success("Successfully processed the image")
    return jsonify(response_dict), 200
  except Exception as e:
    return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500

@app.route('/process_frame_alphabet', methods=['POST'])
def process_frame():
  logger.info("Got request to process the image")
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400
  
  file = request.files['file']

  try:
    response_dict = image_processor.process(file, chapter=2)
    logger.success("Successfully processed the image")
    return jsonify(response_dict), 200
  except Exception as e:
    return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500
  
@app.route('/get_words', methods=['GET'])
def get_words():
  logger.info("Got request to send words to the user")
  if 'chapter' not in request.args:
    return jsonify({'error': 'No chapter provided'}), 400
    
  chapter = request.args['chapter']
  words = word_generator.get_words(chapter)
  logger.success("Successfully sent words to the user")
  return jsonify({'words': words}), 200

@app.route('/health', methods=['GET'])
def health():
  return jsonify({'status': 'Healthy'}), 200
    
if __name__ == '__main__':
    app.run(debug=False)

