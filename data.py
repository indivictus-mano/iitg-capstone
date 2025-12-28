import random

def get_thumbnail(topic, i):
    # Deterministic color/image based on topic for visual consistency
    colors = {
        'Tech': '00f2ff', 'Travel': 'ffaa00', 'Food': 'ff4500', 'Fitness': '00ff7f',
        'Gaming': '9932cc', 'Mindfulness': '87ceeb', 'Finance': '228b22',
        'Fashion': 'ff69b4', 'History': 'deb887', 'Science': '4169e1'
    }
    c = colors.get(topic, 'ffffff')
    return f"https://placehold.co/640x360/1a1a1a/{c}?text={topic}+{i}"

def generate_stats():
    return {
        'views': random.randint(1000, 5000000),
        'likes': random.randint(500, 200000),
        'dislikes': random.randint(10, 5000),
        'uploaded_time': f"{random.randint(1, 11)} months ago"
    }

# 10 Topics, 10 Items each
TOPICS = [
    # (Topic Name, Default Mood)
    ('Tech', 'happy'), 
    ('Travel', 'happy'),
    ('Food', 'happy'), 
    ('Fitness', 'angry'), # Intensity -> "Energy"
    ('Gaming', 'happy'),
    ('Mindfulness', 'stressed'), # Cure for stress
    ('Finance', 'stressed'), # Often stressful
    ('Fashion', 'happy'),
    ('History', 'lonely'), # Reflection
    ('Science', 'lonely') # Deep thought
]

