import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ARXIS · Research Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Epilogue:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
    --bg:       #080810;
    --bg2:      #0d0d1a;
    --surface:  #10101f;
    --border:   #1a1a30;
    --amber:    #f5a623;
    --cyan:     #00d4ff;
    --red:      #ff4560;
    --green:    #00e096;
    --text:     #ddd8f0;
    --muted:    #4a4a6a;
    --mono:     'IBM Plex Mono', monospace;
    --display:  'Bebas Neue', sans-serif;
    --body:     'Epilogue', sans-serif;
}

html, body, [class*="css"], .stApp {
    font-family: var(--body);
    color: var(--text);
    background: var(--bg) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 55% 35% at 10% 5%,  rgba(245,166,35,0.07) 0%, transparent 65%),
        radial-gradient(ellipse 40% 30% at 90% 90%, rgba(0,212,255,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2.5rem 4rem;
    max-width: 1300px;
    position: relative;
    z-index: 1;
}

/* ── TOP BAR ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.4rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
}
.topbar-logo {
    font-family: var(--display);
    font-size: 1.8rem;
    letter-spacing: 0.12em;
    color: var(--text);
    line-height: 1;
}
.topbar-logo span { color: var(--amber); }
.topbar-tag {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    border: 1px solid var(--border);
    padding: 0.3rem 0.7rem;
    border-radius: 3px;
}
.topbar-dot {
    width: 7px; height: 7px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--green);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── HERO ── */
.hero {
    padding: 0 0 3rem;
    max-width: 820px;
}
.hero-kicker {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hero-kicker::before {
    content: '';
    display: inline-block;
    width: 24px; height: 1px;
    background: var(--cyan);
}
.hero h1 {
    font-family: var(--display);
    font-size: clamp(3.5rem, 7vw, 6.5rem);
    font-weight: 400;
    line-height: 0.92;
    letter-spacing: 0.04em;
    color: var(--text);
    margin: 0 0 1.5rem;
}
.hero h1 em { color: var(--amber); font-style: normal; }
.hero-desc {
    font-size: 1rem;
    font-weight: 300;
    color: var(--muted);
    line-height: 1.75;
    max-width: 560px;
}

/* ── INPUT ZONE ── */
.input-zone {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    max-width: 860px;
}
.input-zone::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--amber), var(--cyan));
}
.input-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 0.6rem;
}

/* ── EXAMPLES ── */
.examples-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
    align-items: center;
}
.ex-chip {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 0.28rem 0.65rem;
    background: var(--bg2);
}

/* ── STREAMLIT OVERRIDES ── */
.stTextInput > div > div > input {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
    font-size: 1rem !important;
    padding: 0.85rem 1rem !important;
    caret-color: var(--amber) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 2px rgba(245,166,35,0.15) !important;
}
.stTextInput > label { display: none !important; }

.stButton > button {
    background: var(--amber) !important;
    color: #080810 !important;
    font-family: var(--display) !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(245,166,35,0.2) !important;
    transition: box-shadow 0.2s, opacity 0.2s !important;
    margin-top: 0.8rem !important;
}
.stButton > button:hover {
    box-shadow: 0 0 36px rgba(245,166,35,0.4) !important;
    opacity: 0.92 !important;
}
.stSpinner > div { color: var(--amber) !important; }

/* ── SECTION DIVIDER ── */
.sec-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border) 30%, var(--border) 70%, transparent);
    margin: 3rem 0 2.5rem;
}

/* ── RESULTS ── */
.results-header {
    font-family: var(--display);
    font-size: 2.8rem;
    letter-spacing: 0.06em;
    color: var(--text);
    margin-bottom: 2rem;
    line-height: 1;
}
.results-header span { color: var(--cyan); }

/* ── RAW CARDS ── */
.raw-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.raw-card-header {
    padding: 0.7rem 1.2rem;
    border-bottom: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--cyan);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.raw-card-header::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 6px var(--cyan);
}
.raw-card-body {
    padding: 1rem 1.2rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    color: #7070a0;
    line-height: 1.8;
    max-height: 220px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.raw-card-body::-webkit-scrollbar { width: 3px; }
.raw-card-body::-webkit-scrollbar-thumb { background: var(--border); }

/* ── REPORT CARD ── */
.report-card {
    background: var(--surface);
    border: 1px solid rgba(245,166,35,0.25);
    border-radius: 4px;
    padding: 2.5rem 3rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}
.report-card::before {
    content: 'REPORT';
    position: absolute;
    top: 1.6rem; right: 2rem;
    font-family: var(--display);
    font-size: 4.5rem;
    letter-spacing: 0.1em;
    color: rgba(245,166,35,0.04);
    line-height: 1;
    pointer-events: none;
    user-select: none;
}
.report-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--amber) 0%, transparent 100%);
}
.report-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.report-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(245,166,35,0.3), transparent);
}

/* ── CRITIC CARD ── */
.critic-card {
    background: var(--surface);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 4px;
    padding: 2rem 2.5rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}
.critic-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--cyan) 0%, transparent 100%);
}
.critic-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.critic-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,212,255,0.3), transparent);
}
.score-block {
    display: inline-flex;
    align-items: baseline;
    gap: 0.3rem;
    margin-bottom: 1.5rem;
    padding: 0.6rem 1.2rem;
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 3px;
    background: rgba(0,212,255,0.05);
}
.score-num {
    font-family: var(--display);
    font-size: 2.8rem;
    color: var(--cyan);
    line-height: 1;
    text-shadow: 0 0 20px rgba(0,212,255,0.5);
}
.score-denom {
    font-family: var(--mono);
    font-size: 0.9rem;
    color: var(--muted);
}

