from src.loader import load_website
from src.chunker import chunk_text
from src.llm_engine import LLMChatBot
import streamlit as st


st.title("CHATBOT with Vector Search")

st.write("### Input Data")

url = st.text_input("What page would you like to parse?")

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
    query = st.chat_input("What is your question?")

    if query:
        with st.spinner("Thinking..."):
            response = st.session_state.bot.generate_response(query, st.session_state.chunk, st.session_state.index, st.session_state.embeddings)

        st.write(response)