# Override moods for variety
MOOD_MAP = {
    'Tech': ['happy', 'happy', 'angry', 'happy', 'happy', 'stressed', 'happy', 'happy', 'happy', 'happy'], # Angry = Rant
    'Travel': ['happy', 'happy', 'lonely', 'happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'lonely'], # Lonely = Solo travel
    'Food': ['happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'happy', 'stressed'], # Stressed = Comfort food
    'Fitness': ['angry', 'angry', 'happy', 'angry', 'angry', 'stressed', 'angry', 'angry', 'angry', 'angry'], # Stressed = Yoga
    'Gaming': ['happy', 'angry', 'happy', 'happy', 'lonely', 'happy', 'happy', 'angry', 'happy', 'happy'],
    'Mindfulness': ['stressed', 'stressed', 'stressed', 'stressed', 'sad', 'stressed', 'stressed', 'stressed', 'stressed', 'sad'],
    'Finance': ['stressed', 'stressed', 'angry', 'stressed', 'happy', 'stressed', 'stressed', 'stressed', 'stressed', 'angry'],
    'Fashion': ['happy', 'happy', 'happy', 'happy', 'lonely', 'happy', 'happy', 'happy', 'happy', 'happy'],
    'History': ['lonely', 'sad', 'angry', 'lonely', 'lonely', 'lonely', 'sad', 'angry', 'lonely', 'lonely'],
    'Science': ['lonely', 'happy', 'happy', 'lonely', 'lonely', 'lonely', 'angry', 'happy', 'lonely', 'lonely']
}

TITLES = {
    'Tech': [
        'The Truth About AI Sentience', 'iPhone 25 Pro Leaks', 'Coding in 2025', 'NVIDIA Stock Analysis',
        'Robots Taking Over?', 'Quantum Leaps', 'VR is Finally Good', 'Cybersecurity Nightmares', 'Tech Detox', 'SpaceX Launch Reaction'
    ],
    'Travel': [
        'Solo in Tokyo', 'Hidden Gems of Italy', 'Van Life Reality', 'Digital Nomad Guide', 
        'Most Dangerous Roads', 'Luxury vs Budget Paris', 'Packing Hacks', 'Island Hopping', 'Antarctica Trip', 'Cultural Shocks'
    ],
    'Food': [
        'Best Burger in NYC', 'Spicy Noodle Challenge', 'Vegan for 30 Days', 'Street Food Tour', 
        'Michelin Star Experience', 'Cooking with Grandma', 'Coffee Science', 'Chocolate History', 'Meal Prep Easy', 'Exotic Fruit Tasting'
    ],
    'Fitness': [
        '1000 Pushup Challenge', 'Yoga for Back Pain', 'Marathon Training', 'Gym Fails', 
        'Steroids Explained', 'Keto Diet Results', 'Meditation for Gym Rats', 'Home Workout', 'Crossfit Cult?', 'Sleep and Gains'
    ],
    'Gaming': [
        'GTA 6 Review', 'Minecraft Hardcore', 'E-Sports Drama', 'Retro Console Restoration', 
        'Why We Game', 'Speedrun World Record', 'VR Horror is Terrifying', 'Indie Game Spotlight', 'Console Wars', 'Top 10 RPGs'
    ],
    'Mindfulness': [
        'Rain Sounds 10H', 'Guided Meditation', 'Stoicism 101', 'Letting Go', 
        'Social Media Anxiety', 'Minimalist Living', 'Journaling Routine', 'Breathwork', 'Silence Retreat', 'Nature Healing'
    ],
    'Finance': [
        'Market Crash Coming?', 'Crypto Pumps', 'Passive Income Ideas', 'Real Estate Bubble', 
        'Retire at 30', 'Credit Card Hacks', 'Inflation Explained', 'Side Hustles', 'Warren Buffet Advice', 'Budgeting 101'
    ],
    'Fashion': [
        'Thrift Flip', 'Met Gala Review', 'Streetwear Trends', 'Capsule Wardrobe', 
        'Sneaker Collection', 'Fast Fashion Truth', 'Luxury Bag Unboxing', 'Color Theory', 'Style Evolution', 'Seasonal Essentials'
    ],
    'History': [
        'WW2 Untold Stories', 'Ancient Rome', 'Fall of Civilizations', 'Cold War Spies', 
        'Industrial Revolution', 'Medieval Life', 'Pyramid Global Mysteries', 'Titanic Facts', 'Samurai History', 'Viking Myths'
    ],
    'Science': [
        'Black Holes Explained', 'Aliens Exist?', 'Crispr Gene Editing', 'Ocean Depths', 
        'Mars Colonization', 'Physics Paradoxes', 'Evolution Evidence', 'Climate Solutions', 'Brain Mysteries', 'Time Travel Theory'
    ]
}

CONTENT_DATA = []

# Generate Content
count = 0
for topic, _ in TOPICS:
    moods = MOOD_MAP[topic]
    titles = TITLES[topic]
    for i in range(10):
        count += 1
        item_mood = moods[i]
        title = titles[i]
        
        # Simulated "AI Blog Content"
        content_body = f"""
        <p class="lead">In this article about <strong>{title}</strong>, we dive deep into the world of {topic}.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        <h3>Why this matters</h3>
        <p>The intersection of {topic} and modern life creates unique challenges and opportunities. especially when we consider the feeling of being <strong>{item_mood}</strong>.</p>
        <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
        <h3>Key Takeaways</h3>
        <ul>
            <li>Insight 1: {title} is changing everything.</li>
            <li>Insight 2: Understanding {topic} is crucial.</li>
            <li>Insight 3: The future looks valid.</li>
        </ul>
        <p>Thanks for reading! Don't forget to like and subscribe for more {topic} content.</p>
        """

        CONTENT_DATA.append({
            'id': f'vid_{count}',
            'title': title,
            'type': 'Blog', # User asked for Blogs, but UI is Video-like
            'genre': topic,
            'mood': item_mood,
            'thumbnail': get_thumbnail(topic, i+1),
            'description': f"An in-depth look at {title}. #{topic} #AI",
            'body': content_body,
            'author': f'{topic} Daily',
            'author_img': f'https://placehold.co/100x100/333/fff?text={topic[0]}',
            **generate_stats()
        })
