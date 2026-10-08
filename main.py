# Laborator: funcții, metode și importuri pe web - Fișierul principal
# Student: Razvan

import argparse
import csv
from datetime import datetime
import webtools


def main():
    parser = argparse.ArgumentParser(description="Generează raport web.")
    parser.add_argument(
        "url",
        nargs="?",
        default="https://cybercor.org",
        help="URL-ul de analizat",
    )
    args = parser.parse_args()

    url = args.url

    # Exercițiul 49: Raport CSV
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    with open("report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        for p in paths_to_check:
            full_url = url.rstrip("/") + "/" + p.lstrip("/")
            st = webtools.get_status(full_url)
            now_iso = datetime.now().isoformat()
            writer.writerow([p, st, now_iso])

    # Exercițiul 50: Proiect final
    webtools.site_report(url)


if __name__ == "__main__":
    main()