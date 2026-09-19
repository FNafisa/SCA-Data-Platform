import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SCA Data Platform", page_icon="📊", layout="wide")

SCA_TEAL = "#00665E"
SCA_GREEN = "#49AD5B"
SCA_GOLD = "#D6A847"

st.markdown("""
<style>
  .stApp { background: #f3f7f6; }
  [data-testid="stHeader"] { background: transparent; }
  .block-container { max-width: 1600px; padding-top: 1.4rem; }
  .platform-title { color:#102a2a; font-size:1.5rem; font-weight:800; margin:0; }
  .platform-subtitle { color:#687b79; font-size:.84rem; margin-bottom:1.25rem; }
  .section-label { color:#00877c; font-size:.72rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
  .summary-card { background:#00665e; color:white; border-radius:16px; padding:1.2rem; min-height:420px; }
  .summary-card h3 { margin:0 0 .2rem; font-size:1rem; }
  .summary-card p { color:#bfe1dc; font-size:.75rem; margin:0 0 1rem; }
  .summary-metric { border-bottom:1px solid rgba(255,255,255,.18); padding:.65rem 0; }
  .summary-metric span { color:#bfe1dc; display:block; font-size:.72rem; }
  .summary-metric strong { display:block; font-size:1.35rem; }
  div[data-testid="stMetric"] { background:white; border:1px solid #d8e4e1; border-radius:12px; padding:.75rem 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="platform-title">SCA Data Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="platform-subtitle">Saudi Contractors Authority · Phase 1 admin workspace</p>', unsafe_allow_html=True)

st.markdown('<div class="section-label">01 · Metadata</div>', unsafe_allow_html=True)
st.subheader("Membership dataset")
metadata = st.columns(5)
metadata[0].metric("Data product", "Contractors Memberships")
metadata[1].metric("Actual income", "257.3M SAR")
metadata[2].metric("Total registrants", "1,749")
metadata[3].metric("Active registrants", "1,157")
metadata[4].metric("Quality status", "96.4%")

st.divider()
st.markdown('<div class="section-label">02 · Visuals</div>', unsafe_allow_html=True)
st.subheader("Contractors membership overview")

summary_col, visuals_col = st.columns([1, 3], gap="large")
with summary_col:
    st.markdown("""
    <div class="summary-card">
      <h3>Membership summary</h3><p>Aggregated figures for the selected period</p>
      <div class="summary-metric"><span>Total registrants</span><strong>1,749</strong></div>
      <div class="summary-metric"><span>Active registrants</span><strong>1,157</strong></div>
      <div class="summary-metric"><span>Contractors</span><strong>1,721</strong></div>
      <div class="summary-metric"><span>Affiliates</span><strong>28</strong></div>
      <div class="summary-metric"><span>Actual income</span><strong>257.3M</strong></div>
    </div>
    """, unsafe_allow_html=True)

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
data = pd.DataFrame({
    "Month": months,
    "Registrations 2025": [72,96,84,110,89,101,65,61,118,141,132,145],
    "Registrations 2026": [88,122,101,139,108,127,79,74,146,172,161,178],
    "Transaction amount": [3.9,3.5,3.3,5.4,4.7,5.1,5.3,5.3,2.3,0,0,0],
    "Expected renewals": [1638,1415,1173,1047,1370,1107,1645,1703,12897,14398,15090,15041],
    "Actual renewals": [141,371,280,162,259,195,190,111,21,13,9,19],
})

with visuals_col:
    f1, f2, f3 = st.columns(3)
    year = f1.selectbox("Year", [2026, 2025, 2024])
    period = f2.selectbox("Period", ["Year to date", "Last 90 days", "Last 12 months"])
    registrant = f3.selectbox("Registrant", ["All types", "Contractors", "Affiliates"])

    tabs = st.tabs(["Registrations", "Transactions", "Renewals", "Registrant types", "Status"])
    with tabs[0]:
        fig = px.bar(data, x="Month", y=["Registrations 2025", "Registrations 2026"], barmode="group", color_discrete_sequence=[SCA_TEAL, SCA_GOLD])
        fig.update_layout(height=370, legend_title_text="", margin=dict(l=10,r=10,t=25,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with tabs[1]:
        fig = px.line(data, x="Month", y="Transaction amount", markers=True, color_discrete_sequence=[SCA_GREEN])
        fig.update_layout(height=370, yaxis_title="Amount (M SAR)", margin=dict(l=10,r=10,t=25,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with tabs[2]:
        fig = px.bar(data, x="Month", y=["Expected renewals", "Actual renewals"], barmode="group", color_discrete_sequence=[SCA_GREEN, SCA_TEAL])
        fig.update_layout(height=370, legend_title_text="", margin=dict(l=10,r=10,t=25,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with tabs[3]:
        types = pd.DataFrame({"Type":["SC-0-5","SC-6-49","SC-50-249","SC-250UP","NSC","Individual"],"Count":[239,1084,9,3,386,28]})
        fig = px.bar(types, x="Count", y="Type", orientation="h", color_discrete_sequence=[SCA_TEAL])
        fig.update_layout(height=370, margin=dict(l=10,r=10,t=25,b=10))
        st.plotly_chart(fig, use_container_width=True)
    with tabs[4]:
        fig = go.Figure(go.Pie(labels=["Paid","Not paid","Pending"], values=[1157,592,4], hole=.6, marker_colors=[SCA_TEAL,SCA_GREEN,SCA_GOLD]))
        fig.update_layout(height=370, margin=dict(l=10,r=10,t=25,b=10))
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown('<div class="section-label">03 · Configuration</div>', unsafe_allow_html=True)
st.subheader("Prepare the data view")
left, right = st.columns([3, 2], gap="large")
with left:
    c1, c2 = st.columns(2)
    c1.selectbox("Primary dimension", ["Registration month", "Membership type", "Region"])
    c2.selectbox("Metric", ["Active memberships", "Transaction amount", "Renewal rate"])
    c3, c4 = st.columns(2)
    c3.selectbox("Date range", ["Year to date", "Last 90 days", "Last 12 months"])
    c4.text_input("Filter", placeholder="e.g. status = active")
    st.multiselect("Transformation steps", ["Remove duplicates", "Standardize membership classes", "Handle missing values"], default=["Remove duplicates", "Standardize membership classes"])
with right:
    st.metric("Input", "24,892 rows")
    st.metric("Estimated output", "24,106 rows")
    if st.button("Run transformation", type="primary", use_container_width=True):
        st.success("View refreshed successfully")
