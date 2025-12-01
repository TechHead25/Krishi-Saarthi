#main.py

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.params import File
from pydantic import BaseModel
import joblib
import numpy as np
import xgboost as xgb
from ai_chatbot import ai_chatbot_response
import os
from PIL import Image
from weather import get_weather
from optimizer import optimize_yield, get_fertilizer_names
from crop_recommender import recommend_crop
from market import get_best_market
from plant import analyze_with_plant_id ,PLANT_ID_API_KEY
import streamlit as st
import requests
from database import get_db, init_db

app = FastAPI(title="Krishi Saarthi Backend")
init_db()

MODEL_PATH = r"C:\Projects\SIH\AI2\model\xgb_model.pkl"
obj = joblib.load(MODEL_PATH)
model, FEATURES, le = obj["model"], obj["features"], obj["label_encoder"]
print("Loaded crops:", list(le.classes_))


# 🟢 Updated Input Data model (added latitude + longitude)
class InputData(BaseModel):
    crop: str
    location: str
    fertilizer_kg_per_ha: float = 100
    irrigation_mm: float = 200

    nitrogen_ppm: float = 40
    phosphorus_ppm: float = 30
    potassium_ppm: float = 30
    soil_ph: float = 6.5

    latitude: float = 0.0
    longitude: float = 0.0
# ---------------------------
# Simple Auth Models
# ---------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    name: str
    username: str
    phone: str
    password: str
    location: str
# Dummy in-memory users (you can replace with DB later)

def dummy_transcribe_audio(audio_bytes: bytes) -> str:
    # TODO: integrate Whisper / Google STT / Vosk etc.
    return "Voice transcription feature is not fully configured yet."


USERS_DB = {}
@app.post("/login")
def login(data: dict):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM farmers WHERE username=? AND password=?", 
                (data["username"], data["password"]))
    user = cur.fetchone()

    if not user:
        return {"detail": "Invalid username or password"}

    return {
        "username": user["username"],
        "name": user["name"],
        "phone": user["phone"],
        "location": user["location"]
    }

@app.post("/signup")
def signup(data: dict):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            "INSERT INTO farmers (name, phone, location, username, password) VALUES (?, ?, ?, ?, ?)",
            (data["name"], data["phone"], data["location"], data["username"], data["password"])
        )
        db.commit()
        return {"message": "Account created successfully"}
    except:
        return {"detail": "Username already exists"}

# ---------------------------
# Root Endpoint
# ---------------------------
@app.get("/")
def root():
    return {"message": "Krishi Saarthi Backend is running!"}

@app.post("/admin_login")
def admin_login(data: dict):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM admins WHERE username=? AND password=?", 
                (data["username"], data["password"]))
    admin = cur.fetchone()

    if not admin:
        return {"detail": "Invalid admin credentials"}

    return {"message": "Admin login successful"}
@app.get("/admin/farmers")
def get_farmers():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, name, phone, location, username FROM farmers")
    farmers = cur.fetchall()
    return [dict(row) for row in farmers]

