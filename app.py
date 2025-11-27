import streamlit as st
import os
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="AI Product Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS from file
def load_css():
    css_file = Path("css/styles.css")
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Inject CSS
css_content = load_css()
if css_content:
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Additional Streamlit-specific CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stApp {
        margin-top: 0;
        padding-top: 0;
        background: #f8fafc;
    }
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
    }
    /* Header styling */
    .chat-header-wrapper {
        background: #AB162B;
        padding: 14px 16px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-bottom: 0;
    }
    .chat-header-wrapper .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
    }
    .chat-header-wrapper .brand img {
        height: 30px;
    }
    .chat-header-wrapper .tools {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .chat-header-wrapper button {
        height: 36px;
        padding: 0 12px;
        border: 1px solid rgba(255,255,255,0.3);
        background: white;
        border-radius: 8px;
        cursor: pointer;
        color: #AB162B;
        font-weight: 500;
    }
    /* Messages container */
    .messages-container {
        padding: 16px;
        background: white;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    /* Input area */
    .composer-wrapper {
        padding: 10px;
        border-top: 1px solid #e2e8f0;
        background: white;
        display: flex;
        gap: 8px;
    }
    .stTextInput > div > div > input {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 8px 12px;
        font-family: Roboto, Helvetica, Arial;
    }
    .stForm button {
        width: 42px;
        height: 42px;
        border: 1px solid #e2e8f0;
        background: white;
        border-radius: 10px;
    }
    .stForm button[kind="primary"] {
        background: #AB162B;
        color: white;
        border-color: #AB162B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant', 'text': 'Hello! What are you looking for today?'}
    ]

if 'show_admin' not in st.session_state:
    st.session_state.show_admin = False

if 'show_recs' not in st.session_state:
    st.session_state.show_recs = False

if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'products' not in st.session_state:
    st.session_state.products = [
        {'id': '20456', 'title': 'COMPREHENSIVE GLOVE PROGRAM', 'description': 'Disposable, Work, and Industrial Gloves', 'image': 'images/glovesprogram_catalogimage.png', 'quantity': 1, 'price': 100.00},
        {'id': '2551', 'title': 'FLEET TREAT™', 'description': 'Ultra-Concentrated, Multi-Functional Diesel Fuel Additive', 'image': 'images/fleettreat_catalog_image.png', 'quantity': 1, 'price': 536.20},
        {'id': '20064', 'title': 'TITAN TACK™', 'description': 'Heavy-Duty, Moly-Fortified Aluminum Complex Grease', 'image': 'images/titantack2_catalog_image.png', 'quantity': 1, 'price': 520.00},
        {'id': '20165', 'title': 'TITAN SEIZE NOT™ PASTE', 'description': 'Copper and Graphite Fortified, High-Performance Anti-Seize', 'image': 'images/titanseizenotpaste_catalog_image.png', 'quantity': 1, 'price': 110.00},
        {'id': '2478', 'title': 'NUTCRACKER PLUS™ AEROSOL', 'description': 'High-Performance Penetrating Lubricant', 'image': 'images/nutcrackerplusaerosol_catalog_image.png', 'quantity': 1, 'price': 200.00},
        {'id': '2541', 'title': 'BRUTE™', 'description': 'Hyper-Concentrated Truck, Trailer, and Car Wash', 'image': 'images/brute_catalog_image.png', 'quantity': 1, 'price': 400.00},
        {'id': '5737', 'title': 'BOA WRAP', 'description': 'Cable, Wire, and Hose Abrasion Protection Wrap', 'image': 'images/boawrap__catalog_.png', 'quantity': 1, 'price': 90.00},
        {'id': '2484', 'title': 'PYTHON FUSION TAPE', 'description': 'Cable, Hose, and Wire Repair Tape', 'image': 'images/python__catalog_.png', 'quantity': 1, 'price': 50.00},
    ]

if 'selected_options' not in st.session_state:
    st.session_state.selected_options = {}

if 'active_ids' not in st.session_state:
    st.session_state.active_ids = set()

if 'show_glove_program' not in st.session_state:
    st.session_state.show_glove_program = False

if 'is_thinking' not in st.session_state:
    st.session_state.is_thinking = False

# Options for product selection
OPTIONS = [
    '1/325 GL (2505LB)',
    '1/54 GL (METAL DRUM)',
    '1/5 GL (38 LBS NET)',
    '4/1 GL',
    'SAMPLE GL',
    'SAMPLE PT'
]

# Utility functions
def get_price_for_option(product_id, option, base_price):
    if option == '1/325 GL (2505LB)':
        return base_price * 325 * 0.75
    elif option == '1/54 GL (METAL DRUM)':
        return base_price * 54 * 0.85
    elif option == '1/5 GL (38 LBS NET)':
        return base_price * 5 * 0.9
    elif option == '4/1 GL':
        return base_price * 4 * 0.95
    elif option == 'SAMPLE GL':
        return base_price
    elif option == 'SAMPLE PT':
        return base_price * 0.125
    return base_price

def get_cart_count():
    return sum(st.session_state.cart.values())

def get_visible_products():
    return [p for p in st.session_state.products if not (p['title'] == 'COMPREHENSIVE GLOVE PROGRAM' and not st.session_state.show_glove_program)]

# Handle message sending
def handle_send(text):
    st.session_state.messages.append({'role': 'user', 'text': text})
    st.session_state.is_thinking = True
    st.rerun()

# Process AI response
def process_ai_response(text):
    text_lower = text.lower()
    if 'commercial plumbing' in text_lower or 'underground utility' in text_lower:
        return """If they are installing underground plumbing and utilities, then they are sure to have heavy equipment (i.e. All-In-One Fleet Treat, Titan Tack, Titan Seize Not, Nutcracker, Brute, Boa Wrap, Python Tape, etc.) and they may need dust suppression and erosion control (MinCryl X-50) and they will need work gloves (Comprehensive Glove Program) and PPE (Safetyman). They are sure to have spills (Fuel & Oil Be Gone is great for rainbows on puddles, Insta-Zorb is great for removing muddy water from holes and Siege is great for hydraulic oil and fuel spill). After they install pipes, they typically jet them to remove dirt and debris (Muddog or Devour Ultra). They are working in dirty environments, so they'll need waterless hand cleaners (Double Duty Towels, Nutcase). For pipe fittings, they can use Moly DSD Aerosol and Titan 2250. I'm sure they'd love to have some Aqua Lights and Vision Pro Lights. Everyone loves Index-Tend Pry Bars. Hope that helps!"""
    elif 'sealed air' in text_lower:
        return """Collin Brown, Carter Conley might be able to assist on this, but here are some products I know we've sold to Sealed Air (Bristol PA, Lyman SC, Hudson NC, Lenoir NC, Simpsonville SC, and Iowa Park TX) in the past: Ivory 3333, Citra-Soy, Siege, Stallion Aerosol, Miracle Tool, Grrreat Grape, Assassin Aerosol, Forever Soft, Gask-It, Seal-It, Foam-Away Aerosol, and a bunch of Handyman tools."""
    elif 'glove program' in text_lower:
        st.session_state.show_glove_program = True
        return 'Added Comprehensive Glove Program catalog to the list'
    elif 'double duty towels' in text_lower:
        return '2 products are available - Double Duty Towels, Superco One Step Heavy Duty Towels. Which product would you like to add to list'
    else:
        return 'Great! I will help you with appropriate product recommendations'

# Main app logic
if st.session_state.show_admin:
    # Admin Dashboard
    st.markdown("""
    <div style="background: #AB162B; padding: 16px; margin: -1rem -1rem 24px -1rem;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 10px; color: white; font-weight: 700; font-size: 1.25rem;">
                <span>⚙️</span>
                <span>Admin Dashboard</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Assistant", key="admin_back_btn"):
        st.session_state.show_admin = False
        st.rerun()
    
    st.markdown("### Basic Monitoring")
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {'icon': '📊', 'value': '1,247', 'label': 'Total Queries'},
        {'icon': '✅', 'value': '1,189', 'label': 'Successful Responses'},
        {'icon': '⚡', 'value': '1.2s', 'label': 'Avg Response Time'},
        {'icon': '👥', 'value': '23', 'label': 'Active Users'}
    ]
    
    for i, metric in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div style="background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; text-align: center;">
                <div style="font-size: 32px; color: #AB162B; margin-bottom: 8px;">{metric['icon']}</div>
                <div style="font-size: 1.75rem; font-weight: 700; margin-bottom: 4px; color: #0f172a;">{metric['value']}</div>
                <div style="font-size: 0.875rem; color: #64748b;">{metric['label']}</div>
            </div>
            """, unsafe_allow_html=True)
        
else:
    # Main Chat Interface
    # Header
    st.markdown("""
    <div class="chat-header-wrapper">
        <div class="brand">
            <img src="images/momar-haystack-icon.png" alt="logo" onerror="this.style.display='none'">
            <span>AI Product Assistant</span>
        </div>
        <div class="tools">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Header buttons
    col1, col2 = st.columns([10, 1])
    with col1:
        pass  # Spacer
    with col2:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Admin Dashboard", key="admin_btn"):
                st.session_state.show_admin = True
                st.rerun()
        with btn_col2:
            if st.button("New Chat", key="new_chat_btn"):
                st.session_state.messages = [{'role': 'assistant', 'text': 'Hello! What are you looking for today?'}]
                st.session_state.show_recs = False
                st.session_state.show_cart = False
                st.session_state.cart = {}
                st.rerun()
    
    # Main content area
    if st.session_state.show_recs:
        main_col, aside_col = st.columns([2, 1])
    else:
        main_col = st.container()
        aside_col = None
    
    with main_col:
        # Messages
        st.markdown('<div class="messages-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg['role'] == 'assistant':
                st.markdown(f"""
                <div style="display: flex; gap: 10px; align-items: flex-end; margin-bottom: 12px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #f1f5f9; display: flex; align-items: center; justify-content: center; color: #475569; font-size: 14px; flex-shrink: 0;">
                        ✨
                    </div>
                    <div style="max-width: 62%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 12px; background: white;">
                        {msg['text']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; gap: 10px; align-items: flex-end; margin-bottom: 12px; justify-content: flex-end;">
                    <div style="max-width: 62%; padding: 10px 12px; border: 1px solid #e5e5e5; border-radius: 12px; background: #e5e5e5; color: #000;">
                        {msg['text']}
                    </div>
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: #AB162B; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; flex-shrink: 0;">
                        👤
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if st.session_state.is_thinking:
            st.markdown("""
            <div style="display: flex; gap: 10px; align-items: flex-end; margin-bottom: 12px;">
                <div style="width: 28px; height: 28px; border-radius: 8px; background: #f1f5f9; display: flex; align-items: center; justify-content: center; color: #475569; font-size: 14px; flex-shrink: 0;">
                    ✨
                </div>
                <div style="padding: 12px 16px; border: 1px solid #e2e8f0; border-radius: 12px; background: white; display: flex; gap: 4px; align-items: center;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #64748b; display: inline-block; animation: bounce 1.4s infinite;"></span>
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #64748b; display: inline-block; animation: bounce 1.4s infinite 0.2s;"></span>
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #64748b; display: inline-block; animation: bounce 1.4s infinite 0.4s;"></span>
                </div>
            </div>
            <style>
                @keyframes bounce {
                    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
                    40% { transform: scale(1.2); opacity: 1; }
                }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        with st.form("chat_form", clear_on_submit=True):
            input_col1, input_col2, input_col3 = st.columns([10, 1, 1])
            with input_col1:
                user_input = st.text_input("", placeholder="Ask anything ...", key="user_input", label_visibility="collapsed")
            with input_col2:
                mic_clicked = st.form_submit_button("🎤", use_container_width=True)
            with input_col3:
                send_clicked = st.form_submit_button("➤", use_container_width=True, type="primary")
        
        if send_clicked and user_input:
            handle_send(user_input)
            # Simulate AI thinking
            time.sleep(0.8)
            st.session_state.is_thinking = False
            
            response = process_ai_response(user_input)
            st.session_state.messages.append({'role': 'assistant', 'text': response})
            st.session_state.show_recs = True
            st.rerun()
        
        if mic_clicked:
            st.info("Voice input feature coming soon!")
    
    # Recommendations/Cart Panel
    if st.session_state.show_recs and aside_col:
        with aside_col:
            if st.session_state.show_cart:
                # Cart view
                st.markdown("### Cart")
                if st.button("← Back", key="cart_back"):
                    st.session_state.show_cart = False
                    st.rerun()
                
                cart_items = [p for p in st.session_state.products if st.session_state.cart.get(p['id'], 0) > 0]
                if not cart_items:
                    st.info("Your cart is empty.")
                else:
                    for item in cart_items:
                        st.markdown(f"""
                        <div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; margin-bottom: 12px; background: white;">
                            <div style="display: flex; gap: 12px;">
                                <img src="{item['image']}" alt="{item['title']}" style="width: 112px; height: 84px; border-radius: 10px; object-fit: cover;" onerror="this.style.display='none'">
                                <div style="flex: 1;">
                                    <div style="font-weight: 600; color: #0f172a;">{item['title']}</div>
                                    <div style="color: #64748b; font-size: 14px;">Qty: {st.session_state.cart[item['id']]}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if cart_items:
                    st.markdown("""
                    <div style="position: sticky; bottom: 0; padding: 12px; border-top: 1px solid #e2e8f0; background: white; margin-top: 20px;">
                        <a href="place-order.html" style="display: block; width: 100%; background: #AB162B; color: white; text-align: center; padding: 10px; border-radius: 8px; text-decoration: none;">
                            Place Order
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Recommendations view
                cart_count = get_cart_count()
                header_col1, header_col2 = st.columns([3, 1])
                with header_col1:
                    st.markdown("### Recommendations")
                with header_col2:
                    if cart_count > 0:
                        if st.button(f"🛒 ({cart_count})", key="view_cart"):
                            st.session_state.show_cart = True
                            st.rerun()
                
                visible_products = get_visible_products()
                for item in visible_products:
                    selected_option = st.session_state.selected_options.get(item['id'], OPTIONS[0])
                    current_price = get_price_for_option(item['id'], selected_option, item['price'])
                    
                    st.markdown(f"""
                    <div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; margin-bottom: 12px; background: white;">
                        <div style="display: flex; gap: 12px; margin-bottom: 10px;">
                            <img src="{item['image']}" alt="{item['title']}" style="width: 112px; height: 84px; border-radius: 10px; object-fit: cover;" onerror="this.style.display='none'">
                            <div style="flex: 1;">
                                <div style="font-weight: 600; color: #0f172a;">{item['title']}</div>
                                <div style="color: #64748b; font-size: 14px; margin-bottom: 4px;">{item['description']}</div>
                                <div style="color: #64748b; font-size: 12px;">Unit Price: <strong>${current_price:,.2f}</strong></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if item['id'] in st.session_state.active_ids:
                        # Show stepper
                        qty_col1, qty_col2, qty_col3 = st.columns([1, 2, 1])
                        with qty_col1:
                            if st.button("−", key=f"dec_{item['id']}"):
                                item['quantity'] = max(0, item['quantity'] - 1)
                                if item['quantity'] == 0:
                                    if item['id'] in st.session_state.cart:
                                        del st.session_state.cart[item['id']]
                                    st.session_state.active_ids.discard(item['id'])
                                else:
                                    st.session_state.cart[item['id']] = item['quantity']
                                st.rerun()
                        with qty_col2:
                            st.markdown(f"<div style='text-align: center; padding: 8px;'>{item['quantity']}</div>", unsafe_allow_html=True)
                        with qty_col3:
                            if st.button("+", key=f"inc_{item['id']}"):
                                item['quantity'] += 1
                                st.session_state.cart[item['id']] = item['quantity']
                                st.rerun()
                    else:
                        # Show option select and add button
                        opt_col1, opt_col2 = st.columns([3, 1])
                        with opt_col1:
                            option = st.selectbox("", OPTIONS, key=f"opt_{item['id']}", label_visibility="collapsed")
                            st.session_state.selected_options[item['id']] = option
                        with opt_col2:
                            if st.button("+", key=f"add_{item['id']}"):
                                st.session_state.active_ids.add(item['id'])
                                st.session_state.cart[item['id']] = item['quantity']
                                st.rerun()
