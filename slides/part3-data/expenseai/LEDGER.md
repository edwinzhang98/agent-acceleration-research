# 实验侧总账 — 169 个情形各测过几次、过了几次

_由 `scripts/situation_ledger.py` 于 2026-09-20 05:52 生成。每跑完一批重跑一次。设计侧的对应文档是 `gw_policy_data/reports/POLICY_READING.md`。有答案快照的批次用快照重算（精确）；更早的批次读当时的 score 文件，按单据名映射到情形（数据后来重新生成过的单据映射不上，那一趟就不计）。因基础设施故障作废的运行（API 余额不足、没有一轮到达 agent、运行未正常结束、某轮出错且零花费）整趟不计入任何统计，列在文末。符号：✓ 通过 · ✗ 未通过（括号里是原因） · ○ 可报可不报且已说明。批次号只写后五位（`13-05` = 20260913-05），字母是 trip。_

## 汇总

- 情形总数 169；有过有效测量的 169；至少通过一次的 160；测过但从未通过的 9；从未有效测量的 0。
- 纳入的运行：41 趟，25 个批次；因基础设施故障排除 8 趟（不计入任何统计，见文末）。

## 每个情形

| 情形 | 判定 | trip | 通过/测量 | 每次运行的结果 | 涉及的单据 |
|---|---|---|---|---|---|
| `AIR-COACH-DIRECT` Coach ticket bought from the airline | 照报 | A | 4/4 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓<br>18-02 P ✓ | American Airlines DCA-ORD receipt.pdf<br>Delta Air Lines DCA-BOS receipt.pdf<br>JetBlue Airways DCA-ORD receipt.pdf |
| `AIR-COACH-INTL` Coach ticket to a foreign city, bought in USD | 照报 | B H | 6/6 | 11-01 B ✓<br>13-01 B ✓<br>13-05 H ✓<br>14-02 B ✓<br>14-03 H ✓<br>18-02 P ✓ | American Airlines YYZ-DCA receipt.pdf<br>Delta Air Lines LHR-IAD receipt.pdf<br>Delta Air Lines YYZ-DCA receipt.pdf<br>JetBlue Airways YUL-DCA receipt.pdf |
| `AIR-AGENCY` Coach ticket booked through iBuy+ Travel / Travel Leaders | 照报 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | United Airlines DCA-LGA receipt (Travel Leaders).pdf |
| `AIR-IBUY-PRETRIP` iBuy+ ticket for NEXT month's trip, claimed now | 报 + flag | F | 1/2 | 13-03 F ✗（缺 flag）<br>14-02 F ✓ | American Airlines DCA-SEA receipt (iBuy+ Travel, future trip |
| `AIR-OOP-PRETRIP` Airline-direct ticket for a trip not yet taken | 不报 + 说明 | K | 1/2 | 13-08 K ✓<br>14-06 K ✗（缺 Comment） | JetBlue Airways DCA-SFO receipt (trip next month).pdf (不报) |
| `AIR-BAG` First checked bag fee | 照报 | A | 4/4 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓<br>18-02 P ✓ | American Airlines checked bag receipt.pdf<br>Delta Air Lines checked bag receipt.pdf<br>JetBlue Airways checked bag receipt.pdf |
| `AIR-BAG-EXCESS` Sports-equipment baggage fee (bicycle) | 不报 + 说明 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | United Airlines sports equipment fee.pdf (不报) |
| `AIR-WIFI` In-flight Wi-Fi | 照报 | C | 1/1 | 14-02 C ✓ | Delta Air Lines Wi-Fi receipt.pdf |
| `AIR-WIFI-OTHER-CARRIER` In-flight Wi-Fi receipt from an airline the traveler did not fly | 报 + flag | I | 2/3 | 13-06 I ✗（缺 flag）<br>13-15 I ✓<br>14-04 I ✓ | Delta Air Lines Wi-Fi receipt.pdf |
| `AIR-SEAT-ECONOMY` Paid advance seat assignment inside economy | 报 + flag | A | 0/1 | 14-02 A ✗（缺 flag） | American Airlines seat assignment receipt.pdf |
| `AIR-EXTRA-LEGROOM` Extra-legroom seat upgrade | 报 + flag | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | American Airlines extra-legroom seat upgrade receipt.pdf<br>American Airlines extra-legroom seat upgrade receipt.pdf (不报 |
| `AIR-PRIORITY` Priority boarding | 报 + flag | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | American Airlines priority boarding receipt.pdf<br>American Airlines priority boarding receipt.pdf (不报) |
| `AIR-PREMIUM-NOMEMO` First class on a short domestic flight, no approval in the folder | 报 + flag | I | 2/3 | 13-06 I ✗（缺 Comment）<br>13-15 I ✓<br>14-04 I ✓ | American Airlines ATL-DCA receipt (First).pdf<br>American Airlines ATL-DCA receipt (First).pdf (不报) |
| `AIR-PREMIUM-LONGHAUL-MEMO` Business class on a 7-hour international segment, with the dean's memo | 照报 | G | 2/2 | 13-14 G ✓<br>14-03 G ✓ | Dean approval - business class airfare.pdf (不报)<br>United Airlines CDG-DCA receipt (Business).pdf<br>United Airlines CDG-IAD receipt (Business).pdf |
| `AIR-PREMIUM-LONGHAUL-NOMEMO` Business class on a 7-hour segment, memo missing | 报 + flag | O | 2/3 | 13-10 O ✓<br>13-16 O ✗（缺 flag；行缺失）<br>14-01 O ✓ | American Airlines LHR-DCA receipt (Business).pdf<br>American Airlines LHR-IAD receipt (Business).pdf |
| `AIR-ECREDIT` Ticket paid partly with an airline eCredit of unknown origin | 报 + flag | C | 2/3 | 11-01 C ✓<br>13-01 C ✗（缺 flag）<br>14-02 C ✓ | Delta Air Lines DCA-ATL receipt (eCredit applied).pdf |
| `AIR-MILES-AWARD` Award ticket paid with miles (only taxes charged) | 不报 + 说明 | H | 1/2 | 13-05 H ✓<br>14-03 H ✗（该不报却报了） | Delta Air Lines DCA-ORD award ticket receipt.pdf (不报) |
| `AIR-MILES-UPGRADE-COPAY` Coach fare plus a cash co-pay for a miles upgrade | 减额后报 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | American Airlines DCA-SEA receipt (miles upgrade).pdf |
| `AIR-REFUNDED` Ticket later refunded in full (refund confirmation in the folder) | 不报 + 说明 | B | 3/3 | 11-01 B ✓<br>13-01 B ✓<br>14-02 B ✓ | Delta Air Lines DCA-BOS receipt (later refunded).pdf (不报)<br>Delta refund confirmation.pdf (不报) |
| `AIR-CHANGE-NOREASON` Fare difference for a changed flight, no reason given | 报 + flag | F | 0/2 | 13-03 F ✗（缺 flag）<br>14-02 F ✗（缺 Comment；缺 flag） | American Airlines ticket change receipt.pdf |
| `AIR-CHANGE-REASON` Fare difference for a changed flight, reason in the notes | 照报 | A | 3/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓ | American Airlines ticket change receipt (earlier return).pdf<br>American Airlines ticket change receipt (later return).pdf |
| `AIR-CANCEL-PENALTY` Airline cancellation penalty for a business-caused cancellation | 照报 | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | American Airlines cancellation fee receipt.pdf<br>Delta Air Lines cancellation fee receipt.pdf |
| `AIR-COMPANION` Ticket for the traveler's spouse on the same booking | 不报 + 说明 | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | United Airlines DCA-SFO receipt MEI ZHANG.pdf (不报)<br>United Airlines DCA-SFO receipt WEI ZHANG.pdf (不报)<br>United Airlines DCA-SFO receipt.pdf |
| `AIR-COMPANION-MEMO` Spouse's ticket with the Vice President's written pre-approval | 照报 | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | American Airlines DCA-ORD receipt MEI ZHANG.pdf<br>Delta Air Lines DCA-ORD receipt MEI ZHANG.pdf<br>VP approval - companion travel.pdf (不报) |
| `AIR-INDIRECT-COMPARISON` Personal stop-over routing, with the direct-fare screenshot | 减额后报 | I | 3/3 | 13-06 I ✓<br>13-15 I ✓<br>14-04 I ✓ | American Airlines DCA-ATL receipt (via LGA).pdf<br>Fare comparison at booking (direct route).pdf (不报) |
| `AIR-INDIRECT-NOCOMPARISON` Personal stop-over routing without a fare comparison | 报 + flag | K | 1/2 | 13-08 K ✓<br>14-06 K ✗（flag 未写补件） | JetBlue Airways DCA-SFO receipt (via LGA).pdf |
| `AIR-FOREIGN-CARRIER-GRANT` Non-US carrier on a federal grant (Fly America) | 报 + flag | E | 1/2 | 13-02 E ✓<br>14-02 E ✗（缺 Comment；缺 flag） | British Airways LHR-DCA receipt.pdf<br>British Airways LHR-IAD receipt.pdf |
| `AIR-CLUB` Airport lounge day pass | 不报 + 说明 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | Airport lounge day pass.pdf (不报) |
| `AIR-INSURANCE` Trip / baggage insurance bought with the ticket | 不报 + 说明 | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | Travel insurance confirmation.pdf (不报) |
| `AIR-GLOBAL-ENTRY` Global Entry / TSA PreCheck application fee | 报 + flag | E | 1/2 | 13-02 E ✗（行缺失）<br>14-02 E ✓ | Global Entry fee receipt.pdf |
| `AIR-PASSPORT` Passport renewal / visa fee before an international trip | 报 + flag | B | 2/3 | 11-01 B ✓<br>13-01 B ✓<br>14-02 B ✗（flag 未写补件） | Passport or visa fee receipt.pdf |
| `AIR-PCARD-PAID` Ticket paid with the GW P-Card | 报 + flag | K | 2/2 | 13-08 K ✓<br>14-06 K ✓ | JetBlue Airways SFO-DCA receipt (P-Card).pdf (不报) |
| `AIR-OUTSIDE-REIMBURSED` Ticket the host institution reimburses | 不报 + 说明 | O | 3/3 | 13-10 O ✓<br>13-16 O ✓<br>14-01 O ✓ | United Airlines DCA-LGA receipt (host reimburses).pdf (不报) |
| `LOD-FOLIO` Hotel folio, several nights at varying rates | 照报 | B F | 6/6 | 11-01 B ✓<br>13-01 B ✓<br>13-12 N ✓<br>14-02 B ✓<br>14-02 F ✓<br>18-02 P ✓ | Boston Park Plaza folio.pdf<br>Sheraton Boston Hotel folio.pdf<br>Sheraton Grand Seattle folio.pdf<br>The Roosevelt Hotel folio.pdf |
| `LOD-FOLIO-PERSONAL` Folio with a movie, minibar and health-club charge on it | 减额后报 | A | 3/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓ | Hyatt Regency Chicago folio.pdf |
| `LOD-FOLIO-LAUNDRY-SHORT` Laundry on a four-day trip | 减额后报 | M | 2/3 | 13-07 J ✓<br>13-11 M ✓<br>14-06 M ✗（应减额却全额报；行缺失） | New York Marriott Marquis folio (4 nights).pdf<br>The Westin Copley Place, Boston folio (4 nights).pdf |
| `LOD-FOLIO-LAUNDRY-LONG` Laundry on a seven-day trip | 照报 | D J | 3/4 | 11-01 D ✓<br>13-01 D ✗（拆分: night 2026-08-07: 280.95 != expected 246.45 (or 251.38 with the daily extra)）<br>14-02 D ✓<br>14-05 J ✓ | Hotel Nikko San Francisco folio (7 nights).pdf<br>The Roosevelt Hotel folio (7 nights).pdf |
| `LOD-FOLIO-PARKING` Hotel valet parking on the folio | 照报 | N | 2/2 | 13-03 F ✓<br>14-06 N ✓ | Sheraton Grand Seattle folio (with parking).pdf<br>The Roosevelt Hotel folio (with parking).pdf |
| `LOD-FOLIO-ROOMSERVICE-BIG` Room-service dinner over $75 on the folio, no itemised ticket | 报 + flag | F | 0/2 | 13-03 F ✗（缺 flag）<br>14-02 F ✗（flag 未写补件） | Hyatt Regency Seattle folio (room service).pdf |
| `LOD-FOLIO-ROOMSERVICE-SMALL` Room-service breakfast under $75 on the folio | 照报 | K | 2/2 | 13-08 K ✓<br>14-06 K ✓ | Hotel Nikko San Francisco folio (breakfast).pdf |
| `LOD-FOLIO-INTERNET` Hotel internet charge on the folio | 照报 | K | 2/2 | 13-08 K ✓<br>14-06 K ✓ | Hilton San Francisco Union Square folio (internet).pdf |
| `LOD-FOLIO-INTERNET-GRANT` Hotel internet on a federal research grant | 报 + flag | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Hotel Indigo Atlanta Downtown by IHG folio (internet).pdf |
| `LOD-FOLIO-INROOM-ALCOHOL` In-room bar alcohol on the folio | 减额后报 | I | 3/3 | 13-06 I ✓<br>13-15 I ✓<br>14-04 I ✓ | Hotel Indigo Atlanta Downtown by IHG folio (in-room bar).pdf |
| `LOD-OTA` Expedia-style prepaid receipt: nightly prices and one tax total | 照报 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | Expedia receipt New York Marriott Marquis.pdf |
| `LOD-FOREIGN` Foreign hotel folio in the local currency | 照报 | B E G H O | 13/14 | 11-01 B ✓<br>13-01 B ✓<br>13-02 E ✓<br>13-04 G ✓<br>13-05 H ✓<br>13-10 O ✓<br>13-14 G ✓<br>13-16 O ✓<br>14-01 O ✓<br>14-02 B ✓<br>14-02 E ✗（商家）<br>14-03 G ✓<br>14-03 H ✓<br>18-02 P ✓ | Chelsea Hotel, Toronto folio CAD.pdf<br>Hotel Bonaventure Montreal folio CAD.pdf<br>Novotel Paris Centre Tour Eiffel folio EUR.pdf<br>Premier Inn London County Hall folio GBP.pdf<br>The Bloomsbury Hotel folio GBP.pdf |
| `LOD-NOSHOW` No-show charge for a reservation not cancelled | 不报 + 说明 | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Hotel Indigo Atlanta Downtown by IHG no-show charge.pdf (不报)<br>Hyatt Regency Atlanta no-show charge.pdf (不报) |
| `LOD-CANCEL-FEE-AIRLINE` Hotel cancellation fee caused by an airline cancellation | 报 + flag | K | 1/2 | 13-03 F ✗（缺 flag；行缺失）<br>14-06 K ✓ | Hilton San Francisco Union Square late cancellation charge.p<br>Sheraton Grand Seattle late cancellation charge.pdf |
| `LOD-AIRBNB-STAFF` Airbnb stay by a staff member | 报 + flag | K | 2/2 | 13-08 K ✓<br>14-06 K ✓ | Airbnb receipt.pdf |
| `LOD-AIRBNB-STUDENT` Airbnb stay by a student, no prior approval in the folder | 报 + flag | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | Airbnb receipt.pdf<br>Airbnb receipt.pdf (不报) |
| `LOD-SUITE` Junior suite instead of a standard room | 报 + flag | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Boston Park Plaza folio (suite).pdf |
| `LOD-PERSONAL-DAYS` Two personal nights added to the stay | 减额后报 | I | 3/3 | 13-06 I ✓<br>13-15 I ✓<br>14-04 I ✓ | Hyatt Regency Atlanta folio (incl. weekend).pdf |
| `LOD-COMPANION-SURCHARGE` Additional-guest charge for the spouse on the folio | 减额后报 | H | 1/2 | 13-05 H ✗（应减额却全额报；行缺失）<br>14-03 H ✓ | Palmer House, a Hilton Hotel folio (two guests).pdf |
| `LOD-DEPOSIT-DUP` Deposit receipt plus the final folio that applies it | 不报 + 说明 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | The Westin Copley Place, Boston deposit receipt.pdf (不报)<br>The Westin Copley Place, Boston folio.pdf |
| `LOD-BOOKING-CONF` Reservation confirmation with no payment taken | 不报 + 说明 | A | 1/1 | 14-02 A ✓ | Hyatt Regency Chicago reservation confirmation.pdf (不报) |
| `LOD-RESORT-FEE` Mandatory destination / resort fee on the folio | 报 + flag | J | 1/2 | 13-07 J ✗（缺 flag）<br>14-05 J ✓ | New York Marriott Marquis folio (destination fee).pdf<br>The Roosevelt Hotel folio (destination fee).pdf |
| `MEAL-TRAVEL-SMALL` Travel meal alone, under $75 | 照报 | A A B C C D F I J K M N | 25/25 | 11-01 A ✓<br>11-01 B ✓<br>11-01 C ✓<br>11-01 D ✓<br>13-01 A ✓<br>13-01 B ✓<br>13-01 C ✓<br>13-01 D ✓<br>13-03 F ✓<br>13-06 I ✓<br>13-07 J ✓<br>13-08 K ✓<br>13-11 M ✓<br>13-12 N ✓<br>13-15 I ✓<br>14-02 A ✓<br>14-02 B ✓<br>14-02 C ✓<br>14-02 D ✓<br>14-02 F ✓<br>14-04 I ✓<br>14-05 J ✓<br>14-06 K ✓<br>14-06 M ✓<br>14-06 N ✓ | Blue Bottle Coffee — Mint Plaza check.pdf<br>Boston Chops Downtown check.pdf<br>Canlis check.pdf<br>Clover Food Lab check.pdf<br>Do-Rite Donuts & Coffee check.pdf<br>Estrellita check.pdf<br>Gramercy Tavern check.pdf<br>J. Christopher's check.pdf<br>Joe's Shanghai check.pdf<br>Katz's Delicatessen check.pdf<br>Legal Sea Foods — Park Square check.pdf<br>Lou Malnati's Pizzeria check.pdf<br>Quartino Ristorante check (2).pdf<br>Quartino Ristorante check.pdf<br>Serious Pie Downtown check.pdf<br>South City Kitchen Midtown check.pdf<br>Super Duper Burgers check.pdf<br>The Slanted Door check.pdf<br>The Varsity check.pdf<br>Win Indonesian Grill & Gastrobar check.pdf<br>Xi'an Famous Foods check.pdf<br>Zuni Café check.pdf |
| `MEAL-TRAVEL-BIG-ITEMIZED` Travel meal over $75 with the itemised check | 照报 | A G | 6/6 | 11-01 A ✓<br>13-01 A ✓<br>13-04 G ✓<br>13-14 G ✓<br>14-02 A ✓<br>14-03 G ✓ | Girl & the Goat dinner check.pdf<br>Ostra dinner check.pdf<br>RPM Steak dinner check.pdf |
| `MEAL-TRAVEL-BIG-SLIP` Meal over $75 with only the card slip | 报 + flag | C | 1/1 | 14-02 C ✓ | Estrellita card slip.pdf |
| `MEAL-DELIVERY` Food delivery to the hotel with fees and a tip | 照报 | A | 1/1 | 14-02 A ✓ | Uber Eats Lou Malnati's Pizzeria.pdf |
| `MEAL-BUSINESS` Business dinner with collaborators, no alcohol | 照报 | B I | 6/6 | 11-01 B ✓<br>13-01 B ✓<br>13-06 I ✓<br>13-15 I ✓<br>14-02 B ✓<br>14-04 I ✓ | Boston Chops Downtown business dinner check.pdf<br>Legal Sea Foods — Park Square business dinner check.pdf<br>Mary Mac's Tea Room business dinner check.pdf<br>South City Kitchen Midtown business dinner check.pdf |
| `MEAL-BUSINESS-ALCOHOL` Business meal with wine on the check | 拆分 | A | 3/4 | 11-01 A ✓<br>13-01 A ✗（缺 flag）<br>14-02 A ✓<br>18-02 P ✓ | Girl & the Goat business lunch check.pdf<br>Ostra business lunch check.pdf<br>The Purple Pig business lunch check.pdf |
| `MEAL-BUSINESS-ALCOHOL-GRANT` Business meal with wine, on a federal grant | 拆分 | C | 1/3 | 11-01 C ✗（与会人: expected 3 attendee(s), got 1）<br>13-01 C ✓<br>14-02 C ✗（行缺失） | South City Kitchen Midtown business dinner check.pdf<br>Win Indonesian Grill & Gastrobar business dinner check.pdf |
| `MEAL-GROUP-FUNCTION` Group dinner for twelve with the invitation list | 照报 | B | 2/3 | 11-01 B ✗（与会人: expected 11 attendee(s), got 2）<br>13-01 B ✓<br>14-02 B ✓ | Attendee list - workshop dinner.txt (不报)<br>Ostra group dinner check.pdf<br>Toro group dinner check.pdf |
| `MEAL-TIP-EXCESSIVE` Lunch with a tip near 80% | 报 + flag | A | 2/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✗（行缺失） | Girl & the Goat lunch check (large tip).pdf<br>RPM Steak lunch check (large tip).pdf |
| `MEAL-INTL-PERDIEM` Meal receipt from an international day | 不报 + 说明 | B B E G H O | 11/13 | 11-01 B ✓<br>13-01 B ✓<br>13-02 E ✗（缺 Comment）<br>13-04 G ✗（缺 Comment）<br>13-05 H ✓<br>13-10 O ✓<br>13-14 G ✓<br>13-16 O ✓<br>14-01 O ✓<br>14-02 B ✓<br>14-02 E ✓<br>14-03 G ✓<br>14-03 H ✓ | Canoe check CAD.pdf (不报)<br>Olive et Gourmando check CAD.pdf (不报)<br>Paul — Gare du Nord check EUR.pdf (不报)<br>Pret A Manger — Euston Rd check GBP.pdf (不报)<br>Schwartz's Deli check CAD.pdf (不报)<br>Tim Hortons — Bay St check CAD.pdf (不报)<br>Toqué! check CAD.pdf (不报) |
| `TA-INTL-ITINERARY` Per diem for the foreign leg, claimed through Concur's Travel Allowance itinerary | 照报 | B E G H O | 5/7 | 13-16 O ✓<br>14-01 O ✓<br>14-02 B ✓<br>14-02 E ✓<br>14-03 G ✓<br>14-03 H ✗（餐补: a per-diem meals line on every day of the foreign leg — missing 2026-0；餐补: an incidentals line on every day of the foreign leg — missing 2026-08-）<br>18-02 P ✗（餐补: a per-diem meals line on every day of the foreign leg — missing 2026-0；餐补: an incidentals line on every day of the foreign leg — missing 2026-08-） | Travel Allowance 2026-07-23 – 2026-07-28 (餐补行)<br>Travel Allowance 2026-08-09 – 2026-08-13 (餐补行)<br>Travel Allowance 2026-08-13 – 2026-08-17 (餐补行)<br>Travel Allowance 2026-08-16 – 2026-08-19 (餐补行)<br>Travel Allowance 2026-08-18 – 2026-08-22 (餐补行)<br>Travel Allowance 2026-08-28 – 2026-08-31 (餐补行) |
| `TA-INTL-PROVIDED-MEALS` Meals provided abroad (the host's lunch and dinner), deducted from the per diem | 报 + flag | E G | 0/2 | 14-02 E ✗（缺 Comment；缺 flag）<br>14-03 G ✗（缺 Comment；缺 flag） | 已提供的餐: 2026-07-25 lunch; 2026-07-26 dinner<br>已提供的餐: 2026-08-11 lunch; 2026-08-12 dinner |
| `MEAL-LOCAL-PERSONAL` Lunch alone on a local (< 50 mile) business day | 不报 + 说明 | L | 3/3 | 13-09 L ✓<br>13-13 L ✓<br>14-06 L ✓ | Tatte Bakery & Café — Bethesda lunch (local day).pdf (不报) |
| `MEAL-LOCAL-IN-MEETING` Lunch during an all-day local meeting | 报 + flag | L | 1/4 | 13-01 D ✗（缺 flag）<br>13-09 L ✗（缺 flag）<br>13-13 L ✓<br>14-06 L ✗（缺 flag；行缺失） | Woodmont Grill lunch (workshop day).pdf |
| `MEAL-LOCAL-BUSINESS` Local lunch with a visiting collaborator | 照报 | L | 3/3 | 13-09 L ✓<br>13-13 L ✓<br>14-06 L ✓ | Founding Farmers DC lunch with visitor.pdf |
| `MEAL-CELEBRATION` Cake for a lab member's birthday | 不报 + 说明 | L | 3/3 | 13-09 L ✓<br>13-13 L ✓<br>14-06 L ✓ | Bakery receipt (birthday).pdf (不报) |
| `MEAL-WITH-SPOUSE` Dinner for two where the second person is the spouse | 减额后报 | D H | 4/5 | 11-01 D ✗（应减额却全额报；行缺失）<br>13-01 D ✓<br>13-05 H ✓<br>14-02 D ✓<br>14-03 H ✓ | Lou Malnati's Pizzeria dinner for two.pdf<br>RPM Steak dinner for two.pdf<br>Zuni Café dinner for two.pdf |
| `MEAL-AFFIDAVIT` Meal with no receipt, covered by a Missing Receipt Acknowledgement form | 报 + flag | C | 2/3 | 11-01 C ✗（缺 flag）<br>13-01 C ✓<br>14-02 C ✓ | Missing receipt form - Mary Mac's Tea Room.pdf<br>Missing receipt form - Win Indonesian Grill & Gastrobar.pdf |
| `MEAL-DUP-SLIP-ITEMIZED` Itemised check AND card slip for the same meal | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Din Tai Fung — Pacific Place card slip.pdf (不报)<br>Din Tai Fung — Pacific Place itemised check.pdf<br>The Pink Door card slip.pdf (不报)<br>The Pink Door itemised check.pdf |
| `MEAL-ATTENDEE-APPROVER` Business lunch where one attendee is the report's approver | 报 + flag | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | Joe's Shanghai lunch check.pdf<br>Katz's Delicatessen lunch check.pdf |
| `MEAL-INTERNAL-STAFF` Working lunch with two GW colleagues on the trip | 照报 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | Joe's Shanghai working lunch.pdf<br>Shake Shack — Madison Square Park working lunch.pdf |
| `MEAL-COFFEE-SMALL` Coffee and a pastry | 照报 | A C D D J K | 13/13 | 11-01 A ✓<br>11-01 C ✓<br>11-01 D ✓<br>13-01 A ✓<br>13-01 C ✓<br>13-01 D ✓<br>13-07 J ✓<br>13-08 K ✓<br>14-02 A ✓<br>14-02 C ✓<br>14-02 D ✓<br>14-05 J ✓<br>14-06 K ✓ | Blue Bottle Coffee — Mint Plaza coffee (2).pdf<br>Blue Bottle Coffee — Mint Plaza coffee.pdf<br>Do-Rite Donuts & Coffee coffee.pdf<br>Intelligentsia Coffee — Millennium Park coffee.pdf<br>J. Christopher's coffee.pdf<br>Joe Coffee Company — Grand Central coffee.pdf<br>Octane Coffee — Westside coffee.pdf<br>Tartine Bakery coffee (2).pdf<br>Tartine Bakery coffee.pdf<br>Xi'an Famous Foods coffee.pdf |
| `GT-UBER` Ride-share between airport, hotel and venue | 照报 | A A A B B D D E H I J K | 19/20 | 11-01 A ✓<br>11-01 B ✓<br>11-01 D ✓<br>13-01 A ✓<br>13-01 B ✓<br>13-01 D ✓<br>13-02 E ✓<br>13-05 H ✓<br>13-06 I ✓<br>13-07 J ✓<br>13-08 K ✓<br>13-15 I ✓<br>14-02 A ✗（行缺失）<br>14-02 B ✓<br>14-02 D ✓<br>14-02 E ✓<br>14-03 H ✓<br>14-04 I ✓<br>14-05 J ✓<br>14-06 K ✓ | Uber Aug 04 755 PM.pdf<br>Uber Aug 07 705 AM.pdf<br>Uber Aug 08 1241 PM.pdf<br>Uber Aug 09 1212 PM.pdf<br>Uber Aug 10 855 AM.pdf<br>Uber Aug 10 920 AM.pdf<br>Uber Aug 11 1148 AM.pdf<br>Uber Aug 11 955 PM.pdf<br>Uber Aug 12 348 PM.pdf<br>Uber Aug 13 1120 AM.pdf<br>Uber Aug 14 528 PM.pdf<br>Uber Aug 15 928 AM.pdf<br>Uber Aug 20 148 PM.pdf<br>Uber Aug 22 905 PM.pdf<br>Uber Aug 24 528 PM.pdf<br>Uber Aug 24 812 PM.pdf<br>Uber Aug 24 841 AM.pdf<br>Uber Aug 25 748 AM.pdf<br>Uber Aug 28 828 AM.pdf<br>Uber Aug 29 212 PM.pdf<br>Uber Jul 22 1228 PM.pdf<br>Uber Jul 22 748 PM.pdf<br>Uber Sep 04 948 PM.pdf<br>Uber Sep 06 1212 PM.pdf |
| `GT-UBER-TIP-UPDATED` Original and UPDATED ride receipts (tip added afterwards) | 不报 + 说明 | A | 2/3 | 11-01 A ✓<br>13-01 A ✗（该不报却报了）<br>14-02 A ✓ | Uber Aug 11 UPDATED receipt.pdf<br>Uber Aug 11 receipt.pdf (不报) |
| `GT-UBER-DUP-IDENTICAL` The same ride receipt saved twice under two names | 不报 + 说明 | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Uber airport to hotel Jul 13.pdf<br>Uber hotel to venue Jul 15.pdf<br>Uber_from_ATL_to_hotel.pdf (不报)<br>Uber_hotel_to_venue_receipt.pdf (不报) |
| `GT-TAXI` Taxi with a printed meter receipt | 照报 | A | 3/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓ | Flash Cab Company receipt.pdf |
| `GT-TAXI-FOREIGN` Taxi abroad, receipt in the local currency | 照报 | E G O | 10/10 | 11-01 B ✓<br>13-01 B ✓<br>13-02 E ✓<br>13-04 G ✓<br>13-10 O ✓<br>13-14 G ✓<br>13-16 O ✓<br>14-01 O ✓<br>14-02 E ✓<br>14-03 G ✓ | Taxi London receipt GBP.pdf<br>Taxi Montréal receipt CAD.pdf<br>Taxi Paris receipt EUR.pdf |
| `GT-TRANSIT` Public transit fare-machine receipt | 照报 | A B J O | 10/11 | 11-01 A ✓<br>11-01 B ✓<br>13-01 A ✓<br>13-01 B ✓<br>13-07 J ✓<br>13-10 O ✓<br>13-16 O ✗（日期）<br>14-01 O ✓<br>14-02 A ✓<br>14-02 B ✓<br>14-05 J ✓ | CTA fare receipt.pdf<br>MBTA fare receipt.pdf<br>MTA New York City Transit fare receipt.pdf |
| `GT-SHUTTLE` Airport shuttle van | 照报 | E | 4/4 | 11-01 D ✓<br>13-01 D ✓<br>13-08 K ✓<br>14-02 E ✓ | Airport shuttle receipt.pdf |
| `GT-RAIL-ACELA-BUSINESS` Acela Business Class instead of a flight | 照报 | B | 3/3 | 11-01 B ✓<br>13-01 B ✓<br>14-02 B ✓ | Amtrak Acela eTicket.pdf |
| `GT-RAIL-ACELA-FIRST` Acela First Class (upgrade from Business) | 减额后报 | G | 1/3 | 13-04 G ✗（应减额却全额报；行缺失）<br>13-14 G ✗（缺 Comment；缺 flag；行缺失）<br>14-03 G ✓ | Amtrak Acela First Class eTicket.pdf |
| `GT-RAIL-COACH` Northeast Regional coach ticket | 照报 | J | 1/2 | 13-07 J ✗（费用类型）<br>14-05 J ✓ | Amtrak Northeast Regional eTicket.pdf |
| `GT-BUS` Intercity bus ticket home from New York / Boston | 照报 | J | 2/2 | 13-07 J ✓<br>14-05 J ✓ | Megabus eTicket (return).pdf |
| `GT-RENTAL-PREFERRED` Hertz / Enterprise / National rental, no extra insurance | 照报 | C | 4/4 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓<br>18-02 P ✓ | Enterprise Rent-A-Car rental agreement.pdf<br>National Car Rental rental agreement.pdf |
| `GT-RENTAL-OTHER-CDW` Avis / Budget rental WITH CDW and liability bought | 照报 | K | 2/2 | 13-08 K ✓<br>14-06 K ✓ | Budget rental agreement.pdf |
| `GT-RENTAL-OTHER-NOCDW` Avis / Budget rental WITHOUT the required insurance | 报 + flag | F | 1/2 | 13-03 F ✗（缺 flag）<br>14-02 F ✓ | Avis rental agreement.pdf |
| `GT-RENTAL-PREFERRED-EXTRA-INSURANCE` Hertz rental with an LDW bought although insurance is included | 报 + flag | I | 2/3 | 13-06 I ✗（缺 flag）<br>13-15 I ✓<br>14-04 I ✓ | Enterprise Rent-A-Car rental agreement (with LDW).pdf |
| `GT-RENTAL-PREPAID-FUEL` Rental with the prepaid fuel option | 报 + flag | I | 2/3 | 13-06 I ✗（行缺失）<br>13-15 I ✓<br>14-04 I ✓ | Hertz rental agreement (prepaid fuel).pdf |
| `GT-RENTAL-FUEL` Gas station receipt for the rental car | 照报 | C | 3/4 | 11-01 C ✗（费用类型）<br>13-01 C ✓<br>14-02 C ✓<br>18-02 P ✓ | BP gas receipt (rental refuel).pdf<br>Shell gas receipt (rental refuel).pdf |
| `GT-RENTAL-FUEL-DATE-MISMATCH` Refuel receipt dated two days AFTER the rental was returned | 报 + flag | F | 1/2 | 13-03 F ✓<br>14-02 F ✗（行缺失） | Exxon gas receipt (rental refuel, dated after return).pdf |
| `GT-RENTAL-SPECIALTY` Premium SUV / luxury rental without approval | 报 + flag | K | 1/2 | 13-08 K ✓<br>14-06 K ✗（flag 未写补件） | Hertz rental agreement (premium vehicle).pdf |
| `GT-RENTAL-INTL-STAFF` Rental abroad by staff with CDW and liability | 照报 | B | 4/4 | 11-01 B ✓<br>13-01 B ✓<br>14-02 B ✓<br>18-02 P ✓ | Hertz rental agreement London GBP.pdf<br>Hertz rental agreement Montréal CAD.pdf |
| `GT-RENTAL-INTL-STUDENT` Rental abroad by a student | 不报 + 说明 | H | 1/2 | 13-05 H ✓<br>14-03 H ✗（该不报却报了） | Hertz rental agreement Toronto CAD.pdf (不报) |
| `GT-RENTAL-VAN15` 15-passenger van rented by a student group | 不报 + 说明 | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | Enterprise rental agreement (15-passenger van).pdf (不报) |
| `GT-RENTAL-STUDENT-NONPREFERRED` Student rents from a non-preferred company | 报 + flag | D | 2/3 | 11-01 D ✗（日期）<br>13-01 D ✓<br>14-02 D ✓ | SIXT rental agreement.pdf |
| `GT-RENTAL-CARWASH` Car wash receipt | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Car wash receipt.pdf (不报) |
| `GT-RENTAL-REPAIR` Tire repair receipt | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Tire repair receipt.pdf (不报) |
| `GT-PARKING-FINE` Parking citation | 不报 + 说明 | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | Parking citation.pdf (不报) |
| `GT-GAS-PERSONAL` Gas for personal car | 不报 + 说明 | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Gas for personal car.pdf (不报) |
| `GT-RENTAL-TOLL` Toll charges while driving the rental | 照报 | C I | 4/4 | 13-06 I ✓<br>13-15 I ✓<br>14-02 C ✓<br>14-04 I ✓ | E-ZPass tolls (rental).pdf |
| `GT-EZPASS-MIXED` E-ZPass statement mixing trip tolls with commute tolls | 减额后报 | L | 3/3 | 13-09 L ✓<br>13-13 L ✓<br>14-06 L ✓ | E-ZPass statement.pdf |
| `GT-MILEAGE-OFFICE` Mileage from the office to a meeting and back | 照报 | L | 3/3 | 13-09 L ✓<br>13-13 L ✓<br>14-06 L ✓ | mileage_log.txt |
| `GT-MILEAGE-COMMUTE` Commute logged as mileage | 不报 + 说明 | L | 3/3 | 13-09 L ✓<br>13-13 L ✓<br>14-06 L ✓ | mileage_log.txt (不报) |
| `GT-MILEAGE-FROM-HOME` Mileage logged from home when the office is closer | 减额后报 | L | 2/3 | 13-09 L ✗（缺 Comment；缺 flag）<br>13-13 L ✓<br>14-06 L ✓ | mileage_log.txt |
| `GT-MILEAGE-TWO-TRAVELERS` Two colleagues in one car, both logging mileage | 报 + flag | L | 0/3 | 13-09 L ✗（缺 Comment；缺 flag；行缺失）<br>13-13 L ✗（缺 flag；行缺失）<br>14-06 L ✗（缺 Comment；缺 flag） | mileage_log.txt |
| `GT-MILEAGE-AIRPORT-DROPOFF` Spouse drives the traveler to the airport and back | 报 + flag | K | 1/2 | 13-08 K ✗（缺 flag；行缺失）<br>14-06 K ✓ | mileage_log.txt |
| `GT-CAR-IN-LIEU-OF-AIR` Drove 420 miles instead of flying, with the airfare comparison | 减额后报 | N | 2/2 | 13-12 N ✓<br>14-06 N ✓ | Fare comparison at booking (lowest airfare).pdf (不报)<br>mileage_log.txt |
| `GT-DRIVE-200PLUS-NO-QUOTE` Drove more than 200 miles with no cost comparison | 报 + flag | M | 0/2 | 13-11 M ✗（缺 Comment；缺 flag）<br>14-06 M ✗（日期） | mileage_log.txt |
| `GT-PARKING` Parking garage receipt at the meeting venue | 照报 | C M N | 9/9 | 11-01 A ✓<br>11-01 C ✓<br>13-01 A ✓<br>13-01 C ✓<br>13-11 M ✓<br>13-12 N ✓<br>14-02 C ✓<br>14-06 M ✓<br>14-06 N ✓ | Parking receipt.pdf |
| `GT-LIMO-NOAPPROVAL` Black-car service without the VP's written pre-approval in the folder | 报 + flag | B | 3/3 | 11-01 B ✓<br>13-01 B ✓<br>14-02 B ✓ | Executive sedan invoice.pdf<br>Executive sedan invoice.pdf (不报) |
| `GT-LIMO-MEMO` Private sedan service with the VP's written pre-approval | 照报 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Executive sedan invoice (approved).pdf<br>VP approval - private car service.pdf (不报) |
| `GT-STALE-STAFF` Ride receipt from a different trip, more than 60 days old (staff) | 不报 + 说明 | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Uber Chicago Mar 15.pdf (不报) |
| `GT-STALE-STUDENT` Old receipt from an earlier trip (student — 60-day rule waived) | 不报 + 说明 | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | Uber Chicago Apr 21.pdf (不报) |
| `GT-PERSONAL-DETOUR` Ride to a personal destination during the trip | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Uber Jul 29 evening.pdf (不报)<br>Uber Jul 30 evening.pdf (不报) |
| `REG-PLAIN` Conference registration | 照报 | B D H J | 11/11 | 11-01 B ✓<br>11-01 D ✓<br>13-01 B ✓<br>13-01 D ✓<br>13-05 H ✓<br>13-07 J ✓<br>13-11 M ✓<br>14-02 B ✓<br>14-02 D ✓<br>14-03 H ✓<br>14-05 J ✓ | ELDS e.V. registration receipt.pdf<br>MOSS Association registration receipt.pdf<br>MWAI Society registration receipt.pdf<br>NEDS Society registration receipt.pdf<br>NYC Data Week Foundation registration receipt.pdf<br>WCAI Foundation registration receipt.pdf |
| `REG-MEMBERSHIP-PAID` Registration invoice with a paid society membership on it | 拆分 | A | 3/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓ | MOSS Association registration receipt (with membership).pdf |
| `REG-MEMBERSHIP-COMP` Registration with a complimentary ($0) membership line | 照报 | M | 2/2 | 13-03 F ✓<br>14-06 M ✓ | NEDS Society registration receipt.pdf<br>WCAI Foundation registration receipt.pdf |
| `REG-WORKSHOP` Pre-conference tutorial add-on | 照报 | A K | 5/5 | 11-01 A ✓<br>13-01 A ✓<br>13-08 K ✓<br>14-02 A ✓<br>14-06 K ✓ | BayML Foundation tutorial add-on receipt.pdf<br>MOSS Association tutorial add-on receipt.pdf |
| `REG-BANQUET` Optional conference banquet ticket | 报 + flag | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | WCAI Foundation banquet ticket receipt.pdf |
| `REG-PCARD` Registration paid with the GW P-Card | 报 + flag | C | 2/3 | 11-01 C ✗（该不报却报了）<br>13-01 C ✓<br>14-02 C ✓ | SEAM Society registration receipt (P-Card).pdf (不报) |
| `REG-ABSTRACT-FEE` Abstract submission / publication fee | 报 + flag | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | ICML-East Organizing Committee abstract fee receipt.pdf<br>NEDS Society abstract fee receipt.pdf |
| `REG-MEMBERSHIP-ONLY` Society membership dues on their own | 报 + flag | G | 2/3 | 13-04 G ✗（该不报却报了）<br>13-14 G ✓<br>14-03 G ✓ | NEDS Society membership dues receipt.pdf (不报)<br>NEMS Society membership dues receipt.pdf (不报) |
| `REG-VIRTUAL` Online-only conference registration | 报 + flag | E | 1/2 | 13-02 E ✗（该不报却报了）<br>14-02 E ✓ | Virtual workshop registration receipt.pdf (不报) |
| `OTH-HOTEL-INTERNET-SEPARATE` Hotel Wi-Fi day pass receipt | 照报 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Hotel Wi-Fi day pass receipt.pdf |
| `OTH-PHONE-ROAMING` Mobile roaming charges | 报 + flag | B | 2/3 | 11-01 B ✗（缺 flag）<br>13-01 B ✓<br>14-02 B ✓ | Mobile roaming charges.pdf |
| `OTH-POSTER` Poster printing | 报 + flag | A | 2/3 | 11-01 A ✗（缺 flag）<br>13-01 A ✓<br>14-02 A ✓ | Poster printing.pdf |
| `OTH-LUGGAGE-STORAGE` Luggage storage | 照报 | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Luggage storage.pdf |
| `OTH-VALET` Valet parking at the meeting venue | 照报 | D I | 8/8 | 11-01 B ✓<br>11-01 D ✓<br>13-01 B ✓<br>13-01 D ✓<br>13-06 I ✓<br>13-15 I ✓<br>14-02 D ✓<br>14-04 I ✓ | Valet parking at the meeting venue.pdf |
| `OTH-NEWSPAPER` Newsstand receipt | 不报 + 说明 | A | 3/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓ | Newsstand receipt.pdf (不报) |
| `OTH-BOOKS-RESEARCH` Conference proceedings volume | 报 + flag | E | 1/2 | 13-02 E ✗（行缺失）<br>14-02 E ✓ | Conference proceedings volume.pdf |
| `OTH-CARD-LATE-FEE` Credit-card late fee | 不报 + 说明 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | Credit-card late fee.pdf (不报) |
| `OTH-CLOTHING` Clothing bought on the trip | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Clothing bought on the trip.pdf (不报) |
| `OTH-HAIRCUT` Haircut | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Haircut.pdf (不报) |
| `OTH-LUGGAGE-PURCHASE` Replacement suitcase | 不报 + 说明 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Replacement suitcase.pdf (不报) |
| `OTH-TOILETRIES` Pharmacy receipt (toiletries) | 不报 + 说明 | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | Pharmacy receipt (toiletries).pdf (不报) |
| `OTH-MEDICINE` Over-the-counter medicine | 不报 + 说明 | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | Over-the-counter medicine.pdf (不报) |
| `OTH-VACCINATION-REQUIRED` Travel clinic — required vaccination | 报 + flag | E | 1/1 | 14-02 E ✓ | Travel clinic — required vaccination.pdf |
| `OTH-VACCINATION-FLU` Flu shot | 不报 + 说明 | D | 3/3 | 11-01 D ✓<br>13-01 D ✓<br>14-02 D ✓ | Flu shot.pdf (不报) |
| `OTH-GIFT-NOAPPROVAL` Flowers for the session chair | 报 + flag | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | Flowers for the host.pdf (不报)<br>Flowers for the session chair.pdf |
| `OTH-EVENT-DECOR` Table decorations for the GW-hosted reception | 照报 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | Table decorations for the GW-hosted reception.pdf |
| `OTH-CHARITY` Donation receipt | 不报 + 说明 | H | 2/2 | 13-05 H ✓<br>14-03 H ✓ | Donation receipt.pdf (不报) |
| `OTH-LOST-PROPERTY` Replacement of a stolen charger | 不报 + 说明 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Replacement of a stolen charger.pdf (不报) |
| `OTH-DEPENDENT-CARE` Babysitter while away | 不报 + 说明 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Babysitter while away.pdf (不报) |
| `OTH-PET-CARE` Dog boarding | 不报 + 说明 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Dog boarding.pdf (不报) |
| `OTH-CLUB-FEES` Golf with the collaborators | 报 + flag | A | 3/3 | 11-01 A ✓<br>13-01 A ✓<br>14-02 A ✓ | Golf with the collaborators.pdf<br>Golf with the collaborators.pdf (不报) |
| `OTH-ENTERTAINMENT-LAVISH` VIP table at a club for the collaborators, no VP approval in the folder | 报 + flag | G | 2/3 | 13-04 G ✗（缺 Comment）<br>13-14 G ✓<br>14-03 G ✓ | VIP table at a club for the collaborators, no VP approval in<br>VIP table at a club for the collaborators.pdf (不报) |
| `OTH-SUPPLIES` Office supplies bought on the trip | 报 + flag | C | 2/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✗（缺 Comment；缺 flag） | Office supplies bought on the trip.pdf |
| `OTH-SPORTS-EQUIPMENT` Running shoes | 不报 + 说明 | G | 3/3 | 13-04 G ✓<br>13-14 G ✓<br>14-03 G ✓ | Running shoes.pdf (不报) |
| `OTH-ATM-FEE` ATM withdrawal abroad — the operator and foreign-transaction fees are conversion fees | 减额后报 | B | 4/4 | 11-01 B ✓<br>13-01 B ✓<br>14-02 B ✓<br>18-02 P ✓ | ATM withdrawal fee abroad.pdf<br>ATM withdrawal fee abroad.pdf (不报) |
| `OTH-FX-FEE-STATEMENT` Card statement excerpt with foreign-transaction fees | 照报 | B | 0/1 | 14-02 B ✗（商家） | Visa statement excerpt.pdf |
| `OTH-PAYMENT-INDIVIDUAL` Cash paid to a student helper, handwritten receipt | 不报 + 说明 | G | 1/3 | 13-04 G ✗（缺 Comment）<br>13-14 G ✗（缺 Comment；缺 flag）<br>14-03 G ✓ | Handwritten receipt - student helper.txt (不报) |
| `OTH-VENDOR-INVOICE` An unpaid vendor invoice (Net 30) in the folder | 不报 + 说明 | C | 1/3 | 11-01 C ✗（缺 flag；该不报却报了）<br>13-01 C ✗（缺 flag）<br>14-02 C ✓ | Vendor invoice - poster printing.pdf (不报) |
| `OTH-GIFT-MEMO` Flowers for a retiring collaborator, with the dean's written approval | 照报 | J | 2/2 | 13-07 J ✓<br>14-05 J ✓ | Dean approval - retirement gift.pdf (不报)<br>Florist receipt.pdf |
| `DOC-PROGRAM` Conference program (agenda) | 不报 + 说明 | A B J | 4/4 | 13-07 J ✓<br>14-02 A ✓<br>14-02 B ✓<br>14-05 J ✓ | Conference program.pdf (不报) |
| `DOC-APPROVAL-ORPHAN` An approval memo for an expense that is not in the folder | 不报 + 说明 | B | 1/1 | 14-02 B ✓ | Dean approval - premium economy.pdf (不报) |
| `DOC-CARD-DETAIL-ITEMIZED` Card transaction detail WITH items (valid as a receipt for goods) | 报 + flag | E | 1/2 | 13-02 E ✓<br>14-02 E ✗（缺 Comment） | Card transaction detail - adapter.pdf |
| `DOC-CARD-DETAIL-BARE` Card transaction detail WITHOUT items (not a receipt) | 报 + flag | C | 3/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✓ | Card transaction detail - bookstore.pdf (不报) |
| `DOC-NOTES-PERDIEM-DOMESTIC` Traveler asks for per diem on a domestic trip | 报 + flag | D | 1/3 | 11-01 D ✗（缺 flag）<br>13-01 D ✗（缺 flag）<br>14-02 D ✓ | trip_notes.txt (不报) |
| `DOC-NOTES-PURPOSE-INADEQUATE` Notes give only 'Attend conference' as the purpose | 报 + flag | E | 0/2 | 13-02 E ✗（缺 Comment；缺 flag）<br>14-02 E ✗（缺 Comment；缺 flag） | trip_notes.txt (不报) |
| `DOC-DATE-VS-NOTES` Taxi receipt printed after the time the notes say the traveler left the city | 报 + flag | M | 1/1 | 14-06 M ✓ | Boston Cab Dispatch, Inc. receipt Sep 11.pdf |
| `FUND-GRANT-ENTERTAINMENT` Entertainment receipt on a federal grant | 不报 + 说明 | C | 2/3 | 11-01 C ✓<br>13-01 C ✓<br>14-02 C ✗（该不报却报了） | Concert tickets receipt.pdf (不报) |
| `FX-BOTH-CURRENCIES` Taxi card slip showing the local amount AND a dynamic-currency-conversion USD amount | 报 + flag | B | 0/2 | 14-02 B ✗（缺 flag）<br>18-02 P ✗（缺 Comment；缺 flag） | London Black Cab (TfL licensed) card slip (DCC).pdf<br>Taxi Coop Montréal card slip (DCC).pdf |
| `FX-HANDWRITTEN` Foreign receipt with the traveler's handwritten USD conversion | 照报 | E | 2/2 | 13-02 E ✓<br>14-02 E ✓ | Taxi London receipt (handwritten conversion).pdf |
| `TIME-REG-OLD-BUT-FINE` Registration paid 100 days before the trip | 照报 | F | 2/2 | 13-03 F ✓<br>14-02 F ✓ | CanStat Association registration receipt (early bird).pdf<br>PNW Stats Association registration receipt (early bird).pdf |

## 测过但从未通过

- `AIR-SEAT-ECONOMY` Paid advance seat assignment inside economy — 1 次：缺 flag
- `AIR-CHANGE-NOREASON` Fare difference for a changed flight, no reason given — 2 次：缺 Comment；缺 flag；缺 flag
- `LOD-FOLIO-ROOMSERVICE-BIG` Room-service dinner over $75 on the folio, no itemised ticket — 2 次：flag 未写补件；缺 flag
- `TA-INTL-PROVIDED-MEALS` Meals provided abroad (the host's lunch and dinner), deducted from the per diem — 2 次：缺 Comment；缺 flag
- `GT-MILEAGE-TWO-TRAVELERS` Two colleagues in one car, both logging mileage — 3 次：缺 Comment；缺 flag；缺 Comment；缺 flag；行缺失；缺 flag；行缺失
- `GT-DRIVE-200PLUS-NO-QUOTE` Drove more than 200 miles with no cost comparison — 2 次：日期；缺 Comment；缺 flag
- `OTH-FX-FEE-STATEMENT` Card statement excerpt with foreign-transaction fees — 1 次：商家
- `DOC-NOTES-PURPOSE-INADEQUATE` Notes give only 'Attend conference' as the purpose — 2 次：缺 Comment；缺 flag
- `FX-BOTH-CURRENCIES` Taxi card slip showing the local amount AND a dynamic-currency-conversion USD amount — 2 次：缺 Comment；缺 flag；缺 flag

## 从未有效测量


## 纳入的运行

| 批次 | trip | 得分 | 来源 |
|---|---|---|---|
| 20260911-01 | A `trip_a_chicago` | 98.8% | 当时的 score2.txt |
| 20260911-01 | B `trip_b_boston_montreal` | 97.2% | 当时的 score2.txt |
| 20260911-01 | C `trip_c_atlanta_grant` | 91.2% | 当时的 score2.txt |
| 20260911-01 | D `trip_d_sf_student` | 87.5% | 当时的 score2.txt |
| 20260913-01 | A `trip_a_chicago` | 97.6% | 当时的 score.txt |
| 20260913-01 | B `trip_b_boston_montreal` | 100.0% | 当时的 score.txt |
| 20260913-01 | C `trip_c_atlanta_grant` | 97.1% | 当时的 score.txt |
| 20260913-01 | D `trip_d_sf_student` | 88.7% | 当时的 score.txt |
| 20260913-02 | E `trip_e_nyc_london_grant` | 90.6% | 答案快照重算 |
| 20260913-03 | F `trip_f_seattle_staff` | 90.5% | 答案快照重算 |
| 20260913-04 | G `trip_g_boston_paris_staff` | 88.9% | 当时的 score3.txt |
| 20260913-05 | H `trip_h_chicago_toronto_student` | 95.3% | 答案快照重算 |
| 20260913-06 | I `trip_i_atlanta_staff` | 92.5% | 当时的 score.txt |
| 20260913-07 | J `trip_j_nyc_rail_staff` | 94.6% | 答案快照重算 |
| 20260913-08 | K `trip_k_sf_staff` | 96.1% | 答案快照重算 |
| 20260913-09 | L `trip_l_local_dc` | 68.0% | 答案快照重算 |
| 20260913-10 | O `trip_o_london_staff` | 100.0% | 答案快照重算 |
| 20260913-11 | M `trip_m_boston_drive_staff` | 90.5% | 答案快照重算 |
| 20260913-12 | N `trip_n_nyc_drive_staff` | 100.0% | 答案快照重算 |
| 20260913-13 | L `trip_l_local_dc` | 93.1% | 答案快照重算 |
| 20260913-14 | G `trip_g_boston_paris_staff` | 88.9% | 答案快照重算 |
| 20260913-15 | I `trip_i_atlanta_staff` | 100.0% | 答案快照重算 |
| 20260913-16 | O `trip_o_london_staff` | 87.0% | 答案快照重算 |
| 20260914-01 | O `trip_o_london_staff` | 100.0% | 答案快照重算 |
| 20260914-02 | A `trip_a_chicago` | 96.6% | 答案快照重算 |
| 20260914-02 | B `trip_b_boston_montreal` | 96.6% | 答案快照重算 |
| 20260914-02 | C `trip_c_atlanta_grant` | 93.4% | 答案快照重算 |
| 20260914-02 | D `trip_d_sf_student` | 100.0% | 答案快照重算 |
| 20260914-02 | E `trip_e_nyc_london_grant` | 90.7% | 答案快照重算 |
| 20260914-02 | F `trip_f_seattle_staff` | 93.7% | 答案快照重算 |
| 20260914-03 | G `trip_g_boston_paris_staff` | 97.0% | 答案快照重算 |
| 20260914-03 | H `trip_h_chicago_toronto_student` | 92.9% | 答案快照重算 |
| 20260914-04 | I `trip_i_atlanta_staff` | 100.0% | 答案快照重算 |
| 20260914-05 | J `trip_j_nyc_rail_staff` | 100.0% | 答案快照重算 |
| 20260914-06 | K `trip_k_sf_staff` | 94.5% | 答案快照重算 |
| 20260914-06 | L `trip_l_local_dc` | 86.2% | 答案快照重算 |
| 20260914-06 | M `trip_m_boston_drive_staff` | 87.0% | 答案快照重算 |
| 20260914-06 | N `trip_n_nyc_drive_staff` | 100.0% | 答案快照重算 |
| 20260918-01 | R `trip_r_adjunct_no_travel` | 56.8% | 答案快照重算 |
| 20260918-02 | P `trip_p_boston_london_postdoc` | 61.9% | 答案快照重算 |
| 20260918-02 | Q `trip_q_new_faculty_no_travel` | 52.4% | 答案快照重算 |

排除的运行（基础设施故障，未命中不是 agent 的；不计入以上任何统计）：

- 20260914-02 G（API 余额不足，运行中途被截断）
- 20260914-02 H（API 余额不足，未实际运行）
- 20260914-02 I（API 余额不足，未实际运行）
- 20260914-02 J（API 余额不足，未实际运行）
- 20260914-02 K（API 余额不足，未实际运行）
- 20260914-02 L（API 余额不足，未实际运行）
- 20260914-02 M（API 余额不足，未实际运行）
- 20260914-02 N（API 余额不足，未实际运行）
