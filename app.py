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

# --- 2. THE ADMIN LOCK ---
with st.sidebar:
    st.title("🔐 Access Control")
    pwd = st.text_input("Admin Password", type="password")
    is_admin = (pwd == "admin123") 

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .story-card { background: white; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center;">🌤️ Story Nest</h1>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["✨ Create Magic", "📚 My Library"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        kid_name = st.text_input("Adventurer Name", "Anaya")
        world = st.selectbox("World", ["Cloud City", "Peppa's Muddy Puddles", "Ninja Village", "Arendelle", "Pokemon Training"])
    with c2:
        kid_hobby = st.text_input("Favorite Hobby", "reading")

    if st.button("Generate Story ✨"):
        # The fix: Everything below this is indented 4 spaces!
        intro = f"Once upon a time, in the magical realm of {world}, lived a brave adventurer named {kid_name}. "
        
        if world == "Cloud City":
            mid = f"The clouds were unusually heavy today. {kid_name} realized that by using the power of {kid_hobby}, they could make the clouds dance! Every time they practiced, the sky turned a brilliant pink. "
            end = f"A giant wind-dragon appeared, but {kid_name} taught the dragon how to enjoy {kid_hobby} too. Now, they spend their days reading together among the stars."
        elif world == "Peppa's Muddy Puddles":
            mid = f"Peppa Pig and {kid_name} found the world's biggest muddy puddle! They decided that {kid_hobby} was the best way to stay balanced while jumping. George joined in with his dinosaur, making the biggest splash ever seen! "
            end = f"Daddy Pig lost his glasses in the deep mud, but {kid_name} used their {kid_hobby} skills to spot them. Everyone had a big laugh and finished the day with delicious strawberry cake."
        elif world == "Arendelle":
            mid = f"A freezing storm had locked the castle gates. Elsa asked {kid_name} for help. By combining ice magic with {kid_hobby}, they created a glowing, warm path through the blizzard. "
            end = f"Even Olaf joined in, realizing that {kid_hobby} is what brings people together. Summer returned to Arendelle, and it was the warmest celebration the kingdom had ever known."
        else:
            mid = f"It was a day of pure adventure where {kid_hobby} helped solve every mystery. "
            end = f"Finally, {kid_name} realized that as long as they had their favorite hobby, they could conquer any world."

        full_story = intro + mid + end
        
        image_map = {
            "Cloud City": "assets/cloudcity.jpg",
            "Peppa's Muddy Puddles": "assets/peppa.jpg",
            "Ninja Village": "assets/ninja.jpg",
            "Arendelle": "assets/frozen.jpg",
            "Pokemon Training": "assets/pokemon.jpg"
        }
        img = image_map.get(world)

        st.divider()
        col_a, col_b = st.columns([1.5, 1])
        with col_a:
            st.markdown(f'<div class="story-card">{full_story}</div>', unsafe_allow_html=True)
            st.success("Adventure saved to Library!")
        with col_b:
            if img and os.path.exists(img):
                st.image(img)
            else:
                st.info(f"Visual for {world}")
        
        save_to_library(kid_name, full_story, img)

with tab2:
    st.subheader("Saved Adventures")
    conn = sqlite3.connect('stories.db')
    c = conn.cursor()
    c.execute("SELECT id, name, story, image_path FROM library ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    for sid, sname, stext, spath in rows:
        with st.expander(f"📖 {sname}'s Adventure"):
            st.write(stext)
            if is_admin:
                if st.button(f"🗑️ Delete #{sid}", key=f"del_{sid}"):
                    delete_story(sid)
                    st.rerun()