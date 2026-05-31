   import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page config layout set up to widest screen
st.set_page_config(page_title="Price-Volume Spurts Pro Scanner", layout="wide", initial_sidebar_state="expanded")

st.title("📈 TechnoFunda Price-Volume Spurts Trending Scanner")
st.write("India's premium institutional delivery tracking engine. Sorted from high-to-low momentum blocks.")

# 1. Scaled Up High-Momentum Database covering major multi-cap setups (Large, Mid, Small Caps)
@st.cache_data(ttl=3600)  # Cache data for 1 hour to prevent constant slow re-runs
def get_nifty_momentum_universe():
    universe = [
        # --- AGRI CHEMICALS & FERTILIZERS ---
        {"ticker": "UPL.NS", "name": "UPL Limited", "industry": "Agri Chemicals", "cap": "Large Cap"},
        {"ticker": "PIIND.NS", "name": "PI Industries", "industry": "Agri Chemicals", "cap": "Large Cap"},
        {"ticker": "COROMANDEL.NS", "name": "Coromandel Intl", "industry": "Agri Chemicals", "cap": "Mid Cap"},
        {"ticker": "FACT.NS", "name": "FACT", "industry": "Agri Chemicals", "cap": "Mid Cap"},
        {"ticker": "DEEPAKFERT.NS", "name": "Deepak Fertilizers", "industry": "Agri Chemicals", "cap": "Small Cap"},
        {"ticker": "RCF.NS", "name": "Rashtriya Chemicals", "industry": "Agri Chemicals", "cap": "Small Cap"},
        {"ticker": "GNFC.NS", "name": "GNFC", "industry": "Agri Chemicals", "cap": "Small Cap"},
        {"ticker": "GSFC.NS", "name": "GSFC", "industry": "Agri Chemicals", "cap": "Small Cap"},
        {"ticker": "ARIES.NS", "name": "Aries Agro", "industry": "Agri Chemicals", "cap": "Small Cap"},
        {"ticker": "MANGCHEFER.NS", "name": "Mangalore Chem", "industry": "Agri Chemicals", "cap": "Small Cap"},
        {"ticker": "ZUARI.NS", "name": "Zuari Agro", "industry": "Agri Chemicals", "cap": "Small Cap"},
        
        # --- RAILWAYS ---
        {"ticker": "IRFC.NS", "name": "IRFC", "industry": "Railways", "cap": "Large Cap"},
        {"ticker": "RVNL.NS", "name": "RVNL", "industry": "Railways", "cap": "Mid Cap"},
        {"ticker": "IRCON.NS", "name": "IRCON", "industry": "Railways", "cap": "Mid Cap"},
        {"ticker": "RAILTEL.NS", "name": "RailTEL", "industry": "Railways", "cap": "Small Cap"},
        {"ticker": "TITAGARH.NS", "name": "Titagarh Rail", "industry": "Railways", "cap": "Small Cap"},
        {"ticker": "TEXRAIL.NS", "name": "Texmaco Rail", "industry": "Railways", "cap": "Small Cap"},
        
        # --- DEFENSE ---
        {"ticker": "HAL.NS", "name": "Hindustan Aeronautics", "industry": "Defense", "cap": "Large Cap"},
        {"ticker": "BEL.NS", "name": "Bharat Electronics", "industry": "Defense", "cap": "Large Cap"},
        {"ticker": "MAZDOCK.NS", "name": "Mazagon Dock", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "COCHINSHIP.NS", "name": "Cochin Shipyard", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "BDL.NS", "name": "Bharat Dynamics", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "BEML.NS", "name": "BEML Limited", "industry": "Defense", "cap": "Small Cap"},
        
        # --- GREEN ENERGY & POWER ---
        {"ticker": "NTPC.NS", "name": "NTPC", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "TATAPOWER.NS", "name": "Tata Power", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "SUZLON.NS", "name": "Suzlon Energy", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "IREDA.NS", "name": "IREDA", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "SJVN.NS", "name": "SJVN", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "KPIGREEN.NS", "name": "KPI Green Energy", "industry": "Green Energy & Power", "cap": "Small Cap"},
        
        # --- INFRASTRUCTURE & REALTY ---
        {"ticker": "LT.NS", "name": "Larsen & Toubro", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "DLF.NS", "name": "DLF", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "GMRINFRA.NS", "name": "GMR Infra", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "GODREJPROP.NS", "name": "Godrej Properties", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "NBCC.NS", "name": "NBCC India", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        {"ticker": "SUNTECK.NS", "name": "Sunteck Realty", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        
        # --- SPECIALTY CHEMICALS ---
        {"ticker": "SRF.NS", "name": "SRF Limited", "industry": "Specialty Chemicals", "cap": "Large Cap"},
        {"ticker": "TATACHEM.NS", "name": "Tata Chemicals", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "DEEPAKNTR.NS", "name": "Deepak Nitrite", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "LXCHEM.NS", "name": "Laxmi Organic", "industry": "Specialty Chemicals", "cap": "Small Cap"},
        
        # --- AUTOMOBILES & EV ---
        {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "RKFORGE.NS", "name": "Ramkrishna Forgings", "industry": "Automobiles & EV", "cap": "Small Cap"},
        {"ticker": "OLECTRA.NS", "name": "Olectra Greentech", "industry": "Automobiles & EV", "cap": "Small Cap"}
    ]
    return pd.DataFrame(universe)

# 2. Optimized Vectorized Data Engine
def process_institutional_spurts(df_db, lookback_history=45):
    tickers = df_db['ticker'].tolist()
    
    total_days_needed = lookback_history + 40
    start_date = (datetime.now() - timedelta(days=total_days_needed)).strftime('%Y-%m-%d')
    
    data = yf.download(tickers, start=start_date, progress=False)
    if data.empty or 'Volume' not in data.columns or 'Close' not in data.columns:
        return pd.DataFrame(), []
        
    volume_df = data['Volume'].ffill().bfill()
    close_df = data['Close'].ffill().bfill()
    
    active_trading_dates = volume_df.index[-lookback_history:]
    date_strings = [d.strftime('%d %b') for d in active_trading_dates]
    
    stock_matrix = []
    
    for _, row in df_db.iterrows():
        t = row['ticker']
        if t in volume_df.columns and len(volume_df[t]) >= lookback_history:
            spurt_history = {}
            total_trending_days_count = 0
            
            for idx in range(-lookback_history, 0):
                date_obj = volume_df[t].index[idx]
                date_str = date_obj.strftime('%d %b')
                
                day_vol = volume_df[t].iloc[idx]
                pos = volume_df.index.get_loc(date_obj)
                historical_avg_20 = volume_df[t].iloc[max(0, pos-20):pos].mean()
                
                price_today = close_df[t].iloc[idx]
                price_prev = close_df[t].iloc[idx-1] if (pos-1) >= 0 else price_today
                day_return = ((price_today - price_prev) / price_prev) * 100
                
                if historical_avg_20 > 0 and day_vol > (historical_avg_20 * 1.5) and day_return >= 1.0:
                    spurt_history[date_str] = f"{day_return:+.1f}% ({int(day_vol/historical_avg_20)}x)"
                    total_trending_days_count += 1
                else:
                    spurt_history[date_str] = "-"
                    
            base_info = {
                "ticker": t,
                "name": row['name'],
                "industry": row['industry'],
                "cap": row['cap'],
                "trending_days": total_trending_days_count,
                "last_close": round(close_df[t].iloc[-1], 2)
            }
            base_info.update(spurt_history)
            stock_matrix.append(base_info)
            
    return pd.DataFrame(stock_matrix), date_strings

# --- Sidebar Controls ---
st.sidebar.header("🎯 Timeframe & Universe")

window_selection = st.sidebar.selectbox(
    "Select Lookback Viewport",
    ["Today Data Only", "Yesterday Data", "3 Days Before", "7 Days Before", "15 Days Before", "30 Days Before", "45 Days Before"]
)

mapping_lookback = {
    "Today Data Only": 1, "Yesterday Data": 2, "3 Days Before": 3,
    "7 Days Before": 7, "15 Days Before": 15, "30 Days Before": 30, "45 Days Before": 45
}
active_lookback = mapping_lookback[window_selection]

cap_selection = st.sidebar.selectbox("Market Cap Selection", ["All Market Stocks", "Large Cap", "Mid Cap", "Small Cap"])

# Execute Engine
df_db = get_nifty_momentum_universe()

with st.spinner("Processing Price-Volume Matrix... Please wait."):
    df_matrix, valid_dates = process_institutional_spurts(df_db, lookback_history=active_lookback)

if not df_matrix.empty:
    if cap_selection != "All Market Stocks":
        df_matrix = df_matrix[df_matrix['cap'] == cap_selection]
        
    industry_ranking = df_matrix.groupby('industry').agg(
        Total_Spikes=('trending_days', 'sum'),
        Total_Stocks=('ticker', 'count')
    ).reset_index()
    
    industry_ranking['Score'] = (industry_ranking['Total_Spikes'] / industry_ranking['Total_Stocks']).round(2)
    industry_ranking = industry_ranking.sort_values(by='Score', ascending=False).reset_index(drop=True)
    
    st.subheader(f"🏆 Sorted Industry Lead Matrix ({window_selection})")
    
    for rank, ind_row in industry_ranking.iterrows():
        ind_name = ind_row['industry']
        score = ind_row['Score']
        
        # Native safe status icons based on scoring velocity
        if score >= 1.5:
            status_badge = f"🟢 #{rank+1} {ind_name.upper()} | Score: {score} [CRITICAL MOMENTUM]"
        elif score >= 0.5:
            status_badge = f"🔵 #{rank+1} {ind_name.upper()} | Score: {score} [STEADY ACCUMULATION]"
        else:
            status_badge = f"⚪ #{rank+1} {ind_name.upper()} | Score: {score} [FLATLINE]"
            
        with st.expander(status_badge, expanded=(rank == 0)):
            sub_stocks = df_matrix[df_matrix['industry'] == ind_name].copy()
            sub_stocks = sub_stocks.sort_values(by='trending_days', ascending=False)
            
            # Use safe native dataframes with dynamic conditional formatting
            display_cols = ["name", "ticker", "cap", "last_close", "trending_days"] + valid_dates
            final_display = sub_stocks[display_cols].copy()
            
            # Dynamic formatting function for native dataframes
            def highlight_spurts(val):
                if isinstance(val, str) and "%" in val:
                    return 'background-color: #1E8449; color: white; font-weight: bold; text-align: center;'
                elif val == "-":
                    return 'background-color: #2C3E50; color: #7F8C8D; text-align: center; opacity: 0.5;'
                return ''

            # Render beautifully using Streamlit's new fully functional native element
            st.dataframe(
                final_display.style.applymap(highlight_spurts, subset=valid_dates),
                use_container_width=True,
                hide_index=True
            )
else:
    st.info("No active breakout data fetched. Filters change karke try kijiye.")
