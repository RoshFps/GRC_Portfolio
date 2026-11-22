# KPI and KRI dashboard. Reads the risk register, the SoA and the BIA and
# writes output/kpi-kri.html.
#
# KPIs show how well the security work is going.
# KRIs are warning signs that the risk is getting too high.
# Each one has a target I picked; the page marks it OK or ACTION.
#
# python3 kpi_kri.py [YYYY-MM-DD]

import re
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook

here = Path(__file__).parent
root = here.parent
today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()

register = load_workbook(root / "risk-register" / "saarland-university-risk-register.xlsx")
soa = load_workbook(root / "soa" / "saarland-university-soa.xlsx")["SoA"]
bia = load_workbook(root / "bcm" / "saarland-university-bia.xlsx")

# risk appetite = the High threshold on the Scoring Method sheet
appetite = register["Scoring Method"]["B15"].value

# risks
risks = []
for row in register["Risk Register"].iter_rows(min_row=5, values_only=True):
    if not row[0]:
        break
    due = row[15].date() if isinstance(row[15], datetime) else row[15]
    is_open = row[14] not in ("Closed", "Accepted")
    risks.append({
        "before": row[6] * row[7], "after": row[18] * row[19], "open": is_open,
        "late": (today - due).days if is_open and due < today else 0,
        "controls": re.findall(r"A\.\d+\.\d+", row[11] or ""),
    })
open_risks = [r for r in risks if r["open"]]

# SoA status per control
status = {}
for row in soa.iter_rows(min_row=5, values_only=True):
    if row[0]:
        status[row[0]] = (row[3], row[9])  # applicable, status
applicable = [s for a, s in status.values() if a == "Yes"]

# BIA recovery targets vs what we can do today (peak column)
rto = bia["RTO & RPO"]
rto_target, rpo_target = rto["B7"].value, rto["B9"].value
recovery_now, data_loss_now = rto["B10"].value, rto["B11"].value
actions = [row[6] for row in bia["Actions"].iter_rows(min_row=5, values_only=True) if row[0]]


def pct(part, whole):
    return round(100 * part / whole) if whole else 0


def weak(r):
    # a risk is badly covered if at least half its controls are only Planned or Not implemented
    bad = sum(status.get(c, ("", ""))[1] in ("Planned", "Not implemented") for c in r["controls"])
    return bad * 2 >= len(r["controls"])


# work out the numbers
on_time = pct(sum(not r["late"] for r in open_risks), len(open_risks))
implemented = pct(applicable.count("Implemented"), len(applicable))
in_place = pct(sum(s in ("Implemented", "Partially implemented") for s in applicable), len(applicable))
actions_done = actions.count("Done")
above_before = sum(r["before"] >= appetite for r in open_risks)
above_after = sum(r["after"] >= appetite for r in risks)
late_high = sum(r["before"] >= appetite and r["late"] > 0 for r in risks)
longest_late = max(r["late"] for r in risks)
weak_risks = sum(weak(r) for r in risks)
rto_gap = max(0, recovery_now - rto_target)
rpo_gap = max(0, data_loss_now - rpo_target)

# (name, value, target, ok?)
kpis = [
    ("Open risks with the fix on time", f"{on_time}%", ">= 80%", on_time >= 80),
    ("Applicable controls fully implemented", f"{implemented}%", ">= 50%", implemented >= 50),
    ("Applicable controls at least partly in place", f"{in_place}%", ">= 80%", in_place >= 80),
    ("BIA actions done", f"{actions_done} of {len(actions)}", "all", actions_done == len(actions)),
]
kris = [
    ("Open risks above appetite (before treatment)", above_before, "<= 5", above_before <= 5),
    ("Risks still above appetite after treatment", above_after, "0", above_after == 0),
    ("Overdue fixes on high or critical risks", late_high, "0", late_high == 0),
    ("Longest overdue fix (days)", longest_late, "<= 30", longest_late <= 30),
    ("Risks where half or more of the controls are weak", weak_risks, "<= 2", weak_risks <= 2),
    ("Exam system recovery gap (hours over RTO)", rto_gap, "0", rto_gap == 0),
    ("Exam data loss gap (hours over RPO)", rpo_gap, "0", rpo_gap == 0),
]


def table(rows):
    lines = "".join(f"<tr><td>{n}</td><td>{v}</td><td>{t}</td><td>{'OK' if ok else '<b>ACTION</b>'}</td></tr>"
                    for n, v, t, ok in rows)
    return f"<table><tr><th>Indicator</th><th>Now</th><th>Target</th><th></th></tr>{lines}</table>"


html = f"""<!doctype html>
<meta charset="utf-8">
<title>KPI and KRI dashboard</title>
<style>
body {{ font-family: Arial; max-width: 800px; margin: 20px auto; padding: 0 16px; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border: 1px solid black; padding: 4px 8px; text-align: left; }}
</style>
<h1>KPI and KRI dashboard</h1>
<p>As of {today}. Data from the risk register, the SoA and the BIA.</p>
<h2>KPIs: how the security work is going</h2>
{table(kpis)}
<h2>KRIs: warning signs</h2>
{table(kris)}
"""
(here / "output").mkdir(exist_ok=True)
(here / "output" / "kpi-kri.html").write_text(html)

for name, value, target, ok in kpis + kris:
    print(f"{'OK    ' if ok else 'ACTION'}  {name}: {value} (target {target})")
