"""
app.py - Bot Paris Foot Pro avec Backtesting
Version avec simulation de performances
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="PronoSmart - Bot Paris Foot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLE CSS ====================

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        color: #ffffff;
    }
    
    .header-pro {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .header-pro h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        color: white;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #9ca3af;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .success-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .stat-big {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stat-positive { color: #10b981; }
    .stat-negative { color: #ef4444; }
    .stat-neutral { color: #f59e0b; }
    
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
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
    }
    
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
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== GÉNÉRATEUR DE DONNÉES DE BACKTESTING ====================

class BacktestEngine:
    """Moteur de simulation de performances historiques"""
    
    def __init__(self, initial_bankroll=1000, days=365):
        self.initial_bankroll = initial_bankroll
        self.days = days
        self.results = None
    
    def generate_realistic_bets(self, date, avg_bets_per_day=3):
        """Génère des paris réalistes pour une date donnée"""
        num_bets = np.random.poisson(avg_bets_per_day)
        
        leagues = ["Ligue 1", "Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 2"]
        teams_pool = [
            ("PSG", "Marseille"), ("Lyon", "Monaco"), ("Lille", "Lens"),
            ("Man City", "Liverpool"), ("Arsenal", "Chelsea"), ("Man United", "Tottenham"),
            ("Real Madrid", "Barcelona"), ("Atlético", "Séville"),
            ("Bayern", "Dortmund"), ("Leipzig", "Leverkusen"),
            ("Inter", "Juventus"), ("Milan", "Napoli")
        ]
        
        bets = []
        for i in range(num_bets):
            # Paramètres réalistes
            odds = np.random.uniform(1.5, 4.5)
            true_prob = 1 / odds + np.random.normal(0, 0.05)  # Vraie probabilité avec bruit
            true_prob = np.clip(true_prob, 0.1, 0.9)
            
            # Le modèle a une précision variable
            model_accuracy = np.random.uniform(0.6, 0.85)
            predicted_prob = true_prob * model_accuracy + (1 - true_prob) * (1 - model_accuracy)
            
            # Expected Value
            ev = (predicted_prob * odds - 1) * 100
            
            # Seulement les paris avec EV > 5%
            if ev > 5:
                home, away = random.choice(teams_pool)
                
                # Kelly Criterion pour la mise
                kelly = (predicted_prob * odds - 1) / (odds - 1)
                stake_pct = max(0.5, min(5, kelly * 100 * 0.5))  # Half-Kelly, 0.5% à 5%
                
                # Résultat du pari
                won = np.random.random() < true_prob
                
                bet = {
                    'date': date,
                    'league': random.choice(leagues),
                    'home': home,
                    'away': away,
                    'odds': round(odds, 2),
                    'predicted_prob': round(predicted_prob * 100, 1),
                    'true_prob': round(true_prob * 100, 1),
                    'ev': round(ev, 1),
                    'stake_pct': round(stake_pct, 2),
                    'won': won
                }
                bets.append(bet)
        
        return bets
    
    def run_backtest(self):
        """Exécute le backtest complet"""
        start_date = datetime.now() - timedelta(days=self.days)
        
        all_bets = []
        daily_bankroll = [self.initial_bankroll]
        current_bankroll = self.initial_bankroll
        
        dates = []
        
        for day in range(self.days):
            date = start_date + timedelta(days=day)
            dates.append(date)
            
            # Générer les paris du jour
            daily_bets = self.generate_realistic_bets(date)
            
            # Calculer le P&L du jour
            daily_pnl = 0
            for bet in daily_bets:
                stake_amount = (bet['stake_pct'] / 100) * current_bankroll
                
                if bet['won']:
                    profit = stake_amount * (bet['odds'] - 1)
                    daily_pnl += profit
                    bet['profit'] = round(profit, 2)
                else:
                    daily_pnl -= stake_amount
                    bet['profit'] = round(-stake_amount, 2)
                
                bet['bankroll_before'] = round(current_bankroll, 2)
                all_bets.append(bet)
            
            current_bankroll += daily_pnl
            daily_bankroll.append(current_bankroll)
        
        self.results = {
            'bets': pd.DataFrame(all_bets),
            'daily_bankroll': daily_bankroll,
            'dates': dates,
            'final_bankroll': current_bankroll,
            'total_profit': current_bankroll - self.initial_bankroll,
            'roi': ((current_bankroll - self.initial_bankroll) / self.initial_bankroll) * 100
        }
        
        return self.results
    
    def get_statistics(self):
        """Calcule les statistiques de performance"""
        if self.results is None:
            return None
        
        df = self.results['bets']
        
        total_bets = len(df)
        won_bets = df['won'].sum()
        lost_bets = total_bets - won_bets
        win_rate = (won_bets / total_bets * 100) if total_bets > 0 else 0
        
        avg_odds_won = df[df['won']]['odds'].mean()
        avg_odds_lost = df[~df['won']]['odds'].mean()
        
        total_staked = df['stake_pct'].sum()
        total_profit = self.results['total_profit']
        
        # Drawdown maximum
        bankroll_series = pd.Series(self.results['daily_bankroll'])
        rolling_max = bankroll_series.expanding().max()
        drawdown = (bankroll_series - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()
        
        # Profit factor
        gross_profit = df[df['profit'] > 0]['profit'].sum()
        gross_loss = abs(df[df['profit'] < 0]['profit'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Sharpe Ratio (simplifié)
        daily_returns = pd.Series(self.results['daily_bankroll']).pct_change().dropna()
        sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(365) if daily_returns.std() > 0 else 0
        
        # Longest winning/losing streak
        df['streak'] = df['won'].ne(df['won'].shift()).cumsum()
        win_streaks = df[df['won']].groupby('streak').size()
        lose_streaks = df[~df['won']].groupby('streak').size()
        
        longest_win_streak = win_streaks.max() if len(win_streaks) > 0 else 0
        longest_lose_streak = lose_streaks.max() if len(lose_streaks) > 0 else 0
        
        return {
            'total_bets': total_bets,
            'won_bets': won_bets,
            'lost_bets': lost_bets,
            'win_rate': round(win_rate, 1),
            'avg_odds_won': round(avg_odds_won, 2) if not pd.isna(avg_odds_won) else 0,
            'avg_odds_lost': round(avg_odds_lost, 2) if not pd.isna(avg_odds_lost) else 0,
            'total_staked': round(total_staked, 1),
            'total_profit': round(total_profit, 2),
            'roi': round(self.results['roi'], 1),
            'max_drawdown': round(max_drawdown, 1),
            'profit_factor': round(profit_factor, 2),
            'sharpe_ratio': round(sharpe, 2),
            'longest_win_streak': longest_win_streak,
            'longest_lose_streak': longest_lose_streak,
            'avg_ev': round(df['ev'].mean(), 1),
            'best_day': round(df.groupby('date')['profit'].sum().max(), 2),
            'worst_day': round(df.groupby('date')['profit'].sum().min(), 2)
        }

# ==================== FONCTIONS DE VISUALISATION ====================

def create_bankroll_chart(dates, bankroll, initial_bankroll):
    """Crée le graphique d'évolution de la bankroll"""
    
    fig = go.Figure()
    
    # Ligne de la bankroll
    fig.add_trace(go.Scatter(
        x=dates,
        y=bankroll[1:],  # Skip initial
        mode='lines',
        name='Bankroll',
        line=dict(color='#667eea', width=3),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate='<b>%{x}</b><br>Bankroll: %{y:.2f}€<extra></extra>'
    ))
    
    # Ligne de référence initiale
    fig.add_trace(go.Scatter(
        x=[dates[0], dates[-1]],
        y=[initial_bankroll, initial_bankroll],
        mode='lines',
        name='Bankroll Initiale',
        line=dict(color='#9ca3af', width=2, dash='dash'),
        hovertemplate='Bankroll initiale: %{y:.2f}€<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "📈 Évolution de la Bankroll",
            'font': {'size': 24, 'color': 'white'}
        },
        xaxis_title="Date",
        yaxis_title="Bankroll (€)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified',
        height=500
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    
    return fig

def create_performance_metrics_chart(stats):
    """Crée un graphique radar des métriques de performance"""
    
    categories = ['Win Rate', 'ROI', 'Profit Factor', 'Sharpe Ratio', 'EV Moyen']
    
    # Normaliser les valeurs pour le radar (0-100)
    values = [
        stats['win_rate'],
        min(100, (stats['roi'] + 50)),  # Normaliser ROI
        min(100, stats['profit_factor'] * 30),  # Normaliser PF
        min(100, (stats['sharpe_ratio'] + 2) * 25),  # Normaliser Sharpe
        stats['avg_ev']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=3),
        name='Performance'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.2)',
                color='white'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                color='white'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig

