
import os
import ollama


class LocalLLM:
    """Generate responses using Gemini or local Ollama."""

    def __init__(self, model="qwen2.5:3b"):
        self.model = model
        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

    @staticmethod
    def _get_gemini_api_key():
        """Read the key from environment variables or Streamlit secrets."""

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            return api_key

        try:
            import streamlit as st
            return st.secrets.get("GEMINI_API_KEY")
        except Exception:
            return None

    def generate_response(
        self,
        customer_message,
        category,
        support_guidance
    ):
        prompt = f"""
You are a professional customer support assistant.

Draft a helpful, polite, and empathetic response.

CUSTOMER MESSAGE:
{customer_message}

DETECTED CATEGORY:
{category}

APPROVED SUPPORT GUIDANCE:
{support_guidance}

Instructions:
1. Use the approved support guidance.
2. Do not invent policies, refund approvals, delivery dates,
   or actions that have not been confirmed.
3. Do not ask for an order ID if one was already provided.
4. Ask only for information that is genuinely missing.
5. Do not claim to have checked customer accounts or tracking
   systems that you cannot access.
6. Keep the response concise and customer-friendly.
7. Return only the suggested response.
"""

        api_key = self._get_gemini_api_key()

        # Online deployment: use Gemini when a key is configured.
        if api_key:
            from google import genai

            client = genai.Client(api_key=api_key)

            result = client.models.generate_content(
                model=self.gemini_model,
                contents=prompt
            )

            content = result.text

            if not content or not content.strip():
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return content.strip()

        # Local development: use Ollama and Qwen.
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