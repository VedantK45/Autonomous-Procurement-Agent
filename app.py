import streamlit as st
import os
import json
import time
import sys
import re
from io import StringIO
from main_logic import run_intelligence_crew

st.set_page_config(page_title="IntelSentry AI", layout="wide")

# 1. Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_seen_background_time" not in st.session_state:
    st.session_state.last_seen_background_time = 0
if "active_query" not in st.session_state:
    st.session_state.active_query = None

st.title("🛡️ Universal Intelligence Sentry")

# Sidebar for Thinking Process
with st.sidebar:
    st.header("🧠 Agent Thinking Process")
    log_area = st.empty()
    st.info("The agents use a hierarchical process where the Manager delegates to Specialists.")

# --- THE AUTO-REFRESH & UPDATE LOGIC (FOR WATCHER) ---
if os.path.exists("background_results.json"):
    with open("background_results.json", "r") as f:
        try:
            data = json.load(f)
        except:
            data = []
    
    if data and data[-1]["timestamp"] > st.session_state.last_seen_background_time:
        latest_entry = data[-1]
        st.session_state.last_seen_background_time = latest_entry["timestamp"]
        
        if st.session_state.active_query:
            st.toast(f"🔄 New file detected: {latest_entry['file_name']}. Re-analyzing...", icon="📂")
            
            with st.spinner(f"Updating results with {latest_entry['file_name']}..."):
                # Capturing Logs for Sidebar
                old_stdout = sys.stdout
                sys.stdout = mystdout = StringIO()
                
                # Re-run the STANDING query
                result_dict = run_intelligence_crew(st.session_state.active_query)
                
                sys.stdout = old_stdout
                log_area.code(mystdout.getvalue())
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result_dict["answer"],
                    "metadata": {
                        "time": result_dict["time_taken"], 
                        "sources": result_dict["sources"], 
                        "accuracy": result_dict["accuracy"]
                    }
                })
            st.rerun()

# --- DISPLAY CHAT WITH ADD-ONS ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        if msg["role"] == "assistant" and "metadata" in msg:
            m = msg["metadata"]
            cols = st.columns(3)
            cols[0].caption(f"⏱️ Time: {m['time']}s")
            cols[1].caption(f"🎯 Accuracy: {m['accuracy']}%")
            cols[1].progress(m['accuracy'] / 100)
            src_text = ", ".join(m['sources']) if m['sources'] else "Direct Knowledge"
            cols[2].caption(f"📂 Sources: {src_text}")

# --- MANUAL INPUT ---
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.active_query = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Thinking Status Container
        with st.status("🛠️ Agents are thinking...", expanded=False) as status:
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            
            # CALLING MAIN LOGIC (Returns Dictionary)
            result_dict = run_intelligence_crew(prompt)
            
            sys.stdout = old_stdout
            log_area.code(mystdout.getvalue())
            status.update(label="✅ Analysis Complete", state="complete")
        
        # Display the Main Answer
        st.markdown(result_dict["answer"])
        
        # Display Add-ons using dictionary data
        addon_cols = st.columns(3)
        addon_cols[0].metric("Generation Time", f"{result_dict['time_taken']}s")
        addon_cols[1].metric("Accuracy Score", f"{result_dict['accuracy']}%")
        
        source_display = ", ".join(result_dict["sources"]) if result_dict["sources"] else "General Scan"
        addon_cols[2].write(f"**Sources Found:**\n{source_display}")

        # Store in session state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result_dict["answer"],
            "metadata": {
                "time": result_dict["time_taken"], 
                "sources": result_dict["sources"],
                "accuracy": result_dict["accuracy"]
            }
        })