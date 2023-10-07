# ingester
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

base_url = "https://gpt-index.readthedocs.io/en/stable/"

response = requests.get(base_url)

soup = BeautifulSoup(response.text, 'html.parser')

anchors = soup.find_all('a')

filtered_urls = [a['href'] for a in anchors]

urls_list = []
count = 0

for url in filtered_urls:
    if 'http' not in url and '.html' in url:
        full_url = base_url + url
        print(full_url)
        urls_list.append(full_url)
        count += 1

print(f"Found {count} documents")


for url in urls_list:
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()
    # # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)
