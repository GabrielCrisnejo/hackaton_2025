import streamlit as st
from backend import ask_question

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="IMDB AI Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>
    /* Using direct URL for background image and improved gradient overlay */
    .stApp {
        background-image: url('image.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Add dark overlay for better text readability */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 20, 0.6);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Title styling with gradient */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #00d4ff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #8b8b9f;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(20, 20, 40, 0.8);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 12px;
        color: #ffffff;
        font-size: 1.1rem;
        padding: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #ff00ff 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Response card styling */
    .response-card {
        background: rgba(20, 20, 40, 0.6);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
    }
    
    .response-title {
        color: #00d4ff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .response-text {
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: #00d4ff !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 40, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #ff00ff 100%);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# UI
# ---------------------------
st.markdown('<h1 class="main-title">🎬 IMDB AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Pregúntame cualquier cosa sobre películas en nuestra base de datos</p>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Question input
    question = st.text_input(
        "Tu pregunta",
        placeholder="Ej: Detalles de Saving Private Ryan",
        label_visibility="collapsed"
    )
    
    # Submit button
    submit_button = st.button("🔍 Buscar Respuesta")
    
    # Process question
    if submit_button and question:
        with st.spinner("🧠 Pensando..."):
            answer = ask_question(question)
        
        # Display response in styled card
        st.markdown(f"""
        <div class="response-card">
            <div class="response-title">
                🎯 Respuesta
            </div>
            <div class="response-text">
                {answer}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif submit_button and not question:
        st.warning("⚠️ Por favor, ingresa una pregunta")

# Add some example questions
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    with st.expander("💡 Preguntas de ejemplo"):
        st.markdown("""
        - Detalles de Saving Private Ryan
        - ¿Cuál es el género de la película Inception?
        - ¿Quién fue el director de The Dark Knight?
        - ¿Qué año se publicó Titanic?
        - ¿Cuál es la duración de Gladiator?
        - Dame información sobre películas de Christopher Nolan
        """)
