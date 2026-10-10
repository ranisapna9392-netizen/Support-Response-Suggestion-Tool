
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResponseMatcher:
    """Match customer messages with the most relevant support response."""

    def __init__(self, data_path=None, threshold=0.10):
        if data_path is None:
            project_root = Path(__file__).resolve().parent.parent
            data_path = project_root / "data" / "responses.json"

        self.data_path = Path(data_path)
        self.threshold = threshold

        self.responses = self._load_responses()

        # Create a flat list of all example queries
        self.example_queries = []
        self.example_categories = []
        self.example_responses = []

        for item in self.responses:
            for query in item["queries"]:
                self.example_queries.append(query)
                self.example_categories.append(item["category"])
                self.example_responses.append(item["response"])

        # Convert queries into TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.query_vectors = self.vectorizer.fit_transform(
            self.example_queries
        )

    def _load_responses(self):
        """Load and validate the JSON dataset."""

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.data_path}"
            )

        with self.data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "The dataset must contain a JSON list."
            )

        required_fields = {"category", "queries", "response"}

        for index, item in enumerate(data):

            if not isinstance(item, dict):
                raise ValueError(
                    f"Record {index + 1} must be a JSON object."
                )

            if not required_fields.issubset(item):
                raise ValueError(
                    f"Record {index + 1} must contain "
                    "category, queries, and response."
                )

            if not isinstance(item["queries"], list):
                raise ValueError(
                    f"'queries' must be a list in record {index + 1}."
                )

            if len(item["queries"]) == 0:
                raise ValueError(
                    f"Record {index + 1} must contain at least one query."
                )

            if not isinstance(item["response"], str):
                raise ValueError(
                    f"'response' must be a string in record {index + 1}."
                )

        return data

    def get_suggestions(self, customer_message, top_n=3):
        """Return the most relevant support suggestions."""

        if not isinstance(customer_message, str):
            raise TypeError(
                "Customer message must be a string."
            )

        if not customer_message.strip():
            raise ValueError(
                "Please provide a customer message."
            )

        customer_vector = self.vectorizer.transform(
            [customer_message]
        )

        similarities = cosine_similarity(
            customer_vector,
            self.query_vectors
        ).flatten()

        ranked_indices = similarities.argsort()[::-1]

        suggestions = []

        seen_categories = set()

        for index in ranked_indices:

            score = float(similarities[index])
            category = self.example_categories[index]

            # Avoid showing the same category multiple times
            if category in seen_categories:
                continue

            # Stop if similarity is below our threshold
            if score < self.threshold:
                break

            seen_categories.add(category)

            suggestions.append({
                "category": category,
                "matched_query": self.example_queries[index],
                "suggested_response": self.example_responses[index],
                "similarity_score": round(score, 4)
            })

            if len(suggestions) >= top_n:
                break

        return suggestions


if __name__ == "__main__":

    matcher = ResponseMatcher()

    customer_message = input(
        "Enter the customer's message: "
    )

    results = matcher.get_suggestions(
        customer_message,
        top_n=3
    )

    print("\nSuggested Responses")
    print("=" * 60)

    if not results:
        print(
            "\nNo confident match found."
            "\nPlease review the customer's issue manually."
        )

    else:
        for rank, result in enumerate(results, start=1):

            print(f"\nSuggestion {rank}")
            print(f"Category: {result['category']}")
            print(
                f"Matched query: "
                f"{result['matched_query']}"
            )
            print(
                f"Similarity score: "
                f"{result['similarity_score']:.2%}"
            )
            print(
                f"Suggested response: "
                f"{result['suggested_response']}"
            )

