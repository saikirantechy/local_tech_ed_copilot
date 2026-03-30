import streamlit as st
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

# Page Configuration MUST be the first Streamlit command
st.set_page_config(page_title="Local Tech-Ed RAG Copilot", layout="wide", initial_sidebar_state="expanded")

def load_css():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
    }

    .main {
        background-color: #0f172a;
        color: white;
    }

    .stTextInput input, .stFileUploader {
        border-radius: 12px;
        padding: 10px;
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }

    .stButton button {
        border-radius: 10px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: bold;
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }

    /* Style for metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .chat-bubble {
        padding: 12px;
        border-radius: 12px;
        margin: 10px 0;
    }
    .user {
        background-color: #2563eb;
    }
    .bot {
        background-color: #334155;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

@st.cache_resource
def load_models():
    """Load the embedding and generation models."""
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    generator = pipeline(
        "text-generation", 
        model="Qwen/Qwen2.5-1.5B-Instruct", 
        max_new_tokens=256,
        do_sample=False,
        return_full_text=False
    )
    return embedder, generator

with st.spinner("Loading models..."):
    try:
        embedder, generator = load_models()
    except Exception as e:
        st.error(f"Failed to load models. {e}")
        st.stop()

# Initialize session state variables
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
    st.session_state.chunks = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        try:
            reader = PdfReader(uploaded_file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        except Exception as e:
            return ""
    elif uploaded_file.name.endswith((".md", ".txt")):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    return ""

def chunk_text(text, source_name, chunk_size=250, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append({
            "text": " ".join(words[start:end]),
            "source": source_name
        })
        start += chunk_size - overlap
    return chunks

# --- Sidebar Navigation ---
st.sidebar.title("🤖 Local Tech-Ed Copilot")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📚 Knowledge Base",
    "💬 Chat",
    "📊 Dashboard",
    "👨‍💻 About"
])

st.sidebar.markdown("---")
st.sidebar.info("System Status: **Online** 🟢")

# --- Page Logic ---
if page == "🏠 Home":
    st.title("🚀 Local Tech-Ed RAG Copilot")
    st.subheader("Your AI-powered learning assistant")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### ✨ Premium Features
        - 📄 **Multi-Format:** Upload PDFs, TXTs, and Markdown notes
        - ⚡ **Instant Answers:** Ask questions and get cited responses
        - 🔒 **100% Privacy:** Zero API calls. Your data stays on your machine
        - 🧠 **Smart RAG:** Advanced FAISS-based retrieval system
        """)
        st.button("🚀 Get Started", use_container_width=True)
    with col2:
        st.markdown("""
        ### 👨‍🎓 Built for Excellence
        Engineered for students, developers, and the startup ecosystem to maximize productivity securely.
        """)

elif page == "📚 Knowledge Base":
    st.title("📂 Upload Knowledge")
    st.markdown("Upload your study materials, documentation, or textbooks.")
    
    uploaded_files = st.file_uploader("Upload Files (PDF, TXT, MD)", type=["pdf", "md", "txt"], accept_multiple_files=True)
    
    if st.button("Process Documents", use_container_width=True):
        if uploaded_files:
            with st.spinner("Extracting text, chunking, and forming neural embeddings..."):
                all_chunks = []
                for file in uploaded_files:
                    text = extract_text_from_file(file)
                    if text:
                        all_chunks.extend(chunk_text(text, file.name))
                
                if all_chunks:
                    texts = [c["text"] for c in all_chunks]
                    embeddings = embedder.encode(texts, convert_to_numpy=True)
                    embeddings_np = np.array(embeddings).astype("float32")
                    
                    dimension = embeddings_np.shape[1]
                    index = faiss.IndexFlatL2(dimension)
                    index.add(embeddings_np)
                    
                    st.session_state.faiss_index = index
                    st.session_state.chunks = all_chunks
                    st.session_state.doc_count = len(uploaded_files)
                    
                    st.success(f"✅ Indexed! Processed {len(uploaded_files)} files into {len(all_chunks)} searchable chunks.")
                    st.balloons()
                else:
                    st.warning("No valid text could be extracted.")
        else:
            st.warning("Please upload at least one document.")

elif page == "💬 Chat":
    st.title("💬 AI Copilot Chat")
    
    if st.session_state.faiss_index is None:
        st.warning("⚠️ Your knowledge base is empty! Please upload documents in the **Knowledge Base** tab first.")
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "citations" in msg and msg["citations"]:
                    with st.expander("📚 Sources"):
                        for cite in msg["citations"]:
                            st.info(f"**Source:** {cite['source']}\n\n**Content:**\n> {cite['text']}...")

        if prompt := st.chat_input("Ask something..."):
            st.session_state.query_count += 1
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Searching index..."):
                    query_embedding = embedder.encode([prompt], convert_to_numpy=True).astype("float32")
                    distances, indices = st.session_state.faiss_index.search(query_embedding, k=3)
                    
                    retrieved_chunks = [st.session_state.chunks[i] for i in indices[0]]
                    context = "\n\n".join([f"Source: {c['source']}\nContent: {c['text']}" for c in retrieved_chunks])
                    
                    system_prompt = (
                        "You are a helpful Tech-Ed assistant. Answer the user's question based ONLY on the following context. "
                        "Explicitly mention the source document for each piece of information in your answer. "
                        "If the answer is not in the context, say 'I cannot answer this based on the provided documents'.\n\n"
                        f"Context:\n{context}"
                    )
                    
                    chat_prompt = generator.tokenizer.apply_chat_template(
                        [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                        tokenize=False,
                        add_generation_prompt=True
                    )
                    
                    try:
                        outputs = generator(chat_prompt)
                        assistant_response = outputs[0]["generated_text"]
                    except Exception as e:
                        assistant_response = f"Error during generation: {e}"
                        retrieved_chunks = []

                    citations = [{"source": c["source"], "text": c["text"]} for c in retrieved_chunks]
                    st.markdown(assistant_response)
                    
                    if citations:
                        with st.expander("📚 Sources"):
                            for cite in citations:
                                st.info(f"**Source:** {cite['source']}\n\n> {cite['text']}...")
                    
                    # Store
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": assistant_response,
                        "citations": citations
                    })

elif page == "📊 Dashboard":
    st.title("📊 Analytics")
    st.markdown("Track your local AI system usage offline.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    chunk_count = len(st.session_state.chunks)
    
    col1.metric("Indexed Documents", st.session_state.doc_count)
    col2.metric("Knowledge Chunks", chunk_count)
    col3.metric("Total Queries", st.session_state.query_count)
    
    st.markdown("### ⚙️ System Resources")
    st.progress(100, "FAISS Database: Online")
    st.progress(100, "Language Model: Qwen 1.5B loaded")

elif page == "👨‍💻 About":
    st.title("👨‍💻 About Project")
    st.markdown("""
    ### 🚀 Local Tech-Ed RAG Copilot
    Built by **Sai Kiran BK / saikirantechy**
    
    - **AI + RAG System** using State-of-the-Art local models
    - **100% Offline Processing**
    - Built for students, developers, faculty, and the startup ecosystem.
    
    🔗 **GitHub:** [https://github.com/saikirantechy](https://github.com/saikirantechy)
    """)
