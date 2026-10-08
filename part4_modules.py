# Laborator: funcții, metode și importuri pe web
# Student: Razvan

from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
import re
import socket
import ssl
import urllib.parse
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10  # secunde


# Exercițiul 35: Descompunerea unui URL
def parse_url_demo(url: str):
    """Descompune un URL în componentele sale principale."""
    parsed = urllib.parse.urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment,
    }


# Exercițiul 36: Compunerea URL-urilor
def resolve_relative_urls(base: str, relatives: list) -> list:
    """Transformă legăturile relative în URL-uri absolute."""
    return [urllib.parse.urljoin(base, rel) for rel in relatives]


# Exercițiul 37: Extragerea legăturilor cu RegEx
def extract_links(html: str) -> list:
    """Extrage toate legăturile href dintr-un șir HTML fără duplicate."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))


# Exercițiul 38: Interne sau externe?
def split_links(links: list, domain: str) -> tuple:
    """Separă o listă de legături în interne și externe domeniului specificat."""
    internal = set()
    external = set()
    for link in links:
        abs_url = urllib.parse.urljoin(f"https://{domain}", link)
        netloc = urllib.parse.urlparse(abs_url).netloc
        if netloc == domain or netloc == "":
            internal.add(abs_url)
        else:
            external.add(abs_url)
    return list(internal), list(external)


# Exercițiul 39: Propriile metode (Parser HTML pentru imagini)
class ImageFinder(HTMLParser):
    """Clasă pentru colectarea atributului src al fiecărui tag <img>."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src")
            if src:
                self.images.append(src)


# Exercițiul 40: Amprenta paginii
def page_fingerprint(url: str) -> str:
    """Calculează amprenta SHA-256 a conținutului paginii."""
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()


# Exercițiul 41: Salvarea și încărcarea din JSON
def save_and_load_headers(url: str, filename: str = "headers.json") -> dict:
    """Salvează antetele paginii în JSON și le citește înapoi."""
    res = requests.get(url, timeout=TIMEOUT)
    headers_dict = dict(res.headers)

    # Salvare în fișier
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(headers_dict, f, indent=2)

    # Încărcare din fișier
    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    return loaded


# Exercițiul 42: Interogare DNS
def resolve(hostname: str) -> str:
    """Returnează adresa IP a numelui de gazdă specificat."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "N/A"


# Exercițiul 43: Expirarea certificatului SSL
def cert_days_left(hostname: str) -> int:
    """Se conectează la portul 443 și calculează câte zile mai sunt până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert["notAfter"]
                # Conversie dată
                not_after = datetime.strptime(
                    not_after_str, "%b %d %H:%M:%S %Y %Z"
                ).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                days_left = (not_after - now).days
                return days_left
    except Exception:
        return -1


# --- Executarea testelor ---
if __name__ == "__main__":
    print("=== Testare Partea 4 ===")

    # Ex 35
    parsed_info = parse_url_demo("https://cybercor.org/path?x=1#top")
    print("35. Componente URL:", parsed_info)

    # Ex 36
    resolved = resolve_relative_urls(BASE_URL, ["/about", "contact.html", "../index.html"])
    print("\n36. URL-uri absolute:", resolved)

    # Ex 37 & 38
    res = requests.get(BASE_URL, timeout=TIMEOUT)
    all_links = extract_links(res.text)
    domain_name = urllib.parse.urlparse(BASE_URL).netloc
    internal_links, external_links = split_links(all_links, domain_name)
    print(
        f"\n37/38. Legături găsite: Total {len(all_links)} | Interne: {len(internal_links)} | Externe: {len(external_links)}"
    )

    # Ex 39 Testare parser HTML cu verificare assert conform instrucțiunilor
    test_html = """
    <html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fără src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
    finder = ImageFinder()
    finder.feed(test_html)
    print("\n39. Test ImageFinder cu HTML local:", finder.images)
    assert finder.images == [
        "/logo.png",
        "poza.jpg",
        "https://cdn.example.com/banner.webp",
    ], "Testul pe parser a eșuat"
    print("39. Testul pe parser a trecut cu succes!")

    # Ex 40
    print("\n40. Hash SHA-256 al paginii:", page_fingerprint(BASE_URL))

    # Ex 41
    headers_loaded = save_and_load_headers(BASE_URL)
    print("\n41. Antet din JSON salvat (Server):", headers_loaded.get("Server"))

    # Ex 42
    ip_addr = resolve(domain_name)
    print(f"\n42. Adresa IP pentru {domain_name}:", ip_addr)

    # Ex 43
    days = cert_days_left(domain_name)
    print(f"\n43. Zile rămase până la expirarea certificatului SSL:", days)

# În exercițiul 39, metoda handle_starttag() este apelată automat de metoda internă .feed() a clasei HTMLParser,
