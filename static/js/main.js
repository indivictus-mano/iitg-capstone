const moodInput = document.getElementById('mood-input');
const searchBtn = document.getElementById('search-btn');
const heroSection = document.getElementById('hero');
const resultsSection = document.getElementById('results-section');
const grid = document.getElementById('grid');
const loader = document.getElementById('loader');
const moodTitle = document.getElementById('mood-title');

function setInput(text) {
    moodInput.value = text;
    getRecommendations(text);
}

searchBtn.addEventListener('click', () => {
    const text = moodInput.value;
    if (text.trim()) getRecommendations(text);
});

moodInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const text = moodInput.value;
        if (text.trim()) getRecommendations(text);
    }
});

async function getRecommendations(userInput) {
    // UI State: Loading
    // Hide initial feed if present
    const initialFeed = document.getElementById('initial-feed');
    if (initialFeed) initialFeed.style.display = 'none';

    // Show Dynamic Header
    document.getElementById('dynamic-header').classList.remove('hidden');

    heroSection.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userInput })
        });

        const data = await response.json();

        if (data.error) throw new Error(data.error);

        renderResults(data.mood, data.recommendations);
    } catch (error) {
        console.error(error);
        alert('Failed to get recommendations. Please try again.');
        heroSection.classList.remove('hidden');
    } finally {
        loader.classList.add('hidden');
    }
}

function renderResults(mood, items) {
    moodTitle.innerHTML = `Vibe Detected: <span style="text-transform:capitalize; color: #3ea6ff">${mood}</span>`;
    grid.innerHTML = ''; // Clear previous

    if (items.length === 0) {
        grid.innerHTML = '<p style="text-align:center; col-span:3">No specific matches found, but here is some trending content...</p>';
        return;
    }

    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';

        let iconClass = 'fa-file-alt';
        if (item.type === 'Movie') iconClass = 'fa-film';
        if (item.type === 'Song') iconClass = 'fa-music';

        card.innerHTML = `
            <div class="thumbnail" onclick="window.location.href='/watch/${item.id}'">
                <img src="${item.thumbnail}" alt="${item.title}">
                <div class="duration" onclick="filterByTopic('${item.genre}')" style="cursor: pointer; z-index: 10;">${item.genre}</div>
            </div>
            <div class="card-content">
                <div class="card-icon"><i class="fas ${iconClass}"></i></div>
                <div class="card-text">
                    <div class="card-title" onclick="window.location.href='/watch/${item.id}'">${item.title}</div>
                    <div class="card-meta">
                        ${item.type} • ${formatViews(item.views)} views • ${item.uploaded_time}
                    </div>
                    <div class="card-actions">
                        <button class="action-btn" onclick="likeItem('${item.id}')"><i class="far fa-thumbs-up"></i></button>
                        <button class="action-btn"><i class="far fa-thumbs-down"></i></button>
                        <button class="action-btn"><i class="fas fa-share"></i></button>
                    </div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    resultsSection.classList.remove('hidden');
}

function formatViews(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num;
}

async function likeItem(id) {
    const btn = event.currentTarget; // Get button element
    const icon = btn.querySelector('i');

    // Optimistic UI
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        icon.style.color = '#3ea6ff';
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        icon.style.color = '';
    }

    try {
        await fetch('/api/interact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'like', id: id })
        });
    } catch (e) {
        console.error(e);
    }
}

// Theme Logic
const themeToggle = document.getElementById('theme-toggle');
const headerThemeToggle = document.getElementById('header-theme-toggle');

function toggleTheme() {
    if (document.body.classList.contains('light-theme')) {
        document.body.classList.remove('light-theme');
        localStorage.setItem('theme', 'dark');
        if (themeToggle) themeToggle.checked = true;
    } else {
        document.body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
        if (themeToggle) themeToggle.checked = false;
    }
}

// Init State
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'light') {
    document.body.classList.add('light-theme');
    if (themeToggle) themeToggle.checked = false;
} else {
    // Default dark
    if (themeToggle) themeToggle.checked = true;
}

if (themeToggle) {
    themeToggle.addEventListener('change', toggleTheme);
}
if (headerThemeToggle) {
    headerThemeToggle.addEventListener('click', toggleTheme);
}

// Global Filter Logic (Clicking Genre on card)
function filterByTopic(topic) {
    event.stopPropagation();
    window.location.href = `/?topic=${encodeURIComponent(topic)}`;
}
