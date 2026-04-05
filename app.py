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

def delete_story(story_id):
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("DELETE FROM library WHERE id = ?", (story_id,))
    conn.commit()
    conn.close()

init_db()

# --- 2. SIDEBAR & ACCESS CONTROL ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    if is_admin:
        st.success("Admin Mode: Active")
    else:
        st.info("Readers Mode: Active")
    
    st.divider()
    st.markdown("### 📱 Request a Story")
    st.write("Want your own adventure? Message the author!")
    
    # CHANGE THIS to your actual phone number (Example: 919876543210)
    my_phone = "YOUR_PHONE_NUMBER_HERE" 
    msg = "Hi! I'd like a story for Story Nest! My name is ____ and I love ____. Can you make one in the world of ____?"
    wa_link = f"https://wa.me/{my_phone}?text={urllib.parse.quote(msg)}"
    
    st.markdown(f'''
        <a href="{wa_link}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 12px; 
            border-radius: 10px; cursor: pointer; font-weight: bold; width: 100%;">
                💬 WhatsApp the Author
            </button>
        </a>
    ''', unsafe_allow_html=True)

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .story-card { 
        background: white; padding: 35px; border-radius: 20px; 
        border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        font-size: 1.25rem; line-height: 1.8; color: #334155;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; color:#0284c7;">🌤️ Story Nest</h1>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    if is_admin:
        c1, c2 = st.columns(2)
        with c1:
            kid_name = st.text_input("Adventurer Name", "Anaya")
            world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Arendelle", "Pokemon Training", "Ninja Village"])
        with c2:
            kid_hobby = st.text_input("Favorite Hobby", "reading")

        if st.button("Generate Story ✨"):
            # --- LONG STORY ENGINE ---
            intro = f"In the wondrous land of {world}, there lived a famous adventurer named {kid_name}. "
            
            if world == "Cloud City":
                mid = f"The clouds were heavy with silver rain. {kid_name} realized that by practicing {kid_hobby}, they could turn the raindrops into sparkling jewels that floated! Every time they laughed, the sky turned a brilliant shade of purple. "
                end = f"A giant wind-dragon saw the jewels and asked to join in. {kid_name} taught the dragon all about {kid_hobby}, and they flew together across the sky."
            elif world == "Peppa's Muddy Puddles":
                mid = f"Peppa Pig and {kid_name} discovered a puddle so vast it looked like a chocolate lake! They put on their golden boots and realized that {kid_hobby} was the secret to jumping higher than Daddy Pig ever could. "
                end = f"Suddenly, Daddy Pig lost his glasses in the deep mud. {kid_name} used their incredible {kid_hobby} skills to fish them out. Everyone cheered and jumped in one last puddle!"
            elif world == "Arendelle":
                mid = f"Elsa was worried her ice magic was too cold, but {kid_name} used the warmth of {kid_hobby} to turn the snow into glowing sparkles. "
                end = f"Anna and Olaf cheered! {kid_name} was named the 'Hero of Summer' for showing everyone that {kid_hobby} is the best magic of all."
            else:
                mid = f"In the world of {world}, {kid_name} discovered that every mystery could be solved with the power of {kid_hobby}. "
                end = f"It was the best adventure ever, and {kid_name} couldn't wait to return!"

            full_story = intro + mid + end
            
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
                st.success("Tale saved to Library!")
            with col_img:
                if img_path and os.path.exists(img_path):
                    st.image(img_path)
                else:
                    st.info(f"Visual for {world} will appear here.")
            
            save_to_library(kid_name, full_story, img_path)
            st.balloons()
    else:
        st.subheader("Welcome to the Nest!")
        st.write("Browse the library to read stories, or use the WhatsApp button in the sidebar to request your own!")

with tab2:
    st.subheader("Community Adventures")
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("SELECT id, name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    for sid, sname, stext, spath in rows:
        with st.expander(f"📖 {sname}'s Adventure"):
            l, r = st.columns([2, 1])
            with l:
                st.write(stext)
                if is_admin:
                    if st.button(f"🗑️ Delete #{sid}", key=f"del_{sid}"):
                        delete_story(sid)
                        st.rerun()
            with r:
                if spath and os.path.exists(spath):
                    st.image(spath)