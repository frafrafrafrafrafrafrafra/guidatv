import requests
import json
from datetime import datetime, timedelta, timezone
import pytz

# Lista canali (escluso canale DTH#11386 che dà problemi)
CHANNELS = [
    {"name":"CNBC HD","site_id":"DTH#10713"},
    {"name":"Sky Crime","site_id":"DTH#11216"},
    {"name":"Sky Serie +1","site_id":"DTH#11247"},
    {"name":"Sky Sport","site_id":"DTH#11490"},
    {"name":"Sky Sport","site_id":"DTH#11491"},
    {"name":"Sky Sport","site_id":"DTH#11492"},
    {"name":"Sky Sport","site_id":"DTH#11494"},
    {"name":"Sky Sport","site_id":"DTH#11496"},
    {"name":"Sky Sport","site_id":"DTH#11497"},
    {"name":"Sky News","site_id":"DTH#445"},
    {"name":"Sky Sport","site_id":"DTH#617"},
    {"name":"NHK World TV HD","site_id":"DTH#6862"},
    {"name":"Sky Crime","site_id":"DTH#8336"},
    {"name":"Sky Atlantic +1","site_id":"DTH#8453"},
    {"name":"Heroes Collection","site_id":"DTH#9047"},
    {"name":"20Mediaset HD","site_id":"DTH#10458"},
    {"name":"ACI Sport Tv","site_id":"DTH#7587"},
    {"name":"Al Jazeera Intl. HD","site_id":"DTH#5113"},
    {"name":"BBC World News","site_id":"DTH#891"},
    {"name":"BIKE","site_id":"DTH#11278"},
    {"name":"Bloomberg","site_id":"DTH#349"},
    {"name":"Boing","site_id":"DTH#6628"},
    {"name":"Boomerang","site_id":"DTH#472"},
    {"name":"Boomerang +1","site_id":"DTH#479"},
    {"name":"CNN Intl.","site_id":"DTH#312"},
    {"name":"CACCIA e Pesca","site_id":"DTH#520"},
    {"name":"Canale 5 HD","site_id":"DTH#10354"},
    {"name":"Cartoon Network HD","site_id":"DTH#9693"},
    {"name":"Cartoon +1","site_id":"DTH#476"},
    {"name":"CARTOONITO DTT","site_id":"DTH#8132"},
    {"name":"cielo","site_id":"DTH#8133"},
    {"name":"Cine34 HD","site_id":"DTH#10893"},
    {"name":"Class CNBC","site_id":"DTH#308"},
    {"name":"Classica HD","site_id":"DTH#11437"},
    {"name":"Comedy Central","site_id":"DTH#318"},
    {"name":"Comedy +1","site_id":"DTH#8353"},
    {"name":"DMAX HD","site_id":"DTH#8933"},
    {"name":"DeAJunior","site_id":"DTH#7427"},
    {"name":"DeAKids","site_id":"DTH#460"},
    {"name":"DeAKids +1","site_id":"DTH#364"},
    {"name":"Deejay TV","site_id":"DTH#462"},
    {"name":"Discovery HD","site_id":"DTH#9059"},
    {"name":"Discovery +1","site_id":"DTH#331"},
    {"name":"EQUtv","site_id":"DTH#8293"},
    {"name":"Emilia Romagna 24","site_id":"DTH#10615"},
    {"name":"Euronews","site_id":"DTH#801"},
    {"name":"Eurosport HD","site_id":"DTH#9057"},
    {"name":"Eurosport 2 HD","site_id":"DTH#9060"},
    {"name":"Explorer HD Channel","site_id":"DTH#11262"},
    {"name":"Fashion TV","site_id":"DTH#810"},
    {"name":"Focus HD","site_id":"DTH#10470"},
    {"name":"Food Network HD","site_id":"DTH#10534"},
    {"name":"Fox Business","site_id":"DTH#6741"},
    {"name":"Fox News","site_id":"DTH#446"},
    {"name":"France 24 English HD","site_id":"DTH#7968"},
    {"name":"France 24 Francais HD","site_id":"DTH#5119"},
    {"name":"-frisbee-","site_id":"DTH#6610"},
    {"name":"Gambero Rosso HD","site_id":"DTH#9099"},
    {"name":"Gambero Rosso HD","site_id":"DTH#11055"},
    {"name":"GIALLO HD","site_id":"DTH#8131"},
    {"name":"HGTV HD","site_id":"DTH#11154"},
    {"name":"History HD","site_id":"DTH#9101"},
    {"name":"History +1","site_id":"DTH#123"},
    {"name":"Horse TV HD","site_id":"DTH#6611"},
    {"name":"i24news","site_id":"DTH#8273"},
    {"name":"Inter TV","site_id":"DTH#9893"},
    {"name":"Iris HD","site_id":"DTH#10467"},
    {"name":"Italia 1 HD","site_id":"DTH#10454"},
    {"name":"Mediaset Italia2 HD","site_id":"DTH#10469"},
    {"name":"K2","site_id":"DTH#6240"},
    {"name":"LA7D","site_id":"DTH#6624"},
    {"name":"LA7 HD","site_id":"DTH#319"},
    {"name":"La 5 HD","site_id":"DTH#10466"},
    {"name":"Lazio Style HD","site_id":"DTH#7527"},
    {"name":"MTV HD","site_id":"DTH#9195"},
    {"name":"MTV Music","site_id":"DTH#528"},
    {"name":"MTV Music","site_id":"DTH#11054"},
    {"name":"Mediaset Extra HD","site_id":"DTH#10465"},
    {"name":"Milan TV","site_id":"DTH#9513"},
    {"name":"Motor Trend HD","site_id":"DTH#8130"},
    {"name":"Nick Jr","site_id":"DTH#461"},
    {"name":"Nick Jr +1","site_id":"DTH#6701"},
    {"name":"Nickelodeon","site_id":"DTH#320"},
    {"name":"Nickelodeon +1","site_id":"DTH#6140"},
    {"name":"NOVE HD","site_id":"DTH#9753"},
    {"name":"Caccia e PESCA","site_id":"DTH#6220"},
    {"name":"QVC","site_id":"DTH#6626"},
    {"name":"RTL 102.5 HD","site_id":"DTH#6885"},
    {"name":"Radio Italia TV HD","site_id":"DTH#9833"},
    {"name":"Radio Italia Trend Tv HD","site_id":"DTH#10033"},
    {"name":"Radio Monte Carlo","site_id":"DTH#10993"},
    {"name":"RADIONORBA TV","site_id":"DTH#8213"},
    {"name":"RADIOFRECCIA HD","site_id":"DTH#10616"},
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
    {"name":"Sky Arte","site_id":"DTH#8473"},
    {"name":"Sky Arte +1","site_id":"DTH#11276"},
    {"name":"Sky Arte +1","site_id":"DTH#11277"},
    {"name":"Sky Atlantic","site_id":"DTH#9095"},
    {"name":"Sky Cinema Action","site_id":"DTH#9050"},
    {"name":"Sky Cinema Comedy","site_id":"DTH#9039"},
    {"name":"Sky Cinema Drama","site_id":"DTH#10518"},
    {"name":"Sky Cinema Due","site_id":"DTH#9034"},
    {"name":"Sky Cinema Due +24","site_id":"DTH#10517"},
    {"name":"Sky Cinema Family","site_id":"DTH#9042"},
    {"name":"Sky Cinema Romance","site_id":"DTH#9055"},
    {"name":"Sky Cinema Suspense","site_id":"DTH#10515"},
    {"name":"Sky Cinema Uno","site_id":"DTH#9044"},
    {"name":"Sky Cinema Uno +24","site_id":"DTH#9037"},
    {"name":"Sky Documentaries","site_id":"DTH#11239"},
    {"name":"Sky Documentaries","site_id":"DTH#11241"},
    {"name":"Sky Documentaries +1","site_id":"DTH#11240"},
    {"name":"Sky Documentaries +1","site_id":"DTH#11243"},
    {"name":"Sky Investigation","site_id":"DTH#11246"},
    {"name":"Sky Investigation +1 HD","site_id":"DTH#11238"},
    {"name":"Sky Meteo24","site_id":"DTH#321"},
    {"name":"Sky Nature","site_id":"DTH#11242"},
    {"name":"Sky Nature","site_id":"DTH#11245"},
    {"name":"Sky Serie","site_id":"DTH#11244"},
    {"name":"Sky Sport 4K","site_id":"DTH#10013"},
    {"name":"Sky Sport","site_id":"DTH#9046"},
    {"name":"Sky Sport","site_id":"DTH#8613"},
    {"name":"Sky Sport","site_id":"DTH#615"},
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
    {"name":"TG24PrimoPiano","site_id":"DTH#6510"},
    {"name":"Sky TG24","site_id":"DTH#9117"},
    {"name":"Sky Uno","site_id":"DTH#9115"},
    {"name":"Sky Uno +1","site_id":"DTH#9114"},
    {"name":"Super!","site_id":"DTH#6460"},
    {"name":"SuperTennis HD","site_id":"DTH#6000"},
    {"name":"TG NORBA 24","site_id":"DTH#6481"},
    {"name":"TgCom24 HD","site_id":"DTH#10473"},
    {"name":"TRM h24","site_id":"DTH#9013"},
    {"name":"TV8 HD","site_id":"DTH#8195"},
    {"name":"TV2000 HD","site_id":"DTH#7588"},
    {"name":"TOPcrime HD","site_id":"DTH#10468"},
    {"name":"27Twentyseven HD","site_id":"DTH#11342"},
    {"name":"VH1 HD","site_id":"DTH#10918"},
    {"name":"Virgin Radio","site_id":"DTH#11344"},
    {"name":"ZONA DAZN 2","site_id":"DTH#11401"},
    {"name":"ZONA DAZN 3","site_id":"DTH#11403"},
    {"name":"ZONA DAZN 4","site_id":"DTH#11405"},
    {"name":"ZONA DAZN 5","site_id":"DTH#11404"},
    {"name":"ZONA DAZN","site_id":"DTH#11402"},
]

