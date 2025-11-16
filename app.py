import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import io
import time
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Assistants Entretien",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }
    
    label, p, span, div {
        color: #E0E0E0 !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        height: 48px !important;
        cursor: pointer !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08)) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }
    
    .stButton > button {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
        height: 48px !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00D4AA, #00A88E) !important;
        border: none !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        height: 48px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #00E4BA, #00B89E) !important;
        transform: translateY(-2px) !important;
    }
    
    .stAlert {
        background-color: #1A1A1A !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderHeader {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    .stProgress > div > div > div > div {
        background-color: #00D4AA !important;
    }
    
    .stProgress > div > div {
        background-color: #1A1A1A !important;
    }
    
    a {
        color: #00D4AA !important;
    }
    
    hr {
        border-color: #333333 !important;
    }

    /* Force un fond sombre pour les iframes des components.html */
    iframe {
        background-color: #0A0A0A !important;
    }
</style>
""", unsafe_allow_html=True)

def custom_button(button_text, button_type="copy", url=None):
    """Bouton personnalisé identique pour copier et lien"""
    
    button_id = f"btn_{abs(hash(button_text + str(time.time()))) % 100000}"
    
    if button_type == "copy":
        onclick_action = f"copyText_{button_id}()"
    else:
        onclick_action = f"window.open('{url}', '_blank')"
    
    html = f"""
    <div style="width: 100%; height: 56px; background-color: #0A0A0A;">
        <button id="{button_id}" style="
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(10px);
            color: white;
            margin: 0;
            padding: 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            width: 100%;
            height: 48px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
        " onmouseover="this.style.background='linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08))'; this.style.transform='translateY(-2px)'" 
           onmouseout="this.style.background='linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))'; this.style.transform='translateY(0)'"
           onclick="{onclick_action}">
            {button_text}
        </button>
    </div>
    """
    
    components.html(html, height=56)

def copy_button(text_to_copy, button_text="Copier"):
    """Bouton copier avec gestion du texte"""
    
    button_id = f"btn_{abs(hash(text_to_copy)) % 100000}"
    text_escaped = json.dumps(text_to_copy)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #0A0A0A;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                overflow: visible;
            }}
        </style>
    </head>
    <body>
        <div style="width: 100%; height: 60px; background-color: #0A0A0A; margin: 0; padding: 4px 0; box-sizing: border-box; overflow: visible;">
            <button id="{button_id}" style="
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                backdrop-filter: blur(10px);
                color: white;
                margin: 0;
                padding: 0;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 500;
                width: 100%;
                height: 48px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
            " onmouseover="this.style.background='linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08))'; this.style.transform='translateY(-2px)'" 
               onmouseout="this.style.background='linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))'; this.style.transform='translateY(0)'"
               onclick="copy_{button_id}()">
                {button_text}
            </button>
        </div>
        
        <script>
        function copy_{button_id}() {{
            navigator.clipboard.writeText({text_escaped}).then(function() {{
                const btn = document.getElementById('{button_id}');
                btn.innerHTML = '✓ Copié';
                btn.style.background = 'linear-gradient(135deg, #00D4AA, #00A88E)';
                setTimeout(function() {{
                    btn.innerHTML = '{button_text}';
                    btn.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))';
                }}, 2000);
            }}).catch(function() {{
                alert('Erreur de copie');
            }});
        }}
        </script>
    </body>
    </html>
    """
    
    components.html(html, height=60)

