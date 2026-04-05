import streamlit as st
import sqlite3
import os
import urllib.parse

# --- 1. DATABASE SETUP ---
# We use 'stories.db' consistently for both saving and reading
DB_FILE = 'stories.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS library 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, story TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

def save_to_library(name, story, img_path):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO library (name, story, image_path) VALUES (?, ?, ?)", (name, story, img_path))
    conn.commit()
    conn.close()

init_db()

# --- 2. SIDEBAR & WHATSAPP ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    st.divider()
    st.markdown("### 📱 Request a Story")
    
    # Use your number here (Example: 49176...) No spaces or + signs
    my_phone = "YOUR_PHONE_NUMBER" 
    msg = "Hi! I'd like a long story for Story Nest!"
    # Direct wa.me link fixes the 404 issue
    wa_link = f"https://wa.me/{my_phone}?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''<a href="{wa_link}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">💬 WhatsApp the Author</button></a>''', unsafe_allow_html=True)

# --- 3. UI & STORY ENGINE ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""<style>.story-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-size: 1.2rem; line-height: 2.0; color: #334155; font-family: 'Georgia', serif; }</style>""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    if is_admin:
        kid_name = st.text_input("Adventurer Name", "Ahaan")
        world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Arendelle", "Pokemon Training", "Ninja Village"])
        hobby = st.text_input("Favorite Hobby", "playing")

        if st.button("Generate Story ✨"):
            # Detailed Story Content
            if world == "Ninja Village":
                full_story = f"In the hidden {world}, {kid_name} was a master of {hobby}. One day, a mystery arose that required a long journey through the Jade Mountains... [Insert full 500-word text here]"
            else:
                full_story = f"Deep in {world}, {kid_name} used the power of {hobby} to save the day. It was a long and legendary adventure filled with magic... [Insert full 500-word text here]"
            
            image_map = {"Cloud City": "assets/cloudcity.jpg", "Peppa's Muddy Puddles": "assets/peppa pig.jpg", "Arendelle": "assets/elsa & anna.jpg", "Pokemon Training": "assets/pokemon.jpg", "Ninja Village": "assets/ninja.jpg"}
            img_path = image_map.get(world)

            st.markdown(f'<div class="story-card">{full_story}</div>', unsafe_allow_html=True)
            save_to_library(kid_name, full_story, img_path)
            st.success("Tale saved to Library!")
            st.balloons()

with tab2:
    st.subheader("Saved Adventures")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("The library is empty. Generate a story in the first tab to see it here!")
    else:
        for name, story, path in rows:
            with st.expander(f"📖 {name}'s Tale"):
                st.write(story)
                if path and os.path.exists(path):
                    st.image(path)