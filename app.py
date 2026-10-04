import os
from typing import Any, Dict, List, Optional
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "").rstrip("/")
TIMEOUT = 12

st.set_page_config(
    page_title="Eventify — Smart Event Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #061329;
    --navy2: #091a36;
    --blue: #1677ff;
    --cyan: #39d8ff;
    --white: #f7fbff;
    --muted: #91a1ba;
    --line: rgba(148,181,226,.16);
    --glass: rgba(8,25,51,.72);
}

* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    color: var(--white);
    background:
      radial-gradient(circle at 8% 4%, rgba(23,119,255,.18), transparent 25%),
      radial-gradient(circle at 92% 15%, rgba(57,216,255,.10), transparent 24%),
      linear-gradient(180deg, #030b1b 0%, #061329 46%, #041025 100%);
}

.block-container {
    max-width: 1240px;
    padding: 0.8rem 1.7rem 4rem;
}
#MainMenu, footer { visibility: hidden; }
div[data-testid="stToolbar"] { display: none; }
header[data-testid="stHeader"] { background: transparent; }

.stButton > button {
    min-height: 42px;
    border-radius: 12px;
    border: 1px solid rgba(122,185,255,.22);
    background: rgba(13,43,82,.72);
    color: white;
    font-weight: 700;
    transition: .2s;
}
.stButton > button:hover {
    background: rgba(22,119,255,.18);
    border-color: rgba(57,216,255,.6);
    transform: translateY(-1px);
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background: #081a34 !important;
    border: 1px solid rgba(122,185,255,.18) !important;
    border-radius: 12px !important;
}
input, textarea { color: white !important; }

