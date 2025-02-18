import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import os
from gemini_helper import get_description
from price_helper import search_prices

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
                        if cleaned_description.startswith("```json"):
                            cleaned_description = cleaned_description[7:]
                        if cleaned_description.endswith("```"):
                            cleaned_description = cleaned_description[:-3]
                        cleaned_description = cleaned_description.strip()

                        items = json.loads(cleaned_description)

                        # Prepare data for table
                        table_data = []
                        for item in items:
                            features = (
                                ", ".join(item["details"]["distinctive_features"])
                                if item["details"]["distinctive_features"]
                                else ""
                            )
                            focus = "✓" if item["details"]["is_main_focus"] else ""
                            # Get price estimates
                            try:
                                prices = search_prices(
                                    item["item_name"],
                                    item["details"]["type"],
                                    item["details"]["brand"],
                                )
                                print(f"Price search results: {prices}")
                            except Exception as e:
                                print(f"Error in price search: {str(e)}")
                                prices = {
                                    "new_price": "Error",
                                    "used_price": "Error",
                                    "search_query": "",
                                    "amazon_url": "",
                                    "ebay_url": ""
                                }

                            table_data.append(
                                {
                                    "Main Focus": focus,
                                    "Item Name": item["item_name"],
                                    "Type": item["details"]["type"],
                                    "Brand": item["details"]["brand"],
                                    "Color": item["details"]["color"],
                                    "Condition": item["details"]["condition"],
                                    "New Price Range": prices["new_price"],
                                    "Used Price Range": prices["used_price"],
                                    "Distinctive Features": features,
                                }
                            )

                        # Update session state with new data
                        st.session_state.table_data = table_data

                    except json.JSONDecodeError as e:
                        st.error(f"Failed to parse analysis results: {str(e)}")
                        st.write("Raw response:")
                        st.code(description)
                else:
                    st.error("Failed to analyze image")

                # Clean up temp file
                os.remove(temp_path)

        # Display table if data exists
        if "table_data" in st.session_state:
            st.write("### Items Detected")
            st.write("Edit item names and use update buttons to search for new prices")

            # Convert table data to DataFrame for editing
            import pandas as pd

            df = pd.DataFrame(st.session_state.table_data)

            # Create columns for layout
            for index, row in df.iterrows():
                with st.container():
                    cols = st.columns([3, 2, 2, 2, 1])

                    # Column 1: Item details
                    with cols[0]:
                        item_name = st.text_input(
                            "Item Name",
                            row["Item Name"],
                            key=f"name_{index}",
                        )
                        brand = st.text_input(
                            "Brand", row["Brand"], key=f"brand_{index}"
                        )
                        st.write(f"**Type:** {row['Type']}")

                    # Column 2: Color and Condition
                    with cols[1]:
                        st.write(f"**Color:** {row['Color']}")
                        st.write(f"**Condition:** {row['Condition']}")
                        if row["Main Focus"] == "✓":
                            st.write("**Main Focus:** Yes")

                    # Column 3: Current Prices and Links
                    with cols[2]:
                        if f"prices_{index}" in st.session_state:
                            prices = st.session_state[f"prices_{index}"]
                        else:
                            prices = {
                                "new_price": row["New Price Range"],
                                "used_price": row["Used Price Range"],
                                "amazon_url": f"https://www.amazon.com/s?k={row['Brand']}+{row['Item Name']}+{row['Type']}".replace(
                                    " ", "+"
                                ),
                                "ebay_url": f"https://www.ebay.com/sch/i.html?_nkw={row['Brand']}+{row['Item Name']}+{row['Type']}".replace(
                                    " ", "+"
                                ),
                            }
                        st.write("**Current Prices:**")
                        st.write(f"New: {prices['new_price']}")
                        st.write(f"Used: {prices['used_price']}")
                        st.write("**Search Links:**")
                        st.markdown(
                            f"[Amazon]({prices['amazon_url']}) | [eBay]({prices['ebay_url']})"
                        )

                    # Column 4: Features
                    with cols[3]:
                        st.write("**Features:**")
                        st.write(row["Distinctive Features"])

                    # Column 5: Update button
                    with cols[4]:
                        if st.button("Update", key=f"update_{index}"):
                            with st.spinner("Updating prices..."):
                                updated_prices = search_prices(
                                    item_name, row["Type"], brand
                                )
                                # Update the row in session state
                                st.session_state.table_data[index][
                                    "New Price Range"
                                ] = updated_prices["new_price"]
                                st.session_state.table_data[index][
                                    "Used Price Range"
                                ] = updated_prices["used_price"]
                                st.session_state.table_data[index][
                                    "Item Name"
                                ] = item_name
                                st.session_state.table_data[index]["Brand"] = brand
                                st.rerun()

                    st.divider()


if __name__ == "__main__":
    main()
