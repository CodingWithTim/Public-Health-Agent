import streamlit as st
from agent import stream_agentic_response
from db import Database

# Initialize the database
db = Database()

st.title("Chat with Public Health Agent 💬")

# Session states to track login status and current user
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def login_form(db):
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if db.authenticate(login_username, login_password):
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.username = login_username
        else:
            st.error("Invalid username or password.")

def signup_form(db):
    signup_username = st.text_input("New Username", key="signup_username")
    signup_password = st.text_input("New Password", type="password", key="signup_password")
    location = st.text_input("Your Location (City, State, Country)", key="location")
    age = st.text_input("Your Age", key="age")
    occupation = st.text_input("Your Occupation", key="occupation")
    company = st.text_input("Your Company", key="company")
    if st.button("Sign Up"):
        if db.user_exists(signup_username):
            st.error("Username already exists. Please choose a different one.")
        else:
            personal_info = {
                "location": location,
                "age": age,
                "occupation": occupation,
                "company": company,
            }
            db.create_account(signup_username, signup_password, personal_info)
            st.success("Account created successfully! You can now log in.")

if not st.session_state.logged_in:
    # Show login/create account form
    st.subheader("Login or Create an Account")
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        login_form(db)

    with tab_signup:
        signup_form(db)
else:
    # If logged in, show user info and logout button
    user_data = db.get_user_data(st.session_state.username)
    personal_info = user_data.get("personal_info", {})

    st.sidebar.title("User Info")
    for k, v in personal_info.items():
        st.sidebar.write(f"**{k}:**", v)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.messages = []
        # st.experimental_rerun()

    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("How can I recycle lab waste?")
    if prompt:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("I am thinking..."):
                # Get assistant response
                response = st.write_stream(stream_agentic_response(prompt, personal_info))
        
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Save updated messages to the database
        db.update_user_messages(st.session_state.username, st.session_state.messages)
