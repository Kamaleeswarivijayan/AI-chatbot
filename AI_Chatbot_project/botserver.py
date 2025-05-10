from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the simplified query-response dataset
df = pd.read_csv('data/customer_queries.csv')  # Adjust if path differs
df['query'] = df['query'].str.lower()  # Normalize case

# Vectorize queries
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['query'])

@app.route('/ask', methods=['POST'])
def ask():
    user_msg = request.json.get('message', '').lower()

    if not user_msg.strip():
        return jsonify({'response': "Please enter a valid question."})

    user_vec = vectorizer.transform([user_msg])
    similarity_scores = cosine_similarity(user_vec, X)

    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[0, best_match_index]

    # Optional: set threshold for confidence
    if best_score < 0.3:
        return jsonify({'response': "I'm sorry, I couldn't understand your question. Can you please rephrase?"})

    best_response = df.iloc[best_match_index]['response']
    return jsonify({'response': best_response})

if __name__ == '__main__':
    app.run(debug=True)
