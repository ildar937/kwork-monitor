import requests
from bs4 import BeautifulSoup

TOKEN = "8657084178:AAEpghLehd1ijjP57qacmaN3kKFkQtcCNj4"
CHAT_ID = "663371928"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    requests.post(url, data=data)

def get_projects():
    # Прямая ссылка на ленту всех заказов
    url = "https://kwork.ru/projects" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # На Kwork карточки заказов лежат в этих блоках
        items = soup.find_all('div', class_='want-card')
        
        if not items:
            send_telegram("🧐 Заказов на главной не видно. Пробую найти скрытые...")
            # Попытка найти через другой селектор, если дизайн сменился
            items = soup.select('.project-list .want-card')

        if items:
            send_telegram(f"✅ <b>Нашел заказы! Вывожу первые 10 штук:</b>")
            for item in items[:10]: # Выводим только 10, чтобы не спамить
                title_el = item.find('a')
                price_el = item.find('div', class_='all_price') or item.find('span', class_='wants-card__header-price')
                
                if title_el:
                    title = title_el.text.strip()
                    link = title_el['href']
                    if not link.startswith('http'): link = 'https://kwork.ru' + link
                    price = price_el.text.strip() if price_el else "Цена договорная"
                    
                    msg = f"📌 <b>{title}</b>\n💰 <code>{price}</code>\n🔗 <a href='{link}'>Смотреть заказ</a>"
                    send_telegram(msg)
        else:
            send_telegram("🚫 На Kwork сейчас пусто или сработала защита от ботов. Попробуй позже.")
            
    except Exception as e:
        send_telegram(f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    get_projects()
