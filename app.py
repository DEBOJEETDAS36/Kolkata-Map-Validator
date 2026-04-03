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



# import streamlit as st
# import pandas as pd
# from src.engine import GeoAuditEngine

# # --- DASHBOARD CONFIGURATION ---
# st.set_page_config(page_title="GeoAudit Kolkata", layout="wide")
# st.title("📍 GeoAudit Kolkata: Market-Ready MVP")
# st.markdown("Professional Geospatial Validation for Logistics & Mapping Operations.")

# # --- INITIALIZE SESSION STATE ---
# # This keeps your data persistent across button clicks
# if 'audit_df' not in st.session_state:
#     st.session_state.audit_df = None
# if 'engine_instance' not in st.session_state:
#     st.session_state.engine_instance = None

# # --- SIDEBAR CONTROLS ---
# st.sidebar.header("Audit Settings")
# threshold = st.sidebar.slider("Accuracy Threshold (km)", 0.1, 2.0, 0.5)

# st.sidebar.subheader("💰 Financial Settings")
# cost_per_km = st.sidebar.number_input("Cost per KM (₹)", value=12.0)

# # --- MAIN INTERFACE ---
# st.subheader("1. Run Live Batch Audit")

# if st.button("Start Kolkata Audit", key="run_main_audit"):
#     # Initialize engine and run logic
#     engine = GeoAuditEngine(threshold=threshold)
#     engine.run_batch_audit("data/landmarks.json")
    
#     # Save to session state
#     st.session_state.audit_df = pd.DataFrame(engine.audit_results)
#     st.session_state.engine_instance = engine
#     st.success("Audit Completed Successfully!")

# # --- DISPLAY RESULTS (Only if audit has been run) ---
# if st.session_state.audit_df is not None:
#     df = st.session_state.audit_df
#     engine = st.session_state.engine_instance

#     # 1. Metrics
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Audited", len(df))
#     col2.metric("Failed Routes", len(df[df['status'] == 'FAIL']))
#     col3.metric("Avg Variance (km)", round(df['variance_km'].mean(), 2))

#     # 2. Map View
#     st.subheader("2. Spatial Distribution of Audit Points")
#     st.map(df[['lat', 'lon']])

#     # -- Chart View ---

# if st.session_state.audit_df is not None:
#     df = st.session_state.audit_df
    
#     st.subheader("4. Distance Comparison Analysis")
    
#     # Prepare data for the chart
#     chart_data = df[['name', 'crow_flies_km', 'actual_road_km', 'reported_km']]
#     chart_data = chart_data.set_index('name')
    
#     # Display the Comparison Bar Chart
#     st.bar_chart(chart_data)
    
#     st.info("💡 **Insight:** If 'Reported KM' is significantly lower than 'Actual Road KM', the driver is being underpaid for that route.")

#     # 3. Data Table
#     st.subheader("3. Detailed Audit Log")
#     st.dataframe(df.style.map(
#         lambda x: 'background-color: #ffcccc' if x == 'FAIL' else 'background-color: #ccffcc', 
#         subset=['status']
#     ))

#     # Calculate total overpayment based on variance
#     total_overpayment = (df['variance_km'] * cost_per_km).sum()
#     col3.metric("Est. Payout Variance", f"₹{round(total_overpayment, 2)}")

#     # 4. Export Options
#     st.divider()
#     st.subheader("4. Export Professional Reports")
    
#     col_csv, col_pdf = st.columns(2)
    
#     with col_csv:
#         csv_data = df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="📊 Download CSV Report",
#             data=csv_data,
#             file_name="kolkata_audit.csv",
#             mime="text/csv",
#             key="csv_download"
#         )

#     with col_pdf:
#         # Generate the PDF buffer from the engine saved in session state
#         pdf_buffer = engine.export_pdf_buffer()
#         st.download_button(
#             label="📥 Download PDF Certificate",
#             data=pdf_buffer,
#             file_name="GeoAudit_Kolkata_Report.pdf",
#             mime="application/pdf",
#             key="pdf_download"
#         )


import streamlit as st
import pandas as pd
from src.engine import GeoAuditEngine

