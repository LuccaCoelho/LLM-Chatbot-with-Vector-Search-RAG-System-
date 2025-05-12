import faiss
import ollama
from sentence_transformers import SentenceTransformer


class LLMChatBot:
    """
    A chatbot that uses sentence embeddings and FAISS indexing for efficient similarity search, 
    combined with the LLaMA-3 language model for generating responses.
    """        
    def __init__(self, embedding_model= "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Args:
            embedding_model (str, optional): The name of the SentenceTransformer model to use for embeddings. Defaults to "sentence-transformers/all-MiniLM-L6-v2".
        """            
        self.embedding_model = SentenceTransformer(embedding_model)

    @staticmethod
    def query_llama3(prompt, model="llama3"):
        """
        Sends a prompt to the LLaMA-3 model and returns its response.

        Args:
            prompt (_type_): The input prompt for the language model.
            model (str, optional): The name of the LLaMA model to use. Defaults to "llama3".

        Returns:
            str: The generated response from the language model.
        """
        # invoke llama3 and pass the prompt to generate a response
        response = ollama.generate(
            model=model,
            prompt=prompt,
            stream=False
        )

        return response["response"]

    def embedded_and_faiss_index(self, chunk_df):
        """
        enerates embeddings for text chunks and builds a FAISS index for efficient similarity search.

        Args:
            chunk_df (pandas.DataFrame): A DataFrame containing text chunks to be indexed.

        Returns:
            tuple: A tuple containing:
                embeddings (numpy.ndarray): The generated embeddings for all chunks.
                index (faiss.IndexFlatL2): The FAISS index containing the embeddings.
                texts (list): The list of original text chunks.
        """
        # get the text portion of the dataframe and pass it to a list
        texts = chunk_df["text"].tolist()
        
        # Calculates a fixed-size vector representation for each text in list
        embeddings = self.embedding_model.encode(texts)

        # make it easier to search through the embeddings
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        return embeddings, index, texts

    def find_relevant_data(self, query, chunk_list, index, embedding, top_k=5):
        """
        Finds the most relevant text chunks for a given query

        Args:
            query (str): The search query.
            chunk_list (list): List of text chunks to search through.
            index (faiss.IndexFlatL2): The FAISS index containing chunk embeddings.
            embedding (numpy.ndarray): The embeddings of all chunks.
            top_k (int, optional): Number of most relevant chunks to return. Defaults to 5.

        Returns:
            list: A list of the top-k most relevant text chunks.
        """
        
        # Encode the user's query into a vector embedding using the embedding model
        # The encode() method expects a list of texts, so we wrap the query in a list
        query_embedding = self.embedding_model.encode([query])

        # Search the vector index for the top_k most similar embeddings to our query
        # _ (underscore) contains the distances/scores (which we ignore here)
        # I contains the indices of the nearest neighbors in the index
        _, I = index.search(query_embedding, top_k)

        # Retrieve the actual text chunks corresponding to the found indices
        # I[0] accesses the first (and only) set of results since we searched with one query
        # For each index in I[0], we get the corresponding chunk from chunk_list
        return [chunk_list[i] for i in I[0]]

    def generate_response(self, query, chunk, index, embeddings):
        """
        Generates a response to a query using relevant context from the indexed chunks.

        Args:
            query (str): The user's question or prompt.
            chunk (list): List of all text chunks.
            index (faiss.IndexFlatL2): The FAISS index containing chunk embeddings.
            embeddings (numpy.ndarray): The embeddings of all chunks.

        Returns:
            str: The generated response from the language model.
        """
        # store the relevant chunks into a parameter  
        context = "\n".join(self.find_relevant_data(query, chunk, index, embeddings))

        # create our prompt to be passed tollama3
        prompt = f"Use the following context to find the answer tot he question: \n {context}.\n Question: {query} \n Answer: "

        # invoke llama3 and store the response into a parameter
        response = self.query_llama3(prompt)

        return response
