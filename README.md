# 🔗 LLaMA 3 Chatbot for Any URL

This is a local, private chatbot that allows you to input any URL and ask questions about its content using **LLaMA 3**, **FAISS**, and **Sentence Transformers**.

Everything runs **locally** and **free**, using [Ollama](https://ollama.com) to host LLaMA 3.

---

## 📦 Features
- 🌐 Input any **URL**
- 🔍 Automatically **scrapes** and cleans page text
- 📚 Splits content into **semantic chunks**
- 📌 Uses **Sentence Transformers** for embeddings
- 🧠 Builds an in-memory **FAISS vector store**
- 🤖 Answers questions using **LLaMA 3** from Ollama

---

## 🧰 Tech Stack

| Component       | Tool                                     |
|---------------- |------------------------------------------|
| LLM Backend     | [LLaMA 3 via Ollama](https://ollama.com) |
| Embeddings      | `sentence-transformers` (MiniLM)         |
| Vector DB       | `faiss-cpu`                              |
| Web Scraping    | `requests` + `BeautifulSoup`             |
| Data Cleaning   | `pandas`                                 |                  
| UI              | `Streamlit`                              |
| Language        | Python                                   |

---

## 💻 Try Out on Streamlit

[LLaMA 3 Chatbot](https://study-bot.streamlit.app/)

## 🛠️ Set Up on Your Machine

### 1. Clone the Repo

```bash
git clone https://github.com/LuccaCoelho/LLM-Chatbot-with-Vector-Search-RAG-System-.git
cd LLM-Chatbot-with-Vector-Search-RAG-System-
```
### 2. Install Ollama

[Download Ollama](https://ollama.com/download) and install it for your OS. Then
```bash
ollama pull llama3
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Ollama in the Background

```bash
ollama run llama3
```

### 5. Run the Application

```bash
streamlit run app.py
```
