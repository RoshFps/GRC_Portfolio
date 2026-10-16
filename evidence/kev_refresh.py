#!/usr/bin/env python3
"""Pull the CISA Known Exploited Vulnerabilities (KEV) catalogue and summarise
what it says about the technology a university runs.

Standard library only. Usage:
    python3 kev_refresh.py [--out output] [--file kev.json]

Writes output/kev-summary.json (machine readable) and output/kev-summary.md.
The catalogue is global and not specific to universities, so the numbers are
context for likelihood scoring, not a measurement of Saarland University.
"""
import argparse
import collections
import datetime as dt
import json
import pathlib
import sys
import urllib.request

SOURCES = [
    "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
    "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json",
]

# Vendor groups mapped to register risks. Judgement call, documented in
# likelihood-review.md: which vendors a German university plausibly runs.
GROUPS = {
    "Edge and remote access (VPN, firewall, gateway)": {
        "risks": "R01, R06, R16",
        "vendors": ["Fortinet", "Ivanti", "Citrix", "Palo Alto Networks", "SonicWall",
                    "Cisco", "F5", "Juniper", "Check Point", "Zyxel"],
    },
    "Windows, Office and Exchange (Microsoft)": {
        "risks": "R01, R02, R08",
        "vendors": ["Microsoft"],
    },
    "Virtualisation and backup/file transfer": {
        "risks": "R01, R12",
        "vendors": ["VMware", "Progress", "Veeam"],
    },
    "Web, mail and collaboration servers": {
        "risks": "R06, R14",
        "vendors": ["Apache", "Atlassian", "Roundcube", "Synacor", "Zimbra", "WordPress",
                    "Jenkins", "GitLab", "PaperCut"],
    },
    "Printers, cameras and IoT devices": {
        "risks": "R16",
        "vendors": ["D-Link", "TP-Link", "NETGEAR", "QNAP", "MikroTik", "Mitel"],
    },
}


def load(path=None):
    if path:
        return json.loads(pathlib.Path(path).read_text()), str(path)
    last = None
    for url in SOURCES:
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r), url
        except Exception as e:  # try the next mirror
            last = e
    sys.exit(f"could not download KEV: {last}")


def summarise(data, source):
    v = data["vulnerabilities"]
    today = dt.date.today().isoformat()
    by_year = collections.Counter(x["dateAdded"][:4] for x in v)
    ransom = [x for x in v if x["knownRansomwareCampaignUse"] == "Known"]
    ransom_year = collections.Counter(x["dateAdded"][:4] for x in ransom)
    vendors = collections.Counter(x["vendorProject"] for x in v)
    groups = {}
    for name, g in GROUPS.items():
        sel = [x for x in v if x["vendorProject"] in g["vendors"]]
        last12 = [x for x in sel if x["dateAdded"] >= (dt.date.today() - dt.timedelta(days=365)).isoformat()]
        groups[name] = {
            "risks": g["risks"],
            "vendors": g["vendors"],
            "entries": len(sel),
            "added_last_12_months": len(last12),
            "known_ransomware_use": sum(x["knownRansomwareCampaignUse"] == "Known" for x in sel),
        }
    return {
        "retrieved": today,
        "source": source,
        "catalogue_version": data.get("catalogVersion"),
        "date_released": data.get("dateReleased"),
        "total": len(v),
        "known_ransomware_use": len(ransom),
        "added_by_year": dict(sorted(by_year.items())),
        "ransomware_by_year_added": dict(sorted(ransom_year.items())),
        "top_vendors": vendors.most_common(15),
        "groups": groups,
    }


def markdown(s):
    L = [f"# CISA KEV summary", "",
         f"Retrieved {s['retrieved']} from {s['source']}. Catalogue version {s['catalogue_version']}, "
         f"released {s['date_released']}.", "",
         "The catalogue is global and not specific to universities. It lists vulnerabilities with "
         "evidence of active exploitation, so it supports the *likelihood* column of the risk register "
         "but does not measure Saarland University.", "",
         f"- Entries: **{s['total']}**; with known use in ransomware campaigns: "
         f"**{s['known_ransomware_use']}** ({s['known_ransomware_use']/s['total']:.0%}).", "",
         "| Year added | Entries | Of which known ransomware use |", "|---|---|---|"]
    for y, n in s["added_by_year"].items():
        L.append(f"| {y} | {n} | {s['ransomware_by_year_added'].get(y, 0)} |")
    L += ["", "| Technology group | Register risks | Entries | Added last 12 months | Known ransomware use |",
          "|---|---|---|---|---|"]
    for n, g in s["groups"].items():
        L.append(f"| {n} ({', '.join(g['vendors'])}) | {g['risks']} | {g['entries']} | "
                 f"{g['added_last_12_months']} | {g['known_ransomware_use']} |")
    L += ["", "Top vendors by number of entries: " + ", ".join(f"{k} {n}" for k, n in s["top_vendors"]) + ".", ""]
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="output")
    ap.add_argument("--file", help="use a local KEV json instead of downloading")
    a = ap.parse_args()
    data, src = load(a.file)
    s = summarise(data, src)
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "kev-summary.json").write_text(json.dumps(s, indent=2) + "\n")
    (out / "kev-summary.md").write_text(markdown(s))
    print(markdown(s))
