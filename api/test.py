import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent

# 定义要抓取的新闻网页和基础链接
url = "https://www.ettoday.net/news/news-list.htm"
url_fornews = "https://www.ettoday.net/news/"

# 抓取并保存新闻数据为 JSON 文件
def fetch_and_save_news_as_json():
    # 生成随机 UA
    ua = UserAgent()
    headers = {'user-agent': ua.random}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    # 解析 HTML 并获取新闻项
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all('div', class_='part_list_2')

    # 存储新闻数据
    news_data = []
    for i, item in enumerate(news_items[:5]):  # 只取前5则新闻
        title = item.find('h3').text
        relative_link = item.find('a')['href']
        full_link = urljoin(url_fornews, relative_link)  # 转换为完整链接
        news_data.append({"title": title, "link": full_link})

    # 将数据保存到 JSON 文件
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
    print("新闻数据已保存为 JSON 文件。")

# 从 JSON 文件读取新闻数据
def read_news_from_json():
    try:
        with open("news_data.json", "r", encoding="utf-8") as f:
            news_data = json.load(f)
        # 仅展示格式化的新闻信息
        for news in news_data:
            print(f"随选新闻: {news['title']}\n网址: {news['link']}\n")
    except FileNotFoundError:
        print("JSON 文件未找到，请先运行抓取并保存新闻数据的函数。")

# 调用函数保存数据到 JSON
fetch_and_save_news_as_json()

# 调用函数读取数据
#read_news_from_json()
