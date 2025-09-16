"""
Streamlit application for content analysis and extraction.
"""
import asyncio
import streamlit as st
import httpx
from config.settings import settings
from frontend.components import (
    apply_extractor_theme, display_app_header, 
    display_analysis_results, display_search_results
)


def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="Content Extractor",
        page_icon="⚡",
        layout="centered",
    )
    
    # Apply theme
    apply_extractor_theme()
    
    # Display header
    display_app_header(
        "Content Extractor",
        "Intelligent Content Comprehension & Data Extraction"
    )
    
    # Sidebar menu
    st.sidebar.title("Choose Action")
    mode = st.sidebar.radio(
        "Select an API Endpoint:", 
        ["Analyze Text (POST /analyze)", "Search Analyses (GET /search)"]
    )
    
    # Analyze Text Mode
    if mode == "Analyze Text (POST /analyze)":
        st.subheader("Analyze New Content")
        text_input = st.text_area("Paste your content to analyze:", height=200)
        
        if st.button("Run Analysis"):
            if not text_input.strip():
                st.warning("Please enter some text first.")
            else:
                with st.spinner("Analyzing content..."):
                    try:
                        # Use httpx for async HTTP requests
                        async def make_request():
                            async with httpx.AsyncClient() as client:
                                response = await client.post(
                                    f"{settings.API_BASE_URL}/analyze", 
                                    json={"text": text_input},
                                    timeout=30.0
                                )
                                return response
                        
                        # Run async request in sync context
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        response = loop.run_until_complete(make_request())
                        loop.close()
                        
                        if response.status_code == 200:
                            data = response.json()
                            display_analysis_results(data)
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Failed to connect to API: {e}")
    
    # Search Mode
    elif mode == "Search Analyses (GET /search)":
        st.subheader("Search Past Analyses")
        search_term = st.text_input("Enter keyword or topic to search:")
        
        if st.button("Search"):
            if not search_term.strip():
                st.warning("Please enter a search term first.")
            else:
                with st.spinner("Searching database..."):
                    try:
                        # Use httpx for async HTTP requests
                        async def make_search_request():
                            async with httpx.AsyncClient() as client:
                                response = await client.get(
                                    f"{settings.API_BASE_URL}/search", 
                                    params={"topic": search_term},
                                    timeout=30.0
                                )
                                return response
                        
                        # Run async request in sync context
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        response = loop.run_until_complete(make_search_request())
                        loop.close()
                        
                        if response.status_code == 200:
                            results = response.json()
                            display_search_results(results)
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Search failed: {e}")


if __name__ == "__main__":
    main()
