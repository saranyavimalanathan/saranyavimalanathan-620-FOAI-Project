import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Load dataset
data = pd.read_csv("dataset.csv")

X = data["message"]
y = data["label"]


# Convert text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_vectorized = vectorizer.fit_transform(X)


# Train Machine Learning model
model = LogisticRegression()

model.fit(X_vectorized, y)


# Save trained model
with open("scamlens_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)


print("ScamLens AI model trained successfully!")