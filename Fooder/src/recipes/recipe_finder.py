import requests
from typing import List, Dict, Any

class RecipeFinder:
    def __init__(self, api_key: str):
        """
        Initialize the recipe finder with Spoonacular API key
        
        Args:
            api_key (str): Spoonacular API key
        """
        self.api_key = api_key
        self.base_url = "https://api.spoonacular.com/recipes"
        
        if not api_key:
            raise ValueError("Spoonacular API key is required")

    def find_recipes(self, ingredients: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find recipes based on detected food items
        
        Args:
            ingredients (List[str]): List of detected food items
            limit (int): Maximum number of recipes to return
            
        Returns:
            List[Dict[str, Any]]: List of recipes with their details
        """
        # Join ingredients with commas for API query
        ingredients_str = ','.join(ingredients)
        
        # API endpoint for finding recipes by ingredients
        endpoint = f"{self.base_url}/findByIngredients"
        
        # Query parameters
        params = {
            'apiKey': self.api_key,
            'ingredients': ingredients_str,
            'number': limit,
            'ranking': 2,  # Maximize used ingredients
            'ignorePantry': True  # Ignore common ingredients
        }
        
        try:
            # Make API request
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            recipes = response.json()
            
            # Get detailed information for each recipe
            detailed_recipes = []
            for recipe in recipes:
                recipe_id = recipe['id']
                detailed_recipe = self._get_recipe_details(recipe_id)
                if detailed_recipe:
                    detailed_recipes.append(detailed_recipe)
            
            return detailed_recipes
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recipes: {str(e)}")
            return []

    def _get_recipe_details(self, recipe_id: int) -> Dict[str, Any]:
        """
        Get detailed information for a specific recipe
        
        Args:
            recipe_id (int): Recipe ID
            
        Returns:
            Dict[str, Any]: Detailed recipe information
        """
        endpoint = f"{self.base_url}/{recipe_id}/information"
        
        params = {
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recipe details: {str(e)}")
            return None
