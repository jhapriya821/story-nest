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

init_db()

# --- 2. SIDEBAR & WHATSAPP ---
with st.sidebar:
    st.title("🔐 Admin Portal")
    pwd = st.text_input("Enter Password", type="password")
    is_admin = (pwd == "admin123") 
    
    st.divider()
    st.markdown("### 📱 Request a Story")
    my_phone = "YOUR_PHONE_NUMBER" # Update this with your digits!
    msg = "Hi! I'd like a long story for Story Nest!"
    wa_link = f"https://api.whatsapp.com/send?phone={my_phone}&text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">💬 WhatsApp the Author</button></a>', unsafe_allow_html=True)

# --- 3. UI STYLING ---
st.set_page_config(page_title="Story Nest", layout="wide")
st.markdown("""<style>.story-card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-size: 1.2rem; line-height: 2.0; color: #334155; font-family: 'Georgia', serif; }</style>""", unsafe_allow_html=True)

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
            # --- MEGA STORY ENGINE (200-500 WORDS PER WORLD) ---
            if world == "Ninja Village":
                full_story = f"""High above the misty peaks of the Jade Mountains lies the legendary {world}, where the very air thrums with ancient energy. Our story begins with the swiftest student at the Shadow Academy, a young hero named {kid_name}. While other ninjas practiced their stealth and swordplay, {kid_name} possessed a unique gift that Master Satoshi called 'The Spark.' This spark came from {kid_name}'s absolute love for **{kid_hobby}**. One crisp morning, the Great Bell chimed—a sound that only rang in times of great mystery. The Golden Katana, the village's source of light, had vanished! Master Satoshi looked at {kid_name} and said, 'The Shadow Monkeys have taken it to the Echoing Caves. They are too fast for our guards, but they cannot resist a challenge of the heart.' {kid_name} set off immediately, leaping from cherry blossom tree to bamboo forest. Upon reaching the Echoing Caves, the Shadow Monkeys appeared, chattering and ready to cause mischief. Instead of drawing a weapon, {kid_name} simply sat down and began {kid_hobby}. The monkeys stopped. They had never seen anything so fascinating! Slowly, one by one, the monkeys joined in. The caves, which were once dark and scary, filled with the sounds of laughter and joy. The Shadow Monkeys were so happy to have a friend to spend time {kid_hobby} with that they willingly handed over the Golden Katana. {kid_name} returned to {world} not just with the treasure, but with an army of monkey friends! Master Satoshi beamed with pride, declaring that {kid_name} had taught the whole village that the true power of a ninja isn't in hiding, but in the joy of shared adventure."""
            
            elif world == "Peppa's Muddy Puddles":
                full_story = f"""It was a beautifully rainy day in the rolling green hills where Peppa Pig lived. The sky was filled with fluffy gray clouds, which meant only one thing: Muddy Puddles! {kid_name} had just arrived for a visit, wearing the shiniest golden boots ever seen. Peppa and George were already outside, breathless with excitement. 'Hurry up, {kid_name}!' Peppa giggled. 'The biggest puddle in the world is just behind the hill!' But as they reached the giant puddle, they found a problem. Mr. Bull was doing roadworks, and a large pile of bricks was blocking the way to the puddle. 'Oh dear,' said Mummy Pig. 'I don't think we can jump today.' But {kid_name} had a better idea. They knew that **{kid_hobby}** was the secret to solving any problem. Using their skills in {kid_hobby}, {kid_name} organized a brilliant game that involved everyone. They turned the brick-moving into a grand parade, and before they knew it, the path was clear! Daddy Pig was so impressed he tried to do a giant jump, but he landed with a huge 'SPLASH' and lost his glasses in the mud. {kid_name} used their {kid_hobby} eyes to spot them instantly. The afternoon was spent jumping, laughing, and learning that {kid_hobby} makes every rainy day feel like a sunny one. They all finished with a delicious strawberry cake, celebrating the best puddle-jumping day in history."""

            elif world == "Pokemon Training":
                full_story = f"""The sun was rising over Pallet Town as {kid_name} stepped out into the tall grass, a brand new PokeBall strapped to their belt. This wasn't just any day—it was the day of the Great Pokemon Tournament. Pikachu was at their side, sparks of electricity dancing on its cheeks. 'Pika-pi!' it chirped, feeling the excitement in the air. The challenge was massive: they had to navigate the Whispering Woods and find the hidden Crystal Badge. Along the way, they met many rival trainers, but {kid_name} had a secret weapon that wasn't a move like Thunderbolt or Flamethrower. Their secret was the art of **{kid_hobby}**. When they encountered a grumpy Snorlax blocking the bridge, other trainers tried to wake it with loud music. But {kid_name} decided to start {kid_hobby}. The gentle rhythm and fun of {kid_hobby} were so contagious that even the Snorlax woke up with a smile and danced out of the way! As they reached the final arena, the legendary Mewtwo appeared. It wanted to see the strength of a true trainer's heart. {kid_name} didn't fight; they shared the joy of {kid_hobby} with the Pokemon. Mewtwo was amazed. It realized that training wasn't just about battling, but about the bond created through {kid_hobby}. {kid_name} was crowned the Grand Champion, proving to the whole world that the best trainers are the ones who know how to have the most fun."""

            elif world == "Arendelle":
                full_story = f"""The kingdom of Arendelle was shimmering under a blanket of fresh, magical snow. Queen Elsa had created a magnificent winter festival, but something was missing. The Northern Lights, which usually guided the reindeer home, had dimmed. Anna, Olaf, and Kristoff were worried, but Elsa knew exactly who to call: the legendary adventurer {kid_name}. When {kid_name} arrived, the gates of the castle flew open. 'We need a special kind of magic,' Elsa explained. 'A magic that comes from the heart.' {kid_name} knew exactly what to do. They gathered everyone in the town square and began **{kid_hobby}**. As {kid_name} showed them the wonder of {kid_hobby}, the snow beneath their feet began to glow with a warm, golden light. Olaf started dancing, his carrot nose twitching with delight. The energy from their {kid_hobby} rose higher and higher into the sky, touching the clouds and reigniting the Northern Lights in a burst of pink, green, and blue. The reindeer followed the lights back home just in time for the grand feast. Anna hugged {kid_name}, thanking them for saving the festival. From that night on, a new tradition was born in Arendelle: every winter, the citizens would gather to celebrate {kid_hobby}, reminding everyone that even the coldest winter can be warmed by a playful spirit."""

            else: # Cloud City
                full_story = f"""High above the world, where the air is as sweet as cotton candy, sits the floating majestic {world}. {kid_name} lived in a house made of solid sunset-beams. The city was famous for its flying whales and singing birds, but one day, the clouds began to turn a heavy, dull gray. The city started to sink! The Great Balloon that held the city up was losing its lift. {kid_name} raced to the control tower where the Mayor was panicking. 'We need more joy-energy!' he cried. {kid_name} stepped onto the highest balcony. They realized that the citizens had forgotten how to have fun. So, {kid_name} began **{kid_hobby}** with all their might. Slowly, the neighbors looked out their windows and joined in. The more they focused on {kid_hobby}, the lighter the clouds became. The gray turned into bright white, then a soft pink. The city rose back up, higher than ever before. {kid_name} had saved {world} by reminding everyone that **{kid_hobby}** is the fuel that keeps dreams afloat. The story of their bravery was written in the stars for all to see."""

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
                    st.warning(f"Image not found at: {img_path}")
            
            save_to_library(kid_name, full_story, img_path)
            st.balloons()