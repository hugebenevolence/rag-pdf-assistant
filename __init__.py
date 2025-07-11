# __init__.py
"""
SQLite fix for Streamlit Cloud deployment
"""

import sys
import os

# Fix SQLite version for ChromaDB on Streamlit Cloud
try:
    # Check if we're on Streamlit Cloud
    if os.getenv('STREAMLIT_CLOUD') or 'streamlit' in sys.modules:
        # Try to import pysqlite3 first
        try:
            import pysqlite3
            sys.modules['sqlite3'] = pysqlite3
        except ImportError:
            # If pysqlite3 is not available, try to continue with system sqlite3
            import sqlite3
            # Check SQLite version
            if sqlite3.sqlite_version_info < (3, 35, 0):
                print("⚠️ Warning: SQLite version is older than 3.35.0. ChromaDB may not work properly.")
                print(f"Current SQLite version: {sqlite3.sqlite_version}")
                print("Consider upgrading SQLite or use an alternative vector store.")
except Exception as e:
    print(f"Warning: SQLite fix failed: {e}")
    pass
