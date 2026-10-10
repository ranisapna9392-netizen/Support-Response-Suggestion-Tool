import sys
from pathlib import Path

# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.support_pipeline import SupportPipeline


# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Support Response Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 2. Session state and callbacks
# --------------------------------------------------
def clear_form():
    st.session_state["customer_message_input"] = ""
    st.session_state["result"] = None
    st.session_state["error"] = None


if "pipeline" not in st.session_state:
    st.session_state["pipeline"] = SupportPipeline()

if "result" not in st.session_state:
    st.session_state["result"] = None

if "error" not in st.session_state:
    st.session_state["error"] = None

if "customer_message_input" not in st.session_state:
    st.session_state["customer_message_input"] = ""


# --------------------------------------------------
# 3. Sidebar
# --------------------------------------------------
with st.sidebar:
    st.title("💬 Support Assistant")
    st.caption("Customer service response workspace")

    st.divider()

    st.subheader("How it works")

    st.markdown(
        """
        **01 — Enter a message**

        Paste the customer's query into the input box.

        **02 — Analyze the issue**

        The application identifies a likely support category.

        **03 — Generate a response**

        The AI prepares a professional response for review.
        """
    )

    st.divider()

    st.subheader("Good to know")

    st.info(
        "AI-generated responses are suggestions. "
        "Review them before sending them to customers."
    )

    st.caption(
        "Order records, payment systems and customer databases "
        "are not accessed unless separately integrated."
    )


# --------------------------------------------------
# 4. Main heading
# --------------------------------------------------
st.title("💬 Support Response Suggestion Tool")

st.markdown("### Turn customer queries into helpful responses.")

st.write(
    "Analyze customer issues, identify the likely category, "
    "and generate a professional response to help your support "
    "team work more efficiently."
)

st.divider()


# --------------------------------------------------
# 5. Message input
# --------------------------------------------------
st.subheader("✉️ Customer Message")

st.caption(
    "Enter the customer's complete message for a more "
    "context-aware response."
)

customer_message = st.text_area(
    "Message",
    placeholder=(
        "Example: My order is delayed by 10 days. "
        "My order ID is R-3333."
    ),
    height=180,
    key="customer_message_input",
    label_visibility="collapsed"
)

st.caption(
    f"Characters: {len(customer_message):,} | "
    "Include relevant details already provided by the customer."
)

generate_col, clear_col, space_col = st.columns([2, 1, 5])

with generate_col:
    generate_clicked = st.button(
        "✨ Generate Response",
        type="primary",
        use_container_width=True
    )

with clear_col:
    st.button(
        "🗑️ Clear",
        on_click=clear_form,
        use_container_width=True
    )


# --------------------------------------------------
# 6. Generate response
# --------------------------------------------------
if generate_clicked:

    if not customer_message.strip():
        st.session_state["result"] = None
        st.session_state["error"] = None

        st.warning(
            "Please enter a customer message before "
            "generating a response."
        )

    else:
        try:
            with st.spinner(
                "Analyzing the issue and preparing a response..."
            ):
                result = st.session_state["pipeline"].process(
                    customer_message.strip()
                )

            # Validate the pipeline output.
            if not isinstance(result, dict):
                raise TypeError(
                    "SupportPipeline.process() must return a dictionary. "
                    f"Received: {type(result).__name__}"
                )

            st.session_state["result"] = result
            st.session_state["error"] = None

        except Exception as error:
            st.session_state["result"] = None
            st.session_state["error"] = str(error)


# --------------------------------------------------
# 7. Error display
# --------------------------------------------------
if st.session_state["error"]:

    st.error(
        "We couldn't generate a response. "
        "Please check the technical details below."
    )

    with st.expander("View technical error"):
        st.code(st.session_state["error"])


# --------------------------------------------------
# 8. Analysis results
# --------------------------------------------------
result = st.session_state["result"]

if isinstance(result, dict):

    st.divider()
    st.header("📊 Analysis Results")

    status = result.get("status")

    # ----------------------------------------------
    # No matching category
    # ----------------------------------------------
    if status == "no_match":

        st.warning(
            result.get(
                "message",
                "No matching support category was found."
            )
        )

    # ----------------------------------------------
    # Pipeline-reported error
    # ----------------------------------------------
    elif status == "error":

        st.error(
            result.get(
                "message",
                "The pipeline could not process this message."
            )
        )

    # ----------------------------------------------
    # Successful analysis
    # ----------------------------------------------
    elif status == "success":

        # Your pipeline may return the response fields
        # either at the top level or inside suggested_response.
        response = result.get("suggested_response")

        if isinstance(response, dict):
            details = response
        else:
            details = result

        category = details.get(
            "category",
            result.get("category", "Not available")
        )

        similarity_score = details.get(
            "similarity_score",
            result.get("similarity_score")
        )

        original_message = details.get(
            "original_message",
            customer_message.strip()
        )

        suggested_text = details.get("suggested_response")

        # Handle pipelines that return the response as a string.
        if isinstance(response, str):
            suggested_text = response

        # Summary metrics
        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                label="Detected Category",
                value=str(category)
            )

        with metric_col2:
            if isinstance(similarity_score, (int, float)):
                # Accommodate scores represented as 0.85 or 85.
                normalized_score = (
                    similarity_score / 100
                    if similarity_score > 1
                    else similarity_score
                )

                st.metric(
                    label="Text Similarity",
                    value=f"{normalized_score:.2%}"
                )
            else:
                st.metric(
                    label="Text Similarity",
                    value="Not available"
                )

        st.write("")

        # Original message
        with st.container(border=True):
            st.subheader("📝 Original Customer Message")
            st.write(original_message)

        st.write("")

        # Suggested response
        with st.container(border=True):
            st.subheader("🤖 Suggested Support Response")

            if isinstance(suggested_text, str) and suggested_text.strip():

                st.success(suggested_text)

                st.caption(
                    "Review the wording and verify factual claims "
                    "before sending this response."
                )

                st.download_button(
                    label="⬇️ Download Response",
                    data=suggested_text,
                    file_name="suggested_support_response.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            else:
                st.warning(
                    "The analysis succeeded, but the pipeline did not "
                    "return a suggested response in the expected format. "
                    "Check the output of SupportPipeline.process()."
                )

        with st.expander("What does text similarity mean?"):
            st.write(
                "Text similarity indicates how closely the customer "
                "message matches the examples used by the category "
                "matcher. It is not a measure of response quality, "
                "factual accuracy, or customer satisfaction."
            )

    # ----------------------------------------------
    # Unexpected status
    # ----------------------------------------------
    else:

        st.warning(
            "The pipeline returned an unexpected status: "
            f"{status!r}. Check SupportPipeline.process() "
            "to confirm its output format."
        )


# --------------------------------------------------
# 9. Footer
# --------------------------------------------------
st.divider()

st.caption(
    "Support Response Suggestion Tool | "
    "AI-assisted drafting with human review"
)

