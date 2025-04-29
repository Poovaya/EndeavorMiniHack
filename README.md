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
cd pdf-uploader
npm install
```

This installs:

- @mui/material
- @mui/icons-material
- axios
- concurrently (for parallel dev startup)

---

## ▶️ Start the App


In two terminal tabs:

```bash
# Tab 1 (backend)
source venv/bin/activate
python app.py

# Tab 2 (frontend)
cd pdf-uploader
npm start
```

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
