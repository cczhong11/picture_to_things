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
        Analyze this image and return a valid JSON array.
        Format your response EXACTLY like this example:
        [
            {
                "item_name": "Blue Nike Sneaker",
                "details": {
                    "type": "Athletic Footwear",
                    "brand": "Nike",
                    "color": "Blue and White",
                    "condition": "New",
                    "distinctive_features": ["Mesh upper", "White swoosh logo"],
                    "is_main_focus": true
                }
            }
        ]
        
        Important:
        - Return ONLY the JSON array, no other text
        - Use proper JSON syntax with double quotes
        - Boolean values must be true or false (lowercase)
        - Always include all fields, use empty string "" or empty array [] if no value
        - List main focus item first, followed by background items
        """

        # Generate description
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None
