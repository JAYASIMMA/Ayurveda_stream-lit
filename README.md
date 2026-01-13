# 🌿 AyurParam AI - Ayurvedic Knowledge Assistant

A beautiful Streamlit application powered by Ollama, providing ancient Ayurvedic wisdom through modern AI.

## Features

- 🎨 **Elegant Dark/Light Themes** - Premium black & white design with gold accents
- 🤖 **Ollama Integration** - Configurable API endpoint and model
- 📖 **Formatted Responses** - Beautiful markdown rendering with proper formatting
- ⚙️ **Customizable Parameters** - Control temperature, top-p, top-k, and token length
- 🌿 **Ancient Wisdom** - Learn about herbs, doshas, treatments, and classical texts

## Deployment

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run ayurparam_streamlit.py
```

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and branch
6. Set main file path: `ayurparam_streamlit.py`
7. Click "Deploy"

## Configuration

Configure your Ollama API URL and model in the sidebar:
- **Ollama API URL**: Your Ollama server endpoint
- **Model Name**: e.g., `Jayasimma/Ayurveda-8b`

## Technologies

- **Streamlit** - Web framework
- **Ollama** - AI model serving
- **Python** - Backend language

## Disclaimer

This AI provides information based on Ayurvedic texts for educational purposes only. Please consult a qualified Ayurvedic practitioner for medical advice.

---

Made with 💚 | Powered by Bettrlabs
