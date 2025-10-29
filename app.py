"""
app.py - Bot Paris Foot Pro avec Backtesting Avancé
Version avec comparaisons et objectifs de profit
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
    
    .comparison-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .winner-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-left: 1rem;
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
    
    .goal-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-left: 4px solid #6366f1;
        padding: 2rem;
        border-radius: 16px;
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
    
    .progress-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 30px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        transition: width 1s ease;
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

# ==================== MOTEUR DE BACKTESTING ====================

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
            odds = np.random.uniform(1.5, 4.5)
            true_prob = 1 / odds + np.random.normal(0, 0.05)
            true_prob = np.clip(true_prob, 0.1, 0.9)
            
            model_accuracy = np.random.uniform(0.6, 0.85)
            predicted_prob = true_prob * model_accuracy + (1 - true_prob) * (1 - model_accuracy)
            
            ev = (predicted_prob * odds - 1) * 100
            
            if ev > 5:
                home, away = random.choice(teams_pool)
                kelly = (predicted_prob * odds - 1) / (odds - 1)
                stake_pct = max(0.5, min(5, kelly * 100 * 0.5))
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
            
            daily_bets = self.generate_realistic_bets(date)
            
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
        
        bankroll_series = pd.Series(self.results['daily_bankroll'])
        rolling_max = bankroll_series.expanding().max()
        drawdown = (bankroll_series - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()
        
        gross_profit = df[df['profit'] > 0]['profit'].sum()
        gross_loss = abs(df[df['profit'] < 0]['profit'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        daily_returns = pd.Series(self.results['daily_bankroll']).pct_change().dropna()
        sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(365) if daily_returns.std() > 0 else 0
        
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

# ==================== COMPARAISON AVEC PLACEMENTS CLASSIQUES ====================

def calculate_investment_comparison(initial_amount, days):
    """
    Calcule l'évolution de placements classiques sur la même période
    """
    # Taux annuels moyens
    LIVRET_A_RATE = 0.03  # 3% par an (taux 2024)
    ACTIONS_RATE = 0.07   # 7% par an (moyenne historique CAC40)
    CRYPTO_RATE = 0.15    # 15% par an (très volatil, moyenne haussière)
    
    # Conversion en taux journalier
    daily_livret = (1 + LIVRET_A_RATE) ** (1/365) - 1
    daily_actions = (1 + ACTIONS_RATE) ** (1/365) - 1
    daily_crypto = (1 + CRYPTO_RATE) ** (1/365) - 1
    
    livret_values = [initial_amount]
    actions_values = [initial_amount]
    crypto_values = [initial_amount]
    
    for day in range(days):
        # Livret A (croissance linéaire)
        livret_values.append(livret_values[-1] * (1 + daily_livret))
        
        # Actions (croissance avec volatilité)
        volatility = np.random.normal(0, 0.01)  # 1% de volatilité journalière
        actions_values.append(actions_values[-1] * (1 + daily_actions + volatility))
        
        # Crypto (croissance avec forte volatilité)
        volatility_crypto = np.random.normal(0, 0.03)  # 3% de volatilité
        crypto_values.append(crypto_values[-1] * (1 + daily_crypto + volatility_crypto))
    
    return {
        'livret_a': livret_values,
        'actions': actions_values,
        'crypto': crypto_values,
        'livret_final': livret_values[-1],
        'actions_final': actions_values[-1],
        'crypto_final': crypto_values[-1],
        'livret_roi': ((livret_values[-1] - initial_amount) / initial_amount) * 100,
        'actions_roi': ((actions_values[-1] - initial_amount) / initial_amount) * 100,
        'crypto_roi': ((crypto_values[-1] - initial_amount) / initial_amount) * 100
    }

def create_comparison_chart(dates, bot_values, livret_values, actions_values, initial_amount):
    """Crée un graphique de comparaison des investissements"""
    
    fig = go.Figure()
    
    # Bot de paris
    fig.add_trace(go.Scatter(
        x=dates,
        y=bot_values[1:],
        mode='lines',
        name='🤖 Bot Paris Foot',
        line=dict(color='#667eea', width=4),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # Livret A
    fig.add_trace(go.Scatter(
        x=dates,
        y=livret_values[1:],
        mode='lines',
        name='🏦 Livret A (3%/an)',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    # Actions
    fig.add_trace(go.Scatter(
        x=dates,
        y=actions_values[1:],
        mode='lines',
        name='📈 Actions CAC40 (7%/an)',
        line=dict(color='#f59e0b', width=3, dash='dot')
    ))
    
    # Ligne de référence
    fig.add_trace(go.Scatter(
        x=[dates[0], dates[-1]],
        y=[initial_amount, initial_amount],
        mode='lines',
        name='Capital Initial',
        line=dict(color='#9ca3af', width=2, dash='dash'),
        showlegend=False
    ))
    
    fig.update_layout(
        title={
            'text': "💰 Comparaison: Bot vs Placements Classiques",
            'font': {'size': 24, 'color': 'white'}
        },
        xaxis_title="Date",
        yaxis_title="Valeur du Capital (€)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    
    return fig

# ==================== CALCUL D'OBJECTIFS ====================

def calculate_doubling_time(roi_annual):
    """
    Calcule le temps pour doubler la bankroll
    Utilise la règle de 72 et le ROI annuel
    """
    if roi_annual <= 0:
        return None
    
    # Règle de 72
    years = 72 / roi_annual
    days = years * 365
    months = years * 12
    
    return {
        'days': int(days),
        'months': round(months, 1),
        'years': round(years, 1)
    }

def calculate_growth_projection(initial_amount, roi_annual, target_multiplier=2):
    """
    Projette la croissance future et calcule quand l'objectif sera atteint
    """
    if roi_annual <= 0:
        return None
    
    daily_rate = (1 + roi_annual/100) ** (1/365) - 1
    
    current = initial_amount
    days = 0
    projection = [initial_amount]
    
    # Calculer jusqu'à atteindre l'objectif (max 5 ans)
    target = initial_amount * target_multiplier
    max_days = 365 * 5
    
    while current < target and days < max_days:
        current *= (1 + daily_rate)
        projection.append(current)
        days += 1
    
    return {
        'days_to_target': days if current >= target else None,
        'projection': projection,
        'achieved': current >= target
    }

def create_goal_progress_chart(current, target, days_elapsed, days_estimated):
    """Crée un graphique de progression vers l'objectif"""
    
    progress_pct = min(100, (current / target) * 100)
    
    fig = go.Figure()
    
    # Barre de progression
    fig.add_trace(go.Bar(
        x=[progress_pct],
        y=['Progression'],
        orientation='h',
        marker=dict(
            color='#667eea',
            line=dict(color='#764ba2', width=2)
        ),
        text=f'{progress_pct:.1f}%',
        textposition='inside',
        textfont=dict(size=20, color='white'),
        hovertemplate=f'<b>{progress_pct:.1f}%</b> de l\'objectif<extra></extra>'
    ))
    
    fig.update_layout(
        title="🎯 Progression vers l'Objectif de Doublement",
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=150,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig

# ==================== INTERFACE PRINCIPALE ====================

def main():
    inject_css()
    
    # Header
    st.markdown("""
    <div class="header-pro">
        <h1>⚽ PronoSmart - Backtesting Avancé</h1>
        <p>Simulation, Comparaisons & Objectifs de Profit</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/financial-analytics.png", width=80)
        st.title("Configuration")
        
        st.markdown("### 💰 Paramètres")
        
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
        st.markdown("### 🎯 Objectif")
        
        target_multiplier = st.selectbox(
            "Multiplier la bankroll par :",
            [2, 3, 5, 10],
            index=0,
            format_func=lambda x: f"×{x} ({initial_bankroll * x:.0f}€)"
        )
        
        st.markdown("---")
        
        if st.button("🚀 LANCER LE BACKTEST", key="run_backtest"):
            st.session_state['run_backtest'] = True
            st.session_state['backtest_params'] = {
                'bankroll': initial_bankroll,
                'days': days,
                'target_multiplier': target_multiplier
            }
        
        st.markdown("---")
        st.caption("💡 Simulation avec données réalistes")
    
    # Contenu principal
    if 'run_backtest' not in st.session_state:
        # Page d'accueil
        st.info("""
        ### 👋 Module de Backtesting Professionnel
        
        **Nouvelles fonctionnalités :**
        
        💰 **Comparaison avec placements classiques**
        - Livret A (3%/an)
        - Actions CAC40 (7%/an)
        - Voyez la différence avec le bot !
        
        🎯 **Objectifs de profit**
        - Calculez le temps pour doubler votre bankroll
        - Projections de croissance
        - Timeline précise
        
        👈 Configurez vos paramètres et lancez le backtest !
        """)
        
        # Métriques d'exemple
        col1, col2, col3, col4 = st.columns(4)
        
        examples = [
            ("🤖", "+42.5%", "ROI Bot"),
            ("🏦", "+3.0%", "Livret A"),
            ("📈", "+7.0%", "Actions"),
            ("🎯", "1.7 ans", "Pour doubler")
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
        
        with st.spinner('🔄 Simulation en cours...'):
            # Backtest du bot
            engine = BacktestEngine(
                initial_bankroll=params['bankroll'],
                days=params['days']
            )
            results = engine.run_backtest()
            stats = engine.get_statistics()
            
            # Comparaison avec placements classiques
            comparison = calculate_investment_comparison(
                params['bankroll'],
                params['days']
            )
            
            # Calcul des objectifs
            roi_annual = (stats['roi'] / params['days']) * 365
            doubling_time = calculate_doubling_time(roi_annual)
            projection = calculate_growth_projection(
                params['bankroll'],
                roi_annual,
                params['target_multiplier']
            )
        
        st.success('✅ Simulation terminée !')
        
        # Onglets
        tab1, tab2, tab3, tab4 = st.tabs([
            "💰 Comparaisons",
            "🎯 Objectifs",
            "📊 Vue d'ensemble",
            "📋 Statistiques"
        ])
        
        # ========== TAB 1: COMPARAISONS ==========
        with tab1:
            st.subheader("💰 Bot vs Placements Classiques")
            
            # Graphique de comparaison
            fig_comparison = create_comparison_chart(
                results['dates'],
                results['daily_bankroll'],
                comparison['livret_a'],
                comparison['actions'],
                params['bankroll']
            )
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            st.markdown("---")
            
            # Tableau comparatif
            st.markdown("### 📊 Résultats sur {} jours".format(params['days']))
            
            # Créer 3 colonnes pour les comparaisons
            col1, col2, col3 = st.columns(3)
            
            placements = [
                {
                    'name': '🤖 Bot Paris Foot',
                    'final': results['final_bankroll'],
                    'profit': stats['total_profit'],
                    'roi': stats['roi'],
                    'col': col1,
                    'color': '#667eea'
                },
                {
                    'name': '🏦 Livret A',
                    'final': comparison['livret_final'],
                    'profit': comparison['livret_final'] - params['bankroll'],
                    'roi': comparison['livret_roi'],
                    'col': col2,
                    'color': '#10b981'
                },
                {
                    'name': '📈 Actions CAC40',
                    'final': comparison['actions_final'],
                    'profit': comparison['actions_final'] - params['bankroll'],
                    'roi': comparison['actions_roi'],
                    'col': col3,
                    'color': '#f59e0b'
                }
            ]
            
            # Déterminer le gagnant
            winner = max(placements, key=lambda x: x['roi'])
            
            for placement in placements:
                with placement['col']:
                    is_winner = placement['name'] == winner['name']
                    
                    st.markdown(f"""
                    <div class="comparison-card">
                        <h3>{placement['name']}
                        {' <span class="winner-badge">🏆 GAGNANT</span>' if is_winner else ''}
                        </h3>
                        <div style="margin: 1.5rem 0;">
                            <div style="color: #9ca3af; font-size: 0.9rem;">Capital Final</div>
                            <div style="font-size: 2.5rem; font-weight: 800; color: {placement['color']};">
                                {placement['final']:.2f}€
                            </div>
                        </div>
                        <div style="margin: 1rem 0;">
                            <div style="color: #9ca3af; font-size: 0.9rem;">Profit</div>
                            <div style="font-size: 1.8rem; font-weight: 700; color: {'#10b981' if placement['profit'] > 0 else '#ef4444'};">
                                {'+' if placement['profit'] > 0 else ''}{placement['profit']:.2f}€
                            </div>
                        </div>
                        <div>
                            <div style="color: #9ca3af; font-size: 0.9rem;">ROI</div>
                            <div style="font-size: 1.5rem; font-weight: 700; color: {placement['color']};">
                                {'+' if placement['roi'] > 0 else ''}{placement['roi']:.1f}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Analyse comparative
            bot_vs_livret = stats['roi'] - comparison['livret_roi']
            bot_vs_actions = stats['roi'] - comparison['actions_roi']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="success-card">
                    <h3>🎯 Performance Relative</h3>
                    <ul>
                        <li><strong>{'+' if bot_vs_livret > 0 else ''}{bot_vs_livret:.1f}%</strong> vs Livret A</li>
                        <li><strong>{'+' if bot_vs_actions > 0 else ''}{bot_vs_actions:.1f}%</strong> vs Actions</li>
                        <li>Soit <strong>{abs(stats['total_profit'] - (comparison['livret_final'] - params['bankroll'])):.2f}€</strong> de plus que le Livret A</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Projection sur 5 ans
                roi_annual = (stats['roi'] / params['days']) * 365
                
                projection_5y_bot = params['bankroll'] * ((1 + roi_annual/100) ** 5)
                projection_5y_livret = params['bankroll'] * ((1 + 0.03) ** 5)
                projection_5y_actions = params['bankroll'] * ((1 + 0.07) ** 5)
                
                st.markdown(f"""
                <div class="warning-card">
                    <h3>🔮 Projection sur 5 ans</h3>
                    <ul>
                        <li>Bot: <strong>{projection_5y_bot:.2f}€</strong></li>
                        <li>Livret A: <strong>{projection_5y_livret:.2f}€</strong></li>
                        <li>Actions: <strong>{projection_5y_actions:.2f}€</strong></li>
                        <li>Différence: <strong>+{(projection_5y_bot - projection_5y_livret):.2f}€</strong></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # ========== TAB 2: OBJECTIFS ==========
        with tab2:
            st.subheader(f"🎯 Objectif : Multiplier par {params['target_multiplier']}")
            
            target_amount = params['bankroll'] * params['target_multiplier']
            current_amount = results['final_bankroll']
            
            # Progression actuelle
            progress = min(100, (current_amount / target_amount) * 100)
            
            st.markdown(f"""
            <div class="goal-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h3 style="margin: 0;">De {params['bankroll']:.0f}€ à {target_amount:.0f}€</h3>
                        <p style="color: #9ca3af; margin: 0.5rem 0;">Capital actuel: <strong>{current_amount:.2f}€</strong></p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 3rem; font-weight: 900; color: #6366f1;">
                            {progress:.0f}%
                        </div>
                    </div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%;">
                        {progress:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Calculs temporels
            if doubling_time:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">⏱️ Temps pour doubler</div>
                        <div class="metric-value">{doubling_time['months']:.1f}</div>
                        <div class="metric-label">Mois</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📅 Soit en jours</div>
                        <div class="metric-value">{doubling_time['days']}</div>
                        <div class="metric-label">Jours</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">🗓️ Ou en années</div>
                        <div class="metric-value">{doubling_time['years']:.1f}</div>
                        <div class="metric-label">Années</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Timeline de progression
            if projection and projection['achieved']:
                target_date = datetime.now() + timedelta(days=projection['days_to_target'])
                
                st.markdown(f"""
                <div class="success-card">
                    <h3>✅ Objectif Atteignable !</h3>
                    <p style="font-size: 1.2rem;">
                        Au rythme actuel, vous atteindrez <strong>{target_amount:.0f}€</strong> 
                        dans environ <strong>{projection['days_to_target']} jours</strong>
                    </p>
                    <p style="color: #9ca3af;">
                        Date estimée : <strong>{target_date.strftime('%d %B %Y')}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Graphique de projection
                projection_dates = [datetime.now() + timedelta(days=i) for i in range(len(projection['projection']))]
                
                fig_proj = go.Figure()
                
                fig_proj.add_trace(go.Scatter(
                    x=projection_dates,
                    y=projection['projection'],
                    mode='lines',
                    name='Projection',
                    line=dict(color='#667eea', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(102, 126, 234, 0.2)'
                ))
                
                # Ligne objectif
                fig_proj.add_trace(go.Scatter(
                    x=[projection_dates[0], projection_dates[-1]],
                    y=[target_amount, target_amount],
                    mode='lines',
                    name='Objectif',
                    line=dict(color='#10b981', width=3, dash='dash')
                ))
                
                fig_proj.update_layout(
                    title="🚀 Projection de Croissance vers l'Objectif",
                    xaxis_title="Date",
                    yaxis_title="Bankroll (€)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig_proj, use_container_width=True)
            
            else:
                st.markdown(f"""
                <div class="warning-card">
                    <h3>⚠️ Objectif Ambitieux</h3>
                    <p style="font-size: 1.1rem;">
                        Au rythme actuel, l'objectif de <strong>{target_amount:.0f}€</strong> 
                        nécessite plus de 5 ans.
                    </p>
                    <p style="color: #9ca3af;">
                        💡 Conseil : Réduisez l'objectif ou augmentez la performance du bot
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Simulation par paliers
            st.markdown("### 📊 Paliers de Croissance")
            
            milestones = [
                (1.5, "×1.5"),
                (2, "×2"),
                (3, "×3"),
                (5, "×5"),
                (10, "×10")
            ]
            
            milestone_data = []
            for mult, label in milestones:
                target = params['bankroll'] * mult
                if doubling_time:
                    # Estimation basée sur le ROI annuel
                    roi_annual = (stats['roi'] / params['days']) * 365
                    if roi_annual > 0:
                        years_needed = np.log(mult) / np.log(1 + roi_annual/100)
                        months_needed = years_needed * 12
                    else:
                        months_needed = float('inf')
                else:
                    months_needed = float('inf')
                
                milestone_data.append({
                    'Objectif': label,
                    'Montant': f"{target:.0f}€",
                    'Temps estimé': f"{months_needed:.1f} mois" if months_needed < 120 else "10+ ans",
                    'Réaliste': '✅' if months_needed < 36 else '⚠️' if months_needed < 60 else '❌'
                })
            
            df_milestones = pd.DataFrame(milestone_data)
            st.dataframe(df_milestones, use_container_width=True, hide_index=True)
        
        # ========== TAB 3: VUE D'ENSEMBLE ==========
        with tab3:
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
            
            # Graphique d'évolution de la bankroll
            fig_bankroll = go.Figure()
            
            fig_bankroll.add_trace(go.Scatter(
                x=results['dates'],
                y=results['daily_bankroll'][1:],
                mode='lines',
                name='Bankroll',
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            
            fig_bankroll.add_trace(go.Scatter(
                x=[results['dates'][0], results['dates'][-1]],
                y=[params['bankroll'], params['bankroll']],
                mode='lines',
                name='Bankroll Initiale',
                line=dict(color='#9ca3af', width=2, dash='dash')
            ))
            
            fig_bankroll.update_layout(
                title="📈 Évolution de la Bankroll",
                xaxis_title="Date",
                yaxis_title="Bankroll (€)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig_bankroll, use_container_width=True)
        
        # ========== TAB 4: STATISTIQUES ==========
        with tab4:
            st.subheader("📊 Statistiques Détaillées")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 📋 Général")
                st.metric("Total Paris", stats['total_bets'])
                st.metric("Paris Gagnés", f"{stats['won_bets']} ({stats['win_rate']:.1f}%)")
                st.metric("Paris Perdus", stats['lost_bets'])
            
            with col2:
                st.markdown("### 💰 Rentabilité")
                st.metric("ROI", f"{stats['roi']:.1f}%")
                st.metric("Profit Factor", stats['profit_factor'])
                st.metric("Sharpe Ratio", stats['sharpe_ratio'])
            
            with col3:
                st.markdown("### 🎯 Performance")
                st.metric("EV Moyen", f"{stats['avg_ev']:.1f}%")
                st.metric("Max Drawdown", f"{stats['max_drawdown']:.1f}%")
                st.metric("Plus Longue Série", f"✅ {stats['longest_win_streak']}")

if __name__ == "__main__":
    main()
