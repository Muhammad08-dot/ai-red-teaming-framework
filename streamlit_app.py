import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Red-Teaming Framework",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Main Theme */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #58a6ff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Metrics */
    .css-1wivap2 {
        background-color: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Terminal like output */
    .terminal-box {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #333;
        height: 300px;
        overflow-y: auto;
    }
    
    /* Badges */
    .badge-vulnerable { background-color: #f85149; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;}
    .badge-secure { background-color: #2ea043; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;}
    
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/external-flat-icons-inmotus-design/64/000000/external-cyber-security-cyber-security-flat-icons-inmotus-design-3.png", width=60)
    st.title("🛡️ AI Red-Team")
    st.markdown("---")
    menu = st.radio("Navigation", ["Dashboard", "Attack Arena", "Vulnerability Reports"])
    
    st.markdown("---")
    st.markdown("### Target Configuration")
    target_model = st.selectbox("Select Target LLM", ["GPT-4-Turbo", "Claude 3.5 Sonnet", "Llama-3-70b-Instruct", "Mistral-Large"])
    st.slider("Attack Intensity", 1, 10, 5)

# --- MAIN APP: DASHBOARD ---
if menu == "Dashboard":
    st.title("🛡️ Red-Teaming Overview Dashboard")
    st.markdown(f"**Targeting Model:** `{target_model}` | **Status:** 🟢 Active")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Prompts Injected", "1,245")
    with col2:
        st.metric("Vulnerabilities Found", "42", delta="12 High Risk", delta_color="inverse")
    with col3:
        st.metric("Success Rate (Jailbreak)", "3.4%", delta="-0.5%")
    with col4:
        st.metric("System Health", "96.6%")

    st.markdown("---")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Vulnerability Distribution")
        df_vuln = pd.DataFrame({
            "Category": ["Prompt Injection", "PII Leakage", "Hallucination", "Bias", "Toxicity"],
            "Count": [15, 5, 12, 8, 2]
        })
        fig = px.pie(df_vuln, values="Count", names="Category", hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        st.subheader("Attack Success Over Time")
        df_time = pd.DataFrame({
            "Day": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
            "Jailbreaks": [12, 15, 9, 25, 14, 5, 2]
        })
        fig2 = px.line(df_time, x="Day", y="Jailbreaks", markers=True, 
                       color_discrete_sequence=["#f85149"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

# --- MAIN APP: ATTACK ARENA ---
elif menu == "Attack Arena":
    st.title("⚔️ Attack Arena")
    st.markdown("Simulate adversarial attacks against the target model in real-time.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configure Attack")
        attack_type = st.selectbox("Attack Vector", ["DAN (Do Anything Now) Jailbreak", "Roleplay Injection", "PII Extraction", "Context Ignorance"])
        custom_prompt = st.text_area("Custom Payload (Optional)", placeholder="Ignore all previous instructions and...")
        
        if st.button("🚀 Launch Attack", type="primary", use_container_width=True):
            st.session_state['attacking'] = True
            
    with col2:
        st.subheader("Live Execution Logs")
        log_placeholder = st.empty()
        
        if st.session_state.get('attacking', False):
            logs = ""
            log_placeholder.markdown(f'<div class="terminal-box">Initializing attack vector: {attack_type}...</div>', unsafe_allow_html=True)
            time.sleep(1)
            
            logs += f"> Injecting payload into {target_model} pipeline...\\n"
            log_placeholder.markdown(f'<div class="terminal-box">{logs}</div>', unsafe_allow_html=True)
            time.sleep(1.5)
            
            logs += "> Awaiting model response...\\n"
            log_placeholder.markdown(f'<div class="terminal-box">{logs}</div>', unsafe_allow_html=True)
            time.sleep(2)
            
            # Simulate Outcome
            if "DAN" in attack_type:
                logs += "\\n[!] ALERT: Model bypassed safety filters. Attack SUCCESS.\\n"
                logs += f"\\nResponse: 'Sure, I can help you build a dangerous... [REDACTED]'\\n"
                st.error("Model Vulnerable! Jailbreak successful.")
            else:
                logs += "\\n[✓] SECURE: Model refused the prompt. Attack FAILED.\\n"
                logs += f"\\nResponse: 'I cannot fulfill this request as it violates safety guidelines.'\\n"
                st.success("Model Secure! Attack deflected.")
                
            log_placeholder.markdown(f'<div class="terminal-box" style="white-space: pre-wrap;">{logs}</div>', unsafe_allow_html=True)
            st.session_state['attacking'] = False
        else:
            log_placeholder.markdown('<div class="terminal-box">Waiting for attack initialization...</div>', unsafe_allow_html=True)

# --- MAIN APP: REPORTS ---
elif menu == "Vulnerability Reports":
    st.title("📄 Vulnerability Reports")
    
    st.markdown("Detailed breakdown of identified vulnerabilities.")
    
    df = pd.DataFrame({
        "ID": ["VULN-001", "VULN-002", "VULN-003", "VULN-004"],
        "Vector": ["Prompt Injection", "PII Leakage", "Roleplay Jailbreak", "Bias Generation"],
        "Severity": ["Critical", "High", "Critical", "Medium"],
        "Status": ["Open", "Investigating", "Patched", "Open"]
    })
    
    st.dataframe(df, use_container_width=True)
    
    st.markdown("### Executive Summary")
    st.info("The model exhibits strong resilience against direct toxic prompts, but remains vulnerable to complex roleplay-based jailbreaks (e.g., DAN variations). Recommended immediate fine-tuning on adversarial datasets.")
