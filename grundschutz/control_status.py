# Lists, for every risk in the register, the Annex A controls that treat it
# and their status in the SoA. Writes control-status.txt.
#
# Usage: python3 control_status.py

import re
from pathlib import Path

import openpyxl

WEAK = {"Planned", "Not implemented"}


here = Path(__file__).parent
REGISTER = here.parent / "risk-register" / "saarland-university-risk-register.xlsx"
SOA = here.parent / "soa" / "saarland-university-soa.xlsx"


def main(reg_path=REGISTER, soa_path=SOA, out=here / "control-status.txt"):
    # control -> status, from the SoA sheet (column A and J)
    status = {}
    for r in openpyxl.load_workbook(soa_path)["SoA"].iter_rows(min_row=5, values_only=True):
        if r[0]:
            status[str(r[0]).strip()] = r[9]

    lines = ["Controls behind each risk and their SoA status", "",
             "Made by control_status.py from the risk register and the SoA. Weak means the",
             "control is only Planned or Not implemented.", ""]
    for r in openpyxl.load_workbook(reg_path)["Risk Register"].iter_rows(min_row=5, values_only=True):
        if not r[0]:
            continue
        controls = re.findall(r"A\.\d+\.\d+", r[11] or "")
        weak = sum(status.get(c) in WEAK for c in controls)
        lines.append(f"{r[0]} {r[1]} (L{r[6]} x I{r[7]}), weak {weak} of {len(controls)}")
        for c in controls:
            lines.append(f"    {c:<8} {status.get(c, '?')}")
        lines.append("")

    text = "\n".join(lines)
    with open(out, "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
