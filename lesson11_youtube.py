# THIS LESSON IS NOT REVIEWED BECAUSE YOUTUBE HAS CHANGE DESIGN TOTALY AND SO NESSASARY NEW RESEARCHE BEFORE PARSIN

mport requests
from bs4 import BeautifulSoup


def get_response(url: str) -> requests.Response:
    r = requests.get(url)
    return r


def get_page_data(response: requests.Response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['content_html']

    soup = BeautifulSoup(html, "lxml")
    print(soup)
    items = soup.find_all("a", id="video-title")
    print(items)


def main():
    url = "https://www.youtube.com/user/Wylsacom/videos"
    r = get_response(url)
    get_page_data(r)


if __name__ == '__main__':
    main()