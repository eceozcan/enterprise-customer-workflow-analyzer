import streamlit as st
import pandas as pd
import json
from langchain_community.llms import Ollama

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Enterprise AI Customer Insights & Workflow",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Initialization (History and Theme)
if "history" not in st.session_state:
    st.session_state.history = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"  # Default theme

# ---------------------------------------------------------
# 2. SIDEBAR & THEME SELECTION
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=64)
    st.title("System Settings")
    
    # 🌙 / ☀️ THEME TOGGLE
    st.subheader("🎨 Appearance Theme")
    theme_option = st.radio(
        "Select Theme:",
        ["🌙 Dark Mode", "☀️ Light Mode"],
        index=0 if st.session_state.theme == "dark" else 1
    )
    st.session_state.theme = "dark" if "Dark" in theme_option else "light"

    st.divider()

    st.caption("Local LLM & Pipeline Controls")
    selected_model = st.selectbox("Select LLM Model", ["qwen2.5", "llama3.2"], index=0)
    temperature = st.slider("Model Creativity (Temperature)", 0.0, 1.0, 0.1, step=0.05)
    
    st.divider()
    
    st.subheader("✉️ Response Draft Settings")
    response_tone = st.radio(
        "Customer Response Tone:",
        ["Corporate & Formal 🏢", "Empathetic & Friendly 🤝", "Concise & Solution-Oriented ⚡"]
    )
    
    st.divider()
    if st.button("🗑️ Clear Analysis History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ---------------------------------------------------------
# 3. DYNAMIC THEME & CSS INJECTION (FULL-SCREEN THEME COMPATIBILITY)
# ---------------------------------------------------------
if st.session_state.theme == "dark":
    # 🌙 DARK MODE
    st.markdown("""
        <style>
        /* Main Background & Text Colors */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d !important;
        }
        /* Metric Cards */
        .stMetric {
            background-color: #1f2937 !important;
            border: 1px solid #374151 !important;
            border-radius: 10px;
            padding: 12px;
        }
        .stMetric label, .stMetric [data-testid="stMetricValue"] {
            color: #f9fafb !important;
        }
        /* Textarea and Input Fields */
        textarea, input {
            background-color: #1f2937 !important;
            color: #f9fafb !important;
            border: 1px solid #4b5563 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    # ☀️ LIGHT MODE
    st.markdown("""
        <style>
        /* Main Background & Text Colors */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        /* Metric Cards */
        .stMetric {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px;
            padding: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .stMetric label, .stMetric [data-testid="stMetricValue"] {
            color: #0f172a !important;
        }
        /* Textarea and Input Fields */
        textarea, input {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Ollama Connection
llm = Ollama(model=selected_model, temperature=temperature)

# ---------------------------------------------------------
# 4. MAIN HEADER & METRICS (DASHBOARD HEAD)
# ---------------------------------------------------------
st.title("⚡ Enterprise Customer Workflow Analyzer")
st.caption("Multi-Step Customer Experience Analytics Dashboard Powered by Local LLMs & Ollama")

# Live Analytics Metrics
m1, m2, m3, m4 = st.columns(4)
total_analyzed = len(st.session_state.history)

with m1:
    st.metric("Total Analyzed", total_analyzed)
with m2:
    high_urgency = sum(1 for item in st.session_state.history if item.get("urgency") in ["High", "Yüksek"])
    st.metric("High Urgency 🚨", high_urgency)
with m3:
    negative_count = sum(1 for item in st.session_state.history if item.get("sentiment") in ["Negative", "Mixed", "Olumsuz", "Karmaşık"])
    st.metric("Action Required ⚠️", negative_count)
with m4:
    st.metric("Active Engine", f"{selected_model.upper()} (Local)")

st.divider()

# ---------------------------------------------------------
# 5. TAB STRUCTURE
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📝 Single Review Analysis", "📁 Batch CSV Analysis", "📊 History & Export"])

# ---------------------------------------------------------
# TAB 1: SINGLE REVIEW ANALYSIS
# ---------------------------------------------------------
with tab1:
    col_in, col_out = st.columns([1, 1], gap="medium")
    
    with col_in:
        st.subheader("🔍 Customer Input")
        default_text = "I ordered the product last week. Delivery was super fast and packaging was great. However, the battery drains much faster than expected, so I am a bit disappointed."
        user_input = st.text_area("Paste Customer Feedback to Analyze:", value=default_text, height=150)
        
        run_btn = st.button("Run Workflow 🚀", type="primary", use_container_width=True)

    if run_btn:
        if not user_input.strip():
            st.warning("Please enter text for analysis.")
        else:
            with col_out:
                st.subheader("⚙️ Workflow Running...")
                
                # Step 1: Summarization
                with st.spinner("1/3: Summarizing Text..."):
                    prompt_summary = f"Summarize the following customer feedback in English in exactly 1 or 2 sentences. Do not add explanations:\n\n{user_input}"
                    summary_res = llm.invoke(prompt_summary).strip()

                # Step 2: Sentiment and Category Analysis (JSON)
                with st.spinner("2/3: Generating Structured JSON Analysis..."):
                    prompt_analysis = f"""Analyze the text below. Return ONLY a valid JSON object.
JSON Template:
{{
  "sentiment": "Positive / Negative / Neutral / Mixed",
  "category": "Shipping / Product Quality / Customer Service / Price / Other",
  "urgency": "High / Medium / Low"
}}
Text: {user_input}"""
                    analysis_raw = llm.invoke(prompt_analysis).strip()
                    
                    try:
                        clean_json = analysis_raw.replace("```json", "").replace("```", "").strip()
                        parsed_json = json.loads(clean_json)
                    except:
                        parsed_json = {"sentiment": "Mixed", "category": "Product Quality", "urgency": "Medium"}

                # Step 3: Response Draft Generation
                with st.spinner("3/3: Drafting Customer Response..."):
                    prompt_reply = f"""You are a Customer Relations Representative.
Specified Tone: {response_tone}
Write an email response to the customer feedback below.
Rules:
1. Write ONLY in English.
2. Strictly adhere to the selected tone ({response_tone}).
3. Focus on resolving the issue politely and professionally with a standard corporate closing (e.g., "Best regards,").

Customer Feedback: {user_input}"""
                    reply_res = llm.invoke(prompt_reply).strip()

                # Save Record to Session State
                record = {
                    "text": user_input,
                    "summary": summary_res,
                    "sentiment": parsed_json.get("sentiment", "Neutral"),
                    "category": parsed_json.get("category", "Other"),
                    "urgency": parsed_json.get("urgency", "Medium"),
                    "response": reply_res
                }
                st.session_state.history.append(record)

                st.success("✅ Workflow Completed!")
                st.divider()
                
                st.markdown("**📌 Summary:**")
                st.info(summary_res)
                
                st.markdown("**📊 Structured Analysis:**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Sentiment", parsed_json.get("sentiment"))
                c2.metric("Category", parsed_json.get("category"))
                c3.metric("Urgency", parsed_json.get("urgency"))
                
                st.markdown("**✉️ Drafted Response:**")
                st.success(reply_res)

# ---------------------------------------------------------
# TAB 2: BATCH CSV ANALYSIS
# ---------------------------------------------------------
with tab2:
    st.subheader("📂 Batch Analysis via CSV File")
    st.caption("Upload a CSV file containing a 'review' or 'feedback' column.")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("📋 **Uploaded Data Preview:**", df.head(3))
        
        target_col = st.selectbox("Select Target Feedback Column:", df.columns)
        
        if st.button("Start Batch Analysis ⚡", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            total_rows = len(df)
            
            for idx, row in df.iterrows():
                text = str(row[target_col])
                status_text.text(f"Processing ({idx+1}/{total_rows}): {text[:40]}...")
                
                prompt = f"""Analyze the following text. Output ONLY a valid JSON:
{{"summary": "1 sentence summary", "sentiment": "Positive/Negative/Mixed", "category": "Shipping/Product Quality/Other", "urgency": "High/Medium/Low"}}
Text: {text}"""
                
                res = llm.invoke(prompt)
                try:
                    clean_res = res.replace("```json", "").replace("```", "").strip()
                    parsed = json.loads(clean_res)
                except:
                    parsed = {"summary": "Could not extract summary", "sentiment": "Neutral", "category": "Other", "urgency": "Low"}
                
                results.append(parsed)
                st.session_state.history.append({"text": text, **parsed, "response": "Skipped in batch mode"})
                progress_bar.progress((idx + 1) / total_rows)
                
            status_text.success("🎉 All CSV Rows Analyzed Successfully!")
            
            res_df = pd.DataFrame(results)
            final_df = pd.concat([df, res_df], axis=1)
            st.dataframe(final_df, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: ANALYSIS HISTORY & EXPORT
# ---------------------------------------------------------
with tab3:
    st.subheader("📜 Complete Analysis History")
    
    if len(st.session_state.history) == 0:
        st.info("No analysis has been performed yet.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True)
        
        st.divider()
        col_dl1, col_dl2 = st.columns(2)
        
        csv_data = history_df.to_csv(index=False).encode('utf-8')
        col_dl1.download_button(
            label="📥 Export Results as CSV",
            data=csv_data,
            file_name="ai_analysis_results.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        json_data = json.dumps(st.session_state.history, ensure_ascii=False, indent=2)
        col_dl2.download_button(
            label="📥 Export Results as JSON",
            data=json_data,
            file_name="ai_analysis_results.json",
            mime="application/json",
            use_container_width=True
        )