import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="AyurParam - Ayurvedic AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def get_theme_colors(theme):
    """Return color scheme based on selected theme"""
    if theme == 'dark':
        return {
            'gradient_start': '#064e3b',
            'gradient_mid': '#065f46',
            'gradient_end': '#047857',
            'primary': '#22c55e',
            'accent': '#10b981',
            'bg_overlay': 'rgba(0, 0, 0, 0.5)',
            'glass_bg': 'rgba(255, 255, 255, 0.05)',
            'glass_border': 'rgba(255, 255, 255, 0.1)',
            'text_primary': '#ffffff',
            'text_secondary': '#cbd5e1',
            'card_bg': 'rgba(255, 255, 255, 0.05)',
            'response_bg_start': 'rgba(34, 197, 94, 0.15)',
            'response_bg_end': 'rgba(16, 185, 129, 0.1)',
        }
    else:  # light theme
        return {
            'gradient_start': '#d1fae5',
            'gradient_mid': '#a7f3d0',
            'gradient_end': '#6ee7b7',
            'primary': '#059669',
            'accent': '#047857',
            'bg_overlay': 'rgba(255, 255, 255, 0.8)',
            'glass_bg': 'rgba(255, 255, 255, 0.7)',
            'glass_border': 'rgba(6, 95, 70, 0.2)',
            'text_primary': '#0f172a',
            'text_secondary': '#475569',
            'card_bg': 'rgba(255, 255, 255, 0.7)',
            'response_bg_start': 'rgba(5, 150, 105, 0.1)',
            'response_bg_end': 'rgba(4, 120, 87, 0.05)',
        }

# Get current theme colors
colors = get_theme_colors(st.session_state.theme)

# Dynamic CSS based on theme
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_mid']} 50%, {colors['gradient_end']} 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 80%, {colors['response_bg_start']} 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, {colors['response_bg_end']} 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}
    
    .main-header {{
        text-align: center;
        padding: 2rem 0 1rem 0;
    }}
    
    .main-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['accent']} 50%, {colors['primary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: gradient-shift 3s ease infinite;
        text-shadow: 0 0 40px {colors['response_bg_start']};
    }}
    
    @keyframes gradient-shift {{
        0%, 100% {{ filter: brightness(1); }}
        50% {{ filter: brightness(1.3); }}
    }}
    
    .subtitle {{
        font-size: 1.2rem;
        color: {colors['text_secondary']};
        font-weight: 400;
        letter-spacing: 1px;
    }}
    
    .glass-card {{
        background: {colors['glass_bg']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {colors['glass_border']};
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }}
    
    .response-area {{
        background: linear-gradient(135deg, {colors['response_bg_start']} 0%, {colors['response_bg_end']} 100%);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid {colors['glass_border']};
        border-left: 4px solid {colors['primary']};
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        color: {colors['text_primary']};
        font-size: 1.05rem;
        line-height: 1.9;
        box-shadow: 0 4px 24px {colors['response_bg_start']};
        animation: fadeIn 0.5s ease-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['accent']} 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2.5rem !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px {colors['response_bg_start']} !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-size: 0.95rem !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px {colors['response_bg_start']} !important;
    }}
    
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {colors['card_bg']} 0%, {colors['glass_bg']} 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid {colors['glass_border']};
    }}
    
    .sidebar-section {{
        background: {colors['card_bg']};
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        border: 1px solid {colors['glass_border']};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    
    .stTextInput input, .stTextArea textarea {{
        background: {colors['card_bg']} !important;
        border: 1px solid {colors['glass_border']} !important;
        border-radius: 10px !important;
        color: {colors['text_primary']} !important;
        font-size: 0.95rem !important;
    }}
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: {colors['text_secondary']} !important;
        opacity: 0.6 !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {colors['primary']} !important;
        box-shadow: 0 0 0 2px {colors['response_bg_start']} !important;
    }}
    
    .stSlider > div > div > div {{
        background: linear-gradient(90deg, {colors['gradient_start']}, {colors['primary']}) !important;
    }}
    
    .stSlider > div > div > div > div {{
        background: {colors['primary']} !important;
        box-shadow: 0 0 10px {colors['response_bg_start']} !important;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['glass_bg']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {colors['primary']}, {colors['accent']});
        border-radius: 5px;
    }}
    
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .feature-card {{
        background: {colors['glass_bg']};
        backdrop-filter: blur(10px);
        border: 1px solid {colors['glass_border']};
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }}
    
    .feature-card:hover {{
        transform: translateY(-8px) scale(1.02);
        border-color: {colors['primary']};
        box-shadow: 0 12px 40px {colors['response_bg_start']};
    }}
    
    .feature-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px {colors['response_bg_start']});
    }}
    
    .feature-title {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {colors['primary']};
        margin-bottom: 0.5rem;
    }}
    
    .feature-desc {{
        font-size: 0.9rem;
        color: {colors['text_secondary']};
        line-height: 1.5;
    }}
    
    /* Theme Toggle Button */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: {colors['glass_bg']};
        backdrop-filter: blur(10px);
        border: 1px solid {colors['glass_border']};
        border-radius: 50px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px {colors['response_bg_start']};
    }}
    
    /* Labels */
    label {{
        color: {colors['text_primary']} !important;
        font-weight: 500 !important;
    }}
    
    /* Success/Warning/Error boxes */
    .stSuccess, .stWarning, .stError {{
        color: {colors['text_primary']} !important;
    }}
