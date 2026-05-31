import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page config layout set up to widest screen to look exactly like the premium sheets
st.set_page_config(page_title="Price-Volume Spurts Pro Scanner", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS safely for Python 3.14 (Single-line formatting to prevent parser multi-line errors)
st.markdown("<style>.reportview-container { background: #111216; }</style>", unsafe_html=True)
st.markdown("<style>.reportview-container .main .block-container { padding-top: 1rem; }</style>", unsafe_html=True)
st.markdown("<style>.green-strip { background-color: #2ECC71 !important; color: white !important; text-align: center; padding: 6px 4px; font-weight: bold; border-radius: 2px; font-size: 11px; box-shadow: inset 0 0 4px rgba(0,0,0,0.2); min-height: 24px; display: flex; align-items: center; justify-content: center; }</style>", unsafe_html=True)
st.markdown("<style>.empty-strip { background-color: #2C3E50 !important; color: #7F8C8D !important; text-align: center; padding: 6px 4px; border-radius: 2px; font-size: 11px; min-height: 24px; display: flex; align-items: center; justify-content: center; opacity: 0.25; }</style>", unsafe_html=True)
st.markdown("<style>.stock-table { width: 100%; border-collapse: separate; border-spacing: 2px 4px; margin: 10px 0; }</style>", unsafe_html=True)
st.markdown("<style>.stock-table th { background-color: #1A252F; color: #ECF0F1; padding: 10px 8px; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #34495E; }</style>", unsafe_html=True)
st.markdown("<style>.stock-table td { background-color: #141D26; color: #E5E8E8; padding: 8px; font-size: 12px; vertical-align: middle; }</style>", unsafe_html=True)
st.markdown("<style>.industry-trigger { font-size: 15px; font-weight: bold; }</style>", unsafe_html=True)

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
        {"ticker": "OLECTRA.NS", "name": "Olectra Greentech", "industry": "Automobiles & EV", "cap": "Small Cap"},
        
        # --- PHARMA & HEALTHCARE ---
        {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "CIPLA.NS", "name": "Cipla", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "LUPIN.NS", "name": "Lupin", "industry": "Pharma & Healthcare", "cap": "Mid Cap"},
        {"ticker": "GLENMARK.NS", "name": "Glenmark Pharma", "industry": "Pharma & Healthcare", "cap": "Mid Cap"},
        {"ticker": "JUBLPHARMA.NS", "name": "Jubilant Pharma", "industry": "Pharma & Healthcare", "cap": "Small Cap"},
        
        # --- METALS & MINING ---
        {"ticker": "TATASTEEL.NS", "name": "Tata Steel", "industry": "Metals & Mining", "cap": "Large Cap"},
        {"ticker": "JSWSTEEL.NS", "name": "JSW Steel", "industry": "Metals & Mining", "cap": "Large Cap"},
        {"ticker": "HINDALCO.NS", "name": "Hindalco", "industry": "Metals & Mining", "cap": "Large Cap"},
        {"ticker": "SAIL.NS", "name": "SAIL", "industry": "Metals & Mining", "cap": "Mid Cap"},
        {"ticker": "NMDC.NS", "name": "NMDC", "industry": "Metals & Mining", "cap": "Mid Cap"}
    ]
    return pd.DataFrame(universe)

