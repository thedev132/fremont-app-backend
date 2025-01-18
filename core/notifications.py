import requests
import markdown
from bs4 import BeautifulSoup

def markdown_to_text(markdown_text):
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)
    # Strip HTML tags to get plain text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def send_notifications(tokens, title, body, id):
    # Convert the markdown body to plain text
    plain_text_body = markdown_to_text(body)
    
    messages = [{"to": token, "title": title, "body": plain_text_body, "id": id} for token in tokens]

    for i in range(0, len(messages), 100):
        r = requests.post("https://exp.host/--/api/v2/push/send", json=messages[i : i + 100])

        if not r.ok:
            pass
