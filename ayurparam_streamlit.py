import streamlit as st
import requests
import json
import markdown


# Page configuration
st.set_page_config(
    page_title="Bettrlabs - Ayurvedic AI",
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
            'gradient_start': '#000000',
            'gradient_mid': '#1a1a1a',
            'gradient_end': '#0a0a0a',
            'primary': '#d4af37',  # Gold
            'accent': '#f4e4b7',   # Light gold
            'secondary': '#00d4ff', # Cyan accent
            'bg_overlay': 'rgba(0, 0, 0, 0.8)',
            'glass_bg': 'rgba(255, 255, 255, 0.05)',
            'glass_border': 'rgba(212, 175, 55, 0.3)',
            'text_primary': '#ffffff',
            'text_secondary': '#d1d5db',
            'card_bg': 'rgba(255, 255, 255, 0.08)',
            'response_bg': 'rgba(212, 175, 55, 0.1)',
            'response_border': '#d4af37',
        }
    else:  # light theme
        return {
            'gradient_start': '#ffffff',
            'gradient_mid': '#f0f0f0',
            'gradient_end': '#e5e5e5',
            'primary': '#000000',  # Black for high contrast default text
            'accent': '#d4af37',   # Gold accent
            'secondary': '#0ea5e9', 
            'bg_overlay': 'rgba(255, 255, 255, 0.98)',
            'glass_bg': 'rgba(255, 255, 255, 0.98)',
            'glass_border': 'rgba(0, 0, 0, 0.1)',
            'text_primary': '#000000', # Pure black for maximum readability
            'text_secondary': '#374151', # Dark gray
            'card_bg': '#ffffff', # Pure white background for inputs
            'response_bg': 'rgba(240, 240, 240, 0.8)',
            'response_border': '#d4af37',
            'input_bg': '#ffffff', # Distinct input background
            'input_text': '#000000', # Dark text for inputs
            'sidebar_text': '#000000' # Sidebar text
        }

# Get current theme colors
colors = get_theme_colors(st.session_state.theme)

