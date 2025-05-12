import requests
from bs4 import BeautifulSoup

def load_website(url: str) -> str:
    """
    Loads and extracts paragraph content from a website URL.

    Args:
        url (str): The URL of the website to load and extract content from.

    Returns:
        str: A string containing all paragraph text from the website joined by newlines.
    """
    # requesting access to the url
    response = requests.get(url)

    # parsing the html
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    # joining every paragraph into a str
    content = "\n".join([p.get_text() for p in paragraphs if p.get_text(strip=True)])

    return content