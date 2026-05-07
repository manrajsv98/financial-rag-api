import requests
import streamlit as st


# This is your deployed FastAPI backend URL on Render.
# Streamlit will send API requests to this backend.

API_BASE_URL = "https://financial-rag-api-i8uu.onrender.com"
MAX_FILE_SIZE_MB = 5

# Basic page configuration for the Streamlit app.
st.set_page_config(
    page_title="Document Intelligence",
    page_icon="📈",
)


# Main page title and description.
st.title("📈 Document Intelligence")


st.divider()

st.write(
    "Ask questions over ingested documents and receive grounded answers with sources."
)

st.divider()

st.html(
    """
    <div style='padding: 1.25rem 1.5rem; border-radius: 18px; background: linear-gradient(135deg, #111827 0%, #1f2937 100%); border: 1px solid #374151; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(0,0,0,0.18);'>

        <h2 style='margin: 0 0 0.6rem 0; color: #ffffff; font-size: clamp(1.5rem, 5vw, 1.8rem);'>
            🚀 Quick Start Guide
        </h2>

        <p style='margin: 0 0 1rem 0; color: #d1d5db; font-size: 0.95rem;'>
            Upload a PDF, process it, then ask questions grounded in the document.
        </p>

        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.6rem;'>

            <div style='background:#374151; padding:0.7rem; border-radius:12px; color:white;'>
                <strong>1. Upload</strong><br>
                <span style='color:#d1d5db; font-size:0.85rem;'>Upload a PDF in the sidebar.</span>
            </div>

            <div style='background:#374151; padding:0.7rem; border-radius:12px; color:white;'>
                <strong>2. Configure</strong><br>
                <span style='color:#d1d5db; font-size:0.85rem;'>Set chunk size & overlap.</span>
            </div>

            <div style='background:#374151; padding:0.7rem; border-radius:12px; color:white;'>
                <strong>3. Ask</strong><br>
                <span style='color:#d1d5db; font-size:0.85rem;'>Enter your question.</span>
            </div>

            <div style='background:#374151; padding:0.7rem; border-radius:12px; color:white;'>
                <strong>4. Review</strong><br>
                <span style='color:#d1d5db; font-size:0.85rem;'>Check answer & sources.</span>
            </div>

        </div>
    </div>
    """
)

# -----------------------------
# Sidebar: Document ingestion
# -----------------------------

st.sidebar.header("📥 Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)

chunk_size = st.sidebar.number_input(
    "Chunk size",
    min_value=50,
    max_value=1000,
    value=500,
)

overlap = st.sidebar.number_input(
    "Overlap",
    min_value=0,
    max_value=300,
    value=50,
)

if st.sidebar.button("Ingest Uploaded Document"):
    if uploaded_file is None:
        st.sidebar.warning("Please upload a PDF first.")

    elif uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.sidebar.error(
            f"File too large. Please upload a PDF under {MAX_FILE_SIZE_MB}MB."
        )

    else:
        try:
            with st.spinner("Uploading and ingesting document..."):
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                }

                data = {
                    "chunk_size": chunk_size,
                    "overlap": overlap,
                }

                response = requests.post(
                    f"{API_BASE_URL}/ingest",
                    files=files,
                    data=data,
                    timeout=300,
                )

            if response.status_code == 200:
                st.sidebar.success("Document ingested successfully")
                st.sidebar.json(response.json())
            else:
                st.sidebar.error("Ingestion failed")
                st.sidebar.text(response.text)

        except requests.exceptions.ReadTimeout:
            st.sidebar.error(
                "Ingestion took too long. Try a smaller PDF or use a larger chunk size."
            )

        except requests.exceptions.RequestException as error:
            st.sidebar.error("Could not connect to the backend service.")
            st.sidebar.text(str(error))


# -----------------------------
# Main area: Question answering
# -----------------------------

st.divider()

st.subheader("Ask a question")

# User question input.
question = st.text_input(
    "Question",
    value="What is your question?",
)

# Controls how many chunks the retriever returns.
top_k = st.slider(
    "Number of chunks to retrieve",
    min_value=1,
    max_value=10,
    value=3,
)

# When clicked, this calls the FastAPI /ask endpoint.
if st.button("Ask"):
    # Basic frontend validation.
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            response = requests.post(
                f"{API_BASE_URL}/ask",
                json={
                    "question": question,
                    "top_k": top_k,
                },
                timeout=120,
            )

        # If API call succeeds, show answer and sources.
        if response.status_code == 200:
            result = response.json()

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            # Sources are the chunks retrieved from the vector database.
            for i, source in enumerate(result["sources"], start=1):
                with st.expander(f"Source {i}"):
                    st.json(source)

        # If API call fails, show error.
        else:
            st.error("Request failed")
            st.text(response.text)

