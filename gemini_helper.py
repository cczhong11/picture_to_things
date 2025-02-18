import google.generativeai as genai
from PIL import Image

def get_description(image_path, model: genai.GenerativeModel):
    """Get description for an image using Gemini model"""
    try:
        # Open and resize image to W/5 x H/5
        image = Image.open(image_path)
        width, height = image.size
        new_width = max(1, width // 5)
        new_height = max(1, height // 5)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        prompt = """
        Analyze this image and return a JSON array of items/objects in the picture.
        For each item use this structure:
        {
            "item_name": "name of the item",
            "details": {
                "type": "type/category of the item",
                "brand": "brand name if visible/identifiable",
                "color": "color(s) of the item",
                "condition": "condition or state of the item",
                "distinctive_features": ["list any notable features or characteristics"],
                "is_main_focus": boolean indicating if this is the main focus of the image
            }
        }
        
        Return ONLY the JSON array of items, no additional text.
        List the main focus item first, followed by other visible items.
        Be precise and detailed about each item.
        If brands are visible, make sure to include them accurately.
        """

        # Generate description
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None
