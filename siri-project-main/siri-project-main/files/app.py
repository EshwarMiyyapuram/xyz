"""
Smart Medicine Reminder & Health Tracker
Premium dark glassmorphism UI — bioluminescent health aesthetic.
"""

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, date

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MedTrack Pro · Health Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PREMIUM CSS — Dark Glass + Bioluminescent
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

:root {
  --cyan:      #00e5ff;
  --cyan-dim:  rgba(0,229,255,.13);
  --cyan-glow: rgba(0,229,255,.3);
  --mint:      #00ffa3;
  --mint-dim:  rgba(0,255,163,.12);
  --rose:      #ff4d8d;
  --rose-dim:  rgba(255,77,141,.13);
  --amber:     #ffb300;
  --amber-dim: rgba(255,179,0,.13);
  --violet:    #b388ff;
  --bg-deep:   #060d14;
  --bg-mid:    #0a1628;
  --bg-card:   rgba(255,255,255,.04);
  --border:    rgba(255,255,255,.07);
  --border-hi: rgba(0,229,255,.28);
  --text-hi:   #f0f9ff;
  --text-mid:  #94a3b8;
  --text-lo:   #334155;
  --r-xl: 24px; --r-lg: 16px; --r-md: 12px;
}

html, body, [class*="css"], .stApp {
  font-family: 'Outfit', sans-serif !important;
  background: var(--bg-deep) !important;
  color: var(--text-hi) !important;
}

/* Ambient glow background */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 70% 45% at 15% 8%,  rgba(0,229,255,.07) 0%, transparent 60%),
    radial-gradient(ellipse 55% 40% at 85% 85%, rgba(0,255,163,.05) 0%, transparent 55%),
    radial-gradient(ellipse 50% 50% at 50% 50%, rgba(179,136,255,.03) 0%, transparent 60%);
  pointer-events: none; z-index: 0;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #070e1a 0%, #091424 100%) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-hi) !important; }
section[data-testid="stSidebar"] .stRadio label {
  font-size: .93rem !important; font-weight: 500 !important;
  padding: .6rem 1rem !important; border-radius: var(--r-md) !important;
  color: var(--text-mid) !important; transition: all .2s !important;
  border: 1px solid transparent !important; cursor: pointer !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
  background: var(--cyan-dim) !important; color: var(--cyan) !important;
  border-color: var(--border-hi) !important;
}

/* ── GLASS CARD ── */
.glass-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 1.75rem 2rem;
  margin-bottom: 1.25rem;
  position: relative; overflow: hidden;
  transition: border-color .25s, box-shadow .25s;
}
.glass-card::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,.025) 0%, transparent 55%);
  pointer-events: none;
}
.glass-card:hover { border-color: rgba(0,229,255,.18); box-shadow: 0 0 40px rgba(0,229,255,.05), 0 8px 32px rgba(0,0,0,.35); }
.glass-card.ac-cyan   { border-color: rgba(0,229,255,.22);  box-shadow: 0 0 28px rgba(0,229,255,.05); }
.glass-card.ac-mint   { border-color: rgba(0,255,163,.22);  box-shadow: 0 0 28px rgba(0,255,163,.05); }
.glass-card.ac-rose   { border-color: rgba(255,77,141,.22); box-shadow: 0 0 28px rgba(255,77,141,.05); }
.glass-card.ac-amber  { border-color: rgba(255,179,0,.22);  box-shadow: 0 0 28px rgba(255,179,0,.05); }

.card-label { font-size:.68rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--text-lo); margin-bottom:.5rem; }
.card-title { font-size:1.05rem; font-weight:600; color:var(--text-hi); margin-bottom:1rem; }

/* ── HERO ── */
.hero-banner {
  background: linear-gradient(130deg, #091e35 0%, #071220 55%, #091828 100%);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 2.5rem 2.75rem;
  margin-bottom: 2rem;
  position: relative; overflow: hidden;
}
.hero-banner::before {
  content: '';
  position: absolute; top: -55%; right: -5%;
  width: 480px; height: 480px;
  background: radial-gradient(circle, rgba(0,229,255,.11) 0%, transparent 65%);
  pointer-events: none;
}
.hero-banner::after {
  content: '';
  position: absolute; bottom: -45%; left: 25%;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(0,255,163,.06) 0%, transparent 65%);
  pointer-events: none;
}
.hero-eyebrow { font-size:.7rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:var(--cyan); margin-bottom:.7rem; }
.hero-title { font-family:'Playfair Display',serif; font-size:2.5rem; font-weight:700; color:var(--text-hi); line-height:1.15; margin-bottom:.7rem; }
.hero-title em { color:var(--cyan); font-style:italic; }
.hero-sub { font-size:.97rem; color:var(--text-mid); max-width:520px; line-height:1.65; }

