import time
import requests
import datetime as dt
import pytz
import os
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe

import streamlit as st
import streamlit.components.v1 as components

# ==== ELPEEF Miniapps ====
ELPEEF_APPS = {
    "Blockchain 101": {
        "url": "https://blockchain101.elpeef.com/?utm_source=learn3",
        "title": "📖 Blockchain 101"
    },
    "Token Lab": {
        "url": "https://tokenlab.elpeef.com/?utm_source=learn3",
        "title": "🧪 Token Lab"
    },
    "DAO Sandbox": {
        "url": "https://daosandbox.elpeef.com/?utm_source=learn3",
        "title": "🗳 DAO Sandbox"
    },
    "DeFi Workshop": {
        "url": "https://defiworkshop.elpeef.com/?utm_source=learn3",
        "title": "💱 DeFi Workshop"
    },
    "Smart Contract Studio": {
        "url": "https://smartcontractstudio.elpeef.com/?utm_source=learn3",
        "title": "⚒️ Smart Contract Studio"
    },
    "Gas & Performance": {
        "url": "https://gasperformance.elpeef.com/?utm_source=learn3",
        "title": "⚡ Gas & Performance"
    },
    "Audit Security": {
        "url": "https://auditsecurity.elpeef.com/?utm_source=learn3",
        "title": "🔐 Audit Security"
    },
    "Web3 Lab": {
        "url": "https://web3lab.elpeef.com/?utm_source=learn3",
        "title": "🔗 Web3 Lab"
    },
    "Certification": {
        "url": "https://certlearn3.elpeef.com/?utm_source=learn3",
        "title": "🎓 Certification"
    }
}

import streamlit as st
import streamlit.components.v1 as components

def iframe_with_mobile_notice(content_html, height):
    style = """
    <style>
      @media (max-width: 768px) {
          .hide-on-mobile { display:none!important; }
          .show-on-mobile {
              display:block!important;
              padding:24px 12px;
              background:#ffecec;
              color:#d10000;
              font-weight:bold;
              text-align:center;
              border-radius:12px;
              font-size:1.2em;
              margin-top:24px;
          }
      }
      @media (min-width: 769px) {
          .show-on-mobile { display:none!important; }
      }
    </style>
    """
    notice = '''
      <div class="show-on-mobile">
        📱 Tampilan ini tidak tersedia di perangkat seluler.<br>
        Silakan buka lewat laptop atau desktop untuk pengalaman penuh 💻
      </div>
    '''
    components.html(
        style +
        f'<div class="hide-on-mobile">{content_html}</div>' +
        notice,
        height=height
    )

def iframe(src, height=720, width="100%", hide_top=0, hide_bottom=0, title=None):
    if title:
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
    iframe_height = height + hide_top + hide_bottom
    top_offset = -hide_top
    content_html = f'''
        <div style="height:{height}px; overflow:hidden; position:relative;">
            <iframe src="{src}" width="{width}" height="{iframe_height}px"
                    frameborder="0"
                    style="position:relative; top:{top_offset}px;">
            </iframe>
        </div>
    '''
    iframe_with_mobile_notice(content_html, height)

def embed_lab(url, title="", hide_top=72, hide_bottom=0, height=720):
    if title:
        st.markdown(f"### {title}", unsafe_allow_html=True)
    iframe_height = height + hide_top + hide_bottom
    top_offset = -hide_top
    content_html = f'''
      <div style="position:relative;width:100%;height:{height}px;overflow:hidden;border-radius:12px;">
        <div id="loader"
            style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
                    font-weight:600;opacity:.6;transition:opacity .3s ease">
          Loading module…
        </div>
        <iframe id="ELPEEF" src="{url}"
          style="position:absolute; top:{top_offset}px; left:0;
                 width:100%; height:{iframe_height}px;
                 border:0; border-radius:12px; overflow:hidden"></iframe>
      </div>
      <script>
        const ifr = document.getElementById('ELPEEF');
        ifr.addEventListener('load', () => {{
          const l = document.getElementById('loader');
          if (l) {{
            l.style.opacity = 0;
            setTimeout(() => l.style.display = 'none', 300);
          }}
        }});
      </script>
    '''
    iframe_with_mobile_notice(content_html, height)

if st.query_params.get("ping") == "1":
    st.write("ok"); st.stop()

