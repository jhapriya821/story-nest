import streamlit as st
import sqlite3
import os
import urllib.parse

# --- 1. DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS library 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, story TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

def save_to_library(name, story, img_path):
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("INSERT INTO library (name, story, image_path) VALUES (?, ?, ?)", (name, story, img_path))
    conn.commit()
    conn.close()

init_db()

# --- 2. SIDEBAR & WHATSAPP FIX ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    st.divider()
    st.markdown("### 📱 Request a Story")
    
    # Put your number here (e.g., 49176...) No spaces, no +
    my_phone = "YOUR_PHONE_NUMBER_HERE" 
    
    msg = "Hi! I'd like a long story for Story Nest! My name is ____ and I love ____."
    # Updated to the direct wa.me link for better mobile/desktop opening
    wa_link = f"https://wa.me/{my_phone}?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''
        <a href="{wa_link}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 12px; 
            border-radius: 10px; cursor: pointer; font-weight: bold; width: 100%; font-size: 16px;">
                💬 WhatsApp the Author
            </button>
        </a>
    ''', unsafe_allow_html=True)

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""<style>.story-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-size: 1.2rem; line-height: 2.2; color: #334155; font-family: 'Georgia', serif; }</style>""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; color:#0284c7;">🌤️ Story Nest</h1>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    if is_admin:
        c1, c2 = st.columns(2)
        with c1:
            kid_name = st.text_input("Adventurer Name", "Ahaan")
            world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Arendelle", "Pokemon Training", "Ninja Village"])
        with c2:
            kid_hobby = st.text_input("Favorite Hobby", "playing")

        if st.button("Generate Story ✨"):
            # --- MEGA STORY ENGINE ---
            if world == "Ninja Village":
                full_story = f"High above the misty peaks of the Jade Mountains lies the legendary {world}. {kid_name} was the swiftest student at the Shadow Academy. While others practiced swordplay, {kid_name} used the power of {kid_hobby}... [This story will be 500 words long in your actual app]"
                # Note: Copy the long text blocks from my previous message here for each world!
            else:
                full_story = f"In the land of {world}, {kid_name} went on a journey that lasted for weeks. They used {kid_hobby} to solve every puzzle. [Imagine 500 words of adventure here!]"

            image_map = {
                "Cloud City": "assets/cloudcity.jpg",
                "Peppa's Muddy Puddles": "assets/peppa pig.jpg", 
                "Arendelle": "assets/elsa & anna.jpg",
                "Pokemon Training": "assets/pokemon.jpg",
                "Ninja Village": "assets/ninja.jpg"
            }
            img_path = image_map.get(world)

            st.divider()
            col_story, col_img = st.columns([1.5, 1])
            with col_story:
                st.markdown(f'<div class="story-card">{full_story}</div>', unsafe_allow_html=True)
            with col_img:
                if img_path and os.path.exists(img_path):
                    st.image(img_path)
                else:
                    st.warning("⚠️ Put images in 'assets' folder!")
            
            save_to_library(kid_name, full_story, img_path)
            st.balloons()