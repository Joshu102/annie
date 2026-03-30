import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Page Config & UI Styling (Google Vibe)
st.set_page_config(page_title="Google AI Search", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #202124; }
    .result-card { padding: 15px; margin-bottom: 20px; border-radius: 8px; }
    .result-url { color: #bdc1c6; font-size: 14px; margin-bottom: 5px; }
    .result-title { color: #8ab4f8; font-size: 20px; text-decoration: none; font-weight: bold; }
    .result-title:hover { text-decoration: underline; }
    .result-snippet { color: #bdc1c6; font-size: 15px; line-height: 1.5; margin-top: 8px; }
    .ad-badge { color: #ffffff; background-color: #202124; border: 1px solid #bdc1c6; 
                padding: 2px 6px; border-radius: 3px; font-size: 12px; margin-right: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Load Model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# 3. Mega Database (Matter ekkuva + Ad links)
database = [
    {
        "title": "India - Wikipedia, the free encyclopedia",
        "url": "https://en.wikipedia.org/wiki/India",
        "content": "India, officially the Republic of India, is a country in South Asia. It is the seventh-largest country by area and the most populous country in the world. With a rich history spanning over 5,000 years, India is known for its diverse culture, heritage, and as the birthplace of four major religions.",
        "is_ad": False
    },
    {
        "title": "Ad: Best AI Course 2026 - Master Data Science",
        "url": "https://www.coursera.org/specializations/ai",
        "content": "Learn Artificial Intelligence from top industry experts. Get certified in Machine Learning, Deep Learning, and NLP. Enroll now for a 20% discount on professional certifications.",
        "is_ad": True
    },
    {
        "title": "Artificial Intelligence - IBM Topics",
        "url": "https://www.ibm.com/topics/artificial-intelligence",
        "content": "Artificial Intelligence leverages computers and machines to mimic the problem-solving and decision-making capabilities of the human mind. It includes sub-fields like Machine Learning and Deep Learning which use neural networks to process data.",
        "is_ad": False
    },
    {
        "title": "Python Programming Language - Official Site",
        "url": "https://www.python.org/",
        "content": "Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability. Python is used widely in automation, web development, and is the #1 language for AI research.",
        "is_ad": False
    },
    {
        "title": "History of the Indian Subcontinent",
        "url": "https://www.britannica.com/place/India",
        "content": "The history of India begins with the Indus Valley Civilization and the coming of the Aryans. It has seen the rise of great empires like the Maurya, Gupta, and Mughal, leading to the modern democratic republic we see today.",
        "is_ad": False
    }
]

# Pre-processing
texts = [d['content'] for d in database]
db_embeddings = model.encode(texts)

# 4. Search Interface
st.image("https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_92x30dp.png", width=150)
query = st.text_input("", placeholder="Search Google or type a URL", label_visibility="collapsed")

if query:
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, db_embeddings)[0]
    
    # Sorting by similarity
    sorted_indices = np.argsort(similarities)[::-1]
    
    st.write(f"<p style='color:#bdc1c6; font-size:14px;'>About {len(database)} results found</p>", unsafe_allow_html=True)
    
    found = False
    for i in sorted_indices:
        # High Accuracy Filter: Threshold > 0.25
        if similarities[i] > 0.25:
            found = True
            item = database[i]
            ad_tag = '<span class="ad-badge">Ad</span>' if item['is_ad'] else ''
            
            st.markdown(f"""
                <div class="result-card">
                    <div class="result-url">{item['url']}</div>
                    <a class="result-title" href="{item['url']}" target="_blank">{ad_tag}{item['title']}</a>
                    <div class="result-snippet">{item['content']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    if not found:
        st.error("No accurate results found, mama! Try another query.")