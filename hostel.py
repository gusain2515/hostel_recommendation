import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def load_and_process_data(file_path):
 
    try:
        # Load the data
        data = pd.read_csv(file_path, index_col=False)

        # Calculate the number of ratings for each hostel
        num_rating_df = data.groupby('Hostel_Name').count()['Hostel_Rating_Simple'].reset_index()
        num_rating_df.rename(columns={'Hostel_Rating_Simple': 'num_ratings'}, inplace=True)

        # Calculate the average rating for each hostel
        avg_rating_df = data.groupby('Hostel_Name').mean()['Hostel_Rating_Simple'].reset_index()
        avg_rating_df.rename(columns={'Hostel_Rating_Simple': 'avg_rating'}, inplace=True)

        # Merge with the original data
        merged_data = data.merge(avg_rating_df, on='Hostel_Name')
        processed_data = merged_data.merge(num_rating_df, on='Hostel_Name')

        # Filter popular hostels with at least 2 ratings
        processed_data = processed_data[processed_data['num_ratings'] >= 2].sort_values('avg_rating', ascending=False)

        # Create a 'tags' column combining relevant features
        processed_data['tags'] = (
            processed_data['Hostel_Rating'].astype(str) +
            processed_data['Hostel_Location'].astype(str) +
            processed_data['Gender'].astype(str)
        )

        # Clean tags by removing spaces and converting to lowercase
        processed_data['tags'] = processed_data['tags'].str.replace(" ", "").str.lower()

        # Vectorize the tags for cosine similarity calculation
        vectorizer = CountVectorizer(max_features=500, stop_words='english')
        vectors = vectorizer.fit_transform(processed_data['tags']).toarray()

        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(vectors)

        return processed_data, similarity_matrix

    except Exception as e:
        print(f"Error processing data: {e}")
        raise

def recommend(hostel_name, data, similarity_matrix):

    try:
        # Check if the hostel exists in the dataset
        if hostel_name not in data['Hostel_Name'].values:
            raise ValueError(f"Hostel '{hostel_name}' not found in the dataset.")

        # Find the index of the input hostel
        hostel_index = data[data['Hostel_Name'] == hostel_name].index[0]

        # Retrieve similarity scores for the input hostel
        distances = similarity_matrix[hostel_index]

        # Get a sorted list of similar hostels
        similar_hostels = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        # Prepare recommendation results
        recommendations = []
        for idx, score in similar_hostels:
            if data.iloc[idx]['Hostel_Name'] != hostel_name and data.iloc[idx]['Gender'] == data.iloc[hostel_index]['Gender']:
                recommendations.append({
                    'Hostel Name': data.iloc[idx]['Hostel_Name'],
                    'Location': data.iloc[idx]['Hostel_Location'],
                    'Average Rating': round(data.iloc[idx]['avg_rating'], 2),
                    'Yearly Fees': data.iloc[idx]['Yearly_Hostel_Fees']
                })

        return recommendations

    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []

if __name__ == "__main__":
    # Path to the CSV file
    FILE_PATH = "main_database.csv"

    try:
        # Load and process data
        processed_data, similarity_matrix = load_and_process_data(FILE_PATH)

        # Example: Recommend similar hostels for 'royal stay'
        hostel_name = "royal stay"
        recommendations = recommend(hostel_name, processed_data, similarity_matrix)

        # Print recommendations
        if recommendations:
            print(f"Recommendations for '{hostel_name}':\n")
            for rec in recommendations:
                print(f"{rec['Hostel Name']}, {rec['Location']}, {rec['Average Rating']}, {rec['Yearly Fees']}")
        else:
            print(f"No recommendations found for '{hostel_name}'.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
