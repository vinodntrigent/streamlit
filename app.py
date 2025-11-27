import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Momar - AI Assistant11",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-style design
def load_css():
    css = """
    <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Global styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            height: 100%;
            overflow: hidden;
        }
        
        .stApp {
            margin-top: 0;
            padding-top: 0;
            background-color: #343541;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Block container styling */
        .main .block-container {
            padding-top: 0;
            padding-bottom: 0;
            max-width: 100%;
            height: 100%;
        }
        
        /* Fixed Header */
        .chat-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background-color: #202123;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 0 20px;
        }
        
        .header-content {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #ECECF1;
        }
        
        .header-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }
        
        .header-title {
            font-size: 18px;
            font-weight: 600;
            color: #ECECF1;
        }
        
        /* Main Chat Container */
        .chat-container {
            position: fixed;
            top: 60px;
            bottom: 100px;
            left: 0;
            right: 0;
            overflow-y: auto;
            padding: 20px 0;
            background-color: #343541;
        }
        
        .chat-messages {
            max-width: 768px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Message Styling */
        .message-wrapper {
            display: flex;
            gap: 20px;
            padding: 20px 0;
            width: 100%;
        }
        
        .message-wrapper.user {
            background-color: #343541;
        }
        
        .message-wrapper.assistant {
            background-color: #444654;
        }
        
        .message-avatar {
            width: 30px;
            height: 30px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            font-size: 16px;
        }
        
        .message-avatar.user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .message-avatar.assistant {
            background: linear-gradient(135deg, #10a37f 0%, #1a7f64 100%);
        }
        
        .message-content {
            flex: 1;
            color: #ECECF1;
            font-size: 16px;
            line-height: 1.75;
            padding-top: 4px;
        }
        
        .message-content p {
            margin: 0;
        }
        
        /* Input Footer */
        .chat-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 100px;
            background-color: #343541;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 20px;
        }
        
        .input-container {
            max-width: 768px;
            width: 100%;
            position: relative;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            background-color: #40414F !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            padding: 12px 100px 12px 16px !important;
            font-size: 16px !important;
            color: #ECECF1 !important;
            width: 100% !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.3) !important;
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #8E8EA0 !important;
        }
        
        .stTextInput label {
            display: none !important;
        }
        
        /* Form container */
        .stForm {
            margin: 0 !important;
            position: relative !important;
        }
        
        /* Input container wrapper */
        .input-container {
            position: relative !important;
        }
        
        .input-container .stTextInput {
            position: relative !important;
            margin-bottom: 0 !important;
        }
        
        /* Hide button columns and position buttons absolutely */
        .stForm div[data-testid="column"] {
            position: absolute !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            width: auto !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        .stForm div[data-testid="column"]:nth-of-type(1) {
            right: 50px !important;
        }
        
        .stForm div[data-testid="column"]:nth-of-type(2) {
            right: 8px !important;
        }
        
        /* Style buttons */
        .stForm button {
            background-color: transparent !important;
            border: none !important;
            color: #8E8EA0 !important;
            cursor: pointer !important;
            padding: 8px !important;
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            border-radius: 6px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 18px !important;
            z-index: 10 !important;
            margin: 0 !important;
        }
        
        .stForm button:hover {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: #ECECF1 !important;
        }
        
        /* Scrollbar styling */
        .chat-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: #343541;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: #565869;
            border-radius: 4px;
        }
        
        .chat-container::-webkit-scrollbar-thumb:hover {
            background: #6B6D7E;
        }
        
        /* Hide Streamlit default elements */
        .element-container {
            margin-bottom: 0 !important;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_css()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Momar, your AI assistant. How can I help you today?"}
    ]

# Fixed Header
st.markdown("""
    <div class="chat-header">
        <div class="header-content">
            <div class="header-icon">💬</div>
            <div class="header-title">Momar</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Chat Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "assistant":
        st.markdown(f"""
            <div class="message-wrapper assistant">
                <div class="message-avatar assistant">🤖</div>
                <div class="message-content">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    elif msg["role"] == "user":
        st.markdown(f"""
            <div class="message-wrapper user">
                <div class="message-avatar user">👤</div>
                <div class="message-content">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Fixed Footer with Input
st.markdown('<div class="chat-footer">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "", 
        placeholder="Message Momar...", 
        key="user_input", 
        label_visibility="collapsed"
    )
    # Create buttons in a row, positioned via CSS
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        mic_clicked = st.form_submit_button("🎤", use_container_width=True)
    with btn_col2:
        send_clicked = st.form_submit_button("➤", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle form submission
if send_clicked and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Here you would add AI response logic
    st.session_state.messages.append({"role": "assistant", "content": f"I understand you said: {user_input}. How can I assist you further?"})
    st.rerun()

if mic_clicked:
    st.info("Voice input feature coming soon!")
