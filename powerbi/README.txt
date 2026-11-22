Power BI risk dashboard

The same 18 risks as the register, as a Power BI project (.pbip). The data is
inside the model, so there is nothing to connect.

Open risk-dashboard.pbip in Power BI Desktop (Windows). If it says the format
isn't supported, turn on these preview features under File > Options and
settings > Options and restart: "Power BI Project (.pbip) save option", "Store
semantic model using TMDL format" and "Store reports using enhanced metadata
format (PBIR)".

What's in it
- risk-dashboard.SemanticModel: the Risk table plus the calculated columns and
  measures (open risks, late fixes, danger before and after fixes, and so on).
- risk-dashboard.Report: one page with KPI cards, two heatmaps (before and
  after fixes), owners, the late-fixes table and slicers.

The heatmap cells use the same four rating colours as the Excel register
(measures Heat Colour and Heat Colour After). If they don't show, select the
matrix, then Format > Cell elements > Background colour > fx > Field value >
Heat Colour.

Late fixes use TODAY(), so the number changes with the date you open it.
