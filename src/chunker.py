import pandas as pd

def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits a text into overlapping chunks of specified size.

    Args:
        text (_type_): The input text to be chunked.
        chunk_size (int, optional): The size of each chunk in characters. Defaults to 500.
        overlap (int, optional): The number of overlapping characters between consecutive chunks. Defaults to 100.

    Returns:
        pandas.DataFrame: A DataFrame containing the chunks with their IDs and text.
    """
    # initial empty chunk list
    chunk_list = []

    start = 0
    chunk_id = 0

    # while start < len(text) we still have text to go over
    while start < len(text):
        # find the end of the text we would like to chunk
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            # append selected chunk to the list
            chunk_list.append({"chunk_id": chunk_id, "text": chunk})
            chunk_id += 1

            # new chunk will overlap 100 characters from previous chunk to give better context to llama3
            start += chunk_size - overlap

    # transform the chunk_list into a pandas dataframe
    df = pd.DataFrame(chunk_list)

    return df