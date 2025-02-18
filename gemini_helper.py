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
        Analyze this image and return a JSON object focusing on the main items/objects in the picture.
        Use this structure:
        {
            "main_focus": "describe the primary object/item that is the focus of the image",
            "item_details": {
                "type": "type/category of the item",
                "brand": "brand name if visible/identifiable",
                "color": "color(s) of the item",
                "condition": "condition or state of the item",
                "distinctive_features": ["list any notable features or characteristics"]
            },
            "background_items": ["list any other visible items in the background, if any"]
        }
        
        Return ONLY the JSON object, no additional text.
        Be precise and detailed about the main item in focus.
        If the brand is visible, make sure to include it accurately.
        """

        # Generate description
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None
