import streamlit as st
import wikipedia
import os

# 1. Page Config & Professional Dark UI
st.set_page_config(page_title="Neural Matter AI", layout="wide")

st.markdown("""
    <style>
    .main { background: #000000 !important; }
    .featured-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 30px;
        border-left: 5px solid #00f2ff; margin-bottom: 30px;
    }
    .result-link {
        color: #8ab4f8; font-size: 22px; text-decoration: none; font-weight: bold;
    }
    .result-link:hover { text-decoration: underline; }
    .name-tag { color: #ccff00; font-size: 22px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if 'active' not in st.session_state: st.session_state.active = False

# ==================== HOME PAGE ====================
if not st.session_state.active:
    st.write("")
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h1 style='text-align: center; color: white;'>🧠 NEURAL MATTER AI</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid #444;'>
                <p style='color: #8ab4f8; text-align: center;'>PROJECT BY</p>
                <div class='name-tag'>SUMA SREE | JHANSI TANUJA | NAVYA SRI</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH SEARCH 🚀", use_container_width=True):
            st.session_state.active = True
            st.rerun()

# ==================== SEARCH PAGE (MATTER & LINKS) ====================
else:
    st.sidebar.button("⬅️ Home", on_click=lambda: st.session_state.update({"active": False}))
    
    query = st.text_input("", placeholder="Search anything (Ex: Black Hole, India, Python)...")

    if query:
        with st.spinner('Neural Link Establishing...'):
            try:
                wikipedia.set_lang("en")
                # Multiple results search
                search_list = wikipedia.search(query, results=6)
                
                if search_list:
                    # 1. MAIN MATTER (AI Overview)
                    main_page = wikipedia.page(search_list[0], auto_suggest=False)
                    st.markdown(f"""
                        <div class='featured-box'>
                            <div style='color: #00f2ff; font-size: 14px; font-weight: bold;'>AI OVERVIEW: {main_page.title}</div>
                            <div style='color: white; font-size: 19px; line-height: 1.8; margin-top: 15px;'>
                                {main_page.summary[:1200]}...
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # 2. MULTIPLE SEARCH LINKS
                    st.write("<p style='color:#bdc1c6; font-size: 18px;'>People also search for:</p>", unsafe_allow_html=True)
                    
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
                st.error("Connection error! Please try again in a moment.")