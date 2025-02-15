import os
from pathlib import Path
from dotenv import load_dotenv
from vision.food_detector import FoodDetector
from recipes.recipe_finder import RecipeFinder

def main():
    # Load environment variables
    load_dotenv()

    # Initialize components
    detector = FoodDetector()
    recipe_finder = RecipeFinder(api_key=os.getenv('SPOONACULAR_API_KEY'))

    def process_image(image_path: str):
        """
        Process an image and return related recipes
        
        Args:
            image_path (str): Path to the image file
        """
        # Ensure image exists
        if not Path(image_path).exists():
            print(f"Error: Image not found at {image_path}")
            return

        try:
            # Detect food items in the image
            detected_items = detector.detect(image_path)
            
            if not detected_items:
                print("No food items detected in the image")
                return

            print(f"Detected food items: {', '.join(detected_items)}")
            
            # Get recipes for detected items
            recipes = recipe_finder.find_recipes(detected_items)
            
            # Display recipes
            print("\nRelated Recipes:")
            for i, recipe in enumerate(recipes, 1):
                print(f"\n{i}. {recipe['title']}")
                print(f"Ready in: {recipe['readyInMinutes']} minutes")
                print(f"URL: {recipe['sourceUrl']}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    main()
    print("\nEnter image path (or 'q' to quit):")
    while True:
        image_path = input("> ").strip()
        if image_path.lower() == 'q':
            break
        process_image(image_path)
