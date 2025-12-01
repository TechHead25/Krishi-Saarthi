# ui.py  — Krishi Saarthi modern UI

import streamlit as st
import requests

# ===========================
# CONFIG & GLOBALS
# ===========================
BACKEND_URL = "http://127.0.0.1:8000"
# ========= MULTILINGUAL SUPPORT =========
if "lang" not in st.session_state:
    st.session_state.lang = "en"
T = {}
translations = {
    "en": {
        "lang_label": "🌐 Language",
        "lang_name": "English",
        "title": "Krishi Saarthi: Smart Crop & Fertilizer Advisor",

        "login_title": "Farmer Portal",
        "farmer_login_tab": "Farmer Login",
        "farmer_signup_tab": "Farmer Sign Up",

        "nav_predict": "Predict Yield",
        "nav_recommend": "Recommend Crop",
        "nav_optimize": "Optimize Yield",
        "nav_chat": "AI Chat",
        "nav_market": "Best Marketplace",
        "nav_disease": "Disease Detection",
        "nav_logout": "Logout",

        "predict_header": "Predict Yield for a Chosen Crop",
        "predict_sub": "Enter basic details to estimate yield.",
        "recommend_header": "Recommend Best Crop",
        "recommend_sub": "Based on location, fertilizer and irrigation.",
        "optimize_header": "Optimize Fertilizer & Irrigation",
        "optimize_sub": "Find the best input levels to maximize yield.",
        "chat_header": "AI Farming Assistant",
        "chat_sub": "Ask anything about crops, soil, irrigation or markets.",
        "market_header": "Best Marketplace for Your Yield",
        "market_sub": "Compare mandi prices after transport cost.",
        "disease_header": "Crop Disease Detection",
        "disease_sub": "Upload a clear image of the leaf for offline analysis.",

        "crop_label": "Select Crop",
        "location_label": "Location (City)",
        "fert_label": "Fertilizer (kg/ha)",
        "irr_label": "Irrigation (mm)",

        "btn_predict": "Predict Yield",
        "btn_recommend": "Recommend Crop",
        "btn_optimize": "Optimize",
        "btn_ask_ai": "Ask AI",
        "btn_best_market": "Find Best Market",
        "btn_analyze_disease": "Analyze Disease",
        "btn_admin_login": "Admin Login",
        "btn_admin_logout": "Admin Logout",

        "ai_question": "Your Question",
        "ai_voice_upload": "Or upload a voice question (audio)",
        "ai_voice_button": "Transcribe & Ask",
    },

    "hi": {
        "lang_label": "🌐 भाषा",
        "lang_name": "हिंदी",
        "title": "कृषि सारथी: स्मार्ट फसल व उर्वरक सलाहकार",

        "login_title": "किसान पोर्टल",
        "farmer_login_tab": "किसान लॉगिन",
        "farmer_signup_tab": "पंजीकरण",

        "nav_predict": "उपज की भविष्यवाणी",
        "nav_recommend": "फसल की सिफारिश",
        "nav_optimize": "उर्वरक व सिंचाई अनुकूलन",
        "nav_chat": "एआई चैट",
        "nav_market": "सर्वश्रेष्ठ मंडी",
        "nav_disease": "रोग पहचान",
        "nav_logout": "लॉगआउट",

        "predict_header": "चुनी गई फसल के लिए उपज की भविष्यवाणी",
        "predict_sub": "उपज का अनुमान लगाने के लिए विवरण भरें।",
        "recommend_header": "सर्वोत्तम फसल की सिफारिश",
        "recommend_sub": "स्थान, उर्वरक और सिंचाई के आधार पर।",
        "optimize_header": "उर्वरक व सिंचाई का अनुकूलन",
        "optimize_sub": "अधिकतम उपज के लिए सर्वोत्तम स्तर खोजें।",
        "chat_header": "एआई कृषि सहायक",
        "chat_sub": "फसल, मिट्टी, सिंचाई या मंडी से संबंधित प्रश्न पूछें।",
        "market_header": "आपकी उपज के लिए सर्वश्रेष्ठ मंडी",
        "market_sub": "परिवहन लागत के बाद मंडी लाभ की तुलना।",
        "disease_header": "फसल रोग पहचान",
        "disease_sub": "पत्ते की साफ़ तस्वीर अपलोड करें।",

        "crop_label": "फसल चुनें",
        "location_label": "स्थान (शहर)",
        "fert_label": "उर्वरक (किग्रा/हे)",
        "irr_label": "सिंचाई (मिमी)",

        "btn_predict": "उपज जानें",
        "btn_recommend": "फसल सुझाएँ",
        "btn_optimize": "अनुकूलित करें",
        "btn_ask_ai": "एआई से पूछें",
        "btn_best_market": "सर्वश्रेष्ठ मंडी खोजें",
        "btn_analyze_disease": "रोग जांचें",
        "btn_admin_login": "एडमिन लॉगिन",
        "btn_admin_logout": "एडमिन लॉगआउट",

        "ai_question": "अपना प्रश्न लिखें",
        "ai_voice_upload": "या ऑडियो से प्रश्न अपलोड करें",
        "ai_voice_button": "ऑडियो पहचानें व पूछें",
    },

    "kn": {
        "lang_label": "🌐 ಭಾಷೆ",
        "lang_name": "ಕನ್ನಡ",
        "title": "ಕೃಷಿ ಸಾರಥಿ: ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಮತ್ತು ರಸಗೊಬ್ಬರ ಸಲಹೆಗಾರ",

        "login_title": "ರೈತ ಪೋರ್ಟಲ್",
        "farmer_login_tab": "ರೈತ ಲಾಗಿನ್",
        "farmer_signup_tab": "ಹೊಸ ಖಾತೆ",

        "nav_predict": "ಉತ್ಪಾದನೆ ಮುನ್ಸೂಚನೆ",
        "nav_recommend": "ಬೆಳೆ ಶಿಫಾರಸು",
        "nav_optimize": "ರಸಗೊಬ್ಬರ & ನೀರಾವರಿ ಉತ್ತಮೀಕರಣ",
        "nav_chat": "ಎಐ ಚಾಟ್",
        "nav_market": "ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
        "nav_disease": "ರೋಗ ಗುರುತಿಸುವಿಕೆ",
        "nav_logout": "ಲಾಗ್‌ಔಟ್",

        "predict_header": "ಆಯ್ದ ಬೆಳೆಗಾಗಿ ಉತ್ಪಾದನೆ ಮುನ್ಸೂಚನೆ",
        "predict_sub": "ಉತ್ಪಾದನೆ ಅಂದಾಜಿಗೆ ವಿವರ ನೀಡಿ.",
        "recommend_header": "ಅತ್ಯುತ್ತಮ ಬೆಳೆ ಶಿಫಾರಸು",
        "recommend_sub": "ಸ್ಥಳ, ರಸಗೊಬ್ಬರ ಮತ್ತು ನೀರಾವರಿ ಆಧಾರಿತ.",
        "optimize_header": "ರಸಗೊಬ್ಬರ ಮತ್ತು ನೀರಾವರಿ ಉತ್ತಮೀಕರಣ",
        "optimize_sub": "ಗರಿಷ್ಠ ಉತ್ಪಾದನೆಗೆ ಸೂಕ್ತ ಮಟ್ಟ ಕಂಡುಹಿಡಿಯಿರಿ.",
        "chat_header": "ಎಐ ಕೃಷಿ ಸಹಾಯಕ",
        "chat_sub": "ಬೆಳೆ, ಮಣ್ಣು, ನೀರಾವರಿ ಅಥವಾ ಮಾರುಕಟ್ಟೆ ಬಗ್ಗೆ ಕೇಳಿ.",
        "market_header": "ನಿಮ್ಮ ಉತ್ಪನ್ನಕ್ಕೆ ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
        "market_sub": "ಸಾರಿಗೆ ವೆಚ್ಚದ ನಂತರ ಲಾಭದ ಲೆಕ್ಕಾಚಾರ.",
        "disease_header": "ಬೆಳೆ ರೋಗ ಪತ್ತೆ",
        "disease_sub": "ಇಲೆಯ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ.",

        "crop_label": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        "location_label": "ಸ್ಥಳ (ನಗರ)",
        "fert_label": "ರಸಗೊಬ್ಬರ (ಕೆಜಿ/ಹೆ)",
        "irr_label": "ನೀರಾವರಿ (ಮಿಮೀ)",

        "btn_predict": "ಉತ್ಪಾದನೆ ತಿಳಿ",
        "btn_recommend": "ಬೆಳೆ ಶಿಫಾರಸು",
        "btn_optimize": "ಉತ್ತಮಗೊಳಿಸಿ",
        "btn_ask_ai": "ಎಐಗೆ ಕೇಳಿ",
        "btn_best_market": "ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "btn_analyze_disease": "ರೋಗ ವಿಶ್ಲೇಷಿಸಿ",
        "btn_admin_login": "Admin Login",
        "btn_admin_logout": "Admin Logout",

        "ai_question": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಬರೆಯಿರಿ",
        "ai_voice_upload": "ಅಥವಾ ಧ್ವನಿ ಪ್ರಶ್ನೆಯನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ",
        "ai_voice_button": "ಧ್ವನಿ ಗುರುತಿಸಿ & ಕೇಳಿ",
    },

    "te": {
        "lang_label": "🌐 భాష",
        "lang_name": "తెలుగు",
        "title": "కృషి సారథి: స్మార్ట్ పంట & ఎరువుల సలహాదారు",

        "login_title": "రైతు పోర్టల్",
        "farmer_login_tab": "రైతు లాగిన్",
        "farmer_signup_tab": "కొత్త ఖాతా",

        "nav_predict": "దిగుబడి అంచనా",
        "nav_recommend": "పంట సిఫార్సు",
        "nav_optimize": "ఎరువులు & పిచికారీ ఆప్టిమైజేషన్",
        "nav_chat": "ఎ ఐ చాట్",
        "nav_market": "ఉత్తమ మార్కెట్",
        "nav_disease": "వ్యాధి నిర్ధారణ",
        "nav_logout": "లాగ్ అవుట్",

        "predict_header": "ఎంచుకున్న పంటకు దిగుబడి అంచనా",
        "predict_sub": "దిగుబడి అంచనాకు వివరాలు ఇవ్వండి.",
        "recommend_header": "ఉత్తమ పంట సిఫార్సు",
        "recommend_sub": "స్థానం, ఎరువు మరియు నీటి ఆధారంగా.",
        "optimize_header": "ఎరువులు మరియు నీటి ఆప్టిమైజేషన్",
        "optimize_sub": "గరిష్ట దిగుబడికి సరైన స్థాయిలు.",
        "chat_header": "ఎ ఐ వ్యవసాయ సహాయకుడు",
        "chat_sub": "పంట, నేల, నీటి సరఫరా లేదా మార్కెట్ గురించి అడగండి.",
        "market_header": "మీ దిగుబడికి ఉత్తమ మార్కెట్",
        "market_sub": "రవాణా ఖర్చుల తర్వాత లాభం పోలిక.",
        "disease_header": "పంట వ్యాధి గుర్తింపు",
        "disease_sub": "ఆకుని స్పష్టమైన ఫోటోను అప్లోడ్ చేయండి.",

        "crop_label": "పంట ఎంచుకోండి",
        "location_label": "స్థానం (నగరం)",
        "fert_label": "ఎరువు (కేజీ/హెక్టార్)",
        "irr_label": "పారుదల (మిల్లీమీటర్లు)",

        "btn_predict": "దిగుబడి చూపించు",
        "btn_recommend": "పంట సూచించు",
        "btn_optimize": "ఆప్టిమైజ్ చేయి",
        "btn_ask_ai": "ఎ ఐని అడగండి",
        "btn_best_market": "ఉత్తమ మార్కెట్ కనుగొనండి",
        "btn_analyze_disease": "వ్యాధి విశ్లేషణ",
        "btn_admin_login": "Admin Login",
        "btn_admin_logout": "Admin Logout",

        "ai_question": "మీ ప్రశ్నను రాయండి",
        "ai_voice_upload": "లేదా వాయిస్ ప్రశ్న అప్లోడ్ చేయండి",
        "ai_voice_button": "వాయిస్ గుర్తించి అడగండి",
    }
}

