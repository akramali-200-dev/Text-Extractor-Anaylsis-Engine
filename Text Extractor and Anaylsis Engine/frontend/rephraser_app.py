"""
Streamlit application for academic text rephrasing.
"""
import asyncio
import streamlit as st
from config.settings import settings
from services.ai_service import ai_service
from frontend.components import (
    apply_academic_theme, display_app_header, display_chat_message
)


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Athena – Research Writing Mentor",
        page_icon="🎓",
        layout="centered",
    )
    
    # Apply theme
    apply_academic_theme()
    
    # Display header
    display_app_header(
        "Athena",
        "Your Personal Research Writing Mentor"
    )
    
    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    
    # Display conversation
    with st.container():
        for msg in st.session_state.messages:
            display_chat_message(msg["role"], msg["content"])
    
    # Input box
    st.session_state.user_input = st.text_area(
        "Enter your research text or question:", 
        st.session_state.user_input, 
        height=120
    )
    
    # Submit button
    col1, col2 = st.columns([5, 1])
    with col2:
        submit = st.button("Discuss", use_container_width=True)
    
    # Handle submission
    if submit and st.session_state.user_input.strip():
        user_text = st.session_state.user_input
        st.session_state.messages.append({"role": "user", "content": user_text})
        st.session_state.user_input = ""  # Clear input after submission
        
        with st.spinner("Athena is analyzing and refining your text..."):
            try:
                # Run async function in sync context
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                bot_reply = loop.run_until_complete(
                    ai_service.rephrase_text(
                        user_text, 
                        st.session_state.messages[:-1]  # Exclude the current user message
                    )
                )
                loop.close()
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()


if __name__ == "__main__":
    main()
