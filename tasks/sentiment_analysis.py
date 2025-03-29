from textblob import TextBlob
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize
from tqdm import tqdm


def classify_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


def preprocess_text(text):
    # Remove special characters and emojis
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Convert to lowercase
    text = text.lower()

    return text


def calculate_embeddings(texts):
    # Load model
    model = SentenceTransformer("all-mpnet-base-v2")

    # Encode reference texts
    return model.encode(texts, normalize_embeddings=True)


def compare_embeddings(text):
    # Define risk level examples
    high_risk_level_sentences = [
        "i don't want to live anymore",
    ]

    medium_risk_level_sentences = [
        "i am feeling overwhelmed",
        "i need help",
    ]

    # Calculate embeddings for risk level examples
    high_risk_embeddings = calculate_embeddings(high_risk_level_sentences)
    medium_risk_embeddings = calculate_embeddings(medium_risk_level_sentences)

    # Calculate embeddings for input text sentence by sentence
    sentences = sent_tokenize(text)
    sentences = [preprocess_text(sentence) for sentence in sentences]
    text_embeddings = calculate_embeddings(sentences)

    # Calculate similarity scores
    high_risk_similarity_matrix = cosine_similarity(
        text_embeddings, high_risk_embeddings
    )
    medium_risk_similarity_matrix = cosine_similarity(
        text_embeddings, medium_risk_embeddings
    )

    # Find maximum similarity scores
    high_risk_similarities = high_risk_similarity_matrix.max(axis=1)
    medium_risk_similarities = medium_risk_similarity_matrix.max(axis=1)

    # Classify risk level
    if high_risk_similarities.max() > 0.5:
        return "High"
    elif medium_risk_similarities.max() > 0.5:
        return "Moderate"
    else:
        return "Low"


def main():
    # Load data
    data = pd.read_csv("reddit_posts.csv")

    # Classify sentiment
    data["sentiment"] = data["preprocessed_content"].apply(classify_sentiment)

    # Classify risk levels
    tqdm.pandas(desc="Processing risk levels")
    data["risk_level"] = data["content"].progress_apply(compare_embeddings)

    print(data)
    # Save data
    data.to_csv("data_with_sentiment.csv", mode="w", index=False)


# Example usage
if __name__ == "__main__":
    main()
