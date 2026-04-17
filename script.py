ще фильтрует запросы.")
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
