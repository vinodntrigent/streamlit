import streamlit as st

# Avatar SVG content as a string
ai_svg_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles-icon lucide-sparkles"><path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"/><path d="M20 2v4"/><path d="M22 4h-4"/><circle cx="4" cy="20" r="2"/></svg>
"""

user_svg_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-user-round-icon lucide-circle-user-round"><path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/></svg>
"""

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
    [data-testid="stLayoutWrapper"] {
        width: 90%;
        max-width: initial;
        margin: 0 auto;
    }
    .header-container {
        position: fixed;
        width: 100%;
        padding-top: 2rem;
        z-index: 500;
    }
    section > div > div > div:nth-child(3) {
        margin-top: -65px;
    }
    /* Anchor chat input to bottom */
    .chat-messages {
        padding-bottom: 100px;
    }
    /* Target the chat input container - multiple selectors to catch it */
    div[data-testid="stChatInputContainer"],
    form[data-testid="stChatInputForm"],
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background-color: white !important;
        padding: 1rem !important;
        border-top: 1px solid #e0e0e0 !important;
        z-index: 100 !important;
        width: 100% !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
    }
    /* Style the input field to make room for buttons */
    div[data-testid="stChatInputContainer"] input,
    form[data-testid="stChatInputForm"] input {
        padding-right: 5rem !important;
    }
    /* Mic button container - positioned inside chat input, before send button */
    .mic-button-container {
        position: fixed !important;
        bottom: 1.25rem !important;
        right: 4.5rem !important;
        z-index: 101 !important;
        display: flex !important;
        align-items: center !important;
    }
    /* Style the mic button */
    .mic-button-container button {
        background-color: transparent !important;
        border: none !important;
        padding: 0.5rem !important;
        cursor: pointer !important;
        font-size: 1.2rem !important;
        color: #666 !important;
        transition: all 0.2s ease !important;
        min-width: auto !important;
        width: auto !important;
        height: auto !important;
    }
    .mic-button-container button:hover {
        color: #ab162b !important;
        transform: scale(1.1) !important;
    }
    /* Recording state */
    .mic-button-container button.recording {
        color: #ff4444 !important;
        animation: pulse 1.5s infinite !important;
    }
    /* Mic button styling */
    .mic-button {
        background-color: #f0f0f0;
        border: 1px solid #d0d0d0;
        border-radius: 50%;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .mic-button:hover {
        background-color: #e0e0e0;
    }
    .mic-button.recording {
        background-color: #ff4444;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    </style>
""", unsafe_allow_html=True)

# Create custom header
st.markdown("""
    <div class="header-container">
        <div class="header-title">Momar Haystack AI Product Assistant</div>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize speech-to-text state
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# Messages container
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat input for the user (will be anchored to bottom via CSS)
prompt = st.chat_input("Ask a question...")

# Speech-to-text button positioned inside chat input, before send button
st.markdown('<div class="mic-button-container">', unsafe_allow_html=True)
mic_button_clicked = st.button("🎤", key="mic_button", help="Start voice input")
if mic_button_clicked:
    st.session_state.is_recording = not st.session_state.is_recording
    if st.session_state.is_recording:
        st.info("🎤 Recording... Click again to stop.")
    else:
        st.info("Recording stopped.")
st.markdown('</div>', unsafe_allow_html=True)

# Handle chat input
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # with st.chat_message("user", avatar=user_svg_icon):
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a simple assistant response (replace with your LLM integration)
    assistant_response = f"{prompt}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    # with st.chat_message("assistant", avatar=ai_svg_icon):
    with st.chat_message("assistant"):
        st.write(assistant_response)