# Quick CSS theme (dark + teal accents)
st.markdown("""
<style>
:root { --accent:#20c997; --accent2:#7c4dff; }
.block-container { padding-top: 1rem; }
section[data-testid="stSidebar"] .st-expander { border:1px solid #313131; border-radius:12px; }
div[data-testid="stMetric"]{
  background: linear-gradient(135deg, rgba(32,201,151,.08), rgba(124,77,255,.06));
  border: 1px solid rgba(128,128,128,.15);
  padding: 12px; border-radius: 12px;
}
.stButton>button, .stDownloadButton>button{
  border-radius:10px; border:1px solid rgba(255,255,255,.15);
}
.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"]{
  background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.08);
  border-radius: 10px; padding: 6px 12px;
}
[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.image(
        "https://i.imgur.com/E5LaGaa.png",
        use_container_width=True
    )
    st.sidebar.markdown("📘 **About**")
    st.sidebar.markdown("""
    Learn3 adalah platform edukasi Web3 interaktif yang dikemas seperti game petualangan. Memadukan AI bot dan mentor, gamifikasi, serta real-world tools dari ekosistem blockchain.
    Kami percaya belajar Web3 bukan sekadar membaca teori, tapi perjalanan interaktif:

    - mulai dari dasar,
    
    - naik level lewat simulasi,
    
    - eksplorasi frontier research,
    
    - dan menutup perjalanan dengan reward on-chain sebagai bukti pencapaian.

    Showcase dan dokumentasi ada disini [Doc](https://learn3showcase.vercel.app)
    
    ---
    #### 🔮 Vision Statement
    User belajar lewat chatbot AI, latihan simulasi DeFi & DAO, eksperimen smart contract, hingga riset cutting-edge seperti zkML.
    Setiap langkah terhubung dengan ekosistem STC (GasVision, Bench, Converter, Analytics) untuk pengalaman nyata.
    Di akhir perjalanan, user mendapatkan sertifikat Soul Bound Token (SBT) eksklusif — bukti abadi di blockchain bahwa mereka adalah bagian dari pionir Web3.

    ---
    ### ❓ How to Get the Badges
    Terdapat 10 Badge di seluruh modul yang tersebar untuk didapatkan. Jelajahi modul per modul untuk mencarinya. Kumpulkan minimal 6 Badge maka kamu berhak untuk claim sertifikat 🎓
    
    ---
    ### 🎯 Quiz Leaderboard
    Quiz disini hanya bersifat simulasi dan latihan. 
    Klik [join](https://wayground.com/join?gc=53764642) agar kamu bisa simpan progress, isi nama dan avatar sendiri, serta bandingkan peringkatmu dengan peserta lainnya. 
    Untuk mengeklaim Badge, sebaiknya masukkan nama asli disertai dengan email yang valid saaat mengisi nama peserta quiz.

    ---
    ### 🧩 Apps Showcase
    Lihat disini untuk semua tools yang kami kembangkan:
    [ELPEEF](https://showcase.elpeef.com/)

    ---
    #### 🙌 Dukungan & kontributor
    - ⭐ **Star / Fork**: [GitHub repo](https://github.com/mrbrightsides/learn3)
    - Built with 💙 by [Khudri](https://s.id/khudri)
    - Dukung pengembangan proyek ini melalui: 
      [💖 GitHub Sponsors](https://github.com/sponsors/mrbrightsides) • 
      [☕ Ko-fi](https://ko-fi.com/khudri) • 
      [💵 PayPal](https://www.paypal.com/paypalme/akhmadkhudri) • 
      [🍵 Trakteer](https://trakteer.id/akhmad_khudri)

    Versi UI: v1.0 • Streamlit • Theme Dark
    """)

# ===== Page setup =====
st.set_page_config(
    page_title="Learn3",
    page_icon="🌐",
    layout="wide"
)

col1, col2 = st.columns([2, 2])
with col1:
    st.markdown("""
        # Learn Web3 with Learn3 🌐
    """)
with col2:
    st.markdown("""
        ## Chat. Code. Chained. Certified — Your Web3 Journey Starts Here
    """)
st.markdown("""
        > 💡 Untuk tampilan dan pengalaman belajar yang optimal, disarankan menggunakan browser pada laptop atau PC untuk mengakses Learn3
    """)

# ===== Tab utama =====
tabs = st.tabs([
    "🤖 AI Playground", 
    "📖 Blockchain 101",
    "🧪 Token Lab",
    "🗳 DAO Sandbox",
    "💱 DeFi Workshop",
    "⚒️ Smart Contract Studio",
    "⚡ Gas & Performance",
    "🔐 Audit Security",
    "🔗 Web3 Lab",
    "🎓 Certification"
])

# ===== Tab: Chatbot =====
with tabs[0]:
    st.subheader("🤖 Chatbot AI-powered Playground")
    st.markdown("""
        Tanya jawab interaktif tentang blockchain, smart contract, dan Web3. Pilih sesuai kebutuhan kamu.
    """)
    st.markdown("""
        Belajar dasar (Bot + Chat + Tutor) → Latihan (Simulators) → Quiz → Eksplorasi lanjut (Research) → Bebas tanya (AI Gateway).
    """)
    
    # --- Persist pilihan widget
    if "chat_widget" not in st.session_state:
        st.session_state.chat_widget = "BlockTutor"  # default
    
    widget_opt = st.radio(
        " ",
        ["BlockBot","BlockChat","BlockTutor","DAO Voter Simulator","LP Simulator","Quiz","Research","AI Gateway"],
        horizontal=True, label_visibility="collapsed",
        index=["BlockBot","BlockChat","BlockTutor","DAO Voter Simulator","LP Simulator","Quiz","Research","AI Gateway"].index(st.session_state.chat_widget),
        key="chat_widget"
    )
    
    URLS = {
        "BlockBot": "https://my.artibot.ai/learn3bot",
        "BlockChat": "https://bot.writesonic.com/share/bot/a148b878-259e-4591-858a-8869b9b23604",
        "BlockTutor": "https://www.chatbase.co/chatbot-iframe/RIURX1Atx537tDeYNcw8R",
        "DAO Voter Simulator": "https://tawk.to/chat/68ba6085721af15d8752fbc5/1j4c0i358",
        "LP Simulator": "https://denser.ai/u/embed/chatbot_o90yjz0cba1ymfmzi2nwr",
        "Quiz": "https://wayground.com/embed/quiz/68bb727d3fa528df7533c75e",
        "Research": "https://zenoembed.textcortex.com/?embed_id=emb_01k4cfh76fehtte5jgmy3atz69",
        "AI Gateway": "https://learn3ai.vercel.app/"
    }
    chosen_url = URLS[widget_opt]
    
    cache_bust = st.toggle("Force refresh chat (cache-bust)", value=False)
    final_url = f"{chosen_url}?t={int(time.time())}" if cache_bust else chosen_url
    
    st.write(f"💬 Chat aktif: **{widget_opt}**")
    st.caption("Jika area kosong, kemungkinan dibatasi oleh CSP/X-Frame-Options dari penyedia.")
    
    if widget_opt == "BlockChat":
        # Botsonic: sembunyikan header atas dengan crop ~56px (atur sesuai kebutuhan)
        embed_cropped(final_url, hide_px=50, height=720, title=None)
    else:
        # Widget lain tetap pakai iframe standar
        iframe(src=final_url, height=720)
    
    if st.button(f"🔗 Klik disini jika ingin menampilkan halaman chat {widget_opt} dengan lebih baik"):
        st.markdown(f"""<meta http-equiv="refresh" content="0; url={chosen_url}">""", unsafe_allow_html=True)

# === Tab 1: Blockchain 101 (iframe ke ELPEEF) ===
with tabs[1]:
    app = ELPEEF_APPS["Blockchain 101"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)
    
# === Tab 2: Token Lab (iframe ke ELPEEF) ===
with tabs[2]:
    app = ELPEEF_APPS["Token Lab"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)

# === Tab 3: DAO Sandbox (iframe ke ELPEEF) ===
with tabs[3]:
    app = ELPEEF_APPS["DAO Sandbox"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)
    
# === Tab 4: DeFi Workshop (iframe ke ELPEEF) ===
with tabs[4]:
    app = ELPEEF_APPS["DeFi Workshop"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)

# === Tab 5: Smart Contract Studio (iframe ke ELPEEF) ===
with tabs[5]:
    app = ELPEEF_APPS["Smart Contract Studio"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)
    
# === Tab 6: Gas & Performance (iframe ke ELPEEF) ===
with tabs[6]:
    app = ELPEEF_APPS["Gas & Performance"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)
    
# === Tab 7: Audit Security (iframe ke ELPEEF) ===
with tabs[7]:
    app = ELPEEF_APPS["Audit Security"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)

# === Tab 8: Web3 Lab (iframe ke ELPEEF) ===
with tabs[8]:
    app = ELPEEF_APPS["Web3 Lab"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)

# === Tab 9: Certification (iframe ke ELPEEF) ===
with tabs[9]:
    app = ELPEEF_APPS["Certification"]
    embed_lab(app["url"], app["title"], hide_top=0, hide_bottom = -5)