def link_button(button_text, url):
    """Bouton lien avec style identique au bouton copier"""
    
    button_id = f"btn_{abs(hash(button_text + url)) % 100000}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #0A0A0A;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                overflow: visible;
            }}
        </style>
    </head>
    <body>
        <div style="width: 100%; height: 60px; background-color: #0A0A0A; margin: 0; padding: 4px 0; box-sizing: border-box; overflow: visible;">
            <button id="{button_id}" style="
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                backdrop-filter: blur(10px);
                color: white;
                margin: 0;
                padding: 0;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 500;
                width: 100%;
                height: 48px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
            " onmouseover="this.style.background='linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08))'; this.style.transform='translateY(-2px)'" 
               onmouseout="this.style.background='linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))'; this.style.transform='translateY(0)'"
               onclick="window.open('{url}', '_blank')">
                {button_text}
            </button>
        </div>
    </body>
    </html>
    """
    
    components.html(html, height=60)

def generate_pdf(transcription, interview_name, date, progress_bar=None):
    if progress_bar:
        progress_bar.progress(10, text="Initialisation...")
        time.sleep(0.15)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    if progress_bar:
        progress_bar.progress(30, text="Création des styles...")
        time.sleep(0.15)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=20, 
                                 textColor='#1f4788', spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold')
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, 
                                textColor='#666666', spaceAfter=4, fontName='Helvetica')
    content_style = ParagraphStyle('ContentStyle', parent=styles['Normal'], fontSize=11, 
                                   leading=14, alignment=TA_JUSTIFY, fontName='Helvetica', spaceAfter=8)
    footer_style = ParagraphStyle('FooterStyle', parent=styles['Normal'], fontSize=8, 
                                  textColor='#999999', alignment=TA_CENTER, fontName='Helvetica-Oblique')
    
    if progress_bar:
        progress_bar.progress(50, text="Construction du contenu...")
        time.sleep(0.15)
    
    story = []
    story.append(Paragraph("TRANSCRIPTION D'ENTRETIEN", title_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"<b>Nom de l'entretien :</b> {interview_name}", meta_style))
    story.append(Paragraph(f"<b>Date de l'entretien :</b> {date}", meta_style))
    story.append(Paragraph(f"<b>Date de création du document :</b> {datetime.now().strftime('%d/%m/%Y à %H:%M')}", meta_style))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("<b>TRANSCRIPTION INTÉGRALE</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))
    
    if progress_bar:
        progress_bar.progress(70, text="Formatage...")
        time.sleep(0.15)
    
    text_clean = transcription.replace('\n\n', ' ').replace('\n', ' ')
    story.append(Paragraph(text_clean, content_style))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("Document généré automatiquement", footer_style))
    
    if progress_bar:
        progress_bar.progress(90, text="Génération du PDF...")
        time.sleep(0.15)
    
    doc.build(story)
    buffer.seek(0)
    
    if progress_bar:
        progress_bar.progress(100, text="PDF créé")
        time.sleep(0.2)
    
    return buffer

def get_chatgpt_prompt():
    return """PROMPT PREMIUM – ANALYSE PROFESSIONNELLE D’ENTRETIEN (VERSION AVANCÉE ET COMPLÈTE)

Tu es un expert en analyse d’entretiens professionnels, spécialisé en ressources humaines, management, organisations et qualité de vie au travail.
Ton rôle est de produire une analyse professionnelle approfondie, structurée, nuancée, solide et contextualisée, à partir de la transcription complète d’un entretien individuel.

Je vais te fournir un verbatim d’entretien.
À partir de celui-ci, tu dois produire une analyse écrite complète comprenant des niveaux de lecture :

descriptif (faits issus de l’entretien)

analytique (interprétation RH et psychosociale)

managérial (enjeux organisationnels)

stratégique (fidélisation, engagement, risques)

Ton style doit être professionnel, structuré, concis, mais riche, comme dans un rapport RH élaboré.
Tu peux citer certains extraits du verbatim pour étayer tes analyses.

📌 STRUCTURE EXACTE À PRODUIRE (VERSION DÉTAILLÉE)
Titre : ANALYSE PROFESSIONNELLE – ENTRETIEN [NOM + FONCTION]
1. Contexte et présentation générale

Inclure systématiquement :

identité professionnelle (poste, ancienneté, unité)

âge si disponible

vision globale de la personne (posture, ton, dynamisme, préoccupations, maturité)

