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
    /* Ensure the input itself is styled */
    div[data-testid="stChatInputContainer"] input,
    form[data-testid="stChatInputForm"] input {
        width: 100% !important;
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

# Messages container
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat input for the user (will be anchored to bottom via CSS)
if prompt := st.chat_input("Ask a question..."):
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
