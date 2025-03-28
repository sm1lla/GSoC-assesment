import praw
import csv
from datetime import datetime
import os
from dotenv import load_dotenv
import re
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

load_dotenv()

SECRET = os.getenv("SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")


KEYWORDS = [
    "depressed",
    "depression help",
    "addiction",
    "overwhelmed",
    "suicidal",
    "mental health",
    "anxiety",
    "crying",
    "substance abuse",
    "self-harm",
    "drug addiction",
    "hopeless",
    "panic attack",
]

sub_reddits = [
    "mentalhealth",
    "MentalHealthSupport",
    "depression_help",
    "depression",
    "SuicideWatch",
    "MentalHealthIsland",
]

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET,
    username=USER_NAME,
    password=PASSWORD,
    user_agent="data_extractor",
)
# Check if the credentials are valid
print(reddit.user.me())


def contains_keywords(text, keywords):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)


def preprocess_text(text):
    # Remove special characters and emojis
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Convert to lowercase
    text = text.lower()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    text = " ".join(word for word in text.split() if word not in stop_words)

    return text


# Extract posts from a subreddit
def extract_posts(subreddit_name, keywords):
    subreddit = reddit.subreddit(subreddit_name)
    extracted_data = []

    for post in subreddit.top(limit=None):
        if contains_keywords(post.title, keywords) or contains_keywords(
            post.selftext, keywords
        ):
            extracted_data.append(
                {
                    "post_id": post.id,
                    "timestamp": datetime.fromtimestamp(post.created_utc).isoformat(),
                    "content": post.title + "\n" + post.selftext,
                    "preprocessed_content": preprocess_text(
                        post.title + "\n" + post.selftext
                    ),
                    "likes": post.score,
                    "comments": post.num_comments,
                    "shares": post.num_crossposts,
                }
            )

    return extracted_data


# Save extracted data to a CSV file (append mode)
def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "post_id",
                "timestamp",
                "content",
                "preprocessed_content",
                "likes",
                "comments",
                "shares",
            ],
        )
        if not file_exists:
            writer.writeheader()  # Write header only if the file doesn't exist
        writer.writerows(data)


# Main function
def main():
    subreddit_name = "mentalhealth"  # Change this to the subreddit you want to scrape
    output_file = "reddit_posts.csv"

    for subreddit_name in sub_reddits:
        print(f"Extracting posts from r/{subreddit_name}...")
        posts = extract_posts(subreddit_name, KEYWORDS)
        print(f"Extracted {len(posts)} posts.")
        print(f"Saving data to {output_file}...")
        save_to_csv(posts, output_file)
        print("Data saved successfully.")


if __name__ == "__main__":
    main()
