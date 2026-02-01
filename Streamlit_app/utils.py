import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import inv

def load_csx_data_from_excel(tickers):
    """Load CSX equity price data from Excel files."""
    import streamlit as st
    from io import BytesIO
    
    frames = []
    for ticker in tickers:
        try:
            # Try to load from uploaded files
            # Load from local data folder relative to this script
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "data", f"{ticker}.xlsx")
            df = pd.read_excel(file_path, parse_dates=['Date'], usecols=['Date', 'Closing Price'])
            df = df.rename(columns={'Closing Price': ticker})
            df[ticker] = pd.to_numeric(df[ticker], errors='coerce')
            df = df.set_index('Date').sort_index()
            frames.append(df)
        except Exception as e:
            st.error(f"Error loading {ticker}.xlsx: {e}")
            return None
    
    if not frames:
        st.error("No data files loaded successfully!")
        return None
    
    prices = pd.concat(frames, axis=1, join='outer')
    prices = prices.ffill().dropna()
    return prices

def treat_outliers(df, threshold=3):
    """
    Identifies returns beyond (Mean +/- 3*StdDev) and 
    clips them to the boundary values.
    """
    df_cleaned = df.copy()
    for col in df_cleaned.columns:
        mu = df_cleaned[col].mean()
        sigma = df_cleaned[col].std()
        lower_bound = mu - threshold * sigma
        upper_bound = mu + threshold * sigma
        df_cleaned[col] = df_cleaned[col].clip(lower=lower_bound, upper=upper_bound)
    return df_cleaned

def portfolio_variance(weights, Sigma):
    """Calculate portfolio variance"""
    return weights @ Sigma @ weights

def portfolio_return(weights, mu):
    """Calculate portfolio return"""
    return weights @ mu

def compute_gmv_analytical(Sigma, mu, tickers):
    """Compute Global Minimum Variance Portfolio using analytical solution"""
    n = len(tickers)
    ones = np.ones(n)
    Sigma_inv = inv(Sigma)
    
    w_gmv = Sigma_inv @ ones / (ones.T @ Sigma_inv @ ones)
    
    gmv_return = w_gmv @ mu
    gmv_variance = w_gmv @ Sigma @ w_gmv
    gmv_volatility = np.sqrt(gmv_variance)
    
    return w_gmv, gmv_return, gmv_volatility

def analytical_efficient_portfolio(target_return, mu, Sigma_inv, ones, A, B, C, D):
    """Compute efficient portfolio for target return using analytical formula"""
    lambda1 = (C - B * target_return) / D
    lambda2 = (A * target_return - B) / D
    
    w = lambda1 * (Sigma_inv @ ones) + lambda2 * (Sigma_inv @ mu)
    return w

def compute_gmv_numerical(Sigma, mu, tickers, long_only=False):
    """Compute GMV Portfolio using numerical optimization"""
    n = len(tickers)
    w0 = np.ones(n) / n
    
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    
    bounds = tuple((0, 1) for _ in range(n)) if long_only else None
    
    result = minimize(
        portfolio_variance,
        w0,
        args=(Sigma,),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'ftol': 1e-9, 'disp': False}
    )
    
    w_gmv = result.x
    gmv_return = portfolio_return(w_gmv, mu)
    gmv_volatility = np.sqrt(portfolio_variance(w_gmv, Sigma))
    
    return w_gmv, gmv_return, gmv_volatility, result.success

def compute_efficient_frontier_analytical(mu, Sigma, Sigma_inv, ones, tickers, n_points=100):
    """Compute efficient frontier using analytical method"""
    n = len(tickers)
    
    # Helper variables for Lagrangian multipliers method
    A = ones.T @ Sigma_inv @ ones
    B = ones.T @ Sigma_inv @ mu
    C = mu.T @ Sigma_inv @ mu
    D = A * C - B**2
    
    min_return = mu.min()
    max_return = mu.max()
    target_returns = np.linspace(min_return, max_return, n_points)
    
    frontier_points = []
    for target_ret in target_returns:
        w = analytical_efficient_portfolio(target_ret, mu, Sigma_inv, ones, A, B, C, D)
        port_vol = np.sqrt(w @ Sigma @ w)
        frontier_points.append({
            'return': target_ret,
            'volatility': port_vol,
            'weights': w
        })
    
    return frontier_points, A, B, C, D

def compute_efficient_frontier_numerical(mu, Sigma, tickers, n_points=100, long_only=False):
    """Compute efficient frontier points using numerical optimization"""
    n = len(tickers)
    w0 = np.ones(n) / n
    
    min_return = -0.15
    max_return = 0.40
    target_returns = np.linspace(min_return, max_return, n_points)
    
    frontier_points = []
    bounds = tuple((0, 1) for _ in range(n)) if long_only else None
    
    for target_ret in target_returns:
        constraints = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w, tr=target_ret: portfolio_return(w, mu) - tr}
        ]
        
        result = minimize(
            portfolio_variance,
            w0,
            args=(Sigma,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'ftol': 1e-9, 'disp': False}
        )
        
        if result.success:
            w = result.x
            port_vol = np.sqrt(portfolio_variance(w, Sigma))
            frontier_points.append({
                'return': target_ret,
                'volatility': port_vol,
                'weights': w
            })
    
    return frontier_points

def calculate_oos_performance(weights, returns_oos):
    """Calculate out-of-sample performance metrics"""
    port_returns_oos = returns_oos @ weights
    
    realized_return = port_returns_oos.mean() * 252
    realized_vol = port_returns_oos.std() * np.sqrt(252)
    
    cumulative_returns = (1 + port_returns_oos).cumprod()
    
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        'realized_return': realized_return,
        'realized_vol': realized_vol,
        'cumulative_returns': cumulative_returns,
        'max_drawdown': max_drawdown
    }
