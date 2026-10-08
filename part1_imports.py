# Laborator: funcții, metode și importuri pe web
# Student: <Numele Tău>

import sys
import time
import requests
import urllib.request

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 1. Primul import
print("1. Versiune requests:", requests.__version__)
# Explicație: 'urllib' este inclus în biblioteca standard Python (este preinstalat),
# în timp ce 'requests' este o bibliotecă terță creată de comunitate și necesită instalare separată.

# Exercițiul 2. Două stiluri de import
res1 = requests.get(BASE_URL, timeout=TIMEOUT)
print("2. Status (requests.get):", res1.status_code)

from requests import get

res2 = get(BASE_URL, timeout=TIMEOUT)
print("2. Status (from requests import get):", res2.status_code)
# Avantaj 'import requests': Evită conflictele de nume și arată clar originea funcției.
# Avantaj 'from requests import get': Scrie cod mai scurt și apelează direct funcția.

# Exercițiul 3. Alias-uri
import requests as rq

res3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("3. Status (alias rq):", res3.status_code)
# Un alias scurt (ex: rq, np, pd) face codul concis când este folosit des,
# dar poate îngreuna citirea dacă este neobișnuit sau obscur.

# Exercițiul 4. Doar biblioteca standard
req = urllib.request.Request(
    BASE_URL, 
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)
with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
    status_code = response.status
    body_bytes = response.read()
    body_text = body_bytes.decode("utf-8")
    print("4. Status urllib:", status_code)
    print("4. Primele 200 de caractere:\n", body_text[:200])
    
# Exercițiul 5. Priviți în interiorul unui modul
# print(dir(requests))
# 'get' -> funcție | 'Response' -> clasă | 'exceptions' -> modul

# Exercițiul 6. Citiți documentația
res_timeout = requests.get(BASE_URL, timeout=TIMEOUT)
print("6. Request reusit cu timeout explicit:", res_timeout.status_code)

# Exercițiul 7. Cronometrarea unei cereri
t_start = time.perf_counter()
res_time = requests.get(BASE_URL, timeout=TIMEOUT)
t_end = time.perf_counter()

print(f"7. Durată totală (perf_counter): {t_end - t_start:.4f} secunde")
print(f"7. Timp răspuns server (elapsed): {res_time.elapsed.total_seconds():.4f} secunde")

# Exercițiul 8. Când un import eșuează
try:
    import bs4
except ImportError:
    print("8. Instalați modulul cu: pip install beautifulsoup4")