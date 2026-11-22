GRC Portfolio

My GRC project. I built the main ISMS (ISO 27001) and business continuity
documents for my own university, Saarland University. The public facts are
real and sourced from the internet; the risks, scores, owners and dates are made up.

Folders
  risk-register/  18 risks with scores, owners, controls and fixes
  soa/            Statement of Applicability, all 93 Annex A controls
  bcm/            BIA, continuity plan and tabletop exercise for exam registration
  dashboard/      risk dashboard and KPI/KRI page
  powerbi/        the dashboard in Power BI
  evidence/       public data behind the likelihood scores
  grundschutz/    risks mapped to BSI IT-Grundschutz

Run
  pip install openpyxl matplotlib
  python3 risk-register/build_register.py
  python3 soa/build_soa.py
  python3 bcm/build_bia.py
  python3 dashboard/risk_dashboard.py
  python3 dashboard/kpi_kri.py
  python3 grundschutz/control_status.py
  cd evidence && python3 kev_refresh.py

Start with the register; the other scripts read from it.
