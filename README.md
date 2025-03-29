# GSoC assessment

This is a submission for the GSoC Candidate Assessment for the Task [AI-Powered Behavioral Analysis for Suicide Prevention, Substance Use, and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis](https://humanai.foundation/gsoc/2025/proposal_ISSR3.html) from HumanAI.
The deliverables for task 1 are `data_extraction.py` and `reddit_posts.csv`, for task 2 `sentiment_analysis.py`, `data_with_sentiment.csv` and `Data Exploration.ipynb` and for task 3 `extract_location.py`, `data_with_location.csv` and `Data Exploration.ipynb`.

These are the individual tasks:


## Task 1 Social Media Data Extraction & Preprocessing (API Handling & Text Cleaning)
*Estimated Time: 1-1.5 hours*

Use Twitter/X API or Reddit API to extract posts related to mental health distress, substance use, or suicidality.
Apply a predefined list of 10-15 keywords (e.g., "depressed," "addiction help," "overwhelmed," "suicidal") to filter relevant posts.
Store Post ID, Timestamp, Content, Engagement Metrics (likes, comments, shares) in a structured CSV/JSON format.
Remove stopwords, emojis, and special characters for NLP preprocessing.

📌 Deliverable:
- A Python script that retrieves and stores filtered social media posts.
- A cleaned dataset ready for NLP analysis

## Task 2: Sentiment & Crisis Risk Classification (NLP & Text Processing)
*Estimated Time: 1.5-2 hours*

Apply VADER (for Twitter) or TextBlob for sentiment classification (Positive, Neutral, Negative).
Use TF-IDF or Word Embeddings (BERT, Word2Vec) to detect high-risk crisis terms.
Categorize posts into Risk Levels:
High-Risk: Posts with direct crisis language (e.g., “I don’t want to be here anymore”)
Moderate Concern: Seeking help, discussing struggles (e.g., “I feel lost lately”)
Low Concern: General discussions about mental health

📌 Deliverable:
- A script that classifies posts based on sentiment and risk level.
- A table or plot showing the distribution of posts by sentiment and risk category.

## Task 3: Crisis Geolocation & Mapping (Basic Geospatial Analysis & Visualization)
*Estimated Time: 1-2 hours*

Extract location metadata from the dataset using:
Geotagged posts (if available)
NLP-based place recognition (e.g., "Need help in Austin" → Maps to Austin, TX)
Generate a heatmap of crisis-related posts using Folium or Plotly.
Display top 5 locations with the highest crisis discussions.

📌 Deliverable:
- A Python script that geocodes posts and generates a heatmap of crisis discussions.
- A visualization of regional distress patterns in the dataset.- 
