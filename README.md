# Image Content Analyzer

A Streamlit application that uses Google's Gemini Vision AI to analyze images and search for item prices across online marketplaces.

## Features

- Image upload and analysis using Google Gemini Vision AI
- Automatic item detection and categorization
- Real-time price searching on Amazon and eBay
- Interactive table with editable item names and brands
- Direct links to product searches
- Price comparison between new and used items

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required dependencies:
```bash
pip install streamlit google-generativeai Pillow requests beautifulsoup4
```

3. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Enter your Google Gemini API key when prompted
3. Upload an image to analyze
4. Click "Analyze Image" to detect items
5. Edit item names/brands and use "Update" buttons to refresh price searches

## Components

- `app.py`: Main Streamlit application
- `gemini_helper.py`: Google Gemini Vision AI integration
- `price_helper.py`: Price searching functionality for Amazon and eBay

## Requirements

- Python 3.7+
- Streamlit
- Google Generative AI
- Pillow
- BeautifulSoup4
- Requests

## Notes

- Price searching is done through web scraping and may be subject to rate limiting
- Image analysis requires a valid Google Gemini API key
- The application resizes images before processing to optimize performance

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
