# MOSS 2026 Chicago — assembled trip `trip_a_chicago`

_Conference in Chicago — ordinary trip with a handful of traps_

- traveler: Changhong Zhang (staff), funding Non-Grant
- Chicago, Illinois, 2026-08-10 + 4 days
- 27 files, 23 expected lines, 5 skips, 6 required flags; expected total of the USD-currency lines 3541.79; of all lines (foreign-currency lines at their approximate USD) 3541.79; per-diem lines not included

| situation | files | expected | provisions |
|---|---|---|---|
| `AIR-COACH-DIRECT` #0 | `American Airlines DCA-ORD receipt.pdf` | line 501.40 USD | AIR-COACH (p.9); AIR-LOWEST (p.10); DOC-75 (p.12, p.24) |
| `AIR-BAG` #0 | `American Airlines checked bag receipt.pdf` | line 35.00 USD | AIR-ANCILLARY-OK (p.10) |
| `AIR-SEAT-ECONOMY` #0 | `American Airlines seat assignment receipt.pdf` | line 34.00 USD; flag (seat) | AIR-ANCILLARY-OK (p.10); AIR-ANCILLARY-NO (p.10, App. B p.30) |
| `AIR-CHANGE-REASON` #0 | `American Airlines ticket change receipt (later return).pdf` | line 108.00 USD | AIR-CHANGE (p.11, App. A p.28) |
| `LOD-FOLIO-PERSONAL` #0 | `Hyatt Regency Chicago folio.pdf` | line 1120.60 USD; not at full 1182.59 | LOD-ITEMIZE (p.12–13 (Documentation) + Concur); APPB-PERSONAL (App. B p.30–31) |
| `LOD-BOOKING-CONF` #0 | `Hyatt Regency Chicago reservation confirmation.pdf` | skip `Hyatt Regency Chicago reservation confirmation.pdf` | DOC-75 (p.12, p.24) |
| `MEAL-TRAVEL-SMALL` #0 | `Quartino Ristorante check.pdf` | line 39.27 USD | MEAL-TRAVEL (p.12) |
| `MEAL-TRAVEL-SMALL` #1 | `Quartino Ristorante check (2).pdf` | line 42.49 USD | MEAL-TRAVEL (p.12) |
| `MEAL-TRAVEL-BIG-ITEMIZED` #0 | `RPM Steak dinner check.pdf` | line 91.53 USD | DOC-75 (p.12, p.24); MEAL-TRAVEL (p.12) |
| `MEAL-BUSINESS-ALCOHOL` #0 | `The Purple Pig business lunch check.pdf` | line 94.07 USD; line 41.84 USD; flag (alcohol, wine) | MEAL-ALCOHOL (p.12–13, App. A p.28); MEAL-BUSINESS (p.11–12) |
| `MEAL-DELIVERY` #0 | `Uber Eats Lou Malnati's Pizzeria.pdf` | line 40.46 USD | MEAL-TRAVEL (p.12); APPA-TIPS (App. A p.29, App. B p.30) |
| `MEAL-TIP-EXCESSIVE` #0 | `RPM Steak lunch check (large tip).pdf` | line 70.61 USD; flag (tip, gratuity) | APPA-TIPS (App. A p.29, App. B p.30) |
| `MEAL-COFFEE-SMALL` #0 | `Intelligentsia Coffee — Millennium Park coffee.pdf` | line 12.02 USD | MEAL-TRAVEL (p.12) |
| `GT-UBER` #0 | `Uber Aug 10 920 AM.pdf` | line 59.90 USD | GT-AIRPORT (p.15, App. A p.29) |
| `GT-UBER` #1 | `Uber Aug 11 955 PM.pdf` | line 20.10 USD | GT-AIRPORT (p.15, App. A p.29) |
| `GT-UBER` #2 | `Uber Aug 12 348 PM.pdf` | line 20.85 USD | GT-AIRPORT (p.15, App. A p.29) |
| `GT-UBER-TIP-UPDATED` #0 | `Uber Aug 11 receipt.pdf`, `Uber Aug 11 UPDATED receipt.pdf` | line 21.35 USD; skip `Uber Aug 11 receipt.pdf` | GT-AIRPORT (p.15, App. A p.29); REPORT-ONE (p.22) |
| `GT-TAXI` #0 | `Flash Cab Company receipt.pdf` | line 52.80 USD | GT-AIRPORT (p.15, App. A p.29) |
| `GT-TRANSIT` #0 | `CTA fare receipt.pdf` | line 15.00 USD | GT-AIRPORT (p.15, App. A p.29) |
| `REG-MEMBERSHIP-PAID` #0 | `MOSS Association registration receipt (with membership).pdf` | line 590.00 USD; flag (membership, dues) | MISC-75 (p.18); APPB-CLUBS (App. B p.30) |
| `REG-WORKSHOP` #0 | `MOSS Association tutorial add-on receipt.pdf` | line 90.00 USD | MISC-75 (p.18) |
| `OTH-POSTER` #0 | `Poster printing.pdf` | line 125.50 USD; flag (poster, printing) | MISC-75 (p.18) |
| `OTH-NEWSPAPER` #0 | `Newsstand receipt.pdf` | skip `Newsstand receipt.pdf` | APPB-READING (App. B p.31) |
| `OTH-CLUB-FEES` #0 | `Golf with the collaborators.pdf` | line 315.00 USD; flag (group event, preauthoriz + ask for the document) | APPB-CLUBS (App. B p.30); ENT-TASTE (p.19) |
| `DOC-PROGRAM` #0 | `Conference program.pdf` | skip `Conference program.pdf` | DOC-75 (p.12, p.24) |

