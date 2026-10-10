
import ollama


class LocalLLM:
    def __init__(self, model="qwen2.5:3b"):
        self.model = model

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
7. Do not claim that you have checked an account or tracking
   system because you do not have access to those systems.
8. Keep the response clear, concise, and customer-friendly.
9. Return only the suggested response, without analysis.
"""

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