/* ── STAT STRIP ── */
.stat-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.75rem; }
.stat-tile {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 1.2rem 1.4rem;
  position: relative; overflow: hidden;
  transition: transform .2s, box-shadow .2s;
}
.stat-tile:hover { transform: translateY(-3px); box-shadow: 0 12px 36px rgba(0,0,0,.4); }
.stat-tile::after { content:''; position:absolute; bottom:0; left:0; right:0; height:3px; border-radius:0 0 var(--r-lg) var(--r-lg); }
.stat-tile.sc::after  { background: linear-gradient(90deg, var(--cyan), transparent); }
.stat-tile.sm::after  { background: linear-gradient(90deg, var(--mint), transparent); }
.stat-tile.sr::after  { background: linear-gradient(90deg, var(--rose), transparent); }
.stat-tile.sa::after  { background: linear-gradient(90deg, var(--amber), transparent); }
.stat-tile.sv::after  { background: linear-gradient(90deg, var(--violet), transparent); }
.tile-icon  { font-size:1.5rem; margin-bottom:.5rem; display:block; }
.tile-val   { font-size:1.9rem; font-weight:800; line-height:1.1; margin-bottom:.3rem; }
.tile-label { font-size:.75rem; color:var(--text-mid); font-weight:500; letter-spacing:.03em; }
.stat-tile.sc .tile-val { color:var(--cyan); }
.stat-tile.sm .tile-val { color:var(--mint); }
.stat-tile.sr .tile-val { color:var(--rose); }
.stat-tile.sa .tile-val { color:var(--amber); }
.stat-tile.sv .tile-val { color:var(--violet); }

/* ── SECTION HEADING ── */
.s-eye  { font-size:.66rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--cyan); margin-bottom:.3rem; }
.s-head { font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:700; color:var(--text-hi); margin-bottom:1.2rem; }

/* ── PILL ── */
.pill { display:inline-flex; align-items:center; padding:.28rem .8rem; border-radius:999px; font-size:.78rem; font-weight:600; }
.p-c { background:var(--cyan-dim);  color:var(--cyan);  border:1px solid rgba(0,229,255,.2); }
.p-m { background:var(--mint-dim);  color:var(--mint);  border:1px solid rgba(0,255,163,.2); }
.p-r { background:var(--rose-dim);  color:var(--rose);  border:1px solid rgba(255,77,141,.2); }
.p-a { background:var(--amber-dim); color:var(--amber); border:1px solid rgba(255,179,0,.2); }
.p-v { background:rgba(179,136,255,.12); color:var(--violet); border:1px solid rgba(179,136,255,.2); }

/* ── MED ROW ── */
.med-row {
  display:flex; align-items:center; justify-content:space-between;
  padding:.7rem 1rem;
  border-radius:var(--r-md);
  background:rgba(255,255,255,.025);
  border:1px solid var(--border);
  margin-bottom:.45rem;
  transition:all .2s;
}
.med-row:hover { background:rgba(0,229,255,.05); border-color:rgba(0,229,255,.15); }
.med-name { font-weight:600; font-size:.92rem; color:var(--text-hi); }
.med-sub  { font-size:.78rem; color:var(--text-mid); margin-top:.1rem; }

/* ── ORB STATUS ── */
.orb {
  width:72px; height:72px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:1.6rem; margin:0 auto .8rem;
  position:relative;
}
.orb::after {
  content:''; position:absolute; inset:-6px;
  border-radius:50%; border:2px solid;
  opacity:.35;
  animation: pulse 2.2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{transform:scale(1);opacity:.35} 50%{transform:scale(1.12);opacity:.12} }
.o-g  { background:rgba(0,255,163,.12); border:1px solid rgba(0,255,163,.3); }
.o-g::after { border-color:var(--mint); }
.o-w  { background:rgba(255,179,0,.12); border:1px solid rgba(255,179,0,.3); }
.o-w::after { border-color:var(--amber); }
.o-b  { background:rgba(255,77,141,.12); border:1px solid rgba(255,77,141,.3); }
.o-b::after { border-color:var(--rose); }

/* ── TIP CARD ── */
.tip-tile {
  background:var(--bg-card); border:1px solid var(--border);
  border-radius:var(--r-lg); padding:1.2rem .9rem; text-align:center;
  transition:transform .2s, border-color .2s;
}
.tip-tile:hover { transform:translateY(-4px); border-color:rgba(0,229,255,.2); }
.tip-tile .ti { font-size:1.8rem; margin-bottom:.5rem; }
.tip-tile .tt { font-weight:700; font-size:.86rem; color:var(--text-hi); margin-bottom:.3rem; }
.tip-tile .td { font-size:.75rem; color:var(--text-mid); line-height:1.55; }

/* ── DIVIDER ── */
.dvd { height:1px; background:linear-gradient(90deg,transparent,var(--border),transparent); margin:1.5rem 0; }

