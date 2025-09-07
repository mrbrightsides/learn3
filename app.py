import time
import requests
import datetime as dt
import pytz
import os
import pandas as pd
import streamlit as st
from streamlit.components.v1 import iframe

if st.query_params.get("ping") == "1":
    st.write("ok"); st.stop()

# ===== Komponen: Waktu Sholat =====
from components.waktu_sholat import (
    TZ, METHODS, fetch_timings_by_city, parse_today_times,
    to_local_datetime, next_prayer, fmt_delta
)

# ===== Komponen: Quran =====
from components.quran import render_quran_tab

# ===== Komponen: Zakat =====
from components.zakat import (
    zakat_kalkulator, OZT_TO_GRAM,
    fetch_gold_price_idr_per_gram, format_rp, nisab_emas_idr
)

# ===== Komponen: Masjid Terdekat =====
from components.masjid import (
    show_nearby_mosques
)

# ===== Komponen: Murottal =====
from components.murottal import (
    RADIO_API, fetch_radios, show_murottal_tab
)

# ===== Komponen: Khutbah GPT =====
from components.khutbah_gpt import (
    render_khutbah_form, generate_khutbah, generate_khutbah_gpt
)

# ===== Komponen: Live TV =====
from components.live_tv import render_live_tv_tab

# ===== Komponen: Chat Ustadz =====
from components.chat_ustadz import show_chat_ustadz_tab

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
    st.sidebar.markdown("📘 **About**")
    st.sidebar.markdown("""
    Learn3 adalah platform edukasi Web3 interaktif yang dikemas seperti game petualangan. Memadukan AI bot dan mentor, gamifikasi, serta real-world tools dari ekosistem blockchain.
    Kami percaya belajar Web3 bukan sekadar membaca teori, tapi perjalanan interaktif:

    - mulai dari dasar,
    
    - naik level lewat simulasi,
    
    - eksplorasi frontier research,
    
    - dan menutup perjalanan dengan reward on-chain sebagai bukti pencapaian.""")

    ---
    st.sidebar.markdown("📘 **Vision Statement**")
    st.sidebar.markdown("""
    User belajar lewat chatbot AI, latihan simulasi DeFi & DAO, eksperimen smart contract, hingga riset cutting-edge seperti zkML.
    Setiap langkah terhubung dengan ekosistem STC (GasVision, Bench, Converter, Analytics) untuk pengalaman nyata.
    Di akhir perjalanan, user mendapatkan sertifikat NFT/SBT eksklusif — bukti abadi di blockchain bahwa mereka adalah bagian dari pionir Web3.""")
    
    ---
    st.sidebar.markdown("📘 **How to Get the Badges**")
    st.sidebar.markdown("""
    Terdapat 10 Badge di seluruh modul yang ada untuk didapatkan. Jelajahi modul per modul untuk mencarinya. Kumpulkan minimal 6 Badge maka kamu berhak untuk claim sertifikat 🎓
    
    ---
    #### 🙌 Dukungan & kontributor
    - ⭐ **Star / Fork**: [GitHub repo](https://github.com/mrbrightsides/learn3)
    - Built with 💙 by [Khudri](https://khudri.elpeef.com)

    Versi UI: v1.0 • Streamlit • Theme Dark
    """)

# ===== Page setup =====
st.set_page_config(
    page_title="Learn3",
    page_icon="🚀",
    layout="wide"
)

col1, col2 = st.columns([2, 2])
with col1:
    st.markdown("""
        # Learn Web3 with Learn3 🌍
    """)
with col2:
    st.markdown("""
        ## Chat. Code. Chained. Certified — Your Web3 Journey Starts Here
    """)

st.caption(" >💡 Belajar Web3 gak harus kaku. Di Learn3, kamu bisa ngobrol sama bot, main quiz, latihan simulasi DeFi & DAO, sampai bikin smart contract sendiri. Fun kayak nongkrong, serius di hasilnya, dan reward-nya on-chain 🚀")

# ===== Tab utama =====
tabs = st.tabs([
    "🤖 Chatbot", 
    "📖 Blockchain 101",
    "🎨 Token & NFT Lab",
    "🗳 DAO Playground",
    "💱 DeFi Workshop",
    "⚒️ Smart Contract Studio",
    "⚡ Gas & Performance",
    "🔐 Security & Audit",
    "🔗 AI × Web3 Lab",
    "🎓 NFT/SBT Certification"
])

