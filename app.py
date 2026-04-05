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

# --- 2. THE ADMIN LOCK (THIS HIDES THE BUTTONS) ---
with st.sidebar:
    st.title("🔐 Access Control")
    st.markdown("Only the Admin can delete stories from the library.")
    
    # The 'is_admin' variable starts as False
    # Change 'admin123' to your preferred secret password
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
        world = st.selectbox("World", ["Cloud City", "Candy Forest", "Undersea Party"])
    with c2:
        kid_hobby = st.text_input("Favorite Hobby", "reading")
        st.write("Ready to create your story?")

    if st.button("Generate Story ✨"):
        # Triple quotes prevent "unterminated string" syntax errors
        if world == "Cloud City":
            story = f"""In the fluffy {world}, a hero named {kid_name} used {kid_hobby} 
            to light up the sky and save the floating kingdom!"""
        elif world == "Candy Forest":
            story = f"""In the sweet {world}, {kid_name} found a chocolate path. 
            By {kid_hobby}, they guided the gummy bears back to their village!"""
        else:
            story = f"""In the deep {world}, {kid_name} threw a dance party. 
            The fish joined in because they loved {kid_hobby}!"""
        
        image_map = {
            "Cloud City": "assets/cloudcity.jpg",
            "Candy Forest": "assets/candy.jpg",
            "Undersea Party": "assets/sea.jpg"
        }
        img = image_map.get(world)
        
        st.divider()
        col_a, col_b = st.columns([1.5, 1])
        with col_a:
            st.markdown(f'<div class="story-card">{story}</div>', unsafe_allow_html=True)
            st.success("Tale saved!")
        with col_b:
            if os.path.exists(img):
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
                
                # --- CRITICAL: THE HIDE LOGIC ---
                # This button ONLY renders if 'is_admin' is True
                if is_admin:
                    st.divider()
                    if st.button(f"🗑️ Delete Story #{sid}", key=f"del_{sid}"):
                        delete_story(sid)
                        st.rerun()
                # If is_admin is False, the code above is skipped entirely.
                
            with right:
                if spath and os.path.exists(spath):
                    st.image(spath)