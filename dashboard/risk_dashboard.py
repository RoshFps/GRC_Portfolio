# Risk dashboard: reads the risk register and makes 3 charts and an HTML page.
# Scores, rating bands and the risk appetite all come from the workbook, so
# after editing the register just run it again.
#
# python3 risk_dashboard.py [YYYY-MM-DD]
#
# The date is used for the overdue check (default: today).

import sys
from datetime import date, datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import load_workbook

here = Path(__file__).parent
register = here.parent / "risk-register" / "saarland-university-risk-register.xlsx"
today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
out = here / "output"
out.mkdir(exist_ok=True)

COLOURS = {"Low": "#C6EFCE", "Medium": "#FFE699", "High": "#F4B183", "Critical": "#C00000"}


wb = load_workbook(register)

# rating bands from the Scoring Method sheet, e.g. Low 1, Medium 5, High 10, Critical 15
bands = [(r[0], r[1]) for r in wb["Scoring Method"].iter_rows(min_row=13, max_row=16, max_col=2, values_only=True)]
appetite = dict(bands)["High"]  # residual score must stay below High


def rating(score):
    name = bands[0][0]
    for band, minimum in bands:
        if score >= minimum:
            name = band
    return name


# risks from the Risk Register sheet (data starts in row 5)
risks = []
for row in wb["Risk Register"].iter_rows(min_row=5, values_only=True):
    if not row[0]:
        break
    due = row[15].date() if isinstance(row[15], datetime) else row[15]
    is_open = row[14] not in ("Closed", "Accepted")
    risks.append({
        "id": row[0], "title": row[1], "owner": row[5].replace("Chief Information Security Officer (CISO)", "CISO"),
        "before": row[6] * row[7], "after": row[18] * row[19],
        "pos_before": (row[6], row[7]), "pos_after": (row[18], row[19]),
        "due": due, "open": is_open,
        "late": (today - due).days if is_open and due < today else 0,
    })

# 1. heatmap, before and after treatment
fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
for ax, key, title in [(axes[0], "pos_before", "Before treatment"), (axes[1], "pos_after", "After treatment")]:
    for l in range(1, 6):
        for i in range(1, 6):
            ax.add_patch(plt.Rectangle((i - 0.5, l - 0.5), 1, 1, color=COLOURS[rating(l * i)], ec="black"))
            ids = [r["id"] for r in risks if r[key] == (l, i)]
            text = "\n".join(" ".join(ids[k:k + 2]) for k in range(0, len(ids), 2))
            ax.text(i, l, text, ha="center", va="center", fontsize=7,
                    color="white" if rating(l * i) == "Critical" else "black")
    ax.set(xlim=(0.5, 5.5), ylim=(0.5, 5.5), xlabel="Impact", ylabel="Likelihood", title=title)
    ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(out / "heatmap.png", dpi=150)

# 2. score before and after treatment, one line per risk
risks.sort(key=lambda r: r["before"])
fig, ax = plt.subplots(figsize=(7, 6))
for y, r in enumerate(risks):
    ax.plot([r["after"], r["before"]], [y, y], color="black", lw=0.8)
    ax.plot(r["before"], y, "o", mfc="white", mec="black")
    ax.plot(r["after"], y, "o", color="black")
ax.axvline(appetite - 0.5, color="black", ls="--", lw=0.8)
ax.set_yticks(range(len(risks)), [r["id"] for r in risks])
ax.set_xlabel("Score (white = before, black = after, dashed line = risk appetite)")
fig.tight_layout()
fig.savefig(out / "movement.png", dpi=150)

# 3. open risks per owner
owners = {}
for r in risks:
    owners[r["owner"]] = owners.get(r["owner"], 0) + r["open"]
fig, ax = plt.subplots(figsize=(9, 3))
ax.barh(list(owners), list(owners.values()), color="black")
ax.set_xlabel("Open risks")
fig.tight_layout()
fig.savefig(out / "owners.png", dpi=150)

# 4. html page
late = sorted([r for r in risks if r["late"]], key=lambda r: -r["late"])
kpis = [("Risks", len(risks)),
        ("Open", sum(r["open"] for r in risks)),
        ("Overdue", len(late)),
        ("High or critical before", sum(r["before"] >= appetite for r in risks)),
        ("High or critical after", sum(r["after"] >= appetite for r in risks))]
kpi_rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in kpis)
late_rows = "".join(f"<tr><td>{r['id']}</td><td>{r['title']}</td><td>{r['owner']}</td>"
                    f"<td>{r['due']}</td><td>{r['late']}</td></tr>" for r in late)

html = f"""<!doctype html>
<meta charset="utf-8">
<title>Risk dashboard</title>
<style>
body {{ font-family: Arial; max-width: 900px; margin: 20px auto; padding: 0 16px; }}
img {{ width: 100%; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid black; padding: 4px 8px; text-align: left; }}
</style>
<h1>Risk dashboard</h1>
<p>As of {today}. Source: {register.name}</p>
<table>{kpi_rows}</table>
<h2>Heatmap</h2>
<img src="heatmap.png">
<h2>Before and after treatment</h2>
<img src="movement.png">
<h2>Open risks per owner</h2>
<img src="owners.png">
<h2>Overdue fixes</h2>
<table><tr><th>ID</th><th>Risk</th><th>Owner</th><th>Due</th><th>Days late</th></tr>{late_rows}</table>
"""
(out / "risk-dashboard.html").write_text(html)
print(f"{len(risks)} risks, {kpis[1][1]} open, {len(late)} overdue on {today}")
