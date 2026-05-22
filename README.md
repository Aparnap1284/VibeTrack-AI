# 🎵 VibeTrack AI

An AI-powered music recommendation system that suggests songs based on the vibe, emotion, and context of a user's video caption using NLP and semantic embeddings.

---

## 🚀 Features

* 🎙️ Caption-based music recommendations
* 🧠 NLP-powered semantic similarity using Sentence Transformers
* 🎭 Automatic mood detection from captions
* 🎼 Genre-based filtering
* 🌍 Language-based filtering
* 🎧 Instant Spotify & YouTube search links
* 🌈 Mood preview images
* 💜 Beautiful Streamlit UI with responsive design
* 🔀 Recommendation diversity logic

---

## 🧠 How It Works

VibeTrack AI uses:

* **Sentence Transformers (`all-MiniLM-L6-v2`)**
* **Semantic Embeddings**
* **Cosine Similarity**
* **Mood Detection Logic**
* **Metadata Filtering**

The system converts both:

* user captions
* song metadata

into semantic vector embeddings and recommends emotionally relevant tracks.

---

## 🛠️ Tech Stack

| Technology            | Purpose                 |
| --------------------- | ----------------------- |
| Python                | Core development        |
| Streamlit             | Frontend UI             |
| Sentence Transformers | Semantic NLP embeddings |
| Scikit-learn          | Similarity utilities    |
| Pandas                | Dataset handling        |
| PyTorch               | Transformer backend     |

---

## 📂 Project Structure

```text
VibeTrack-AI/
│
├── app/
│   ├── ui.py
│   └── styles.css
│
├── src/
│   └── recommend_music.py
│
├── dataset/
│   └── reels_dataset.csv
│
├── assets/
│   ├── romantic.jpg
│   ├── energetic.jpg
│   ├── peaceful.jpg
│   └── ...
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Aparnap1284/VibeTrack-AI.git
cd VibeTrack-AI
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

OR manually:

```bash
pip install streamlit pandas sentence-transformers scikit-learn torch
```

---

## 4️⃣ Run the App

```bash
streamlit run app/ui.py
```

---

# 🎯 Example Inputs

| Caption                   | Expected Mood |
| ------------------------- | ------------- |
| party songs               | Energetic     |
| beach sunset vibes        | Peaceful      |
| broken heart alone        | Sad           |
| gym beast mode            | Motivational  |
| romantic walk under stars | Romantic      |

---

# 🧠 Recommendation Pipeline

```text
User Caption
      ↓
Mood Detection
      ↓
Semantic Embedding Generation
      ↓
Cosine Similarity Matching
      ↓
Genre + Language Filtering
      ↓
Mood Score Boosting
      ↓
Top Song Recommendations
```

---

# ✨ Key AI Features

## 🔹 Semantic Search

Instead of keyword matching, the system understands contextual meaning.

Example:

```text
"night drive in rain"
```

matches emotionally similar songs even without exact words.

---

## 🔹 Mood Detection Engine

Captions are analyzed for emotional intent:

* Romantic
* Energetic
* Peaceful
* Motivational
* Sad
* Melancholic

---

## 🔹 Smart Prompt-Style Embeddings

Song metadata is converted into structured semantic prompts:

```text
Song: Perfect.
Singer: Ed Sheeran.
Mood: Romantic.
Genre: Ballad.
Language: English.
```

This improves embedding quality significantly.

---

## 🎵 Main Interface

* Caption input
* Genre selector
* Language selector
* AI recommendations
* Mood preview panel

---

# 🔮 Future Improvements

* Spotify API integration
* YouTube API integration
* Real audio feature analysis
* Collaborative filtering
* Playlist generation
* Emotion detection from images/videos
* Transformer fine-tuning
* User preference learning

---

# 👩‍💻 Author

## Aparna Patel

Pre-final Year CSE Student @ UEC
Backend Developer & AI Enthusiast

* Java
* Python
* NLP
* APIs
* Machine Learning

---

# 🔗 GitHub Repository

[VibeTrack AI GitHub Repository](https://github.com/Aparnap1284/VibeTrack-AI?utm_source=chatgpt.com)

---

# 💜 Acknowledgements

* Sentence Transformers
* Hugging Face
* Streamlit
* Scikit-learn
* PyTorch
* Edunet Foundation
* AICTE
* Microsoft AI Internship Initiative

---

# ⭐ If You Like This Project

Star the repository and connect on LinkedIn 🚀
