import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
from src.models.predict import predict_logistic, predict_distilbert

st.set_page_config(
    page_title="AI Phishing Email Detector",
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI-Powered Phishing Email Detection System")
st.markdown(
    """
    This prototype analyses email content and classifies it as **phishing** or **legitimate**
    using both a traditional machine learning model and a transformer-based NLP model.
    """
)

st.markdown("---")

app_mode = st.radio(
    "Choose analysis mode",
    ["Single Model", "Compare Both Models"],
    horizontal=True
)

if app_mode == "Single Model":
    model_choice = st.selectbox(
        "Select model",
        ["Logistic Regression (TF-IDF)", "DistilBERT"]
    )
else:
    model_choice = None

sample_emails = {
    "None": "",
    "Sample phishing": """Subject: Urgent Account Verification Required

Dear user,

Your account has been temporarily suspended due to suspicious activity.
Please verify your account immediately by clicking the link below:

http://secure-login-verification.com

Failure to act within 24 hours will result in permanent suspension.

Regards,
Security Team""",
    "Sample legitimate": """Subject: Meeting Rescheduled

Hi team,

The project meeting has been moved to 2:00 PM tomorrow in Room B12.
Please bring your weekly progress updates.

Thanks,
Michael""",
    "Sample harder phishing": """Subject: Updated Payroll Document

Hello,

Please review the attached payroll update and confirm your employee details by the end of today.
Use the secure link below to avoid salary delay:

www-payroll-check-portal.net

Best regards,
HR Department"""
}

sample_choice = st.selectbox("Load a sample email", list(sample_emails.keys()))

default_text = sample_emails[sample_choice]

email_text = st.text_area(
    "Enter email content",
    value=default_text,
    height=260,
    placeholder="Paste the subject and body of an email here..."
)

analyse_clicked = st.button("Analyse Email")

def render_result(title, result):
    prediction = result["prediction"]
    confidence = result["confidence"]
    legit_prob = result["probabilities"][0]
    phishing_prob = result["probabilities"][1]

    st.subheader(title)

    if prediction == 1:
        st.error("Prediction: Phishing")
        st.write(
            "This email contains patterns commonly associated with phishing, such as "
            "urgency, suspicious links, or deceptive language."
        )
    else:
        st.success("Prediction: Legitimate")
        st.write(
            "This email appears more consistent with normal legitimate communication."
        )

    st.write("**Confidence level**")
    st.progress(float(confidence))
    st.write(f"{confidence:.4f}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Legitimate", f"{legit_prob:.4f}")
    with col_b:
        st.metric("Phishing", f"{phishing_prob:.4f}")

if analyse_clicked:
    if not email_text.strip():
        st.warning("Please enter some email text before running analysis.")
    else:
        with st.spinner("Analysing email..."):
            if app_mode == "Single Model":
                if model_choice == "Logistic Regression (TF-IDF)":
                    result = predict_logistic(email_text)
                else:
                    result = predict_distilbert(email_text)

                render_result("Detection Result", result)

                st.info(f"Model used: {model_choice}")

                with st.expander("Show cleaned text used for prediction"):
                    st.write(result["cleaned_text"])

            else:
                logistic_result = predict_logistic(email_text)
                distilbert_result = predict_distilbert(email_text)

                col1, col2 = st.columns(2)

                with col1:
                    render_result("Logistic Regression (TF-IDF)", logistic_result)

                with col2:
                    render_result("DistilBERT", distilbert_result)

                with st.expander("Show cleaned text used for prediction"):
                    st.write(logistic_result["cleaned_text"])

st.markdown("---")

with st.expander("About this system"):
    st.write(
        """
        This system was developed as a final year project to compare traditional machine
        learning and transformer-based NLP methods for phishing email detection.
        """
    )

st.caption("Final Year Project Prototype — Cybersecurity and Artificial Intelligence")