éléments clés qui ressortent immédiatement du verbatim

comment elle vit actuellement son poste

Objectif : dresser un portrait synthétique mais complet en 6–10 lignes.

2. Parcours et trajectoire professionnelle

Structure recommandée :

2.1. Formation et stages

décrire les différents terrains de stage

préciser ce que chaque expérience lui a apporté

montrer les cohérences / ruptures / apprentissages

2.2. Premiers postes et débuts professionnels

difficultés rencontrées

points marquants, positifs et négatifs

éléments qui expliquent ses choix actuels

2.3. Transition vers le poste actuel

motivations explicites

motivations implicites (analyser entre les lignes)

rôle du contexte personnel

cohérence entre parcours et service actuel

Objectif : expliquer le sens de sa trajectoire.

3. Facteurs de satisfaction et ressources au travail

Répartis en sous-thèmes, avec puces développées :

3.1. Environnement humain et esprit d’équipe

bienveillance

soutien perçu

entraide réelle ou symbolique

impact sur son bien-être

3.2. Développement professionnel, formation, apprentissage

formation continue

apprentissage quotidien

motivation à progresser

3.3. Sens du travail et relation patient

ce qui l’anime

sa posture soignante

valeurs professionnelles

⚠️ Développe chaque point en 2–3 phrases, pas juste des puces minimales.

4. Difficultés, vulnérabilités et facteurs de risque

Créer des sous-parties, comme :

4.1. Stress, adrénaline, charge mentale

anticipations anxieuses

situations critiques (CT, CIT…)

risques psychosociaux associés

peur de mal faire

4.2. Charge émotionnelle et empathie

difficultés face aux histoires de vie des patients

risques liés à l’hyper-empathie

stratégies de régulation actuelles

4.3. Relations d’équipe : intégration, tensions, mise à l’écart

dynamiques de groupe

vulnérabilité comme jeune diplômée

effets sur son engagement

4.4. Insécurité professionnelle liée à l’organisation médicale

stress lié à l’absence de médecin

sentiment d’être “entre deux chaises"

impact sur la prise en charge et la confiance professionnelle

Objectif : identifier clairement les risques de fragilisation.

5. Fidélisation : ce qui l’attache / ce qui pourrait l’éloigner
5.1. Facteurs d’attachement

Liste développée :

relations et ambiance

apprentissage continu

supervision / écoute

cohérence avec ses valeurs professionnelles

5.2. Risques de départ

Liste développée :

stress chronique

mise à l’écart persistante

manque de reconnaissance

manque de présence médicale

difficultés émotionnelles répétées

Objectif : fournir une lecture stratégique RH.

6. Enjeux managériaux repérables

Liste détaillée (format paragraphes courts ou puces développées) :

accueil et intégration des nouveaux

régulation des tensions et prévention du “bruit de couloir”

besoin de feedback structuré

prévention des risques psychosociaux

articulation équipe infirmière / présence médicale

maintien d’une culture collective bienveillante

7. Pistes d’action concrètes (priorisées)

Produire des actions opérationnelles et réalistes, par exemple :

7.1. Intégration et accompagnement

tuteur dédié

entretien de suivi à 3–6 mois

7.2. Espaces de parole

réactivation des analyses de pratiques

groupes de parole avec psychologue

7.3. Reconnaissance et feedback

entretiens réguliers

valorisation explicite des compétences

7.4. Gestion du stress et soutien émotionnel

formations ciblées

débriefings systématiques après CT/CIT

7.5. Organisation médicale

clarification des plages de présence médicale

meilleure communication auprès des équipes

8. Conclusion

3–5 phrases maximum :

portrait global

points forts

points de vigilance

enjeux clés pour la fidélisation

synthèse finale RH

🎯 CONSIGNES DE RÉDACTION

Analyse très professionnelle.

Style fluide, clair et structuré.

Niveau d’exigence : cabinet RH / psychologue du travail / consultant QVT.

Toujours citer certains extraits pertinents du verbatim (sans excès).

