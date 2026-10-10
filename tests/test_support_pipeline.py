
from unittest.mock import MagicMock

from src.support_pipeline import SupportPipeline


def test_pipeline_returns_success_for_matching_message():
    pipeline = SupportPipeline()

    pipeline.matcher = MagicMock()
    pipeline.llm = MagicMock()

    pipeline.matcher.get_suggestions.return_value = [
        {
            "category": "Payment Issues",
            "suggested_response": "Please check your payment details.",
            "similarity_score": 0.85
        }
    ]

    pipeline.llm.generate_response.return_value = (
        "Thank you for contacting us. We can help with your payment concern."
    )

    result = pipeline.process(
        "My payment was deducted twice."
    )

    assert result["status"] == "success"
    assert result["category"] == "Payment Issues"
    assert "payment concern" in result["suggested_response"]


def test_pipeline_returns_no_match():
    pipeline = SupportPipeline()

    pipeline.matcher = MagicMock()
    pipeline.llm = MagicMock()

    pipeline.matcher.get_suggestions.return_value = []

    result = pipeline.process(
        "Tell me about photosynthesis."
    )

    assert result["status"] == "no_match"
    pipeline.llm.generate_response.assert_not_called()


def test_pipeline_handles_llm_error():
    pipeline = SupportPipeline()

    pipeline.matcher = MagicMock()
    pipeline.llm = MagicMock()

    pipeline.matcher.get_suggestions.return_value = [
        {
            "category": "Payment Issues",
            "suggested_response": "Please check your payment details.",
            "similarity_score": 0.85
        }
    ]

    pipeline.llm.generate_response.side_effect = RuntimeError(
        "Test model error"
    )

    result = pipeline.process("My payment failed.")

    assert result["status"] == "error"
    assert "Test model error" in result["message"]