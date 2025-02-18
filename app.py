import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from gemini_helper import get_description

# Configure page
st.set_page_config(page_title="Image Analyzer", layout="wide")


def main():
    st.title("Image Content Analyzer")
    st.write("Upload an image to analyze its contents using Google Gemini")

    # API Key input
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")
    if not api_key:
        st.warning("Please enter your Google Gemini API Key to proceed")
        st.stop()

    # Initialize Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        st.stop()

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file", type=["png", "jpg", "jpeg"]
    )

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
                    try:
                        # Clean the response to ensure it's valid JSON
                        cleaned_description = description.strip()
                        if cleaned_description.startswith('```json'):
                            cleaned_description = cleaned_description[7:]
                        if cleaned_description.endswith('```'):
                            cleaned_description = cleaned_description[:-3]
                        cleaned_description = cleaned_description.strip()
                        
                        items = json.loads(cleaned_description)
                        st.write("### Items Detected")
                        
                        # Prepare data for table
                        table_data = []
                        for item in items:
                            features = ", ".join(item['details']['distinctive_features']) if item['details']['distinctive_features'] else ""
                            focus = "✓" if item['details']['is_main_focus'] else ""
                            table_data.append({
                                "Main Focus": focus,
                                "Item Name": item['item_name'],
                                "Type": item['details']['type'],
                                "Brand": item['details']['brand'],
                                "Color": item['details']['color'],
                                "Condition": item['details']['condition'],
                                "Distinctive Features": features
                            })
                        
                        # Display as table
                        st.table(table_data)
                    except json.JSONDecodeError as e:
                        st.error(f"Failed to parse analysis results: {str(e)}")
                        st.write("Raw response:")
                        st.code(description)
                else:
                    st.error("Failed to analyze image")

                # Clean up temp file
                os.remove(temp_path)


if __name__ == "__main__":
    main()
