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
    #current_time = datetime.now()

    #變換ua
    ua = UserAgent()
    user_agent = ua.random

    headers = {'user-agent': user_agent}
    #print(headers)

    # 格式化并打印当前时间
    #formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    #print("執行時間：", formatted_time)

    try:
        response = fetch_url_with_retry(url, headers=headers)
        #print("第一次就成功", formatted_time)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        response.raise_for_status()
        #print(f"Error fetching URL: {e}")
    return response.status_code
    
    


        

