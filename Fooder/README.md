# Fooder - Food Recognition and Recipe Finder

An AI-powered application that recognizes food items in images and suggests relevant recipes.

## Features

- Food item detection using YOLOv11n (latest version)
- Web interface via Flask server
- Recipe recommendations from Spoonacular API
- Support for common food items like fruits, vegetables, and prepared dishes

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Spoonacular API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Fooder
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your Spoonacular API key:
```
SPOONACULAR_API_KEY=your_api_key_here
```

## Usage

1. Activate the virtual environment (if not already activated):
```bash
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

2. Run the Flask server:
```bash
python src/main.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

4. Use the web interface to:
   - Upload food images (max size: 10MB)
   - View detected food items
   - Get recipe recommendations based on detected items
   - See processing time and detection confidence scores

## Supported Food Items

The current version can detect:

### Fruits
- apple, banana, orange, pear, grapefruit, lemon, strawberry, grape

### Vegetables
- broccoli, carrot, cucumber, lettuce, tomato, potato, corn

### Prepared Foods
- sandwich, hot dog, pizza, burger, sushi, pasta
- donut, cake, ice cream, cookie, pastry

### Other Categories
- Staples: rice, bread
- Beverages: coffee, wine, juice
- Proteins: chicken, beef, fish, eggs
- Condiments: ketchup, mustard, sauce
- Generic: food, fruit, vegetable

## API Rate Limits

Please note that the Spoonacular API has rate limits depending on your subscription plan. Monitor your usage to avoid exceeding these limits.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
