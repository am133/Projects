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

    def find_recipes(self, items: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find recipes based on detected food items, handling both prepared foods and ingredients differently
        
        Args:
            items (List[str]): List of detected food items
            limit (int): Maximum number of recipes to return
            
        Returns:
            List[Dict[str, Any]]: List of recipes with their details
        """
        from vision.food_detector import FoodDetector
        
        # Separate items into prepared foods and ingredients
        prepared_foods = [item for item in items if item in FoodDetector.PREPARED_FOODS]
        ingredients = [item for item in items if item not in FoodDetector.PREPARED_FOODS]
        
        recipes = []
        
        # Handle prepared foods
        if prepared_foods:
            recipes.extend(self._search_recipes_by_query(prepared_foods, limit))
            
        # Handle ingredients
        if ingredients:
            recipes.extend(self._find_recipes_by_ingredients(ingredients, limit))
            
        return recipes[:limit]  # Ensure we don't exceed the limit
        
    def _search_recipes_by_query(self, foods: List[str], limit: int) -> List[Dict[str, Any]]:
        """
        Search recipes for prepared foods using the complexSearch endpoint
        
        Args:
            foods (List[str]): List of prepared food items
            limit (int): Maximum number of recipes to return
            
        Returns:
            List[Dict[str, Any]]: List of recipes matching the query
        """
        # Join food items with OR for broader search
        query = ' OR '.join(f'"{food}"' for food in foods)
        
        # API endpoint for complex search
        endpoint = f"{self.base_url}/complexSearch"
        
        # Query parameters
        params = {
            'apiKey': self.api_key,
            'query': query,
            'number': limit,
            'addRecipeInformation': True,  # Include full recipe details
            'fillIngredients': True,  # Include ingredient information
            'instructionsRequired': True  # Only return recipes with instructions
        }
        
        try:
            # Make API request
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            results = response.json()
            
            return results.get('results', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching recipes: {str(e)}")
            return []
            
    def _find_recipes_by_ingredients(self, ingredients: List[str], limit: int) -> List[Dict[str, Any]]:
        """
        Find recipes based on ingredients using the findByIngredients endpoint
        
        Args:
            ingredients (List[str]): List of ingredients
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
