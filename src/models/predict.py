from pathlib import Path
import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

from src.preprocessing.cleaning import clean_email_text

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SAVED_MODELS_DIR = BASE_DIR / "saved_models"


def load_logistic_resources():
    vectorizer = joblib.load(SAVED_MODELS_DIR / "tfidf_vectorizer.pkl")
    model = joblib.load(SAVED_MODELS_DIR / "logistic_regression_model.pkl")
    return vectorizer, model


def predict_logistic(email_text: str):
    cleaned_text = clean_email_text(email_text)
    vectorizer, model = load_logistic_resources()

    X = vectorizer.transform([cleaned_text])
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    confidence = probabilities[prediction]

    return {
        "cleaned_text": cleaned_text,
        "prediction": int(prediction),
        "confidence": float(confidence),
        "probabilities": probabilities.tolist()
    }


def load_distilbert_resources():
    model_path = SAVED_MODELS_DIR / "distilbert_phishing_model"

    tokenizer = AutoTokenizer.from_pretrained(str(model_path), local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(str(model_path), local_files_only=True)
    model.eval()

    return tokenizer, model


def predict_distilbert(email_text: str):
    cleaned_text = clean_email_text(email_text)
    tokenizer, model = load_distilbert_resources()

    inputs = tokenizer(
        cleaned_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.cpu().numpy()[0]
        probabilities = softmax(logits)
        prediction = probabilities.argmax()
        confidence = probabilities[prediction]

    return {
        "cleaned_text": cleaned_text,
        "prediction": int(prediction),
        "confidence": float(confidence),
        "probabilities": probabilities.tolist()
    }