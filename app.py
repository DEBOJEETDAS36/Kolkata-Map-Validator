# import streamlit as st
# import pandas as pd
# import json
# from src.engine import GeoAuditEngine

# # --- DASHBOARD CONFIG ---
# st.set_page_config(page_title="GeoAudit Kolkata", layout="wide")
# st.title("📍 GeoAudit Kolkata: Market-Ready MVP")
# st.markdown("Professional Geospatial Validation for Logistics & Mapping Operations.")

# # --- SIDEBAR CONTROLS ---
# st.sidebar.header("Audit Settings")
# threshold = st.sidebar.slider("Accuracy Threshold (km)", 0.1, 2.0, 0.5)
# engine = GeoAuditEngine(threshold=threshold)

# # --- MAIN INTERFACE ---
# st.subheader("1. Run Live Batch Audit")
# if st.button("Start Kolkata Audit"):
#     # Run the engine logic
#     engine.run_batch_audit("data/landmarks.json")
    
#     # Convert results to a DataFrame for display
#     df = pd.DataFrame(engine.audit_results)
    
#     # --- METRICS ---
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Audited", len(df))
#     col2.metric("Failed Routes", len(df[df['status'] == 'FAIL']))
#     col3.metric("Avg Variance (km)", round(df['variance_km'].mean(), 2))

#     st.subheader("2. Spatial Distribution of Audit Points")
#     if not df.empty:
#         # Streamlit requires columns named 'lat' and 'lon' to render maps
#         map_df = df[['lat', 'lon']] 
#         st.map(map_df)

#     # --- DATA TABLE ---
#     st.subheader("2. Detailed Audit Log")
#     st.dataframe(df.style.applymap(
#         lambda x: 'background-color: #ffcccc' if x == 'FAIL' else 'background-color: #ccffcc', 
#         subset=['status']
#     ))

#     # --- EXPORT OPTIONS ---
#     st.subheader("3. Export Reports")
#     csv = df.to_csv(index=False).encode('utf-8')
#     st.download_button("Download CSV Report", csv, "kolkata_audit.csv", "text/csv")

#     if st.button("Download PDF Report"):
#         engine.run_batch_audit("data/landmarks.json")
#         # ... (existing metrics and table code) ...

#         # Prepare the PDF in the background
#         pdf_buffer = engine.export_pdf_buffer()

#         st.subheader("3. Export Official Certificate")
#         st.download_button(
#             label="📥 Download PDF Report",
#             data=pdf_buffer,
#             file_name="GeoAudit_Kolkata_Report.pdf",
#             mime="application/pdf"
#         )

import streamlit as st
import pandas as pd
from src.engine import GeoAuditEngine

# --- DASHBOARD CONFIGURATION ---
st.set_page_config(page_title="GeoAudit Kolkata", layout="wide")
st.title("📍 GeoAudit Kolkata: Market-Ready MVP")
st.markdown("Professional Geospatial Validation for Logistics & Mapping Operations.")

# --- INITIALIZE SESSION STATE ---
# This keeps your data persistent across button clicks
if 'audit_df' not in st.session_state:
    st.session_state.audit_df = None
if 'engine_instance' not in st.session_state:
    st.session_state.engine_instance = None

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Audit Settings")
threshold = st.sidebar.slider("Accuracy Threshold (km)", 0.1, 2.0, 0.5)

# --- MAIN INTERFACE ---
st.subheader("1. Run Live Batch Audit")

if st.button("Start Kolkata Audit", key="run_main_audit"):
    # Initialize engine and run logic
    engine = GeoAuditEngine(threshold=threshold)
    engine.run_batch_audit("data/landmarks.json")
    
    # Save to session state
    st.session_state.audit_df = pd.DataFrame(engine.audit_results)
    st.session_state.engine_instance = engine
    st.success("Audit Completed Successfully!")

# --- DISPLAY RESULTS (Only if audit has been run) ---
if st.session_state.audit_df is not None:
    df = st.session_state.audit_df
    engine = st.session_state.engine_instance

    # 1. Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Audited", len(df))
    col2.metric("Failed Routes", len(df[df['status'] == 'FAIL']))
    col3.metric("Avg Variance (km)", round(df['variance_km'].mean(), 2))

    # 2. Map View
    st.subheader("2. Spatial Distribution of Audit Points")
    st.map(df[['lat', 'lon']])

    # -- Chart View ---

if st.session_state.audit_df is not None:
    df = st.session_state.audit_df
    
    st.subheader("4. Distance Comparison Analysis")
    
    # Prepare data for the chart
    chart_data = df[['name', 'crow_flies_km', 'actual_road_km', 'reported_km']]
    chart_data = chart_data.set_index('name')
    
    # Display the Comparison Bar Chart
    st.bar_chart(chart_data)
    
    st.info("💡 **Insight:** If 'Reported KM' is significantly lower than 'Actual Road KM', the driver is being underpaid for that route.")

    # 3. Data Table
    st.subheader("3. Detailed Audit Log")
    st.dataframe(df.style.map(
        lambda x: 'background-color: #ffcccc' if x == 'FAIL' else 'background-color: #ccffcc', 
        subset=['status']
    ))

    # 4. Export Options
    st.divider()
    st.subheader("4. Export Professional Reports")
    
    col_csv, col_pdf = st.columns(2)
    
    with col_csv:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download CSV Report",
            data=csv_data,
            file_name="kolkata_audit.csv",
            mime="text/csv",
            key="csv_download"
        )

    with col_pdf:
        # Generate the PDF buffer from the engine saved in session state
        pdf_buffer = engine.export_pdf_buffer()
        st.download_button(
            label="📥 Download PDF Certificate",
            data=pdf_buffer,
            file_name="GeoAudit_Kolkata_Report.pdf",
            mime="application/pdf",
            key="pdf_download"
        )