/* ── INPUT OVERRIDES ── */
.stTextInput input, .stNumberInput input, .stDateInput input {
  background:rgba(255,255,255,.04) !important;
  border:1px solid var(--border) !important;
  border-radius:var(--r-md) !important;
  color:var(--text-hi) !important;
  font-family:'Outfit',sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color:var(--cyan) !important;
  box-shadow:0 0 0 3px rgba(0,229,255,.1) !important;
  outline:none !important;
}
label { color:var(--text-mid) !important; font-weight:500 !important; font-size:.86rem !important; }

/* ── BUTTON ── */
.stButton > button {
  background:linear-gradient(135deg,#00b8d4,#0077a8) !important;
  color:#fff !important; border:none !important;
  border-radius:var(--r-md) !important;
  padding:.55rem 1.5rem !important;
  font-family:'Outfit',sans-serif !important;
  font-weight:600 !important; font-size:.9rem !important;
  letter-spacing:.03em !important;
  box-shadow:0 4px 18px rgba(0,184,212,.25) !important;
  transition:all .2s !important;
}
.stButton > button:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 8px 28px rgba(0,184,212,.35) !important;
  filter:brightness(1.08) !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
  background:var(--bg-card) !important;
  border:1px solid var(--border) !important;
  border-radius:var(--r-lg) !important;
  padding:1rem 1.25rem !important;
}
[data-testid="stMetricLabel"] { color:var(--text-mid) !important; font-size:.78rem !important; font-weight:500 !important; }
[data-testid="stMetricValue"] { color:var(--cyan) !important; font-size:1.55rem !important; font-weight:700 !important; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius:var(--r-lg) !important; border:1px solid var(--border) !important; overflow:hidden !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
  background:rgba(0,229,255,.07) !important;
  color:var(--cyan) !important;
  border:1px solid rgba(0,229,255,.22) !important;
  box-shadow:none !important;
}
.stDownloadButton > button:hover { background:rgba(0,229,255,.14) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg-deep); }
::-webkit-scrollbar-thumb { background:rgba(0,229,255,.18); border-radius:99px; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility:hidden !important; }

