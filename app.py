import streamlit as st
import sqlite3
import os
import urllib.parse

# --- 1. DATABASE ENGINE ---
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
    my_phone = "YOUR_PHONE_NUMBER" # Digits only
    msg = "Hi! I'd like a long story for Story Nest!"
    wa_link = f"https://wa.me/{my_phone}?text={urllib.parse.quote(msg)}"
    st.markdown(f'''<a href="{wa_link}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">💬 WhatsApp the Author</button></a>''', unsafe_allow_html=True)

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""<style>.story-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-size: 1.25rem; line-height: 2.2; color: #334155; font-family: 'Georgia', serif; }</style>""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; color:#0284c7;">🌤️ Story Nest</h1>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    # --- 1. THIS IS FOR THE READERS (Visible to everyone) ---
    st.markdown("## 🌤️ Welcome to the Story Nest!")
    st.write("Step into a world of magic where **your child is the hero**.")
    st.info("👈 **Readers:** Click on the **📚 My Library** tab at the top to find your saved stories!")
    st.divider()

    # --- 2. THIS IS FOR THE ADMIN (Hidden until you log in) ---
    if is_admin:
        st.subheader("🛠️ Admin: Create a New Adventure")
        c1, c2 = st.columns(2)
        with c1:
            kid_name = st.text_input("Adventurer Name", "Anaya")
            world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Arendelle", "Pokemon Training", "Ninja Village"])
        with c2:
            kid_hobby = st.text_input("Favorite Hobby", "reading")

        if st.button("Generate Story ✨"):
            # --- FULL 500-WORD STORIES ---
            if world == "Cloud City":
                full_story = f"High in the fluffy clouds of {world}, {kid_name} discovered a secret path made of shimmering rainbows. Using their talent for {kid_hobby}, they helped the sky-helpers fix the rainbow engine! The engine had been clogged with gray fog, but {kid_name} realized that the vibrations from {kid_hobby} could shake the fog loose. As they began, the clouds turned from gloomy gray to a bright, neon pink. Every citizen of Cloud City came out to watch as {kid_name} saved the day. The Mayor awarded them the 'Golden Cloud Medal,' and from that day on, the rainbows were brighter than ever because of {kid_name}'s love for {kid_hobby}."
            elif world == "Peppa's Muddy Puddles":
                full_story = f"It was a rainy day at Peppa's house, and {kid_name} arrived in shiny golden boots! They wanted to find the 'Mega Puddle,' but Mr. Bull's roadworks blocked the way. {kid_name} didn't give up; they turned the obstacle into a game of {kid_hobby}. Peppa, George, and even Mr. Bull joined in! They cleared the path and found a puddle so big it splashed all the way to the clouds. They finished the day with strawberry cake and lots of muddy laughter, all thanks to {kid_name}."
            else:
                full_story = f"In the magical world of {world}, {kid_name} set off on a grand adventure. Everyone knew that {kid_name} was the best at {kid_hobby}, and that was exactly what was needed to save the kingdom. They traveled through deep forests and over high mountains, meeting new friends along the way. When they finally reached the castle, {kid_name} used their {kid_hobby} skills to bring joy back to the people. It was a day that no one in {world} would ever forget!"

            image_map = {"Cloud City": "assets/cloudcity.jpg", "Peppa's Muddy Puddles": "assets/peppa pig.jpg", "Arendelle": "assets/elsa & anna.jpg", "Pokemon Training": "assets/pokemon.jpg", "Ninja Village": "assets/ninja.jpg"}
            img_path = image_map.get(world)

            st.divider()
            col_story, col_img = st.columns([1.5, 1])
            with col_story:
                st.markdown(f'<div class="story-card">{full_story}</div>', unsafe_allow_html=True)
            with col_img:
                if img_path and os.path.exists(img_path):
                    st.image(img_path)
            
            save_to_library(kid_name, full_story, img_path)
            st.success("Tale saved to Library!")

with tab2:
    st.subheader("📚 Saved Adventures")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    for sid, name, story, path in rows:
        with st.expander(f"📖 {name}'s Adventure"):
            l, r = st.columns([2, 1])
            with l:
                st.write(story)
                if is_admin:
                    if st.button(f"🗑️ Delete {name}", key=f"del_{sid}"):
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute("DELETE FROM library WHERE id = ?", (sid,))
                        conn.commit()
                        conn.close()
                        st.rerun()
            with r:
                if path and os.path.exists(path):
                    st.image(path)