CROPS = ["wheat", "rice", "maize", "cotton", "sugarcane", "soybean", "groundnut"]
if "mode" not in st.session_state:
    st.session_state.mode = "login"   

if "auth" not in st.session_state:
    st.session_state.auth = {
        "logged_in": False,
        "name": None,
        "location": None
    }


    

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False



st.set_page_config(
    page_title="Krishi Saarthi: Smart Crop & Fertilizer Advisor",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===========================
# STYLES
# ===========================
def inject_css():
    st.markdown(
        """
        <style>
        /* ===== MAIN APP TEXT: BLACK ===== */
        .stApp, .stApp * {
            color: #000000 !important;
        }

        .stApp {
            background-color: #f3f5f7;
        }

        /* ===== SIDEBAR (WHITE TEXT ON DARK) ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #101820, #15232f);
        }
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* ===== CARDS ===== */
        .ks-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.08);
            border: 1px solid #e2e8f0;
            color: #000000 !important;
        }
        .ks-card * {
            color: #000000 !important;
        }

        .ks-card-highlight {
            border-left: 4px solid #166534;
        }

        /* ===== HEADINGS ===== */
        .ks-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #000000 !important;
        }

        .ks-subtitle {
            font-size: 0.95rem;
            color: #000000 !important;
        }

        /* ===== INPUT LABELS ===== */
        label, .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: #000000 !important;
            font-weight: 600;
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background-color: #166534;
            color: #ffffff !important;
            border-radius: 6px;
            border: none;
            padding: 0.4rem 1rem;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #15803d;
            color: #ffffff !important;
        }

        /* ===== INPUT FIELD TEXT VISIBILITY FIX ===== */

        /* Text typed inside inputs */
        input, textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
        }

        /* Number input text */
        input[type="number"] {
            color: #000000 !important;
            background-color: #ffffff !important;
        }

        /* Selectbox selected value */
        div[data-baseweb="select"] span {
            color: #000000 !important;
        }

        /* Placeholder text */
        ::placeholder {
            color: #555555 !important;
            opacity: 1 !important;
        }

        /* Dropdown menu items */
        div[data-baseweb="menu"] * {
            color: #000000 !important;
        }

        /* Input containers */
        div[data-testid="stTextInput"],
        div[data-testid="stNumberInput"],
        div[data-testid="stSelectbox"],
        div[data-testid="stTextArea"] {
            background-color: #f3f5f7 !important;
            border-radius: 6px;
        }
        /* Selected value in ALL selectboxes */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 6px;
}

/* Text inside selectbox */
div[data-baseweb="select"] span {
    color: #000000 !important;
    font-weight: 500;
}

/* Dropdown menu background */
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
}

/* Dropdown menu options text */
div[data-baseweb="menu"] * {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* ====== SIDEBAR LANGUAGE SELECT FIX ====== */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #000000 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* ====== SELECT CROP DROPDOWN FIX ====== */
div[data-testid="stSelectbox"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
}

        /* Dataframes */
        .dataframe * {
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()


# ===========================
# HELPERS
# ===========================
def soil_inputs(prefix=""):
    col1, col2 = st.columns(2)
    with col1:
        fert = st.number_input(
            "Fertilizer (kg/ha)", 0.0, 1000.0, 100.0, key=prefix + "fert"
        )
    with col2:
        irr = st.number_input(
            "Irrigation (mm)", 0.0, 2000.0, 200.0, key=prefix + "irr"
        )
    return fert, irr

def show_weather_card(weather: dict):
    if not weather:
        return
    with st.container():
        st.markdown(
            '<div class="ks-card"><div class="ks-title">Weather</div>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Temperature**")
            st.write(f"{weather.get('avg_temp_c', '-')} °C")
            st.write("**Humidity**")
            st.write(f"{weather.get('humidity_pct', '-')} %")
        with col2:
            st.write("**Rainfall**")
            st.write(f"{weather.get('rainfall_mm', '-')} mm")
            city = weather.get("city", "-")
            country = weather.get("country", "-")
            st.write("**Location**")
            st.write(f"{city}, {country}")
        st.markdown("</div>", unsafe_allow_html=True)


def post_json(endpoint: str, payload: dict, timeout: int = 40):
    try:
        r = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, timeout=timeout)
    except Exception as e:
        st.error(f"API error: {e}")
        return None

    try:
        data = r.json()
    except Exception:
        st.error("Backend returned non-JSON response.")
        st.code(r.text)
        return None

    if r.status_code != 200:
        st.error(data.get("detail", data.get("error", f"HTTP {r.status_code}")))
        return None

    if "error" in data:
        st.error(data["error"])
        return None

    return data


# ===========================
# LOGIN & SIGNUP
# ===========================
def login_signup_screen():
    st.title(f" {T['login_title']}")

    col_main, col_admin = st.columns([4, 1])

    with col_main:
        tab_login, tab_signup = st.tabs(["Farmer Login", "Farmer Sign Up"])

        with tab_login:
            st.subheader("Farmer Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                payload = {"username": username, "password": password}
                try:
                    r = requests.post(f"{BACKEND_URL}/login", json=payload, timeout=20)
                    data = r.json()
                except Exception as e:
                    st.error(f"Login error: {e}")
                    return

                if r.status_code == 200:
                    st.session_state.auth = {
                        "logged_in": True,
                        "name": data.get("name"),
                        "location": data.get("location")
                    }
                    st.session_state.mode = "farmer"
                    st.success("Farmer Logged In Successfully")
                    st.rerun()
                else:
                    st.error(data.get("detail", "Invalid username or password"))

        with tab_signup:
            st.subheader("Create Farmer Account")

            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            location = st.text_input("Village / City")
            username = st.text_input("Choose Username", key="su_user")
            password = st.text_input("Choose Password", type="password", key="su_pass")

            if st.button("Create Account"):
                if not all([name, phone, location, username, password]):
                    st.error("All fields are required.")
                else:
                    payload = {
                        "name": name,
                        "phone": phone,
                        "location": location,
                        "username": username,
                        "password": password
                    }
                    try:
                        r = requests.post(f"{BACKEND_URL}/signup", json=payload, timeout=20)
                        data = r.json()
                    except Exception as e:
                        st.error(f"Signup error: {e}")
                        return

                    if r.status_code == 200:
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error(data.get("detail", "Signup failed."))

    # ===== SMALL ADMIN LOGIN BUTTON =====
    with col_admin:
        st.markdown("###Admin")
        if st.button("Admin Login"):
            st.session_state.mode = "admin_login"
            st.rerun()

# ===========================
# MAIN SECTIONS
# ===========================
def section_predict():
    st.markdown(
        '<div class="ks-card ks-card-highlight">',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="ks-title">{T["predict_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ks-subtitle">{T["predict_sub"]}</div>', unsafe_allow_html=True)
   

    crop = st.selectbox("Select Crop", CROPS, key="pred_crop")
    default_loc = st.session_state.auth.get("location") or "Bangalore"
    location = st.text_input("Location (City)", default_loc, key="pred_loc")

    fert, irr = soil_inputs("pred_")
    

    if st.button("Predict Yield"):
        payload = {
    "crop": crop,
    "location": location,
    "fertilizer_kg_per_ha": fert,
    "irrigation_mm": irr,
}
        data = post_json("/predict", payload)
        if data:
            st.success(f"Predicted yield: {data['predicted_yield_t_per_ha']} t/ha")
            weather = data.get("weather_used", {})
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("") 
            col_main, col_weather = st.columns([2, 1])
            with col_main:
                pass  
            with col_weather:
                show_weather_card(weather)
            return

    st.markdown("</div>", unsafe_allow_html=True)


def section_recommend():
    st.markdown(
        '<div class="ks-card ks-card-highlight">',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="ks-title">{T["recommend_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ks-subtitle">{T["recommend_sub"]}</div>', unsafe_allow_html=True)
   

    default_loc = st.session_state.auth.get("location") or "Bangalore"
    location = st.text_input("Location (City)", default_loc, key="rec_loc")

    fert, irr = soil_inputs("rec_")

    
    if st.button("Recommend Crop"):
        payload = {
    "location": location,
    "crop": "",
    "fertilizer_kg_per_ha": fert,
    "irrigation_mm": irr,
}
        data = post_json("/recommend_crop", payload, timeout=60)
        if data:
            st.success(f"Recommended crop: {data['recommended_crop']}")
            st.write(f"Expected yield: {data['expected_yield_t_per_ha']} t/ha")

            mix = data.get("fertilizer_npk_kg_per_ha", data.get("fertilizer_npk", {}))
            if mix:
                st.write(
                    f"Recommended Fertilizer Mix (kg/ha): N {mix.get('N','-')} | "
                    f"P {mix.get('P','-')} | K {mix.get('K','-')}"
                )
            st.write(
                f"Best irrigation: {data.get('best_irrigation_mm', '-')} mm"
            )

            fert_names = data.get(
                "recommended_fertilizer_names",
                data.get("recommended_fertilizers_names", []),
            )
            if fert_names:
                st.write("Fertilizer types:")
                for f in fert_names:
                    st.markdown(f"- {f}")

            weather = data.get("weather_used", {})
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")
            col_main, col_weather = st.columns([2, 1])
            with col_weather:
                show_weather_card(weather)
            return

    st.markdown("</div>", unsafe_allow_html=True)


def section_optimize():
    st.markdown(
        '<div class="ks-card ks-card-highlight">',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="ks-title">{T["optimize_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ks-subtitle">{T["optimize_sub"]}</div>', unsafe_allow_html=True)


    crop = st.selectbox("Select Crop", CROPS, key="opt_crop")
    default_loc = st.session_state.auth.get("location") or "Bangalore"
    location = st.text_input("Location (City)", default_loc, key="opt_loc")

    fert, irr = soil_inputs("opt_")
    

    if st.button("Optimize"):
        payload = {
    "crop": crop,
    "location": location,
    "fertilizer_kg_per_ha": fert,
    "irrigation_mm": irr,
}
        data = post_json("/optimize_yield", payload, timeout=60)
        if data:
            st.success(f"Optimized yield: {data['optimized_yield_t_per_ha']} t/ha")
            st.write(f"Best fertilizer: {data['best_fertilizer_kg_per_ha']} kg/ha")
            st.write(f"Best irrigation: {data['best_irrigation_mm']} mm")

            mix = data.get("fertilizer_npk_kg_per_ha", data.get("fertilizer_npk", {}))
            if mix:
                st.write(
                    f"Recommended Fertilizer Mix (kg/ha): N {mix.get('N','-')} | "
                    f"P {mix.get('P','-')} | K {mix.get('K','-')}"
                )

            fert_names = data.get(
                "recommended_fertilizer_names",
                data.get("recommended_fertilizers", []),
            )
            if fert_names:
                st.write("Fertilizer types:")
                for f in fert_names:
                    st.markdown(f"- {f}")

            weather = data.get("weather_used", {})
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")
            col_main, col_weather = st.columns([2, 1])
            with col_weather:
                show_weather_card(weather)
            return

    st.markdown("</div>", unsafe_allow_html=True)


def section_chat():
    global T
    st.markdown(
        '<div class="ks-card ks-card-highlight">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="ks-title">{T["chat_header"]}</div>'
        f'<div class="ks-subtitle">{T["chat_sub"]}</div>',
        unsafe_allow_html=True,
    )

    user_msg = st.text_area(T["ai_question"], key="chat_text")
    crop = st.selectbox(T["crop_label"], CROPS, key="chat_crop")

    fert, irr = soil_inputs("chat_")

    col1, col2, col3 = st.columns(3)
    with col1:
        temp = st.number_input("Temperature (°C)", 0.0, 50.0, 26.0)
    with col2:
        hum = st.number_input("Humidity (%)", 0.0, 100.0, 70.0)
    with col3:
        rain = st.number_input("Rainfall (mm)", 0.0, 1000.0, 120.0)

    # ---- TEXT CHAT ----
    if st.button(T["btn_ask_ai"]):
        if not user_msg.strip():
            st.error("Please enter a question.")
        else:
            payload = {
                "message": user_msg,
                "crop": crop,
                "fertilizer_kg_per_ha": fert,
                "irrigation_mm": irr,
                "avg_temp_c": temp,
                "humidity_pct": hum,
                "rainfall_mm": rain,
                "lang": T  
            }
            data = post_json("/chat", payload)
            if data:
                st.markdown("**Chatbot Reply:**")
                st.write(data.get("reply", "No reply received."))

    st.markdown("---")

    # ---- VOICE CHAT ----
    st.markdown(f"#### 🎙️ {T['ai_voice_upload']}")
    audio_file = st.file_uploader(" ", type=["wav", "mp3", "m4a"], key="voice_upload")

    if st.button(T["ai_voice_button"]):
        if not audio_file:
            st.error("Please upload an audio file.")
        else:
            files = {
                "file": (
                    audio_file.name,
                    audio_file.getvalue(),
                    audio_file.type,
                )
            }
            try:
                r = requests.post(f"{BACKEND_URL}/voice_chat", files=files, timeout=60)
                data = r.json()
            except Exception as e:
                st.error(f"API error: {e}")
                st.markdown("</div>", unsafe_allow_html=True)
                return

            if "reply" not in data:
                st.error("Unexpected response from backend.")
                st.json(data)
            else:
                if "question" in data:
                    st.markdown("**Transcribed Question:**")
                    st.write(data["question"])
                st.markdown("**Chatbot Reply (Voice):**")
                st.write(data["reply"])

    st.markdown("</div>", unsafe_allow_html=True)


def section_best_market():
    st.markdown(
        '<div class="ks-card ks-card-highlight">',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="ks-title">{T["market_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ks-subtitle">{T["market_sub"]}</div>', unsafe_allow_html=True)

    crop = st.selectbox("Select Crop", CROPS, key="m_crop")
    default_loc = st.session_state.auth.get("location") or "Bangalore"
    location = st.text_input("Location (City)", default_loc, key="m_loc")

    fert, irr = soil_inputs("m_")

    

    if st.button("Find Best Market"):
        payload = {
    "crop": crop,
    "location": location,
    "fertilizer_kg_per_ha": fert,
    "irrigation_mm": irr,
}
        data = post_json("/best_market", payload, timeout=60)
        if data:
            best = data.get("best_market", {})
            st.success(f"Best Mandi: {best.get('market', 'N/A')}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Price (₹/quintal)", best.get("price_per_quintal", 0))
            with col2:
                st.metric("Distance (km)", best.get("distance_km", 0))
            with col3:
                st.metric("Net Profit (₹)", best.get("net_profit", 0))

            all_markets = data.get("all_market_comparisons", [])
            if all_markets:
                st.write("Detailed comparison:")
                st.dataframe(all_markets)

    st.markdown("</div>", unsafe_allow_html=True)


def section_disease():
    st.markdown(
        '<div class="ks-card ks-card-highlight">',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="ks-title">{T["disease_header"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ks-subtitle">{T["disease_sub"]}</div>', unsafe_allow_html=True)


    uploaded_file = st.file_uploader(
        "Upload crop image (leaf close-up)", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, use_column_width=True)

    if st.button("Analyze Disease"):
        if not uploaded_file:
            st.error("Please upload an image first.")
        else:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }
            try:
                r = requests.post(
                    f"{BACKEND_URL}/disease_detect", files=files, timeout=60
                )
                data = r.json()
            except Exception as e:
                st.error(f"API error: {e}")
                st.markdown("</div>", unsafe_allow_html=True)
                return

            if "infected" not in data:
                st.error("Unexpected response from backend.")
                st.json(data)
            else:
                if data["infected"]:
                    st.error(
                        f"Plant appears INFECTED (Severity: {data.get('severity','unknown')})"
                    )
                else:
                    st.success("Plant appears HEALTHY")

                st.write(f"**Disease / Condition:** {data.get('disease_name', 'N/A')}")
                st.write(f"**Advice:** {data.get('advice', 'N/A')}")
                st.write(f"**Prevention:** {data.get('prevention', 'N/A')}")
                if "confidence" in data:
                    st.info(f"Confidence: {data['confidence']} %")
                if "mode" in data:
                    st.caption(f"Detection mode: {data['mode']}")

    st.markdown("</div>", unsafe_allow_html=True)

def admin_login_screen():
    st.title("Admin Login")

    username = st.text_input("Admin Username", key="admin_user")
    password = st.text_input("Admin Password", type="password", key="admin_pass")

    if st.button("Login as Admin"):
        payload = {"username": username, "password": password}

        try:
            r = requests.post(f"{BACKEND_URL}/admin_login", json=payload, timeout=10)
            data = r.json()
        except Exception as e:
            st.error(f"API error: {e}")
            return

        if r.status_code == 200:
            st.success("Admin Login Successful")
            st.session_state.mode = "admin"
            st.rerun()
        else:
            st.error(data.get("detail", "Invalid admin credentials"))

    if st.button("⬅️ Back to Farmer Login"):
        st.session_state.mode = "login"
        st.rerun()

def admin_dashboard():
    st.title("Farmer Database (Admin Panel)")

    r = requests.get(f"{BACKEND_URL}/admin/farmers")
    farmers = r.json()

    if farmers:
        st.dataframe(farmers)

        farmer_ids = [str(f["id"]) for f in farmers]
        selected = st.selectbox("Select Farmer ID to Delete", farmer_ids)

        if st.button("Delete Farmer"):
            requests.delete(f"{BACKEND_URL}/admin/farmer/{selected}")
            st.success("Farmer Deleted")
            st.rerun()
    else:
        st.info("No farmers registered yet.")

# ===========================
# APP ENTRYPOINT
# ===========================
def main():
    global T

    # ===== LANGUAGE SELECTOR =====
    st.sidebar.selectbox(
        "Language / भाषा / ಭಾಷೆ / భాష",
        ["en", "hi", "kn", "te"],
        index=["en", "hi", "kn", "te"].index(st.session_state.lang),
        key="lang_select",
        format_func=lambda x: translations[x]["lang_name"],
    )

    st.session_state.lang = st.session_state.lang_select
    T = translations[st.session_state.lang]

    # ========= LOGIN MODE =========
    if st.session_state.mode == "login":
        login_signup_screen()
        return

    # ========= ADMIN LOGIN MODE =========
    if st.session_state.mode == "admin_login":
        admin_login_screen()
        return

    # ========= ADMIN DASHBOARD =========
    if st.session_state.mode == "admin":
        admin_dashboard()

        if st.button("Admin Logout"):
            st.session_state.mode = "login"
            st.rerun()
        return

    # ========= FARMER DASHBOARD =========
    if st.session_state.mode == "farmer":

        st.sidebar.title("Farmer Menu")

        page = st.sidebar.radio(
            "Go to",
            [
                "Predict Yield",
                "Recommend Crop",
                "Optimize Yield",
                "AI Chat",
                "Best Marketplace",
                "Disease Detection",
                "Logout",
            ],
        )

        if page == "Predict Yield":
            section_predict()
        elif page == "Recommend Crop":
            section_recommend()
        elif page == "Optimize Yield":
            section_optimize()
        elif page == "AI Chat":
            section_chat()
        elif page == "Best Marketplace":
            section_best_market()
        elif page == "Disease Detection":
            section_disease()
        elif page == "Logout":
            st.session_state.auth = {"logged_in": False, "name": None, "location": None}
            st.session_state.mode = "login"
            st.rerun()


if __name__ == "__main__":
    main()

