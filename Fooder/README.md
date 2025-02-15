# Fooder - Food Recognition and Recipe Finder

An AI-powered application that recognizes food items in images and suggests relevant recipes.

## Features

- Food item detection using YOLOv5
- Recipe recommendations from Spoonacular API
- Support for common food items like fruits, vegetables, and prepared dishes

## Prerequisites

- Python 3.7+
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

2. Run the application:
```bash
python src/main.py
```

3. When prompted, enter the path to your food image. The application will:
   - Detect food items in the image
   - Find relevant recipes
   - Display recipe details including title, cooking time, and source URL

4. Enter 'q' to quit the application.

## Supported Food Items

The current version can detect:
- Fruits: apple, banana, orange
- Vegetables: broccoli, carrot
- Prepared foods: sandwich, hot dog, pizza, donut, cake

## API Rate Limits

Please note that the Spoonacular API has rate limits depending on your subscription plan. Monitor your usage to avoid exceeding these limits.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
