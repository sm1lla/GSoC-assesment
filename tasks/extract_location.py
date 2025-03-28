import pandas as pd
import spacy
from geopy.geocoders import Nominatim
import time  # Add this import for introducing delays


# Load spaCy's English model
model = spacy.load("en_core_web_sm")

# Initialize the geocoder with a user agent and increased timeout
geolocator = Nominatim(user_agent="location_extracter", timeout=10)


# Function to extract locations using NER
def extract_locations(text):
    doc = model(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    return locations


def get_coordinates(place_name):
    try:
        location = geolocator.geocode(place_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    # Load data
    data = pd.read_csv("data_with_sentiment.csv")

    # Extract locations
    data["locations"] = data["preprocessed_content"].apply(extract_locations)

    # Extract coordinates using geocoding API with a delay
    data["coordinates"] = data["locations"].apply(
        lambda locations: [get_coordinates(location) for location in locations]
    )

    # Save data to a new CSV file
    data.to_csv("data_with_location.csv", mode="w", index=False)


# Example usage
if __name__ == "__main__":
    main()
