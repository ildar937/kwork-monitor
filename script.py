import requests
from bs4 import BeautifulSoup

TOKEN = "8657084178:AAEpghLehd1ijjP57qacmaN3kKFkQtcCNj4"
CHAT_ID = "663371928"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})

def get_kwork_rss():
    # RSS-лента Кворка - ее они отдают охотнее, чем страницы сайта
    url = "https://kwork.ru/projects?c=all&t=all&rss=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'xml') # Читаем как XML
        items = soup.find_all('item')
        
        if not items:
            send("🚫 Лента пуста. Кворк всё еще фильтрует запросы.")
            return

        send(f"📦 <b>ПОСЛЕДНИЕ ЗАКАЗЫ С KWORK:</b>")
        for item in items[:10]:
            title = item.title.text if item.title else "Без названия"
            link = item.link.text if item.link else "https://kwork.ru"
            desc = item.description.text if item.description else ""
            # Очищаем описание от лишнего мусора
            clean_desc = BeautifulSoup(desc, "html.parser").text[:150] + "..."
            
            msg = f"📌 <b>{title}</b>\n\n{clean_desc}\n\n🔗 <a href='{link}'>ОТКРЫТЬ</a>"
            send(msg)
            
    except Exception as e:
        send(f"🚨 Ошибка: {e}")

if __name__ == "__main__":
    get_kwork_rss()