/* ---------- NAVBAR ---------- */
.navbar {
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--line);
    margin-bottom: 24px;
}
.brand {
    display:flex;
    align-items:center;
    gap:10px;
    font-weight:800;
    font-size:20px;
}
.brand-mark {
    width:35px;
    height:35px;
    display:grid;
    place-items:center;
    border-radius:10px;
    background:linear-gradient(135deg,#1680ff,#29d7ff);
    color:white;
    box-shadow:0 0 25px rgba(22,128,255,.35);
}
.nav-links {
    display:flex;
    align-items:center;
    gap:26px;
    color:#9aabc4;
    font-size:12px;
}
.nav-links span:first-child { color:white; }
.user-chip {
    padding:8px 12px;
    border-radius:20px;
    background:rgba(255,255,255,.045);
    border:1px solid var(--line);
}

/* ---------- HERO ---------- */
.hero {
    position:relative;
    overflow:hidden;
    min-height:475px;
    border-radius:28px;
    border:1px solid rgba(111,170,240,.22);
    background:
      linear-gradient(90deg, rgba(4,14,31,.98) 0%,
                        rgba(5,21,43,.90) 46%,
                        rgba(5,20,39,.62) 100%),
      radial-gradient(circle at 82% 52%, rgba(29,142,255,.42), transparent 30%),
      #071a35;
    box-shadow:0 30px 100px rgba(0,0,0,.35);
}

.hero:before {
    content:"";
    position:absolute;
    width:600px;
    height:600px;
    right:-150px;
    top:-120px;
    border-radius:50%;
    background:
      radial-gradient(circle, rgba(49,211,255,.28) 0 2%, transparent 2.5% 8%, rgba(49,211,255,.12) 8.5% 9%, transparent 9.5%);
    background-size:42px 42px;
    mask-image:radial-gradient(circle,black,transparent 68%);
    opacity:.65;
}
.hero:after {
    content:"✦";
    position:absolute;
    right:14%;
    top:23%;
    font-size:170px;
    color:rgba(55,216,255,.08);
    text-shadow:0 0 55px rgba(23,119,255,.45);
}
.hero-content {
    position:relative;
    z-index:2;
    padding:58px 52px;
    max-width:690px;
}
.eyebrow {
    display:inline-flex;
    align-items:center;
    gap:7px;
    color:#6ee4ff;
    border:1px solid rgba(57,216,255,.24);
    background:rgba(57,216,255,.06);
    border-radius:30px;
    padding:8px 13px;
    font-size:10px;
    font-weight:800;
    letter-spacing:.8px;
    text-transform:uppercase;
}
.hero h1 {
    margin:22px 0 16px;
    font-size:clamp(42px,5.6vw,70px);
    line-height:1.02;
    letter-spacing:-3px;
}
.grad {
    background:linear-gradient(90deg,#fff 5%,#65d8ff 58%,#4d82ff 100%);
    -webkit-background-clip:text;
    color:transparent;
}
.hero p {
    color:#9cadc6;
    max-width:590px;
    line-height:1.75;
    font-size:14px;
}
.hero-actions {
    display:flex;
    gap:10px;
    margin-top:27px;
}
.hero-mini {
    margin-top:32px;
    display:flex;
    gap:22px;
    flex-wrap:wrap;
    color:#8295b1;
    font-size:10px;
}
.hero-mini b { color:#dcecff; }

/* event illustration */
.stage {
    position:absolute;
    right:6%;
    bottom:0;
    width:42%;
    height:82%;
    opacity:.92;
}
.stage-screen {
    position:absolute;
    left:13%;
    top:13%;
    width:74%;
    height:42%;
    border:1px solid rgba(91,205,255,.5);
    border-radius:18px;
    background:
      radial-gradient(circle at 50% 35%, rgba(57,216,255,.40), transparent 20%),
      linear-gradient(145deg,#0d3a6a,#071426);
    box-shadow:0 0 55px rgba(23,119,255,.27);
}
.stage-screen:before {
    content:"SMART EVENT";
    position:absolute;
    left:12%;
    top:25%;
    color:#9feeff;
    font-size:11px;
    letter-spacing:3px;
}
.stage-screen:after {
    content:"AI ASSISTANT";
    position:absolute;
    left:12%;
    top:45%;
    color:white;
    font-weight:800;
    font-size:21px;
}
.spot {
    position:absolute;
    width:150px;
    height:150px;
    border-radius:50%;
    background:radial-gradient(circle,rgba(57,216,255,.55),transparent 65%);
    filter:blur(3px);
}
.spot.one { left:3%; top:30%; }
.spot.two { right:0; top:22%; }
.crowd {
    position:absolute;
    bottom:-15px;
    left:0;
    right:0;
    height:48%;
    background:
      radial-gradient(ellipse at 8% 85%, #020711 0 30px, transparent 31px),
      radial-gradient(ellipse at 20% 88%, #020711 0 37px, transparent 38px),
      radial-gradient(ellipse at 34% 82%, #020711 0 34px, transparent 35px),
      radial-gradient(ellipse at 48% 89%, #020711 0 40px, transparent 41px),
      radial-gradient(ellipse at 61% 82%, #020711 0 34px, transparent 35px),
      radial-gradient(ellipse at 75% 87%, #020711 0 42px, transparent 43px),
      radial-gradient(ellipse at 90% 82%, #020711 0 38px, transparent 39px);
}

/* ---------- SEARCH CARD ---------- */
.search-card {
    position:relative;
    z-index:5;
    margin:-44px 6% 0;
    padding:20px;
    border:1px solid rgba(130,185,240,.23);
    border-radius:19px;
    background:rgba(8,25,51,.94);
    box-shadow:0 20px 55px rgba(0,0,0,.30);
}
.search-title { font-size:14px; font-weight:800; }
.search-sub { font-size:10px; color:#8193ad; margin-top:3px; }

/* ---------- SECTIONS ---------- */
.section {
    margin-top:54px;
}
.section-top {
    display:flex;
    justify-content:space-between;
    align-items:end;
    margin-bottom:17px;
}
.section h2 {
    margin:0;
    font-size:27px;
    letter-spacing:-1px;
}
.section-top p {
    margin:5px 0 0;
    color:#8293ad;
    font-size:11px;
}

/* ---------- EVENT CARDS ---------- */
.event-card {
    overflow:hidden;
    border-radius:17px;
    border:1px solid var(--line);
    background:linear-gradient(180deg,#0a1b35,#07152b);
    box-shadow:0 18px 50px rgba(0,0,0,.22);
}
.event-art {
    height:125px;
    display:grid;
    place-items:center;
    position:relative;
    overflow:hidden;
    background:
      radial-gradient(circle at 65% 30%,rgba(57,216,255,.27),transparent 25%),
      linear-gradient(135deg,#0b2b53,#071225);
}
.event-art .big { font-size:53px; filter:drop-shadow(0 0 15px rgba(57,216,255,.35)); }
.event-art .line {
    position:absolute;
    width:80%;
    height:1px;
    bottom:23px;
    background:linear-gradient(90deg,transparent,#31d8ff,transparent);
}
.event-body { padding:15px; }
.category {
    color:#63dcff;
    font-size:9px;
    font-weight:800;
    letter-spacing:.8px;
    text-transform:uppercase;
}
.event-title { font-size:15px; font-weight:750; margin-top:6px; }
.meta {
    color:#8294af;
    font-size:10px;
    line-height:1.8;
    margin-top:9px;
}
.badge-live {
    display:inline-block;
    margin-top:10px;
    padding:5px 8px;
    border-radius:7px;
    color:#69edbd;
    background:rgba(45,226,157,.07);
    border:1px solid rgba(45,226,157,.14);
    font-size:9px;
    font-weight:800;
}

/* ---------- AI ---------- */
.ai-panel {
    border:1px solid rgba(69,186,255,.2);
    border-radius:22px;
    padding:23px;
    background:
      radial-gradient(circle at 95% 5%,rgba(28,129,255,.12),transparent 28%),
      #07172f;
    box-shadow:0 20px 60px rgba(0,0,0,.22);
}
.ai-heading {
    display:flex;
    gap:12px;
    align-items:center;
}
.ai-icon {
    width:43px;height:43px;border-radius:13px;
    display:grid;place-items:center;
    background:linear-gradient(135deg,#147bff,#31d8ff);
    box-shadow:0 0 25px rgba(22,123,255,.3);
}
.ai-heading b { font-size:15px; }
.ai-heading span { display:block;color:#8295af;font-size:10px;margin-top:3px; }
.chat {
    padding:12px 14px;
    border-radius:13px;
    margin-top:9px;
    font-size:12px;
    line-height:1.55;
}
.chat.user {
    background:rgba(24,112,255,.12);
    border:1px solid rgba(24,112,255,.15);
}
.chat.ai {
    background:rgba(255,255,255,.035);
    border:1px solid var(--line);
}

/* ---------- FEATURES ---------- */
.feature {
    min-height:150px;
    padding:22px;
    border:1px solid var(--line);
    border-radius:17px;
    background:rgba(8,25,51,.55);
}
.feature-icon { font-size:24px; }
.feature h3 { font-size:14px; margin:13px 0 7px; }
.feature p { color:#8192ab; font-size:10px; line-height:1.65; }

/* ---------- LOGIN ---------- */
.login-wrap {
    max-width:440px;
    margin:9vh auto;
}
.login-head { text-align:center; margin-bottom:25px; }
.login-head .brand-mark { margin:auto; }
.login-head h1 { font-size:35px; margin:15px 0 5px; }
.login-head p { color:#8293ad; font-size:12px; }
.login-card {
    padding:29px;
    border:1px solid var(--line);
    border-radius:22px;
    background:rgba(7,23,47,.9);
    box-shadow:0 30px 90px rgba(0,0,0,.32);
}

/* ---------- MOBILE ---------- */
@media(max-width:800px) {
    .block-container { padding: .7rem 1rem 3rem; }
    .nav-links { display:none; }
    .hero { min-height:560px; }
    .hero-content { padding:34px 25px; }
    .hero h1 { font-size:43px; }
    .stage { width:92%; right:4%; height:42%; opacity:.7; }
    .search-card { margin:-30px 3% 0; }
}
</style>
""", unsafe_allow_html=True)

for key, default in [
    ("logged_in", False),
    ("token", None),
    ("user", None),
    ("messages", []),
]:
    if key not in st.session_state:
        st.session_state[key] = default
def api(method: str, endpoint: str, *, json=None, params=None, auth=True):
    headers = {"Accept": "application/json"}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    r = requests.request(
        method,
        f"{BACKEND_URL}{endpoint}",
        json=json,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )
    if not r.ok:
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        raise RuntimeError(f"{r.status_code}: {detail}")
    return r.json() if r.content else {}


def login(email, password):
    data = api(
        "POST",
        "/auth/login",
        json={"email": email, "password": password},
        auth=False,
    )
    token = data.get("access_token") or data.get("token")
    if not token:
        raise RuntimeError("Backend login response has no access_token/token.")

    st.session_state.token = token
    st.session_state.user = data.get("user") or {
        "email": email,
        "name": data.get("name", email.split("@")[0]),
        "user_id": data.get("user_id") or data.get("id"),
    }
    st.session_state.logged_in = True


def events():
    data = api("GET", "/events", params={"status": "published"})
    if isinstance(data, list):
        return data
    return data.get("events", data.get("items", []))


def ask_ai(question):
    user = st.session_state.user or {}
    data = api(
        "POST",
        "/assistant/chat",
        json={
            "message": question,
            "user_id": user.get("user_id") or user.get("id"),
        },
    )
    return data.get("response") or data.get("answer") or data.get("message") or str(data)


def username():
    u = st.session_state.user or {}
    return u.get("name") or u.get("full_name") or u.get("email", "User").split("@")[0]


def value(e, *keys, default="—"):
    for k in keys:
        if e.get(k) not in (None, ""):
            return e[k]
    return default

def login_page():
    st.markdown("""
    <div class="login-wrap">
      <div class="login-head">
        <div class="brand-mark">✦</div>
        <h1>Eventify <span class="grad">AI</span></h1>
        <p>Where every event begins — intelligently.</p>
      </div>
      <div class="login-card">
    """, unsafe_allow_html=True)

    st.markdown("### Welcome back 👋")
    st.caption("Sign in to discover events and talk to your AI event assistant.")

    with st.form("login"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submit = st.form_submit_button("Continue to Eventify  →", use_container_width=True)

        if submit:
            if not email or not password:
                st.warning("Enter your email and password.")
            else:
                try:
                    with st.spinner("Signing you in..."):
                        login(email, password)
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

    st.markdown("</div></div>", unsafe_allow_html=True)
def nav():
    st.markdown(f"""
    <div class="navbar">
      <div class="brand">
        <div class="brand-mark">✦</div>
        <span>Eventify AI</span>
      </div>
      <div class="nav-links">
        <span>Home</span>
        <span>Upcoming Events</span>
        <span>AI Assistant</span>
        <span class="user-chip">Hi, {username()}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Small logout button without disturbing navbar visual.
    _, logout_col = st.columns([9, 1])
    with logout_col:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.messages = []
            st.rerun()
def event_card(e, index):
    icons = ["🎤", "💻", "🎓", "🏆", "🎨", "🎵"]
    title = value(e, "title", "name", default="Untitled Event")
    category = value(e, "category", "event_type", default="EVENT")
    date = value(e, "event_date", "date", "start_date", default="Date TBA")
    venue = value(e, "venue_name", "venue", "location", default="Venue TBA")
    seats = value(e, "available_seats", "seats_available", default="—")
    status = value(e, "status", default="published")

    st.markdown(f"""
    <div class="event-card">
      <div class="event-art">
        <div class="big">{icons[index % len(icons)]}</div>
        <div class="line"></div>
      </div>
      <div class="event-body">
        <div class="category">{category}</div>
        <div class="event-title">{title}</div>
        <div class="meta">
          📅 {date}<br>
          📍 {venue}<br>
          👥 {seats} seats available
        </div>
        <span class="badge-live">{str(status).upper()}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def home():
    nav()

    # HERO
    st.markdown("""
    <div class="hero">
      <div class="hero-content">
        <span class="eyebrow">✦ SMART EVENT DISCOVERY</span>
        <h1>Where Every<br><span class="grad">Event Begins.</span></h1>
        <p>
          Discover upcoming events, explore venues and get instant answers
          with your AI-powered event companion — all connected to live
          Smart Event Management data.
        </p>

        <div class="hero-actions">
          <span class="eyebrow">● LIVE BACKEND DATA</span>
          <span class="eyebrow">AI ASSISTED</span>
        </div>

        <div class="hero-mini">
          <span><b>01</b> Discover</span>
          <span><b>02</b> Ask AI</span>
          <span><b>03</b> Find your event</span>
        </div>
      </div>

      <div class="stage">
        <div class="spot one"></div>
        <div class="spot two"></div>
        <div class="stage-screen"></div>
        <div class="crowd"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # SEARCH / FILTER STYLE CARD
    st.markdown("""
    <div class="search-card">
      <div class="search-title">Find your next experience ✦</div>
      <div class="search-sub">Use the AI Assistant for natural-language event discovery.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)

    # AI
    st.markdown("""
    <div class="ai-panel">
      <div class="ai-heading">
        <div class="ai-icon">✦</div>
        <div>
          <b>Ask AI Assistant anything</b>
          <span>Events • Venues • Dates • Availability • Recommendations</span>
        </div>
      </div>
    """, unsafe_allow_html=True)

    if st.session_state.messages:
        for role, msg in st.session_state.messages[-6:]:
            cls = "user" if role == "user" else "ai"
            label = "You" if role == "user" else "Eventify AI"
            st.markdown(f'<div class="chat {cls}"><b>{label}</b><br>{msg}</div>', unsafe_allow_html=True)

    with st.form("assistant", clear_on_submit=True):
        q = st.text_input(
            "Ask AI",
            placeholder="Try: Show me AI workshops happening this week...",
            label_visibility="collapsed",
        )
        ask = st.form_submit_button("Ask Assistant  →", use_container_width=True)

        if ask and q.strip():
            st.session_state.messages.append(("user", q.strip()))
            try:
                with st.spinner("Finding the best answer..."):
                    ans = ask_ai(q.strip())
            except Exception as e:
                ans = f"AI service unavailable: {e}"
            st.session_state.messages.append(("ai", ans))
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # EVENTS
    st.markdown("""
    <div class="section-top" style="margin-top:52px;">
      <div>
        <h2>Upcoming Events</h2>
        <p>Live published events fetched directly from your backend</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        items = events()
        if not items:
            st.info("No published events are available right now.")
        else:
            for start in range(0, min(len(items), 9), 3):
                cols = st.columns(3, gap="medium")
                for j, col in enumerate(cols):
                    i = start + j
                    if i < len(items):
                        with col:
                            event_card(items[i], i)
    except Exception as e:
        st.warning(f"Unable to fetch events: {e}")

    # FEATURES
    st.markdown("""
    <div class="section-top" style="margin-top:58px;">
      <div>
        <h2>Everything in one place</h2>
        <p>Designed for the user side of your Smart Event Management System</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    features = [
        ("🎟️", "Discover Events", "Browse live published events from the backend without manually searching multiple pages."),
        ("✦", "AI Event Assistant", "Ask natural-language questions and let your agent find relevant event information."),
        ("⚡", "Fast Experience", "A clean user portal focused on quick discovery, availability and useful answers."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature">
              <div class="feature-icon">{icon}</div>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height:48px"></div>
    <div style="text-align:center;color:#61728d;font-size:10px;">
      EVENTIFY AI · SMART EVENT MANAGEMENT SYSTEM
    </div>
    """, unsafe_allow_html=True)
if st.session_state.logged_in:
    home()
else:
    login_page()
