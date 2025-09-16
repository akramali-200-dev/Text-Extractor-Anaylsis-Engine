"""
Shared frontend components for Streamlit applications.
"""
import streamlit as st
from typing import Dict, Any


def apply_extractor_theme():
    """Apply modern tech theme for extractor application."""
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            font-family: 'Inter', sans-serif;
            color: #e0e0e0;
        }
        .main {
            padding: 2rem;
            background: rgba(20, 20, 20, 0.9);
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }
        .title {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 0.3em;
            color: #00eaff;
            text-align: center;
        }
        .subtitle {
            font-size: 1.15em;
            margin-bottom: 2em;
            color: #cccccc;
            text-align: center;
        }
        .stButton button {
            width: 100%;
            background: linear-gradient(90deg, #00eaff, #0077ff);
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 0.6em;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #0077ff, #00eaff);
            transform: translateY(-2px);
        }
        textarea {
            border-radius: 10px !important;
            border: 1px solid #444 !important;
            padding: 12px !important;
            font-size: 1em !important;
            background: rgba(30, 30, 30, 0.9) !important;
            color: #e0e0e0 !important;
            font-family: 'Inter', sans-serif !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_academic_theme():
    """Apply elegant academic theme for rephraser application."""
    st.markdown(
        """
        <style>
        body {
            background: #fefefe;
            font-family: 'Merriweather', serif;
            color: #2c2c2c;
        }
        .main {
            padding: 2rem;
            background: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }
        .assistant {
            background: #fafafa;
            color: #2c2c2c;
            padding: 1em;
            border-left: 4px solid #4B8BBE;
            border-radius: 8px;
            margin-bottom: 1em;
            font-size: 1.05em;
        }
        .user {
            background: #f0f7ff;
            color: #2c2c2c;
            padding: 1em;
            border-left: 4px solid #1E88E5;
            border-radius: 8px;
            margin-bottom: 1em;
            font-size: 1.05em;
        }
        .title {
            font-size: 2.2em;
            font-weight: bold;
            margin-bottom: 0.3em;
            color: #1E1E1E;
            text-align: center;
        }
        .subtitle {
            font-size: 1.15em;
            margin-bottom: 2em;
            color: #555555;
            text-align: center;
        }
        .stButton button {
            width: 100%;
            background: #1E88E5;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 0.6em;
            font-size: 1em;
            transition: background 0.3s ease;
        }
        .stButton button:hover {
            background: #1669bb;
        }
        textarea {
            border-radius: 8px !important;
            border: 1px solid #ddd !important;
            padding: 10px !important;
            font-size: 1em !important;
            font-family: 'Georgia', serif !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def display_app_header(title: str, subtitle: str):
    """Display application header with title and subtitle."""
    st.markdown(f'<div class="title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)


def display_analysis_results(data: Dict[str, Any]):
    """Display analysis results in a formatted way."""
    st.success("Analysis Complete!")
    
    st.subheader("Summary")
    st.write(data.get("summary", "No summary found."))
    
    st.subheader("Metadata")
    st.json({
        "Title": data.get("title"),
        "Topics": data.get("topics"),
        "Sentiment": data.get("sentiment"),
        "Keywords": data.get("keywords"),
        "Created At": data.get("created_at"),
    })


def display_search_results(results: Dict[str, Any]):
    """Display search results in a formatted way."""
    st.success(f"Found {results['count']} results")
    
    for item in results["results"]:
        with st.expander(item.get("title") or "Untitled"):
            st.write(f"**Summary:** {item.get('summary')}")
            st.json(item)


def display_chat_message(role: str, content: str):
    """Display chat message with appropriate styling."""
    if role == "user":
        st.markdown(f"<div class='user'><strong>You:</strong><br>{content}</div>", unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"<div class='assistant'><strong>Athena:</strong><br>{content}</div>", unsafe_allow_html=True)
