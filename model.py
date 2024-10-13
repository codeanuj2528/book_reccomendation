import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load data (you can adjust the path to your data)
data = pd.read_csv('data/books.csv')

# Handle missing values
data['Author'] = data['Author'].fillna('Unknown Author')
data['Publisher'] = data['Publisher'].fillna('Unknown Publisher')

# Combine relevant features into a single string
data['combined_features'] = data['Title'] + " " + data['Author'] + " " + data['Publisher'] + " " + data['Genre'] + " " + data['SubGenre']

# Vectorize the combined features using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['combined_features'])

# Apply K-Means clustering
num_clusters = 5  # You can adjust the number of clusters based on the data size
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
data['cluster'] = kmeans.fit_predict(tfidf_matrix)

def get_all_book_titles():
    return data['Title'].tolist()  # Return all titles as a list

# Function to get book recommendations based on the same cluster
def get_recommendations(title):
    # Get the cluster of the requested book
    try:
        book_cluster = data[data['Title'].str.lower() == title.lower()]['cluster'].values[0]
    except IndexError:
        raise IndexError("Book not found in the dataset.")
    
    # Get books in the same cluster
    similar_books = data[data['cluster'] == book_cluster]['Title'].tolist()
    
    # Remove the requested book from the list of recommendations
    similar_books.remove(title)

    # Return the top 5 recommendations from the same cluster
    return similar_books[:5]
