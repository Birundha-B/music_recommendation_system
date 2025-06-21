import streamlit as st
from recommend import df, recommend_songs

# Page settings
st.set_page_config(page_title="Music Recommender 🎵", page_icon="🎧", layout="centered")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        color: #ffdd59;
        text-shadow: 2px 2px 5px #00000099;
    }
    .stSelectbox>div>div>div>select {
        background-color: #3b3b98;
        color: #fff;
        font-weight: 600;
        padding: 0.4rem;
        border-radius: 8px;
    }
    div.stButton > button:first-child {
        background-color: #ff6b6b;
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        border: none;
        transition: background-color 0.3s ease;
        box-shadow: 0 5px 15px #ff6b6baa;
    }
    div.stButton > button:first-child:hover {
        background-color: #ee5253;
        box-shadow: 0 8px 20px #ee5253cc;
        cursor: pointer;
    }
    .stTable {
        background-color: #2f3640;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 0 15px #10ac84aa;
        color: #f5f6fa !important;
    }
    .stTable thead th {
        background-color: #57606f !important;
        color: #f5f6fa !important;
    }
    .stTable tbody tr:nth-child(even) {
        background-color: #353b48 !important;
    }
    .stTable tbody tr:hover {
        background-color: #40739e !important;
        color: #f5f6fa !important;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown('<h1 class="title">🎶 Instant Music Recommender</h1>', unsafe_allow_html=True)

# Dropdown
song_list = ["Choose an option"] + sorted(df['song'].dropna().unique())
selected_song = st.selectbox("🎵 Select a song:", song_list)

# Button & Recommendation Logic
if st.button("🚀 Recommend Similar Songs"):
    if selected_song is None or selected_song == "Choose an option" or selected_song.strip() == "":
        st.error("❌ Invalid input: Please select a song.")
    else:
        recommendations = recommend_songs(selected_song)
        st.markdown("### 🎉 Top similar songs:")
        st.table(recommendations)