## Deliberate traps

_Contradictions and duplicates put in on purpose; any other contradiction in the folder is a generator defect._

- `LOD-BOOKING-CONF` (`Hyatt Regency Chicago reservation confirmation.pdf`): A reservation confirmation for the same stay the folio bills, with no payment taken; do not file it as a second lodging line.
- `GT-UBER-TIP-UPDATED` (`Uber Aug 11 receipt.pdf`, `Uber Aug 11 UPDATED receipt.pdf`): An original and an UPDATED receipt for the same ride (the tip added afterwards); file the ride once at the updated amount and leave the original out.

## Turns sent to the agent

**Turn 1** (6 files): REHEARSAL ON THE REAL CONCUR SITE — never submit, never use ready_to_submit; end every turn with `done`. Work only on the report named below. Read trip_notes.txt (and mileage_log.txt if present) first: they carry the purpose, the attendees, the remarks that decide several files. Apply the institution policy: file what it allows, leave out what it does not and say so, split what must be split, and `flag` every judgment call with its basis. Not every file is an expense. Attach each receipt to its line. Turn 1: create the expense report 'MOSS 2026 Chicago' — business purpose: Present a paper at MOSS 2026 (Midwest Optimization & Systems Symposium), Chicago IL, Aug 11–13 2026, and meet the symposium's benchmark working group; travel type Domestic; funding Non-Grant; Oracle Alias: pick any alias from the search as a PLACEHOLDER and flag it. Then add the lines for these files: American Airlines DCA-ORD receipt.pdf; American Airlines checked bag receipt.pdf; American Airlines seat assignment receipt.pdf; American Airlines ticket change receipt (later return).pdf; MOSS Association registration receipt (with membership).pdf; MOSS Association tutorial add-on receipt.pdf. Call done with a COMPACT summary (one line per line added, one line per open item; under 25 lines).

**Turn 2** (2 files): REHEARSAL ON THE REAL CONCUR SITE — never submit, never use ready_to_submit; end every turn with `done`. Work only on the report named below. Read trip_notes.txt (and mileage_log.txt if present) first: they carry the purpose, the attendees, the remarks that decide several files. Apply the institution policy: file what it allows, leave out what it does not and say so, split what must be split, and `flag` every judgment call with its basis. Not every file is an expense. Attach each receipt to its line. Turn 2: continue on the report 'MOSS 2026 Chicago'. Handle lodging (itemize every folio by night: room rate + tax per night; leave personal charges out) — the files: Hyatt Regency Chicago folio.pdf; Hyatt Regency Chicago reservation confirmation.pdf. Call done with a COMPACT summary (one line per line added, one line per open item; under 25 lines).

**Turn 3** (7 files): REHEARSAL ON THE REAL CONCUR SITE — never submit, never use ready_to_submit; end every turn with `done`. Work only on the report named below. Read trip_notes.txt (and mileage_log.txt if present) first: they carry the purpose, the attendees, the remarks that decide several files. Apply the institution policy: file what it allows, leave out what it does not and say so, split what must be split, and `flag` every judgment call with its basis. Not every file is an expense. Attach each receipt to its line. Turn 3: continue on the report 'MOSS 2026 Chicago'. Handle meals (attendees from trip_notes.txt; alcohol split off to 52611; international days are per diem, not actual cost) — the files: Quartino Ristorante check.pdf; Quartino Ristorante check (2).pdf; RPM Steak dinner check.pdf; The Purple Pig business lunch check.pdf; Uber Eats Lou Malnati's Pizzeria.pdf; RPM Steak lunch check (large tip).pdf; Intelligentsia Coffee — Millennium Park coffee.pdf. Call done with a COMPACT summary (one line per line added, one line per open item; under 25 lines).

**Turn 4** (11 files): REHEARSAL ON THE REAL CONCUR SITE — never submit, never use ready_to_submit; end every turn with `done`. Work only on the report named below. Read trip_notes.txt (and mileage_log.txt if present) first: they carry the purpose, the attendees, the remarks that decide several files. Apply the institution policy: file what it allows, leave out what it does not and say so, split what must be split, and `flag` every judgment call with its basis. Not every file is an expense. Attach each receipt to its line. Turn 4: continue on the report 'MOSS 2026 Chicago'. Handle ground transportation, mileage (from mileage_log.txt, if present), everything else, and the documents that are not receipts — the files: Uber Aug 10 920 AM.pdf; Uber Aug 11 955 PM.pdf; Uber Aug 12 348 PM.pdf; Uber Aug 11 receipt.pdf; Uber Aug 11 UPDATED receipt.pdf; Flash Cab Company receipt.pdf; CTA fare receipt.pdf; Poster printing.pdf; Newsstand receipt.pdf; Golf with the collaborators.pdf; Conference program.pdf. Then check that EVERY file in the folder has been either filed or deliberately left out, write the Report Header Comment (Report Details → Report Header → Comment → Save) listing every document left out and why in one clause each, report the report total, and call done with a COMPACT summary of this turn's lines and every open item (under 30 lines).

