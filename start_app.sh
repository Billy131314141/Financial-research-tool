#!/bin/bash

echo "Starting Financial Research Tool..."
echo "=================================="
echo ""

cd "/Users/makwinglai/Desktop/Financial research tool"

echo "Checking Python version..."
python --version
echo ""

echo "Checking Streamlit installation..."
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
echo ""

echo "Starting Streamlit application..."
echo "Please open your browser to the URL shown below"
echo ""

streamlit run main.py


