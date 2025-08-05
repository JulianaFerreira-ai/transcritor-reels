#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
venv/bin/python -m streamlit run app.py
