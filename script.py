import requests
from bs4 import BeautifulSoup

TOKEN = "8657084178:AAEpghLehd1ijjP57qacmaN3kKFkQtcCNj4"
CHAT_ID = "663371928"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True})

def get_kwork():
    # Заходим на страницу заказов с кучей заголовков для маскировки
    url = "https://kwork.ru/projects"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://google.com'
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code != 200:
            send(f"❌ Kwork ответил ошибкой {res.status_code}. Попробуем позже.")
            return

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Самый надежный способ - ищем все ссылки, которые ведут на проекты
        found = False
        projects = soup.find_all('div', class_='want-card')
        
        if projects:
            send(f"🚀 <b>ПРЯМОЙ ЭФИР: СВЕЖИЕ ЗАКАЗЫ</b>")
            for p in projects[:15]:
                link_el = p.find('a', href=True)
                price_el = p.find('div', class_='all_price') or p.find('span', class_='wants-card__header-price')
                
                if link_el and '/projects/' in link_el['href']:
                    title = link_el.text.strip()
                    link = link_el['href']
                    price = price_el.text.strip() if price_el else "Цена договорная"
                    
                    send(f"💎 <b>{title}</b>\n💰 <code>{price}</code>\n🔗 <a href='{link}'>ОТКРЫТЬ</a>")
                    found = True
        
        if not found:
            send("⚠️ Kwork спрятал заказы за проверку. Ждем 10-15 минут, пока «остынет».")
            
    except Exception as e:
        send(f"🚨 Ошибка: {e}")

if __name__ == "__main__":
    get_kwork()
