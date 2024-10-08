import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent

# 要抓取的新闻网页
url = "https://www.ettoday.net/news/news-list.htm"
url_fornews = "https://www.ettoday.net/news/"

def fetch_url_with_retry(url, headers):
    return requests.get(url, headers=headers)

# 抓取新闻标题和链接的函数，限制只抓取前5则
def scrape_news():
    # 获取当前日期和时间
    current_time = datetime.now()

    #變換ua
    ua = UserAgent()
    user_agent = ua.random

    headers = {'user-agent': user_agent}
    #print(headers)

    # 格式化并打印当前时间
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    #print("執行時間：", formatted_time)

    try:
        response = fetch_url_with_retry(url, headers=headers)
        #print("第一次就成功", formatted_time)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching URL: {e}")
        return []
    
    messages = []  # 用于存储消息的列表

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        news_items = soup.find_all('div', class_='part_list_2')
        if news_items:
            for i, item in enumerate(news_items[:5]):  # 获取前五则新闻
                title = item.find('h3').text
                relative_link = item.find('a')['href']
                full_link = urljoin(url_fornews, relative_link)  # 将相对链接转换为完整链接
                message = f"隨選新聞: {title}\n網址: {full_link}"
                
                messages.append(message)  # 将消息添加到列表

        return messages


# 调用函数并打印结果
#news_messages = scrape_news()
#for message in news_messages:
#    print(message)
