---
title: Pan-European Company Registry Lakehouse
summary: Six national company registers (52 million rows) ingested, cleaned, historised and geocoded on Databricks serverless and AWS, then published as an interactive map and insights that refresh every month.
started: 2026-07
updated: 2026-10-15
status: live
stack: [PySpark, Databricks Serverless, Delta Lake, Unity Catalog, AWS Lambda, Amazon S3, AWS SAM, GitHub Actions, Leaflet]
cover: images/projects/eu-company-registry.png
cover_alt: Six national registers flowing through landing, bronze, silver and gold layers to a map
repo: https://github.com/cato-byte/eu-company-registry-lakehouse
featured: true
highlights:
  - {value: "52M", label: "register rows, refreshed monthly"}
  - {value: "6", label: "national registers, one harmonised model"}
  - {value: "97%", label: "of companies on the map, with free geocoding"}
  - {value: "~200", label: "tests, all runnable on a laptop"}
points:
  - "Ingestion with AWS Lambda and S3, scheduled by EventBridge and deployed with SAM through GitHub OIDC."
  - "Medallion architecture on Databricks serverless: raw bronze, SCD Type 2 silver with one Delta MERGE per snapshot, Kimball gold."
  - "Data-quality engine with quarantine and abort thresholds, schema-drift contracts, ANSI-safe parsing of every register's quirks."
  - "Tiered geocoding with offline joins and free government geocoders, instead of a paid API."
  - "Change detection: an unchanged month costs one small task. CI/CD with tests, approval and service-principal deploys."
  - "Results published as static JSON: a live map and insights on operating companies, fishing hubs and company survival."
---

## At a glance

<ul class="stats"><li><strong>52M</strong><span>register rows in the latest snapshots, from 6 countries</span></li><li><strong>97%</strong><span>of current companies placed on the map, for free</span></li><li><strong>~200</strong><span>tests, all runnable on a laptop</span></li><li><strong>1</strong><span>small task when nothing changed: unchanged data costs almost nothing</span></li></ul>

## The problem

Most European countries publish their company register as open data, and each one does it differently. France publishes a 9 GB CSV of *establishments*, the UK a CSV with headers like ` CompanyNumber` (leading space included), Norway a single 2.8 GB pretty-printed JSON array, Estonia a `;`-delimited file with a byte-order mark. Identifiers, dates, industry codes, statuses and addresses all follow national conventions.

The goal was a pipeline that turns those six registers into one trustworthy model, keeps their history, and answers questions none of them answers alone: where companies really are, which of them actually operate, where fishing matters, how long new companies survive. It had to run unattended every month, cost little, and be testable without a cloud bill.

## Data sources

| Country | Register | Format | Grain | Rows |
|---|---|---|---|---|
| France | INSEE SIRENE, StockEtablissement | CSV, 9.3 GB | establishment | 44.3M |
| United Kingdom | Companies House, Basic Company Data | CSV, 2.6 GB | legal entity | 5.7M |
| Ireland | CRO companies | CSV | legal entity | 0.8M |
| Norway | Brønnøysund, Enhetsregisteret | JSON array, 2.8 GB | legal entity | 1.2M |
| Estonia | RIK e-Business Register, basic data | CSV, `;`, BOM | legal entity | 0.4M |
| Spain | Navarra establishments, yearly panel | CSV, 9 years in one file | establishment | 0.4M |

<div class="callout"><p><strong>Two data realities, made explicit instead of hidden.</strong> Spain has no free bulk national register, so the Spanish slice is Navarra's regional open data. France and Navarra publish establishments (sites), the others legal entities. The model records each source's grain, and every insight states which registers it can and can't use.</p></div>

## Architecture

<ol class="pipeline"><li><strong>Ingest</strong><span>Scheduled Lambdas resolve each register's current URL, stream it to S3 under <code>ingest_date=</code>, skip unchanged files by SHA-256, and rewrite Norway's JSON array as NDJSON.</span><span class="tool">AWS Lambda · EventBridge · S3</span></li><li><strong>Bronze</strong><span>Schema-drift check against a contract, then every column landed as STRING with lineage. Append-only, one table per register.</span><span class="tool">PySpark · Delta Lake</span></li><li><strong>Silver</strong><span>Per-source parsing and cleaning into one canonical model, data-quality rules and quarantine, then one SCD Type 2 MERGE per country and snapshot.</span><span class="tool">PySpark · Delta MERGE</span></li><li><strong>Geo</strong><span>Tiered geocoding: register coordinates, then postcode, district and town joins against GeoNames, plus a background worker on free government geocoders.</span><span class="tool">Spark · Lambda</span></li><li><strong>Gold</strong><span>Kimball star: company dimension, industry dimension, map aggregates and seven insight tables, with explicit country coverage.</span><span class="tool">PySpark · Delta Lake</span></li><li><strong>Publish</strong><span>Small aggregated JSON and GeoJSON written straight into this website's bucket. The <a href="/en/projects/eu-company-registry/insights.html">insights page</a> reads them in the browser.</span><span class="tool">S3 · Leaflet</span></li></ol>

