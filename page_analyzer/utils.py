import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests import Response

MAX_LENGTH = 255


def validate(url):
    errors = []
    if not validators.url(url):
        errors.append('Некорректный URL')
    elif len(url) > MAX_LENGTH:
        errors.append('URL превышает 255 символов')
    elif not url:
        errors.append('URL обязателен для заполнения')
    return errors


def normalize(url):
    normalized_url = urlparse(url)
    return f"{normalized_url.scheme}://{normalized_url.netloc}"


def parse_url(response: Response):
    status_code = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.text[:MAX_LENGTH] if soup.h1 else ''
    title = soup.title.text[:MAX_LENGTH] if soup.title else ''
    d_tag = soup.find('meta', attrs={'name': 'description'})
    description = d_tag.get('content')[:MAX_LENGTH] if d_tag else ''
    return status_code, h1, title, description
