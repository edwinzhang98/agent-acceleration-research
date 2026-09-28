# 2026-09-28 — Cached-read prices of each mainstream vendor's latest model

Trigger: the formula scan's deck to-do (D149) found that Part 1 states "a cached read costs 0.1×" as a flat rule. Edwin decided that the main text gives one example in parentheses, namely the mainstream vendor whose latest model is cheapest, and that the appendix lists every vendor in full, each at its latest model's API price. "Mainstream" is taken here as the five vendors with first-party frontier APIs in the evidence base: Anthropic, OpenAI, Google, xAI and DeepSeek. Mistral, Alibaba (Qwen), Moonshot and Zhipu were not checked. "Cheapest" is read as the cheapest cached read, because that is the quantity the example illustrates.

Method: the official pricing pages were read on 28 Sep 2026 (curl, text extracted; xAI's page renders client-side and was read in the built-in browser). All prices are USD per million tokens, standard tier, short context. Ratios are calc.

## 1. Evidence and verification table

New evidence (same schema as the dossier's evidence tables):

| ID | Figure | Exactly what was measured | Source | Date | Type | Found by | Confidence / notes |
|---|---|---|---|---|---|---|---|
| E224 | **xAI Grok 4.7: input $2.00, cached input $0.50, output $6.00 per 1M tokens → cached read 0.25× input (calc.)** | List price per 1M tokens, standard (us-east-1), prompts ≤200K tokens; model page: "Input Tokens $2.00/ 1M tokens · Cached tokens $0.50/ 1M tokens · Output Tokens $6.00/ 1M tokens"; "We charge different rates for requests which exceed the 200K context window" (those rates not read) | https://docs.x.ai/developers/models/grok-4.7 ; https://docs.x.ai/developers/models ("Meet grok-4.7 … New"; "use Grok 4.7. It is the most capable model we've built"; page "Last updated: September 21, 2026") | Read 28 Sep 2026 | Primary (vendor docs; site titled "SpaceXAI Docs") | cache-price check | ✅ New vendor for the evidence base. Latest model = the one the page labels "New" and recommends; no release date on the page. The page data encode the same prices in units of $0.0001 per 1M tokens (`"promptTextTokenPrice":"20000"`, `"cachedPromptTokenPrice":"5000"`) |
| E225 | **DeepSeek-V4.1-Flash (released 10 Sep 2026): input $0.30 (cache miss), $0.006 (cache hit), output $1.20 per 1M tokens at peak; off-peak exactly half ($0.15 / $0.003 / $0.60) → cached read 0.02× input (calc.)** | Official list price per 1M tokens; "1M INPUT TOKENS (CACHE HIT) OFF-PEAK $0.003 … PEAK $0.006"; "(CACHE MISS) OFF-PEAK $0.15 … PEAK $0.3"; "1M OUTPUT TOKENS OFF-PEAK $0.6 … PEAK $1.2"; "Off-peak rates are half of the peak rates. Peak hours are 01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday"; "The legacy names deepseek-v4-flash and deepseek-v4-flash-vision-exp are still accepted, but the corresponding models have been retired … billed at the Flash price" | https://api-docs.deepseek.com/quick_start/pricing ; https://api-docs.deepseek.com/news/news260910 ("DeepSeek-V4.1-Flash Release 2026/09/10") | Read 28 Sep 2026 | Primary (vendor docs) | cache-price check | ✅ Replaces the OpenRouter-only DeepSeek row of §4.4 (D155). The other listed model, DeepSeek-V4-Pro-0813 (GA 13 Aug 2026), costs $1.32 input, $0.044 cache hit and $3.96 output at peak |

Re-checks of figures the dossier already holds:

| Reference | Recorded as | Primary source says (verbatim; location) | Verdict |
|---|---|---|---|
| §4.4 l. 816, E84 (Claude Opus 5.5) | $4 input, $0.20 cache read, $5.00 5-min write, $20 output; reads 0.05× on Opus 5.5 | Pricing page, model table: "Claude Opus 5.5 … $4 / MTok $20 / MTok $5 / MTok $8 / MTok $0.20 / MTok" (input, output, 5m writes, 1h writes, hits and refreshes); caching table: "Cache read (hit) 0.1x base input price (0.025x on Claude Fable 5.1 and Claude Mythos 5.1; 0.05x on Claude Opus 5.5)" | Confirmed; the 1-hour write is $8 (2×). Opus 5.5 is Anthropic's latest model: the models overview lists Fable 5.1, Opus 5.5, Sonnet 5 and Haiku 4.5 with retirement "Not sooner than September 1, 2027" for Fable 5.1 and "Not sooner than September 22, 2027" for Opus 5.5, which matches the 22 Sep 2026 release date in §4.4 |
| §4.4 l. 821–822 (GPT-6 Sol, GPT-6 Luna) | Sol $2 / $0.20 / $2.50 / $10; Luna $0.10 / $0.01 / $0.125 / $0.50 | Pricing page, short context: "gpt-6-sol $2.00 $0.20 $2.50 $10.00", "gpt-6-luna $0.10 $0.01 $0.125 $0.50" (input, cached input, cache writes, output). Changelog, Sep 22: "Released GPT-6 Sol ( gpt-6-sol ) and GPT-6 Luna ( gpt-6-luna )"; GPT-6 Astra released Sep 3 | Confirmed; Sol and Luna are OpenAI's latest models (same day); cached read 0.1× on both |
| §4.4 l. 826 (Gemini 3.8 Flash) | $0.75 / $0.075 (+$0.50/M tok/h storage) / $3.75, introductory to 31 Dec 2026 | Pricing page: "Input price … $0.75 through December 31, 2026. $1.50 starting January 1, 2027"; "Context caching price … $0.075 through December 31, 2026. $0.15 starting January 1, 2027. $0.50 / 1,000,000 tokens per hour (storage price)"; output "$3.75 … $7.50 starting January 1, 2027" | Confirmed; cached read 0.1× both before and after the price change. Latest Google model: the page's newest text model id is gemini-3.8-flash (release date 2 Sep 2026 from §4.4; the pricing page shows none) |
| Which latest model is cheapest | — | Cached read: DeepSeek-V4.1-Flash $0.006 (peak) < GPT-6 Luna $0.01 < Gemini 3.8 Flash $0.075 < Opus 5.5 and GPT-6 Sol $0.20 < Grok 4.7 $0.50. Normal input: GPT-6 Luna $0.10 < DeepSeek-V4.1-Flash $0.30 (peak; $0.15 off-peak) (calc.) | The main-text example is DeepSeek-V4.1-Flash ($0.006 vs $0.30). Judged on normal input price, GPT-6 Luna would be the cheapest instead |
| Cross-vendor ratio | Deck: "a cached read costs 0.1×" | Cached read ÷ input on each latest model: DeepSeek 0.02×, Anthropic Opus 5.5 0.05×, OpenAI 0.1×, Google 0.1×, xAI 0.25× (calc.) | The flat 0.1× is OpenAI's and Google's rate, not a rule (D156) |

## 2. D-ledger additions

| ID | Claim | Conflict | Resolution |
|---|---|---|---|
| D155 | §4.4 row "DeepSeek V4 Flash (cheapest endpoint) \| $0.09 \| — \| — \| $0.18 \| OpenRouter, 30 Jun 2026 [V]" | DeepSeek's own page (28 Sep 2026) says V4 Flash is retired and its model name is served and billed as DeepSeek-V4.1-Flash, at $0.30 input, $0.006 cache hit and $1.20 output (peak), or half that off-peak. The $0.09 / $0.18 figures are a third-party router's price for the retired model | **Superseded.** Use the official V4.1-Flash row (E225). Router prices stay out of list-price tables |
| D156 | Deck Part 1 (pages 2, 7, 8; Appendix A3-2 row 5-3; A5): "a cached read costs 0.1×"; the formula scan's D149 found the Anthropic exceptions | Across the five vendors' latest models the cached-read share of the input price is 0.02× (DeepSeek), 0.05× (Opus 5.5), 0.1× (OpenAI, Google) and 0.25× (Grok 4.7) (E84, E224, E225, calc.) | **Deck corrected on Edwin's rule:** the main text gives the cheapest example in parentheses (DeepSeek-V4.1-Flash, $0.006 vs $0.30); Appendix A3 lists every vendor's latest model; the page-8 gap between the uncached and cached conventions (and its Appendix A3-3 summary) becomes "4–50× on the read price only, by vendor (calc.)"; A5 reads "0.02–0.25× of a normal read, by vendor". Closes the deck to-do of D149 |

## 3. E-ledger patches (exact replacement text, for v3.1)

- §4.4 (l. 830): replace `| DeepSeek V4 Flash (cheapest endpoint) | $0.09 | — | — | $0.18 | OpenRouter, 30 Jun 2026 [V] |` with `| DeepSeek V4.1 Flash (10 Sep 2026; official, peak rate) | $0.30 | $0.006 | — | $1.20 | Off-peak exactly half ($0.15 / $0.003 / $0.60; peak 01–04 and 06–10 UTC on weekdays); the retired deepseek-v4-flash name is billed as V4.1 Flash (E225, D155) |`.
- §4.4, insert after l. 828 (the Gemini 3.5 Flash-Lite row): `| xAI Grok 4.7 (latest; read 28 Sep 2026) | $2.00 | $0.50 | — | $6.00 | Prompts over 200K tokens billed at higher rates (not read) (E224) |`.
- E84 (l. 326), figure cell: after `writes 1.25× (5-min) / 2× (1-h);` insert ` other vendors' latest models (28 Sep 2026): DeepSeek-V4.1-Flash 0.02×, OpenAI GPT-6 and Gemini 3.8 Flash 0.1×, Grok 4.7 0.25× (E224, E225, D156);`.

## 4. Still open

- Release dates not printed on the pricing pages: Grok 4.7 (no date found), Gemini 3.8 Flash (2 Sep 2026 from §4.4 only), Claude Opus 5.5 (22 Sep 2026 from §4.4, matching the retirement date).
- Grok 4.7's rates above 200K context were not read.
- Vendors outside the five (Mistral, Alibaba Qwen, Moonshot, Zhipu) were not checked. If they count as mainstream, the cheapest example could change.
- The example uses the cheapest cached read. If Edwin means the cheapest model overall, GPT-6 Luna ($0.10 input, $0.01 cached) replaces DeepSeek-V4.1-Flash.
- DeepSeek's peak/off-peak split means its "normal" price depends on the hour; the deck quotes the peak (base) rate.
- The patches above go into v3.1 with the earlier ones (D141–D156).
