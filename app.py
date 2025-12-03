import streamlit as st

# Custom CSS for header styling
st.markdown(f"""
    <style>
    .stApp > header {
        visibility: hidden;
    }
    .stApp {
        margin-top: 0rem;
    }
    .header-container {
        background-color: #ab162b;
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
    }
    .header-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 500;
        font-family: sans-serif;
    }
    .stMainBlockContainer {
        max-width: initial;
        padding: 0;
    }
    .stAppHeader {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Create custom header
st.markdown("""
    <div class="header-container">
        <div class="header-title">AI Product Assistant</div>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input for the user
if prompt := st.chat_input("Say something"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a simple assistant response (replace with your LLM integration)
    assistant_response = f"You said: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.write(assistant_response)
