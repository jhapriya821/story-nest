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

# --- 2. SIDEBAR & AUTH ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    st.divider()
    st.markdown("### 📱 Contact Author")
    wa_link = "https://wa.me/YOUR_PHONE_NUMBER" # Replace with your digits
    st.markdown(f'''<a href="{wa_link}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 10px; width: 100%; cursor: pointer;">WhatsApp Me</button></a>''', unsafe_allow_html=True)

# --- 3. MAIN UI ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown('<h1 style="text-align:center; color:#0284c7;">🌤️ Story Nest</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    # PUBLIC SECTION (Visible to everyone)
    st.markdown("## 🌤️ Welcome to the Story Nest!")
    st.write("Step into a world of magic where **your child is the hero**.")
    
    with st.expander("✨ Request a Story for your Child"):
        g_name = st.text_input("Child's Name", key="g_n")
        g_love = st.text_input("What do they love?", key="g_l")
        if st.button("Send Request"):
            st.success(f"Got it! I'll create a story for {g_name} soon!")

    st.info("👈 **Readers:** Click the **📚 My Library** tab to see saved stories!")
    st.divider()

  # ADMIN SECTION (Only for you)
    if is_admin:
        st.subheader("🛠️ Admin: Create a New Adventure")
        c1, c2 = st.columns(2)
        with c1:
            kid_name = st.text_input("Adventurer Name", "Anaya")
            world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Arendelle", "Pokemon Training", "Ninja Village", "✨ Bedtime: Moon & Stars"])
        with c2:
            kid_hobby = st.text_input("Favorite Hobby", "reading")

        if st.button("Generate & Save Story ✨"):
            # 1. Create the text
            if world == "Cloud City":
                full_story = f"High in the clouds of {world}, {kid_name} used their {kid_hobby} skills to fix the rainbow engine and save the sky!"
            elif world == "Peppa's Muddy Puddles":
                full_story = f"It was a rainy day at Peppa's house, and {kid_name} arrived in shiny boots to play {kid_hobby} in the mud!"
            elif world == "✨ Bedtime: Moon & Stars":
                full_story = f"As the sun set, {kid_name} used {kid_hobby} to help the stars twinkle. Now, it's time for sleep. Goodnight, {kid_name}."
            else:
                full_story = f"In {world}, {kid_name} went on a grand {kid_hobby} adventure that no one will ever forget!"

            # 2. Pick the image (Matches your assets folder)
            image_map = {
                "Cloud City": "assets/cloudcity.jpg", 
                "Peppa's Muddy Puddles": "assets/peppa pig.jpg",
                "Arendelle": "assets/elsa & anna.jpg",
                "Pokemon Training": "assets/pokemon.jpg",
                "Ninja Village": "assets/ninja.jpg",
                "✨ Bedtime: Moon & Stars": "assets/cloudcity.jpg"
            }
            img_path = image_map.get(world, "assets/cloudcity.jpg")

            # 3. SAVE AND REFRESH
            save_to_library(kid_name, full_story, img_path)
            st.success(f"Success! {kid_name}'s story is now in the Library.")
            st.rerun()

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
                if path and os.path.exists(path):
                    st.image(path)