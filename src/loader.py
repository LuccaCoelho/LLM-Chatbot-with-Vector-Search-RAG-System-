import requests
from bs4 import BeautifulSoup

def load_website(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    content = "\n".join([p.get_text() for p in paragraphs if p.get_text(strip=True)])

    return content