### How the pieces connect

Three systems are involved, and none of them holds another's secrets.

- **GitHub** holds the code. A push to `main` runs the full test suite, waits for my approval in a `production` environment, then deploys twice: the ingestion stack to AWS with SAM, and the Databricks job as an Asset Bundle. AWS access goes through GitHub OIDC, a short-lived role that only that environment can assume, so no AWS key is stored anywhere. Databricks deploys as a service principal over OAuth.
- **AWS** holds the data. EventBridge schedules the downloads (France on the 2nd, the UK and Ireland on the 3rd, and so on), Lambda lands the files in S3, and CloudWatch alarms on any Lambda error.
- **Databricks** holds the compute. The job runs on serverless compute on the 6th of each month and reaches S3 only through Unity Catalog: an IAM role, a storage credential, an external location and a volume. The bucket name never appears in the code or the repository.

The last task writes the website's JSON into the same bucket that serves this site, so the page and its data share one origin. The site is never redeployed for new data, and it never talks to AWS or Databricks at runtime.

## Architectural decisions

**Medallion with SCD2 silver and a Kimball gold, not Data Vault.** The first version of this project was a Data Vault 2.0 model, and I replaced it on purpose. Data Vault pays off when many systems describe the same business keys. Here no key is ever shared: a SIRET and a UK company number never refer to the same company, so every hub was a renamed copy of one register's ID column, and every query became a five or six-way join, each shuffle billed on serverless. The registers publish full snapshots, so history is exactly what an SCD Type 2 merge produces, and Delta already gives the audit trail (time travel, `RESTORE`, Change Data Feed). I kept the Data Vault ideas that earn their place: hash keys, a `hash_diff` for change detection, record source and lineage, and insert-only raw history in bronze.

**Everything lands as text.** Bronze stores every column as STRING. A bad value can never fail a load, and silver can always be rerun with better parsing.

