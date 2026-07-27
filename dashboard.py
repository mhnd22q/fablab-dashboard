import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="FABLAB Machinery Dashboard", page_icon="🛠️", layout="wide")

NAVY = "#1B3A63"
ORANGE = "#F26B22"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .block-container {{ padding-top: 2rem; max-width: 1100px; }}
    .field-label {{
        color: {NAVY};
        font-weight: 600;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 2px;
    }}
    .field-value {{
        font-size: 15px;
        margin-bottom: 16px;
        color: #1a1a1a;
    }}
    hr {{ border-color: #E3E7EC; }}
    </style>
    """,
    unsafe_allow_html=True,
)

df = pd.read_csv("FABLAB_cleaned.csv")

# ---------- Header ----------
logo_l, title_c, logo_r = st.columns([1, 3, 1])
with logo_l:
    if os.path.exists("assets/sec_logo.png"):
        st.image("assets/sec_logo.png", width=110)
with title_c:
    st.markdown(
        f"<h1 style='text-align:center; color:{NAVY}; margin-bottom:0; font-weight:700; letter-spacing:0.01em;'>FABLAB Machinery Dashboard</h1>",
        unsafe_allow_html=True,
    )
with logo_r:
    if os.path.exists("assets/innovation_energy_logo.png"):
        st.image("assets/innovation_energy_logo.png", width=140)

st.markdown(f"<hr style='margin-top:1.2rem; margin-bottom:2rem; border-top:1px solid #E3E7EC;'>", unsafe_allow_html=True)

df["Display_Label"] = df["#"].astype(str) + " — " + df["Name"]

# ---------- Machine selector ----------
selected_label = st.selectbox("Select a machine:", df["Display_Label"])
machine = df[df["Display_Label"] == selected_label].iloc[0]

card = st.container(border=True)
col1, col2 = card.columns([1, 2])

with col1:
    image_path = str(machine["Image_File"])
    if os.path.exists(image_path):
        st.image(image_path, width=260)
    else:
        st.info("No image available")

with col2:
    st.markdown(f"<h2 style='color:{NAVY}; margin-top:0;'>{machine['Name']}</h2>", unsafe_allow_html=True)

    def field(label, value):
        st.markdown(
            f"<div class='field-label'>{label}</div><div class='field-value'>{value}</div>",
            unsafe_allow_html=True,
        )

    fcol1, fcol2 = st.columns(2)
    with fcol1:
        field("Machine Number", machine["#"])
        field("Model / Part Number", machine["Model/ Part Number"])
        field("Quantity", machine["Quantity"])
        field("Available Accessories", "Yes" if machine["Available Accessories"] else "No")
    with fcol2:
        field("General Features", machine["General Features"])
        field("Testing Main Items", machine["Testing Main Items"])
        field("Expected Testing Frequency / Year", machine["Expect Testing Frequency per Year"])

st.write("")

# ---------- User Manual summary ----------
with st.expander("📘 User Manual (Summary)", expanded=False):
    manual_text = machine.get("User_Manual", "")
    if pd.notna(manual_text) and str(manual_text).strip():
        st.write(manual_text)
    else:
        st.write("No manual summary added yet for this machine.")
    st.caption(
        "General operational summary — always follow the manufacturer's official manual for safety-critical steps."
    )

# ---------- Official PDF manual ----------
manual_path = machine.get("Manual_PDF", "")
if pd.notna(manual_path) and str(manual_path).strip() and os.path.exists(str(manual_path)):
    st.subheader("📄 Official User Manual")
    with open(manual_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="⬇️ Download User Manual (PDF)",
        data=pdf_bytes,
        file_name=os.path.basename(manual_path),
        mime="application/pdf",
    )