Expliciter les liens entre discours, besoins et enjeux organisationnels.

Aucune mention du prompt ou de la manière dont tu écris.

Aucun jugement moral.

Voici la transcription à analyser :

"""

# ========== INTERFACE ==========

st.title("Assistants Entretien")
st.markdown("### Transcription iPhone → Documents professionnels")
st.markdown("---")

st.markdown("### Informations de l'entretien")

col1, col2 = st.columns(2)
with col1:
    interview_name = st.text_input("Nom de l'entretien", placeholder="Ex: Entretien Charlotte - Infirmière")
with col2:
    interview_date = st.date_input("Date de l'entretien", datetime.now())

st.markdown("### Transcription")

transcription = st.text_area("Texte complet", height=350, placeholder="Collez ici la transcription...", label_visibility="collapsed")

if transcription:
    word_count = len(transcription.split())
    st.caption(f"{word_count:,} mots | ~{word_count//150} min estimées")

st.markdown("---")

button_disabled = not (transcription and interview_name)

generate_button = st.button("Générer le PDF", type="primary", use_container_width=True, disabled=button_disabled)

if generate_button and transcription and interview_name:
    progress_container = st.empty()
    
    with progress_container.container():
        progress_bar = st.progress(0, text="Démarrage...")
        pdf_buffer = generate_pdf(transcription, interview_name, interview_date.strftime('%d/%m/%Y'), progress_bar)
        
        st.session_state['pdf_buffer'] = pdf_buffer
        st.session_state['pdf_filename'] = f"transcription_{interview_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        st.session_state['generation_done'] = True
        st.session_state['saved_transcription'] = transcription
    
    progress_container.empty()
    st.success("PDF créé")
    time.sleep(0.5)
    st.rerun()

if st.session_state.get('generation_done', False):
    st.markdown("---")
    st.markdown("### Documents générés")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.download_button(
            "Télécharger PDF Transcription",
            st.session_state['pdf_buffer'], 
            st.session_state['pdf_filename'],
            mime="application/pdf",
            use_container_width=True
        )
    
    with col2:
        if st.button("Nouveau", use_container_width=True):
            for key in ['generation_done', 'pdf_buffer', 'pdf_filename', 'saved_transcription']:
                st.session_state.pop(key, None)
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Générer l'analyse ChatGPT")
    st.markdown("Copiez le prompt ci-dessous puis collez-le dans ChatGPT")
    
    with st.expander("Voir le prompt complet", expanded=False):
        saved_transcription = st.session_state.get('saved_transcription', '')
        full_text = get_chatgpt_prompt() + saved_transcription
        st.code(full_text, language=None)
    
    col1, col2 = st.columns(2)
    
    saved_transcription = st.session_state.get('saved_transcription', '')
    full_text = get_chatgpt_prompt() + saved_transcription
    
    with col1:
        copy_button(full_text, "Copier Prompt")
    
    with col2:
        link_button("Ouvrir ChatGPT", "https://chat.openai.com")
    
    st.markdown("<br><br>", unsafe_allow_html=True)

with st.expander("Fonctionnement de l'assistant"):
    st.markdown("""
    ### Guide d'utilisation
    
    **1. Collez la transcription**  
    Collez le texte de votre entretien dans la zone de texte.
    
    <br>
    
    **2. Remplissez les informations**  
    Indiquez le nom de l'entretien et la date.
    
    <br>
    
    **3. Générez le PDF de transcription**  
    Cliquez sur "Générer le PDF" puis téléchargez le document.
    
    <br>
    
    **4. Créez l'analyse ChatGPT**  
    Cliquez sur "Copier Prompt" puis sur "Ouvrir ChatGPT".  
    Collez le contenu copié dans ChatGPT pour obtenir l'analyse professionnelle.
    
    <br>
    
    **Résultat :** Deux documents professionnels (transcription + analyse professionnelle).
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Application locale | Données sécurisées")