@app.delete("/admin/farmer/{farmer_id}")
def delete_farmer(farmer_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM farmers WHERE id=?", (farmer_id,))
    db.commit()
    return {"message": "Farmer deleted successfully"}

# ---------------------------
# Predict Yield Endpoint
# ---------------------------
@app.post("/predict")
def predict(req: InputData):
    try:
        weather_data = get_weather(req.location)

        if req.crop not in le.classes_:
            raise ValueError(f"Unknown crop: {req.crop}")

        crop_encoded = int(le.transform([req.crop])[0])

        row = {
            "nitrogen_ppm": req.nitrogen_ppm,
            "phosphorus_ppm": req.phosphorus_ppm,
            "potassium_ppm": req.potassium_ppm,
            "soil_ph": req.soil_ph,
            "fertilizer_kg_per_ha": req.fertilizer_kg_per_ha,
            "irrigation_mm": req.irrigation_mm,
            "crop_encoded": crop_encoded,
            "avg_temp_c": weather_data["avg_temp_c"],
            "humidity_pct": weather_data["humidity_pct"],
            "rainfall_mm": weather_data["rainfall_mm"],
        }

        x_input = np.array([[row[f] for f in FEATURES]])
        dmat = xgb.DMatrix(x_input, feature_names=FEATURES)
        pred = float(model.predict(dmat)[0])

        return {
            "crop": req.crop,
            "location": req.location,
            "predicted_yield_t_per_ha": round(pred, 3),
            "weather_used": weather_data
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------
# Recommend Best Crop
# ---------------------------
@app.post("/recommend_crop")
def recommend_crop_api(req: InputData):
    try:
        weather_data = get_weather(req.location)

        soil = {
            "nitrogen_ppm": req.nitrogen_ppm,
            "phosphorus_ppm": req.phosphorus_ppm,
            "potassium_ppm": req.potassium_ppm,
            "soil_ph": req.soil_ph,
            "fertilizer_kg_per_ha": req.fertilizer_kg_per_ha,
            "irrigation_mm": req.irrigation_mm,
        }

        res = recommend_crop(model, FEATURES, le, soil, weather_data, budget_fert=200, budget_irr=500)
        fert_names = get_fertilizer_names(res["best_crop"])

        return {
            "recommended_crop": res["best_crop"],
            "expected_yield_t_per_ha": round(res["expected_yield_t_per_ha"], 3),
            "best_fertilizer_kg_per_ha": res["best_fertilizer_kg_per_ha"],
            "best_irrigation_mm": res["best_irrigation_mm"],
            "fertilizer_npk_kg_per_ha": res["fertilizer_npk"],
            "recommended_fertilizer_names": fert_names,
            "weather_used": weather_data
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------
# Optimize Yield
# ---------------------------
@app.post("/optimize_yield")
def optimize_yield_api(req: InputData):
    try:
        weather_data = get_weather(req.location)

        if req.crop not in le.classes_:
            raise ValueError(f"Unknown crop: {req.crop}")

        crop_encoded = int(le.transform([req.crop])[0])

        payload = {
            "nitrogen_ppm": req.nitrogen_ppm,
            "phosphorus_ppm": req.phosphorus_ppm,
            "potassium_ppm": req.potassium_ppm,
            "soil_ph": req.soil_ph,
            "fertilizer_kg_per_ha": req.fertilizer_kg_per_ha,
            "irrigation_mm": req.irrigigation_mm,
            "crop_encoded": crop_encoded,
            "avg_temp_c": weather_data["avg_temp_c"],
            "humidity_pct": weather_data["humidity_pct"],
            "rainfall_mm": weather_data["rainfall_mm"],
        }

        opt = optimize_yield(model, FEATURES, payload)
        fert_names = get_fertilizer_names(req.crop)

        return {
            "crop": req.crop,
            "optimized_yield_t_per_ha": round(opt["expected_yield_t_per_ha"], 3),
            "best_fertilizer_kg_per_ha": opt["best_fertilizer_kg_per_ha"],
            "best_irrigation_mm": opt["best_irrigation_mm"],
            "fertilizer_npk_kg_per_ha": opt["fertilizer_npk"],
            "recommended_fertilizer_names": fert_names,
            "weather_used": weather_data
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------
# BEST MARKET ENDPOINT
# ---------------------------
@app.post("/best_market")
def best_market_api(req: InputData):
    try:
        weather_data = get_weather(req.location)

        crop = req.crop.lower()
        if crop not in le.classes_:
            raise ValueError(f"Unknown crop: {req.crop}")

        crop_encoded = int(le.transform([crop])[0])

        row = {
            "nitrogen_ppm": req.nitrogen_ppm,
            "phosphorus_ppm": req.phosphorus_ppm,
            "potassium_ppm": req.potassium_ppm,
            "soil_ph": req.soil_ph,
            "fertilizer_kg_per_ha": req.fertilizer_kg_per_ha,
            "irrigation_mm": req.irrigation_mm,
            "crop_encoded": crop_encoded,
            "avg_temp_c": weather_data["avg_temp_c"],
            "humidity_pct": weather_data["humidity_pct"],
            "rainfall_mm": weather_data["rainfall_mm"],
        }

        x_input = np.array([[row[f] for f in FEATURES]])
        d = xgb.DMatrix(x_input, feature_names=FEATURES)
        predicted_yield = float(model.predict(d)[0])  # in tons

        best_market, all_markets = get_best_market(
            crop, req.latitude, req.longitude, predicted_yield
        )

        return {
            "crop": crop,
            "predicted_yield_tons": round(predicted_yield, 3),
            "best_market": best_market,
            "all_market_comparisons": all_markets,
            "weather_used": weather_data
        }

    except Exception as e:
        return {"error": str(e)}


# ---------------------------
# Simple Chat Endpoint
# ---------------------------


@app.post("/chat")
def chat(req: dict):
    try:
        user_msg = str(req.get("message", "")).replace("\n", " ").strip()

        if not user_msg:
            return {"reply": "Please enter a farming question."}

        try:
            reply = ai_chatbot_response(user_msg, req)
        except Exception as ai_err:
            print("AI ERROR:", ai_err)
            reply = "AI service is currently unavailable. Please try again."

        return {"reply": reply}

    except Exception as e:
        print("CHAT ENDPOINT ERROR:", e)
        return {"error": str(e)}
    

@app.post("/voice_chat")
async def voice_chat(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        text_question = dummy_transcribe_audio(audio_bytes)

        # You can reuse your existing chat logic here:
        # For now, we just echo + wrap with your chat endpoint style.
        reply = f"I understood your voice question as: '{text_question}'. Please integrate real STT for production."

        return {
            "question": text_question,
            "reply": reply
        }

    except Exception as e:
        return {"error": str(e)}
    
@app.post("/disease_detect")
async def disease_detect(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Please upload a valid image.")

        img_bytes = await file.read()
        result = analyze_with_plant_id(img_bytes)

        # ✅ Ensure result always has these keys
        if "infected" not in result:
            return {
                "infected": False,
                "severity": "unknown",
                "disease_name": "Unable to analyze",
                "advice": "Image unclear or API unavailable.",
                "prevention": "Try again with a clearer image.",
                "confidence": 0
            }

        return {
            "filename": file.filename,
            **result
        }

    except Exception as e:
        print("DISEASE API ERROR:", e)
        return {
            "infected": False,
            "severity": "unknown",
            "disease_name": "API Error",
            "advice": "Disease detection service is temporarily unavailable.",
            "prevention": "Please try again later.",
            "confidence": 0
        }

@app.get("/plant_test")
def plant_test():
    return {
        "api_key_loaded": bool(PLANT_ID_API_KEY),
        "api_key_length": len(PLANT_ID_API_KEY) if PLANT_ID_API_KEY else 0
    }
