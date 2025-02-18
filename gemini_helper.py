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
        Analyze this image and return a JSON object with the following structure:
        {
            "scene": "description of the scene (indoor/outdoor, environment)",
            "people": "description of people if any (count, actions, expressions)",
            "objects": ["list of main objects identified"],
            "mood": "overall mood or emotion of the scene"
        }
        
        Return ONLY the JSON object, no additional text.
        """

        # Generate description
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None