# Fuso orario Roma
ROME_TZ = pytz.timezone('Europe/Rome')

def format_date_rome(dt: datetime) -> str:
    """Formatta la data in ISO 8601 Zulu (UTC) con conversione da Roma."""
    dt_rome = ROME_TZ.localize(dt.replace(tzinfo=None))
    dt_utc = dt_rome.astimezone(timezone.utc)
    return dt_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

def fetch_guide_for_day(env: str, channel_id: str, day_rome: datetime):
    """Scarica i programmi per un singolo giorno, con gestione errori."""
    from_str = format_date_rome(day_rome.replace(hour=0, minute=0, second=0, microsecond=0))
    to_str = format_date_rome(day_rome.replace(hour=23, minute=59, second=59, microsecond=999999))
    url = f"https://apid.sky.it/gtv/v1/events?from={from_str}&to={to_str}&pageSize=999&pageNum=0&env={env}&channels={channel_id}"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        events = data.get('events', [])
        return events
    except Exception as e:
        print(f"Errore fetch canale {channel_id} giorno {day_rome.date()}: {e}")
        return []

def fetch_month_guide(env: str, channel_id: str, start_date_rome: datetime, days=30):
    """Scarica il palinsesto di un canale per più giorni."""
    month_guide = []
    for i in range(days):
        day = start_date_rome + timedelta(days=i)
        events = fetch_guide_for_day(env, channel_id, day)
        month_guide.append({
            'date': day.strftime('%Y-%m-%d'),
            'events': events
        })
    return month_guide

