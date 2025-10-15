import streamlit as st
from agent import run_agent

st.set_page_config(page_title="ColumbusAI Agent", layout="wide")
st.title("🤖 ColumbusAI Agent")

# Initialize chat history in session_state
if "history" not in st.session_state:
    st.session_state.history = []

# Chat container
chat_container = st.container()

# Input box
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="input_text")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Show spinner while agent processes
    with st.spinner("Thinking... 🤔"):
        response = run_agent(user_input)

    # Save to history
    st.session_state.history.append({"user": user_input, "agent": response})

# Display chat messages (ChatGPT-style)
for message in st.session_state.history:
    with chat_container:
        # User bubble (right-aligned, dark blue)
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-end; margin:5px 0;'>
                <div style='background-color:#0B5FFF; color:white; padding:10px 15px; border-radius:15px; max-width:70%;'>
                    {message['user']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Agent bubble (left-aligned, light gray)
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-start; margin:5px 0;'>
                <div style='background-color:#E5E5EA; color:#111; padding:10px 15px; border-radius:15px; max-width:70%;'>
                    {message['agent']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
