import streamlit as st
import google.generativeai as genai
from groq import Groq

# --- CONFIGURATION VISUELLE (Design Purple & Dark) ---
st.set_page_config(page_title="BookAI", page_icon="B", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #000000; color: white; }
    .stButton>button { 
        background-color: #7B42F6; color: white; 
        border-radius: 12px; height: 3.5em; width: 100%;
        font-weight: bold; border: none; font-size: 18px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1A1A1A; color: white; border: 1px solid #7B42F6;
    }
    .credit-badge { 
        background: #1A1A1A; padding: 10px; border-radius: 20px;
        border: 1px solid #7B42F6; text-align: center; color: #7B42F6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- RÉCUPÉRATION DES CLÉS (Via les secrets Streamlit) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.warning("⚠️ Configuration des clés API manquante dans les Secrets.")

# --- INTERFACE ---
st.markdown("<div class='credit-badge'>TONIO : 56 Crédit(s)</div>", unsafe_allow_html=True)
st.title("Ebook pro en 5 minutes")

niche = st.text_input("NICHE DE L'EBOOK", placeholder="Ex: Fitness, Marketing...")
ton = st.selectbox("TON DE RÉDACTION", ["Autoritaire & Éducatif", "Amical & Inspirant", "Direct"])
description = st.text_area("DESCRIPTION", placeholder="Décrivez votre idée simplement...")
pages = st.slider("NOMBRE DE PAGES CIBLE", 1, 50, 10)

if st.button("GÉNÉRER LE PLAN"):
    # Logique stratégique selon tes captures AI Studio
    structure = "choses simples sans chapitres"
    if pages >= 40: structure = "un plan modulaire pro complet"
    elif pages >= 20: structure = "une structure par chapitres détaillés"

    prompt = f"Expert Marketing. Génère un plan pour un ebook de {pages} pages sur {niche}. Ton: {ton}. Description: {description}. Structure demandée: {structure}."
    
    with st.spinner("L'IA crée ton marketing en béton..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.success("Plan stratégique généré !")
            st.markdown(response.text)
        except:
            # Béquille Groq
            completion = client_groq.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(completion.choices[0].message.content)
