import os
from typing import Any, Dict, List, Optional
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 12

st.set_page_config(
    page_title="Eventify AI — Smart Event Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #05070d;
    --panel: #0b0f18;
    --panel2: #101624;
    --line: rgba(255,255,255,.08);
    --text: #f5f7fb;
    --muted: #8c96a8;
    --blue: #2f7cff;
    --cyan: #19d9ff;
    --purple: #7c5cff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 82% 10%, rgba(37,124,255,.12), transparent 27%),
        radial-gradient(circle at 15% 30%, rgba(25,217,255,.06), transparent 25%),
        linear-gradient(180deg, #05070d 0%, #060812 55%, #05070d 100%);
    color: var(--text);
}

.block-container {
    max-width: 1280px;
    padding: 1.2rem 2rem 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* hide default streamlit chrome */
#MainMenu, footer { visibility: hidden; }
div[data-testid="stToolbar"] { display: none; }

/* buttons */
.stButton > button {
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 12px;
    background: rgba(255,255,255,.045);
    color: #fff;
    font-weight: 600;
    min-height: 42px;
    transition: .2s ease;
}
.stButton > button:hover {
    border-color: rgba(25,217,255,.5);
    background: rgba(25,217,255,.08);
    transform: translateY(-1px);
}

/* inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: #0c111c !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: 12px !important;
}
input, textarea {
    color: white !important;
}

/* top nav */
.topnav {
    height: 66px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--line);
    margin-bottom: 28px;
}
.brand {
    display: flex;
    gap: 10px;
    align-items: center;
    font-weight: 800;
    font-size: 20px;
}
.logo {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #168dff, #6f50ff);
    box-shadow: 0 0 24px rgba(47,124,255,.35);
}
.navpill {
    color: #aeb8ca;
    font-size: 13px;
    padding: 8px 12px;
}
.navright {
    display: flex;
    align-items: center;
    gap: 8px;
}

/* hero */
.hero {
    min-height: 390px;
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 44px;
    position: relative;
    overflow: hidden;
    background:
      radial-gradient(circle at 75% 48%, rgba(36,131,255,.25), transparent 25%),
      radial-gradient(circle at 80% 45%, rgba(25,217,255,.13), transparent 42%),
      linear-gradient(110deg, #080b12 0%, #0a0f19 58%, #07111b 100%);
    box-shadow: 0 25px 80px rgba(0,0,0,.35);
}
.hero:after {
    content: "🎟️";
    position: absolute;
    right: 7%;
    top: 50%;
    transform: translateY(-50%);
    font-size: 160px;
    filter: drop-shadow(0 0 30px rgba(25,217,255,.25));
    opacity: .9;
}
.badge {
    display: inline-flex;
    padding: 7px 12px;
    border-radius: 999px;
    color: #6ce7ff;
    background: rgba(25,217,255,.07);
    border: 1px solid rgba(25,217,255,.2);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .7px;
    text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(42px, 5vw, 72px);
    line-height: .98;
    margin: 20px 0 18px;
    letter-spacing: -3px;
}
.gradient-text {
    background: linear-gradient(90deg, #ffffff 10%, #5dc9ff 55%, #8a70ff 95%);
    -webkit-background-clip: text;
    color: transparent;
}
.hero p {
    max-width: 570px;
    color: #9ca7ba;
    line-height: 1.7;
    font-size: 15px;
}
.hero-tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 25px;
}
.hero-tag {
    padding: 7px 10px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,.035);
    border-radius: 9px;
    color: #aeb8ca;
    font-size: 11px;
}

/* assistant */
.assistant-card {
    margin-top: 22px;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid rgba(25,217,255,.14);
    background: linear-gradient(135deg, rgba(12,18,29,.96), rgba(7,12,20,.96));
    box-shadow: 0 0 45px rgba(25,217,255,.06);
}
.assistant-title {
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 4px;
}
.assistant-sub {
    color: var(--muted);
    font-size: 11px;
    margin-bottom: 13px;
}
.chat-bubble {
    border-radius: 14px;
    padding: 13px 15px;
    margin: 7px 0;
    line-height: 1.55;
    font-size: 13px;
}
.user-bubble {
    background: rgba(47,124,255,.13);
    border: 1px solid rgba(47,124,255,.18);
}
.ai-bubble {
    background: rgba(255,255,255,.035);
    border: 1px solid var(--line);
}

/* sections */
.section-head {
    display: flex;
    align-items: end;
    justify-content: space-between;
    margin: 48px 0 18px;
}
.section-head h2 {
    margin: 0;
    font-size: 28px;
    letter-spacing: -1px;
}
.section-head p {
    margin: 5px 0 0;
    color: var(--muted);
    font-size: 12px;
}

/* cards */
.event-card {
    background: linear-gradient(180deg, #0c111c, #090d15);
    border: 1px solid var(--line);
    border-radius: 18px;
    overflow: hidden;
    min-height: 250px;
    box-shadow: 0 15px 45px rgba(0,0,0,.2);
}
.event-img {
    height: 125px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 54px;
    background:
      radial-gradient(circle at 70% 40%, rgba(35,145,255,.30), transparent 35%),
      linear-gradient(135deg, #111a2b, #080b12);
}
.event-body { padding: 15px; }
.event-category {
    color: #64dfff;
    text-transform: uppercase;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .8px;
}
.event-title {
    margin-top: 6px;
    font-weight: 700;
    font-size: 15px;
}
.event-meta {
    color: #8894a8;
    font-size: 11px;
    margin-top: 9px;
    line-height: 1.6;
}
.status {
    display: inline-block;
    margin-top: 11px;
    padding: 5px 8px;
    border-radius: 7px;
    background: rgba(50,220,145,.08);
    border: 1px solid rgba(50,220,145,.15);
    color: #61e7ae;
    font-size: 9px;
    font-weight: 700;
}

/* feature cards */
.feature {
    padding: 24px;
    border-radius: 18px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,.025);
    min-height: 155px;
}
.feature-icon { font-size: 23px; }
.feature h3 { font-size: 15px; margin: 14px 0 8px; }
.feature p { color: var(--muted); font-size: 11px; line-height: 1.6; }

/* login */
.login-wrap {
    max-width: 460px;
    margin: 9vh auto 0;
}
.login-brand {
    text-align: center;
    margin-bottom: 28px;
}
.login-brand .logo {
    margin: auto;
}
.login-brand h1 {
    font-size: 35px;
    margin: 15px 0 5px;
}
.login-brand p { color: var(--muted); font-size: 13px; }
.login-card {
    padding: 28px;
    background: rgba(10,15,25,.92);
    border: 1px solid var(--line);
    border-radius: 22px;
    box-shadow: 0 25px 80px rgba(0,0,0,.35);
}

/* metrics */
.metric {
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 16px;
    background: rgba(255,255,255,.025);
}
.metric-label { color: var(--muted); font-size: 10px; }
.metric-value { font-size: 25px; font-weight: 800; margin-top: 4px; }

/* mobile */
@media (max-width: 760px) {
    .block-container { padding: 1rem 1rem 3rem; }
    .hero { padding: 27px; min-height: 410px; }
    .hero h1 { font-size: 43px; }
    .hero:after { right: 5%; top: 70%; font-size: 100px; }
    .navpill { display: none; }
}
</style>
""", unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def api_request(
    method: str,
    endpoint: str,
    *,
    json: Optional[dict] = None,
    params: Optional[dict] = None,
    auth: bool = True,
) -> Any:
    """Generic backend request. Change endpoint paths below to match your FastAPI routes."""
    headers = {"Accept": "application/json"}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    url = f"{BACKEND_URL}{endpoint}"
    response = requests.request(
        method,
        url,
        json=json,
        params=params,
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )

    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except Exception:
            detail = response.text
        raise RuntimeError(f"{response.status_code}: {detail}")

    if not response.content:
        return {}
    return response.json()
def login_user(email: str, password: str):
    # Adjust this endpoint/payload if your FastAPI auth router differs.
    data = api_request(
        "POST",
        "/auth/login",
        json={"email": email, "password": password},
        auth=False,
    )

    token = data.get("access_token") or data.get("token")
    user = data.get("user") or {
        "email": email,
        "name": data.get("name", email.split("@")[0]),
        "user_id": data.get("user_id"),
    }

    if not token:
        raise RuntimeError("Login response did not contain access_token/token.")

    st.session_state.token = token
    st.session_state.user = user
    st.session_state.logged_in = True

def get_events() -> List[Dict[str, Any]]:
    data = api_request("GET", "/events", params={"status": "published"})

    if isinstance(data, list):
        return data
    return data.get("events", data.get("items", []))


def ask_assistant(message: str) -> str:
    """
    Expected backend:
      POST /assistant/chat
      {
        "message": "...",
        "user_id": "..."
      }

    Expected response:
      {"response": "..."}
    """
    user = st.session_state.user or {}
    payload = {
        "message": message,
        "user_id": user.get("user_id") or user.get("id"),
    }
    data = api_request("POST", "/assistant/chat", json=payload)
    return data.get("response") or data.get("answer") or data.get("message") or str(data)


def get_user_name() -> str:
    user = st.session_state.user or {}
    return user.get("name") or user.get("full_name") or user.get("email", "User").split("@")[0]
def render_login():
    st.markdown("""
    <div class="login-wrap">
      <div class="login-brand">
        <div class="logo">✦</div>
        <h1>Eventify <span class="gradient-text">AI</span></h1>
        <p>Your intelligent event companion</p>
      </div>
      <div class="login-card">
    """, unsafe_allow_html=True)

    st.markdown("### Welcome back 👋")
    st.caption("Login to discover events and ask the AI assistant anything.")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign in to Eventify", use_container_width=True)

        if submitted:
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                try:
                    with st.spinner("Connecting to your account..."):
                        login_user(email, password)
                    st.success("Login successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.caption(f"Backend: `{BACKEND_URL}`")
def render_nav():
    name = get_user_name()
    st.markdown(f"""
    <div class="topnav">
      <div class="brand">
        <div class="logo">✦</div>
        <span>Eventify AI</span>
      </div>
      <div class="navright">
        <span class="navpill">Discover</span>
        <span class="navpill">My Events</span>
        <span class="navpill">AI Assistant</span>
        <span class="navpill">Hi, {name}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([6, 1])
    with c2:
        if st.button("Logout", use_container_width=True):
            for key in ["logged_in", "token", "user", "messages"]:
                st.session_state[key] = False if key == "logged_in" else ([] if key == "messages" else None)
            st.rerun()
def event_value(event, *keys, default="—"):
    for key in keys:
        value = event.get(key)
        if value not in (None, ""):
            return value
    return default

def render_event_card(event, idx):
    title = event_value(event, "title", "name", default="Untitled Event")
    category = event_value(event, "category", "event_type", default="EVENT")
    venue = event_value(event, "venue_name", "venue", "location", default="Venue TBA")
    date = event_value(event, "event_date", "date", "start_date", default="Date TBA")
    seats = event_value(event, "available_seats", "seats_available", default="—")
    status = event_value(event, "status", default="published")
    icons = ["🎤", "💻", "🎨", "🏆", "🎓", "🎵"]
    icon = icons[idx % len(icons)]

    st.markdown(f"""
    <div class="event-card">
      <div class="event-img">{icon}</div>
      <div class="event-body">
        <div class="event-category">{category}</div>
        <div class="event-title">{title}</div>
        <div class="event-meta">📅 {date}<br>📍 {venue}<br>👥 Available seats: {seats}</div>
        <span class="status">{status.upper()}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_home():
    render_nav()

    st.markdown("""
    <section class="hero">
      <span class="badge">✦ AI-powered event discovery</span>
      <h1>Smart Events.<br><span class="gradient-text">One Assistant.</span></h1>
      <p>
        Discover what's happening around you, find the right event,
        check availability and get instant answers — all through one
        intelligent event assistant connected to the backend.
      </p>
      <div class="hero-tags">
        <span class="hero-tag">LIVE EVENT DATA</span>
        <span class="hero-tag">AI ASSISTANT</span>
        <span class="hero-tag">PERSONALIZED</span>
        <span class="hero-tag">FAST DISCOVERY</span>
      </div>
    </section>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="assistant-card">
      <div class="assistant-title">✨ Ask AI Assistant anything</div>
      <div class="assistant-sub">
        Ask about upcoming events, venues, dates, seats, categories or recommendations.
      </div>
    """, unsafe_allow_html=True)

    if st.session_state.messages:
        for role, msg in st.session_state.messages[-6:]:
            css = "user-bubble" if role == "user" else "ai-bubble"
            prefix = "You" if role == "user" else "Eventify AI"
            st.markdown(f'<div class="chat-bubble {css}"><b>{prefix}</b><br>{msg}</div>', unsafe_allow_html=True)

    with st.form("assistant_form", clear_on_submit=True):
        prompt = st.text_input(
            "Ask your question",
            placeholder="e.g. Show me AI workshops this week...",
            label_visibility="collapsed",
        )
        ask = st.form_submit_button("Ask AI  →", use_container_width=True)

        if ask and prompt.strip():
            st.session_state.messages.append(("user", prompt.strip()))
            try:
                with st.spinner("AI is thinking..."):
                    answer = ask_assistant(prompt.strip())
            except Exception as e:
                answer = f"I couldn't reach the AI service right now. Backend says: {e}"
            st.session_state.messages.append(("assistant", answer))
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-head">
      <div>
        <h2>Upcoming events</h2>
        <p>Live data fetched from your Smart Event Management backend</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        events = get_events()
        if not events:
            st.info("No published events are available right now.")
        else:
            # Show up to 6 cards in a responsive grid.
            for start in range(0, min(len(events), 6), 3):
                cols = st.columns(3, gap="medium")
                for j, col in enumerate(cols):
                    i = start + j
                    if i < len(events):
                        with col:
                            render_event_card(events[i], i)
    except Exception as e:
        st.warning(f"Could not fetch events from backend: {e}")
    st.markdown("""
    <div class="section-head">
      <div>
        <h2>Built around your events</h2>
        <p>A clean user-side experience for the Smart Event Management System</p>
      </div>
    </div>

    <div class="feature">
      <div class="feature-icon">🧠</div>
      <h3>AI Event Assistant</h3>
      <p>Ask natural-language questions instead of searching multiple pages manually.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3, gap="medium")
    features = [
        ("🎟️", "Discover events", "Get published events directly from the backend."),
        ("📍", "Find the right place", "Ask the assistant about venues, dates and event details."),
        ("⚡", "Instant answers", "AI handles event-related queries through your agent API."),
    ]
    for col, (icon, title, desc) in zip([a, b, c], features):
        with col:
            st.markdown(f"""
            <div class="feature">
              <div class="feature-icon">{icon}</div>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height:45px"></div>
    <div style="text-align:center;color:#667085;font-size:11px;">
      Eventify AI • Smart Event Management System • User Portal
    </div>
    """, unsafe_allow_html=True)
if not st.session_state.logged_in:
    render_login()
else:
    render_home()
