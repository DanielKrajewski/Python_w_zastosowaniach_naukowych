import requests
import argparse
from bs4 import BeautifulSoup
import json

# Argument parser
parser = argparse.ArgumentParser(description="Scrape fuel prices and save to a JSON file.")
parser.add_argument("output_file", type=str, help="Output JSON file name")
args = parser.parse_args()

# URL strony z cenami paliw
url = "https://www.e-petrol.pl/notowania/rynek-krajowy/ceny-stacje-paliw"

res = requests.get(url)

#print(res.text)
soup = BeautifulSoup(res.text, 'html.parser')

data=[]
for row in soup.select("table#tablesort85 tbody tr"):
    cols = row.find_all("td")
    if len(cols) == 5:
        aktualizacja = cols[0].text.strip()
        wojewodztwo = cols[1].text.strip()
        pb95 = cols[2].text.strip()
        on = cols[3].text.strip()
        lpg = cols[4].text.strip()
        data.append({
            "aktualizacja": aktualizacja,
            "wojewodztwo": wojewodztwo,
            "pb95": pb95,
            "on": on,
            "lpg": lpg
        })

# Zapisz do pliku JSON
with open(args.output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Wyświetlenie wyników w formacie JSON
print(json.dumps(data, ensure_ascii=False, indent=4))

#poetry run python lab05.py fuel_prices.json