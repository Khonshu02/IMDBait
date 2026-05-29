import streamlit as st
from debate_engine import start_debate, get_opening_message, chat
import base64

#--- Page Config-------
st.set_page_config(
    page_title="IMDBait",
    layout="wide"
)

#---Helper: Load img as base64--------
def get_base64_image(image_path):
    """
    Streamlit can't use local img directly in css.
    we convert the img to base64 string so css can embed it.
    """
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

#---Load bg img------
bg_base64 = get_base64_image("assets/IMDBait_bg.png")
logo_base64 = get_base64_image("assets/IMDBait_red.png")

#---Global css-----
st.markdown(f"""
<style>
/* Hide streamlit default elements */
#MainMenu, footer, header {{visibility: hidden;}}
.block-container {{padding: 0 !important; max-width: 100% !important;}}

/* Scrolling background animation */
@keyframes scrollBg {{
    0%   {{ background-position: 0% center; }}
    100% {{ background-position: 100% center; }}
}}

/* Landing page background */
body, .stApp {{
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: cover;
    background-repeat: repeat-x;
    animation: scrollBg 240s linear infinite;
    background-attachment: fixed;
}}
/* Main title */
.main-title {{
    font-size: 80px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 12px;
    text-align: center;
    margin-bottom: 8px;
    font-family: 'Impact', sans-serif;
    text-shadow: 0 0 30px rgba(229, 9, 20, 0.8);
}}

/* Tagline */
.tagline {{
    font-size: 18px;
    color: #aaaaaa;
    text-align: center;
    margin-bottom: 48px;
    font-style: italic;
}}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────
if "debate_started" not in st.session_state:
    st.session_state.debate_started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "movie" not in st.session_state:
    st.session_state.movie = ""
if "mode" not in st.session_state:
    st.session_state.mode = ""

# ── Landing page ──────────────────────────────────────────────
if not st.session_state.debate_started:

    st.markdown(f"""
    <div class="landing-bg">
        <div class="landing-overlay">
            <img src="data:image/png;base64,{logo_base64}" style="width: 600px; margin-top: 14px; margin-bottom: 8px; display: block; margin-left: auto; margin-right: auto;">
            <div class="tagline">Think you know your movies? Prove it.</div>
        
    """, unsafe_allow_html=True)

    # Input form — centered columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        movie = st.text_input("", placeholder="Enter a movie or show...")

        st.markdown("<br>", unsafe_allow_html=True)

        mode_labels = {
            "debate": " Debate",
            "villain": " Villain Defender",
            "plothole": " Plot Hole Hunter",
            "fantheory": " Fan Theory Battle"
        }

        mode = st.selectbox("Pick your mode", list(mode_labels.keys()),
                           format_func=lambda x: mode_labels[x])

        user_side = None
        if mode == "debate":
            user_side = st.text_input("", placeholder="What's your stance?")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("START THE DEBATE", use_container_width=True):
            if not movie.strip():
                st.error("Enter a movie or show name first!")
            elif mode == "debate" and not user_side.strip():
                st.error("Enter your stance for debate mode!")
            else:
                # Store in session state
                st.session_state.movie = movie
                st.session_state.mode = mode
                st.session_state.user_side = user_side

                # Start the debate engine
                start_debate(mode, movie, user_side)

                # Get opening message
                opening = get_opening_message()

                # Save opening to messages
                st.session_state.messages = [
                    {"role": "assistant", "content": opening}
                ]

                st.session_state.debate_started = True
                st.rerun()

    #----- chat page----
    # ── Debate/Chat page ──────────────────────────────────────────
else:
    # CSS for chat page
    st.markdown(f"""
    <style>
    .chat-input-bar{{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #111111;
        padding: 15px 20px;
        border-top: 1px solid #333;
        z-index: 999;
    }}
    .chat-messages{{
        margin-bottom: 100px;
    }}
    .stApp {{
        background: rgba(0, 0, 0, 0.85) !important;
    }}
    .chat-header {{
        text-align: center;
        padding: 20px;
        border-bottom: 1px solid #333;
        margin-bottom: 20px;
    }}
    .chat-header h2 {{
        color: #ffffff;
        font-size: 24px;
        margin: 0;
    }}
    .mode-badge {{
        display: inline-block;
        background: #e50914;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        margin-top: 8px;
    }}
    .chat-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }}
    .msg-ai {{
        background: #1a1a2e;
        border-left: 3px solid #e50914;
        padding: 14px 18px;
        border-radius: 0 12px 12px 0;
        margin: 12px 0;
        color: #ffffff;
        max-width: 85%;
    }}
    .msg-user {{
        background: #1e1e1e;
        border-right: 3px solid #555;
        padding: 14px 18px;
        border-radius: 12px 0 0 12px;
        margin: 12px 0 12px auto;
        color: #ffffff;
        max-width: 85%;
        text-align: right;
    }}
    .sender-label {{
        font-size: 11px;
        color: #888;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Header
    mode_icons = {
        "debate": "Debate Mode",
        "villain": "Villain Defender",
        "plothole": "Plot Hole Hunter",
        "fantheory": "Fan Theory Battle"
    }

    st.markdown(f"""
    <div class="chat-header">
        <h2>IMDBAIT vs You</h2>
        <div style="color:#aaa; font-size:15px; margin-top:4px;">
            {st.session_state.movie}
        </div>
        <div class="mode-badge">{mode_icons[st.session_state.mode]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages
    # Define containers in visual order
    messages_container = st.container()
    input_container = st.container()

    # Input bar — defined second but visually below
    with input_container:
        st.markdown('<div class="chat-input-bar">', unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("",
                placeholder="Make your argument...",
                key="user_input",
                label_visibility="collapsed"
            )
        with col2:
            send = st.button("SEND", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Messages — renders above input
    with messages_container:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div class="msg-ai">
                    <div class="sender-label">IMDBAIT</div>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-user">
                    <div class="sender-label">You</div>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)

        # Streaming happens here — above input, below messages
        if send and user_input:
            from debate_engine import chat_stream
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            st.markdown(f"""
            <div class="msg-user">
                <div class="sender-label">You</div>
                {user_input}
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="msg-ai"><div class="sender-label">IMDBAIT</div>', unsafe_allow_html=True)
            response = st.write_stream(chat_stream(user_input))
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # New debate button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("New Debate", use_container_width=False):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()