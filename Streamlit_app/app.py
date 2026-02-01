import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils import *
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="CSX Quant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Minimalist Design System
st.markdown("""
<style>
    /* Global Font & Data */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    
    /* Backgrounds */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.02em;
        color: #0f172a;
    }
    
    .main-title {
        font-size: 2.25rem;
        font-weight: 600;
        margin-bottom: 2rem;
        color: #0f172a;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 1rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #334155;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .card-metric {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Custom Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Metric styling fix for standard streamlit metrics */
    div[data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# Helper for consistent charts
def style_chart(fig, title="", height=450):
    fig.update_layout(
        template="plotly_white",
        title={
            'text': title,
            'y':0.95,
            'x':0,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': dict(family="Inter", size=18, color="#0f172a")
        },
        font=dict(family="Inter", color="#64748b"),
        hovermode='x unified',
        height=height,
        margin=dict(t=80, l=40, r=40, b=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# Define tickers
tickers = ['ABC', 'CGSM', 'GTI', 'MJQE', 'PAS', 'PEPC', 'PPAP', 'PPSP', 'PWSA']

# Load and preprocess data
@st.cache_data
def load_and_prepare_data():
    """Load and prepare all data"""
    prices = load_csx_data_from_excel(tickers)
    
    if prices is None:
        return None
    
    raw_returns = prices.pct_change().dropna()
    clean_returns = treat_outliers(raw_returns)
    
    split_date = '2025-04-30'
    train_returns = clean_returns[clean_returns.index <= split_date]
    test_returns = clean_returns[clean_returns.index > split_date]
    
    mu_train = train_returns.mean() * 252
    Sigma_train = train_returns.cov() * 252
    
    annual_returns = train_returns.mean() * 252
    annual_volatility = train_returns.std() * np.sqrt(252)
    
    return {
        'prices': prices,
        'raw_returns': raw_returns,
        'clean_returns': clean_returns,
        'train_returns': train_returns,
        'test_returns': test_returns,
        'mu_train': mu_train,
        'Sigma_train': Sigma_train,
        'annual_returns': annual_returns,
        'annual_volatility': annual_volatility
    }

# Initialize data
with st.spinner("Initializing CSX Quant Engine..."):
    data = load_and_prepare_data()

if data is None:
    st.error("Engine failure. Data could not be loaded.")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown('<h3 style="margin-left: 10px; margin-bottom: 20px;">CSX Quant</h3>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Dashboard", "Data Analysis", "Optimization", "Backtest", "Sensitivities"],
        label_visibility="collapsed"
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("CSX Portfolio Optimization v2.0")

# ==================== PAGE 1: DASHBOARD (Executive Summary) ====================
if page == "Dashboard":
    st.markdown('<h1 class="main-title">Executive Overview</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This platform provides institutional-grade portfolio optimization for the Cambodia Securities Exchange (CSX).
    Utilizing Markowitz Mean-Variance optimization to construct efficient portfolios.
    """)
    
    st.markdown("### Key Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="card-metric">
            <div class="metric-label">Universe</div>
            <div class="metric-value">{len(tickers)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="card-metric">
            <div class="metric-label">Observations</div>
            <div class="metric-value">{len(data['prices'])}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        train_len = len(data['train_returns'])
        st.markdown(f'''
        <div class="card-metric">
            <div class="metric-label">Training Set</div>
            <div class="metric-value">{train_len}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        test_len = len(data['test_returns'])
        st.markdown(f'''
        <div class="card-metric">
            <div class="metric-label">Test Set</div>
            <div class="metric-value">{test_len}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">Asset Universe Profile</h3>', unsafe_allow_html=True)
    
    asset_df = pd.DataFrame({
        'Ticker': tickers,
        'Annual Return': (data['annual_returns'] * 100),
        'Annual Volatility': (data['annual_volatility'] * 100)
    })
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(
            asset_df.style.format({
                'Annual Return': '{:.2f}%',
                'Annual Volatility': '{:.2f}%'
            }).background_gradient(cmap='Blues', subset=['Annual Return']),
            use_container_width=True,
            height=400
        )
        
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=asset_df['Annual Volatility'],
            y=asset_df['Annual Return'],
            mode='markers+text',
            text=asset_df['Ticker'],
            textposition="top center",
            marker=dict(size=12, color='#3b82f6', line=dict(width=1, color='white'))
        ))
        fig = style_chart(fig, "Risk-Return Profile", height=400)
        fig.update_layout(xaxis_title="Volatility %", yaxis_title="Return %")
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE 2: DATA EXPLORER & EDA ====================
elif page == "Data Analysis":
    st.markdown('<h1 class="main-title">Data Analysis</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Price History", "Distributions", "Correlations"])
    
    with tab1:
        selected_tickers = st.multiselect("Select Assets", tickers, default=tickers[:3])
        if selected_tickers:
            normalized = (data['prices'][selected_tickers] / data['prices'][selected_tickers].iloc[0]) * 100
            fig = go.Figure()
            # Professional slate/blue palette
            colors = ['#0f172a', '#334155', '#475569', '#64748b', '#94a3b8', '#cbd5e1']
            for i, ticker in enumerate(selected_tickers):
                fig.add_trace(go.Scatter(
                    x=normalized.index, y=normalized[ticker],
                    mode='lines', name=ticker,
                    line=dict(width=2, color=colors[i % len(colors)])
                ))
            fig = style_chart(fig, "Normalized Performance (Base=100)")
            st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
             selected_ticker = st.selectbox("Select Asset", tickers)
        
        hist_data = data['train_returns'][selected_ticker]
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=hist_data,
            nbinsx=50,
            marker_color='#64748b',
            opacity=0.8
        ))
        fig.add_vline(x=hist_data.mean(), line_dash="dash", line_color="#ef4444")
        fig = style_chart(fig, f"Return Distribution: {selected_ticker}")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        corr_matrix = data['train_returns'].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 11, "family": "Inter"}
        ))
        fig = style_chart(fig, "Correlation Matrix", height=600)
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE 3: OPTIMIZATION ====================
elif page == "Optimization":
    st.markdown('<h1 class="main-title">Optimization Engine</h1>', unsafe_allow_html=True)
    
    # Control Panel
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            allow_short = st.toggle("Allow Short Selling", value=True)
        with col2:
            rf_rate = st.number_input("Risk-Free Rate", value=0.0, step=0.01)
    
    st.markdown("---")
    
    mu = data['mu_train'].values
    Sigma = data['Sigma_train'].values
    
    # Calculate GMV
    w_gmv, gmv_ret, gmv_vol, success = compute_gmv_numerical(
        Sigma, mu, tickers, long_only=not allow_short
    )
    
    # Results Section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<h3 class="section-header">Optimal Weights (GMV)</h3>', unsafe_allow_html=True)
        weights_df = pd.DataFrame({
            'Asset': tickers,
            'Weight': w_gmv
        }).sort_values('Weight', ascending=False)
        
        st.dataframe(
            weights_df.style.format({'Weight': '{:.2%}'}).background_gradient(cmap='Greens'),
            use_container_width=True,
            height=400
        )
        
    with col2:
        st.markdown('<h3 class="section-header">Efficient Frontier</h3>', unsafe_allow_html=True)
        
        # Calc Frontier
        frontier = compute_efficient_frontier_numerical(
            mu, Sigma, tickers, n_points=100, long_only=not allow_short
        )
        
        f_rets = np.array([p['return'] for p in frontier])
        f_vols = np.array([p['volatility'] for p in frontier])
        
        fig = go.Figure()
        
        # Frontier Line
        fig.add_trace(go.Scatter(
            x=f_vols * 100, y=f_rets * 100,
            mode='lines', name='Efficient Frontier',
            line=dict(color='#0f172a', width=3)
        ))
        
        # Inefficient (if short selling)
        if allow_short:
             # Basic logic for inefficient part just for viz
             fig.add_trace(go.Scatter(
                x=f_vols * 100, y=(2*gmv_ret - f_rets) * 100, # Mirror for visual check approx
                mode='lines', name='Inefficient',
                line=dict(color='#cbd5e1', width=2, dash='dash')
            ))

        # Assets
        fig.add_trace(go.Scatter(
            x=data['annual_volatility'] * 100,
            y=data['annual_returns'] * 100,
            mode='markers', name='Assets',
            marker=dict(size=10, color='#94a3b8'),
            text=tickers
        ))
        
        # GMV
        fig.add_trace(go.Scatter(
            x=[gmv_vol * 100], y=[gmv_ret * 100],
            mode='markers', name='GMV Portfolio',
            marker=dict(size=15, color='#e11d48', symbol='star')
        ))
        
        fig = style_chart(fig, "Efficient Frontier vs. Assets", height=500)
        fig.update_layout(xaxis_title="Annualized Risk (%)", yaxis_title="Annualized Return (%)")
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE 4: BACKTEST ====================
elif page == "Backtest":
    st.markdown('<h1 class="main-title">Backtest Performance</h1>', unsafe_allow_html=True)
    
    mu = data['mu_train'].values
    Sigma = data['Sigma_train'].values
    
    # Compute Portfolios for Backtest
    w_gmv_short, _, _, _ = compute_gmv_numerical(Sigma, mu, tickers, long_only=False)
    w_gmv_long, _, _, _ = compute_gmv_numerical(Sigma, mu, tickers, long_only=True)
    w_equal = np.ones(len(tickers)) / len(tickers)
    
    # Run OOS
    oos_short = calculate_oos_performance(w_gmv_short, data['test_returns'])
    oos_long = calculate_oos_performance(w_gmv_long, data['test_returns'])
    oos_equal = calculate_oos_performance(w_equal, data['test_returns'])
    
    # Metrics Table
    metrics = pd.DataFrame({
        'Strategy': ['GMV (Long/Short)', 'GMV (Long Only)', 'Equal Weight'],
        'Return': [oos_short['realized_return'], oos_long['realized_return'], oos_equal['realized_return']],
        'Volatility': [oos_short['realized_vol'], oos_long['realized_vol'], oos_equal['realized_vol']],
        'Max Drawdown': [oos_short['max_drawdown'], oos_long['max_drawdown'], oos_equal['max_drawdown']]
    })
    
    col1, col2, col3 = st.columns(3)
    for i, row in metrics.iterrows():
        with [col1, col2, col3][i]:
            st.markdown(f'''
            <div class="card-metric" style="text-align: left;">
                <div class="metric-label" style="color: #3b82f6;">{row['Strategy']}</div>
                <div class="metric-value">{row['Return']:.2%}</div>
                <div style="font-size: 0.9rem; color: #64748b; margin-top: 5px;">
                    Vol: {row['Volatility']:.2%} | DD: {row['Max Drawdown']:.2%}
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
            
    # Cumulative Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=oos_short['cumulative_returns'].index, 
        y=oos_short['cumulative_returns'],
        mode='lines', name='GMV (Long/Short)',
        line=dict(color='#0f172a', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=oos_long['cumulative_returns'].index, 
        y=oos_long['cumulative_returns'],
        mode='lines', name='GMV (Long Only)',
        line=dict(color='#3b82f6', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=oos_equal['cumulative_returns'].index, 
        y=oos_equal['cumulative_returns'],
        mode='lines', name='Equal Weight',
        line=dict(color='#94a3b8', width=2, dash='dash')
    ))
    
    fig = style_chart(fig, "Out-of-Sample Performance", height=500)
    fig.update_layout(yaxis_title="Growth of $1")
    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE 5: SENSITIVITIES ====================
elif page == "Sensitivities":
    st.markdown('<h1 class="main-title">Stress Testing</h1>', unsafe_allow_html=True)
    
    st.info("Simulating efficient frontier behavior under varying correlation regimes.")
    
    mu = data['mu_train'].values
    Sigma = data['Sigma_train'].values
    corr_baseline = data['train_returns'].corr()
    std_diag = np.diag(np.sqrt(np.diag(Sigma)))
    
    # Scenarios
    scenarios = {
        "High Correlation (+50%)": np.clip(corr_baseline * 1.5, -0.99, 0.99),
        "Baseline": corr_baseline,
        "Low Correlation (-50%)": corr_baseline * 0.5
    }
    
    # Fix diagonals
    for k in scenarios:
        np.fill_diagonal(scenarios[k].values, 1.0)
        
    fig = go.Figure()
    colors = {'High Correlation (+50%)': '#ef4444', 'Baseline': '#0f172a', 'Low Correlation (-50%)': '#22c55e'}
    
    for name, corr_matrix in scenarios.items():
        # Reconstruct Sigma
        sigma_scen = std_diag @ corr_matrix.values @ std_diag
        
        # Calc Frontier
        # Using analytical for speed/stability in sensitivity
        ones = np.ones(len(tickers))
        sigma_inv = np.linalg.inv(sigma_scen)
        frontier_pts, _, _, _, _ = compute_efficient_frontier_analytical(
            mu, sigma_scen, sigma_inv, ones, tickers, n_points=50
        )
        
        x = np.array([p['volatility'] for p in frontier_pts]) * 100
        y = np.array([p['return'] for p in frontier_pts]) * 100
        
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='lines', name=name,
            line=dict(color=colors[name], width=2 if name!='Baseline' else 4)
        ))
        
    fig = style_chart(fig, "Frontier Sensitivity to Correlation", height=600)
    fig.update_layout(xaxis_title="Risk %", yaxis_title="Return %")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style="background-color: #f1f5f9; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6;">
        <p style="margin: 0; font-size: 0.95rem; color: #334155;">
        <b>Interpretation:</b> The shape of the efficient frontier is highly sensitive to cross-asset correlations. 
        The <b>Green Curve</b> (Lower Correlation) shifts significantly to the left, demonstrating that 
        lower correlations unlock greater diversification benefits (lower risk for the same return). 
        Conversely, the <b>Red Curve</b> (Higher Correlation) shifts right, showing that when assets move in lockstep, 
        diversification power is eroded.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Missing Sections: Volatility & Return Impact
    st.markdown("---")
    st.markdown('<h3 class="section-header">Asset Sensitivity</h3>', unsafe_allow_html=True)
    
    sens_type = st.radio("Analysis Type", ["Volatility Impact", "Return Impact"], horizontal=True)
    
    if sens_type == "Volatility Impact":
        st.markdown("**Scenario**: What if a single asset's risk changes?")
        
        col1, col2 = st.columns(2)
        with col1:
            target_asset = st.selectbox("Select Asset to Shock", tickers)
        with col2:
            vol_shock = st.slider("Volatility Multiplier", 0.5, 2.0, 1.0, 0.1)
            
        # Calc logic
        asset_idx = tickers.index(target_asset)
        Sigma_mod = Sigma.copy()
        current_std = np.sqrt(Sigma_mod[asset_idx, asset_idx])
        new_std = current_std * vol_shock
        
        # Adjust covariance row/col
        Sigma_mod[asset_idx, :] *= vol_shock
        Sigma_mod[:, asset_idx] *= vol_shock
        
        # Compare GMV weights
        w_base, _, _, _ = compute_gmv_numerical(Sigma, mu, tickers, long_only=True)
        w_mod, _, _, _ = compute_gmv_numerical(Sigma_mod, mu, tickers, long_only=True)
        
        # Display comparison
        comp_df = pd.DataFrame({
            'Asset': tickers,
            'Base Weight': w_base,
            'Shock Weight': w_mod,
            'Delta': w_mod - w_base
        }).sort_values('Delta', ascending=False)
        
        st.dataframe(
            comp_df.style.format({
                'Base Weight': '{:.2%}',
                'Shock Weight': '{:.2%}',
                'Delta': '{:+.2%}'
            }).background_gradient(cmap='RdBu', subset=['Delta'], vmin=-0.2, vmax=0.2),
            use_container_width=True
        )

    else:
        st.markdown("**Scenario**: Impact of return assumptions.")
        st.info("Note: GMV weights are independent of expected returns. This section illustrates statistics only.")
        
        idx = tickers.index(st.selectbox("Inspect Asset", tickers))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'''
            <div class="card-metric">
                <div class="metric-label">Expected Annual Return</div>
                <div class="metric-value">{mu[idx]:.2%}</div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''
            <div class="card-metric">
                <div class="metric-label">Annual Volatility</div>
                <div class="metric-value">{np.sqrt(Sigma[idx, idx]):.2%}</div>
            </div>
            ''', unsafe_allow_html=True)
