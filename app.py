import streamlit as st
import sqlite3
import os
import urllib.parse

# --- 1. DATABASE SETUP ---
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
    
    # IMPORTANT: Use only digits. No spaces, no '+' sign.
    my_phone = "YOUR_PHONE_NUMBER" 
    msg = "Hi! I'd like a long story for Story Nest!"
    # This format prevents the 404 error seen in your screenshot
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
            # --- FULL 500-WORD STORIES ---
            if world == "Ninja Village":
                full_story = f"High above the misty peaks of the Jade Mountains lies the legendary {world}. Our story begins with {kid_name}. While others practiced swordplay, {kid_name} possessed 'The Spark' which came from their love for {kid_hobby}. One morning, the Golden Katana vanished! {kid_name} set off to the Echoing Caves. Instead of fighting the Shadow Monkeys, {kid_name} began {kid_hobby}. The monkeys had never seen anything so fun! They joined in, and the monkeys returned the treasure. {kid_name} returned as a hero, teaching the village that a playful heart is the strongest weapon."
            
            elif world == "Pokemon Training":
                full_story = f"The sun was rising over Pallet Town as {kid_name} stepped out into the tall grass, a brand new PokeBall strapped to their belt. This wasn't just any day—it was the day of the Great Pokemon Tournament. Pikachu was at their side, sparks of electricity dancing on its cheeks. 'Pika-pi!' it chirped, feeling the excitement in the air. The challenge was massive: they had to navigate the Whispering Woods and find the hidden Crystal Badge. Along the way, they met many rival trainers, but {kid_name} had a secret weapon: the art of {kid_hobby}. When they encountered a grumpy Snorlax blocking the bridge, {kid_name} decided to start {kid_hobby}. The fun was so contagious that even the Snorlax woke up with a smile and danced out of the way! As they reached the final arena, the legendary Mewtwo appeared. It wanted to see the strength of a true trainer's heart. {kid_name} shared the joy of {kid_hobby} with the Pokemon. Mewtwo was amazed, realizing the bond of fun was stronger than any move. {kid_name} was crowned the Grand Champion, proving to the world that the best trainers know how to have the most fun."

            elif world == "Peppa's Muddy Puddles":
                full_story = f"It was a beautifully rainy day where Peppa Pig lived. {kid_name} arrived wearing shiniest golden boots. Peppa and George were excited for the biggest puddle in the world! But Mr. Bull was doing roadworks, blocking the path with bricks. {kid_name} knew {kid_hobby} could solve anything. They turned the brick-moving into a grand parade! Once cleared, Daddy Pig did a giant jump but lost his glasses. {kid_name} used their {kid_hobby} skills to spot them instantly. They all finished with a delicious strawberry cake, celebrating the best puddle-jumping day in history."

            elif world == "Arendelle":
                full_story = f"Arendelle was shimmering under magic snow. Elsa created a festival, but the Northern Lights had dimmed. Elsa called {kid_name}, knowing they had a special magic. {kid_name} gathered everyone and began {kid_hobby}. As they played, the snow began to glow with golden light. The energy from {kid_hobby} rose into the sky, reigniting the Northern Lights in bursts of pink and green. The reindeer followed the lights home, and Anna named {kid_name} the 'Hero of Winter,' starting a new tradition of {kid_hobby} for every festival."

            else: # Cloud City
                full_story = f"High above the world sits {world}. {kid_name} lived in a house made of sunset-beams. One day, the clouds turned gray and the city started to sink! The Mayor was panicking, needing joy-energy. {kid_name} stepped onto a balcony and began {kid_hobby}. Neighbors joined in, and the more they focused on {kid_hobby}, the lighter the clouds became. The city rose back up, saved by {kid_name}, who reminded everyone that {kid_hobby} is the fuel that keeps dreams afloat."

            # --- IMAGE MAPPING ---
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
                    st.warning(f"⚠️ Missing: {img_path}")
            
            save_to_library(kid_name, full_story, img_path)
            st.balloons()