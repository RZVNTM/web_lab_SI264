# Laborator: funcții, metode și importuri pe web
# Student: <Nume Prenume>

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Trimitem cererea principală
response = requests.get(BASE_URL, timeout=TIMEOUT)

# Exercițiul 9. Elementele de bază ale răspunsului
print("9. status_code:", response.status_code)  # Atribut
print("9. ok:", response.ok)                    # Atribut
print("9. url:", response.url)                  # Atribut
print("9. encoding:", response.encoding)        # Atribut

# Exercițiul 10. Tratarea erorilor cu o metodă
response.raise_for_status()  # Nu va face nimic dacă status este 200

try:
    res_404 = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    res_404.raise_for_status()  # Va arunca excepție pentru 404
except requests.HTTPError as err:
    print("10. Eroare HTTP prinsă cu succes:", err)

time.sleep(1)  # Pauză de 1 secundă conform regulilor

# Exercițiul 11. Toate antetele
print("\n--- 11. Antete primite ---")
for key, val in response.headers.items():
    print(f"{key}: {val}")

# Exercițiul 12. Metode de dicționar
server_hdr = response.headers.get("Server", "lipsește")
content_type_hdr = response.headers.get("Content-Type", "lipsește")
content_type_lower = response.headers.get("content-type", "lipsește")
print(f"\n12. Server: {server_hdr} | Content-Type: {content_type_hdr}")
print("12. Căutare cu litere mici ('content-type'):", content_type_lower)
# Observație: 'response.headers' ignoră majusculele/minusculele.

# Exercițiul 13. Înlănțuirea metodelor de șir
cyber_count = response.text.lower().count("cyber")
print("\n13. Apariții ale cuvântului 'cyber':", cyber_count)
# Explicație: .lower() returnează un nou șir de caractere, deci putem apela .count() direct pe el.

# Exercițiul 14. Găsirea titlului
html_text = response.text
start = html_text.find("<title>") + len("<title>")
end = html_text.find("</title>")
if start != -1 and end != -1:
    title = html_text[start:end].strip()
else:
    title = "Fără titlu"
print("14. Titlul paginii este:", title)

# Exercițiul 15. Numărarea liniilor
lines = html_text.splitlines()
print(f"15. Număr total de linii: {len(lines)}")
if lines:
    longest_line = max(lines, key=len)
    print("15. Lungimea celei mai lungi linii:", len(longest_line))

# Exercițiul 16. Verificarea HTTPS
if response.url.startswith("https://"):
    print("16. Conexiune securizată")
else:
    print("16. Conexiune nesecurizată")

# Exercițiul 17. Urmărirea redirecționărilor
res_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
print("\n17. Istoric redirecționări:")
for r in res_http.history:
    print(f" -> Code: {r.status_code} | URL: {r.url}")
print(f"17. URL final: {res_http.url}")

time.sleep(1)

# Exercițiul 18. HEAD versus GET
res_head = requests.head(BASE_URL, timeout=TIMEOUT)
res_get = requests.get(BASE_URL, timeout=TIMEOUT)
print(f"\n18. Lungime conținut HEAD: {len(res_head.content)} | GET: {len(res_get.content)}")
# Explicație: Cererea HEAD descarcă doar antetele (fără corpul paginii), deci lungimea conținutului este 0.

time.sleep(1)

# Exercițiul 19. Cookie-uri
if response.cookies:
    for cookie in response.cookies:
        print(f"19. Cookie: {cookie.name}, Secure: {cookie.secure}")
else:
    print("\n19. Niciun cookie setat")

# Exercițiul 20. Sesiuni
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Razvan"})
res_echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("\n20. Rezultat antete trimise în sesiune:")
print(res_echo.json())

# Verificați-vă:
# response.text este un ATRIBUT (o valoare stocată direct în obiect),
# în timp ce response.json() este o METODĂ (o funcție care execută analizarea/parsarea datelor JSON).