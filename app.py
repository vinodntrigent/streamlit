import streamlit as st

# Custom CSS for header styling
st.markdown("""
    <style>
    .stApp > header {
        visibility: hidden;
    }
    .stApp {
        margin-top: 0rem;
    }
    .header-container {
        background-color: #8B0000;
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .logo {
        font-size: 1.5rem;
        color: #D3D3D3;
    }
    .brand-text {
        display: flex;
        flex-direction: column;
    }
    .momar-text {
        font-size: 0.75rem;
        color: white;
        font-weight: 400;
        letter-spacing: 0.05em;
        margin-bottom: -0.2rem;
    }
    .haystack-text {
        font-size: 1.5rem;
        color: white;
        font-weight: bold;
        font-family: sans-serif;
    }
    .ai-assistant-text {
        font-size: 0.9rem;
        color: white;
        font-family: sans-serif;
        margin-top: -0.2rem;
    }
    .chat-input-wrapper {
        position: relative;
    }
    .mic-button-wrapper {
        position: absolute;
        right: 1rem;
        bottom: 0.75rem;
        z-index: 10;
    }
    .mic-button-wrapper button {
        background-color: transparent;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.25rem 0.5rem;
    }
    .mic-button-wrapper button:hover {
        opacity: 0.7;
    }
    </style>
""", unsafe_allow_html=True)

# Create custom header
st.markdown('<div class="header-container">', unsafe_allow_html=True)
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("""
        <div class="header-left">
            <div class="logo">⛰️</div>
            <div class="brand-text">
                <div class="momar-text">MOMAR</div>
                <div class="haystack-text">haystack</div>
                <div class="ai-assistant-text">AI Product Assistant</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with header_col2:
    if st.button("New Chat", key="new_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize recording state
if "recording" not in st.session_state:
    st.session_state.recording = False

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input with mic button positioned next to it
# Using a container to create a custom layout
input_container = st.container()
with input_container:
    # Create a row for input and button
    input_row = st.columns([0.92, 0.08])
    
    with input_row[0]:
        prompt = st.chat_input("Say something")
    
    with input_row[1]:
        # Position button to align with chat input
        st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
        if st.button("🎤", key="mic_button", help="Voice input", use_container_width=True):
            st.session_state.recording = not st.session_state.get("recording", False)
            if st.session_state.recording:
                st.info("Recording... Click again to stop.")
            else:
                st.info("Recording stopped.")
        st.markdown("</div>", unsafe_allow_html=True)

# Handle chat input
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a simple assistant response (replace with your LLM integration)
    assistant_response = f"You said: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.write(assistant_response)