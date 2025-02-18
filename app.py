import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from gemini_helper import get_description

# Configure page
st.set_page_config(page_title="Image Analyzer", layout="wide")

# Initialize Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("Please set GOOGLE_API_KEY environment variable")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

def main():
    st.title("Image Content Analyzer")
    st.write("Upload an image to analyze its contents using Google Gemini")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Add analyze button
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                # Save temporary file
                temp_path = "temp_image.jpg"
                image.save(temp_path)
                
                # Get description
                description = get_description(temp_path, model)
                
                if description:
                    st.write("### Analysis Results:")
                    st.write(description)
                else:
                    st.error("Failed to analyze image")
                
                # Clean up temp file
                os.remove(temp_path)

if __name__ == "__main__":
    main()
