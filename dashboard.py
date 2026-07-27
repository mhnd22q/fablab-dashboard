import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="FABLAB Machinery Dashboard", page_icon="🛠️", layout="wide")

NAVY = "#1B3A63"
ORANGE = "#F26B22"
LIGHT_BG = "#F4F6F9"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {LIGHT_BG}; }}
    div[data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid #E3E7EC;
        border-left: 4px solid {ORANGE};
        border-radius: 10px;
        padding: 14px 18px;
    }}
    .machine-card {{
        background-color: white;
        border-radius: 12px;
        padding: 20px 24px;
        border: 1px solid #E3E7EC;
    }}
    .field-label {{
        color: {NAVY};
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 2px;
    }}
    .field-value {{
        font-size: 15px;
        margin-bottom: 14px;
        color: #222;
    }}
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
        f"<h1 style='text-align:center; color:{NAVY}; margin-bottom:0;'>FABLAB Machinery Dashboard</h1>"
        f"<p style='text-align:center; color:#666; margin-top:4px;'>Innovation Division — Equipment & Documentation Hub</p>",
        unsafe_allow_html=True,
    )
with logo_r:
    if os.path.exists("assets/innovation_energy_logo.png"):
        st.image("assets/innovation_energy_logo.png", width=140)

st.divider()

# ---------- KPI row ----------
total_machines = len(df)
with_manual = df["Manual_PDF"].apply(lambda p: isinstance(p, str) and p.strip() != "").sum()
unique_models = df["Name"].nunique()

k1, k2, k3 = st.columns(3)
k1.metric("Total Machines", total_machines)
k2.metric("Manuals Available", f"{with_manual} / {total_machines}")
k3.metric("Distinct Machine Types", unique_models)

st.write("")

# ---------- Machine selector ----------
selected_name = st.selectbox("Select a machine:", df["Name"])
machine = df[df["Name"] == selected_name].iloc[0]

st.markdown(f"<div class='machine-card'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

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

st.markdown("</div>", unsafe_allow_html=True)

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
st.subheader("📄 Official User Manual")

manual_path = machine.get("Manual_PDF", "")
if pd.notna(manual_path) and str(manual_path).strip() and os.path.exists(str(manual_path)):
    with open(manual_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="⬇️ Download User Manual (PDF)",
        data=pdf_bytes,
        file_name=os.path.basename(manual_path),
        mime="application/pdf",
    )

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = (
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
        f'width="100%" height="600" type="application/pdf"></iframe>'
    )
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.info(
        "No PDF manual uploaded yet for this machine. Add the file under manuals/ "
        "and set its path in the 'Manual_PDF' column of FABLAB_cleaned.csv."
    )

st.divider()
st.caption("FABLAB — Innovation Division · Saudi Electricity Company")
