import streamlit as st
import sqlite3
import os

# --- 1. DATABASE ENGINE (REPAIRS SCHEMA) ---
def init_db():
    """Initializes the database and fixes missing columns automatically."""
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS library 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, story TEXT, image_path TEXT)''')
    
    # Check for 'image_path' to prevent OperationalError
    c.execute("PRAGMA table_info(library)")
    columns = [column[1] for column in c.fetchall()]
    if 'image_path' not in columns:
        c.execute("ALTER TABLE library ADD COLUMN image_path TEXT")
        conn.commit()
    conn.close()

def save_to_library(name, story, img_path):
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("INSERT INTO library (name, story, image_path) VALUES (?, ?, ?)", 
              (name, story, img_path))
    conn.commit()
    conn.close()

def delete_story(story_id):
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("DELETE FROM library WHERE id = ?", (story_id,))
    conn.commit()
    conn.close()

init_db()

# --- 2. THE ADMIN LOCK ---
with st.sidebar:
    st.title("🔐 Access Control")
    st.markdown("Only the Admin can delete stories from the library.")
    pwd = st.text_input("Admin Password", type="password")
    is_admin = (pwd == "admin123") 
    
    if is_admin:
        st.success("Admin Mode: Active")
    else:
        st.info("Readers Mode: Active")

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .story-card { 
        background: white; padding: 30px; border-radius: 15px; 
        border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        font-size: 1.2rem; line-height: 1.8;
    }
    .main-title { color: #0284c7; text-align: center; font-weight: 800; font-size: 3rem; }
    .stButton>button { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. MAIN APP INTERFACE ---
st.markdown('<h1 class="main-title">🌤️ Story Nest</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        kid_name = st.text_input("Adventurer Name", "Anaya")
        # --- FIXED DROPDOWN LIST ---
        world = st.selectbox("World", [
            "Cloud City", "Candy Forest", "Undersea Party", 
            "Ninja Village", "Pokemon Training", "Peppa's Muddy Puddles", 
            "Arendelle (Elsa & Anna)", "Rapunzel's Tower"
        ])
    with c2:
        kid_hobby = st.text_input("Favorite Hobby", "reading")
        st.write("Ready to create your story?")

    if st.button("Generate Story ✨"):
        # --- FIXED STORY LOGIC FOR ALL WORLDS ---
        if st.button("Generate Story ✨"):
        # --- LONG STORY ENGINE ---
        intro = f"Once upon a time, in the magical realm of {world}, lived a brave adventurer named {kid_name}. "
        
        if world == "Cloud City":
            middle = f"{kid_name} noticed the clouds turning grey! Using the power of {kid_hobby}, our hero bounced from marshmallow cloud to silver lining, gathering sunbeams in a golden jar. "
            climax = f"Suddenly, a giant wind-dragon appeared! But {kid_name} showed the dragon how to enjoy {kid_hobby}, and they became best friends, lighting up the sky forever."
        elif world == "Peppa's Muddy Puddles":
            middle = f"Peppa and {kid_name} found the biggest puddle in the world! They decided that {kid_hobby} was the only way to stay balanced while jumping. George joined in with his dinosaur, making a giant splash! "
            climax = f"Daddy Pig lost his glasses in the mud, but {kid_name} used their amazing {kid_hobby} skills to find them. Everyone had a big laugh and a snack of strawberry cake."
        elif world == "Ninja Village":
            middle = f"The Golden Scroll was missing! {kid_name} had to sneak past the sleeping panda guards using the secret technique of {kid_hobby}. It was the quietest move ever performed in the village. "
            climax = f"At the top of the mountain, the scroll was found. It turned out the Master was just using it to practice {kid_hobby}! {kid_name} was awarded a black belt for their bravery."
        elif world == "Arendelle (Elsa & Anna)":
            middle = f"A winter storm was freezing the castle doors shut. Elsa asked {kid_name} to help. By combining ice magic with {kid_hobby}, they created a beautiful glowing path through the snow. "
            climax = f"Olaf accidentally turned into a giant snowball, but {kid_name} saved him with a warm hug and more {kid_hobby}. Summer returned to Arendelle, warmer than ever before!"
        # Add similar long sections for Pokemon, Rapunzel, etc.
        else:
            middle = f"It was a day full of surprises where {kid_hobby} was the key to solving every mystery. "
            climax = f"Finally, {kid_name} realized that as long as they had their favorite hobby, every day was an adventure."

        story = intro + middle + climax + f" And so, {kid_name} returned home, waiting for the next trip to {world}."
        
        # --- FIXED IMAGE MAPPING ---
        image_map = {
            "Cloud City": "assets/cloudcity.jpg",
            "Candy Forest": "assets/candy.jpg",
            "Undersea Party": "assets/sea.jpg",
            "Ninja Village": "assets/ninja.jpg",
            "Pokemon Training": "assets/pokemon.jpg",
            "Peppa's Muddy Puddles": "assets/peppa.jpg",
            "Arendelle (Elsa & Anna)": "assets/frozen.jpg",
            "Rapunzel's Tower": "assets/rapunzel.jpg"
        }
        img = image_map.get(world)
        
        st.divider()
        col_a, col_b = st.columns([1.5, 1])
        with col_a:
            st.markdown(f'<div class="story-card">{story}</div>', unsafe_allow_html=True)
            st.success("Tale saved!")
        with col_b:
            if img and os.path.exists(img):
                st.image(img)
            else:
                st.info(f"Visual for {world}")
            
        save_to_library(kid_name, story, img)
        st.balloons()

with tab2:
    st.subheader("Saved Adventures")
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("SELECT id, name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        st.info("The library is currently empty.")

    for row in rows:
        sid, sname, stext, spath = row
        with st.expander(f"📖 {sname}'s Adventure"):
            left, right = st.columns([2, 1])
            with left:
                st.write(stext)
                if is_admin:
                    st.divider()
                    if st.button(f"🗑️ Delete Story #{sid}", key=f"del_{sid}"):
                        delete_story(sid)
                        st.rerun()
            with right:
                if spath and os.path.exists(spath):
                    st.image(spath)