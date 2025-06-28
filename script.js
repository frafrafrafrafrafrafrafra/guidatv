const API_BASE = "https://apid.sky.it/gtv/v1/events";

function loadChannelList() {
  fetch("channels.json")
    .then(r => r.json())
    .then(channels => {
      const ul = document.getElementById("channel-list");
      channels.forEach(ch => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = `channel.html?name=${encodeURIComponent(ch.name)}&site_id=${encodeURIComponent(ch.site_id)}`;
        a.textContent = ch.name;
        li.appendChild(a);
        ul.appendChild(li);
      });
    });
}

function loadChannelGuide() {
  const params = new URLSearchParams(window.location.search);
  const name = params.get("name");
  const site_id = params.get("site_id");
  document.getElementById("channel-title").textContent = name;

  let currentDate = new Date();
  let programsCache = {};

  function formatDate(d) {
    return d.toISOString().split("T")[0];
  }

  function showDay(d) {
    const key = formatDate(d);
    document.getElementById("current-day").textContent = key;
    if (programsCache[key]) {
      renderPrograms(programsCache[key]);
    } else {
      fetchProgramsForDate(d, data => {
        programsCache[key] = data;
        renderPrograms(data);
      });
    }
  }

  function fetchProgramsForDate(date, cb) {
    const romeOffset = date.getTimezoneOffset() * 60000;
    const localMidnight = new Date(date - romeOffset);
    localMidnight.setHours(0,0,0,0);

    const fromUtc = new Date(localMidnight);
    const toUtc = new Date(localMidnight);
    toUtc.setDate(toUtc.getDate() + 1);

    const fromStr = fromUtc.toISOString();
    const toStr = toUtc.toISOString();

    const [env, chId] = site_id.split("#");

    const url = `${API_BASE}?from=${fromStr}&to=${toStr}&pageSize=999&pageNum=0&env=${env}&channels=${chId}`;

    fetch(url)
      .then(r => r.json())
      .then(json => {
        cb(json.events || []);
      });
  }

  function renderPrograms(events) {
    const container = document.getElementById("programs");
    container.innerHTML = "";
    if (events.length === 0) {
      container.textContent = "Nessun programma trovato.";
      return;
    }
    events.forEach(e => {
      const div = document.createElement("div");
      div.className = "program";
      const start = new Date(e.starttime).toLocaleTimeString("it-IT", {hour:"2-digit", minute:"2-digit"});
      const stop = new Date(e.endtime).toLocaleTimeString("it-IT", {hour:"2-digit", minute:"2-digit"});
      div.innerHTML = `<strong>${start}-${stop}</strong> ${e.eventTitle}<br><em>${e.eventSynopsis || ""}</em>`;
      container.appendChild(div);
    });
  }

  document.getElementById("prev-day").addEventListener("click", () => {
    currentDate.setDate(currentDate.getDate() - 1);
    showDay(currentDate);
  });

  document.getElementById("next-day").addEventListener("click", () => {
    currentDate.setDate(currentDate.getDate() + 1);
    showDay(currentDate);
  });

  showDay(
    currentDate);
}
