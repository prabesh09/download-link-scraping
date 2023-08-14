import requests
from bs4 import BeautifulSoup
import re

start_episode = 1
num_episodes = 12

base_url = "/videos/{name}-episode-"
download_link = "/download?id="

def get_iframe_src(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None

def extract_iframe_src(html_content):
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    iframe_tags = soup.find_all('iframe')
    src_attributes = [iframe['src'] for iframe in iframe_tags if 'src' in iframe.attrs]
    return src_attributes

for i in range(start_episode, num_episodes+1):
    episode_url = f"{base_url}{i}"
    source_code = get_iframe_src(episode_url)

    if source_code:
        iframe_src_list = extract_iframe_src(source_code)
        print(f"Episode {i}:")
        for src in iframe_src_list:
            match = re.search(r'id=(.*?)&', src)
            if match:
                id_value = match.group(1)
                print(f"{download_link}{id_value}")
            else:
                print("ID parameter not found in the link.")
