
import streamlit as st
import re

st.set_page_config(
    page_title="ScamLens AI",
    page_icon="🚨",
    layout="centered"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #102A43;
}
.subtitle {
    text-align: center;
    font-size: 19px;
    color: #667085;
    margin-bottom: 30px;
}
.scam-box, .warning-box, .safe-box {
    color: white;
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    margin-top: 20px;
}
.scam-box {
    background: linear-gradient(135deg, #ff0000, #ff1744);
}
.warning-box {
    background: linear-gradient(135deg, #ff9800, #ffb300);
}
.safe-box {
    background: linear-gradient(135deg, #00a86b, #16c784);
}
.scam-title {
    font-size: 30px;
    font-weight: 900;
}
.scam-score {
    font-size: 21px;
    font-weight: 600;
}
.popup-title {
    color: red;
    font-size: 28px;
    font-weight: 900;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="title">🔍 ScamLens AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Based Intelligent Scam Detection and Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Enter a suspicious message, email, URL or website "
    "content and let ScamLens AI analyze it."
)

# ==========================================
# DETECTION LOGIC
# ==========================================

scam_keywords = [
    "urgent", "immediately", "otp", "password",
    "account blocked", "verify your account",
    "click here", "claim your prize", "won a prize",
    "bank details", "send money", "transfer money",
    "limited time", "act now", "suspended",
    "kyc update", "lottery", "free gift",
    "pin number", "credit card", "debit card",
    "processing fee", "account will be closed",
    "http://", "bit.ly", "wire transfer"
]

safe_keywords = [
    "meeting scheduled", "class starts",
    "assignment submission", "thank you",
    "see you tomorrow", "lecture notes",
    "project discussion", "team meeting",
    "happy birthday", "good morning"
]

# ==========================================
# USER INPUT
# ==========================================

user_input = st.text_area(
    "🔎 Enter suspicious content",
    height=180,
    placeholder=(
        "Example: URGENT! Your bank account has been "
        "blocked. Click here to verify your OTP immediately."
    )
)

# ==========================================
# ANALYZE
# ==========================================

if st.button("🚨 ANALYZE WITH SCAMLENS AI",
             use_container_width=True):

    if not user_input.strip():
        st.warning("Please enter a message first.")

    else:
        text = user_input.lower()

        scam_matches = [
            word for word in scam_keywords
            if word in text
        ]

        safe_matches = [
            word for word in safe_keywords
            if word in text
        ]

        # Simple rule-based demo score.
        # This is NOT the trained ML model's confidence.
        score = min(45 + len(scam_matches) * 12, 99)

        if scam_matches:
            if score >= 60:
                risk = "HIGH RISK"
            else:
                risk = "SUSPICIOUS"
        elif safe_matches:
            risk = "SAFE"
            score = 90
        else:
            risk = "SUSPICIOUS"
            score = 50

        scam_percentage = score if risk != "SAFE" else 10
        safe_percentage = 100 - scam_percentage

        st.session_state["risk"] = risk
        st.session_state["scam_percentage"] = scam_percentage

        st.subheader("🔎 AI Analysis Result")

        if risk == "HIGH RISK":
            st.markdown(f"""
            <div class="scam-box">
                <div class="scam-title">🚨 SCAM DETECTED</div>
                <br>
                <div class="scam-score">HIGH RISK</div>
                <br>
                <div class="scam-score">
                    Risk Indicator: {scam_percentage}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif risk == "SUSPICIOUS":
            st.markdown(f"""
            <div class="warning-box">
                <div class="scam-title">⚠️ SUSPICIOUS</div>
                <br>
                <div class="scam-score">
                    Risk Indicator: {scam_percentage}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class="safe-box">
                <div class="scam-title">✅ SAFE</div>
                <br>
                <div class="scam-score">
                    Safety Indicator: {safe_percentage}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("### 📊 Message Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🚨 Scam Indicator", f"{scam_percentage}%")

        with col2:
            st.metric("✅ Safe Indicator", f"{safe_percentage}%")

        st.write("### 🧠 Analysis Explanation")

        if scam_matches:
            st.write(
                "Potential warning phrases detected: "
                + ", ".join(scam_matches)
            )

        if risk == "HIGH RISK":
            st.error(
                "Do NOT click suspicious links or share OTPs, "
                "passwords, bank details or card information."
            )

        elif risk == "SUSPICIOUS":
            st.warning(
                "Check the sender and verify the information "
                "independently before taking action."
            )

        else:
            st.success(
                "No listed scam indicators were detected. "
                "Still verify unexpected requests independently."
            )

        st.caption(
            "Demo limitation: This version uses keyword rules, "
            "not the trained Logistic Regression model. "
            "Its percentages are indicators, not validated "
            "AI confidence scores."
        )

# ==========================================
# SCAM ALERT POPUP
# ==========================================

if st.session_state.get("risk") == "HIGH RISK":

    @st.dialog("🚨 SCAM ALERT")
    def scam_popup():
        st.markdown(
            '<div class="popup-title">🚨 SCAM DETECTED!</div>',
            unsafe_allow_html=True
        )

        st.write(
            "ScamLens AI detected multiple potential scam indicators."
        )

        st.error(
            "WARNING: Do not share OTPs, passwords or bank details."
        )

        if st.button("I UNDERSTAND", use_container_width=True):
            st.session_state["risk"] = None
            st.rerun()

    scam_popup()