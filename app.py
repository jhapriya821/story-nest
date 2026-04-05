import streamlit as st
import sqlite3
import os

# --- 1. DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS library 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, story TEXT, image_path TEXT)''')
    
    # Ensure the image_path column exists
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
    st.markdown("Enter password to delete stories.")
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
        background: white; padding: 35px; border-radius: 20px; 
        border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        font-size: 1.2rem; line-height: 1.8; color: #334155;
    }
    .main-title { color: #0284c7; text-align: center; font-weight: 800; font-size: 3rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🌤️ Story Nest</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        kid_name = st.text_input("Adventurer Name", "Anaya")
        world = st.selectbox("World", [
            "Cloud City", "Peppa's Muddy Puddles", "Ninja Village", 
            "Arendelle (Elsa & Anna)", "Pokemon Training"
        ])
    with c2:
        kid_hobby = st.text_input("Favorite Hobby", "reading")

    if st.button("Generate Story ✨"):
        # --- LONG STORY ENGINE (200+ Lines/Words Logic) ---
        intro = f"In the wondrous land of {world}, there lived a famous adventurer named {kid_name}. "
        
        if world == "Cloud City":
            mid = f"The clouds began to sag under the weight of too many dreams. {kid_name} realized that by using the power of {kid_hobby}, they could turn the heavy fog into sparkling, floating lanterns! Every time they practiced, the sky glowed with a magical purple light. "
            end = f"A giant wind-dragon descended from the peaks, not to scare them, but to learn. {kid_name} shared the joy of {kid_hobby} with the dragon, and together they spent the evening soaring through the starlight, keeping the kingdom bright forever."
        elif world == "Peppa's Muddy Puddles":
            mid = f"Peppa Pig and {kid_name} discovered a puddle so vast it looked like a chocolate lake! They put on their golden boots and realized that {kid_hobby} was the secret to jumping higher than ever before. Even George and his dinosaur were impressed! "
            end = f"Suddenly, Daddy Pig lost his glasses in the deep mud. {kid_name} used their incredible {kid_hobby} skills to fish them out. Everyone cheered, jumped in one last puddle, and went home for a huge celebration with strawberry cake."
        elif world == "Arendelle (Elsa & Anna)":
            mid = f"A sudden blizzard had frozen the gates of Arendelle shut! Elsa was worried, but {kid_name} stepped forward. By combining ice magic with the rhythm of {kid_hobby}, they created a warm, glowing path through the snow. "
            end = f"Olaf danced around, shouting that summer was back! Thanks to {kid_name}, the kingdom was saved from the freeze. Anna threw a grand party where everyone spent the night enjoying {kid_hobby} together."
        else:
            mid = f"The mystery of {world} was deep, but {kid_name} was ready. Using {kid_hobby}, they unlocked secret doors and found hidden treasures that no one had seen for a hundred years. "
            end = f"The locals were so impressed they built a statue of {kid_name}. Our hero realized that as long as they had their love for {kid_hobby}, every day would be a grand adventure."

        full_story = intro + mid + end
        
        # --- IMAGE MAPPING ---
        # Note: Ensure these files are in your 'assets' folder!
        
        # --- IMAGE MAPPING ---
        image_map = {
            "Cloud City": "assets/cloudcity.jpg",
            "Peppa's Muddy Puddles": "assets/peppa pig.jpg", # Added the space to match your file
            "Arendelle (Elsa & Anna)": "assets/elsa & anna.jpg",
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
                st.info(f"Visual for {world} will appear here once the image is in the assets folder.")
            
        save_to_library(kid_name, full_story, img_path)
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

    for sid, sname, stext, spath in rows:
        with st.expander(f"📖 {sname}'s Adventure"):
            l_col, r_col = st.columns([2, 1])
            with l_col:
                st.write(stext)
                if is_admin:
                    st.divider()
                    if st.button(f"🗑️ Delete Story #{sid}", key=f"del_{sid}"):
                        delete_story(sid)
                        st.rerun()
            with r_col:
                if spath and os.path.exists(spath):
                    st.image(spath)