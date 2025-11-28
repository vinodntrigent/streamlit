import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Haystack AI Product Assistant1",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
def load_css():
    css = """
    <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Remove padding and margins */
        .stApp {
            margin-top: 0;
            padding-top: 0;
            background-color: white;
        }
        
        /* Block container styling */
        .main .block-container {
            padding-top: 0;
            padding-bottom: 0;
            max-width: 100%;
        }
        
        /* Header bar */
        .header-wrapper {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background-color: #DC143C;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .logo-text {
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 0;
        }
        
        .logo-icon {
            font-size: 28px;
            color: white;
        }
        
        .header-center {
            color: white;
            font-size: 18px;
            font-weight: 500;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .header-right {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-left: auto;
            position: relative;
        }
        
        /* Header button container */
        .header-buttons-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Main content area */
        .main-content {
            margin-top: 80px;
            padding: 30px;
            min-height: calc(100vh - 200px);
            padding-bottom: 120px;
        }
        
        /* Chat message styling */
        .chat-container {
            display: flex;
            align-items: flex-start;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .ai-icon {
            font-size: 24px;
            margin-top: 5px;
        }
        
        .message-bubble {
            background-color: #F5F5F5;
            padding: 15px 20px;
            border-radius: 18px;
            max-width: 70%;
            color: #333;
            font-size: 16px;
            line-height: 1.5;
        }
        
        /* Input area styling - anchored to bottom/footer */
        .input-wrapper {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            background-color: white !important;
            padding: 20px 30px !important;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
            z-index: 1000 !important;
            width: 100% !important;
            box-sizing: border-box !important;
            margin: 0 !important;
        }
        
        /* Ensure form inside input-wrapper has no extra margins */
        .input-wrapper .stForm {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .input-wrapper form {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Style text input */
        .stTextInput > div > div > input {
            border: 2px solid #E0E0E0 !important;
            border-radius: 25px !important;
            padding: 10px 100px 10px 20px !important;
            font-size: 16px !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #999 !important;
        }
        
        /* Style form buttons */
        .stForm button {
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
            min-width: 40px !important;
            padding: 0 !important;
            font-size: 18px !important;
        }
        
        /* Ensure body has white background */
        body {
            background-color: white;
        }
        
        /* Hide Streamlit's default input styling */
        .stTextInput label {
            display: none;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load CSS
load_css()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! What are you looking for today?"}
    ]

# Header
st.markdown("""
    <div class="header-wrapper">
        <div class="header-left">
            <span class="logo-icon">☁️</span>
            <span class="logo-text">MOMAR haystack</span>
        </div>
        <div class="header-center">AI Product Assistant</div>
        <div class="header-right">
            <!-- Buttons will be positioned here -->
        </div>
    </div>
""", unsafe_allow_html=True)

# Create buttons
admin_clicked = st.button("Admin Dashboard", key="admin")
new_chat_clicked = st.button("New Chat", key="new_chat")

# Apply custom styling and JavaScript to move buttons into header
st.markdown("""
    <style>
        /* Hide original button containers */
        div[data-testid="column"]:has(button[key="admin"]),
        div[data-testid="column"]:has(button[key="new_chat"]) {
            display: none !important;
        }
        
        /* Style buttons in header */
        .header-right button {
            background-color: #FFB6C1 !important;
            color: #DC143C !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            margin-left: 10px !important;
        }
        
        .header-right button:first-child {
            background-color: #FFB6C1 !important;
            margin-left: 0 !important;
        }
        
        .header-right button:first-child:hover {
            background-color: #FFA0B4 !important;
        }
        
        .header-right button:last-child {
            background-color: white !important;
        }
        
        .header-right button:last-child:hover {
            background-color: #F5F5F5 !important;
        }
    </style>
    <script>
        function moveButtonsToHeader() {
            const headerRight = document.querySelector('.header-right');
            const adminButton = document.querySelector('button[key="admin"]');
            const newChatButton = document.querySelector('button[key="new_chat"]');
            
            if (headerRight && adminButton && newChatButton) {
                // Check if buttons are already moved
                if (headerRight.contains(adminButton) || headerRight.contains(newChatButton)) {
                    return;
                }
                alert('hi');
                // Move buttons to header-right
                headerRight.appendChild(adminButton);
                headerRight.appendChild(newChatButton);
            }
        }
        
        // Run immediately and after delays
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(moveButtonsToHeader, 100);
            });
        } else {
            moveButtonsToHeader();
            setTimeout(moveButtonsToHeader, 100);
            setTimeout(moveButtonsToHeader, 500);
        }
        
        // Also run after Streamlit reruns
        window.addEventListener('load', function() {
            setTimeout(moveButtonsToHeader, 100);
            setTimeout(moveButtonsToHeader, 500);
        });
        
        // Use MutationObserver to detect DOM changes
        const observer = new MutationObserver(function() {
            moveButtonsToHeader();
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    </script>
""", unsafe_allow_html=True)

# Handle header button clicks
if admin_clicked:
    st.info("Admin Dashboard - Coming soon!")

if new_chat_clicked:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! What are you looking for today?"}
    ]
    st.rerun()

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "assistant":
        st.markdown(f"""
            <div class="chat-container">
                <div class="ai-icon">✨</div>
                <div class="message-bubble">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    elif msg["role"] == "user":
        st.markdown(f"""
            <div class="chat-container" style="justify-content: flex-end;">
                <div class="message-bubble" style="background-color: #DC143C; color: white;">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area with form
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    input_col1, input_col2, input_col3 = st.columns([12, 1, 1])
    with input_col1:
        user_input = st.text_input("", placeholder="Ask anything...", key="user_input", label_visibility="collapsed")
    with input_col2:
        mic_clicked = st.form_submit_button("🎤", use_container_width=True)
    with input_col3:
        send_clicked = st.form_submit_button("➤", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Style input buttons
st.markdown("""
    <style>
        /* Style microphone button (first submit button) */
        .stForm div[data-testid="column"]:nth-of-type(2) button {
            background-color: white !important;
            color: #333 !important;
            border: 2px solid #E0E0E0 !important;
        }
        .stForm div[data-testid="column"]:nth-of-type(2) button:hover {
            background-color: #F5F5F5 !important;
        }
        /* Style send button (second submit button) */
        .stForm div[data-testid="column"]:nth-of-type(3) button {
            background-color: #DC143C !important;
            color: white !important;
            border: none !important;
        }
        .stForm div[data-testid="column"]:nth-of-type(3) button:hover {
            background-color: #B8122F !important;
        }
    </style>
""", unsafe_allow_html=True)

# Handle form submission
if send_clicked and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Here you would add AI response logic
    st.session_state.messages.append({"role": "assistant", "content": f"You said: {user_input}"})
    st.rerun()

if mic_clicked:
    st.info("Voice input feature coming soon!")
