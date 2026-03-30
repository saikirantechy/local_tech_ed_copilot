import streamlit as st
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

st.set_page_config(page_title="Local Tech-Ed RAG Copilot", layout="wide")

st.title("🤖 Local Tech-Ed RAG Copilot")
st.markdown("A completely local Retrieval-Augmented Generation system. No paid APIs! Running entirely on CPU.")

@st.cache_resource
def load_models():
    """Load the embedding and generation models."""
    # Load Sentence Transformer for Embeddings
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    # Load the LLM Qwen/Qwen2.5-1.5B-Instruct
    # Using return_full_text=False to ensure we only get the generated response
    generator = pipeline(
        "text-generation", 
        model="Qwen/Qwen2.5-1.5B-Instruct", 
        max_new_tokens=256,
        do_sample=False,
        return_full_text=False
    )
    return embedder, generator

with st.spinner("Loading models... This may take a moment on the first run as models are downloaded (~3.5GB)."):
    try:
        embedder, generator = load_models()
    except Exception as e:
        st.error(f"Failed to load models. Please check your internet connection and dependencies. Error: {e}")
        st.stop()

# Initialize session state for the FAISS index, chunks, and chat history
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_text_from_file(uploaded_file):
    """Extracts text from PDF, Markdown, or TXT file uploaders."""
    if uploaded_file.name.endswith(".pdf"):
        try:
            reader = PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text
        except Exception as e:
            st.error(f"Error reading PDF {uploaded_file.name}: {e}")
            return ""
    elif uploaded_file.name.endswith((".md", ".txt")):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    return ""

def chunk_text(text, source_name, chunk_size=250, overlap=50):
    """Chunks text into smaller, overlapping pieces."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_text = " ".join(words[start:end])
        chunks.append({
            "text": chunk_text,
            "source": source_name
        })
        start += chunk_size - overlap
    return chunks

# --- Sidebar for Document Upload and Processing ---
with st.sidebar:
    st.header("📄 Knowledge Base")
    uploaded_files = st.file_uploader(
        "Upload your study materials (PDF, MD, TXT)", 
        type=["pdf", "md", "txt"], 
        accept_multiple_files=True
    )
    
    if st.button("Process Documents", use_container_width=True):
        if uploaded_files:
            with st.spinner("Extracting text, chunking, and embedding documents..."):
                all_chunks = []
                for file in uploaded_files:
                    text = extract_text_from_file(file)
                    if text:
                        file_chunks = chunk_text(text, file.name)
                        all_chunks.extend(file_chunks)
                
                if all_chunks:
                    st.write(f"Embedding {len(all_chunks)} chunks...")
                    texts = [c["text"] for c in all_chunks]
                    embeddings = embedder.encode(texts, convert_to_numpy=True, show_progress_bar=True)
                    
                    # FAISS requires float32
                    embeddings_np = np.array(embeddings).astype("float32")
                    
                    # Create FAISS Index
                    dimension = embeddings_np.shape[1]
                    index = faiss.IndexFlatL2(dimension)
                    index.add(embeddings_np)
                    
                    # Save to session state
                    st.session_state.faiss_index = index
                    st.session_state.chunks = all_chunks
                    st.success(f"Successfully processed {len(uploaded_files)} files into {len(all_chunks)} searchable chunks!")
                else:
                    st.warning("No valid text could be extracted from the uploaded documents.")
        else:
            st.warning("Please upload at least one document.")

# --- Main Chat Interface ---

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Display citations for assistant messages
        if "citations" in msg and msg["citations"]:
            with st.expander("📚 Sources"):
                for cite in msg["citations"]:
                    st.info(f"**Source:** {cite['source']}\n\n**Content:**\n> {cite['text']}...")

# Handle new user input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.faiss_index is None:
            st.warning("Please upload and process documents in the sidebar before asking questions.")
            st.stop()

        with st.spinner("Searching for answers..."):
            # 1. Retrieve top-k relevant chunks
            query_embedding = embedder.encode([prompt], convert_to_numpy=True).astype("float32")
            # Search returns distances and indices
            distances, indices = st.session_state.faiss_index.search(query_embedding, k=3)
            
            retrieved_chunks = [st.session_state.chunks[i] for i in indices[0]]
            
            # 2. Build the context for the LLM
            context = "\n\n".join([f"Source: {c['source']}\nContent: {c['text']}" for c in retrieved_chunks])
            
            system_prompt = (
                "You are a helpful Tech-Ed assistant. Answer the user's question based ONLY on the following context. "
                "Explicitly mention the source document for each piece of information in your answer. "
                "If the answer is not in the context, say 'I cannot answer this based on the provided documents'.\n\n"
                f"Context:\n{context}"
            )
            
            # Use the tokenizer's chat template to format the prompt correctly
            chat_prompt = generator.tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                tokenize=False,
                add_generation_prompt=True
            )
            
            # 3. Generate the answer
            try:
                outputs = generator(chat_prompt)
                assistant_response = outputs[0]["generated_text"]
            except Exception as e:
                st.error(f"Error during text generation: {e}")
                st.stop()

            # Prepare citations for display
            citations = [
                {
                    "source": chunk["source"],
                    "text": chunk["text"]
                }
                for chunk in retrieved_chunks
            ]
            
            # Display response and citations
            st.markdown(assistant_response)
            with st.expander("📚 Sources (Retrieved Chunks)"):
                for cite in citations:
                    st.info(f"**Source:** {cite['source']}\n\n**Content:**\n> {cite['text']}...")
            
            # Save assistant response and its citations to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": assistant_response,
                "citations": citations
            })
