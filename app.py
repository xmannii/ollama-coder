import streamlit as st
import openai
from typing import List, Dict

from utils.models import get_local_models
from utils.prompts import LANGUAGE_PROMPTS
from components.sidebar import render_sidebar

# Configure OpenAI client for Ollama
client = openai.OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'  # required but unused
)

def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'settings' not in st.session_state:
        st.session_state.settings = None

def display_chat_history():
    """Display chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_system_prompt(settings: dict) -> str:
    """Generate system prompt based on settings"""
    language_prompt = LANGUAGE_PROMPTS.get(settings['language'], "")
    return f"""You are a helpful coding assistant. {language_prompt}
              Provide clear, well-commented code examples.
              Format code blocks with proper markdown syntax using triple backticks."""

def main():
    st.set_page_config(
        page_title="Maux Local AI Code Assistant",
        page_icon="🤖",
        layout="wide"
    )

    # Add Maux branding
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🤖 Maux Local AI Code Assistant")
    with col2:
        st.markdown("""
        <div style='text-align: right; padding-top: 20px;'>
            <a href='https://ai.maux.space' target='_blank' style='color: #FF4B4B;'>
                Try our hosted version ↗
            </a>
        </div>
        """, unsafe_allow_html=True)

    init_session_state()
    
    # Render sidebar and get settings
    models = get_local_models()
    settings = render_sidebar(models)
    st.session_state.settings = settings

    # Display chat history
    display_chat_history()

    # Chat input
    if prompt := st.chat_input("Ask your coding question..."):
        if not settings['model']:
            st.error("Please select a model first!")
            st.stop()

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Get context window messages
                context_messages = st.session_state.messages[-settings['context_window']:]
                
                stream = client.chat.completions.create(
                    model=settings['model'],
                    messages=[
                        {"role": "system", "content": get_system_prompt(settings)},
                        *[{"role": m["role"], "content": m["content"]} for m in context_messages]
                    ],
                    stream=True,
                    temperature=settings['temperature'],
                    max_tokens=settings['max_tokens'],
                    top_p=settings['top_p']
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main() 