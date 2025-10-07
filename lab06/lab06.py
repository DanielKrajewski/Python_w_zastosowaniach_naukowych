from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import argparse

url = 'https://rozklad-pkp.pl/'

options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

service = Service('D:\zajecia2\PYTHON\webdriver\chromedriver.exe')

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
print(url)

#<button mode="primary" size="large" class=" css-47sehv"><span>ZGADZAM SIĘ</span></button>
accept_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//button[@mode='primary']")))
accept_button.click()

#<input type="text" id="from-station" class="form-control form-control--switch station-autocomplete z1 ui-autocomplete-input" name="REQ0JourneyStopsS0G" value="" autocomplete="off">

from_station = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='from-station']")))
from_station.send_keys("Warszawa Centralna")
from_station.send_keys(Keys.RETURN)

to_station = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='to-station']")))
to_station.send_keys("Kraków Główny")
to_station.send_keys(Keys.RETURN)

time.sleep(5)

# Scrollujemy stronę w dół, aby załadować więcej artykułów
for _ in range(2):  # Przewiniemy stronę 2 razy
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)


time.sleep(2)

#wczytaj tabele tras
table = driver.find_element(By.ID, "wyniki")

# Znajdź wszystkie wiersze w tabeli
rows = table.find_elements(By.TAG_NAME, "tr")

# Lista na dane
data_list = []

# Pobieranie danych z tabeli
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) > 0:
        raw_time_status = cells[3].text.strip()  # Pobierz tekst i usuń zbędne spacje/enter
        cleaned_time_status = raw_time_status.replace("\n", " ").replace("odj.", "Odjazd:").replace("przyj.", "Przyjazd:").replace("PRZYJAZD ", "").replace("ODJAZD ", "")
        entry = {
            "Data": cells[2].text,
            "Czas/Status": cleaned_time_status,
            "Czas": cells[4].text,
            "Przesiadki": cells[5].text
        }
        data_list.append(entry)
        print(entry)  # Wypisanie wyniku w konsoli

parser = argparse.ArgumentParser(description="Scrape fuel prices and save to a JSON file.")
parser.add_argument("output_file", type=str, help="Output JSON file name")
args = parser.parse_args()

# Zapisz dane do pliku JSON
with open(args.output_file, "w", encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4)

print(json.dumps(data_list, ensure_ascii=False, indent=4))
# Zamknij przeglądarkę
driver.quit()

#poetry run python lab06.py pociagi.json