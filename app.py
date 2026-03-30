import streamlit as st
from duckduckgo_search import DDGS
import os
import warnings

# 1. Background Settings & Logs Pause
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Neural Matter AI", layout="wide", initial_sidebar_state="collapsed")

# 2. HEAVY GRAPHICS CSS (Neon & Glassmorphism)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a0a2e 100%) !important;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 15px !important;
        font-size: 20px !important;
        padding: 25px !important;
    }
    .featured-box {
        background: rgba(0, 242, 255, 0.05);
        border-radius: 20px; padding: 30px;
        border: 1px solid rgba(0, 242, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.1);
        margin-bottom: 30px;
    }
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px; border-radius: 15px;
        margin-bottom: 20px; border-left: 5px solid #ff00ea;
    }
    .name-tag {
        color: #ccff00; font-size: 24px; font-weight: bold;
        text-shadow: 0 0 10px #ccff00; text-align: center;
    }
    .image-container img {
        border-radius: 15px; border: 2px solid #00f2ff;
        box-shadow: 0 0 15px #00f2ff55;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State for Navigation
if 'active' not in st.session_state: st.session_state.active = False

# ==================== HOME PAGE ====================
if not st.session_state.active:
    st.write("")
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h1 style='text-align: center; color: white; font-size: 60px;'>🧠 NEURAL MATTER</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00f2ff; letter-spacing: 5px;'>ADVANCED SEMANTIC ENGINE</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid #444;'>
                <p style='color: #8ab4f8; text-align: center;'>DEVELOPED BY</p>
                <div class='name-tag'>SUMA SREE • JHANSI TANUJA • NAVYA SRI</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("ACTIVATE NEURAL LINK 🚀", use_container_width=True):
            st.session_state.active = True
            st.rerun()

# ==================== SEARCH PAGE (Live Data + Images) ====================
else:
    st.sidebar.button("⬅️ Back to Terminal", on_click=lambda: st.session_state.update({"active": False}))
    
    query = st.text_input("", placeholder="Vethuku Mama... (Ex: iPhone 15, Black Hole, Elon Musk)")

    if query:
        with st.spinner('Accessing Global Data...'):
            try:
                with DDGS() as ddgs:
                    # 1. Get Text Results
                    text_results = list(ddgs.text(query, max_results=5))
                    # 2. Get Image Results
                    image_results = list(ddgs.images(query, max_results=3))
                
                if text_results:
                    # --- TOP SECTION: IMAGES ---
                    if image_results:
                        img_cols = st.columns(len(image_results))
                        for i, img in enumerate(image_results):
                            with img_cols[i]:
                                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                                st.image(img['image'], use_column_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)

                    # --- FEATURED SNIPPET ---
                    top = text_results[0]
                    st.markdown(f"""
                        <div class='featured-box'>
                            <div style='color: #00f2ff; font-size: 14px; font-weight: bold;'>AI KNOWLEDGE BASE</div>
                            <div style='color: white; font-size: 20px; margin-top: 15px;'>{top['body']}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    # --- REMAINING RESULTS ---
                    for r in text_results[1:]:
                        st.markdown(f"""
                            <div class="result-card">
                                <div style="color: #bdc1c6; font-size: 13px;">{r['href']}</div>
                                <a style="color: #ff00ea; font-size: 22px; text-decoration: none; font-weight: bold;" href="{r['href']}" target="_blank">{r['title']}</a>
                                <div style="color: #bdc1c6; margin-top: 8px;">{r['body']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Data not found in this sector, Dude.")
            except:
                st.error("Connection Interrupted! Try again.")