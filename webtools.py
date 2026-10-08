# Laborator: funcții, metode și importuri pe web - Modulul webtools
# Student: Razvan

from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import hashlib
import json
import re
import socket
import ssl
import time
import urllib.parse
import requests

DEFAULT_HEADERS = {"User-Agent": "WebLab-Razvan"}
TIMEOUT = 10


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectuează o cerere GET către URL folosind antetul implicit."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP."""
    try:
        res = fetch(url)
        return res.status_code
    except requests.RequestException:
        return 0


def get_title(html: str) -> str:
    """Extrage și curăță titlul dintr-un șir HTML folosind BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Fără titlu"


def security_headers(url: str) -> Dict[str, bool]:
    """Verifică antetele de securitate ale unui URL."""
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


def score_headers(results: Dict[str, bool]) -> str:
    """Calculează scorul antetelor (ex: '3/5')."""
    passed = sum(1 for status in results.values() if status)
    return f"{passed}/{len(results)}"


def resolve(hostname: str) -> str:
    """Obține adresa IP a gazdei."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "N/A"


def cert_days_left(hostname: str) -> int:
    """Calculează zilele rămase până la expirarea SSL."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = datetime.strptime(
                    cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                ).replace(tzinfo=timezone.utc)
                return (not_after - datetime.now(timezone.utc)).days
    except Exception:
        return -1


def extract_links(html: str) -> list:
    """Extrage toate legăturile href unice dintr-un șir HTML folosind BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    return list(set(links))


def split_links(links: list, domain: str) -> tuple:
    """Separă legăturile în interne și externe."""
    internal, external = set(), set()
    for link in links:
        abs_url = urllib.parse.urljoin(f"https://{domain}", link)
        netloc = urllib.parse.urlparse(abs_url).netloc
        if netloc == domain or netloc == "":
            internal.add(abs_url)
        else:
            external.add(abs_url)
    return list(internal), list(external)


def fetch_robots(base: str) -> Optional[str]:
    """Descarcă fișierul robots.txt."""
    try:
        res = fetch(base.rstrip("/") + "/robots.txt")
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None


def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    """Extrage căile interzise din robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                paths.append(parts[1].strip())
    return paths


def site_report(url: str) -> dict:
    """Generează raportul complet pentru un site web și îl salvează în report.json."""
    res = fetch(url)
    domain = urllib.parse.urlparse(res.url).netloc

    # Redirecționări pornind de la http://
    http_url = f"http://{domain}"
    res_http = requests.get(http_url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    redirect_chain = [f"{r.status_code} -> {r.url}" for r in res_http.history]
    redirect_str = (
        " -> ".join(redirect_chain)
        if redirect_chain
        else "Nicio redirecționare"
    )

    all_links = extract_links(res.text)
    internal, external = split_links(all_links, domain)
    robots = fetch_robots(url)
    disallowed = disallowed_paths(robots)

    report_data = {
        "url_initial": url,
        "url_final": res.url,
        "status_code": res.status_code,
        "titlu": get_title(res.text),
        "ip_address": resolve(domain),
        "redirectionari": redirect_str,
        "scor_securitate": score_headers(security_headers(url)),
        "zile_certificat_ssl": cert_days_left(domain),
        "legaturi_interne": len(internal),
        "legaturi_externe": len(external),
        "cai_interzise": disallowed,
    }

    # Afișare în consolă
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {report_data['status_code']}")
    print(f"Titlu:             {report_data['titlu']}")
    print(f"Adresă IP:         {report_data['ip_address']}")
    print(f"Redirecționări:    {report_data['redirectionari']}")
    print(f"Scor securitate:   {report_data['scor_securitate']}")
    print(f"Certificat:        {report_data['zile_certificat_ssl']} de zile rămase")
    print(
        f"Legături:          {report_data['legaturi_interne']} interne, {report_data['legaturi_externe']} externe"
    )
    print(f"Căi interzise:     {', '.join(report_data['cai_interzise']) if report_data['cai_interzise'] else 'Niciuna'}")

    # Salvare în report.json
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    print("Salvat în report.json")

    return report_data


# Exercițiul 46: Blocul main
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))

    # --- Comparație cu/fără BeautifulSoup ---
# 1. Siguranță: Slicing-ul manual sau RegEx pot eșua la HTML malformat, majuscule sau atribute complexe.
#    BeautifulSoup folosește un parser real care gestionează automat aceste cazuri marginale.
# 2. Concizie: Permite extragerea directă (ex: soup.title.string, soup.find_all("a", href=True)) fără indici sau expresii regulate.