import requests
import json
from datetime import datetime, timedelta
import pytz
import os
import time
import sys
from xml.etree import ElementTree as ET

ROME_TZ = pytz.timezone("Europe/Rome")

CHANNELS = [
    {"name":"20Mediaset HD","site_id":"DTH#10458"},
    {"name":"27Twentyseven HD","site_id":"DTH#11342"},
    {"name":"Boomerang","site_id":"DTH#472"},
    {"name":"Boomerang +1","site_id":"DTH#479"},
    {"name":"CACCIA e Pesca","site_id":"DTH#520"},
    {"name":"Canale 5 HD","site_id":"DTH#10354"},
    {"name":"Cartoon Network HD","site_id":"DTH#9693"},
    {"name":"Cartoon +1","site_id":"DTH#476"},
    {"name":"Classica HD","site_id":"DTH#11437"},
    {"name":"Comedy Central","site_id":"DTH#318"},
    {"name":"DMAX HD","site_id":"DTH#8933"},
    {"name":"DeAJunior","site_id":"DTH#7427"},
    {"name":"DeAKids","site_id":"DTH#460"},
    {"name":"Deejay TV","site_id":"DTH#462"},
    {"name":"Discovery HD","site_id":"DTH#9059"},
    {"name":"Euronews","site_id":"DTH#801"},
    {"name":"Eurosport HD","site_id":"DTH#9057"},
    {"name":"Eurosport 2 HD","site_id":"DTH#9060"},
    {"name":"Explorer HD Channel","site_id":"DTH#11262"},
    {"name":"Focus HD","site_id":"DTH#10470"},
    {"name":"Food Network HD","site_id":"DTH#10534"},
    {"name":"Gambero Rosso HD","site_id":"DTH#9099"},
    {"name":"GIALLO HD","site_id":"DTH#8131"},
    {"name":"HGTV HD","site_id":"DTH#11154"},
    {"name":"Heroes Collection","site_id":"DTH#9047"},
    {"name":"History HD","site_id":"DTH#9101"},
    {"name":"Inter TV","site_id":"DTH#9893"},
    {"name":"Iris HD","site_id":"DTH#10467"},
    {"name":"Italia 1 HD","site_id":"DTH#10454"},
    {"name":"K2","site_id":"DTH#6240"},
    {"name":"LA7 HD","site_id":"DTH#319"},
    {"name":"LA7D","site_id":"DTH#6624"},
    {"name":"La 5 HD","site_id":"DTH#10466"},
    {"name":"MTV HD","site_id":"DTH#9195"},
    {"name":"MTV Music","site_id":"DTH#528"},
    {"name":"Mediaset Extra HD","site_id":"DTH#10465"},
    {"name":"Mediaset Italia2 HD","site_id":"DTH#10469"},
    {"name":"Milan TV","site_id":"DTH#9513"},
    {"name":"Motor Trend HD","site_id":"DTH#8130"},
    {"name":"Nick Jr","site_id":"DTH#461"},
    {"name":"Nickelodeon","site_id":"DTH#320"},
    {"name":"NOVE HD","site_id":"DTH#9753"},
    {"name":"Caccia e PESCA","site_id":"DTH#6220"},
    {"name":"RADIOFRECCIA HD","site_id":"DTH#10616"},
    {"name":"RADIONORBA TV","site_id":"DTH#8213"},
    {"name":"RTL 102.5 HD","site_id":"DTH#6885"},
    {"name":"Radio Italia TV HD","site_id":"DTH#9833"},
    {"name":"Radio Italia Trend Tv HD","site_id":"DTH#10033"},
    {"name":"Radio Monte Carlo","site_id":"DTH#10993"},
    {"name":"Rai 1 HD","site_id":"DTH#899"},
    {"name":"Rai 2 HD","site_id":"DTH#898"},
    {"name":"Rai 3 HD","site_id":"DTH#897"},
    {"name":"Rai 4","site_id":"DTH#6622"},
    {"name":"Rai 5","site_id":"DTH#6607"},
    {"name":"Rai Gulp","site_id":"DTH#6629"},
    {"name":"Rai Movie","site_id":"DTH#6608"},
    {"name":"Rai News 24","site_id":"DTH#895"},
    {"name":"Rai Premium","site_id":"DTH#6623"},
    {"name":"RAI Sport","site_id":"DTH#807"},
    {"name":"Rai Storia","site_id":"DTH#6630"},
    {"name":"Rai Yoyo","site_id":"DTH#6609"},
    {"name":"Real Time HD","site_id":"DTH#8173"},
    {"name":"Rete 4 HD","site_id":"DTH#10464"},
    {"name":"San Marino RTV","site_id":"DTH#6861"},
    {"name":"Sky Arte","site_id":"DTH#7767"},
    {"name":"Sky Atlantic","site_id":"DTH#9095"},
    {"name":"Sky Cinema Action","site_id":"DTH#9050"},
    {"name":"Sky Cinema Comedy","site_id":"DTH#9039"},
    {"name":"Sky Cinema Drama","site_id":"DTH#10518"},
    {"name":"Sky Cinema Due","site_id":"DTH#9034"},
    {"name":"Sky Cinema Family","site_id":"DTH#9042"},
    {"name":"Sky Cinema Romance","site_id":"DTH#9055"},
    {"name":"Sky Cinema Suspense","site_id":"DTH#10515"},
    {"name":"Sky Cinema Uno","site_id":"DTH#9044"},
    {"name":"Sky Crime","site_id":"DTH#8336"},
    {"name":"Sky Documentaries","site_id":"DTH#11241"},
    {"name":"Sky Investigation","site_id":"DTH#11246"},
    {"name":"Sky Meteo24","site_id":"DTH#321"},
    {"name":"Sky Nature","site_id":"DTH#11242"},
    {"name":"Sky Serie","site_id":"DTH#11244"},
    {"name":"Sky Sport","site_id":"DTH#11490"},
    {"name":"Sky Sport","site_id":"DTH#11491"},
    {"name":"Sky Sport","site_id":"DTH#11492"},
    {"name":"Sky Sport","site_id":"DTH#11494"},
    {"name":"Sky Sport","site_id":"DTH#11496"},
    {"name":"Sky Sport","site_id":"DTH#11497"},
    {"name":"Sky Sport","site_id":"DTH#617"},
    {"name":"Sky Sport","site_id":"DTH#8613"},
    {"name":"Sky Sport","site_id":"DTH#9046"},
    {"name":"Sky Sport","site_id":"DTH#615"},
    {"name":"Sky Sport 4K","site_id":"DTH#10013"},
    {"name":"Sky Sport24","site_id":"DTH#929"},
    {"name":"Sky Sport Arena","site_id":"DTH#7507"},
    {"name":"Sky Sport Calcio","site_id":"DTH#9113"},
    {"name":"Sky Sport F1","site_id":"DTH#9096"},
    {"name":"Sky Sport Golf","site_id":"DTH#10254"},
    {"name":"Sky Sport Max","site_id":"DTH#9103"},
    {"name":"Sky Sport MotoGP","site_id":"DTH#8434"},
    {"name":"Sky Sport NBA","site_id":"DTH#8753"},
    {"name":"Sky Sport Tennis","site_id":"DTH#11237"},
    {"name":"Sky Sport Uno","site_id":"DTH#8714"},
    {"name":"Sky TG24","site_id":"DTH#9117"},
    {"name":"Sky Uno","site_id":"DTH#9115"},
    {"name":"Super!","site_id":"DTH#6460"},
    {"name":"SuperTennis HD","site_id":"DTH#6000"},
    {"name":"TG NORBA 24","site_id":"DTH#6481"},
    {"name":"TgCom24 HD","site_id":"DTH#10473"},
    {"name":"TOPcrime HD","site_id":"DTH#10468"},
    {"name":"TV2000 HD","site_id":"DTH#7588"},
    {"name":"TV8 HD","site_id":"DTH#8195"},
    {"name":"Virgin Radio","site_id":"DTH#11344"},
    {"name":"ZONA DAZN","site_id":"DTH#11402"},
    {"name":"cielo","site_id":"DTH#8133"},
    {"name":"frisbee","site_id":"DTH#6610"}
]


