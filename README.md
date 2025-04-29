# PDF Matcher

A full-stack application that extracts line items from uploaded PDFs, fetches the best matching item names, and allows editing, saving, and exporting results. Built with Flask, React, MongoDB, and Material UI.

---

## 🚀 Features

- PDF upload and extraction via external API
- Batch and per-line matching via external API (proxied through Flask)
- Inline editing with live match lookup
- Selections stored persistently in MongoDB
- Export selected items as CSV
- React frontend + Flask backend (runs in parallel)

---

## 🛠 Prerequisites

| Tool         | Version (or newer) | Install                         |
|--------------|--------------------|----------------------------------|
| Python       | 3.8+               | [python.org](https://python.org) |
| Node.js / npm| Node 16+, npm 8+   | [nodejs.org](https://nodejs.org) |
| MongoDB      | Running locally    | [mongodb.com](https://mongodb.com) |

---

## 📦 Project Structure

```
project-root/
├── backend/         # Flask app.py
├── frontend/        # React App (src/, package.json)
└── start.sh         # Launch helper
```

---

## 🔧 Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # Windows: .\venv\Scripts\Activate
pip install --upgrade pip

# install dependencies
echo "
flask
flask-cors
pymongo
requests
" > requirements.txt

pip install -r requirements.txt
```

---

## 💻 Frontend Setup

```bash
cd ../frontend
npm install
```

This installs:

- @mui/material
- @mui/icons-material
- axios
- concurrently (for parallel dev startup)

---

## ▶️ Start the App

### Option 1: Run backend and frontend separately

In two terminal tabs:

```bash
# Tab 1 (backend)
cd backend
source venv/bin/activate
python app.py

# Tab 2 (frontend)
cd frontend
npm start
```

---

### Option 2: Use the startup script

Create start.sh in the root:

```bash
#!/usr/bin/env bash
set -e

# backend setup
cd backend
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt

# frontend setup
cd ../frontend
npm install

# start both
npm run dev
```

Make it executable:

```bash
chmod +x start.sh
./start.sh
```

---

## 🔁 NPM Scripts (in frontend/package.json)

```json
"scripts": {
  "client": "react-scripts start",
  "server": "cd ../backend && source ../backend/venv/bin/activate && python app.py",
  "dev": "concurrently -k \"npm run client\" \"npm run server\""
}
```

> On Windows: change `source ...` to `call ../backend/venv/Scripts/activate`

---

## ✅ Test Checklist

- [ ] Upload PDF and extract items
- [ ] View batch match suggestions
- [ ] Edit any line item and search
- [ ] Save selection
- [ ] Export selected to CSV

---

## 🧠 Tips

- MongoDB must be running (`localhost:27017`)
- All match calls go through Flask (never direct from frontend)
- You can update selections anytime by editing a row
- Uses Material UI + Autocomplete for smooth UX

---

## 🧹 Clean Up

To clear all saved matches:

```bash
curl -X POST http://localhost:5000/delete-all
```

---

## 📄 License

MIT — use freely, attribution appreciated
