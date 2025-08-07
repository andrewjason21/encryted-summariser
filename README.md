Encrypted Multi-language Text Summarizer
Overview
This project is a Privacy-First Multi-language Text Summarizer built with Gradio and Python. It supports English and Hindi text summarization using TF-IDF based extractive summarization, along with keyword extraction. The summaries are encrypted with strong cryptography (Fernet symmetric encryption) to ensure user privacy.

Complementing the backend app, there is a Chrome browser extension that lets users select any text on web pages and summarize it by calling the deployed backend API.

Features
Extractive summarization and keyword extraction for English and Hindi texts.

Language-specific sentence tokenization and stopword handling.

Summary encryption and decryption with a unique secret key.

Download encrypted summary files for secure storage.

Browser extension enables text summarization directly from any webpage selection.

Easy integration with deployed API hosted on Hugging Face Spaces for permanent availability.

Modern Gradio UI with tabs for summarization/encryption and decryption.

Files in this Repository
app.py — Gradio-based summarization and encryption backend app supporting multi-language.

requirements.txt — Python dependencies for running the app.

manifest.json — Chrome extension manifest declaring permissions and resources.

background.js — Extension background script to create context menu.

popup.html — Extension popup UI showing selected text input and summarization results.

popup.js — Extension frontend JavaScript handling user input, API call, and displaying summary.

Getting Started
Prerequisites
Python 3.x installed

Git installed (optional for cloning)

Chrome browser (or Chromium-based) for the extension

Hugging Face account (optional) for deploying backend API

Backend Setup (Local)
Clone the repo and navigate to backend folder.

Install dependencies:

bash
pip install -r requirements.txt
Run the Gradio app:

bash
python app.py
The app will start locally with a URL (e.g., http://127.0.0.1:7860) for testing.

Deploy Backend on Hugging Face Spaces (Recommended)
Create a Hugging Face Space.

Upload app.py and requirements.txt.

Wait for build and deployment.

Get your Space’s public API URL from the API tab.

Update your browser extension’s popup.js file with this API endpoint.

Browser Extension Setup
Open Chrome and go to chrome://extensions/.

Enable Developer mode.

Click Load unpacked and select the folder containing the extension files (manifest.json, etc.).

Right-click any webpage text and select Summarize Highlighted Text.

In the popup, press Summarize! to get the summary and keywords fetched from backend API.

Usage
Summarize and Encrypt:

Paste or select text.

Choose language (English/Hindi).

Select summary sentence count and keywords count.

Generate encrypted summary with secure key.

Download encrypted file.

Decrypt Encrypted Summary:

Upload encrypted .bin file.

Provide secret key.

Get original decrypted summary.

Troubleshooting
Ensure the backend API URL is correctly set in popup.js.

If you see CORS or Content Security Policy errors, confirm extension permissions and test API calls directly from extension popup.

Check Hugging Face Space build logs for backend errors.

Configure git identity before committing code changes (for GitHub use).

Contributing
Feel free to open issues or pull requests. Suggestions to add languages or abstractive summarization welcome!

License
This project is licensed under the MIT License.

Acknowledgements
Built with Gradio, Cryptography, NLTK, and scikit-learn.

Hosted on Hugging Face Spaces.
