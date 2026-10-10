import os

import ollama


class LocalLLM:
    """Generate responses using local Ollama or hosted Mistral."""

    def __init__(self, model="qwen2.5:3b"):
        self.model = model
        self.mistral_model = os.getenv(
            "MISTRAL_MODEL",
            "mistral-small-2603"
        )

    @staticmethod
    def _get_mistral_api_key():
        """Read the API key from environment variables or Streamlit secrets."""

        api_key = os.getenv("MISTRAL_API_KEY")

        if api_key:
            return api_key

        try:
            import streamlit as st
            return st.secrets.get("MISTRAL_API_KEY")
        except Exception:
            # No Streamlit secret configured; use local Ollama.
            return None

    def generate_response(
        self,
        customer_message,
        category,
        support_guidance
    ):
        prompt = f"""
You are a professional customer support assistant.

Your task is to draft a helpful, polite, and empathetic
response to the customer's message.

CUSTOMER MESSAGE:
{customer_message}

DETECTED CATEGORY:
{category}

APPROVED SUPPORT GUIDANCE:
{support_guidance}

Instructions:
1. Write a professional and empathetic response.
2. Use the approved support guidance.
3. Do not invent policies, refund approvals, delivery dates,
   or actions that have not been confirmed.
4. If the customer has already provided an order ID,
   do not ask for it again.
5. If an order ID is provided, acknowledge it where relevant.
6. Ask only for information that is genuinely missing.
7. Do not claim that you checked an account or tracking
   system because you do not have access to those systems.
8. Keep the response clear, concise, and customer-friendly.
9. Return only the suggested response, without analysis.
"""

        api_key = self._get_mistral_api_key()

        # Use the hosted API when a key is configured.
        if api_key:
            from mistralai.client import Mistral

            with Mistral(api_key=api_key) as client:
                result = client.chat.complete(
                    model=self.mistral_model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1
                )

            content = result.choices[0].message.content

            if not isinstance(content, str) or not content.strip():
                raise RuntimeError(
                    "Mistral returned an empty response."
                )

            return content.strip()

        # Otherwise, use the local Ollama server.
        result = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={"temperature": 0.1}
        )

        return result["message"]["content"].strip()