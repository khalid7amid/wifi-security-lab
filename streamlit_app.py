
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Wi-Fi 6 Security Lab – Extended", layout="wide")
st.title("📶 Wi-Fi 6 Security Lab – Extended Version")
st.markdown("## 📡 Upload your PCAP and answer all questions manually")

uploaded_file = st.file_uploader("📤 Upload your PCAP file", type=["pcap"])

st.markdown("---")
st.markdown("### 📝 Step 2: Fill in your details and answer the questions")

with st.form("lab_form_wifi6_ext"):
    student_name = st.text_input("👤 Full Name")
    student_id = st.text_input("🆔 University ID")

    # Original questions (10)
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

    # 12 new questions focused on Wi-Fi 6
    q11 = st.radio("11️⃣ Is BSS Coloring used in the capture?", ["", "Yes", "No"], index=0)
    q12 = st.radio("12️⃣ Are Target Wake Time (TWT) features visible?", ["", "Yes", "No"], index=0)
    q13 = st.radio("13️⃣ Is OFDMA detected in the packet structure?", ["", "Yes", "No"], index=0)
    q14 = st.radio("14️⃣ Are 1024-QAM frames used?", ["", "Yes", "No"], index=0)
    q15 = st.radio("15️⃣ Are any MU-MIMO transmission indicators present?", ["", "Yes", "No"], index=0)
    q16 = st.radio("16️⃣ Do you observe Enhanced Open (OWE) security?", ["", "Yes", "No"], index=0)
    q17 = st.radio("17️⃣ Do you observe WPA3-SAE authentication?", ["", "Yes", "No"], index=0)
    q18 = st.radio("18️⃣ Are Protected Management Frames (PMF) enforced?", ["", "Yes", "No"], index=0)
    q19 = st.radio("19️⃣ Are any 6 GHz band frames captured?", ["", "Yes", "No"], index=0)
    q20 = st.radio("20️⃣ Is there any evidence of MAC Randomization?", ["", "Yes", "No"], index=0)
    q21 = st.radio("21️⃣ Is the access point advertising 802.11ax (Wi-Fi 6)?", ["", "Yes", "No"], index=0)
    q22 = st.text_area("22️⃣ What is your overall impression of the Wi-Fi 6 security posture of this network?")

    submitted = st.form_submit_button("📤 Submit")

    if submitted:
        if not student_name.strip() or not student_id.strip():
            st.warning("Please enter your full name and university ID.")
        else:
            row = [
                datetime.now().isoformat(),
                student_name,
                student_id,
                q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
                q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22
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
