import streamlit as st
from agent import stream_agentic_response

st.title("Chat with Public Health Agent 💬")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("How can I recycle lab waste?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("I am thinking..."):
            response = st.write_stream(stream_agentic_response(prompt))
    
    st.session_state.messages.append({"role": "assistant", "content": response})