# Dynamic CSS based on theme
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700;800&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {colors['gradient_start']} 0%, {colors['gradient_mid']} 50%, {colors['gradient_end']} 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: {colors['text_primary']} !important;
    }}
    
    /* General text visibility ensuring all labels and inputs are readable */
    p, label, h1, h2, h3, h4, h5, h6, li, span {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Sidebar specific styling */
    section[data-testid="stSidebar"] {{
        background: {colors['gradient_start']};
        border-right: 1px solid {colors['glass_border']};
    }}
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {{
        color: {colors['text_primary']} !important;
    }}

    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 20% 80%, {colors['response_bg']} 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(0, 212, 255, 0.05) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }}
    
    .main-header {{
        text-align: center;
        padding: 3rem 0 2rem 0;
        border-bottom: 1px solid {colors['glass_border']};
        margin-bottom: 2rem;
    }}
    
    .main-title {{
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['accent']} 50%, {colors['primary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.8rem;
        letter-spacing: 2px;
        text-shadow: 0 4px 20px {colors['response_bg']};
    }}
    
    .subtitle {{
        font-size: 1.1rem;
        color: {colors['text_secondary']};
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    
    .glass-card {{
        background: {colors['glass_bg']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {colors['glass_border']};
        border-radius: 16px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
        border-color: {colors['primary']};
    }}
    
    .response-area {{
        background: {colors['response_bg']};
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid {colors['response_border']};
        border-left: 4px solid {colors['primary']};
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        color: {colors['text_primary']};
        font-size: 1.05rem;
        line-height: 2;
        box-shadow: 0 8px 30px {colors['response_bg']};
        animation: fadeIn 0.6s ease-out;
    }}
    
    .response-area h1, .response-area h2, .response-area h3,
    .response-area h4, .response-area h5, .response-area h6 {{
        color: {colors['text_primary']} !important;
        margin-top: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }}
    
    .response-area h2 {{
        border-bottom: 2px solid {colors['primary']};
        padding-bottom: 0.5rem;
    }}
    
    .response-area p {{
        color: {colors['text_primary']} !important;
        margin-bottom: 1.2rem;
    }}
    
    .response-area ul, .response-area ol {{
        color: {colors['text_primary']} !important;
        margin-left: 2rem;
        margin-bottom: 1.5rem;
    }}
    
    .response-area li {{
        color: {colors['text_primary']} !important;
        margin-bottom: 0.8rem;
        padding-left: 0.5rem;
    }}
    
    .response-area li::marker {{
        color: {colors['primary']};
    }}
    
    .response-area strong {{
        color: {colors['primary']} !important;
        font-weight: 700;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['accent']} 100%) !important;
        color: {('#000000' if st.session_state.theme == 'dark' else '#ffffff')} !important;
        font-weight: 700 !important;
        padding: 0.9rem 3rem !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 6px 25px {colors['response_bg']} !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        font-size: 0.9rem !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 10px 35px {colors['response_bg']} !important;
    }}
    
    section[data-testid="stSidebar"] h2 {{
        color: {colors['text_primary']} !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }}
    
    section[data-testid="stSidebar"] h3 {{
        color: {colors['primary']} !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }}
    
    .sidebar-section {{
        background: {colors['card_bg']};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.2rem 0;
        border: 1px solid {colors['glass_border']};
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }}
    
    /* INPUT FIELDS STYLING - Critical for visibility */
    .stTextInput input, .stTextArea textarea {{
        background-color: {colors['card_bg']} !important;
        border: 1px solid {colors['glass_border']} !important;
        border-radius: 8px !important;
        color: {colors['text_primary']} !important; 
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 0.8rem !important;
        caret-color: {colors['primary']} !important;
    }}
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: {colors['text_secondary']} !important;
        opacity: 0.7 !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {colors['primary']} !important;
        box-shadow: 0 0 0 2px {colors['response_bg']} !important;
        background-color: {colors['card_bg']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Ensure validation text is visible */
    .stAlert {{
        color: {colors['text_primary']} !important;
    }}
    
    .stAlert p {{
        color: {colors['text_primary']} !important;
    }}

    /* Ensure spinner text is visible */
    .stSpinner > div > div {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Ensure label text is visible */
    label[data-testid="stWidgetLabel"] {{
        color: {colors['text_primary']} !important;
    }}

    
    .stSlider > div > div > div > div {{
        background: {colors['primary']} !important;
        box-shadow: 0 0 12px {colors['response_bg']} !important;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['gradient_start']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {colors['primary']}, {colors['accent']});
        border-radius: 6px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['primary']};
    }}
    
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin: 2.5rem 0;
    }}
    
    .feature-card {{
        background: {colors['glass_bg']};
        backdrop-filter: blur(10px);
        border: 1px solid {colors['glass_border']};
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {colors['primary']}, {colors['secondary']});
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }}
    
    .feature-card:hover::before {{
        transform: scaleX(1);
    }}
    
    .feature-card:hover {{
        transform: translateY(-10px);
        border-color: {colors['primary']};
        box-shadow: 0 15px 50px {colors['response_bg']};
    }}
    
    .feature-icon {{
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        filter: grayscale(20%);
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover .feature-icon {{
        transform: scale(1.1);
        filter: grayscale(0%);
    }}
    
    .feature-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {colors['primary']};
        margin-bottom: 0.8rem;
        font-family: 'Playfair Display', serif;
    }}
    
    .feature-desc {{
        font-size: 0.95rem;
        color: {colors['text_primary']};
        line-height: 1.7;
        font-weight: 400;
    }}
    
    /* Labels */
    label {{
        color: {colors['text_primary']} !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    
    /* Success/Warning/Error boxes */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)) !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 8px !important;
    }}
    
    .stWarning {{
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(251, 191, 36, 0.05)) !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid #fbbf24 !important;
        border-radius: 8px !important;
    }}
    
    .stError {{
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05)) !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
    }}
    
    /* Markdown headings in main area */
    .main h1, .main h2, .main h3 {{
        color: {colors['text_primary']} !important;
        font-weight: 700 !important;
    }}
    
    .main h3 {{
        color: {colors['primary']} !important;
    }}
    
    .main p {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Divider */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {colors['primary']}, transparent);
        margin: 2rem 0;
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
    # Header without logo (logo only in sidebar)
    st.markdown(f"""
        <div class="main-header">
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 1.3rem; font-weight: 700; color: {colors['primary']}; letter-spacing: 4px; text-transform: uppercase; font-family: 'Playfair Display', serif;">
                    Bettrlabs
                </div>
            </div>
            <div class="main-title">Ayurveda AI</div>
            <div class="subtitle">Ancient Wisdom • Modern Intelligence</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown(f"""
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
        # Logo and branding in sidebar - left aligned using columns for proper vertical alignment
        logo_col, text_col = st.columns([1, 4])
        with logo_col:
            try:
                st.image("logo.jpg", width=50)
            except:
                st.write("🌿")
        
        with text_col:
            st.markdown(f"""
                <div style="font-size: 1.1rem; font-weight: 700; color: {colors['primary']}; letter-spacing: 2px; font-family: 'Playfair Display', serif; padding-top: 10px;">
                    Bettrlabs
                </div>
            """, unsafe_allow_html=True)
        
        # Configuration Heading
        st.markdown(f'''<div class="sidebar-section">
            <h3 style="color: {colors['primary']} !important; margin: 0; padding: 0;">⚙️ Configuration</h3>
        </div>''', unsafe_allow_html=True)
        
        # Theme Toggle - Simple checkbox
        theme_toggle = st.checkbox(
            "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode",
            value=(st.session_state.theme == 'dark'),
            help="Toggle between dark and light themes"
        )
        
        # Update theme based on checkbox
        new_theme = 'dark' if theme_toggle else 'light'
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        # Ollama Settings
        st.markdown(f'''<div class="sidebar-section">
            <h3 style="color: {colors['primary']} !important; margin: 0; padding: 0;">🤖 Ollama Settings</h3>
        </div>''', unsafe_allow_html=True)
        
        ollama_url = st.text_input(
            "Ollama API URL",
            value="",
            placeholder="http://your-server:port/api/generate",
            help="Enter your Ollama API endpoint URL"
        )
        
        model_name = st.text_input(
            "Model Name",
            value="Jayasimma/Ayurveda-8b",
            help="Specify the Ollama model name"
        )
        
        # Generation Parameters
        st.markdown(f'''<div class="sidebar-section">
            <h3 style="color: {colors['primary']} !important; margin: 0; padding: 0;">🎛️ Generation Parameters</h3>
        </div>''', unsafe_allow_html=True)
        
        max_new_tokens = st.slider(
            "Max Output Length",
            min_value=50,
            max_value=1000,
            value=700,
            help="Maximum tokens to generate"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
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
        
        # Info
        st.markdown(f'''<div class="sidebar-section">
            <h3 style="color: {colors['primary']} !important; margin: 0; padding-bottom: 10px;">💡 Quick Tips</h3>
            <div style="color: {colors['text_primary']}; font-size: 0.9rem; line-height: 1.8; font-weight: 400;">
                • Ask about herbs & remedies<br>
                • Inquire about doshas & prakruti<br>
                • Explore disease pathogenesis<br>
                • Learn from ancient texts
            </div>
        </div>''', unsafe_allow_html=True)
    
    # Validation
    if not ollama_url:
        st.markdown(f"""
            <div style="background: {colors['response_bg']}; padding: 1.5rem; border-radius: 12px; border: 1px solid {colors['response_border']}; border-left: 4px solid #fbbf24; display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 1rem;">⚠️</span>
                <span style="font-weight: 500; font-size: 1rem; color: {colors['text_primary']};">
                    Please configure your <strong>Ollama API URL</strong> in the sidebar to get started
                </span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    st.success("✅ Ollama configured successfully! Ready to answer your questions.")
    
    # Question Input
    st.markdown(f"### 🔮 Ask Your Ayurvedic Question")
    
    default_prompt = "What is the Samprapti (pathogenesis) of Amavata according to Ayurveda?"
    user_input = st.text_area(
        "Enter your query",
        placeholder=default_prompt,
        height=130,
        help="Type your question about Ayurveda"
    )
    
    
    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("✨ Generate Answer", type="primary", use_container_width=True)
    
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
                        <div style="display: flex; align-items: center; margin-bottom: 1.5rem; padding: 1.5rem; background: {colors['response_bg']}; border-radius: 12px; border: 1px solid {colors['response_border']}; border-left: 4px solid {colors['primary']};">
                            <span style="font-size: 2rem; margin-right: 1rem;">🌿</span>
                            <span style="font-weight: 700; color: {colors['primary']}; font-size: 1.2rem; font-family: 'Playfair Display', serif;">Ayurveda's Wisdom</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Convert markdown response to HTML
                    html_response = markdown.markdown(response)
                    
                    # Style the HTML content to match theme
                    st.markdown(f"""
                        <div class="response-area">
                            {html_response}
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-card here
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; background: {colors['card_bg']}; padding: 2rem; border-radius: 12px; border: 1px solid {colors['glass_border']};">
            <strong style="color: #f59e0b; font-size: 1.05rem;">⚠️ Medical Disclaimer</strong><br>
            <span style="color: {colors['text_primary']}; font-size: 0.95rem; line-height: 1.7;">
                This AI provides information based on Ayurvedic texts for educational purposes only. 
                Please consult a qualified Ayurvedic practitioner for personalized medical advice.
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="text-align: center; color: {colors['text_secondary']}; font-size: 0.9rem; margin-top: 2rem; font-weight: 400;">
            Made with 💚 | Powered by Bettrlabs
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