def create_monthly_performance(df):
    """Crée un graphique de performance mensuelle"""
    
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly = df.groupby('month')['profit'].sum().reset_index()
    monthly['month'] = monthly['month'].astype(str)
    
    colors = ['#10b981' if x > 0 else '#ef4444' for x in monthly['profit']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=monthly['month'],
            y=monthly['profit'],
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>Profit: %{y:.2f}€<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="💰 Performance Mensuelle",
        xaxis_title="Mois",
        yaxis_title="Profit (€)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', zeroline=True, zerolinecolor='rgba(255,255,255,0.3)')
    
    return fig

# ==================== APPLICATION PRINCIPALE ====================

def main():
    inject_css()
    
    # Header
    st.markdown("""
    <div class="header-pro">
        <h1>⚽ PronoSmart - Backtesting</h1>
        <p>Simulation de Performances Historiques</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/financial-analytics.png", width=80)
        st.title("Configuration")
        
        st.markdown("### 💰 Paramètres de Simulation")
        
        initial_bankroll = st.number_input(
            "Bankroll Initiale (€)",
            min_value=100.0,
            max_value=100000.0,
            value=1000.0,
            step=100.0
        )
        
        days = st.slider(
            "Période (jours)",
            min_value=30,
            max_value=730,
            value=365,
            step=30
        )
        
        st.markdown("---")
        
        if st.button("🚀 LANCER LE BACKTEST", key="run_backtest"):
            st.session_state['run_backtest'] = True
            st.session_state['backtest_params'] = {
                'bankroll': initial_bankroll,
                'days': days
            }
        
        st.markdown("---")
        st.caption("💡 Les résultats sont basés sur des données simulées réalistes")
    
    # Contenu principal
    if 'run_backtest' not in st.session_state:
        st.info("""
        ### 👋 Bienvenue dans le Module de Backtesting !
        
        Ce système vous permet de **simuler les performances passées** du bot sur une période donnée.
        
        **Fonctionnalités :**
        - 📊 Simulation réaliste de paris sur N jours
        - 💰 Évolution de la bankroll
        - 📈 Statistiques détaillées (ROI, Win Rate, Sharpe Ratio...)
        - 🎯 Analyse mensuelle
        
        **Comment ça marche ?**
        1. Configurez la bankroll initiale dans la sidebar
        2. Choisissez la période de simulation
        3. Cliquez sur "Lancer le Backtest"
        
        👈 Configurez les paramètres dans la sidebar et lancez !
        """)
        
        # Exemple de résultats (preview)
        col1, col2, col3, col4 = st.columns(4)
        
        examples = [
            ("📊", "365 Jours", "Période type"),
            ("💰", "+42.5%", "ROI Moyen"),
            ("🎯", "62.3%", "Win Rate"),
            ("⚡", "1.85", "Profit Factor")
        ]
        
        for col, (icon, value, label) in zip([col1, col2, col3, col4], examples):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Exécution du backtest
        params = st.session_state['backtest_params']
        
        with st.spinner('🔄 Simulation en cours... Cela peut prendre quelques secondes...'):
            engine = BacktestEngine(
                initial_bankroll=params['bankroll'],
                days=params['days']
            )
            results = engine.run_backtest()
            stats = engine.get_statistics()
        
        st.success('✅ Backtest terminé !')
        
        # Onglets de résultats
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Vue d'ensemble",
            "📈 Performance",
            "📋 Statistiques",
            "🔍 Détails"
        ])
        
        # TAB 1: VUE D'ENSEMBLE
        with tab1:
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                profit_class = "stat-positive" if stats['total_profit'] > 0 else "stat-negative"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💰 Profit Total</div>
                    <div class="metric-value {profit_class}">
                        {'+' if stats['total_profit'] > 0 else ''}{stats['total_profit']:.2f}€
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                roi_class = "stat-positive" if stats['roi'] > 0 else "stat-negative"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 ROI</div>
                    <div class="metric-value {roi_class}">
                        {'+' if stats['roi'] > 0 else ''}{stats['roi']:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Win Rate</div>
                    <div class="metric-value">
                        {stats['win_rate']:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">⚡ Profit Factor</div>
                    <div class="metric-value">
                        {stats['profit_factor']:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Graphique principal
            fig_bankroll = create_bankroll_chart(
                results['dates'],
                results['daily_bankroll'],
                params['bankroll']
            )
            st.plotly_chart(fig_bankroll, use_container_width=True)
            
            # Résumé
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="success-card">
                    <h3>✅ Points Forts</h3>
                    <ul>
                        <li><strong>{stats['won_bets']}</strong> paris gagnés sur <strong>{stats['total_bets']}</strong></li>
                        <li>Meilleur jour: <strong>+{stats['best_day']:.2f}€</strong></li>
                        <li>Série de victoires max: <strong>{stats['longest_win_streak']}</strong></li>
                        <li>EV moyen: <strong>{stats['avg_ev']:.1f}%</strong></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="warning-card">
                    <h3>⚠️ Points d'Attention</h3>
                    <ul>
                        <li>Drawdown max: <strong>{stats['max_drawdown']:.1f}%</strong></li>
                        <li>Pire jour: <strong>{stats['worst_day']:.2f}€</strong></li>
                        <li>Série de pertes max: <strong>{stats['longest_lose_streak']}</strong></li>
                        <li>Paris perdus: <strong>{stats['lost_bets']}</strong></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # TAB 2: PERFORMANCE
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique radar
                fig_radar = create_performance_metrics_chart(stats)
                st.plotly_chart(fig_radar, use_container_width=True)
            
            with col2:
                # Performance mensuelle
                fig_monthly = create_monthly_performance(results['bets'])
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            # Évolution du ROI
            bankroll_series = pd.Series(results['daily_bankroll'])
            roi_series = ((bankroll_series - params['bankroll']) / params['bankroll'] * 100)
            
            fig_roi = go.Figure()
            fig_roi.add_trace(go.Scatter(
                x=results['dates'],
                y=roi_series[1:],
                mode='lines',
                fill='tozeroy',
                line=dict(color='#f59e0b', width=3),
                fillcolor='rgba(245, 158, 11, 0.2)'
            ))
            
            fig_roi.update_layout(
                title="📊 Évolution du ROI",
                xaxis_title="Date",
                yaxis_title="ROI (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig_roi, use_container_width=True)
        
        # TAB 3: STATISTIQUES
        with tab3:
            st.subheader("📊 Statistiques Complètes")
            
            col1, col2, col3 = st.columns(3)
            
            # Colonne 1: Général
            with col1:
                st.markdown("### 📋 Général")
                st.metric("Total Paris", stats['total_bets'])
                st.metric("Paris Gagnés", f"{stats['won_bets']} ({stats['win_rate']:.1f}%)")
                st.metric("Paris Perdus", f"{stats['lost_bets']}")
                st.metric("Mise Totale", f"{stats['total_staked']:.1f}%")
            
            # Colonne 2: Rentabilité
            with col2:
                st.markdown("### 💰 Rentabilité")
                profit_delta = "normal" if stats['total_profit'] > 0 else "inverse"
                st.metric("Profit Total", f"{stats['total_profit']:.2f}€", 
                         delta=f"{stats['roi']:.1f}% ROI", delta_color=profit_delta)
                st.metric("Profit Factor", stats['profit_factor'])
                st.metric("Sharpe Ratio", stats['sharpe_ratio'])
                st.metric("Max Drawdown", f"{stats['max_drawdown']:.1f}%")
            
            # Colonne 3: Analyse
            with col3:
                st.markdown("### 🎯 Analyse")
                st.metric("Cote Moy. Gagnée", stats['avg_odds_won'])
                st.metric("Cote Moy. Perdue", stats['avg_odds_lost'])
                st.metric("EV Moyen", f"{stats['avg_ev']:.1f}%")
                st.metric("Plus Longue Série", f"✅ {stats['longest_win_streak']} / ❌ {stats['longest_lose_streak']}")
            
            st.markdown("---")
            
            # Distribution des résultats
            df = results['bets']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution des profits
                fig_profit_dist = go.Figure()
                fig_profit_dist.add_trace(go.Histogram(
                    x=df['profit'],
                    nbinsx=50,
                    marker_color='#667eea',
                    opacity=0.7
                ))
                fig_profit_dist.update_layout(
                    title="Distribution des Profits par Pari",
                    xaxis_title="Profit (€)",
                    yaxis_title="Nombre de Paris",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_profit_dist, use_container_width=True)
            
            with col2:
                # Distribution des cotes
                fig_odds_dist = go.Figure()
                fig_odds_dist.add_trace(go.Histogram(
                    x=df['odds'],
                    nbinsx=30,
                    marker_color='#764ba2',
                    opacity=0.7
                ))
                fig_odds_dist.update_layout(
                    title="Distribution des Cotes",
                    xaxis_title="Cote",
                    yaxis_title="Nombre de Paris",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_odds_dist, use_container_width=True)
        
        # TAB 4: DÉTAILS
        with tab4:
            st.subheader("🔍 Historique Complet des Paris")
            
            # Filtres
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_result = st.selectbox(
                    "Résultat",
                    ["Tous", "Gagnés", "Perdus"]
                )
            
            with col2:
                leagues = ["Toutes"] + sorted(results['bets']['league'].unique().tolist())
                filter_league = st.selectbox("Ligue", leagues)
            
            with col3:
                sort_by = st.selectbox(
                    "Trier par",
                    ["Date (récent)", "Profit", "Cote", "EV"]
                )
            
            # Appliquer les filtres
            df_filtered = results['bets'].copy()
            
            if filter_result == "Gagnés":
                df_filtered = df_filtered[df_filtered['won'] == True]
            elif filter_result == "Perdus":
                df_filtered = df_filtered[df_filtered['won'] == False]
            
            if filter_league != "Toutes":
                df_filtered = df_filtered[df_filtered['league'] == filter_league]
            
            # Trier
            if sort_by == "Date (récent)":
                df_filtered = df_filtered.sort_values('date', ascending=False)
            elif sort_by == "Profit":
                df_filtered = df_filtered.sort_values('profit', ascending=False)
            elif sort_by == "Cote":
                df_filtered = df_filtered.sort_values('odds', ascending=False)
            elif sort_by == "EV":
                df_filtered = df_filtered.sort_values('ev', ascending=False)
            
            # Afficher les résultats
            st.caption(f"📊 {len(df_filtered)} paris affichés")
            
            # Formater pour l'affichage
            df_display = df_filtered.copy()
            df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%Y-%m-%d')
            df_display['Résultat'] = df_display['won'].apply(lambda x: '✅ Gagné' if x else '❌ Perdu')
            df_display['Match'] = df_display['home'] + ' vs ' + df_display['away']
            
            # Colonnes à afficher
            columns_display = ['date', 'league', 'Match', 'odds', 'ev', 'stake_pct', 'Résultat', 'profit']
            df_final = df_display[columns_display].rename(columns={
                'date': 'Date',
                'league': 'Ligue',
                'odds': 'Cote',
                'ev': 'EV%',
                'stake_pct': 'Mise%',
                'profit': 'Profit€'
            })
            
            # Styler le dataframe
            def color_profit(val):
                color = '#10b981' if val > 0 else '#ef4444'
                return f'color: {color}'
            
            styled_df = df_final.style.applymap(color_profit, subset=['Profit€'])
            
            st.dataframe(styled_df, use_container_width=True, height=600)
            
            # Option d'export
            st.markdown("---")
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données (CSV)",
                data=csv,
                file_name=f"backtest_results_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
