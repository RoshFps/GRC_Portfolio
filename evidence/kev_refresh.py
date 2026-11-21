# Downloads the CISA Known Exploited Vulnerabilities (KEV) list and counts the
# entries for vendors a university is likely to use. Writes output/kev-summary.txt.
#
# python3 kev_refresh.py
#
# KEV is a global list, so this gives context for the likelihood scores. It
# doesn't measure Saarland University.

import json
import urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

URLS = [
    "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
    "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json",
]

# my own grouping: vendor group -> (register risks, vendors)
GROUPS = {
    "Edge and VPN": ("R01, R06, R16", ["Fortinet", "Ivanti", "Citrix", "Palo Alto Networks", "SonicWall",
                                       "Cisco", "F5", "Juniper", "Check Point", "Zyxel"]),
    "Microsoft": ("R01, R02, R08", ["Microsoft"]),
    "Virtualisation and file transfer": ("R01, R12", ["VMware", "Progress", "Veeam"]),
    "Web, mail and collaboration": ("R06, R14", ["Apache", "Atlassian", "Roundcube", "Synacor", "Zimbra",
                                                 "WordPress", "Jenkins", "GitLab", "PaperCut"]),
    "IoT and network devices": ("R16", ["D-Link", "TP-Link", "NETGEAR", "QNAP", "MikroTik", "Mitel"]),
}

# try cisa.gov first, then the GitHub mirror
for url in URLS:
    try:
        data = json.load(urllib.request.urlopen(url, timeout=60))
        break
    except Exception as e:
        print("could not get", url, e)

vulns = data["vulnerabilities"]
ransom = [v for v in vulns if v["knownRansomwareCampaignUse"] == "Known"]
year_ago = (date.today() - timedelta(days=365)).isoformat()

lines = [
    "CISA KEV summary",
    "",
    f"Downloaded {date.today()} from {url}",
    f"Catalogue version {data['catalogVersion']}",
    "",
    f"Entries: {len(vulns)}",
    f"Used by ransomware: {len(ransom)} ({len(ransom) / len(vulns):.0%})",
    "",
    "Added per year (all / ransomware):",
]
per_year = Counter(v["dateAdded"][:4] for v in vulns)
ransom_per_year = Counter(v["dateAdded"][:4] for v in ransom)
for year in sorted(per_year):
    lines.append(f"  {year}  {per_year[year]} / {ransom_per_year[year]}")

lines += ["", "Vendor groups (entries / added in the last 12 months / ransomware):"]
for name, (risks, vendors) in GROUPS.items():
    group = [v for v in vulns if v["vendorProject"] in vendors]
    recent = sum(v["dateAdded"] >= year_ago for v in group)
    used = sum(v["knownRansomwareCampaignUse"] == "Known" for v in group)
    lines.append(f"  {name} ({risks}): {len(group)} / {recent} / {used}")

top = Counter(v["vendorProject"] for v in vulns).most_common(10)
lines += ["", "Top 10 vendors: " + ", ".join(f"{k} {n}" for k, n in top), ""]

Path("output").mkdir(exist_ok=True)
Path("output/kev-summary.txt").write_text("\n".join(lines))
print("\n".join(lines))