# ===== Tab: Chatbot =====
with tabs[0]:
    st.subheader("🤖 Chatbot AI powered Mentor")
    st.markdown("""
        Tanya jawab interaktif tentang blockchain, smart contract, dan Web3. Pilih sesuai kebutuhan kamu.
    """)
    st.markdown("""
        Belajar dasar (Bot + Chat + Tutor) → Latihan (Simulators) → Quiz → Eksplorasi lanjut (Research) → Bebas tanya (AI Gateway).
    """)
    
    # --- Persist pilihan widget
    if "chat_widget" not in st.session_state:
        st.session_state.chat_widget = "BlockBot"  # default

    widget_opt = st.radio(
        " ", ["BlockBot", "BlockChat", "BlockTutor", "DAO Voter Simulator", "LP Simulator", "Quiz", "Research", "AI Gateway"],
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
        "Quiz": "https://wayground.com/embed/quiz/68bb6d5c1ca00a9af41b931c",
        "Research": "https://zenoembed.textcortex.com/?embed_id=emb_01k4cfh76fehtte5jgmy3atz69",
        "AI Gateway": "https://learn3ai.vercel.app/"
    }
    chosen_url = URLS[widget_opt]

    cache_bust = st.toggle("Force refresh chat (cache-bust)", value=False)
    final_url = f"{chosen_url}?t={int(time.time())}" if cache_bust else chosen_url

    st.write(f"💬 Chat aktif: **{widget_opt}**")
    st.caption("Jika area kosong, kemungkinan dibatasi oleh CSP/X-Frame-Options dari penyedia.")

    iframe(src=final_url, height=720)

    if st.button(f"🔗 Klik disini jika ingin menampilkan halaman chat {widget_opt} dengan lebih baik"):
        st.markdown(
            f"""
            <meta http-equiv="refresh" content="0; url={chosen_url}">
            """,
            unsafe_allow_html=True
        )

# === Tab 1: Waktu Sholat ===
with tabs[1]:
    st.subheader("🕌 Waktu Sholat Harian")
    try:
        city = st.text_input("Kota", value="Palembang")
        country = st.text_input("Negara", value="Indonesia")
        method_name = st.selectbox("Metode perhitungan", list(METHODS.keys()), index=1)
        method = METHODS[method_name]

        payload = fetch_timings_by_city(city, country, method)
        date_readable = payload["date"]["readable"]
        timings = parse_today_times(payload["timings"])

        times_local = {
            n: to_local_datetime(date_readable, t.split(" ")[0])
            for n, t in timings.items()
        }

        st.write(f"📅 **{date_readable}** — Zona: **{TZ.zone}** — Metode: **{method_name}**")
        rows = [(n, timings[n]) for n in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"] if n in timings]
        st.dataframe(pd.DataFrame(rows, columns=["Sholat", "Waktu"]), hide_index=True, use_container_width=True)

        now = dt.datetime.now(TZ)
        name, tnext = next_prayer(now, times_local)
        if name:
            st.success(f"Sholat berikutnya: **{name}** — **{tnext.strftime('%H:%M')}** (≈ {fmt_delta(tnext - now)})")
            st.caption("Hitung mundur diperbarui saat halaman di-run ulang.")
        else:
            st.info("Semua waktu sholat hari ini sudah lewat.")
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")

# === Tab 2: Murottal ===
with tabs[2]:
    show_murottal_tab()

# === Tab 3: Quran ===
with tabs[3]:
    render_quran_tab()

# === Tab 4: Kalkulator Zakat ===
with tabs[4]:
    zakat_kalkulator()

# === Tab 5: Masjid Terdekat ===
with tabs[5]:
    show_nearby_mosques()

# === Tab 6: Event Islam ===
with tabs[6]:
    try:
        from components.event import render_event
        render_event()
    except Exception as e:
        st.warning(f"Gagal memuat kalender lengkap: {e}. Menampilkan kalender sederhana.")
        from components.event import render_simple_hijri_calendar
        render_simple_hijri_calendar()

# === Tab 7: KhutbahGPT ===
with tabs[7]:
    render_khutbah_form()

# === Tab 8: Live TV ===
with tabs[8]:
    render_live_tv_tab()

# === Tab 9: Chat Ustadz ===
with tabs[9]:
    show_chat_ustadz_tab()
