# Mapping the risk register to BSI IT-Grundschutz and German public-sector rules

Replaces the TISAX/VDA ISA mapping from the original plan. TISAX is an automotive assessment scheme and does not fit a public university. For a German university the frameworks that actually apply or are used are:

- **BSI IT-Grundschutz** (BSI-Standard 200-2 and the Kompendium). The HIS-HE study 3/2025 reports that Hamburg requires its Hochschulen to follow IT-Grundschutz (p. 25) and that Bavaria obliges them to run an ISMS under the Hochschul-Informationssicherheitsprogramm (p. 17).
- **Saarland Informationssicherheitsgesetz (IT-SiG SL)**, dated 15 May 2019 (Amtsblatt I Nr. 35 of 12 Sept 2019, p. 653). § 3 requires "angemessene technische und organisatorische Maßnahmen" and information security concepts, and § 3 Abs. 2 requires authorities to inform the central IT service provider of the Land without delay about information relevant to averting security risks. **Open point:** the excerpt I could read does not say whether Universität des Saarlandes counts as a covered body (§ 1 covers authorities and "sonstige der Aufsicht des Landes unterstehende juristische Personen des öffentlichen Rechts"). Check the full text before relying on it.
- **NIS2 (Directive (EU) 2022/2555)**. Per HIS-HE (pp. 6 to 8) it needs national implementation, research institutions are defined so that educational institutions are excluded, and on 3 Nov 2023 the IT-Planungsrat asked the Länder and the Bund not to extend the scope to educational institutions. So a Hochschule is not clearly in scope; this is stated as an open question, not a conclusion. The study text I could read predates any later change in German law, which I did not check.

## How to read the table

Module IDs and titles come from the BSI IT-Grundschutz Kompendium (2023 edition). The IDs ISMS.1, ORP.1 to ORP.5, CON.1 to CON.3, CON.6, OPS.1.1.2 to OPS.1.1.5, DER.1, DER.2.1, DER.4, APP.3.1, SYS.1.1, SYS.2.1, NET.1.1, NET.1.2, INF.1 and INF.2 were checked against a public listing (opensecurityarchitecture.org). The others (SYS.3.1, SYS.3.2.x, SYS.4.4, SYS.1.5, OPS.2.2, OPS.2.3, CON.8, NET.3.2, NET.3.3, APP.5.3, DER.3.1) are from my knowledge of the Kompendium; bsi.bund.de could not be reached from this environment, so check them against the official PDF before publishing. The mapping is my own judgement of which modules address each risk, not an official crosswalk. ISO 27001 controls are the ones already linked in the register.

| Risk | Grundschutz modules | Why |
|---|---|---|
| R01 Ransomware on central IT | OPS.1.1.4 Schutz vor Schadprogrammen; CON.3 Datensicherungskonzept; DER.2.1 Behandlung von Sicherheitsvorfällen; DER.4 Notfallmanagement; OPS.1.1.3 Patch- und Änderungsmanagement | Malware protection, offline backups, incident handling and restart planning are the controls against encryption of core systems. |
| R02 Credential phishing | ORP.3 Sensibilisierung und Schulung; ORP.4 Identitäts- und Berechtigungsmanagement; APP.5.3 Allgemeiner E-Mail-Client und -Server | Awareness, strong authentication and mail filtering. |
| R03 Leak of research data | CON.2 Datenschutz; CON.1 Kryptokonzept; ORP.4 Identitäts- und Berechtigungsmanagement; CON.6 Löschen und Vernichten | Classification of personal data, encryption, access, deletion. |
| R04 Lost or stolen laptops | SYS.3.1 Laptops; SYS.2.1 Allgemeiner Client; CON.1 Kryptokonzept; CON.7 Informationssicherheit auf Auslandsreisen | Device hardening, disk encryption, travel rules. |
| R05 Supplier or uplink outage | OPS.2.3 Nutzung von Outsourcing; OPS.2.2 Cloud-Nutzung; NET.1.1 Netzarchitektur und -design; DER.4 Notfallmanagement | Supplier contracts, redundancy in the network design, continuity plans. |
| R06 Unpatched institute servers | OPS.1.1.3 Patch- und Änderungsmanagement; SYS.1.1 Allgemeiner Server; ISMS.1 Sicherheitsmanagement; OPS.1.1.2 Ordnungsgemäße IT-Administration | Asset inventory and patch process for decentral servers. |
| R07 Campus management outage | DER.4 Notfallmanagement; SYS.1.1 Allgemeiner Server; SYS.1.5 Virtualisierung; INF.2 Rechenzentrum | Redundancy and recovery of the exam registration system (see bcm/). |
| R08 Privileged account misuse | OPS.1.1.2 Ordnungsgemäße IT-Administration; ORP.4 Identitäts- und Berechtigungsmanagement; OPS.1.1.5 Protokollierung | Separation of admin accounts, least privilege, logging of admin actions. |
| R09 Accounts not removed | ORP.4 Identitäts- und Berechtigungsmanagement; ORP.2 Personal | Joiner-mover-leaver process linked to HR and student records. |
| R10 Misconfigured file sharing | CON.2 Datenschutz; OPS.2.2 Cloud-Nutzung; ORP.4 Identitäts- und Berechtigungsmanagement | Sharing rules for cloud and file shares. |
| R11 Espionage on research | ISMS.1 Sicherheitsmanagement; DER.1 Detektion von sicherheitsrelevanten Ereignissen; NET.1.1 Netzarchitektur und -design | Segmentation of lab networks, detection, protection of research data. |
| R12 Data-centre fire, water, power | INF.2 Rechenzentrum; INF.1 Allgemeines Gebäude; CON.3 Datensicherungskonzept | Physical protection and off-site backups. |
| R13 DDoS | NET.1.1 Netzarchitektur und -design; NET.3.2 Firewall; DER.2.1 Behandlung von Sicherheitsvorfällen | Capacity, filtering at the uplink, incident process. |
| R14 Insecure in-house software | CON.8 Software-Entwicklung; APP.3.1 Webanwendungen und Webservices; OPS.1.1.6 Software-Tests und -Freigaben | Secure development rules and testing. |
| R15 Attacks detected too late | DER.1 Detektion von sicherheitsrelevanten Ereignissen; OPS.1.1.5 Protokollierung; DER.2.1 Behandlung von Sicherheitsvorfällen | Central logs, detection and an incident process. |
| R16 Insecure lab and building devices | SYS.4.4 Allgemeines IoT-Gerät; NET.1.1 Netzarchitektur und -design; OPS.1.1.3 Patch- und Änderungsmanagement | Network segregation and patching of embedded devices. |
| R17 Loss of key IT staff | ORP.1 Organisation; OPS.1.1.2 Ordnungsgemäße IT-Administration; ORP.2 Personal | Documentation, deputies, onboarding. |
| R18 Data into public AI tools | ORP.1 Organisation; CON.2 Datenschutz; ORP.3 Sensibilisierung und Schulung | Usage rules, data protection review, awareness. |

## Coverage

Every one of the 18 risks maps to at least two Grundschutz modules. The modules used most often are ORP.4 (5 risks), NET.1.1 (4), DER.2.1, DER.4, OPS.1.1.3, CON.2 and OPS.1.1.2 (3 each).

## Next steps

1. Read the full IT-SiG SL text and settle whether the university is a covered body, and what the reporting duty to the central IT service provider means for the incident process in `bcm/continuity-plan.md`.
2. Check module titles against the official Kompendium PDF.
3. Do a basic check (Basis-Absicherung) of the SoA statuses against the module requirements for the most frequent modules.
