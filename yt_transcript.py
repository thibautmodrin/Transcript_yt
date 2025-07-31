#!/usr/bin/env python3

import os
import sys
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 📌 Configuration des variables d'environnement (à adapter si besoin)
API_KEY = os.getenv("OPENROUTER_API_KEY", "sk-or-v1-") 
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "mistralai/mistral-7b-instruct:free"

def get_transcript(video_id, lang):
    if lang == "fr":
        return YouTubeTranscriptApi().fetch(video_id, languages=["fr"])
    elif lang == "en":
        transcript_list = YouTubeTranscriptApi().list(video_id)
        transcript = transcript_list.find_transcript(["fr"])
        return transcript.translate("en").fetch()
    else:
        raise ValueError("Langue non supportée : utiliser 'fr' ou 'en'")

def summarize_transcript(text, lang):
    os.environ["OPENAI_API_KEY"] = API_KEY
    os.environ["OPENAI_BASE_URL"] = BASE_URL

    llm = ChatOpenAI(model=MODEL, temperature=0.7)

    system_msg = SystemMessage(content="""
Tu es un assistant professionnel qui résume des vidéos YouTube. 
Ta mission est de produire un résumé clair, concis et structuré en français à partir d’une transcription brute.

Voici les consignes :
- Ignore les hésitations ("euh", "bon", etc.).
- Reformule dans un style fluide et écrit.
- Structure le résumé avec des puces ou des paragraphes courts.
- Mets en avant les idées principales, sans recopier tout.
- Supprime les répétitions et digressions.
- Termine par une conclusion ou synthèse si c’est pertinent.
""")

    user_msg = HumanMessage(content=f"""
Voici la transcription complète d'une vidéo YouTube.

Ta tâche : rédiger un résumé structuré, fidèle au contenu mais plus lisible à l’écrit.

---

TRANSCRIPTION :

{text}

---

Commence directement par le résumé. Pas d'intro type "Voici le résumé", va droit au but.
""")

    response = llm.invoke([system_msg, user_msg])
    return response.content

def main():
    if len(sys.argv) != 3:
        print("Usage: ytsummary <video_id> <fr|en>")
        sys.exit(1)

    video_id = sys.argv[1]
    lang = sys.argv[2].lower()

    try:
        print("📥 Récupération de la transcription...")
        transcript_data = get_transcript(video_id, lang)
        text = TextFormatter().format_transcript(transcript_data)

        # 💾 Sauvegarde de la transcription brute
        transcript_dir = os.path.expanduser("~/Bureau/transcript")
        os.makedirs(transcript_dir, exist_ok=True)
        transcript_path = os.path.join(transcript_dir, f"transcript_{video_id}_{lang}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"📄 Transcription enregistrée dans : {transcript_path}")

        print("🧠 Génération du résumé via Mistral...")
        summary = summarize_transcript(text, lang)

        # 💾 Sauvegarde du résumé
        resume_dir = os.path.expanduser("~/Bureau/resumes")
        os.makedirs(resume_dir, exist_ok=True)
        resume_path = os.path.join(resume_dir, f"resume_{video_id}_{lang}.txt")
        with open(resume_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"\n✅ Résumé sauvegardé dans : {resume_path}\n")
        print("📄 Résumé :\n")
        print(summary)


    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
