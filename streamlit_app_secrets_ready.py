
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Wi-Fi Security Lab – Google Sheets", layout="wide")
st.title("🔐 Wi-Fi Security Analysis Lab – Google Sheets Edition")
st.markdown("## 📡 Upload your PCAP and answer all questions manually")

uploaded_file = st.file_uploader("📤 Upload your PCAP file", type=["pcap"])

st.markdown("---")
st.markdown("### 📝 Step 2: Fill in your details and answer the questions")

with st.form("lab_form_sheets"):
    student_name = st.text_input("👤 Full Name")
    student_id = st.text_input("🆔 University ID")

    q1 = st.number_input("1️⃣ How many EAPOL packets?", min_value=0, step=1)
    q2 = st.selectbox("2️⃣ Security protocol?", ["", "WEP", "WPA2", "WPA3"], index=0)
    q3 = st.text_input("3️⃣ MAC of Access Point?")
    q4 = st.text_input("4️⃣ MAC of Client?")
    q5 = st.radio("5️⃣ Is PMKID present?", ["", "Yes", "No"], index=0)
    q6 = st.selectbox("6️⃣ Likely attack type?", ["", "PMKID attack", "Dictionary attack", "Evil Twin", "None"], index=0)
    q7 = st.text_area("7️⃣ Suggest a protection method for this attack.")
    q8 = st.radio("8️⃣ Was the 4-way handshake complete?", ["", "Yes", "No"], index=0)
    q9 = st.text_area("9️⃣ What is the role of EAPOL in Wi-Fi authentication?")
    q10 = st.radio("🔟 Are there any Deauthentication packets?", ["", "Yes", "No"], index=0)

    submitted = st.form_submit_button("📤 Submit")

    if submitted:
        if not student_name.strip() or not student_id.strip():
            st.warning("Please enter your full name and university ID.")
        else:
            row = [
                datetime.now().isoformat(),
                student_name,
                student_id,
                q1, q2, q3, q4, q5, q6, q7, q8, q9, q10
            ]

            try:
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                service_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
                creds = ServiceAccountCredentials.from_service_account_info(service_info, scope)
                client = gspread.authorize(creds)
                sheet = client.open("WiFi Lab Responses").sheet1
                sheet.append_row(row)
                st.success("✅ Your response has been submitted to Google Sheets!")
            except Exception as e:
                st.error(f"❌ Failed to submit to Google Sheets: {e}")
