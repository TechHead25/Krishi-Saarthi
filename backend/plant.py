import base64
import requests
import os

PLANT_ID_API_KEY ="FOW6ptjPpJO5zzKH3SYcPjt4f1ueowonULeqkFoD3gqyIF2UGE"


def analyze_with_plant_id(image_bytes: bytes):

    if not PLANT_ID_API_KEY:
        raise ValueError("PLANT_ID_API_KEY is missing")

    encoded = base64.b64encode(image_bytes).decode("utf-8")

    url =  "https://crop.kindwise.com/api/v1/identification"   

    headers = {
        "Api-Key": PLANT_ID_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "images": [encoded],
        "disease_details": ["cause", "treatment", "prevention"]
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)

    print("PLANT STATUS:", response.status_code)
    print("PLANT RAW TEXT:", response.text[:500])  
    try:
        data = response.json()
    except Exception:
        raise ValueError("Plant.id returned non-JSON (likely invalid key or HTML error)")

    if response.status_code != 200:
        raise ValueError(data)

    assessment = data["health_assessment"]
    healthy = assessment["is_healthy"]["binary"]
    prob = assessment["is_healthy"]["probability"]

    if healthy:
        return {
            "infected": False,
            "severity": "none",
            "disease_name": "Healthy Plant",
            "advice": "Plant shows no visible disease symptoms.",
            "prevention": "Maintain proper irrigation and fertilizer balance.",
            "confidence": round(prob * 100, 2)
        }


    disease = assessment["diseases"][0]

    return {
        "infected": True,
        "severity": "high",
        "disease_name": disease.get("name", "Unknown disease"),
        "advice": (
            disease.get("treatment", {}).get("chemical")
            or disease.get("treatment", {}).get("biological")
            or "Consult nearest agriculture officer."
        ),
        "prevention": disease.get("prevention", "Follow crop rotation and avoid leaf wetness."),
        "confidence": round((1 - prob) * 100, 2)
    }

