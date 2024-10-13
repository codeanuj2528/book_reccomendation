from flask import Flask, request, jsonify, render_template
from model import get_recommendations, get_all_book_titles
import logging

# Initialize the Flask app
app = Flask(__name__)

# Setup logging for the Flask app
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')  # Serve the main HTML template

# Route for fetching recommendations
@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if not title:
        logging.warning("No title provided in the request.")
        return jsonify({'error': 'No title provided!'}), 400
    
    try:
        recommendations = get_recommendations(title)
        logging.info(f"Recommendations for '{title}' returned successfully.")
        return jsonify({'recommendations': recommendations})
    except IndexError:
        logging.error(f"Book '{title}' not found in the dataset.")
        return jsonify({'error': 'Book not found!'}), 404

# New route for fetching book titles for autocomplete
@app.route('/get_book_titles', methods=['GET'])
def get_book_titles():
    try:
        titles = get_all_book_titles()  # Fetch all book titles from the dataset
        logging.info("Book titles fetched successfully.")
        return jsonify({'titles': titles})
    except Exception as e:
        logging.error(f"Error fetching book titles: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting the Flask application...")
    app.run(debug=True,port=80)
