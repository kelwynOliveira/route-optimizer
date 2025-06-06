![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/) [![Google Maps API](https://img.shields.io/badge/API-Google%20Maps-4285F4?logo=googlemaps&logoColor=white)](https://developers.google.com/maps/documentation/distance-matrix)

# 🚗 Route Optimizer with Google Maps (by time)

- Find the most time-efficient route between multiple locations using the Google Distance Matrix API and an optimization algorithm.
- Supports driving, walking, biking, and public transport.

Streamlit app link: [https://routes-maps.streamlit.app/](https://routes-maps.streamlit.app/)

---

## 🖼️ Preview

![Route Optimizer](assets/routes.png)

---

## 🧠 Features

- Add and edit a list of addresses dynamically
- Select start and end points independently
- Choose transportation mode (driving, walking, biking, public transport)
- Optimize route using the **Traveling Salesman Problem** formulation with constraints
- Generate a link to the optimized route directly on **Google Maps**
- Display the route on an embedded map

---

## ⚙️ How to Run

### 1️⃣ Create a virtual environment (optional but recommended)

For macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the app

```bash
streamlit run main.py
```

---

### 4️⃣ Stop the app

To deactivate the virtual environment when you're done:

```bash
deactivate
```

---

## ✨ How It Works

This app uses the **[Google Routes API](https://developers.google.com/maps/documentation/routes)** to calculate travel times between addresses, then applies a **Linear Programming model** to find the shortest-duration route based on:

- Start and end location
- Selected travel mode (car, walk, bike, public transport)

It supports both **circular (round-trip)** and **open (point-to-point)** route planning.

---

## 📁 Project Structure

```
.
├── main.py         # Streamlit app
├── aux.py          # Route calculation and API integration
└── requirements.txt
```

---

## 📌 Notes

- Ensure all addresses are valid and correctly formatted.
- API responses may vary based on limits and usage quota.
