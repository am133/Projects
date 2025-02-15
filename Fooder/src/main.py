import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import time
from vision.food_detector import FoodDetector
from recipes.recipe_finder import RecipeFinder
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../static', static_url_path='')
CORS(app)

# Configure timeouts and limits
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max image size
REQUEST_TIMEOUT = 30  # 30 seconds timeout

def initialize_components():
    """Initialize application components with retry logic"""
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            detector = FoodDetector()
            recipe_finder = RecipeFinder(api_key=os.getenv('SPOONACULAR_API_KEY'))
            return detector, recipe_finder
        except Exception as e:
            retry_count += 1
            logger.error(f"Initialization attempt {retry_count} failed: {str(e)}")
            if retry_count == max_retries:
                raise RuntimeError("Failed to initialize components after multiple attempts")
            time.sleep(2)  # Wait before retrying

# Initialize components with retry logic
detector, recipe_finder = initialize_components()

def timed_function(timeout):
    """Decorator to handle function timeouts"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = f(*args, **kwargs)
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                logger.warning(f"Function {f.__name__} took {elapsed_time:.2f}s to complete")
            return result
        return wrapper
    return decorator

@app.route('/api/detect-and-find-recipes', methods=['POST'])
@timed_function(REQUEST_TIMEOUT)
def detect_and_find_recipes():
    try:
        start_time = time.time()
        
        # Get the base64 encoded image from the request
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Validate image size
        image_str = data['image'].split(',')[1]
        image_size = len(image_str) * 3/4  # Base64 size to actual size
        if image_size > MAX_CONTENT_LENGTH:
            return jsonify({'error': 'Image too large. Maximum size is 10MB'}), 413

        # Decode base64 image
        try:
            image_data = base64.b64decode(image_str)
        except Exception as e:
            return jsonify({'error': 'Invalid image format'}), 400
        
        # Save temporarily with unique name
        temp_path = f'temp_image_{int(time.time())}.jpg'
        with open(temp_path, 'wb') as f:
            f.write(image_data)

        try:
            # Detect food items
            logger.info("Starting food detection")
            detected_items = detector.detect(temp_path)
            logger.info(f"Detection completed. Found {len(detected_items)} items")
        finally:
            # Clean up temp file
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.error(f"Error removing temp file: {str(e)}")

        if not detected_items:
            return jsonify({
                'detected_items': [],
                'recipes': [],
                'message': 'No food items detected in the image'
            })

        # Get recipes
        item_names = [item.split(' (')[0] for item in detected_items]
        recipes = recipe_finder.find_recipes(item_names)

        # Calculate total processing time
        processing_time = time.time() - start_time
        logger.info(f"Total processing time: {processing_time:.2f}s")

        return jsonify({
            'detected_items': detected_items,
            'recipes': recipes,
            'processing_time': round(processing_time, 2)
        })

    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        return jsonify({'error': 'Processing error', 'details': str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
