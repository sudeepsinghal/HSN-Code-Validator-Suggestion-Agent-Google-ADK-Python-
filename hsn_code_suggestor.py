from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from hsn_error_handler import HSNErrorHandler

class HSNCodeSuggestor:
    def __init__(self, df):
        self.df = df
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(df['Description'])

    def suggest(self, query, top_k=5):
        try:
            HSNErrorHandler.validate_description_input(query)
        except Exception as e:
            return str(e)

        try:
            query_vec = self.vectorizer.transform([query.lower()])
            cosine_sim = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

            if cosine_sim.max() < 0.3: # Threshold for similarity
                return "No strong matches found."

            top_indices = cosine_sim.argsort()[-top_k:][::-1]
            results = self.df.iloc[top_indices][['HSNCode', 'Description']]
            return HSNErrorHandler.handle_suggestion_response(results)
        except Exception as e:
            HSNErrorHandler.log_warning(f"Suggestion error: {e}")
            return "An error occurred while generating suggestions."