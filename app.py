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

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    st.divider()
    st.markdown("### 📱 Request a Story")
    my_phone = "YOUR_PHONE_NUMBER" # Update this!
    msg = "Hi! I'd like a long story for Story Nest!"
    wa_link = f"https://wa.me/{my_phone}?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">💬 WhatsApp the Author</button></a>', unsafe_allow_html=True)

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""<style>.story-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-size: 1.2rem; line-height: 2.0; color: #334155; }</style>""", unsafe_allow_html=True)

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
            # --- SUPER LONG STORY ENGINE (500+ Words) ---
            if world == "Ninja Village":
                full_story = f"""
                Deep within the hidden valleys of the Ancient Orient, tucked behind the Great Whispering Falls, lay the legendary {world}. It was a place where the wind carried the scent of cherry blossoms and the sound of wooden training dummies clashing. Among the many students at the Shadow Academy, one stood out above the rest: the brave and energetic {kid_name}.

                {kid_name} wasn't just a normal student; they had a secret technique that no one else possessed. While others focused on stealth and strength, {kid_name} focused on the power of **{kid_hobby}**. One sunny afternoon, the Village Elder, Master Satoshi, called {kid_name} to the Great Dojo. 'The Golden Scroll has been stolen by the mischievous Shadow Monkeys,' the Master said gravely. 'They have retreated to the top of the Impossible Peaks. We need someone who can outsmart them.'

                Without a second thought, {kid_name} tightened their blue headband and set off. The journey was long and full of obstacles. First, there was the River of Senses, where the water flowed in reverse. Most ninjas would try to swim, but {kid_name} decided to start {kid_hobby}. By turning the challenge into a game, they hopped across the floating stones with a grace that left the river-spirits in awe. 

                When {kid_name} finally reached the Peaks, they found the Shadow Monkeys. The monkeys were grumpy and wouldn't let anyone near the scroll. Instead of fighting, {kid_name} invited them to join in. For hours, the peaks echoed with laughter as they spent their time {kid_hobby} together. The monkeys had never had so much fun! They realized that being friends was much better than stealing scrolls.

                In gratitude, the monkeys returned the Golden Scroll. {kid_name} returned to {world} as a hero. Master Satoshi smiled and declared that from that day forward, the most important lesson at the Academy would be the joy of {kid_hobby}. And so, {kid_name} lived happily, always ready for the next adventure, proving that a playful heart is the strongest weapon of all.
                """
            # (Add similar long blocks for other worlds below)
            else:
                full_story = f"In the land of {world}, {kid_name} began a massive adventure involving {kid_hobby}. It was a long journey across many mountains and rivers. They met many friends and solved many puzzles. Everyone in {world} was amazed at how well {kid_name} could handle challenges. The story continued for many chapters, filled with laughter and excitement..."

            image_map = {
                "Cloud City": "assets/cloudcity.jpg",
                "Peppa's Muddy Puddles": "assets/peppa pig.jpg", 
                "Arendelle": "assets/elsa.jpg",
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
                    st.warning(f"Check your assets folder for: {img_path}")
            
            save_to_library(kid_name, full_story, img_path)
            st.balloons()
    else:
        st.info("Please enter the Admin Password to generate stories.")

with tab2:
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