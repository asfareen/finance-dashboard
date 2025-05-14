import streamlit as st
import os

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        # Get credentials from secrets
        stored_username = st.secrets["username"]
        stored_password = st.secrets["password"]

        if username == stored_username and password == stored_password:
            st.session_state['logged_in'] = True
        else:
            st.sidebar.error("Invalid credentials")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
    st.stop()

