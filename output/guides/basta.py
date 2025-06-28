import os
import json

def generate_index_json(directory='output/guides'):
    files = [f for f in os.listdir(directory) if f.endswith('.json') and f != 'index.json']
    files.sort()
    index_path = os.path.join(directory, 'index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2, ensure_ascii=False)
    print(f'Creato {index_path} con {len(files)} file')

if __name__ == "__main__":
    generate_index_json
  ()
