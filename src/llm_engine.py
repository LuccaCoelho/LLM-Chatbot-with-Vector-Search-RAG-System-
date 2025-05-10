import faiss
import requests
from sentence_transformers import SentenceTransformer


class LLMChatBot:
        def __init__(self, embedding_model= "sentence-transformers/all-MiniLM-L6-v2"):
            self.embedding_model = SentenceTransformer(embedding_model)

        def embedded_and_faiss_index(self, chunk_df):
            texts = chunk_df["text"].tolist()
            embeddings = self.embedding_model.encode(texts)
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)

            return embeddings, index, texts

        def find_relevant_data(self, query, chunk_list, index, embedding, top_k=5):
            query_embedding = self.embedding_model.encode([query])
            _, I = index.search(query_embedding, top_k)
            return [chunk_list[i] for i in I[0]]

        def generate_response(self, query, chunk, index, embeddings):
            context = "\n".join(self.find_relevant_data(query, chunk, index, embeddings))

            prompt = f"Use the following context to find the answer tot he question: \n {context}.\n Question: {query} \n Answer: "

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )

            return response.json()["response"].strip()
