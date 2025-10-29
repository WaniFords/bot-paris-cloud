"""
app.py - Bot Paris Foot Pro
Version Premium avec design professionnel
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="PronoSmart - Bot Paris Foot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLE CSS PROFESSIONNEL ====================

def inject_professional_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset et base */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #ffffff;
    }
    
    /* Header personnalisé */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Cartes premium */
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    .premium-card:hover::before {
        opacity: 1;
    }
    
    /* Score badge premium */
    .score-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .score-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .score-value {
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
        line-height: 1;
        margin: 0;
    }
    
    .score-label {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Cartes de paris améliorées */
    .bet-card-pro {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .bet-card-pro:hover {
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .bet-rank {
        position: absolute;
        top: -10px;
        right: 20px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.2rem;
        box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
    }
    
    .bet-teams {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    
    .bet-league {
        color: #9ca3af;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .bet-stats {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        flex: 1;
        min-width: 100px;
    }
    
    .stat-label {
        color: #9ca3af;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.25rem;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .stat-ev { color: #10b981; }
    .stat-odds { color: #f59e0b; }
    .stat-stake { color: #06b6d4; }
    .stat-proba { color: #8b5cf6; }
    
    /* Métriques améliorées */
    .metric-pro {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s;
    }
    
    .metric-pro:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: scale(1.05);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #9ca3af;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Boutons premium */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 1rem 2rem;
        border: none;
        border-radius: 12px;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animation de chargement */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #9ca3af;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #0a0e27 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Success/Error/Warning messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem; }
        .score-value { font-size: 3rem; }
        .bet-stats { flex-direction: column; gap: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== FONCTIONS UTILITAIRES ====================

def get_gradient_color(value, max_value=100):
    """Retourne une couleur en fonction de la valeur"""
    ratio = value / max_value
    if ratio >= 0.7:
        return "#10b981"  # Vert
    elif ratio >= 0.4:
        return "#f59e0b"  # Orange
    else:
        return "#ef4444"  # Rouge

def format_currency(value, bankroll=None):
    """Formate une valeur en pourcentage ou euros"""
    if bankroll:
        euros = (value / 100) * bankroll
        return f"{value:.2f}% ({euros:.2f}€)"
    return f"{value:.2f}%"

def create_performance_chart(data):
    """Crée un graphique de performance avancé"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(data))),
        y=data,
        mode='lines+markers',
        name='Performance',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10, color='#764ba2'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        title="Évolution de la Performance",
        xaxis_title="Jours",
        yaxis_title="Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    return fig