**Downloads outside Spark.** Ingestion is plain Python in Lambda: it resolves URLs that change every month, streams files of several gigabytes without holding them in memory, and refuses a file under half the size of the previous one (that's what a truncated download looks like). Spark only starts when there is data to process.

**Free, tiered geocoding instead of a paid API.** The first version called AWS Location Service from a pandas UDF, with a `sleep` inside the executors. At 52 million rows that's expensive and fragile. Now most companies are placed by joins against an offline gazetteer, in seconds, and precision improves gradually in the background (see *Geocoding* below).

**Static publication instead of an embedded dashboard.** QuickSight and Databricks dashboards both need authentication, embedding setup and a running cost per viewer. A public portfolio page needs none of that. The pipeline exports only aggregates, so no row-level data or names ever leave the lakehouse.

**Pay only for what changed.** The job's first task compares the newest landing files, the gazetteer and the geocoding results with what was last processed. If nothing changed, a condition task ends the run there. If only France changed, only France goes through bronze and silver. Each stage also skips itself when its inputs are unchanged, and a test asserts that a rerun on the same files writes no new table version and no published file.

**Local first.** The whole pipeline runs on a laptop with PySpark 4 and Delta 4, the same versions as serverless, against synthetic fixtures that reproduce every quirk of the real files. Databricks is only used for production volume.

## From raw files to trusted tables: the challenges

### Ingestion

- **Moving targets.** data.gouv.fr and the CKAN portals publish a new URL for every release. Each register has a small JSON request with a *resolver* (`static`, `template`, `datagouv`, `ckan`), so the Lambda finds the current file itself.
- **An unsplittable file.** Norway's register is one 2.8 GB JSON array. Spark would read it in a single task. The Lambda streams it into gzipped NDJSON parts as it downloads, and drops e-mail, phone and website fields on the way.
- **Two notification systems on one bucket.** The geocoding worker was first triggered by S3 events, and the first production deploy failed: Databricks file events already owned an S3 notification rule over the same prefix, and S3 rejects overlapping rules. The worker now runs as a daily sweep of request files that have no result yet, which also retries leftovers.

### Bronze

Before reading a file, its header (or, for NDJSON, its key set) is compared with a contract in `sources.yml`. Reordered columns are logged, added columns are allowed or fatal depending on the source's policy, and removed or renamed columns always stop the run, with a rename suggestion (`codePostalEtablissement → codePostalEtablissment?`). Malformed CSV lines go to `_corrupt_record` instead of shifting every column after them.

### Cleaning

Every cleaning rule traces back to something I found while profiling the real files, and each one is pinned by a test. A few examples:

| Register | What the file contains | What the pipeline does |
|---|---|---|
| Ireland | NACE stored as a float: `311.0` | Integer, left-padded to four digits: `03.11`, marine fishing. Without the pad it reads as 31.1, furniture. |
| Navarra | CNAE `4782.0` in 2021, `4782` in 2022 | Canonicalised *before* hashing. Otherwise every establishment gets a fake new SCD2 version. |
| Navarra | Mojibake in 2022 to 2024: `TravesÃ­a` | Guarded Latin-1 → UTF-8 repair, applied only where the round trip can't throw. |
| Navarra | No establishment ID, and street spelling drifts between years | Key built from tax ID, municipality and the street reduced to its significant letters. |
| France | `[ND]` in any field (person opted out of publication) | Treated as a natural person: no name, no street, no coordinates. |
| France | `1900-01-01` meaning "unknown" | Date sentinel → NULL. |
| UK | SIC as text: `03110 - Marine fishing`, `None Supplied` | Five-digit code → NACE class, placeholders → NULL. |
| Ireland | `********NO ADDRESS DETAILS*******` | Sentinel → NULL. Town parsed from the last address line instead of a hard-coded `DUBLIN`. |
| Estonia | The street is in a different column than its name suggests | Correct column mapped, district rolled up to the city. |
| Norway | Status spread over boolean flags and a deletion date | One derived status with an explicit precedence. |

Parsing is **ANSI-safe**. Serverless runs with ANSI mode on, where a plain `cast` or `to_date` throws on the first bad row and kills the job. The code uses `try_to_timestamp`, `try_cast` and guarded expressions, and a small PySpark linter I wrote for the project fails CI on the throwing variants, on Python UDFs, `collect()`, `cache()` (unsupported on serverless) and other patterns that work locally but fail or cost money in production.

Identifiers are validated with their own check-digit algorithms as native Spark expressions: Luhn for SIREN and SIRET (with La Poste's special rule), mod 11 for Norwegian organisation numbers, the two-pass mod 11 for Estonian registry codes. Property-based tests check each one against a plain Python implementation.

### Silver: quality gates and history

Each row is checked by a single-pass rule engine. A **warning** keeps the row and is counted. An **error** sends it to `silver.quarantine` with the failed rules and the full record as JSON. Each rule can also carry an abort threshold: if 1% of identifiers suddenly fail their checksum, the problem is structural (shifted columns), so the run stops instead of loading garbage. A snapshot with fewer than 80% of the previous row count also stops the run.

History is one Delta `MERGE` per country and snapshot. Changed companies have to be both closed and re-inserted, so they are staged twice, once with a NULL merge key:

```python
(target.alias("t")
    .merge(staged.alias("s"),
           f"t.country_code = '{country}' AND t.is_current AND t.company_key = s._merge_key")
    .whenMatchedUpdate(condition="t.hash_diff <> s.hash_diff", set=close)      # changed: close old version
    .whenNotMatchedInsert(values=insert_values)                                 # new company or new version
    .whenNotMatchedBySourceUpdate(condition=f"t.country_code = '{country}' AND t.is_current",
                                  set=close)                                    # left the register
    .execute())
```

The table enforces its own invariants with CHECK constraints (known countries and statuses, `valid_to >= valid_from`, current rows are open, NACE codes well formed), so a regression in the code can't write an invalid state. It's liquid-clustered on country and industry, and the loader refuses snapshots older than the last one loaded, pointing to `RESTORE` instead.

### Geocoding

Companies are placed at the most precise tier available, and every candidate is checked against the country's bounding box:

1. **Address**, from register coordinates. INSEE publishes Lambert-93 coordinates for about two thirds of French establishments. The projection to latitude and longitude is written as native Spark expressions and verified against PROJ to 1 cm.
2. **Postcode**, **district** and **town**, by joins against the GeoNames gazetteer: full UK postcodes, UK outward codes, Irish Eircode routing keys, town centroids.
3. **Address, gradually.** Each run exports up to 700 of the most valuable coarse locations, fishing companies first. A Lambda geocodes them with free government services (Kartverket for Norway, Maa-amet for Estonia, IGN CartoCiudad for Spain, Nominatim at one request per second elsewhere) and validates every result against the bounding box and, where possible, the register's postcode. The next run merges the results into an insert-only cache, so nothing is geocoded twice.

The result: 97% of current companies are on the map, with no geocoding bill.

### Gold: answers that admit what they don't know

Gold is a Kimball star (`dim_company`, `dim_industry`, map aggregates) plus seven insight tables. The hard part wasn't the SQL, it was knowing what each register can honestly support. The UK, Norwegian and Estonian bulk files list live companies only, so their older years are under-counted and survival can't be measured from them. A `gold.insight_coverage` table lists every country each insight includes or excludes, with the reason, so an unknown is never shown as zero.

### What the first production run taught me

The local suite caught a lot, but production found five more problems, each now covered by a test:

- Parallel tasks created the same tables at the same time. Table creation is now idempotent, and the silver loop runs one country at a time, since all countries merge into one table.
- On Spark Connect, reading a missing path succeeds and only fails when rows are fetched, so a `try` around `load()` never fired. The guards now check eagerly.
- Navarra's 2020 panel has no municipality at all. A data-quality rule stopped that year from loading. The key no longer uses the municipality, and the town is filled from the same establishment's other years.
- `DESCRIBE HISTORY` misparses a column named `location`, so table history is read through the Delta API.
- The OIDC trust failed on the first deploy: repositories with immutable OIDC subjects send `repo:<owner>@<id>/<repo>@<id>`, not `repo:<owner>/<repo>`.

## What the data shows

<div class="callout"><p>The full results, with the interactive map and every chart, are on the <a href="/en/projects/eu-company-registry/insights.html"><strong>insights page</strong></a>. It reads the files the pipeline published on its last run.</p></div>

- **A registered company is not an operating company.** In the UK, only about 59% of active companies look like they operate where they're registered. 27% sit at an address shared by 50 or more companies, and one London address hosts more than 76,000. Without this correction, a company map mostly shows where formation agents are.
- **Fishing hubs appear once counts are normalised.** The location quotient surfaces Shetland, Orkney, the Hebrides and north-east Scotland, and in France the oyster and mussel coast of Charente-Maritime, the Bay of Mont-Saint-Michel and the Thau lagoon.
- **Survival.** Of the French establishments created in 2016, about 38% were still open ten years later, with large differences by industry.
- **The data has a shape.** Every register needed its own fixes, and the data-quality report shows what's left: most Irish companies have no valid postcode, and a few thousand UK company numbers match no known format and wait in quarantine.

## Operations, cost and privacy

- **Orchestration.** One Databricks job with a change gate, for-each tasks per country, per-task timeouts, a duration alert before the timeout, e-mail alerts and `max_concurrent_runs: 1`. Silver never retries: a data-quality failure must stop the run, not repeat it.
- **Cost.** Serverless in cost-optimised mode, unchanged inputs skipped at every level, no Python UDFs, no geocoding API inside Spark. A small estimator predicts the DBUs of a run from input sizes, and a `cost_report` task records the real cost of every run from `system.billing`, so the estimate can be calibrated against it.
- **Privacy.** The repository is public, so it contains no real data: fixtures are synthetic, generated from the real files' shapes with new identifiers that still pass their check digits. Pre-commit hooks and CI scan for secrets and infrastructure identifiers. In the lakehouse, natural persons keep no name or street, and Spanish personal tax IDs are replaced by a keyed hash.
- **Tests.** About 200: parsers (including property-based tests), one test per register pinning its cleaning decisions, SCD2 lifecycle and idempotency, the data-quality engine, geocoding, the Lambdas, query-plan checks (no UDF, no cartesian product, bounded plan size) and a full end-to-end run on all six registers.

## Next steps

- **More fields.** Estonia's activity codes and France's legal forms and company names are in separate files (RIK EMTAK and INSEE StockUniteLegale). Norway's workplace register would place fishing jobs at the actual site rather than the head office.
- **Calibrate the cost model** from the first months of `system.billing` data.
- **Cross-border groups.** Matching the same group across registers would need fuzzy matching on names and addresses. The silver model leaves room for a link table without remodelling.
