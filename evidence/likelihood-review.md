# Likelihood review of the risk register against public data

Reviewed 2026-10-16. For each risk the table compares the likelihood in the register (1 to 5) with what public data shows. "Evidence view" is my judgement from that data; the register itself is unchanged, so scores and the dashboard still match. Evidence files: [incidents.md](incidents.md), [output/kev-summary.md](output/kev-summary.md).

Limits: the KEV catalogue is global and says nothing about Saarland University; the incident counts cover the sector, not the university; EPSS, NVD and BSI/ENISA reports could not be downloaded from this environment (network policy), so they are not used. Where no public data exists the table says so instead of inventing a rate.

| Risk | Register L | Evidence | Evidence view |
|---|---|---|---|
| R01 Ransomware on central IT | 4 | Ransomware-linked KEV entries: 361 of 1,748 (21 %); 67 in edge/remote-access products, 117 in Microsoft products, 17 in virtualisation/file-transfer. Hochschule Hannover reported as ransomware with large parts of IT down (heise headline, 2023). 42 attacks on Hochschulen and research bodies reported to the BKA in 2022 to 2024. | Keep 4. No public incident at Saarland, so not 5. |
| R02 Credential phishing | 5 | No university-specific rate found. Microsoft entries in KEV: 390 (44 added in the last 12 months). | Keep, but the evidence is indirect; 4 would also be defensible. |
| R03 Leak of research data | 3 | Universitätsbibliothek Leipzig: unauthorised access to about 70,000 personal records (Apr 2022). | Keep 3. |
| R04 Lost or stolen laptops | 4 | No public data found. | No evidence either way. |
| R05 Supplier or uplink outage | 2 | No public data found. | No evidence either way. |
| R06 Unpatched institute servers | 4 | 265 edge and 107 web/mail/collaboration entries in KEV; 59 and 20 of them added in the last 12 months. Patch pressure is steady, and decentral servers are the usual gap. | Keep 4. |
| R07 Campus management outage in a peak period | 2 | No public data found. Hannover shows a whole-IT outage is plausible after ransomware, but that is R01. | No evidence either way. |
| R08 Privileged account misuse | 2 | No public data found. | No evidence either way. |
| R09 Accounts not removed | 4 | No public data found. | No evidence either way. |
| R10 Misconfigured file sharing | 3 | No public data found beyond the Leipzig record exposure above. | Keep 3. |
| R11 Espionage on research | 3 | No university-specific data read. | No evidence either way; needs BSI Lagebericht or Verfassungsschutz report. |
| R12 Data-centre fire, water, power | 2 | No public data found. | No evidence either way. |
| R13 DDoS | 3 | FH Münster hit by DDoS twice in January 2022 (KonBriefing). Recorded DDoS of 22.2 Tbps is global (DFN slides). | Keep 3. |
| R14 Insecure in-house software | 3 | KEV has 20 web/collaboration entries added in the last 12 months, but those are third-party products, not in-house code. | No direct evidence. |
| R15 Attacks detected too late | 4 | No public data found. | No evidence either way. |
| R16 Insecure lab and building devices | 3 | 63 KEV entries in D-Link, TP-Link, NETGEAR, QNAP, MikroTik and Mitel products, 16 with known ransomware use. | Keep 3. |
| R17 Loss of key IT staff | 3 | HIS-HE: 3 of the 8 responding science ministries say there is no support for IT staffing questions. | Keep 3. |
| R18 Confidential data into public AI tools | 4 | No public data found. | No evidence either way. |

Result: of 18 likelihoods, 7 are supported or at least not contradicted by public data (R01, R03, R06, R10, R13, R16, R17), R02 is indirect, and 10 have no public evidence. That gap is itself a finding: the register's likelihoods mostly rest on judgement, and the next step is to replace them with the university's own incident and vulnerability-scan data.