# --- DASHBOARD CONFIGURATION ---
st.set_page_config(
    page_title="GeoAudit Kolkata | Logistics Validator", 
    page_icon="📍", 
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📍 GeoAudit Kolkata: Market-Ready MVP")
st.markdown("### Professional Geospatial Validation for Logistics & Mapping Operations.")

# --- INITIALIZE SESSION STATE ---
# Crucial for preventing data loss during PDF/CSV downloads
if 'audit_df' not in st.session_state:
    st.session_state.audit_df = None
if 'engine_instance' not in st.session_state:
    st.session_state.engine_instance = None

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Audit Settings")
    threshold = st.sidebar.slider("Accuracy Threshold (km)", 0.1, 2.0, 0.5, 
                                help="Maximum allowed gap before flagging a 'FAIL'")
    
    st.divider()
    st.subheader("💰 Financial Settings")
    cost_per_km = st.sidebar.number_input("Cost per KM (₹)", value=12.0, step=0.5)
    st.info("Used to calculate estimated payout variance for logistics partners.")

# --- MAIN INTERFACE: BATCH AUDIT ---
st.subheader("1. Run Live Batch Audit")
st.info("This engine compares Geodesic (Crow-flies) vs. OSRM (Actual Road) vs. App Reported distance.")

if st.button("🚀 Start Kolkata Audit", key="run_main_audit"):
    with st.spinner("Accessing OSRM Routing Engine..."):
        # Initialize engine and run logic
        engine = GeoAuditEngine(threshold=threshold)
        engine.run_batch_audit("data/landmarks.json")
        
        # Save results to session state to make them persistent
        st.session_state.audit_df = pd.DataFrame(engine.audit_results)
        st.session_state.engine_instance = engine
        st.success("Audit Completed Successfully!")

# --- DISPLAY RESULTS ---
if st.session_state.audit_df is not None:
    df = st.session_state.audit_df
    engine = st.session_state.engine_instance

    if not df.empty and 'status' in df.columns:
        # 1. KEY PERFORMANCE INDICATORS (KPIs)
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Audited", len(df))
        
        failed_count = len(df[df['status'] == 'FAIL'])
        col2.metric(
            "Failed Routes", 
            failed_count, 
            delta="Action Required" if failed_count > 0 else "Optimal", 
            delta_color="inverse" if failed_count > 0 else "normal"
        )
        
        avg_var = round(df['variance_km'].mean(), 2)
        col3.metric("Avg Variance (km)", f"{avg_var} km")
        
        # Calculate Total Financial Impact
        total_loss = round((df['variance_km'] * cost_per_km).sum(), 2)
        col4.metric("Est. Payout Variance", f"₹{total_loss}")

        # 2. VISUALIZATIONS
        tab1, tab2 = st.tabs(["🗺️ Spatial Distribution", "📊 Distance Comparison"])
        
        with tab1:
            st.subheader("Geospatial Failures in Kolkata")
            # Filter for fails to highlight problem areas
            st.map(df[['lat', 'lon']])

        with tab2:
            st.subheader("Routing Analysis: Road vs. App")
            chart_cols = ['name', 'crow_flies_km', 'actual_road_km', 'reported_km']
            if all(c in df.columns for c in chart_cols):
                chart_df = df[chart_cols].set_index('name')
                st.bar_chart(chart_df)
            else:
                st.warning("Comparison data incomplete. Check OSRM connectivity.")

        # 3. DETAILED DATA TABLE
        st.subheader("4. Detailed Audit Log")
        # Using .map() to avoid the deprecated .applymap() error
        st.dataframe(
            df.style.map(
                lambda x: 'background-color: #ffcccc' if x == 'FAIL' else 'background-color: #ccffcc', 
                subset=['status']
            ),
            use_container_width=True
        )

        # 4. EXPORT OPTIONS
        st.divider()
        st.subheader("5. Export Enterprise Reports")
        c1, c2 = st.columns(2)
        
        with c1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 Download CSV Report", 
                data=csv, 
                file_name="kolkata_audit_data.csv", 
                mime="text/csv", 
                key="csv_dl",
                use_container_width=True
            )
            
        with c2:
            try:
                pdf_buffer = engine.export_pdf_buffer()
                st.download_button(
                    label="📥 Download PDF Certificate", 
                    data=pdf_buffer, 
                    file_name="GeoAudit_Kolkata_Certificate.pdf", 
                    mime="application/pdf", 
                    key="pdf_dl",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF Generation failed: {e}")
            
    else:
        st.warning("No data found. Please check your landmarks.json format.")

else:
    st.info("Click 'Start Kolkata Audit' to generate the geospatial report.")