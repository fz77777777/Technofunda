import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Price-Volume Spurts Trending Scanner", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #111216; }
    .green-bar {
        background-color: #2ECC71;
        color: white;
        text-align: center;
        padding: 4px;
        font-weight: bold;
        border-radius: 4px;
        font-size: 11px;
    }
    .empty-bar {
        background-color: #EAECEE;
        color: #AEB6BF;
        text-align: center;
        padding: 4px;
        border-radius: 4px;
        font-size: 11px;
    }
    </style>
""", unsafe_html=True)

st.title("📈 TechnoFunda Style Price-Volume Spurts Dashboard")
st.write("Yeh scanner poori Indian Market se un stocks aur industries ko dhoondta hai jahan institutional buying (Green Patti) lagatar bani hui hai.")

# 1. Extensive Nifty 500 Momentum & Structural Universe mapped by Sector/Industry
@st.cache_data
def get_comprehensive_database():
    raw_data = [
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
        
        # --- GREEN ENERGY & POWER ---
        {"ticker": "NTPC.NS", "name": "NTPC", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "TATAPOWER.NS", "name": "Tata Power", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "SUZLON.NS", "name": "Suzlon Energy", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "IREDA.NS", "name": "IREDA", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "SJVN.NS", "name": "SJVN", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "NHPC.NS", "name": "NHPC", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "KPIGREEN.NS", "name": "KPI Green Energy", "industry": "Green Energy & Power", "cap": "Small Cap"},
        
        # --- BANKING & FINANCE ---
        {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "SBIN.NS", "name": "State Bank of India", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "PNB.NS", "name": "Punjab National Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "IDFCFIRSTB.NS", "name": "IDFC First Bank", "industry": "Banking & Finance", "cap": "Mid Cap"},
        {"ticker": "UNIONBANK.NS", "name": "Union Bank", "industry": "Banking & Finance", "cap": "Mid Cap"},
        {"ticker": "SOUTHBANK.NS", "name": "South Indian Bank", "industry": "Banking & Finance", "cap": "Small Cap"},
        
        # --- IT & SOFTWARE ---
        {"ticker": "TCS.NS", "name": "TCS", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "INFY.NS", "name": "Infosys", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "WIPRO.NS", "name": "Wipro", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "KPITTECH.NS", "name": "KPIT Technologies", "industry": "IT & Software", "cap": "Mid Cap"},
        {"ticker": "TATAELXSI.NS", "name": "Tata Elxsi", "industry": "IT & Software", "cap": "Mid Cap"},
        {"ticker": "ZENSARTECH.NS", "name": "Zensar Tech", "industry": "IT & Software", "cap": "Small Cap"},
        {"ticker": "HAPPSTMND.NS", "name": "Happiest Minds", "industry": "IT & Software", "cap": "Small Cap"},
        
        # --- SPECIALTY CHEMICALS ---
        {"ticker": "SRF.NS", "name": "SRF Limited", "industry": "Specialty Chemicals", "cap": "Large Cap"},
        {"ticker": "TATACHEM.NS", "name": "Tata Chemicals", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "DEEPAKNTR.NS", "name": "Deepak Nitrite", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "AETHER.NS", "name": "Aether Industries", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "CLEAN.NS", "name": "Clean Science", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "FINEORG.NS", "name": "Fine Organic", "industry": "Specialty Chemicals", "cap": "Mid Cap"},
        {"ticker": "LXCHEM.NS", "name": "Laxmi Organic", "industry": "Specialty Chemicals", "cap": "Small Cap"},
        
        # --- INFRASTRUCTURE & REALTY ---
        {"ticker": "LT.NS", "name": "Larsen & Toubro", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "DLF.NS", "name": "DLF", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "GMRINFRA.NS", "name": "GMR Infra", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "GODREJPROP.NS", "name": "Godrej Properties", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "NBCC.NS", "name": "NBCC India", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        {"ticker": "ITDCEM.NS", "name": "ITD Cementation", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        
        # --- AUTOMOBILES & EV ---
        {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "TVSMOTOR.NS", "name": "TVS Motor", "industry": "Automobiles & EV", "cap": "Large Cap"},
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
    return pd.DataFrame(raw_data)

# 2. Historical Processing Engine to Compute Spurt Conditions Day by Day
def process_trending_days(df_db, lookback_history=45):
    tickers = df_db['ticker'].tolist()
    
    # Downloading extra historical buffer to calculate clean rolling 20-day baseline average
    total_days_needed = lookback_history + 35
    start_date = (datetime.now() - timedelta(days=total_days_needed)).strftime('%Y-%m-%d')
    
    data = yf.download(tickers, start=start_date, progress=False)
    if data.empty or 'Volume' not in data.columns or 'Close' not in data.columns:
        return pd.DataFrame(), []
        
    volume_df = data['Volume'].ffill().bfill()
    close_df = data['Close'].ffill().bfill()
    
    # Extract only the last required working dates
    active_trading_dates = volume_df.index[-lookback_history:]
    date_strings = [d.strftime('%Y-%m-%d') for d in active_trading_dates]
    
    stock_matrix = []
    
    for _, row in df_db.iterrows():
        t = row['ticker']
        if t in volume_df.columns and len(volume_df[t]) >= lookback_history:
            spurt_history = {}
            total_trending_days_count = 0
            
            # Loop backwards through time to fill out matrix rows
            for idx in range(-lookback_history, 0):
                date_str = volume_df[t].index[idx].strftime('%Y-%m-%d')
                
                # Fetch volume parameters
                day_vol = volume_df[t].iloc[idx]
                # Rolling 20-day volume baseline excluding target slot
                pos = volume_df.index.get_loc(volume_df[t].index[idx])
                historical_avg_20 = volume_df[t].iloc[max(0, pos-20):pos].mean()
                
                # Fetch price movement parameters
                price_today = close_df[t].iloc[idx]
                price_prev = close_df[t].iloc[idx-1] if (pos-1) >= 0 else price_today
                day_return = ((price_today - price_prev) / price_prev) * 100
                
                # THE FORMULA CRITERIA: Volume > 1.5x of average AND price up > 1.0%
                if historical_avg_20 > 0 and day_vol > (historical_avg_20 * 1.5) and day_return >= 1.0:
                    spurt_history[date_str] = f"🟩 {day_return:+.1f}%\n({int(day_vol/historical_avg_20)}x)"
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
            # Append dynamic patti values
            base_info.update(spurt_history)
            stock_matrix.append(base_info)
            
    return pd.DataFrame(stock_matrix), date_strings

# --- Side Controls Panel ---
st.sidebar.header("🛠️ Configuration Options")

# User Request: Dynamic lookback range option widget
window_selection = st.sidebar.selectbox(
    "Select Evaluation Viewport",
    ["Today Only", "Yesterday View", "Past 3 Days Churn", "Past 7 Days Churn", "Past 15 Days Cluster", "Past 30 Days Cycle", "Past 45 Days Wave"]
)

mapping_lookback = {
    "Today Only": 1, "Yesterday View": 2, "Past 3 Days Churn": 3,
    "Past 7 Days Churn": 7, "Past 15 Days Cluster": 15,
    "Past 30 Days Cycle": 30, "Past 45 Days Wave": 45
}
active_lookback = mapping_lookback[window_selection]

cap_selection = st.sidebar.selectbox("Market Cap Segment", ["All Stocks Market", "Large Cap", "Mid Cap", "Small Cap"])

# Load Database
df_db = get_comprehensive_database()

with st.spinner("Scanning Indian Market Matrix for Institutional Inflows..."):
    df_matrix, valid_dates = process_trending_days(df_db, lookback_history=active_lookback)

if not df_matrix.empty:
    # Filter matrix rows based on user market cap settings
    if cap_selection != "All Stocks Market":
        df_matrix = df_matrix[df_matrix['cap'] == cap_selection]
        
    # Calculate score metrics to identify top structural strength industries
    industry_ranking = df_matrix.groupby('industry').agg(
        Total_Trending_Spikes=('trending_days', 'sum'),
        Total_Constituent_Stocks=('ticker', 'count')
    ).reset_index()
    
    # Sorting Industry according to cumulative hit frequency strength
    industry_ranking['Strength_Index'] = (industry_ranking['Total_Trending_Spikes'] / industry_ranking['Total_Constituent_Stocks']).round(2)
    industry_ranking = industry_ranking.sort_values(by='Strength_Index', ascending=False).reset_index(drop=True)
    
    st.subheader(f"🏆 Sorted Industry Lead Spectrum ({window_selection})")
    st.write("Industries unme hone wale high volume patti instances ke decreasing order me sorted hain.")
    
    # 3. Generating Customized Interactive Rows with Dropdowns
    for rank, ind_row in industry_ranking.iterrows():
        ind_name = ind_row['industry']
        score = ind_row['Strength_Index']
        
        # Color coding system for expandable blocks
        if score >= 2.0:
            expander_title = f"🔥 #{rank+1} {ind_name.upper()} (Activity Score: {score}) ➔ HIGH ACCUMULATION"
        elif score >= 0.8:
            expander_title = f"📈 #{rank+1} {ind_name.upper()} (Activity Score: {score}) ➔ STEADY INFLOWS"
        else:
            expander_title = f"💤 #{rank+1} {ind_name.upper()} (Activity Score: {score}) ➔ MUTED / CHURN"
            
        with st.expander(expander_title):
            # Fetch inner constituents items mapped inside current sector
            sub_stocks = df_matrix[df_matrix['industry'] == ind_name].copy()
            # Dynamic interior item sorting routine based on highest trending days count
            sub_stocks = sub_stocks.sort_values(by='trending_days', ascending=False)
            
            # Formulating HTML tables natively for custom cells formatting injection
            html_table = f"""
            <table style='width:100%; border-collapse: collapse; margin: 10px 0;'>
                <thead>
                    <tr style='background-color: #1F2A38; color: white;'>
                        <th style='padding:8px; text-align:left;'>Stock Name</th>
                        <th style='padding:8px; text-align:left;'>Cap Class</th>
                        <th style='padding:8px; text-align:left;'>Last Close</th>
                        <th style='padding:8px; text-align:center;'>Total Hits</th>
            """
            
            # Print horizontal timeline dates strings header column blocks
            for d in valid_dates:
                html_table += f"<th style='padding:8px; text-align:center; font-size:11px;'>{d}</th>"
            html_table += "</tr></thead><tbody>"
            
            # Render internal matrix records dynamically row by row
            for _, s_row in sub_stocks.iterrows():
                html_table += f"""
                <tr style='border-bottom: 1px solid #34495E;'>
                    <td style='padding:8px; font-weight:bold;'>{s_row['name']} <br><span style='font-size:10px; color:#7F8C8D;'>{s_row['ticker']}</span></td>
                    <td style='padding:8px;'>{s_row['cap']}</td>
                    <td style='padding:8px; color:#F39C12;'>₹{s_row['last_close']}</td>
                    <td style='padding:8px; text-align:center; font-weight:bold; color:#2ECC71;'>{s_row['trending_days']} Days</td>
                """
                
                # Insert colored block elements depending on day logic hit status
                for d in valid_dates:
                    cell_val = s_row[d]
                    if "🟩" in cell_val:
                        # Split formatting to show price change and ratio clearly inside green container
                        display_val = cell_val.replace("🟩 ", "")
                        html_table += f"<td><div class='green-bar'>{display_val}</div></td>"
                    else:
                        html_table += "<td><div class='empty-bar'>-</div></td>"
                        
                html_table += "</tr>"
                
            html_table += "</tbody></table>"
            st.markdown(html_table, unsafe_html=True)
else:
    st.info("No data available. Filters badaliye ya market open hone ka wait kijiye.")