def create_stats_gauge(value, title):
    """Crée une jauge circulaire"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20, 'color': 'white'}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': "white"},
            'bar': {'color': "#667eea"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=300
    )
    
    return fig

# ==================== DONNÉES DE DÉMO ====================

def get_demo_bets():
    """Génère des paris de démonstration réalistes"""
    import random
    
    leagues = ["Ligue 1", "Premier League", "La Liga", "Bundesliga", "Serie A"]
    teams = [
        ("PSG", "Marseille"), ("Lyon", "Monaco"), ("Lille", "Nice"),
        ("Manchester City", "Liverpool"), ("Arsenal", "Chelsea"),
        ("Real Madrid", "Barcelona"), ("Atlético", "Séville"),
        ("Bayern Munich", "Dortmund"), ("Inter Milan", "Juventus")
    ]
    
    bets = []
    for i in range(8):
        home, away = random.choice(teams)
        bets.append({
            "rank": i + 1,
            "league": random.choice(leagues),
            "home": home,
            "away": away,
            "odds": round(random.uniform(1.5, 3.5), 2),
            "proba": round(random.uniform(45, 75), 1),
            "ev": round(random.uniform(5, 25), 1),
            "stake": round(random.uniform(1, 4), 2),
            "bookmaker": random.choice(["Winamax", "Betclic", "Unibet", "ParionsSport"])
        })
    
    return bets

# ==================== INTERFACE PRINCIPALE ====================

def main():
    inject_professional_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚽ PronoSmart</h1>
        <p>Intelligence Artificielle pour Paris Sportifs Professionnels</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/football2.png", width=80)
        st.title("Configuration")
        
        bankroll = st.number_input(
            "💰 Bankroll (€)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
            help="Votre capital disponible pour les paris"
        )
        
        st.markdown("---")
        
        auto_refresh = st.checkbox("🔄 Actualisation auto", value=False)
        show_details = st.checkbox("📊 Afficher détails", value=True)
        
        st.markdown("---")
        st.caption("Version Pro 2.0")
        st.caption("© 2024 PronoSmart")
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Dashboard", 
        "📊 Analyses", 
        "📈 Performance", 
        "⚙️ Paramètres"
    ])
    
    # ========== TAB 1: DASHBOARD ==========
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🚀 LANCER L'ANALYSE", key="analyze"):
                with st.spinner("🔍 Analyse en cours..."):
                    # Simulation
                    import time
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    st.session_state["bets"] = get_demo_bets()
                    st.session_state["score"] = 78.5
                    st.session_state["last_update"] = datetime.now()
                    
                    st.success("✅ Analyse terminée !")
                    st.balloons()
        
        with col2:
            if "last_update" in st.session_state:
                st.info(f"🕐 Dernière màj: {st.session_state['last_update'].strftime('%H:%M')}")
        
        st.markdown("---")
        
        # Score principal
        if "score" in st.session_state:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                score = st.session_state["score"]
                verdict = "EXCELLENT" if score >= 70 else "BON" if score >= 50 else "MOYEN"
                
                st.markdown(f"""
                <div class="score-display">
                    <div class="score-value">{score:.0f}</div>
                    <div class="score-label">{verdict}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Métriques
        if "bets" in st.session_state:
            bets = st.session_state["bets"]
            
            col1, col2, col3, col4 = st.columns(4)
            
            metrics = [
                ("📊", "Paris Trouvés", len(bets), ""),
                ("💎", "EV Moyen", f"{sum(b['ev'] for b in bets) / len(bets):.1f}", "%"),
                ("💰", "Mise Totale", f"{sum(b['stake'] for b in bets):.1f}", "%"),
                ("⚡", "ROI Potentiel", "+12.5", "%")
            ]
            
            for col, (icon, label, value, unit) in zip([col1, col2, col3, col4], metrics):
                with col:
                    st.markdown(f"""
                    <div class="metric-pro">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div class="metric-value">{value}{unit}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Liste des paris
            st.subheader("🎯 Paris Recommandés")
            
            for bet in bets[:5]:  # Top 5
                st.markdown(f"""
                <div class="bet-card-pro">
                    <div class="bet-rank">{bet['rank']}</div>
                    <div class="bet-league">{bet['league']}</div>
                    <div class="bet-teams">{bet['home']} vs {bet['away']}</div>
                    
                    <div class="bet-stats">
                        <div class="stat-item">
                            <div class="stat-label">Expected Value</div>
                            <div class="stat-value stat-ev">{bet['ev']:.1f}%</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Cote</div>
                            <div class="stat-value stat-odds">{bet['odds']:.2f}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Mise</div>
                            <div class="stat-value stat-stake">{format_currency(bet['stake'], bankroll)}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Probabilité</div>
                            <div class="stat-value stat-proba">{bet['proba']:.1f}%</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 1rem; color: #9ca3af; font-size: 0.85rem;">
                        📍 {bet['bookmaker']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("👆 Cliquez sur 'Lancer l'Analyse' pour commencer")
    
    # ========== TAB 2: ANALYSES ==========
    with tab2:
        st.subheader("📊 Analyses Détaillées")
        
        if "bets" in st.session_state:
            bets = st.session_state["bets"]
            df = pd.DataFrame(bets)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution des EV
                fig_ev = px.histogram(
                    df, 
                    x='ev', 
                    nbins=20,
                    title="Distribution des Expected Values",
                    labels={'ev': 'EV (%)', 'count': 'Nombre'},
                    color_discrete_sequence=['#667eea']
                )
                fig_ev.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_ev, use_container_width=True)
            
            with col2:
                # Distribution des cotes
                fig_odds = px.box(
                    df, 
                    y='odds',
                    title="Distribution des Cotes",
                    labels={'odds': 'Cote'},
                    color_discrete_sequence=['#764ba2']
                )
                fig_odds.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_odds, use_container_width=True)
            
            # Tableau détaillé
            st.markdown("### 📋 Tableau Complet")
            st.dataframe(
                df.style.background_gradient(subset=['ev'], cmap='RdYlGn'),
                use_container_width=True,
                hide_index=True
            )
        
        else:
            st.info("Lancez d'abord une analyse dans le Dashboard")
    
    # ========== TAB 3: PERFORMANCE ==========
    with tab3:
        st.subheader("📈 Suivi de Performance")
        
        # Simulation de données historiques
        import random
        perf_data = [random.randint(60, 90) for _ in range(30)]
        
        # Graphique principal
        fig = create_performance_chart(perf_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Jauges
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(create_stats_gauge(78, "Score Moyen"), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_stats_gauge(85, "Taux de Réussite"), use_container_width=True)
        
        with col3:
            st.plotly_chart(create_stats_gauge(92, "Fiabilité"), use_container_width=True)
    
    # ========== TAB 4: PARAMÈTRES ==========
    with tab4:
        st.subheader("⚙️ Configuration Avancée")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Stratégie")
            
            risk_level = st.select_slider(
                "Niveau de risque",
                options=["Très Prudent", "Prudent", "Équilibré", "Agressif", "Très Agressif"],
                value="Équilibré"
            )
            
            min_ev = st.slider("EV Minimum (%)", 0, 30, 10)
            max_stake = st.slider("Mise Maximum (%)", 1, 10, 5)
            
        with col2:
            st.markdown("### 📊 Filtres")
            
            min_odds = st.number_input("Cote Minimum", 1.0, 10.0, 1.5, 0.1)
            max_odds = st.number_input("Cote Maximum", 1.0, 20.0, 5.0, 0.5)
            
            selected_leagues = st.multiselect(
                "Ligues",
                ["Ligue 1", "Premier League", "La Liga", "Bundesliga", "Serie A"],
                default=["Ligue 1"]
            )
        
        if st.button("💾 Sauvegarder la Configuration"):
            st.success("✅ Configuration sauvegardée !")

if __name__ == "__main__":
    main()