</style>
""", unsafe_allow_html=True)

def clean_response(text: str) -> str:
    """Clean unwanted Unicode escape sequences from the response."""
    import re
    cleaned = re.sub(r'\s*\([\\u0-9a-fA-F]+\)', '', text)
    return cleaned

def query_ollama(prompt: str, ollama_url: str, model_name: str, max_tokens: int, temperature: float, top_p: float, top_k: int) -> str:
    """Send a request to Ollama API and return the response."""
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        raw_response = result.get("response", "")
        cleaned_response = clean_response(raw_response)
        return cleaned_response
        
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <div class="main-title">🌿 AyurParam AI</div>
            <div class="subtitle">Ancient Wisdom • Modern Intelligence • Powered by Ollama</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("""
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🍃</div>
                <div class="feature-title">Herbal Wisdom</div>
                <div class="feature-desc">Discover medicinal herbs and their therapeutic properties</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚕️</div>
                <div class="feature-title">Treatment Insights</div>
                <div class="feature-desc">Traditional healing methods and remedies</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📜</div>
                <div class="feature-title">Ancient Texts</div>
                <div class="feature-desc">Knowledge from classical Ayurvedic scriptures</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Theme Toggle
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎨 Theme")
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button("🌙 Dark", use_container_width=True, type="primary" if st.session_state.theme == 'dark' else "secondary"):
                st.session_state.theme = 'dark'
                st.rerun()
        with theme_col2:
            if st.button("☀️ Light", use_container_width=True, type="primary" if st.session_state.theme == 'light' else "secondary"):
                st.session_state.theme = 'light'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Ollama Settings
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🤖 Ollama Settings")
        
        ollama_url = st.text_input(
            "Ollama API URL",
            value="",
            placeholder="http://your-server:port/api/generate",
            help="Enter your Ollama API endpoint URL"
        )
        
        model_name = st.text_input(
            "Model Name",
            value="Jayasimma/Ayurveda-8b",
            help="Specify the Ollama model name (e.g., Jayasimma/Ayurveda-8b)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Generation Parameters
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Generation Parameters")
        
        max_new_tokens = st.slider(
            "Max Output Length",
            min_value=50,
            max_value=1000,
            value=300,
            help="Maximum tokens to generate"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        top_p = st.slider(
            "Top-p",
            min_value=0.0,
            max_value=1.0,
            value=0.95,
            step=0.05,
            help="Nucleus sampling threshold"
        )
        
        top_k = st.slider(
            "Top-k",
            min_value=1,
            max_value=100,
            value=50,
            help="Number of top tokens to consider"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Info
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 💡 Quick Tips")
        st.markdown(f"""
            <div style="color: {colors['text_secondary']}; font-size: 0.85rem; line-height: 1.7;">
                • Ask about herbs & remedies<br>
                • Inquire about doshas & prakruti<br>
                • Explore disease pathogenesis<br>
                • Learn from ancient texts
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Content
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Validation
    if not ollama_url:
        st.warning("⚠️ Please configure your Ollama API URL in the sidebar to get started")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.success("✅ Ollama configured successfully! Ready to answer your questions.")
    
    # Question Input
    st.markdown("### 🔮 Ask Your Ayurvedic Question")
    
    default_prompt = "What is the Samprapti (pathogenesis) of Amavata according to Ayurveda?"
    user_input = st.text_area(
        "Enter your query",
        placeholder=default_prompt,
        height=130,
        help="Type your question about Ayurveda, herbs, treatments, or concepts"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("🌟 Generate Answer", type="primary", use_container_width=True)
    
    # Response Generation
    if generate_btn:
        if not user_input.strip():
            st.warning("⚠️ Please enter a question to receive an answer")
        else:
            with st.spinner("🔄 Consulting ancient Ayurvedic wisdom..."):
                formatted_prompt = f"<user> {user_input} <assistant>"
                
                response = query_ollama(
                    formatted_prompt,
                    ollama_url,
                    model_name,
                    max_new_tokens,
                    temperature,
                    top_p,
                    top_k
                )
                
                if response.startswith("Error:"):
                    st.error(f"❌ {response}")
                else:
                    st.markdown("### 📖 Response")
                    
                    st.markdown(f"""
                        <div style="display: flex; align-items: center; margin-bottom: 1rem; padding: 1.2rem; background: linear-gradient(135deg, {colors['response_bg_start']}, {colors['response_bg_end']}); border-radius: 12px; border-left: 4px solid {colors['primary']};">
                            <span style="font-size: 1.8rem; margin-right: 0.8rem;">🌿</span>
                            <span style="font-weight: 600; color: {colors['primary']}; font-size: 1.1rem;">AyurParam's Wisdom</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="response-area">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(response)
                    
                    st.markdown("""
                        </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; background: {colors['card_bg']}; padding: 1.5rem; border-radius: 12px; border: 1px solid {colors['glass_border']};">
            <strong style="color: #f59e0b;">⚠️ Medical Disclaimer:</strong>
            <span style="color: {colors['text_secondary']}; font-size: 0.9rem;">
                This AI provides information based on Ayurvedic texts for educational purposes only. 
                Please consult a qualified Ayurvedic practitioner for personalized medical advice and treatment.
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="text-align: center; color: {colors['text_secondary']}; font-size: 0.85rem; margin-top: 1.5rem; opacity: 0.7;">
            Made with 💚 | Powered by Bettrlabs
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
