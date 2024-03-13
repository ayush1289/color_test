#!/bin/bash

# Update package lists and install necessary packages
sudo apt update
sudo apt install -y python3-pip

# Install Python dependencies using pip
pip3 install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py
