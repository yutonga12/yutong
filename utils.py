import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

def search_ebay_items(keyword, max_results=5):
    url = f"https://www.ebay.com/sch/i.html?_nkw={keyword.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = []
    for item in soup.select("li.s-item")[:max_results]:
        title_tag = item.select_one("h3.s-item__title")
        link_tag = item.select_one("a.s-item__link")
        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = link_tag['href']
            items.append({'title': title, 'link': link})
    return items

def check_google_presence(title, num_results=5):
    try:
        results = list(search(title, num_results=num_results, stop=num_results))
        non_ebay = [r for r in results if "ebay" not in r.lower()]
        return non_ebay
    except Exception as e:
        return ["[Google 查询失败]"]