EPG_GUIDE_CHANNELS = {
    "K2": "K2.it",
    "Motor Trend HD": "MotorTrend.it",
    "GIALLO HD": "Giallo.it",
    "frisbee": "Frisbee.it",
    "Food Network HD": "FoodNetwork.it",
    "HGTV HD": "HGTV.it",
    "DMAX HD": "DMAX.it",
    "NOVE HD": "NOVE.it",
    "Real Time HD": "RealTime.it"
}

def fetch_sky_guide_until_exhausted(env, channel_id, now_rome, max_days=60):
    results = []
    for day_offset in range(max_days):
        date = now_rome + timedelta(days=day_offset)
        date_str = date.strftime("%Y-%m-%d")
        from_str = date.strftime("%Y-%m-%dT00:00:00Z")
        to_str = (date + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        url = f"https://apid.sky.it/gtv/v1/events?from={from_str}&to={to_str}&pageSize=999&pageNum=0&env={env}&channels={channel_id}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            events = data.get("events", [])
            print(f"  ✓ {date_str}: {len(events)} eventi trovati")
            if not events:
                break  # Fine guida per questo canale
            results.append({"date": date_str, "events": events})
            time.sleep(0.3)
        except Exception as e:
            print(f"  ✗ Errore per {date_str}: {e}")
            break
    return results

def parse_epg_guide(channel_name_map, xml_root):
    results = {name: {} for name in channel_name_map}
    for prog in xml_root.findall(".//programme"):
        cid = prog.attrib.get("channel", "").strip()
        title_el = prog.find("title")
        start_raw = prog.attrib.get("start", "")
        stop_raw = prog.attrib.get("stop", "")
        if not (cid and title_el is not None and start_raw and stop_raw):
            continue
        for name, target_id in channel_name_map.items():
            if cid.lower() == target_id.lower():
                dt_start = datetime.strptime(start_raw, "%Y%m%d%H%M%S %z").astimezone(ROME_TZ)
                dt_end = datetime.strptime(stop_raw, "%Y%m%d%H%M%S %z").astimezone(ROME_TZ)
                day = dt_start.strftime("%Y-%m-%d")
                event = {
                    "title": title_el.text,
                    "start": dt_start.isoformat(),
                    "end": dt_end.isoformat()
                }
                results[name].setdefault(day, []).append(event)
    return results

def main():
    os.makedirs("output/guides", exist_ok=True)
    now_rome = datetime.now(ROME_TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    print("==> Inizio elaborazione canali Sky")
    for ch in CHANNELS:
        if ch["name"].strip() in EPG_GUIDE_CHANNELS:
            continue
        env_part, channel_id = ch["site_id"].split("#")
        print(f"• Elaboro {ch['name']} ({ch['site_id']})...")
        guide = fetch_sky_guide_until_exhausted(env_part, channel_id, now_rome)
        if not guide:
            print(f"  ⚠ Nessun evento trovato per {ch['name']}, salto salvataggio")
            continue
        out_path = f"output/guides/{ch['site_id'].replace('#','_')}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({
                "name": ch["name"],
                "events_by_date": {g["date"]: g["events"] for g in guide}
            }, f, indent=2, ensure_ascii=False)
        print(f"  ↳ Salvato {out_path}")

    print("==> Inizio scraping epg-guide.com")
    try:
        resp = requests.get("http://epg-guide.com/dttsat.xml", timeout=30)
        resp.raise_for_status()
        xml_root = ET.fromstring(resp.content)
        print("Scaricamento e parsing XML completati.\n")
    except Exception as e:
        print(f"✗ Errore nel download/parsing XML: {e}")
        return

    parsed = parse_epg_guide(EPG_GUIDE_CHANNELS, xml_root)
    for name, events_by_date in parsed.items():
        site_id = next((c["site_id"] for c in CHANNELS if c["name"] == name), None)
        if not site_id:
            print(f"⚠️ Attenzione: site_id non trovato per {name}, salto salvataggio")
            continue
        out_path = f"output/guides/{site_id.replace('#','_')}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({
                "name": name,
                "events_by_date": events_by_date
            }, f, indent=2, ensure_ascii=False)
        total_events = sum(len(ev) for ev in events_by_date.values())
        print(f"  ↳ Salvato {out_path} ({total_events} eventi)")

if __name__ == "__main__":
    main()
