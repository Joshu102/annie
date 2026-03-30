import streamlit as st
import wikipedia
import os

# 1. Page Config & Professional Dark UI
st.set_page_config(page_title="Neural Matter AI", layout="wide")

# Logo file name constant
LOGO_FILE = 'maxresdefault-removebg-preview (1).png'

st.markdown("""
    <style>
    .main { background: #000000 !important; }
    
    /* Logo Highlight Animation */
    .logo-highlight {
        filter: drop-shadow(0 0 15px #ff9900);
        transition: 0.3s;
    }
    .logo-highlight:hover { filter: drop-shadow(0 0 25px #ff9900); }

    .featured-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 30px;
        border-left: 5px solid #00f2ff; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.1);
    }
    .result-link {
        color: #8ab4f8; font-size: 22px; text-decoration: none; font-weight: bold;
    }
    .result-link:hover { text-decoration: underline; color: #00f2ff; }
    .name-tag { color: #ccff00; font-size: 22px; font-weight: bold; text-align: center; text-shadow: 0 0 10px #ccff00; }
    </style>
    """, unsafe_allow_html=True)

if 'active' not in st.session_state: st.session_state.active = False

# ==================== HOME PAGE ====================
if not st.session_state.active:
    st.write("")
    _, col, _ = st.columns([1, 2, 1])
    with col:
        # Custom Logo on Home
        try:
            st.image(LOGO_FILE, use_container_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #ff9900;'>RAMACHANDRA</h1>", unsafe_allow_html=True)
            
        st.markdown("<h1 style='text-align: center; color: white; letter-spacing: 2px;'>🧠 NEURAL MATTER AI</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid #444;'>
                <p style='color: #8ab4f8; text-align: center; font-weight: bold;'>PROJECT BY</p>
                <div class='name-tag'>SUMA SREE | JHANSI TANUJA | NAVYA SRI</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("LAUNCH SEARCH 🚀", use_container_width=True):
            st.session_state.active = True
            st.rerun()

# ==================== SEARCH PAGE (With Logo Highlight) ====================
else:
    # Top Header with Highlighted Logo and Title
    h_col1, h_col2 = st.columns([1, 4])
    with h_col1:
        try:
            st.image(LOGO_FILE, width=120) # Highlighted small logo
        except:
            st.markdown("<h2 style='color:#ff9900;'>RC</h2>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<h2 style='color:#00f2ff; margin-top: 20px;'>NEURAL SEARCH ENGINE</h2>", unsafe_allow_html=True)

    st.sidebar.button("⬅️ Back Home", on_click=lambda: st.session_state.update({"active": False}))
    
    query = st.text_input("", placeholder="Search anything (Ex: India, NASA, Python)...")

    if query:
        with st.spinner('Neural Link Establishing...'):
            try:
                wikipedia.set_lang("en")
                search_list = wikipedia.search(query, results=6)
                
                if search_list:
                    # 1. MAIN MATTER
                    main_page = wikipedia.page(search_list[0], auto_suggest=False)
                    st.markdown(f"""
                        <div class='featured-box'>
                            <div style='color: #00f2ff; font-size: 14px; font-weight: bold; letter-spacing: 1px;'>AI OVERVIEW: {main_page.title}</div>
                            <div style='color: white; font-size: 19px; line-height: 1.8; margin-top: 15px; text-align: justify;'>
                                {main_page.content[:2500]}...
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # 2. MULTIPLE SEARCH LINKS
                    st.write("<p style='color:#bdc1c6; font-size: 18px; font-weight: bold;'>Related Data Nodes Found:</p>", unsafe_allow_html=True)
                    
                    for title in search_list:
                        u = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                        st.markdown(f"""
                            <div style='margin-bottom: 20px; border-bottom: 1px solid #222; padding-bottom: 15px;'>
                                <a class="result-link" href="{u}" target="_blank">{title}</a>
                                <p style='color: #666; font-size: 14px; margin: 0;'>Source: {u}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Mama, information dorkatle. Vere topic search chey.")
            except:
                # Error Handling
                st.error("Connection error! Please try again in a moment.")