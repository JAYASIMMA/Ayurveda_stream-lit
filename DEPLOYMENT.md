# AyurParam AI - Deployment Guide

## ✅ Files Ready for Streamlit Cloud

Your app is now ready to deploy! Here are all the files you need:

### Required Files (✅ Created)
- `ayurparam_streamlit.py` - Main application
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `README.md` - Documentation

## 🚀 How to Deploy to Streamlit Cloud

### Step 1: Push to GitHub
Your code is already pushed to GitHub at:
`https://github.com/JAYASIMMA/Ayurveda_stream-lit.git`

Make sure to push any recent changes:
```bash
git add .
git commit -m "Add deployment files"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io

2. **Sign in** with your GitHub account

3. **Click "New app"** button

4. **Fill in the deployment form**:
   - **Repository**: `JAYASIMMA/Ayurveda_stream-lit`
   - **Branch**: `main`
   - **Main file path**: `ayurparam_streamlit.py`

5. **Advanced settings** (optional):
   - You can add secrets for API keys if needed
   - The app will use the `.streamlit/config.toml` automatically

6. **Click "Deploy"**

7. **Wait** for deployment (usually takes 2-3 minutes)

### Step 3: Configure After Deployment

Once deployed, users will need to:
- Enter their **Ollama API URL** in the sidebar
- Verify the **model name** is correct

## 📝 Notes

- The app requires an **Ollama API endpoint** to function
- Make sure your Ollama server is accessible from the internet
- Consider using environment variables for sensitive configuration

## 🔗 Your Repository
https://github.com/JAYASIMMA/Ayurveda_stream-lit.git

---

Made with 💚 | Powered by Bettrlabs