/* ── DOWNLOAD BTN ── */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--amber) !important;
    border: 1px solid rgba(245,166,35,0.4) !important;
    border-radius: 3px !important;
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    padding: 0.5rem 1.2rem !important;
    transition: background 0.2s, box-shadow 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(245,166,35,0.08) !important;
    box-shadow: 0 0 16px rgba(245,166,35,0.15) !important;
}

[data-testid="stAlert"] {
    background: rgba(255,69,96,0.08) !important;
    border: 1px solid rgba(255,69,96,0.3) !important;
    border-radius: 4px !important;
    color: var(--red) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_score(feedback: str) -> str:
    for line in feedback.splitlines():
        if line.strip().lower().startswith("score"):
            parts = line.strip().split(":")
            if len(parts) > 1:
                return parts[1].strip().split("/")[0].strip()
    return "—"


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("results", {}), ("running", False), ("done", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── TOP BAR ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">ARX<span>IS</span></div>
    <div style="display:flex;align-items:center;gap:1rem;">
        <div class="topbar-tag">RESEARCH INTELLIGENCE</div>
        <div class="topbar-dot"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Multi-Agent AI Pipeline</div>
    <h1>DEEP<br><em>RESEARCH</em><br>ENGINE</h1>
    <p class="hero-desc">
        Four specialized agents collaborate in sequence — hunting, extracting,
        writing, and critiquing — to deliver intelligence-grade research on any topic.
    </p>
</div>
""", unsafe_allow_html=True)

# ── INPUT ZONE ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-zone">', unsafe_allow_html=True)
st.markdown('<div class="input-label">◈ &nbsp;Research Target</div>', unsafe_allow_html=True)
topic = st.text_input(
    "",
    placeholder="e.g. 'LLM agents 2025' or 'CRISPR breakthroughs'",
    key="topic_input",
    label_visibility="collapsed",
)
run_btn = st.button("INITIATE RESEARCH PIPELINE →", use_container_width=True)
st.markdown("""
<div class="examples-row">
    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:#4a4a6a;letter-spacing:0.15em;">TRY →</span>
    <span class="ex-chip">Quantum computing 2025</span>
    <span class="ex-chip">Fusion energy progress</span>
    <span class="ex-chip">LangChain vs LlamaIndex</span>
    <span class="ex-chip">CRISPR gene editing</span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── TRIGGER ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠  No target specified. Enter a research topic.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done    = False
        st.rerun()

# ── PIPELINE EXECUTION ────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    results   = {}
    topic_val = st.session_state.topic_input

    with st.spinner("01 · Search Agent scanning the web…"):
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]})
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("02 · Reader Agent extracting deep content…"):
        ra = build_reader_agent()
        rr = ra.invoke({"messages": [("user",
            f"Based on the following search results about '{topic_val}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{results['search'][:800]}")]})
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("03 · Writer composing the research report…"):
        combined = f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED SCRAPED CONTENT:\n{results['reader']}"
        results["writer"] = writer_chain.invoke({"topic": topic_val, "research": combined})
        st.session_state.results = dict(results)

    with st.spinner("04 · Critic reviewing and scoring the report…"):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()

# ── RESULTS ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="results-header">INTEL <span>OUTPUT</span></div>', unsafe_allow_html=True)

    col_s, col_rd = st.columns(2)
    with col_s:
        if "search" in r:
            st.markdown(f"""
            <div class="raw-card">
                <div class="raw-card-header">Search Agent · Raw Output</div>
                <div class="raw-card-body">{r['search']}</div>
            </div>""", unsafe_allow_html=True)
    with col_rd:
        if "reader" in r:
            st.markdown(f"""
            <div class="raw-card">
                <div class="raw-card-header">Reader Agent · Scraped Content</div>
                <div class="raw-card-body">{r['reader']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    col_rep, col_crit = st.columns([3, 2])

    with col_rep:
        if "writer" in r:
            st.markdown("""
            <div class="report-card">
                <div class="report-label">Final Research Report</div>
            """, unsafe_allow_html=True)
            st.markdown(r["writer"])
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                label="↓  EXPORT REPORT (.md)",
                data=r["writer"],
                file_name=f"arxis_report_{int(time.time())}.md",
                mime="text/markdown",
            )

    with col_crit:
        if "critic" in r:
            score = extract_score(r["critic"])
            st.markdown(f"""
            <div class="critic-card">
                <div class="critic-label">Critic Intelligence Review</div>
                <div class="score-block">
                    <span class="score-num">{score}</span>
                    <span class="score-denom">/10</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(r["critic"])
            st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    margin-top:4rem;
    padding-top:1.5rem;
    border-top:1px solid #1a1a30;
    display:flex;
    justify-content:space-between;
    align-items:center;
">
    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:#4a4a6a;letter-spacing:0.15em;">
        ARXIS · RESEARCH INTELLIGENCE SYSTEM
    </span>
    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:#4a4a6a;letter-spacing:0.1em;">
        POWERED BY LANGCHAIN · OPENROUTER
    </span>
</div>
""", unsafe_allow_html=True)