import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import warnings

# 1. Unwanted Logs & Warnings Pause
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings('ignore')

# 2. Page Config
st.set_page_config(page_title="Neural Matter AI", layout="wide")

# 3. Custom CSS for "Thop" UI
st.markdown("""
    <style>
    .main { background-color: #000000 !important; }
    /* Featured Snippet (Main Matter) */
    .featured-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 25px;
        border: 1px solid #333; margin-bottom: 30px;
        border-left: 5px solid #00f2ff;
    }
    .featured-title { color: #bdc1c6; font-size: 14px; margin-bottom: 10px; }
    .featured-content { color: white; font-size: 20px; line-height: 1.6; }
    
    /* Regular Result Links */
    .result-link { color: #8ab4f8; font-size: 20px; text-decoration: none; }
    .result-link:hover { text-decoration: underline; }
    .result-url { color: #bdc1c6; font-size: 14px; margin-bottom: 2px; }
    .result-text { color: #bdc1c6; font-size: 16px; margin-top: 5px; margin-bottom: 25px; }
    
    .batch-card {
        background: linear-gradient(135deg, #111, #222);
        padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #444;
    }
    .name-tag { color: #ccff00; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. Session State
if 'active' not in st.session_state: st.session_state.active = False

# ==================== HOME PAGE ====================
if not st.session_state.active:
    st.write("")
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h1 style='text-align: center; color: white;'>🧠 NEURAL MATTER ENGINE</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='batch-card'>
                <p style='color: #8ab4f8;'>DEVELOPED BY</p>
                <div class='name-tag'>SUMA SREE | JHANSI TANUJA | NAVYA SRI</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH ENGINE 🚀", use_container_width=True):
            st.session_state.active = True
            st.rerun()

# ==================== SEARCH PAGE (GOOGLE VIBE) ====================
else:
    st.sidebar.button("⬅️ Home", on_click=lambda: st.session_state.update({"active": False}))
    
    @st.cache_resource
    def load_model(): return SentenceTransformer('all-MiniLM-L6-v2')
    model = load_model()

    # Expand database for "India" & AI
    db = [
        {"t": "India - Wikipedia", "u": "https://en.wikipedia.org/wiki/India", "c": "India is the most populous country in the world and the seventh-largest country by area. It is a nuclear-weapon state and has the world's third-largest economy by PPP."},
        {"t": "Indian Economy & Tech", "u": "https://www.india.gov.in/", "c": "India is a global leader in information technology services and is home to the world's third-largest startup ecosystem."},
        {"t": "Artificial Intelligence Basics", "u": "https://www.ibm.com/topics/artificial-intelligence", "c": "Artificial intelligence leverages computers and machines to mimic the problem-solving and decision-making capabilities of the human mind."},
        {"t": "Neural Networks Explained", "u": "https://en.wikipedia.org/wiki/Neural_network", "c": "A neural network is a method in artificial intelligence that teaches computers to process data in a way that is inspired by the human brain."},
        {"t": "Python for Data Science", "u": "https://www.python.org/", "c": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with use of significant indentation."}
    ]

    query = st.text_input("", placeholder="Search something (Try: India)...")

    if query:
        q_vec = model.encode([query])
        d_vecs = model.encode([item['c'] for item in db])
        sims = cosine_similarity(q_vec, d_vecs)[0]
        sorted_indices = sims.argsort()[::-1]

        # --- FIRST RESULT AS FEATURED SNIPPET ---
        top_idx = sorted_indices[0]
        if sims[top_idx] > 0.3:
            st.markdown(f"""
                <div class='featured-box'>
                    <div class='featured-title'>AI Overview: {db[top_idx]['t']}</div>
                    <div class='featured-content'>{db[top_idx]['c']}</div>
                </div>
            """, unsafe_allow_html=True)

        # --- OTHER RESULTS AS LINKS ---
        st.write("<p style='color:#bdc1c6;'>People also search for:</p>", unsafe_allow_html=True)
        for i in sorted_indices:
            if sims[i] > 0.2:
                st.markdown(f"""
                    <div style="max-width: 700px;">
                        <div class="result-url">{db[i]['u']}</div>
                        <a class="result-link" href="{db[i]['u']}" target="_blank">{db[i]['t']}</a>
                        <div class="result-text">{db[i]['c']}</div>
                    </div>
                """, unsafe_allow_html=True)