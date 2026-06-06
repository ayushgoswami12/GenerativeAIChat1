import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

# ==================================================
# PAGE CONFIG 
# ==================================================
st.set_page_config(
    page_title="Minimal AI Dialogue",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS (Vercel / Linear Inspired Minimal UI)
# ==================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #FAFAFA;
        background-color: #0A0A0A;
    }
    
    .stApp {
        background-color: #0A0A0A;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    /* Typography */
    .main-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #FAFAFA;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .sub-title {
        color: #A1A1AA;
        font-size: 1rem;
        font-weight: 300;
        margin-bottom: 3.5rem;
    }

    /* Standard Streamlit Buttons - Styled as sleek outlines */
    div[data-testid="stButton"] button {
        background-color: #0A0A0A !important;
        color: #FAFAFA !important;
        border: 1px solid #27272A !important;
        border-radius: 6px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 400 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #FAFAFA !important;
        background-color: #171717 !important;
    }

    /* Layout Spacing */
    .agent-card-container {
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 20px;
        background: #0A0A0A;
        margin-bottom: 20px;
        transition: border-color 0.2s ease;
    }
    
    .agent-card-container:hover {
        border-color: #52525B;
    }

    /* Chat Elements */
    [data-testid="chat-message-container"] {
        background-color: transparent !important;
        padding: 0 !important;
        margin-bottom: 1.5rem !important;
    }
    
    [data-testid="chat-message-user"] {
        border-left: 2px solid #FAFAFA;
        padding-left: 1rem !important;
    }
    
    [data-testid="chat-message-assistant"] {
        border-left: 2px solid #27272A;
        padding-left: 1rem !important;
    }

    /* Minimal Chat Input */
    [data-testid="stChatInput"] {
        background-color: #0A0A0A !important;
        border-top: 1px solid #27272A !important;
        padding-top: 1rem !important;
    }
    
    [data-testid="stChatInput"] > div {
        background-color: #0A0A0A !important;
        border: 1px solid #27272A !important;
        border-radius: 6px !important;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #FAFAFA !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #FAFAFA !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stChatInput"] button {
        color: #FAFAFA !important;
        background: transparent !important;
    }
    
    [data-testid="stChatInput"] button svg {
        fill: #FAFAFA !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A0A0A;
        border-right: 1px solid #27272A;
    }
    
    /* Hide the default streamlit top anchor links */
    .st-emotion-cache-1kyxreq { display: none; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# ROLES & METADATA
# ==================================================
roles_meta = {
    "Stock Analyst": {
        "prompt": "You are a technical and precise Stock Market Analyst AI. Provide raw data analysis, chart patterns, and minimal narrative.",
        "icon": "📈", 
        "desc": "Technical market analysis, raw data, charts."
    },
    "Coding Assistant": {
        "prompt": "You are an expert Coding Assistant AI. Offer clean, production-ready code with essential documentation. Prioritize efficiency.",
        "icon": "💻", 
        "desc": "Efficient code, debugging, architecture."
    },
    "Gym Instructor": {
        "prompt": "You are a motivating gym instructor AI. Deliver short, high-energy instructions, sustainable fitness advice, and focus on fundamental compound movements.",
        "icon": "🏋️", 
        "desc": "Workout plans, sustainable gains, nutrition."
    },
    "Funny AI": {
        "prompt": "You are a witty and concise AI assistant. Deliver answers with short, clever humor, and minimal fluff.",
        "icon": "⚡", 
        "desc": "Concise wit, jokes, clever humor."
    },
    "Custom AI": {
        "prompt": "CUSTOM",
        "icon": "✨", 
        "desc": "Your unique agent, defined by you."
    }
}

role_choices = list(roles_meta.keys())

# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

if "messages_history" not in st.session_state:
    st.session_state.messages_history = []

# ==================================================
# UI COMPONENTS: Clean Card Generators
# ==================================================
def render_agent_card(title):
    meta = roles_meta[title]
    
    # We use Streamlit native containers to build the card
    with st.container():
        st.markdown(f"""
        <div class="agent-card-container">
            <div style="font-size: 1.2rem; font-weight: 500; color: #FAFAFA; margin-bottom: 4px;">
                {meta['icon']} {title}
            </div>
            <div style="color: #A1A1AA; font-size: 0.9rem; line-height: 1.4; margin-bottom: 20px; min-height: 40px;">
                {meta['desc']}
            </div>
        """, unsafe_allow_html=True)
        
        # Native Streamlit button (no HTML inside it)
        if st.button("Initialize", key=f"btn_{title}"):
            st.session_state.selected_role = title
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# VIEW 1: LANDING PAGE
# ==================================================
if st.session_state.selected_role is None:

    st.markdown("<div class='main-title'>Dialogue.</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Select a specialized instance to initialize context.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        render_agent_card("Stock Analyst")
        render_agent_card("Gym Instructor")

    with col2:
        render_agent_card("Coding Assistant")
        render_agent_card("Funny AI")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Custom AI full width
    render_agent_card("Custom AI")

    st.stop()

# ==================================================
# SIDEBAR CONTROLS
# ==================================================
with st.sidebar:
    st.markdown("<h3 style='color:#FAFAFA; font-weight:500; margin-bottom: 1rem;'>Settings</h3>", unsafe_allow_html=True)
    
    selected_role = st.selectbox(
        "Active Instance",
        role_choices,
        index=role_choices.index(st.session_state.selected_role)
    )

    custom_prompt = ""
    if selected_role == "Custom AI":
        custom_prompt = st.text_area(
            "System Context",
            value="You are a helpful and concise AI assistant.",
            height=150
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Clear Memory"):
        st.session_state.chat_display = []
        st.session_state.messages_history = []
        st.rerun()

    if st.button("← Switch Agent"):
        st.session_state.selected_role = None
        st.session_state.chat_display = []
        st.rerun()

# ==================================================
# SYSTEM PROMPT CONFIGURATION
# ==================================================
current_role_prompt = custom_prompt if selected_role == "Custom AI" else roles_meta[selected_role]['prompt']

if selected_role != st.session_state.selected_role:
    st.session_state.selected_role = selected_role
    st.session_state.chat_display = []
    st.session_state.messages_history = [SystemMessage(content=current_role_prompt)]
    st.rerun()

if not st.session_state.messages_history:
    st.session_state.messages_history = [SystemMessage(content=current_role_prompt)]

# ==================================================
# MODEL INITIALIZATION
# ==================================================
model = ChatGroq(
    model="openai/gpt-oss-120b" 
)

# ==================================================
# VIEW 2: DIALOGUE INTERFACE
# ==================================================
meta = roles_meta[selected_role]

st.markdown(f"<div class='main-title' style='font-size: 1.8rem;'>{meta['icon']} {selected_role}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='color: #A1A1AA; font-size: 0.9rem; margin-bottom: 3rem; padding-bottom: 1rem; border-bottom: 1px solid #27272A;'>Instance actively listening.</div>", unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input & AI Generation
prompt = st.chat_input("Enter command...")


if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_display.append({"role": "user", "content": prompt})
    st.session_state.messages_history.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        with st.spinner("Compiling..."):
            try:
                response = model.invoke(st.session_state.messages_history)
                st.markdown(response.content)
                
                st.session_state.chat_display.append({"role": "assistant", "content": response.content})
                st.session_state.messages_history.append(AIMessage(content=response.content))
            except Exception as e:
                st.error("API Connection Failed.")
                