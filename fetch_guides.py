import requests
import json
import gzip
import os
import time
import pytz
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

ROME_TZ = pytz.timezone("Europe/Rome")

# Lista completa dei canali (prima i canali RSI)
CHANNELS = [
    # Canali RSI (processati per primi)
    {"name": "RSI La 1", "site_id": "DTH#RS1", "rsi_id": "356"},
    {"name": "RSI La 2", "site_id": "DTH#RS2", "rsi_id": "357"},
    {"name": "Canale 5", "site_id": "DTH#10354", "rsi_id": "79"},
    
    # Canali EPGShare
    {"name": "Eurosport 1", "site_id": "DTH#9057"},
    {"name": "Eurosport 2", "site_id": "DTH#9060"},
    {"name": "DMAX", "site_id": "DTH#8933"},
    {"name": "Real Time", "site_id": "DTH#8173"},
    {"name": "Giallo TV", "site_id": "DTH#8131"},
    {"name": "Food Network", "site_id": "DTH#10534"},
    {"name": "Motor Trend", "site_id": "DTH#8130"},
    {"name": "HGTV", "site_id": "DTH#11154"},
    {"name": "K2", "site_id": "DTH#6240"},
    {"name":"Nove","site_id":"DTH#9753"},
    {"name": "Frisbee", "site_id": "DTH#6610"},
    {"name": "Warner TV", "site_id": "DTH#0001"},
    {"name": "Sky Adventure", "site_id": "DTH#0002"},
    {"name": "Sky Sport Legend", "site_id": "DTH#0003"},
    {"name": "Sky Sport Mix", "site_id": "DTH#0004"},
    {"name": "Radio Italia Trend Tv HD", "site_id": "DTH#10033"},
    {"name":"Sky Sport 24","site_id":"DTH#929"},
    {"name":"Sky Sport Arena","site_id":"DTH#7507"},
    {"name":"Sky Sport MotoGP","site_id":"DTH#8434"},
    {"name":"Sky Sport NBA","site_id":"DTH#8753"},
    {"name":"Sky Sport Uno","site_id":"DTH#8714"},
    {"name":"Virgin Radio","site_id":"DTH#11344"},
    
    # Altri canali Sky API
    {"name":"20Mediaset HD","site_id":"DTH#10458"},
    {"name":"27Twentyseven HD","site_id":"DTH#11342"},
    {"name":"Boomerang","site_id":"DTH#472"},
    {"name":"Boomerang +1","site_id":"DTH#479"},
    {"name":"CACCIA e Pesca","site_id":"DTH#520"},
    {"name":"Cartoon Network HD","site_id":"DTH#9693"},
    {"name":"Cartoon +1","site_id":"DTH#476"},
    {"name":"Classica HD","site_id":"DTH#11437"},
    {"name":"Comedy Central","site_id":"DTH#318"},
    {"name":"DeAJunior","site_id":"DTH#7427"},
    {"name":"DeAKids","site_id":"DTH#460"},
    {"name":"Deejay TV","site_id":"DTH#462"},
    {"name":"Euronews","site_id":"DTH#801"},
    {"name":"Focus HD","site_id":"DTH#10470"},
    {"name":"Gambero Rosso HD","site_id":"DTH#9099"},
    {"name":"Heroes Collection","site_id":"DTH#9047"},
    {"name":"History HD","site_id":"DTH#9101"},
    {"name":"Inter TV","site_id":"DTH#9893"},
    {"name":"Iris HD","site_id":"DTH#10467"},
    {"name":"Italia 1 HD","site_id":"DTH#10454"},
    {"name":"LA7 HD","site_id":"DTH#319"},
    {"name":"LA7D","site_id":"DTH#6624"},
    {"name":"La 5 HD","site_id":"DTH#10466"},
    {"name":"MTV HD","site_id":"DTH#9195"},
    {"name":"MTV Music","site_id":"DTH#528"},
    {"name":"Mediaset Extra HD","site_id":"DTH#10465"},
    {"name":"Mediaset Italia2 HD","site_id":"DTH#10469"},
    {"name":"Nick Jr","site_id":"DTH#461"},
    {"name":"Nickelodeon","site_id":"DTH#320"},
    {"name":"Caccia e PESCA","site_id":"DTH#6220"},
    {"name":"RADIOFRECCIA HD","site_id":"DTH#10616"},
    {"name":"RADIONORBA TV","site_id":"DTH#8213"},
    {"name":"RTL 102.5 HD","site_id":"DTH#6885"},
    {"name":"Radio Italia TV HD","site_id":"DTH#9833"},
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
    {"name":"Sky Nature","site_id":"DTH#11242"},
    {"name":"Sky Serie","site_id":"DTH#11244"},
    {"name":"Sky Sport 4K","site_id":"DTH#10013"},
    {"name":"Sky Sport Calcio","site_id":"DTH#9113"},
    {"name":"Sky Sport F1","site_id":"DTH#9096"},
    {"name":"Sky Sport Golf","site_id":"DTH#10254"},
    {"name":"Sky Sport Max","site_id":"DTH#9103"},
    {"name":"Sky Sport Tennis","site_id":"DTH#11237"},
    {"name":"Sky Uno","site_id":"DTH#9115"},
    {"name":"Super!","site_id":"DTH#6460"},
    {"name":"SuperTennis HD","site_id":"DTH#6000"},
    {"name":"TG NORBA 24","site_id":"DTH#6481"},
    {"name":"TgCom24 HD","site_id":"DTH#10473"},
    {"name":"TOPcrime HD","site_id":"DTH#10468"},
    {"name":"TV2000 HD","site_id":"DTH#7588"},
    {"name":"TV8 HD","site_id":"DTH#8195"},
    {"name":"ZONA DAZN","site_id":"DTH#11402"},
    {"name":"cielo","site_id":"DTH#8133"}
]

