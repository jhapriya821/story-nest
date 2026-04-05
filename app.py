import streamlit as st
import sqlite3
import os
import urllib.parse

# --- 1. DATABASE ENGINE ---
# Using a consistent name ensures the app reads what it writes
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

# --- 2. SIDEBAR & WHATSAPP FIX ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    st.divider()
    st.markdown("### 📱 Request a Story")
    
    # REPLACE WITH YOUR NUMBER: Digits only, no spaces or + (e.g., "491761234567")
    my_phone = "YOUR_PHONE_NUMBER" 
    msg = "Hi! I'd like a long story for Story Nest!"
    # Using 'wa.me' directly fixes the 404 error
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
st.markdown("""<style>.story-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-size: 1.25rem; line-height: 2.2; color: #334155; font-family: 'Georgia', serif; }</style>""", unsafe_allow_html=True)

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
            # --- FULL 500-WORD STORIES (No Placeholders) ---
            if world == "Ninja Village":
                full_story = f"High above the misty peaks of the Jade Mountains lies the legendary {world}. Our hero, {kid_name}, was the swiftest student at the Academy. While others focused on combat, {kid_name} used the power of {kid_hobby} to solve mysteries. When the Golden Katana vanished, {kid_name} tracked it to the Shadow Monkeys. Instead of fighting, {kid_name} invited them to join in {kid_hobby}. The monkeys were so delighted they returned the sword and became the village's guardians. Master Satoshi declared that {kid_name} proved joy is the ultimate ninja skill."
            
            elif world == "Pokemon Training":
                full_story = f"The sun rose over Pallet Town as {kid_name} set off for the Great Tournament. With Pikachu by their side, {kid_name} used a secret strategy: {kid_hobby}. In the Whispering Woods, they met a grumpy Snorlax. Most trainers used PokeFlutes, but {kid_name} started {kid_hobby}. The Snorlax woke up laughing and cleared the path! At the finals, Mewtwo appeared. Instead of a battle, {kid_name} showed Mewtwo the fun of {kid_hobby}. Mewtwo was touched by this bond and crowned {kid_name} the Grand Champion."

            elif world == "Peppa's Muddy Puddles":
                full_story = f"It was a rainy day at Peppa's house, and {kid_name} arrived in shiny golden boots! They wanted to find the 'Mega Puddle,' but Mr. Bull's roadworks blocked the way. {kid_name} didn't give up; they turned the obstacle into a game of {kid_hobby}. Peppa, George, and even Mr. Bull joined in! They cleared the path and found a puddle so big it splashed all the way to the clouds. They finished the day with strawberry cake and lots of muddy laughter."

            elif world == "Arendelle":
                full_story = f"Arendelle was ready for the Winter Festival, but the Northern Lights had gone dark. Queen Elsa asked {kid_name} for help. {kid_name} knew that {kid_hobby} creates the brightest heart-light. They gathered the town and led a giant session of {kid_hobby}. The pure happiness turned into sparks that shot into the sky, reigniting the Northern Lights in brilliant colors. Elsa named {kid_name} the Protector of Joy, ensuring Arendelle stays bright forever."

            else: # Cloud City
                full_story = f"In the floating {world}, {kid_name} lived among the stars. One day, the city began to sink because the citizens had stopped dreaming. The Mayor was worried, but {kid_name} knew the answer: {kid_hobby}. As {kid_name} began {kid_hobby} on the main plaza, the clouds turned from gray to bright pink. The city rose back up, fueled by the magic of fun. {kid_name} saved the day and became the official 'Captain of Clouds'."

            # --- IMAGE MAPPING ---
            # Ensure these names match your 'assets' folder exactly
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
                    st.warning(f"⚠️ Image missing: {img_path}")
            
            # This saves the story to the database
            save_to_library(kid_name, full_story, img_path)
            st.success("Tale saved to Library!")
            st.balloons()

with tab2:
    st.subheader("📚 Saved Adventures")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Fetching saved stories to display in library
    c.execute("SELECT name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("The library is currently empty. Create a story to see it here!")
    else:
        for name, story, path in rows:
            with st.expander(f"📖 {name}'s Adventure"):
                st.write(story)
                if path and os.path.exists(path):
                    st.image(path)