# 2. Optimized Vectorized Data Engine
def process_institutional_spurts(df_db, lookback_history=45):
    tickers = df_db['ticker'].tolist()
    
    total_days_needed = lookback_history + 40
    start_date = (datetime.now() - timedelta(days=total_days_needed)).strftime('%Y-%m-%d')
    
    # Vectorized Single Request Batch Download
    data = yf.download(tickers, start=start_date, progress=False)
    if data.empty or 'Volume' not in data.columns or 'Close' not in data.columns:
        return pd.DataFrame(), []
        
    volume_df = data['Volume'].ffill().bfill()
    close_df = data['Close'].ffill().bfill()
    
    # Extract true working dates from yfinance structure
    active_trading_dates = volume_df.index[-lookback_history:]
    date_strings = [d.strftime('%d\n%b') for d in active_trading_dates]
    
    stock_matrix = []
    
    for _, row in df_db.iterrows():
        t = row['ticker']
        if t in volume_df.columns and len(volume_df[t]) >= lookback_history:
            spurt_history = {}
            total_trending_days_count = 0
            
            for idx in range(-lookback_history, 0):
                date_obj = volume_df[t].index[idx]
                date_str = date_obj.strftime('%d\n%b')
                
                day_vol = volume_df[t].iloc[idx]
                pos = volume_df.index.get_loc(date_obj)
                historical_avg_20 = volume_df[t].iloc[max(0, pos-20):pos].mean()
                
                price_today = close_df[t].iloc[idx]
                price_prev = close_df[t].iloc[idx-1] if (pos-1) >= 0 else price_today
                day_return = ((price_today - price_prev) / price_prev) * 100
                
                # Formula setup matching image visual requirements exactly: Volume > 1.5x AND price return >= 1.0%
                if historical_avg_20 > 0 and day_vol > (historical_avg_20 * 1.5) and day_return >= 1.0:
                    spurt_history[date_str] = f"{day_return:+.1f}%|({int(day_vol/historical_avg_20)}x)"
                    total_trending_days_count += 1
                else:
                    spurt_history[date_str] = ""
                    
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
        
    # Aggregate data to score and find top industries automatically
    industry_ranking = df_matrix.groupby('industry').agg(
        Total_Spikes=('trending_days', 'sum'),
        Total_Stocks=('ticker', 'count')
    ).reset_index()
    
    industry_ranking['Score'] = (industry_ranking['Total_Spikes'] / industry_ranking['Total_Stocks']).round(2)
    # SORTING: Industry with most active spikes sits at the very top
    industry_ranking = industry_ranking.sort_values(by='Score', ascending=False).reset_index(drop=True)
    
    st.subheader(f"🏆 Sorted Industry Lead Matrix ({window_selection})")
    
    for rank, ind_row in industry_ranking.iterrows():
        ind_name = ind_row['industry']
        score = ind_row['Score']
        
        if score >= 1.5:
            badge_style = "background-color:#196F3D; color:#2ECC71;"
            status_text = "🚀 CRITICAL MOMENTUM"
        elif score >= 0.5:
            badge_style = "background-color:#112233; color:#5DADE2;"
            status_text = "📈 STEADY ACCUMULATION"
        else:
            badge_style = "background-color:#2C3E50; color:#BDC3C7;"
            status_text = "💤 ACQUISITION FLATLINE"
            
        header_title_html = f"""
        <div style='{badge_style} padding:10px; border-radius:4px; font-weight:bold; margin-top:8px;' class='industry-trigger'>
            #{rank+1} {ind_name.upper()} &nbsp;&nbsp;|&nbsp;&nbsp; Spurt Score: {score} &nbsp;&nbsp;|&nbsp;&nbsp; {status_text}
        </div>
        """
        
        with st.expander(header_title_html, expanded=(rank == 0)):
            sub_stocks = df_matrix[df_matrix['industry'] == ind_name].copy()
            # SORTING: Inside the industry, stocks are sorted high-to-low based on hits
            sub_stocks = sub_stocks.sort_values(by='trending_days', ascending=False)
            
            # Form HTML Table to print exact green/gray blocks layout
            html_table = """
            <table class='stock-table'>
                <thead>
                    <tr>
                        <th style='text-align:left;'>Company Name</th>
                        <th style='text-align:left;'>Market Cap</th>
                        <th style='text-align:left;'>Last Close</th>
                        <th style='text-align:center;'>Trending Days</th>
            """
            for d in valid_dates:
                html_table += f"<th style='text-align:center; min-width:55px; white-space:pre-wrap;'>{d}</th>"
            html_table += "</tr></thead><tbody>"
            
            for _, s_row in sub_stocks.iterrows():
                html_table += f"""
                <tr>
                    <td style='font-weight:bold; color:#3498DB;'>{s_row['name']}<br><span style='font-size:10px; color:#95A5A6;'>{s_row['ticker']}</span></td>
                    <td>{s_row['cap']}</td>
                    <td style='color:#F1C40F; font-weight:bold;'>₹{s_row['last_close']}</td>
                    <td style='text-align:center; font-weight:bold; color:#2ECC71;'>{s_row['trending_days']} d</td>
                """
                
                for d in valid_dates:
                    cell_val = s_row[d]
                    if "|" in cell_val:
                        parts = cell_val.split("|")
                        return_pct = parts[0]
                        multiplier = parts[1]
                        html_table += f"<td><div class='green-strip'>{return_pct}<br><span style='font-size:9px; font-weight:normal;'>{multiplier}</span></div></td>"
                    else:
                        html_table += "<td><div class='empty-strip'>-</div></td>"
                html_table += "</tr>"
                
            html_table += "</tbody></table>"
            st.markdown(html_table, unsafe_html=True)
else:
    st.info("No active breakout data fetched. Filters change karke try kijiye.")