# Mappa nome -> site_id solo per i canali EPGShare (esclusi RSI)
EPGSHARE_CHANNELS = {c["name"]: c["site_id"] for c in CHANNELS[3:25]}  # I primi 3 sono BLUE

def fetch_rsi_guide(channel):
    """Scarica TUTTI i programmi disponibili per il canale RSI"""
    print(f"\n=== Scarico palinsesto completo per {channel['name']} ===")
    all_programs = []
    day_offset = 0
    consecutive_empty_days = 0
    MAX_CONSECUTIVE_EMPTY_DAYS = 3  # Interrompe dopo X giorni vuoti

    while True:
        # Calcola l'intervallo giornaliero (dalla mezzanotte alle 24:00)
        day_start = (datetime.now(ROME_TZ) + timedelta(days=day_offset)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        day_end = day_start + timedelta(days=1)
        
        start_str = day_start.strftime("%Y%m%d%H%M")
        end_str = day_end.strftime("%Y%m%d%H%M")
        
        url = f"https://services.sg101.prd.sctv.ch/catalog/tv/channels/list/(ids={channel['rsi_id']};start={start_str};end={end_str};level=normal)"
        print(f"  Giorno: {day_start.strftime('%Y-%m-%d')}", end=" ")
        
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            items = parse_rsi_items(data)
            
            if not items:
                print("⏭️ Nessun programma")
                consecutive_empty_days += 1
                if consecutive_empty_days >= MAX_CONSECUTIVE_EMPTY_DAYS:
                    print(f"  ⚠️ Interruzione dopo {MAX_CONSECUTIVE_EMPTY_DAYS} giorni vuoti")
                    break
                day_offset += 1
                continue
                
            consecutive_empty_days = 0  # Reset contatore
            
            day_programs = []
            for item in items:
                if parse_rsi_title(item) == "Sendepause":
                    continue
                    
                day_programs.append({
                    "start": parse_rsi_start(item),
                    "end": parse_rsi_stop(item),
                    "title": format_rsi_title(item),
                    "synopsis": parse_rsi_description(item)
                })
            
            print(f"✅ {len(day_programs)} programmi")
            all_programs.extend(day_programs)
            day_offset += 1
            
        except Exception as e:
            print(f"❌ Errore: {str(e)}")
            break
            
        time.sleep(0.5)  # Rate limiting

    return all_programs

def parse_rsi_items(data):
    """Analizza la risposta JSON dell'API RSI"""
    try:
        nodes = data["Nodes"]["Items"]
        channels = [n for n in nodes if n["Kind"] == "Channel"]
        if not channels:
            return []
        
        channel = channels[0]
        if channel["Content"]["Nodes"] and isinstance(channel["Content"]["Nodes"]["Items"], list):
            return [i for i in channel["Content"]["Nodes"]["Items"] if i["Kind"] == "Broadcast"]
        return []
    except (KeyError, TypeError):
        return []

def parse_rsi_title(item):
    """Estrae il titolo del programma"""
    return item["Content"]["Description"]["Title"]

def parse_rsi_description(item):
    """Estrae la descrizione del programma"""
    return item["Content"]["Description"].get("Summary", "")

def parse_rsi_start(item):
    """Estrae l'orario di inizio"""
    return item["Availabilities"][0]["AvailabilityStart"]

def parse_rsi_stop(item):
    """Estrae l'orario di fine"""
    return item["Availabilities"][0]["AvailabilityEnd"]

def format_rsi_title(item):
    """Formatta il titolo con SxEy se disponibile"""
    title = parse_rsi_title(item)
    episode_info = parse_rsi_episode_info(item)
    return f"{episode_info} - {title}" if episode_info else title

def parse_rsi_episode_info(item):
    """Estrae SxEy dall'item"""
    try:
        season = item["Content"]["Description"].get("SeasonNumber")
        episode = item["Content"]["Description"].get("EpisodeNumber")
        return f"S{season}E{episode}" if season and episode else ""
    except:
        return ""

def save_rsi_guide(channel, programs):
    """Salva nel formato standard uguale agli altri canali"""
    events_by_date = {}
    
    for program in programs:
        day = datetime.fromisoformat(program["start"]).strftime("%Y-%m-%d")
        events_by_date.setdefault(day, []).append(program)
    
    output_data = {
        "name": channel["name"],
        "events_by_date": events_by_date
    }
    
    fn = f"output/guides/{channel['site_id'].replace('#','_')}.json"
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"  Salvato {fn} con {len(programs)} programmi su {len(events_by_date)} giorni")

