<div align="center">

# ✈️ AeroFeed

### A Clean, Premium RSS Reader

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**AeroFeed** is a modern, glassmorphism-styled RSS feed reader built with Flask. Browse news from your favorite sources — or paste any RSS/Atom URL — and enjoy a beautifully rendered, card-based article layout with real-time search and image extraction.

</div>

---

## 📖 About

AeroFeed fetches and parses RSS/Atom feeds server-side, extracts article thumbnails from multiple sources (media tags, enclosures, inline HTML), strips unsafe HTML, and serves clean article data through a REST API. The frontend renders everything with staggered animations, skeleton loading states, and a fully responsive dark-mode interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎨 **Premium Dark UI** | Glassmorphism design with gradient glows, neon accents, and smooth micro-animations |
| 📡 **Preset Feeds** | One-click access to TechCrunch, Hacker News, BBC News, and Reddit News |
| 🔗 **Custom RSS URL** | Paste any valid RSS or Atom feed URL to load articles instantly |
| 🔍 **Real-Time Search** | Client-side filtering by title, summary, or author — no page reload needed |
| 🖼️ **Smart Image Extraction** | Pulls thumbnails from `media:content`, enclosures, or inline `<img>` tags with graceful fallbacks |
| 🧹 **HTML Sanitization** | Strips `<script>`, `<style>`, `<iframe>`, and other unsafe tags from summaries |
| 💀 **Skeleton Loading** | Shimmer placeholders displayed while articles are being fetched |
| 📱 **Fully Responsive** | Sidebar collapses into a top nav on tablets; single-column layout on mobile |
| 🔄 **Refresh with Animation** | Spinning icon feedback on the refresh button during API calls |
| ✅ **Unit Tested** | Comprehensive test suite covering date formatting, image extraction, HTML sanitization, and API responses |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Flask
- **Feed Parsing:** feedparser
- **HTML Parsing:** BeautifulSoup4
- **HTTP Client:** Requests
- **Frontend:** Vanilla JavaScript, CSS3 (custom design system)
- **Fonts:** [Inter](https://fonts.google.com/specimen/Inter) & [Outfit](https://fonts.google.com/specimen/Outfit) (Google Fonts)
- **Icons:** [Lucide Icons](https://lucide.dev/)

---

## 📋 Requirements

- Python **3.10** or higher
- pip (Python package manager)

### Python Dependencies

```
Flask>=3.0.0
feedparser>=6.0.10
requests>=2.31.0
beautifulsoup4>=4.12.0
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/duongxauxi/aerofeed-project.git
cd aerofeed-project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Locally

```bash
python app.py
```

The development server starts at **http://127.0.0.1:5000**. Open it in your browser to start reading feeds!

### Running Tests

```bash
python -m unittest tests.py -v
```

---

## 📁 Folder Structure

```
aerofeed-project/
├── app.py                  # Flask application — routes, RSS parsing, API
├── tests.py                # Unit tests (unittest)
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
│
├── templates/
│   └── index.html          # Jinja2 template — main page layout
│
└── static/
    ├── css/
    │   └── style.css       # Complete design system & responsive styles
    └── js/
        └── app.js          # Frontend logic — feed loading, search, rendering
```

---

## 📸 Screenshots

> _Screenshots coming soon! Run the app locally to see the premium dark-mode interface in action._

<!--
Add screenshots here:
![AeroFeed Dashboard](screenshots/dashboard.png)
![Article Cards](screenshots/article-cards.png)
![Mobile View](screenshots/mobile-view.png)
-->

---

## 🗺️ Future Roadmap

- [ ] **Bookmark & Save Articles** — Persist favorite articles with local storage or a database
- [ ] **Dark / Light Theme Toggle** — User-selectable color themes
- [ ] **Feed Categories & Tags** — Organize preset feeds into topic groups
- [ ] **OPML Import/Export** — Import feed lists from other RSS readers
- [ ] **Infinite Scroll / Pagination** — Load more articles on demand
- [ ] **Read Later Queue** — Queue articles for offline reading
- [ ] **PWA Support** — Install AeroFeed as a Progressive Web App on desktop & mobile
- [ ] **Notification Alerts** — Optional browser notifications for new articles
- [ ] **Docker Deployment** — One-command deployment with Docker Compose
- [ ] **User Authentication** — Personal feed lists with login support

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by [Nguyen Tung Duong](https://github.com/duongxauxi)**

</div>
