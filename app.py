"""
app.py - Bot Paris Foot Cloud
Version mobile simplifiée
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import os

# Configuration de la page
st.set_page_config(
    page_title="Bot Paris ⚽",
    page_icon="⚽",
    layout="wide"
)

# Style CSS
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: white;}
    .big-score {
        background: linear-gradient(135deg, #00c853 0%, #00e676 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: white;
        margin: 20px 0;
    }
    .bet-card {
        background: #1e2329;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 4px solid #ff3366;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff3366, #ff5577);
        color: white;
        font-size: 18px;
        padding: 15px;
        border: none;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Titre
st.title("⚽ Bot Paris Foot")
st.caption("Votre assistant de pronostics - Version Cloud")

# Fonction pour récupérer les matchs (API gratuite)
def get_matches():
    """Récupère les matchs du jour"""
    try:
        # API gratuite de football-data.org (pas besoin de clé pour démarrer)
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": st.secrets.get("FOOTBALL_API_KEY", "demo")}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("matches", [])
        else:
            return []
    except Exception as e:
        st.error(f"Erreur API: {e}")
        return []

# Fonction d'analyse simple
def analyze_match(match):
    """Analyse un match et retourne un pari potentiel"""
    home_team = match.get("homeTeam", {}).get("name", "Équipe 1")
    away_team = match.get("awayTeam", {}).get("name", "Équipe 2")
    competition = match.get("competition", {}).get("name", "Ligue")
    
    # Simulation simple (remplacez par votre logique ML)
    import random
    
    if random.random() > 0.7:  # 30% de matchs sélectionnés
        return {
            "rank": 1,
            "home": home_team,
            "away": away_team,
            "league": competition,
            "cote": round(random.uniform(1.5, 3.5), 2),
            "proba": round(random.uniform(50, 75), 1),
            "ev": round(random.uniform(5, 20), 1),
            "mise": round(random.uniform(1, 3), 2)
        }
    return None

# Interface principale
tab1, tab2, tab3 = st.tabs(["🏠 Aujourd'hui", "📊 Stats", "⚙️ Config"])

with tab1:
    st.header("Paris du Jour")
    
    # Bouton pour lancer l'analyse
    if st.button("🚀 ANALYSER LES MATCHS", key="analyze"):
        with st.spinner("🔍 Analyse en cours..."):
            matches = get_matches()
            
            if matches:
                bets = []
                for match in matches[:20]:  # Limiter à 20 matchs
                    bet = analyze_match(match)
                    if bet:
                        bets.append(bet)
                
                # Sauvegarder dans session state
                st.session_state["bets"] = bets
                st.session_state["last_run"] = datetime.now().strftime("%H:%M")
                
                st.success(f"✅ Analyse terminée ! {len(bets)} paris trouvés")
            else:
                st.warning("⚠️ Aucun match disponible pour le moment")
                # Données de démo
                st.session_state["bets"] = [
                    {
                        "rank": 1,
                        "home": "PSG",
                        "away": "Marseille",
                        "league": "Ligue 1",
                        "cote": 1.85,
                        "proba": 65.5,
                        "ev": 12.3,
                        "mise": 2.5
                    },
                    {
                        "rank": 2,
                        "home": "Lyon",
                        "away": "Monaco",
                        "league": "Ligue 1",
                        "cote": 2.10,
                        "proba": 58.2,
                        "ev": 8.7,
                        "mise": 1.8
                    }
                ]
    
    # Afficher les résultats
    if "bets" in st.session_state and st.session_state["bets"]:
        bets = st.session_state["bets"]
        
        # Score global
        avg_ev = sum(b["ev"] for b in bets) / len(bets)
        score = min(100, int(avg_ev * 5))
        
        st.markdown(f"""
        <div class="big-score">
            {score}/100
            <br><small style="font-size: 20px;">
                {"EXCELLENT" if score >= 70 else "BON" if score >= 50 else "MOYEN"}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistiques rapides
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Paris", len(bets))
        with col2:
            st.metric("💎 EV Moyen", f"{avg_ev:.1f}%")
        with col3:
            total_stake = sum(b["mise"] for b in bets)
            st.metric("💰 Mise Totale", f"{total_stake:.1f}%")
        
        st.markdown("---")
        
        # Liste des paris
        st.subheader(f"🏆 Top {len(bets)} Paris")
        
        for i, bet in enumerate(bets, 1):
            st.markdown(f"""
            <div class="bet-card">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <div style="color: #ff3366; font-weight: bold;">
                            #{i} • {bet['league']}
                        </div>
                        <div style="font-size: 18px; font-weight: bold; margin: 5px 0;">
                            {bet['home']} vs {bet['away']}
                        </div>
                        <div style="color: #aaa; font-size: 14px;">
                            Cote: {bet['cote']} • Proba: {bet['proba']}%
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #00e676; font-size: 24px; font-weight: bold;">
                            EV: {bet['ev']}%
                        </div>
                        <div style="color: #ffc400; font-size: 16px;">
                            Mise: {bet['mise']}%
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if "last_run" in st.session_state:
            st.caption(f"Dernière analyse : {st.session_state['last_run']}")
    
    else:
        st.info("👆 Cliquez sur le bouton pour analyser les matchs du jour")

with tab2:
    st.header("📊 Statistiques")
    
    if "bets" in st.session_state and st.session_state["bets"]:
        bets = st.session_state["bets"]
        df = pd.DataFrame(bets)
        
        # Graphique
        import plotly.express as px
        fig = px.bar(df, x="rank", y="ev", 
                     title="Expected Value par Pari",
                     labels={"ev": "EV (%)", "rank": "Rang"})
        fig.update_layout(
            plot_bgcolor="#1e2329",
            paper_bgcolor="#0e1117",
            font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible. Lancez une analyse d'abord.")

with tab3:
    st.header("⚙️ Configuration")
    
    bankroll = st.number_input(
        "💰 Votre Bankroll (€)",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )
    
    if bankroll > 0 and "bets" in st.session_state:
        st.success(f"Bankroll configurée : {bankroll}€")
        
        # Conversion des mises
        st.subheader("💵 Mises en Euros")
        for bet in st.session_state["bets"]:
            euros = (bet["mise"] / 100) * bankroll
            st.write(f"**{bet['home']} vs {bet['away']}** : {bet['mise']}% = **{euros:.2f}€**")
    
    st.markdown("---")
    
    st.info("""
    **ℹ️ À propos**
    
    Cette application cloud vous permet d'analyser les matchs de football 
    et de trouver des value bets depuis n'importe où !
    
    - 🌍 Accessible 24/7
    - 📱 Optimisé mobile
    - 🆓 Gratuit
    
    Version 1.0 - Hébergée sur Streamlit Cloud
    """)
    
    st.caption(f"Dernière mise à jour : {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Footer
st.markdown("---")
st.caption("🔒 Application sécurisée • Données en temps réel")