def fetch_sky_guide_until_exhausted(env, channel_id, now, max_days=60):
    results = []
    for d in range(max_days):
        date = now + timedelta(days=d)
        ds = date.strftime("%Y-%m-%d")
        fr = date.strftime("%Y-%m-%dT00:00:00Z")
        to = (date + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        url = f"https://apid.sky.it/gtv/v1/events?from={fr}&to={to}&pageSize=999&pageNum=0&env={env}&channels={channel_id}"
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            evs = resp.json().get("events", [])
            print(f"  ✓ {ds}: {len(evs)} eventi")
            if not evs:
                break
            results.append({"date": ds, "events": evs})
            time.sleep(0.3)
        except Exception as e:
            print(f"  ✗ Errore {ds}: {e}")
            break
    return results

def download_and_decompress_epgshare():
    print("\n==> Scarico EPG da epgshare01.online ...")
    r = requests.get("https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz", timeout=30)
    r.raise_for_status()
    return gzip.decompress(r.content)

def parse_epgshare(xml_data, chan_map):
    root = ET.fromstring(xml_data)
    cid_map = {}
    for c in root.findall("channel"):
        cid = c.attrib.get("id")
        n = c.findtext("display-name","").strip()
        for k in chan_map:
            if n.lower() == k.lower():
                cid_map[cid] = k
    print(f"Trovati {len(cid_map)} canali EPGShare")

    out = {k: {} for k in chan_map}
    for p in root.findall(".//programme"):
        cid = p.attrib.get("channel")
        if cid not in cid_map:
            continue
        s = p.attrib.get("start")
        e = p.attrib.get("stop")
        t = p.findtext("title","").strip()
        syn = p.findtext("desc","").strip() if p.find("desc") is not None else ""
        if not (s and e and t):
            continue
        ds = datetime.strptime(s, "%Y%m%d%H%M%S %z").astimezone(ROME_TZ)
        de = datetime.strptime(e, "%Y%m%d%H%M%S %z").astimezone(ROME_TZ)
        day = ds.strftime("%Y-%m-%d")
        ev = {"title": t, "start": ds.isoformat(), "end": de.isoformat()}
        if syn:
            ev["synopsis"] = syn
        out[cid_map[cid]].setdefault(day, []).append(ev)
    return out

def main():
    os.makedirs("output/guides", exist_ok=True)
    now = datetime.now(ROME_TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    print("=== INIZIO ELABORAZIONE ===")
    
    # 1. Processa prima i canali RSI
    print("\n=== PROCESSAMENTO CANALI RSI ===")
    for c in CHANNELS[:3]:  # I primi 3 sono BLUE
        programs = fetch_rsi_guide(c)
        save_rsi_guide(c, programs)

    # 2. EPGShare
    try:
        xml = download_and_decompress_epgshare()
        parsed = parse_epgshare(xml, EPGSHARE_CHANNELS)
        print("\n=== SALVATAGGIO EPGSHARE ===")
        for name, days in parsed.items():
            sid = EPGSHARE_CHANNELS[name]
            tot = sum(len(v) for v in days.values())
            if tot == 0:
                print(f"⚠ Nessun evento per {name}, skip")
                continue
            fn = f"output/guides/{sid.replace('#','_')}.json"
            with open(fn, "w", encoding="utf-8") as f:
                json.dump({"name": name, "events_by_date": days}, f, indent=2, ensure_ascii=False)
            print(f"  ↳ Salvato {fn} ({tot} eventi)")
    except Exception as e:
        print("✗ Errore EPGShare:", e)

    # 3. Sky API
    print("\n=== PROCESSAMENTO SKY API ===")
    for c in CHANNELS[3:]:  # Salta i primi 3 (RSI)
        if c["name"] in EPGSHARE_CHANNELS:
            continue
            
        env, cid = c["site_id"].split("#")
        print(f"\n• {c['name']} ({cid})")
        guide = fetch_sky_guide_until_exhausted(env, cid, now)
        if not guide:
            print(f"  ⚠ Nessun evento per {c['name']}, skip")
            continue
        fn = f"output/guides/{c['site_id'].replace('#','_')}.json"
        with open(fn, "w", encoding="utf-8") as f:
            json.dump({
                "name": c["name"],
                "events_by_date": {g["date"]: g["events"] for g in guide}
            }, f, indent=2, ensure_ascii=False)
        print(f"  ↳ Salvato {fn}")

    print("\n=== ELABORAZIONE COMPLETATA ===")

if __name__ == "__main__":
    main()
