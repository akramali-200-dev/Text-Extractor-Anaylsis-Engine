"""
Main application entry point and CLI interface.
"""
import sys
import argparse
import subprocess
import asyncio
from pathlib import Path


def run_api():
    """Run the FastAPI server."""
    print("Starting Content Analysis API...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "api.content_analysis_api:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--reload"
    ])


def run_extractor():
    """Run the extractor Streamlit app."""
    print("Starting Content Extractor...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "frontend/extractor_app.py"
    ])


def run_rephraser():
    """Run the rephraser Streamlit app."""
    print("Starting Athena Rephraser...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "frontend/rephraser_app.py"
    ])


async def test_api():
    """Test the API functionality."""
    print("Testing API functionality...")
    from api.content_analysis_api import test_api
    return await test_api()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Chatbot Application CLI")
    parser.add_argument(
        "command", 
        choices=["api", "extractor", "rephraser", "test"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "api":
        run_api()
    elif args.command == "extractor":
        run_extractor()
    elif args.command == "rephraser":
        run_rephraser()
    elif args.command == "test":
        # Run async test function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_api())
        loop.close()
        return result


if __name__ == "__main__":
    main()
