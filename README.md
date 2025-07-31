
# 📼 ytsummary – Résumeur de vidéos YouTube (FR/EN)

`ytsummary` est un script Python en ligne de commande qui :
1. Récupère automatiquement la **transcription d'une vidéo YouTube** (si disponible).
2. Génère un **résumé structuré et clair** grâce à un **modèle LLM** (Mistral via OpenRouter).
3. Sauvegarde le résumé dans un fichier texte prêt à lire.
4. Ouvre automatiquement l'application de lecture de texte par défaut.

---

## 🚀 Fonctionnalités

- 🔍 Supporte les transcriptions **françaises et anglaises**.
- 🧠 Résumé généré automatiquement avec un **LLM open-source** (gratuit).
- 💾 Fichiers sauvegardés dans :
  - `/home/<user>/Bureau/transcript` pour la transcription
  - `/home/<user>/Bureau/resumes` pour le résumé
- 🖥️ Ouvre automatiquement le fichier résumé dans ton éditeur de texte préféré (`xdg-open`).

---

## 📦 Prérequis

- Python 3.8+
- Compte gratuit sur [https://openrouter.ai](https://openrouter.ai) avec une clé API.

### 🔧 Dépendances Python

Installe-les avec pip :

```bash
pip install youtube-transcript-api langchain langchain-openai openai
```

---

## 🛠️ Configuration

### 1. Exporter ta clé API OpenRouter :

```bash
export OPENROUTER_API_KEY="sk-or-..."
```

Tu peux aussi l'ajouter à ton `~/.bashrc` ou `~/.zshrc`.

---

## 🧑‍💻 Utilisation

```bash
ytsummary <video_id> <langue>
```

- `<video_id>` : identifiant YouTube (ex. `CaWS4HNqdc0`)
- `<langue>` : `fr` ou `en`

### Exemple :

```bash
ytsummary CaWS4HNqdc0 fr
```

✅ Cela va :
1. Télécharger la transcription de la vidéo.
2. Générer un résumé via Mistral.
3. Sauvegarder et ouvrir le résumé dans ton application par défaut.

---

## 📁 Arborescence

```
📁 Bureau
 ├── 📁 transcript
 │    └── transcript_<id>_<lang>.txt
 └── 📁 resumes
      └── resume_<id>_<lang>.txt
```

---

## 🧠 Modèle utilisé

- **Modèle** : `mistralai/mistral-7b-instruct:free`
- **Fournisseur** : OpenRouter (https://openrouter.ai)
- **Coût** : gratuit pour usage raisonnable

---

## 🐛 Limitations

- Fonctionne uniquement avec les vidéos dont les sous-titres sont publics.
- Si la vidéo est trop longue, la requête LLM peut échouer (limite de tokens).
- Dépend d’une connexion internet.

---

## 📜 Licence

Projet personnel – libre d’usage à des fins éducatives ou personnelles.
```
