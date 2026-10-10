
class ResponseGenerator:
    """Generate a final customer-support response."""

    def generate(self, customer_message, suggestion):
        """Create a professional response from a matched suggestion."""

        if not isinstance(customer_message, str):
            raise TypeError(
                "Customer message must be a string."
            )

        if not customer_message.strip():
            raise ValueError(
                "Customer message cannot be empty."
            )

        if not suggestion:
            return (
                "I'm sorry, but I couldn't confidently identify "
                "the issue. Please provide a few more details "
                "so we can assist you."
            )

        category = suggestion["category"]
        response = suggestion["suggested_response"]

        return {
            "category": category,
            "original_message": customer_message,
            "suggested_response": response,
            "similarity_score": suggestion["similarity_score"]
        }


if __name__ == "__main__":

    generator = ResponseGenerator()

    sample_suggestion = {
        "category": "Delivery Issues",
        "suggested_response": (
            "I'm sorry your order hasn't arrived as expected. "
            "Please share your order ID so we can review the "
            "delivery status and help you determine the next steps."
        ),
        "similarity_score": 0.85
    }

    result = generator.generate(
        "My parcel is late.",
        sample_suggestion
    )

    print("\nGenerated Response")
    print("=" * 60)
    print(f"Category: {result['category']}")
    print(
        f"Similarity Score: "
        f"{result['similarity_score']:.2%}"
    )
    print(
        f"Customer Message: "
        f"{result['original_message']}"
    )
    print(
        f"Response: "
        f"{result['suggested_response']}"
    )

