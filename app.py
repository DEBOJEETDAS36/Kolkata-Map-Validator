import streamlit as st
import pandas as pd
import json
from src.engine import GeoAuditEngine

# --- DASHBOARD CONFIG ---
st.set_page_config(page_title="GeoAudit Kolkata", layout="wide")
st.title("📍 GeoAudit Kolkata: Market-Ready MVP")
st.markdown("Professional Geospatial Validation for Logistics & Mapping Operations.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Audit Settings")
threshold = st.sidebar.slider("Accuracy Threshold (km)", 0.1, 2.0, 0.5)
engine = GeoAuditEngine(threshold=threshold)

# --- MAIN INTERFACE ---
st.subheader("1. Run Live Batch Audit")
if st.button("Start Kolkata Audit"):
    # Run the engine logic
    engine.run_batch_audit("data/landmarks.json")
    
    # Convert results to a DataFrame for display
    df = pd.DataFrame(engine.audit_results)
    
    # --- METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Audited", len(df))
    col2.metric("Failed Routes", len(df[df['status'] == 'FAIL']))
    col3.metric("Avg Variance (km)", round(df['variance_km'].mean(), 2))

    st.subheader("2. Spatial Distribution of Audit Points")
    if not df.empty:
        # Streamlit requires columns named 'lat' and 'lon' to render maps
        map_df = df[['lat', 'lon']] 
        st.map(map_df)

    # --- DATA TABLE ---
    st.subheader("2. Detailed Audit Log")
    st.dataframe(df.style.applymap(
        lambda x: 'background-color: #ffcccc' if x == 'FAIL' else 'background-color: #ccffcc', 
        subset=['status']
    ))

    # --- EXPORT OPTIONS ---
    st.subheader("3. Export Reports")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV Report", csv, "kolkata_audit.csv", "text/csv")