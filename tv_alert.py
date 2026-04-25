import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BOT_TOKEN = "8685078633:AAF46dqI3-SWkUWDEQb21yb8YPfgm4VfpUA"
CHAT_ID = "38908105"

XMLTV_URL = "https://epg.pw/xmltv/epg_RU.xml"

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

def normalize(text):
    return (text or "").lower().replace("ё", "е").replace(".", "").replace(",", "").strip()

def send_telegram(text):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20
    )
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

def parse_time(value):
    if not value:
        return "время не указано"
    return datetime.strptime(value[:14], "%Y%m%d%H%M%S").strftime("%d.%m.%Y %H:%M")

def main():
    xml_text = requests.get(XMLTV_URL, timeout=60).text
    root = ET.fromstring(xml_text)

    channel_map = {}
    for ch in root.findall("channel"):
        ch_id = ch.attrib.get("id")
        name_el = ch.find("display-name")
        if ch_id and name_el is not None and name_el.text:
            channel_map[ch_id] = name_el.text

    found = []
    targets = [(title, normalize(title)) for title in PROGRAMS]

    for item in root.findall("programme"):
        title_el = item.find("title")
        if title_el is None or not title_el.text:
            continue

        tv_title = title_el.text
        tv_title_norm = normalize(tv_title)

        for original_title, target_norm in targets:
            if target_norm == tv_title_norm:
                channel_id = item.attrib.get("channel", "канал не указан")
                channel = channel_map.get(channel_id, channel_id)

                start = parse_time(item.attrib.get("start"))
                stop = parse_time(item.attrib.get("stop"))

                found.append(
                    f"Найден эфир:\n"
                    f"«{tv_title}»\n"
                    f"Канал: {channel}\n"
                    f"Начало: {start}\n"
                    f"Конец: {stop}"
                )

    if found:
        send_telegram("\n\n---\n\n".join(found[:20]))
    else:
        print("Эфиров пока не найдено.")

if __name__ == "__main__":
    main()
