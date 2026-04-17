import requests
from bs4 import BeautifulSoup
import os

# ТВОИ ДАННЫЕ
TOKEN = "8657084178:AAEpghLehd1ijjP57qacmaN3kKFkQtcCNj4"
CHAT_ID = "663371928"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        requests.post(url, data=data)
    except:
        pass

def get_all_projects():
    url = "https://kwork.ru/projects?c=all"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Ищем все карточки заказов
        cards = soup.find_all('div', class_='want-card')
        
        if not cards:
            send_telegram("📭 На странице пока нет доступных заказов.")
            return

        send_telegram(f"🔎 <b>Нашел {len(cards)} заказов на первой странице:</b>")

        for card in cards:
            link_el = card.find('a', target='_blank')
            price_el = card.find('div', class_='all_price') # Ищем цену
            
            if link_el:
                link = link_el['href']
                title = link_el.text.strip()
                price = price_el.text.strip() if price_el else "Цена не указана"
                
                msg = f"💎 <b>{title}</b>\n💰 {price}\n👉 <a href='{link}'>ОТКРЫТЬ ЗАКАЗ</a>"
                send_telegram(msg)
                
    except Exception as e:
        send_telegram(f"❌ Ошибка при чтении страницы: {e}")

if __name__ == "__main__":
    get_all_projects()
