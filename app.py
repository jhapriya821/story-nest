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

        if st.button("Generate & Save Story ✨"):
            # --- 500 WORD STORY LOGIC ---
            if world == "Cloud City":
                full_story = f"""High in the fluffy, pink-tinted clouds of {world}, {kid_name} discovered a secret path made of shimmering rainbows that only a true hero could see. Using their incredible talent for {kid_hobby}, they helped the sky-helpers fix the giant rainbow engine which had stopped spinning after a grumpy storm! Every citizen of Cloud City—from the balloon-birds to the giant star-whales—came out to watch as {kid_name} worked their magic. The engine began to hum a happy tune, and suddenly, the entire sky burst into the most beautiful colors anyone had ever seen."""
                
            elif world == "Peppa's Muddy Puddles":
                full_story = f"""It was a wonderfully rainy day at Peppa's house, and {kid_name} arrived wearing the shiniest golden boots anyone had ever seen! Peppa and George were so excited because they wanted to find the 'Mega Puddle' at the edge of the hill, but a fallen tree was blocking the way. {kid_name} didn't give up; they used their clever mind and their love for {kid_hobby} to turn the obstacle into a grand game that everyone could join. Mummy Pig and Daddy Pig cheered as {kid_name} led the way. They found a puddle so big it splashed the treetops!"""
            
            else:
                full_story = f"""In the magical world of {world}, {kid_name} set off on a grand adventure using their skills in {kid_hobby}. They traveled through deep forests and over high mountains, meeting new friends and spreading joy wherever they went. By the time the moon rose, {kid_name} had become the hero of the kingdom."""

            # --- IMAGE MAPPING ---
            image_map = {
                "Cloud City": "assets/cloudcity.jpg", 
                "Peppa's Muddy Puddles": "assets/peppa pig.jpg",
                "Arendelle": "assets/elsa & anna.jpg",
                "Pokemon Training": "assets/pokemon.jpg",
                "✨ Bedtime: Moon & Stars": "assets/cloudcity.jpg"
            }
            img_path = image_map.get(world, "assets/cloudcity.jpg")

            save_to_library(kid_name, full_story, img_path)
            st.balloons()
            st.success(f"Saved {kid_name} to Library!")
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
                if os.path.exists(path):
                    st.image(path)