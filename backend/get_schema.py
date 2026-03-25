import os
import requests
import json
from dotenv import load_dotenv
load_dotenv(override=True)
url = f"{os.environ.get('SUPABASE_URL')}/rest/v1/?apikey={os.environ.get('SUPABASE_KEY')}"
res = requests.get(url)
definitions = res.json().get('definitions', {})

fks = []
for table in ['adoption_requests', 'donations', 'messages', 'pet_images', 'pets', 'shelters', 'users', 'volunteers']:
    props = definitions.get(table, {}).get('properties', {})
    for k, v in props.items():
        desc = v.get('description', '')
        if 'fk table=' in desc and 'pets' in desc:
            fks.append(f"{table}.{k} -> {desc}")

with open('schema_fks.txt', 'w') as f:
    f.write('\n'.join(fks))
print("Done")
