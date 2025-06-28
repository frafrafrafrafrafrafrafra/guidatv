import os
import json

directory = "output/guides"
files = [f for f in os.listdir(directory) if f.endswith(".json") and f != "index.json"]

# opzionale: ordina alfabeticamente
files.sort()

# salva la lista in index.json
with open(os.path.join(directory, "index.json"), "w", encoding="utf-8") as f:
    json.dump(files, f, indent=2)

print(f"Creato {len(files)} file nella lista index.js
on")
