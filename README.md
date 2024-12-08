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
# Note
I sincerely apologize for the inconvenience caused due to the absence of the required dataset (main_database.csv) in this project. The dataset was meant to be included to facilitate the functionality and provide an example for testing the recommendation system. Unfortunately, it was inadvertently left out during the preparation process.

To ensure you can still explore the functionality of the code, you may create a mock dataset with the following columns:

Hostel_Name
Hostel_Rating
Hostel_Location
Hostel_Rating_Simple
Gender
Yearly_Hostel_Fees
