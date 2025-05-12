from src.loader import load_website
from src.chunker import chunk_text
from src.llm_engine import LLMChatBot
import streamlit as st


st.title("LLaMA 3 Chatbot for Any URL")

st.write("### RAG System with Vector Search")

url = st.text_input("Input an URL where LLaMA 3 will get its context from.")

if url and st.button("Load URL"):
    content = load_website(url)
    chunked_content = chunk_text(content)

    bot = LLMChatBot()

    embeddings, index, chunk = bot.embedded_and_faiss_index(chunked_content)

    st.session_state.bot = bot
    st.session_state.embeddings = embeddings
    st.session_state.index = index
    st.session_state.chunk = chunk
    st.markdown("Page loaded successfully")

if "bot" in st.session_state:
    query = st.chat_input("Ask anything related to your URL")

    if query:
        st.write(query)
        with st.spinner("Thinking..."):
            response = st.session_state.bot.generate_response(query, st.session_state.chunk, st.session_state.index, st.session_state.embeddings)

        st.write(response)
