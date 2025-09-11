import streamlit as st
from external_module import render_external_module

OHARA_TOKENLAB = "https://ohara.ai/mini-apps/13b468ca-644e-4736-b06f-2141861901ec?utm_source=learn3"

st.set_page_config(page_title="Learn3 — Token Lab", layout="wide")
render_external_module(
    OHARA_TOKENLAB,
    title="🪙 Token Lab",
    note="Simulasi pembuatan token — versi miniapp. Learn3 × RANTAI"
)
