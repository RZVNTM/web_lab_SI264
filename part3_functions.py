# Laborator: funcții, metode și importuri pe web
# Student: Razvan

from typing import Dict, List, Optional
import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# Exercițiul 21 & 23: Prima funcție cu parametru implicit
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectuează o cerere GET către URL-ul specificat și returnează obiectul răspuns."""
    return requests.get(url, timeout=timeout)


# Exercițiul 22 & 26: Returnarea unei singure valori și adnotări de tip
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code


# Exercițiul 24 & 25: O singură sarcină pe funcție și Docstring
def get_title(html: str) -> str:
    """Extrage și curăță titlul dintr-un șir de caractere HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return "Fără titlu"


# Exercițiul 27: Fără opriri neașteptate
def page_exists(url: str) -> bool:
    """Verifică dacă o pagină există fără a opri programul la erori de rețea."""
    try:
        response = fetch(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


# Exercițiul 28: Returnarea unui dicționar
def check_paths(base: str, paths: List[str]) -> Dict[str, int]:
    """Verifică o listă de căi pe un domeniu și returnează un dicționar {cale: status}."""
    results = {}
    for path in paths:
        full_url = base.rstrip("/") + "/" + path.lstrip("/")
        try:
            res = fetch(full_url)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = 0
        time.sleep(1)  # Pauză între cereri conform regulilor
    return results


# Exercițiul 29: Argumente cu nume
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui singur antet specificat din răspuns."""
    try:
        res = fetch(url)
        return res.headers.get(name, default)
    except requests.RequestException:
        return default


# Exercițiul 30: Antete de securitate
def security_headers(url: str) -> Dict[str, bool]:
    """Verifică prezența a 5 antete esențiale de securitate."""
    sec_list = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    try:
        res = fetch(url)
        return {h: h in res.headers for h in sec_list}
    except requests.RequestException:
        return {h: False for h in sec_list}


# Exercițiul 31: Funcții care apelează funcții
def score_headers(results: Dict[str, bool]) -> str:
    """Returnează scorul antetelor de securitate sub formă de text (ex: '3/5')."""
    passed = sum(1 for status in results.values() if status)
    total = len(results)
    return f"{passed}/{total}"


# Exercițiul 32: Două funcții, o sarcină (robots.txt)
def fetch_robots(base: str) -> Optional[str]:
    """Descarcă conținutul fișierului robots.txt sau returnează None dacă nu există."""
    url = base.rstrip("/") + "/robots.txt"
    try:
        res = fetch(url)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None


def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    """Extrage toate căile interzise (Disallow) din textul fișierului robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                path = parts[1].strip()
                if path:
                    paths.append(path)
    return paths


# Exercițiul 33: Oricâte argumente (*urls)
def response_times(*urls: str) -> Dict[str, float]:
    """Măsoară timpul de răspuns pentru oricâte URL-uri primite ca argumente."""
    results = {}
    for url in urls:
        t0 = time.perf_counter()
        try:
            fetch(url)
            dur = time.perf_counter() - t0
            results[url] = round(dur, 4)
        except requests.RequestException:
            results[url] = -1.0
        time.sleep(1)
    return results


# Exercițiul 34: Argumente cu nume colectate (**details)
def log(message: str, **details) -> None:
    """Afișează un mesaj de logare urmat de detaliile primite ca argumente cu nume."""
    formatted_details = " | ".join([f"{k}={v}" for k, v in details.items()])
    if formatted_details:
        print(f"{message} | {formatted_details}")
    else:
        print(message)


# --- Executarea testelor ---
if __name__ == "__main__":
    print("=== Testare Partea 3 ===")

    # Ex 21 & 22
    print("21/22. Status BASE_URL:", get_status(BASE_URL))
    time.sleep(1)

    # Ex 24 & 25
    res = fetch(BASE_URL)
    title = get_title(res.text)
    print("24/25. Titlu extras:", title)
    print("\n--- Docstring get_title ---")
    print(get_title.__doc__)

    # Ex 27
    print("\n27. Există domeniul fictiv?:", page_exists("https://this-domain-does-not-exist.invalid"))

    # Ex 28
    paths_res = check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"])
    print("\n28. Verificare căi:", paths_res)

    # Ex 29
    server_hdr = get_header(BASE_URL, name="Server")
    print("\n29. Antet Server:", server_hdr)

    # Ex 30 & 31
    sec_hdrs = security_headers(BASE_URL)
    score = score_headers(sec_hdrs)
    print("\n30/31. Scor antete securitate:", score)

    # Ex 32
    robots = fetch_robots(BASE_URL)
    disallowed = disallowed_paths(robots)
    print("\n32. Căi interzise din robots.txt:", disallowed)

    # Ex 33
    times = response_times(BASE_URL, ECHO_URL)
    print("\n33. Timpi de răspuns:", times)

    # Ex 34
    print("\n34. Test funcție de log:")
    log("verificat", url=BASE_URL, status=200)

# Verificați-vă:
# print() doar afișează valoarea pe ecran, fără ca aceasta să poată fi salvată sau prelucrată mai departe.
# return trimite valoarea înapoi acolo unde a fost apelată funcția, permițând stocarea ei într-o variabilă.