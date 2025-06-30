import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os

BASE_URL = "https://tvepg.eu"
SCRAPE_SITE_IDS = {
    "boing": "DTH#6628",
    "cartoonito": "DTH#8132",
}

def get_page(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text

def parse_main_page(html, target_date):
    soup = BeautifulSoup(html, "html.parser")
    programs = []
    rows = soup.find_all("tr", itemtype="http://schema.org/BroadcastEvent")
    for row in rows:
        time_tag = row.find("h5", itemprop="startDate")
        if not time_tag:
            continue
        datetime_str = time_tag["content"]
        program_datetime = datetime.fromisoformat(datetime_str)
        program_date_str = program_datetime.strftime("%Y-%m-%d")
        if program_date_str != target_date:
            continue
        time = program_datetime.strftime("%H:%M")
        name_tag = row.find("h6", itemprop="name")
        title = name_tag.text.strip() if name_tag else "N/A"
        desc_tag = row.find("div", class_="description-text")
        desc = desc_tag.text.strip() if desc_tag else ""
        review_link_tag = row.find("a", href=True)
        review_link = BASE_URL + review_link_tag["href"] if review_link_tag else ""
        programs.append({
            "time": time,
            "title": title,
            "description": desc,
            "review_link": review_link
        })
    return programs

def parse_review_page(html):
    soup = BeautifulSoup(html, "html.parser")
    episode_info = ""
    episode_title = ""
    p_tags = soup.find_all("p", class_="grey-text")
    if p_tags:
        episode_info = p_tags[0].text.strip()
    h4 = soup.find("h4", class_="text-justify")
    if h4:
        p_in_h4 = h4.find("p", class_="grey-text")
        if p_in_h4:
            episode_title = p_in_h4.text.strip()
    return episode_info, episode_title

def fetch_for_date(channel, channel_name, date_obj):
    date_str = date_obj.strftime("%Y-%m-%d")
    url = f"{BASE_URL}/it/italy/channel/{channel}/{date_str}"
    print(f"Scarico {channel_name} per il {date_str}...")
    try:
        html = get_page(url)
    except Exception as e:
        print(f"Errore nel download della pagina: {e}")
        return None
    programs = parse_main_page(html, date_str)
    if not programs:
        return None
    events = []
    for prog in programs:
        episode_info = ""
        episode_title = ""
        if prog["review_link"]:
            try:
                review_html = get_page(prog["review_link"])
                episode_info, episode_title = parse_review_page(review_html)
            except Exception as e:
                print(f"Errore caricamento review {prog['review_link']}: {e}")
        events.append({
            "time": prog["time"],
            "title": prog["title"],
            "episode_info": episode_info,
            "episode_title": episode_title,
            "description": prog["description"]
        })
    return events

def main():
    out_dir = "output/guides"
    os.makedirs(out_dir, exist_ok=True)

    for channel, site_id in SCRAPE_SITE_IDS.items():
        channel_name = channel.capitalize()
        site_id_clean = site_id.replace("#", "_")
        out_path = f"{out_dir}/{site_id_clean}.json"

        today = datetime.now().date()
        events_by_date = {}

        # Primo: 7 giorni indietro (ordina crescente)
        for i in range(7, 0, -1):
            d = today - timedelta(days=i)
            day_events = fetch_for_date(channel, channel_name, d)
            if day_events is None:
                print(f"Nessun programma trovato per {d}, continuo.")
            else:
                events_by_date[d.strftime("%Y-%m-%d")] = day_events

        # Poi da oggi in poi fino a quando non trova programmi
        day_offset = 0
        while True:
            current_date = today + timedelta(days=day_offset)
            day_events = fetch_for_date(channel, channel_name, current_date)
            if day_events is None:
                print(f"Nessun programma trovato per {current_date}, termino.")
                break
            events_by_date[current_date.strftime("%Y-%m-%d")] = day_events
            day_offset += 1

        if not events_by_date:
            print(f"Nessun dato scaricato per {channel_name}.")
            continue

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({
                "name": channel_name,
                "events_by_date": events_by_date
            }, f, ensure_ascii=False, indent=2)

        print(f"Guida salvata in {out_path}")

if __name__ == "__main__":
    main()
