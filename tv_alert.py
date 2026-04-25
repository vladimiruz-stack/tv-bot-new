import requests
from bs4 import BeautifulSoup

BOT_TOKEN = "8685078633:AAF46dqI3-SWkUWDEQb21yb8YPfgm4VfpUA"
CHAT_ID = "38908105"

PROGRAMS = [
    "Клара Румянова. Звезда за кадром",
    "НТВ. Дни творения",
    "Перо и шпага Валентина Пикуля",
    "Эдуард Хиль - Сто хитов короля эстрады",
    "Гоголь и ляхи",
    "Волльвебер. Личный враг Гитлера",
    "Спето в СССР. Госпожа удача",
    "Сталин и писатели",
    "Уроки пения",
    "Владимир Володин. Опереточный герой",
    "Николай Гумилев. Завещание",
    "Никулин и Шуйдин",
    "Алексей Попов. Трагедия в трех актах с прологом и эпилогом",
    "В поисках Франции с Вадимом Глускером",
    "Тайны лазурного берега",
    "Последняя капля",
    "Маленькое черное платье",
    "Снять по-французски",
    "Хранители наследства",
    "Другая жизнь Натальи Шмельковой",
    "Исторические путешествия с Иваном Толстым",
    "Стрит-Арт. Философия прямого действия",
    "Мировые леди",
    "Проявления Павла Каплевича",
    "Последний тусовщик Оттепели",
    "Вначале было дело или История русской промышленности",
]

CHANNELS = [
    "Культура",
    "Первый канал",
    "Россия 1",
    "Россия",
    "НТВ",
    "ТВ Центр",
    "Пятый канал",
    "РЕН ТВ",
    "Звезда",
    "Мир",
    "ОТР",
    "Россия 24",
    "Победа",
    "Дом кино",
    "Время",
    "Москва 24",
    "Санкт-Петербург",
    "78",
    "ГТРК",
    "Вести",
    "Регион",
]

SEARCH_URL = "https://tv.yandex.ru/search?text="


def send_telegram(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20
    )
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)


def check_program(title):
    url = SEARCH_URL + requests.utils.quote(title)
    html = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    ).text

    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)

    found_channel = next((ch for ch in CHANNELS if ch in text), None)

    if found_channel:
        return f"Найден возможный эфир:\n«{title}»\nКанал: {found_channel}\n{url}"

    return None


def main():
    results = []

    for title in PROGRAMS:
        result = check_program(title)
        if result:
            results.append(result)

    if results:
        send_telegram("\n\n---\n\n".join(results))
    else:
        print("Эфиров пока не найдено.")


if __name__ == "__main__":
    main()
