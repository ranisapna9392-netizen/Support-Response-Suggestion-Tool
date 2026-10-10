
from src.response_matcher import ResponseMatcher


def test_delivery_issue_matching():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "my parcel is late"
    )

    assert len(results) > 0
    assert results[0]["category"] == "Delivery Issues"


def test_password_reset_matching():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "I forgot the password for my account"
    )

    assert len(results) > 0
    assert results[0]["category"] == "Password Reset"


def test_payment_issue_matching():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "my card payment was declined"
    )

    assert len(results) > 0
    assert results[0]["category"] == "Payment Issues"


def test_refund_matching():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "I want to get my money back"
    )

    assert len(results) > 0
    assert results[0]["category"] == "Refund Requests"


def test_technical_issue_matching():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "the application crashes whenever I open it"
    )

    assert len(results) > 0
    assert results[0]["category"] == "Technical Issues"


def test_subscription_matching():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "I want to cancel my membership"
    )

    assert len(results) > 0
    assert results[0]["category"] == "Subscription"


def test_unrelated_query():
    matcher = ResponseMatcher()

    results = matcher.get_suggestions(
        "What is the weather today?"
    )

    assert results == []


def test_empty_message():
    matcher = ResponseMatcher()

    try:
        matcher.get_suggestions("")
        assert False
    except ValueError:
        assert True