/* select box dark */
div[data-baseweb="select"] > div {
  background:rgba(255,255,255,.04) !important;
  border:1px solid var(--border) !important;
  border-radius:var(--r-md) !important;
  color:var(--text-hi) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
DB_PATH = "health_tracker.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn(); c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, dosage TEXT NOT NULL,
        time TEXT NOT NULL, added_on TEXT NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL, blood_pressure TEXT,
        sugar_level REAL, heart_rate INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY, name TEXT, age INTEGER, weight REAL)""")
    conn.commit(); conn.close()

def add_medicine(name, dosage, time_str):
    conn = get_conn()
    conn.execute("INSERT INTO medicines (name,dosage,time,added_on) VALUES (?,?,?,?)",
                 (name, dosage, time_str, datetime.now().strftime("%Y-%m-%d")))
    conn.commit(); conn.close()

def get_medicines():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM medicines ORDER BY id DESC", conn)
    conn.close(); return df

def delete_medicine(mid):
    conn = get_conn()
    conn.execute("DELETE FROM medicines WHERE id=?", (mid,))
    conn.commit(); conn.close()

def add_health_record(date_str, bp, sugar, hr):
    conn = get_conn()
    conn.execute("INSERT INTO health_records (date,blood_pressure,sugar_level,heart_rate) VALUES (?,?,?,?)",
                 (date_str, bp, sugar, hr))
    conn.commit(); conn.close()

def get_health_records():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM health_records ORDER BY date DESC", conn)
    conn.close(); return df

def save_profile(name, age, weight):
    conn = get_conn()
    conn.execute("DELETE FROM user_profile")
    conn.execute("INSERT INTO user_profile (id,name,age,weight) VALUES (1,?,?,?)", (name, age, weight))
    conn.commit(); conn.close()

def load_profile():
    conn = get_conn()
    row = conn.execute("SELECT name,age,weight FROM user_profile WHERE id=1").fetchone()
    conn.close()
    return {"name": row[0], "age": row[1], "weight": row[2]} if row else {"name":"","age":30,"weight":70.0}

# ─────────────────────────────────────────────
# DARK CHARTS
# ─────────────────────────────────────────────
def dark_axes(fig, ax, title):
    fig.patch.set_facecolor('#0a1628')
    ax.set_facecolor('#060d14')
    for s in ax.spines.values(): s.set_color('#1a2744')
    ax.tick_params(colors='#475569', labelsize=7.5)
    ax.set_title(title, color='#e2e8f0', fontsize=11.5,
                 fontfamily='sans-serif', fontweight='600', pad=12)
    ax.grid(axis='y', color='#0f1f33', linewidth=0.8, linestyle='--', alpha=.9)
    ax.grid(axis='x', visible=False)

def chart_bp(df):
    fig, ax = plt.subplots(figsize=(5.5, 2.85))
    dark_axes(fig, ax, '🩺  Blood Pressure Trend')
    if df.empty:
        ax.text(.5,.5,'No data yet',ha='center',va='center',color='#334155'); return fig
    sys_v, dia_v, dates = [], [], []
    for _, r in df.iterrows():
        try:
            s, d = map(int, str(r['blood_pressure']).split('/'))
            sys_v.append(s); dia_v.append(d); dates.append(r['date'])
        except: pass
    if not dates:
        ax.text(.5,.5,'No valid BP data',ha='center',va='center',color='#334155'); return fig
    ax.fill_between(dates, sys_v, dia_v, alpha=.08, color='#00e5ff')
    ax.plot(dates, sys_v, 'o-', color='#00e5ff', lw=2, ms=4.5, label='Systolic', zorder=3)
    ax.plot(dates, dia_v, 's--', color='#00ffa3', lw=1.6, ms=3.5, label='Diastolic', zorder=3)
    ax.legend(fontsize=8, facecolor='#0a1628', labelcolor='#94a3b8', edgecolor='#1a2744')
    plt.xticks(rotation=28, ha='right', fontsize=7)
    plt.tight_layout(pad=1.4); return fig

def chart_sugar(df):
    fig, ax = plt.subplots(figsize=(5.5, 2.85))
    dark_axes(fig, ax, '🩸  Sugar Level (mg/dL)')
    valid = df.dropna(subset=['sugar_level']) if not df.empty else df
    if valid.empty:
        ax.text(.5,.5,'No data yet',ha='center',va='center',color='#334155'); return fig
    ax.fill_between(valid['date'], valid['sugar_level'], alpha=.1, color='#b388ff')
    ax.plot(valid['date'], valid['sugar_level'], 'o-', color='#b388ff', lw=2, ms=4.5, zorder=3)
    ax.axhline(140, color='#ffb300', lw=1.2, ls='--', alpha=.65, label='High (140)')
    ax.axhline(70,  color='#00ffa3', lw=1.2, ls='--', alpha=.65, label='Low (70)')
    ax.legend(fontsize=8, facecolor='#0a1628', labelcolor='#94a3b8', edgecolor='#1a2744')
    plt.xticks(rotation=28, ha='right', fontsize=7)
    plt.tight_layout(pad=1.4); return fig

def chart_hr(df):
    fig, ax = plt.subplots(figsize=(5.5, 2.85))
    dark_axes(fig, ax, '❤️  Heart Rate (BPM)')
    valid = df.dropna(subset=['heart_rate']) if not df.empty else df
    if valid.empty:
        ax.text(.5,.5,'No data yet',ha='center',va='center',color='#334155'); return fig
    ax.axhspan(60, 100, alpha=.045, color='#00ffa3')
    ax.fill_between(valid['date'], valid['heart_rate'], alpha=.1, color='#ff4d8d')
    ax.plot(valid['date'], valid['heart_rate'], 'o-', color='#ff4d8d', lw=2, ms=4.5, zorder=3)
    ax.axhline(60,  color='#00ffa3', lw=1, ls='--', alpha=.45)
    ax.axhline(100, color='#00ffa3', lw=1, ls='--', alpha=.45, label='Normal zone')
    ax.legend(fontsize=8, facecolor='#0a1628', labelcolor='#94a3b8', edgecolor='#1a2744')
    plt.xticks(rotation=28, ha='right', fontsize=7)
    plt.tight_layout(pad=1.4); return fig

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:.5rem 1rem 1.25rem">
          <div style="display:flex;align-items:center;gap:.65rem;margin-bottom:.4rem">
            <div style="width:38px;height:38px;
                        background:linear-gradient(135deg,#00e5ff,#00ffa3);
                        border-radius:11px;display:flex;align-items:center;
                        justify-content:center;font-size:1.15rem;flex-shrink:0">💊</div>
            <div>
              <div style="font-weight:800;font-size:1.05rem;color:#f0f9ff;letter-spacing:-.01em">MedTrack</div>
              <div style="font-size:.65rem;color:#00e5ff;letter-spacing:.1em;font-weight:600">PRO</div>
            </div>
          </div>
          <div style="font-size:.76rem;color:#334155;padding-left:.2rem">Your health companion</div>
        </div>
        <div style="height:1px;background:rgba(255,255,255,.06);margin:.25rem 1rem .9rem"></div>
        <div style="font-size:.63rem;font-weight:700;letter-spacing:.14em;color:#1e3a5f;
                    text-transform:uppercase;padding:.2rem 1rem .45rem">Menu</div>
        """, unsafe_allow_html=True)

        nav = st.radio("", [
            "🏠  Home", "👤  Profile",
            "💊  Medicines", "🩺  Health Tracker", "📊  Dashboard",
        ], label_visibility="collapsed")

        profile = load_profile()
        if profile["name"]:
            st.markdown(f"""
            <div style="margin:1.25rem 1rem 0;padding:.85rem 1rem;
                        background:rgba(0,229,255,.05);
                        border:1px solid rgba(0,229,255,.12);
                        border-radius:14px">
              <div style="font-size:.63rem;color:#334155;margin-bottom:.3rem;letter-spacing:.08em">SIGNED IN</div>
              <div style="font-weight:600;color:#f0f9ff;font-size:.9rem">{profile['name']}</div>
              <div style="font-size:.72rem;color:#475569;margin-top:.15rem">{profile['age']} yrs · {profile['weight']} kg</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="position:absolute;bottom:1.5rem;left:0;right:0;
                    text-align:center;font-size:.65rem;color:#1a2744">
          © 2025 MedTrack Pro
        </div>""", unsafe_allow_html=True)
    return nav

# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
def page_home():
    profile = load_profile()
    name = profile["name"] if profile["name"] else "Friend"
    meds_df = get_medicines()
    health_df = get_health_records()
    today_str = date.today().strftime("%Y-%m-%d")
    today_h = health_df[health_df["date"] == today_str] if not health_df.empty else pd.DataFrame()

    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 18 else "Good Evening")

    st.markdown(f"""
    <div class="hero-banner">
      <div class="hero-eyebrow">● Live Dashboard</div>
      <div class="hero-title">{greeting},<br><em>{name}</em></div>
      <div class="hero-sub">Monitor your vitals, track medications, and stay ahead of your health — all from one intelligent dashboard.</div>
    </div>
    """, unsafe_allow_html=True)

    # Stat strip
    hr_v  = int(today_h["heart_rate"].iloc[0])   if not today_h.empty and today_h["heart_rate"].notna().any()  else None
    sg_v  = today_h["sugar_level"].iloc[0]        if not today_h.empty and today_h["sugar_level"].notna().any() else None
    bp_v  = today_h["blood_pressure"].iloc[0]     if not today_h.empty                                          else None

    hr_disp = f"{hr_v}" if hr_v else "—"
    sg_disp = f"{sg_v:.0f}" if sg_v else "—"
    bp_disp = str(bp_v) if bp_v else "—"

    st.markdown(f"""
    <div class="stat-strip">
      <div class="stat-tile sc">
        <span class="tile-icon">💊</span>
        <div class="tile-val">{len(meds_df)}</div>
        <div class="tile-label">Active Medicines</div>
      </div>
      <div class="stat-tile sr">
        <span class="tile-icon">❤️</span>
        <div class="tile-val">{hr_disp}<span style="font-size:.9rem;font-weight:400"> bpm</span></div>
        <div class="tile-label">Today's Heart Rate</div>
      </div>
      <div class="stat-tile sv">
        <span class="tile-icon">🩸</span>
        <div class="tile-val">{sg_disp}<span style="font-size:.85rem;font-weight:400"> mg/dL</span></div>
        <div class="tile-label">Today's Sugar</div>
      </div>
      <div class="stat-tile sm">
        <span class="tile-icon">🩺</span>
        <div class="tile-val" style="font-size:{'1.45rem' if bp_v else '1.9rem'}">{bp_disp}</div>
        <div class="tile-label">Blood Pressure</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.05, 1])

    with col1:
        st.markdown('<div class="s-eye">TODAY</div><div class="s-head">Medicine Schedule</div>', unsafe_allow_html=True)
        if meds_df.empty:
            st.info("No medicines yet — go to **Medicines** to add your first.")
        else:
            for _, row in meds_df.iterrows():
                st.markdown(f"""
                <div class="med-row">
                  <div style="display:flex;align-items:center;gap:.85rem">
                    <div style="width:38px;height:38px;background:rgba(0,229,255,.09);
                                border-radius:10px;display:flex;align-items:center;
                                justify-content:center;font-size:1rem;flex-shrink:0">💊</div>
                    <div>
                      <div class="med-name">{row['name']}</div>
                      <div class="med-sub">{row['dosage']}</div>
                    </div>
                  </div>
                  <span class="pill p-c">⏰ {row['time']}</span>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="s-eye">VITALS</div><div class="s-head">Today\'s Status</div>', unsafe_allow_html=True)
        if today_h.empty:
            st.info("No vitals today — visit **Health Tracker** to log.")
        else:
            r = today_h.iloc[0]
            # Analyse
            try:
                sv = int(str(r['blood_pressure']).split('/')[0])
                bp_info = ('o-g','✅ Normal','good') if sv<120 else (('o-w','⚠️ Elevated','warn') if sv<130 else ('o-b','❗ High','bad'))
            except:
                bp_info = ('o-w','— ?','warn')
            sg = float(r['sugar_level'] or 0)
            sg_info = ('o-g','✅ Normal','good') if sg<100 else (('o-w','⚠️ Pre-high','warn') if sg<140 else ('o-b','❗ High','bad'))
            hv = int(r['heart_rate'] or 0)
            hr_info = ('o-g','✅ Normal','good') if 60<=hv<=100 else (('o-w','⬇️ Low','warn') if hv<60 else ('o-b','❗ High','bad'))

            sc1, sc2, sc3 = st.columns(3)
            for col, icon, lbl, info in [(sc1,'🩺','Blood\nPressure',bp_info),(sc2,'🩸','Sugar\nLevel',sg_info),(sc3,'❤️','Heart\nRate',hr_info)]:
                status_color = {'good':'#00ffa3','warn':'#ffb300','bad':'#ff4d8d'}[info[2]]
                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align:center;padding:1.2rem .7rem">
                      <div class="orb {info[0]}">{icon}</div>
                      <div style="font-size:.76rem;color:#475569;font-weight:600;margin-bottom:.3rem">{lbl.replace(chr(10),' ')}</div>
                      <div style="font-size:.85rem;font-weight:700;color:{status_color}">{info[1]}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Tips
    st.markdown('<div class="dvd"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-eye">WELLNESS</div><div class="s-head">Daily Health Tips</div>', unsafe_allow_html=True)
    tips = [
        ("🥤","Stay Hydrated","8+ glasses of water daily keeps energy and focus sharp."),
        ("🚶","Move Daily","30 min of walking cuts cardiovascular risk significantly."),
        ("😴","Quality Sleep","7–9 hrs of rest naturally lowers blood pressure."),
        ("🥗","Eat Smart","Fill half your plate with veggies and whole grains."),
        ("🧘","Manage Stress","5 min of deep breathing lowers cortisol and heart rate."),
    ]
    cols = st.columns(5)
    for col, (ic, tt, td) in zip(cols, tips):
        with col:
            st.markdown(f"""
            <div class="tip-tile">
              <div class="ti">{ic}</div>
              <div class="tt">{tt}</div>
              <div class="td">{td}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: PROFILE
# ─────────────────────────────────────────────
def page_profile():
    st.markdown('<div class="s-eye">ACCOUNT</div><div class="s-head">User Profile</div>', unsafe_allow_html=True)
    profile = load_profile()
    with st.form("pf"):
        st.markdown('<div class="glass-card ac-cyan"><div class="card-title">📋 Personal Details</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: name   = st.text_input("Full Name",    value=profile["name"], placeholder="e.g. Alex Chen")
        with c2: age    = st.number_input("Age",         1, 120, int(profile["age"]))
        with c3: weight = st.number_input("Weight (kg)", 1.0, 300.0, float(profile["weight"]), .5)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.form_submit_button("💾 Save Profile"):
            if not name.strip(): st.error("Please enter your name.")
            else:
                save_profile(name.strip(), age, weight)
                st.success(f"✅ Profile saved for {name.strip()}!")

    if profile["name"]:
        bmi = profile['weight'] / (1.7 ** 2)
        bmi_label = "Underweight" if bmi<18.5 else ("Normal" if bmi<25 else ("Overweight" if bmi<30 else "Obese"))
        st.markdown(f"""
        <div class="glass-card ac-mint">
          <div class="card-title">Your Health Identity</div>
          <div style="display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap">
            <div style="width:68px;height:68px;
                        background:linear-gradient(135deg,rgba(0,229,255,.18),rgba(0,255,163,.18));
                        border-radius:50%;display:flex;align-items:center;justify-content:center;
                        font-size:1.7rem;border:2px solid rgba(0,229,255,.28);flex-shrink:0">👤</div>
            <div>
              <div style="font-size:1.35rem;font-weight:700;color:#f0f9ff;margin-bottom:.5rem">{profile['name']}</div>
              <div style="display:flex;gap:.5rem;flex-wrap:wrap">
                <span class="pill p-c">🎂 {profile['age']} yrs</span>
                <span class="pill p-m">⚖️ {profile['weight']} kg</span>
                <span class="pill p-v">📊 BMI {bmi:.1f} · {bmi_label}</span>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: MEDICINES
# ─────────────────────────────────────────────
def page_medicines():
    st.markdown('<div class="s-eye">MEDICATIONS</div><div class="s-head">Medicine Reminder</div>', unsafe_allow_html=True)
    with st.form("mf", clear_on_submit=True):
        st.markdown('<div class="glass-card ac-cyan"><div class="card-title">➕ Add New Medicine</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: mn = st.text_input("Medicine Name", placeholder="e.g. Metformin")
        with c2: ds = st.text_input("Dosage",        placeholder="e.g. 500 mg")
        with c3: tm = st.text_input("Time",           placeholder="e.g. 08:00 AM")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.form_submit_button("💊 Add Medicine"):
            if not all([mn.strip(), ds.strip(), tm.strip()]): st.error("Fill in all fields.")
            else:
                add_medicine(mn.strip(), ds.strip(), tm.strip())
                st.success(f"✅ {mn} added!")
                st.rerun()

    meds_df = get_medicines()
    st.markdown('<div class="dvd"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-eye">YOUR MEDICATIONS</div><div class="s-head">Medicine List</div>', unsafe_allow_html=True)

    if meds_df.empty:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem 2rem">
          <div style="font-size:3rem;margin-bottom:.75rem">💊</div>
          <div style="color:#94a3b8;font-size:.95rem">No medicines added yet</div>
        </div>""", unsafe_allow_html=True)
    else:
        for _, row in meds_df.iterrows():
            c1, c2 = st.columns([5.5, 1])
            with c1:
                st.markdown(f"""
                <div class="med-row">
                  <div style="display:flex;align-items:center;gap:.9rem">
                    <div style="width:40px;height:40px;background:rgba(0,229,255,.09);border-radius:10px;
                                display:flex;align-items:center;justify-content:center;font-size:1.05rem;flex-shrink:0">💊</div>
                    <div>
                      <div class="med-name">{row['name']}</div>
                      <div class="med-sub">Added {row['added_on']}</div>
                    </div>
                  </div>
                  <div style="display:flex;gap:.45rem;align-items:center">
                    <span class="pill p-a">📦 {row['dosage']}</span>
                    <span class="pill p-c">⏰ {row['time']}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"d{row['id']}", help="Delete"):
                    delete_medicine(row['id']); st.rerun()

# ─────────────────────────────────────────────
# PAGE: HEALTH TRACKER
# ─────────────────────────────────────────────
def page_health_tracker():
    st.markdown('<div class="s-eye">MONITORING</div><div class="s-head">Health Tracker</div>', unsafe_allow_html=True)

    with st.form("hf", clear_on_submit=True):
        st.markdown('<div class="glass-card ac-mint"><div class="card-title">📝 Log Vitals</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: rd = st.date_input("Date", value=date.today())
        with c2: bp = st.text_input("Blood Pressure", placeholder="120/80")
        with c3: sg = st.number_input("Sugar Level (mg/dL)", 0.0, 800.0, 100.0, 1.0)
        with c4: hr = st.number_input("Heart Rate (BPM)", 0, 250, 72, 1)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.form_submit_button("💾 Save Vitals"):
            if not bp.strip(): st.error("Enter blood pressure e.g. 120/80")
            else:
                try:
                    s, d = map(int, bp.strip().split('/'))
                    if not (0 < s < 300 and 0 < d < 200): raise ValueError
                    add_health_record(str(rd), bp.strip(), sg, int(hr))
                    st.success(f"✅ Vitals saved for {rd}!"); st.rerun()
                except ValueError:
                    st.error("Use Systolic/Diastolic format, e.g. 120/80")

    health_df = get_health_records()
    if health_df.empty: return

    st.markdown('<div class="dvd"></div>', unsafe_allow_html=True)
    latest = health_df.iloc[0]

    st.markdown('<div class="s-eye">ANALYSIS</div><div class="s-head">Latest Status</div>', unsafe_allow_html=True)

    try:
        sv = int(str(latest['blood_pressure']).split('/')[0])
        bp_info = ('o-g','✅ Normal','#00ffa3','p-m') if sv<120 else (('o-w','⚠️ Elevated','#ffb300','p-a') if sv<130 else ('o-b','❗ High','#ff4d8d','p-r'))
    except:
        bp_info = ('o-w','—','#ffb300','p-a')
    sg_v = float(latest['sugar_level'] or 0)
    sg_info = ('o-g','✅ Normal','#00ffa3','p-m') if sg_v<100 else (('o-w','⚠️ Pre-high','#ffb300','p-a') if sg_v<140 else ('o-b','❗ High','#ff4d8d','p-r'))
    hv = int(latest['heart_rate'] or 0)
    hr_info = ('o-g','✅ Normal','#00ffa3','p-m') if 60<=hv<=100 else (('o-w','⬇️ Low','#ffb300','p-a') if hv<60 else ('o-b','❗ High','#ff4d8d','p-r'))

    vc1, vc2, vc3 = st.columns(3)
    for col, icon, lbl, val, info in [
        (vc1,'🩺','Blood Pressure', latest['blood_pressure'], bp_info),
        (vc2,'🩸','Sugar Level',    f"{latest['sugar_level']} mg/dL", sg_info),
        (vc3,'❤️','Heart Rate',     f"{latest['heart_rate']} BPM", hr_info),
    ]:
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center">
              <div class="card-label">{lbl.upper()}</div>
              <div class="orb {info[0]}" style="margin:0 auto .8rem">{icon}</div>
              <div style="font-size:1.45rem;font-weight:800;color:#f0f9ff;margin-bottom:.55rem">{val}</div>
              <span class="pill {info[3]}">{info[1]}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="dvd"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-eye">HISTORY</div><div class="s-head">Recent Records</div>', unsafe_allow_html=True)
    disp = health_df[["date","blood_pressure","sugar_level","heart_rate"]].copy()
    disp.columns = ["Date","Blood Pressure","Sugar (mg/dL)","Heart Rate (BPM)"]
    st.dataframe(disp.head(10), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────
def page_dashboard():
    st.markdown('<div class="s-eye">ANALYTICS</div><div class="s-head">Health Dashboard</div>', unsafe_allow_html=True)
    health_df = get_health_records()
    if health_df.empty:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:4rem 2rem">
          <div style="font-size:3.5rem;margin-bottom:1rem">📊</div>
          <div style="color:#94a3b8;font-size:1.05rem">No records yet</div>
          <div style="color:#334155;font-size:.82rem;margin-top:.35rem">Start logging in <b>Health Tracker</b></div>
        </div>""", unsafe_allow_html=True)
        return

    chart_df = health_df.sort_values("date")
    avg_hr = health_df["heart_rate"].dropna().mean()
    avg_sg = health_df["sugar_level"].dropna().mean()
    max_hr = health_df["heart_rate"].dropna().max() if not health_df["heart_rate"].dropna().empty else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("📅 Total Records",  len(health_df))
    with m2: st.metric("❤️ Avg Heart Rate", f"{avg_hr:.0f} BPM" if not pd.isna(avg_hr) else "—")
    with m3: st.metric("🩸 Avg Sugar",      f"{avg_sg:.1f} mg/dL" if not pd.isna(avg_sg) else "—")
    with m4: st.metric("🩺 Latest BP",      health_df.iloc[0]["blood_pressure"] or "—")

    st.markdown('<div class="dvd"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-eye">TRENDS</div><div class="s-head">Vital Sign Charts</div>', unsafe_allow_html=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown('<div class="glass-card" style="padding:.85rem">', unsafe_allow_html=True)
        st.pyplot(chart_bp(chart_df))
        st.markdown('</div>', unsafe_allow_html=True)
    with cc2:
        st.markdown('<div class="glass-card" style="padding:.85rem">', unsafe_allow_html=True)
        st.pyplot(chart_sugar(chart_df))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cc3, cc4 = st.columns([2, 1])
    with cc3:
        st.markdown('<div class="glass-card" style="padding:.85rem">', unsafe_allow_html=True)
        st.pyplot(chart_hr(chart_df))
        st.markdown('</div>', unsafe_allow_html=True)
    with cc4:
        st.markdown(f"""
        <div class="glass-card ac-rose">
          <div class="card-label">HEART RATE SUMMARY</div>
          <div style="margin-top:1.1rem;display:flex;flex-direction:column;gap:1rem">
            <div>
              <div style="color:#334155;font-size:.72rem;margin-bottom:.2rem">Average</div>
              <div style="font-size:1.85rem;font-weight:800;color:#ff4d8d;line-height:1">{avg_hr:.0f}<span style="font-size:.9rem;font-weight:400;color:#94a3b8"> bpm</span></div>
            </div>
            <div style="height:1px;background:rgba(255,255,255,.05)"></div>
            <div>
              <div style="color:#334155;font-size:.72rem;margin-bottom:.2rem">Peak</div>
              <div style="font-size:1.5rem;font-weight:700;color:#f0f9ff;line-height:1">{max_hr:.0f}<span style="font-size:.82rem;font-weight:400;color:#94a3b8"> bpm</span></div>
            </div>
            <div style="height:1px;background:rgba(255,255,255,.05)"></div>
            <div>
              <div style="color:#334155;font-size:.72rem;margin-bottom:.45rem">Healthy Range</div>
              <span class="pill p-m">60 – 100 BPM</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="dvd"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-eye">DATA</div><div class="s-head">Full Health History</div>', unsafe_allow_html=True)
    disp = health_df[["date","blood_pressure","sugar_level","heart_rate"]].copy()
    disp.columns = ["Date","Blood Pressure","Sugar (mg/dL)","Heart Rate (BPM)"]
    st.dataframe(disp, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Export CSV", disp.to_csv(index=False).encode(), "health_records.csv", "text/csv")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    init_db()
    nav = sidebar()
    if   nav == "🏠  Home":            page_home()
    elif nav == "👤  Profile":         page_profile()
    elif nav == "💊  Medicines":       page_medicines()
    elif nav == "🩺  Health Tracker":  page_health_tracker()
    elif nav == "📊  Dashboard":       page_dashboard()

if __name__ == "__main__":
    main()
