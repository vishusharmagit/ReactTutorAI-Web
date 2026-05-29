import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

st.set_page_config(page_title="React Tutor AI", page_icon="🤖", layout="centered")
st.title("React Tutor AI")
st.caption("Ask React questions with answers sourced from PDF learning material.")

@st.cache_resource
def load_qa_chain():
    # Set up embeddings
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    # Load ChromaDB
    vectorstore = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings,
        collection_name="react_books"
    )
    
    # Set up Groq LLM
    llm = ChatGroq(
        # model="llama3-8b-8192",
        # model="mixtral-8x7b-32768",
        model="llama-3.3-70b-versatile",
        api_key=st.secrets.get("GROQ_API_KEY"),
        temperature=0.7
    )
    
    return vectorstore, llm

vectorstore, llm = load_qa_chain()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask a React question...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieve relevant documents
            docs = retriever.invoke(prompt)
            context = "\n".join([doc.page_content for doc in docs])
            
            # Create prompt
            prompt_text = f"""You are a React tutor AI. Use the following context to answer React questions accurately and helpfully.

Context:
{context}

Question: {prompt}

Answer:"""
            
            response = llm.invoke(prompt_text)
            answer = response.content if hasattr(response, 'content') else str(response)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
