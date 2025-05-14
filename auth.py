import streamlit as st
import streamlit_authenticator as stauth

names = ['Asfareen']
usernames = ['asfareen']
hashed_passwords = [
    '$2b$12$AbcdEfGhIjKlMnOpQrStuvWxYz1234567890'  # <- Use your actual hashed password
]

authenticator = stauth.Authenticate(
    names=names,
    usernames=usernames,
    password_hashes=hashed_passwords,
    cookie_name='stock_dashboard',
    key='abcdef',
    cookie_expiry_days=30
)

def login():
    name, authentication_status, username = authenticator.login('Login', 'sidebar')
    if authentication_status:
        st.session_state['logged_in'] = True
        st.success(f'Welcome, {name}!')
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')
    return authentication_status





