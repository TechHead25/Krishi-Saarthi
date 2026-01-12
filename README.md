# Krishi Saarthi  
## AI-Powered Smart Crop Advisory & Agricultural Decision Support System

Krishi Saarthi is an intelligent, farmer-centric agricultural advisory platform that leverages **Machine Learning, Artificial Intelligence, and real-time data** to assist farmers in making informed decisions related to crop selection, yield prediction, fertilizer and irrigation optimization, disease detection, and market selection.

The system is designed to be **simple, scalable, and accessible**, ensuring that even farmers with minimal technical knowledge can benefit from advanced AI-driven insights.

---

 Features

  Farmer Module
- Secure Login & Signup
- Crop Yield Prediction
- Best Crop Recommendation
- Fertilizer & Irrigation Optimization
- Crop Disease Detection (Image-based)
- AI Chat Assistant (Text + Voice)
- Best Market / Mandi Recommendation
- Multilingual Support (English, Hindi, Kannada, Telugu)

 Admin Module
- Admin Login
- View Registered Farmers
- Delete Farmer Records
- Centralized Admin Dashboard

---

 AI & Machine Learning

- **XGBoost Regression Model** for crop yield prediction
- Multi-crop handling using **Label Encoding**
- Weather-based feature integration
- Fertilizer & irrigation-sensitive predictions
- Offline fallback for disease detection
- Explainable and data-driven recommendations

---

 System Architecture

    Frontend (Streamlit UI)
    |
    | REST APIs
    v
    Backend (FastAPI)
    |
    | Machine Learning Model
    v
    XGBoost Model + SQLite Database

---

 Deployment

- **Backend Hosted On:** Render  
- **Frontend Hosted On:** Lovable  

The backend services are deployed using Render to ensure scalability and reliability.  
The frontend interface is hosted on Lovable to provide a responsive and user-friendly experience.

---

 **Tech Stack**

 Frontend
- Streamlit
- HTML & CSS (Custom UI Styling)
- Multilingual Interface Support

 Backend
- FastAPI
- Python
- SQLite Database
- RESTful APIs
- CORS Middleware

 Machine Learning
- XGBoost
- NumPy
- Scikit-learn
- Joblib

 Tools & Platforms
- Render (Backend Hosting)
- Lovable (Frontend Hosting)
- GitHub (Version Control)

---

**Project Structure**

    Krishi-Saarthi/
    │
    ├── backend/
    │ ├── main.py
    │ ├── optimizer.py
    │ ├── crop_recommender.py
    │ ├── weather.py
    │ ├── market.py
    │ ├── plant.py
    │ ├── database.py
    │ ├── xgb_multi_crop.pkl
    │
    ├── frontend/
    │ ├── ui.py
    │
    ├── requirements.txt
    ├── README.md

---

*How to Run Locally*

Step 1: Clone the Repository
```
git clone https://github.com/TechHead25/Krishi-Saarthi.git
cd Krishi-Saarthi
```
Step 2: Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```
Step 3: Install Dependencies
```
pip install -r requirements.txt
```
Step 4: Run Backend
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
Step 5: Run Frontend
```
streamlit run ui.py
```

---

**Advantages**

- Provides accurate and data-driven agricultural recommendations
- Improves crop yield and reduces fertilizer and irrigation wastage
- Enhances farmer income through better market participation
- Overcomes literacy barriers using voice-based interaction
- Builds farmer trust through explainable AI
- Scalable and adaptable across different regions and crops

---

**Limitations**

- Initial dependency on availability and quality of agricultural data
- Requires access to a basic smartphone and internet connectivity
- Prediction accuracy may be affected by extreme climatic events
- Early adoption may require farmer awareness and training

---

**Future Enhancements**

- Integration of IoT-based soil sensors for real-time monitoring
- Satellite imagery and remote sensing for large-scale crop health analysis
- Deep learning models such as LSTM for seasonal forecasting
- Support for additional crops and regional languages
- Integration with government schemes, insurance platforms, and financial services

---
