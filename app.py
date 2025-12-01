import streamlit as st
import html

# Page configuration
st.set_page_config(
    page_title="Haystack AI Product Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        margin-top: 0;
        padding-top: 0;
        background-color: #FFFFFF;
    }
    
    /* Red Header */
    .header-container {
        background-color: #DC143C;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-square {
        width: 40px;
        height: 40px;
        background-color: white;
        border: 2px solid #DC143C;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: #DC143C;
        flex-shrink: 0;
    }
    
    .haystack-text {
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 0;
    }
    
    .ai-product-text {
        color: #FFB6C1;
        font-size: 20px;
        margin: 0;
        margin-left: 0.5rem;
    }
    
    .header-right {
        display: flex;
        gap: 1rem;
    }
    
    .header-button {
        background-color: white;
        color: #DC143C;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .header-button:hover {
        background-color: #f0f0f0;
    }
    
    /* Main content area */
    .main-content {
        margin-top: 80px;
        padding: 2rem 2rem 120px 2rem;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        min-height: calc(100vh - 200px);
    }
    
    /* Chat messages */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .message-ai {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        max-width: 70%;
    }
    
    .message-user {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        max-width: 70%;
        margin-left: auto;
        flex-direction: row-reverse;
    }
    
    .icon-container {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #E0E0E0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 20px;
    }
    
    .message-bubble {
        padding: 1rem 1.5rem;
        border-radius: 18px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 15px;
    }
    
    .bubble-ai {
        background-color: #F5F5DC;
        color: #333;
    }
    
    .bubble-user {
        background-color: #E6E6FA;
        color: #333;
    }
    
    /* Input area container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem 2rem;
        border-top: 1px solid #E0E0E0;
        z-index: 1000;
    }
    
    .input-wrapper {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        background-color: #F5F5F5;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        gap: 1rem;
    }
    
    /* Input area styling */
    .stTextInput {
        flex: 1;
    }
    
    .stTextInput > div > div > input {
        background-color: transparent;
        border: none;
        padding: 0;
        box-shadow: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: none;
    }
    
    /* Hide Streamlit input label */
    .stTextInput label {
        display: none;
    }
    
    .input-icon {
        font-size: 20px;
        color: #666;
        cursor: pointer;
        flex-shrink: 0;
    }
    
    .input-icon.send {
        color: #DC143C;
    }
    
    /* Style header buttons to match design */
    .header-button-st {
        background-color: white !important;
        color: #DC143C !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    .header-button-st:hover {
        background-color: #f0f0f0 !important;
    }
    
    /* Position header buttons correctly */
    .header-right [data-testid="column"] {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    
    button[key="admin_btn"],
    button[key="new_chat_btn"] {
        background-color: white !important;
        color: #DC143C !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        white-space: nowrap;
    }
    
    button[key="admin_btn"]:hover,
    button[key="new_chat_btn"]:hover {
        background-color: #f0f0f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! What are you looking for today?"}
    ]
    # Add example conversation from design (only on first load)
    if 'example_added' not in st.session_state:
        user_msg = """I have an appt with a commercial plumbing and underground utility company. they do all the underground piping for subdivisions, distribution centers (amazon), and hospitals. my appt is not until the last week in october but i want to be prepared. they also do all of their equipment maintenance on site. which i know we to show when it comes to that. i just need help with the commercial plumbing and underground utility work. can someone help me out on what products to talk about"""
        ai_response = """If they are installing underground plumbing and utilities, then they are sure to have heavy equipment (i.e. All-In-One Fleet Treat, Titan Tacx, Titan Seize Not, Nutcracker, Brute, Boa Wrap, Python Tape, etc.) and they may need dust suppression and erosion control (MinCryl X-50) and they will need work gloves (Comprehensive Glove Program) and PPE (Safetyman). They are sure to have spills (Fuel & Oil Be Gone is great for rainbows on puddles, Insta-Zorb is great for removing muddy water from holes and Siege is great for hydraulic oil and fuel spill). After they install pipes, they typically jet them to remove dirt and debris (Muddog or Devour Ultra). They are working in dirty environments, so they'll need waterless hand cleaners (Double Duty Towels, Nutcase). For pipe fittings, they can use Moly DSD Aerosol and Titan 2250. I'm sure they'd love to have some Aqua Lights and Vision Pro Lights. Everyone loves Index-Tend Pry Bars. Hope that helps!"""
        st.session_state.messages.append({"role": "user", "content": user_msg})
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.session_state.example_added = True

# Render header
st.markdown("""
<div class="header-container">
    <div class="header-left">
        <div class="logo-square">H</div>
        <span class="haystack-text">haystack</span>
        <span class="ai-product-text">AI Product Assistant</span>
    </div>
    <div class="header-right">
""", unsafe_allow_html=True)

# Header buttons
col_admin, col_new = st.columns(2)
with col_admin:
    admin_clicked = st.button("Admin Dashboard", key="admin_btn")
with col_new:
    new_chat_clicked = st.button("New Chat", key="new_chat_btn")

# st.markdown("</div></div>", unsafe_allow_html=True)

# Handle button clicks
if admin_clicked:
    st.info("Admin Dashboard - Add your navigation logic here")

if new_chat_clicked:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! What are you looking for today?"}
    ]
    st.session_state.example_added = False
    st.rerun()

# Main content area
# st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    escaped_content = html.escape(msg["content"])
    if msg["role"] == "assistant":
        st.markdown(f"""
        <div class="message-ai">
            <div class="icon-container">⚡</div>
            <div class="message-bubble bubble-ai">{escaped_content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-user">
            <div class="icon-container">👤</div>
            <div class="message-bubble bubble-user">{escaped_content}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input area with custom styling
st.markdown("""
<div class="input-container">
    <div class="input-wrapper">
""", unsafe_allow_html=True)

col_input, col_mic, col_send = st.columns([15, 1, 1])

with col_input:
    user_input = st.text_input("", key="input", placeholder="Ask anything...", label_visibility="collapsed")

with col_mic:
    st.markdown('<div style="display: flex; align-items: center; justify-content: center; height: 100%;"><span class="input-icon">🎤</span></div>', unsafe_allow_html=True)

with col_send:
    st.markdown('<div style="display: flex; align-items: center; justify-content: center; height: 100%;"><span class="input-icon send">✈️</span></div>', unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# Handle user input
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Add assistant response (placeholder - you can integrate with your AI here)
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Thank you for your message! I'm here to help you with product recommendations."
    })
    
    st.rerun()
