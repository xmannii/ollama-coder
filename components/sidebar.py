import streamlit as st
from utils.prompts import LANGUAGE_PROMPTS

def render_sidebar(models: list):
    with st.sidebar:
        st.header("Settings")
        
        # Model Selection
        if not models:
            st.error("⚠️ No local models found. Please make sure Ollama is running and you have models installed.")
            st.stop()
        
        selected_model = st.selectbox(
            "Select Model",
            models,
            index=0 if models else None,
            key="model_selector"
        )
        
        # Optional Language Selection
        selected_language = st.selectbox(
            "Programming Language (Optional)",
            list(LANGUAGE_PROMPTS.keys()),
            index=0,  # Default to Any/General
            key="language_selector"
        )
        
        # Advanced Settings
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                help="Higher values make output more creative, lower values more focused"
            )
            
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=100,
                max_value=4000,
                value=2000,
                help="Maximum length of the response"
            )
            
            top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                help="Nucleus sampling threshold"
            )
            
            context_window = st.number_input(
                "Context Window",
                min_value=1,
                max_value=10,
                value=4,
                help="Number of previous messages to include as context"
            )
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### Quick Actions")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
            

        return {
            "model": selected_model,
            "language": selected_language,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "context_window": context_window
        } 