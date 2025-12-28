from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from data import CONTENT_DATA
import random

load_dotenv()

app = Flask(__name__)

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory storage (Prototype only)
HISTORY = []
FAVORITES = set() # Store dictionaries is hard with set logic in Python unless immutable, will store IDs
LAST_INTEREST = None # Track the last genre user interacted with

@app.context_processor
def inject_global_vars():
    # Pass current path to templates for valid active state
    return dict(request=request)

@app.route('/')
def index():
    global LAST_INTEREST
    topic = request.args.get('topic')
    
    current_feed_topic = None

    if topic:
        # User requested specific topic -> Show all 10 items of that topic on home page
        initial_feed = [i for i in CONTENT_DATA if i['genre'] == topic]
        current_feed_topic = topic
    
    elif LAST_INTEREST:
        # "homepage should show fully that topic when I return back"
        initial_feed = [i for i in CONTENT_DATA if i['genre'] == LAST_INTEREST]
        current_feed_topic = LAST_INTEREST

    else:
        # Default Home: Show 10 items. 
        # User said "feed 10 should be displayed". We can pick one from each topic to be diverse.
        # Group by genre
        grouped = {}
        for item in CONTENT_DATA:
            g = item['genre']
            if g not in grouped: grouped[g] = []
            grouped[g].append(item)
        
        # Pick 1 random from each of the 10 topics = 10 items
        initial_feed = []
        for g in grouped:
            if grouped[g]:
                initial_feed.append(random.choice(grouped[g]))
        
        # Fallback if less than 10 topics found (shouldn't happen with fixed data)
        if len(initial_feed) < 10:
            initial_feed = random.sample(CONTENT_DATA, 10)

    return render_template('index.html', initial_feed=initial_feed, current_topic=current_feed_topic)

@app.route('/trending')
def trending():
    # "Trending should hold each topic one blogs!"
    # Logic: For each topic, find the one with highest views.
    grouped = {}
    for item in CONTENT_DATA:
        g = item['genre']
        if g not in grouped: grouped[g] = []
        grouped[g].append(item)
    
    trending_feed = []
    for g in grouped:
        # Get max views for this topic
        top_item = max(grouped[g], key=lambda x: x['views'])
        trending_feed.append(top_item)
    
    # Sort these 10 leaders by overall views
    trending_feed.sort(key=lambda x: x['views'], reverse=True)

    return render_template('feed.html', title="Trending Now (Top per Topic)", content=trending_feed)

@app.route('/history')
def history_page():
    # History stored as list of IDs, we need to fetch object
    # Reverse to show recent first
    history_items = []
    for vid_id in reversed(HISTORY):
        item = next((i for i in CONTENT_DATA if i['id'] == vid_id), None)
        if item and item not in history_items: # Avoid duplicates in display
            history_items.append(item)
    return render_template('feed.html', title="Watch History", content=history_items)

@app.route('/favorites')
def favorites():
    fav_items = [i for i in CONTENT_DATA if i['id'] in FAVORITES]
    return render_template('feed.html', title="Your Favorites", content=fav_items)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        user_input = data.get('userInput')

        if not user_input:
            return jsonify({'error': 'Input required'}), 400

        # Call OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a mood classifier. Output only one word from: happy, sad, angry, stressed, lonely."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )

        mood = completion.choices[0].message.content.strip().lower()
        valid_moods = ['happy', 'sad', 'angry', 'stressed', 'lonely']
        if mood not in valid_moods:
            mood = 'happy'

        # Recommendation Engine Logic
        # 1. Filter by Mood
        recommendations = [item for item in CONTENT_DATA if item['mood'] == mood]
        
        # 2. Shuffle for variety
        random.shuffle(recommendations)

        return jsonify({
            'mood': mood,
            'recommendations': recommendations
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/watch/<id>')
def watch(id):
    global LAST_INTEREST
    item = next((i for i in CONTENT_DATA if i['id'] == id), None)
    if not item:
        return "Content not found", 404
    
    # Sticky Interest Update
    # "based on that topic! the homepage should show fully that topic when I return back"
    LAST_INTEREST = item['genre']
    
    # Add to History
    if id not in HISTORY:
        HISTORY.append(id)
    else:
        # Move to end if re-watched
        HISTORY.remove(id)
        HISTORY.append(id)

    # Related Content Logic:
    # 1. Same Genre (Topic)
    # 2. Same Mood (Vibe)
    related = [i for i in CONTENT_DATA if (i['genre'] == item['genre'] or i['mood'] == item['mood']) and i['id'] != id]
    random.shuffle(related)
    
    return render_template('watch.html', item=item, related_items=related[:10])

@app.route('/api/interact', methods=['POST'])
def interact():
    data = request.json
    action = data.get('action')
    item_id = data.get('id')
    
    if action == 'like':
        if item_id in FAVORITES:
            FAVORITES.remove(item_id)
            return jsonify({'status': 'unliked'})
        else:
            FAVORITES.add(item_id)
            return jsonify({'status': 'liked'})
            
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
