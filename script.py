import requests
from bs4 import BeautifulSoup
import os
import time

TOKEN = "8657084178:AAEpghLehd1ijjP57qacmaN3kKFkQtcCNj4"
CHAT_ID = "663371928"
DB_FILE = "sent_ids.txt"
STATUS_FILE = "last_status.txt"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": False}
    try: requests.post(url, data=data)
    except: pass

def get_projects():
    url = "https://kwork.ru/projects?c=all"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.find_all('div', class_='want-card')
        projects = []
        for card in cards:
            link_el = card.find('a', target='_blank')
            if link_el:
                link = link_el['href']
                title = link_el.text.strip()
                projects.append({'id': link, 'title': title, 'link': link})
        return projects
    except: return []

def main():
    now = time.time()
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            try: last_status_time = float(f.read().strip())
            except: last_status_time = 0
    else: last_status_time = 0

    if now - last_status_time > 1800:
        send_telegram("✅ <b>Мониторинг активен.</b> Новых заказов пока нет.")
        with open(STATUS_FILE, 'w') as f: f.write(str(now))

    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: sent_ids = set(f.read().splitlines())
        is_first_run = False
    else:
        sent_ids = set()
        is_first_run = True

    current_projects = get_projects()
    new_found = []
    for p in reversed(current_projects):
        if p['id'] not in sent_ids:
            prefix = "📦 <b>ТЕКУЩИЙ ЗАКАЗ:</b>" if is_first_run else "🔥 <b>НОВЫЙ ЗАКАЗ!</b>"
            msg = f"{prefix}\n{p['title']}\n\n👉 <a href='{p['link']}'>ОТКРЫТЬ НА KWORK</a>"
            send_telegram(msg)
            new_found.append(p['id'])

    if new_found:
        with open(DB_FILE, 'a') as f:
            for nid in new_found: f.write(f"{nid}\n")

if __name__ == "__main__":
    main()
