# LYRCH DEV — Modern Python & GitHub Portfolio

A Bento-Grid developer portfolio built for **Lyrch Ong (Richard Ong)** — Web Designer & Technical Support Specialist with 18+ years of experience in system management, Python/Flask web development, and IT infrastructure.

---

## 🌟 Highlights

- **Obsidian Dark Bento UI**: Cyberpunk neon magenta (`#ff2a85`) aesthetic with glassmorphic cards, responsive grid layout, and interactive micro-animations.
- **Python & Flask Backend (`app.py`)**:
  - Live GitHub API caching and integration (`/api/github/repos`, `/api/github/profile`)
  - Dynamic JSON content management (`/api/content`)
  - Built-in contact inquiry processor (`/api/contact`)
- **GitHub Integration**:
  - Automatically fetches public GitHub repositories, stars, and language tags.
  - Can be hosted on **GitHub Pages** (`https://reianrd328.github.io/myprofile`) with zero hosting cost.
- **CMS Admin Dashboard (`/admin/`)**:
  - Edit bio, skills, services, projects, and contact info directly from the browser.
- **Static Site Generator (`build_static.py`)**:
  - Synchronizes dynamic changes to standalone `index.html` for instant GitHub deployment.

---

## 🛠️ Quick Start with Python

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Local Development Server
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🚀 Deploying to GitHub Pages

To deploy your portfolio statically to GitHub Pages:

1. Build the static `index.html`:
   ```bash
   python build_static.py
   ```
2. Commit and push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Update Bento UI portfolio and Python backend"
   git push origin main
   ```
3. Your site will automatically be live at:
   **https://reianrd328.github.io/myprofile/**

---

## 📁 Project Structure

```
├── app.py                 # Flask server with REST API & GitHub integration
├── build_static.py        # Static builder for GitHub Pages
├── requirements.txt       # Python dependencies (Flask, requests)
├── content.json           # Unified portfolio content database
├── index.html             # Standalone production site for GitHub Pages
├── templates/
│   └── index.html         # Jinja2 / Bento UI template
├── admin/                 # Cloud CMS admin dashboard
└── images/
    ├── theme/             # Bento UI cropped graphics & avatars
    └── portfolio/         # Project showcase screenshots
```

---

## 👤 Author
- **Lyrch Ong (Richard Ong)**
- GitHub: [@reianrd328](https://github.com/reianrd328)
- Email: `songzism@yahoo.com`