
from src.response_matcher import ResponseMatcher
from src.local_llm import LocalLLM


class SupportPipeline:
    """Match customer issues and generate responses using a local LLM."""

    def __init__(self):
        self.matcher = ResponseMatcher()
        self.llm = LocalLLM()

    def process(self, customer_message):
        """Match the issue and generate a support response."""

        suggestions = self.matcher.get_suggestions(
            customer_message,
            top_n=1
        )

        if not suggestions:
            return {
                "status": "no_match",
                "message": (
                    "No confident match found. "
                    "Please review the customer's issue manually."
                )
            }

        best_match = suggestions[0]

        try:
            generated_response = self.llm.generate_response(
                customer_message=customer_message,
                category=best_match["category"],
                support_guidance=best_match["suggested_response"]
            )

            return {
                "status": "success",
                "category": best_match["category"],
                "original_message": customer_message,
                "similarity_score": best_match["similarity_score"],    
                "suggested_response": generated_response
                }
            

        except Exception as error:
            return {
                "status": "error",
                "message": (
                    "The local LLM could not generate a response. "
                    "Please ensure Ollama is running. "
                    f"Details: {error}"
                )
            }


if __name__ == "__main__":

    pipeline = SupportPipeline()

    customer_message = input(
        "Enter the customer's message: "
    )

    result = pipeline.process(customer_message)

    print("\nSupport Response Suggestion")
    print("=" * 60)

    if result["status"] != "success":
        print(result["message"])

    else:
        response = result["result"]

        print(f"Category: {response['category']}")
        print(
            f"Similarity Score: "
            f"{response['similarity_score']:.2%}"
        )
        print(
            f"Customer Message: "
            f"{response['original_message']}"
        )
        print("\nAI-Generated Response:")
        print(response["suggested_response"])

