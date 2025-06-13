# 🎧 **VibeTrack AI**

**An AI-powered music recommender that matches your video's vibe with the perfect soundtrack.**

<p align="center">
  <img src="assets/energetic.jpg" width="300" alt="VibeTrack AI Mood Preview">
</p>

---

## 🔮 **Key Features**

* 🎙️ **Mood Detection** from your video description using NLP
* 🎶 **Music Recommendations** based on mood and selected genre
* 🎧 **Streaming Support** with direct links to Spotify & YouTube
* 💜 **Elegant UI** with a calming purple-themed design
* 🌐 Built using **Streamlit**, ideal for fast web app deployment

---

## ⚙️ **Run Locally**

To run the project on your machine:

```bash
git clone https://github.com/Aparnap1284/VibeTrack-AI.git
cd VibeTrack-AI
pip install -r requirements.txt
streamlit run app/app.py
```

---

## 🛠️ **Tech Stack**

* **Frontend/UI**: Streamlit + CSS styling
* **Backend Logic**: Python
* **NLP Model**: Sentiment/mood classification (based on captions)
* **Deployment Ready**: Can be hosted on Streamlit Cloud, Render, etc.

---

## 🖼️ **Sample Output**

> AI Mood: `Energetic`
> Recommended Songs:
> ✔️ Buzz
> ✔️ Party All Night
> ✔️ Bom Diggy Diggy
> ...and more!

---

## 📌 **Project Structure**

```bash
├── app/
│   ├── app.py               # Main Streamlit app
│   └── styles.css           # Custom UI styles
├── assets/                  # Mood images
├── dataset/                 # CSV data with songs
├── src/
│   └── recommend_music.py   # Recommendation logic
├── requirements.txt
└── README.md
```

---

## 📩 **Feedback / Contribution**

Want to improve the model or UI? Feel free to fork, clone, and contribute through pull requests.

---

