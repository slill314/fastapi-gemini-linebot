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
    
def scrape_news():
    #變換ua
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    
    try:
        response = fetch_url_with_retry(url, headers=headers)
        #print("第一次就成功", formatted_time)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        response.raise_for_status()
        #print(f"Error fetching URL: {e}")   
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='part_list_2')
        if news_items:
            messages = []  # 創建一個列表來存儲新聞信息
            for i, item in enumerate(news_items[0].find_all('h3')[:3]):  # 限制顯示前3條新聞
                title = item.text.strip()
                relative_link = item.find('a')['href']
                full_link = urljoin(url_fornews, relative_link)  # 將相對鏈接轉換為完整鏈接
                message = f"隨選新聞 {i + 1}: {title}\n網址: {full_link}"
                messages.append(message)  # 將每條新聞信息添加到列表中
                #print(message)

    return messages
    


        

