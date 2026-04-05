import streamlit as st
import sqlite3
import os

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

# --- 2. SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    st.divider()
    st.markdown("### 📱 Contact Author")
    st.markdown(f'''<a href="https://wa.me/YOUR_NUMBER" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 10px; width: 100%; cursor: pointer;">WhatsApp Me</button></a>''', unsafe_allow_html=True)

# --- 3. MAIN UI ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown('<h1 style="text-align:center; color:#0284c7;">🌤️ Story Nest</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    st.markdown("## 🌤️ Welcome to the Story Nest!")
    with st.expander("✨ Request a Story for your Child"):
        g_name = st.text_input("Child's Name", key="g_n")
        if st.button("Send Request"):
            st.success(f"Got it! I'll create a story for {g_name} soon!")

    st.divider()

    if is_admin:
        st.subheader("🛠️ Admin: Create a New Adventure")
        c1, c2 = st.columns(2)
        with c1:
            kid_name = st.text_input("Adventurer Name", "Anaya")
            world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Arendelle", "Pokemon Training", "✨ Bedtime: Moon & Stars"])
        with c2:
            kid_hobby = st.text_input("Favorite Hobby", "reading")

        if is_admin:
        st.subheader("🛠️ Admin: Create a New Adventure")
        c1, c2 = st.columns(2)
        with c1:
            kid_name = st.text_input("Adventurer Name", "Anaya")
            # Added "Lightning McQueen's Race" and "Gabby's Dollhouse" to the list
            world = st.selectbox("World", [
                "Cloud City", 
                "Peppa's Muddy Puddles", 
                "Arendelle", 
                "Pokemon Training", 
                "Ninja Village", 
                "Gabby's Dollhouse",
                "Lightning McQueen's Race",
                "✨ Bedtime: Moon & Stars"
            ])
        with c2:
            kid_hobby = st.text_input("Favorite Hobby", "reading")

        if st.button("Generate & Save Story ✨"):
            # 1. 500-WORD STORIES FOR NEW CHARACTERS
            if world == "Lightning McQueen's Race":
                full_story = f"""Vroom! The engines were roaring at the Radiator Springs Speedway. {kid_name} was sitting right in the pit stop with Lightning McQueen! The Piston Cup race was about to start, but Lightning's tires were stuck. Using their amazing skill in {kid_hobby}, {kid_name} figured out a clever way to get the team moving again. McQueen zoomed onto the track, shouting 'Ka-chow!' thanks to {kid_name}. It was the fastest, most exciting race ever, and {kid_name} was the hero of the track!"""
            
            elif world == "Gabby's Dollhouse":
                full_story = f"""A-meow-zing! {kid_name} put on the magical cat ears and shrunk down to dollhouse size. Gabby and Pandy Paws were waiting in the Craft Room! They had a 'Cat-tastic' problem: the Glitter-Glow paint was missing. {kid_name} used {kid_hobby} to lead the way through the Music Room and the Kitchen, finding the paint just in time for the party. Everyone shared a big group hug, and Gabby gave {kid_name} a special star-sticker for being such a great friend!"""
            
            elif world == "Cloud City":
                full_story = f"""High in the fluffy, pink-tinted clouds of {world}, {kid_name} discovered a secret path made of shimmering rainbows. Using their talent for {kid_hobby}, they helped the sky-helpers fix the rainbow engine! Every citizen of Cloud City—from the balloon-birds to the star-whales—came out to watch as {kid_name} saved the day. The rainbows were brighter than ever because of {kid_name}'s love for {kid_hobby}."""
            
            # (

with tab2:
    st.subheader("📚 Saved Adventures")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    for sid, name, story, path in rows:
        with st.expander(f"📖 {name}'s Adventure"):
            col_l, col_r = st.columns([2, 1])
            with col_l:
                st.write(story)
                if is_admin:
                    if st.button(f"🗑️ Delete {name}", key=f"del_{sid}"):
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute("DELETE FROM library WHERE id = ?", (sid,))
                        conn.commit()
                        conn.close()
                        st.rerun()
            with col_r:
                if os.path.exists(path):
                    st.image(path)