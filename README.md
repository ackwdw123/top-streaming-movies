# Top Streaming Movies (Auto‑Updated Daily)

A lightweight, LG‑TV‑friendly dashboard that displays the top trending streaming movies each day.  
This project automatically fetches data, generates a clean HTML page, and publishes it to GitHub Pages for easy viewing on any device — including LG Smart TVs.

---

## 🎬 Live Dashboard (LG TV Friendly)

You can access the live, auto‑updated page here:

**https://ackwdw123.github.io/top-streaming-movies/**

This URL can be bookmarked directly on an LG TV using the built‑in web browser.

---

## 🚀 What This Project Does

- Fetches the top trending movies from TMDB every day  
- Retrieves streaming provider information  
- Generates a TV‑optimized HTML dashboard  
- Publishes the updated page automatically  
- Makes the data available as JSON for other devices or dashboards  

Everything runs without manual intervention.

---

## 🧩 Technical Components

### **1. GitHub Actions (Automation Engine)**
- Runs the update workflow daily (or manually)
- Executes the Python script
- Commits updated files back to the repository
- Publishes the latest version to GitHub Pages

### **2. Python Update Script**
- Fetches trending movies from TMDB API  
- Retrieves streaming provider availability  
- Generates:
  - `index.html` (TV‑friendly dashboard)
  - `movies.json` (machine‑readable API output)

### **3. TMDB API**
- Provides trending movie data  
- Supplies provider availability (Netflix, Hulu, Disney+, etc.)  
- Requires a TMDB API key stored securely as a GitHub Actions secret

### **4. GitHub Pages (Hosting Layer)**
- Serves the dashboard at  
  **https://ackwdw123.github.io/top-streaming-movies/**
- Automatically updates whenever the workflow commits new files

### **5. Icons & Assets**
- Provider icons stored locally in `/icons`
- Used to visually indicate where each movie is available to stream

---

## 🛠 Repository Structure

top-streaming-movies/ 
│ 
├── index.html        # Auto‑generated dashboard 
├── movies.json       # Auto‑generated movie data 
├── update.py         # Python script that fetches & builds the page 
├── icons/            # Streaming provider icons 
├── .github/ 
└── workflows/
    └── update.yml  # GitHub Actions automation 
└── README.md

---

## 🔐 Secrets Required

Set the following GitHub Actions secret:

- **TMDB_API_KEY** — your TMDB API key for fetching trending movies and provider data

---

## 🧪 Running Locally (Optional)

If you want to test the script locally:

```bash
pip install requests
export TMDB_API_KEY="your_key_here"
python update.py


This will regenerate index.html and movies.json in the repo root.


