import streamlit as st
from prompts import create_prompt
from templates import templates
from utils import generate_email, save_pdf
import pyperclip

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Email Writing Assistant",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI Email Writing Assistant")

# -------------------------
# SIDEBAR
# -------------------------
tone = st.sidebar.selectbox(
    "Select Tone",
    ["Professional", "Friendly", "Formal"]
)

purpose = st.sidebar.text_input("Purpose")
recipient = st.sidebar.text_input("Recipient")

# -------------------------
# TEMPLATE
# -------------------------
template = st.selectbox(
    "Templates",
    ["None"] + list(templates.keys())
)

details = ""

if template != "None":
    details = templates[template]

details = st.text_area(
    "Email Details",
    value=details,
    height=200
)

emoji = st.checkbox("😊 Add Emojis")

language = st.selectbox(
    "Translate To",
    ["None", "Hindi", "Kannada", "Tamil", "French", "German"]
)

# -------------------------
# GENERATE BUTTON
# -------------------------
generate = st.button(
    "✨ Generate Email",
    key="generate"
)

email = ""

if generate:

    prompt = create_prompt(
        tone,
        purpose,
        recipient,
        details
    )

    if emoji:
        prompt += "\nAdd suitable emojis."

    email = generate_email(prompt)

    st.session_state.email = email

# -------------------------
# DISPLAY EMAIL
# -------------------------
if "email" in st.session_state:

    email = st.session_state.email

    st.text_area(
        "Generated Email",
        value=email,
        height=350
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        rewrite = st.button(
            "🔄 Rewrite",
            key="rewrite"
        )

    with col2:
        shorten = st.button(
            "✂️ Shorten",
            key="shorten"
        )

    with col3:
        grammar = st.button(
            "📝 Improve Grammar",
            key="grammar"
        )

    translate = st.button(
        "🌐 Translate",
        key="translate"
    )

    copy = st.button(
        "📋 Copy Email",
        key="copy"
    )

    pdf = st.button(
        "📄 Create PDF",
        key="pdf"
    )

    if rewrite:
        new_prompt = f"Rewrite this email professionally:\n\n{email}"
        st.session_state.email = generate_email(new_prompt)
        st.rerun()

    if shorten:
        new_prompt = f"Shorten this email:\n\n{email}"
        st.session_state.email = generate_email(new_prompt)
        st.rerun()

    if grammar:
        new_prompt = f"Improve the grammar without changing the meaning:\n\n{email}"
        st.session_state.email = generate_email(new_prompt)
        st.rerun()

    if translate and language != "None":
        new_prompt = f"Translate this email into {language}:\n\n{email}"
        st.session_state.email = generate_email(new_prompt)
        st.rerun()

    if copy:
        try:
            pyperclip.copy(email)
            st.success("✅ Email copied successfully!")
        except Exception:
            st.warning("Copy failed. Please copy manually.")

    st.download_button(
        "⬇️ Download TXT",
        email,
        file_name="email.txt",
        mime="text/plain",
        key="txt_download"
    )

    if pdf:
        save_pdf(email)

    try:
        with open("email.pdf", "rb") as file:
            st.download_button(
                "📄 Download PDF",
                file,
                file_name="email.pdf",
                mime="application/pdf",
                key="pdf_download"
            )
    except FileNotFoundError:
        pass