# Hostel Recommendation System
This project uses a content-based recommendation approach to suggest hostels similar to the one selected by the user. Recommendations are based on tags combining ratings, location, and gender-specific preferences.
# Features
Hostel Rating Analysis:

Calculates the average and number of ratings for each hostel.
Filters popular hostels based on a minimum number of ratings.
Tag Creation:

Combines ratings, location, and gender into a tag for each hostel.
Content-Based Recommendations:

Uses cosine similarity to recommend hostels with similar tags.
# Key Functions
Recommend(Hostel_Name)
Input: Name of the hostel (e.g., 'royal stay').
Output: A list of recommended hostels with their location, average rating, and yearly fees.
Logic:
Finds hostels similar to the input hostel based on cosine similarity.
Ensures gender-specific recommendations.