def main():
    start_date_rome = datetime.now(ROME_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    full_guide = {}

    for ch in CHANNELS:
        env, channel_id = ch['site_id'].split('#')
        print(f"Fetching {ch['name']} ({ch['site_id']})")
        guide = fetch_month_guide(env, channel_id, start_date_rome, days=30)
        full_guide[ch['name']] = guide

    # Salva su file JSON
    with open('guide_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_guide, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
te_id":"DTH#7968"},
    {"name":"France 24 Francais HD","site_id":"DTH#5119"},
    {"name":"-frisbee-","site_id":"DTH#6610"},
    {"name":"Gambero Rosso HD","site_id":"DTH#9099"},
    {"name":"Gambero Rosso HD","site_id":"DTH#11055"},
    {"name":"GIALLO HD","site_id":"DTH#8131"},
    {"name":"HGTV HD","site_id":"DTH#11154"},
    {"name":"History HD","site_id":"DTH#9101"},
    {"name":"History +1","site_id":"DTH#123"},
    {"name":"Horse TV HD","site_id":"DTH#6611"},
    {"name":"i24news","site_id":"DTH#8273"},
    {"name":"Inter TV","site_id":"DTH#9893"},
    {"name":"Iris HD","site_id":"DTH#10467"},
    {"name":"Italia 1 HD","site_id":"DTH#10454"},
    {"name":"Mediaset Italia2 HD","site_id":"DTH#10469"},
    {"name":"K2","site_id":"DTH#6240"},
    {"name":"LA7D","site_id":"DTH#6624"},
    {"name":"LA7 HD","site_id":"DTH#319"},
    {"name":"La 5 HD","site_id":"DTH#10466"},
    {"name":"Lazio Style HD","site_id":"DTH#7527"},
    {"name":"MTV HD","site_id":"DTH#9195"},
    {"name":"MTV Music","site_id":"DTH#528"},
    {"name":"MTV Music","site_id":"DTH#11054"},
    {"name":"Mediaset Extra HD","site_id":"DTH#10465"},
    {"name":"Milan TV","site_id":"DTH#9513"},
    {"name":"Motor Trend HD","site_id":"DTH#8130"},
    {"name":"Nick Jr","site_id":"DTH#461"},
    {"name":"Nick Jr +1","site_id":"DTH#6701"},
    {"name":"Nickelodeon","site_id":"DTH#320"},
    {"name":"Nickelodeon +1","site_id":"DTH#6140"},
    {"name":"NOVE HD","site_id":"DTH#9753"},
    {"name":"Caccia e PESCA","site_id":"DTH#6220"},
    {"name":"QVC","site_id":"DTH#6626"},
    {"name":"RTL 102.5 HD","site_id":"DTH#6885"},
    {"name":"Radio Italia TV HD","site_id":"DTH#9833"},
    {"name":"Radio Italia Trend Tv HD","site_id":"DTH#10033"},
    {"name":"Radio Monte Carlo","site_id":"DTH#10993"},
    {"name":"RADIONORBA TV","site_id":"DTH#8213"},
    {"name":"RADIOFRECCIA HD","site_id":"DTH#10616"},
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
    {"name":"Sky Arte","site_id":"DTH#8473"},
    {"name":"Sky Arte +1","site_id":"DTH#11276"},
    {"name":"Sky Arte +1","site_id":"DTH#11277"},
    {"name":"Sky Atlantic","site_id":"DTH#9095"},
    {"name":"Sky Cinema Action","site_id":"DTH#9050"},
    {"name":"Sky Cinema Comedy","site_id":"DTH#9039"},
    {"name":"Sky Cinema Drama","site_id":"DTH#10518"},
    {"name":"Sky Cinema Due","site_id":"DTH#9034"},
    {"name":"Sky Cinema Due +24","site_id":"DTH#10517"},
    {"name":"Sky Cinema Family","site_id":"DTH#9042"},
    {"name":"Sky Cinema Romance","site_id":"DTH#9055"},
    {"name":"Sky Cinema Suspense","site_id":"DTH#10515"},
    {"name":"Sky Cinema Uno","site_id":"DTH#9044"},
    {"name":"Sky Cinema Uno +24","site_id":"DTH#9037"},
    {"name":"Sky Documentaries","site_id":"DTH#11239"},
    {"name":"Sky Documentaries","site_id":"DTH#11241"},
    {"name":"Sky Documentaries +1","site_id":"DTH#11240"},
    {"name":"Sky Documentaries +1","site_id":"DTH#11243"},
    {"name":"Sky Investigation","site_id":"DTH#11246"},
    {"name":"Sky Investigation +1 HD","site_id":"DTH#11238"},
    {"name":"Sky Meteo24","site_id":"DTH#321"},
    {"name":"Sky Nature","site_id":"DTH#11242"},
    {"name":"Sky Nature","site_id":"DTH#11245"},
    {"name":"Sky Serie","site_id":"DTH#11244"},
    {"name":"Sky Sport 4K","site_id":"DTH#10013"},
    {"name":"Sky Sport","site_id":"DTH#11386"},
    {"name":"Sky Sport","site_id":"DTH#9046"},
    {"name":"Sky Sport","site_id":"DTH#8613"},
    {"name":"Sky Sport","site_id":"DTH#615"},
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
    {"name":"TG24PrimoPiano","site_id":"DTH#6510"},
    {"name":"Sky TG24","site_id":"DTH#9117"},
    {"name":"Sky Uno","site_id":"DTH#9115"},
    {"name":"Sky Uno +1","site_id":"DTH#9114"},
    {"name":"Super!","site_id":"DTH#6460"},
    {"name":"SuperTennis HD","site_id":"DTH#6000"},
    {"name":"TG NORBA 24","site_id":"DTH#6481"},
    {"name":"TgCom24 HD","site_id":"DTH#10473"},
    {"name":"TRM h24","site_id":"DTH#9013"},
    {"name":"TV8 HD","site_id":"DTH#8195"},
    {"name":"TV2000 HD","site_id":"DTH#7588"},
    {"name":"TOPcrime HD","site_id":"DTH#10468"},
    {"name":"27Twentyseven HD","site_id":"DTH#11342"},
    {"name":"VH1 HD","site_id":"DTH#10918"},
    {"name":"Virgin Radio","site_id":"DTH#11344"},
    {"name":"ZONA DAZN 2","site_id":"DTH#11401"},
    {"name":"ZONA DAZN 3","site_id":"DTH#11403"},
    {"name":"ZONA DAZN 4","site_id":"DTH#11405"},
    {"name":"ZONA DAZN 5","site_id":"DTH#11404"},
    {"name":"ZONA DAZN","site_id":"DTH#11402"},
]

ROME_TZ = pytz.timezone("Europe/Rome")

def fetch_guide_for_day(env, channel_id, date):
    from_str = date.strftime("%Y-%m-%dT00:00:00Z")
    to_date = date + timedelta(days=1)
    to_str = to_date.strftime("%Y-%m-%dT00:00:00Z")
    url = f"https://apid.sky.it/gtv/v1/events?from={from_str}&to={to_str}&pageSize=999&pageNum=0&env={env}&channels={channel_id}"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("events", [])
    except requests.exceptions.RequestException as e:
        print(f"Warning: errore fetch {channel_id} {date.strftime('%Y-%m-%d')}: {e}")
        return []

def fetch_month_guide(env, channel_id, start_date, days=30):
    results = []
    for day_offset in range(days):
        day = start_date + timedelta(days=day_offset)
        events = fetch_guide_for_day(env, channel_id, day)
        results.append({"date": day.strftime("%Y-%m-%d"), "events": events})
    return results

def main():
    now_rome = datetime.now(ROME_TZ)
    start_date_rome = now_rome.replace(hour=0, minute=0, second=0, microsecond=0)

    all_data = {}
    for channel in CHANNELS:
        env, channel_id = channel["site_id"].split("#")
        print(f"Scaricando guida per {channel['name']} ({channel_id})...")
        month_guide = fetch_month_guide(env, channel_id, start_date_rome, days=30)
        all_data[channel_id] = {
            "name": channel["name"],
            "env": env,
            "site_id": channel["site_id"],
            "guide": month_guide
        }
    with open("guides.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print("Download completato, dati salvati in guides.json")

if __name__ == "__main__":
    main()
