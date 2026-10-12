---
title: Pan-European Company Registry Lakehouse
summary: Integrating the open company registers of six European countries into one Data Vault 2.0 lakehouse on Databricks and AWS, with cleaned, geocoded gold tables.
started: 2026-07
updated: 2026-10-12
status: in_progress
stack: [PySpark, Databricks Serverless, Delta Lake, AWS Lambda, Amazon S3, AWS Location Service, Data Vault 2.0]
cover: images/projects/eu-company-registry.png
cover_alt: Six national company registers flowing through landing, bronze, staging, vault and gold layers
repo: https://github.com/cato-byte/eu-company-registry-lakehouse
---

## At a glance

<ul class="stats"><li><strong>6</strong><span>national registers (FR, IE, UK, NO, EE, ES)</span></li><li><strong>5</strong><span>pipeline layers, landing to gold</span></li><li><strong>6</strong><span>Data Vault entities: hubs, link, satellites</span></li><li><strong>2</strong><span>gold tables for analytics</span></li></ul>

## The problem

Most European countries publish their company register as open data, but each publishes it differently. Formats range from CSV to gzipped JSON, delimiters from commas to semicolons. Column names are in French, Norwegian or Estonian, and date formats, legal forms and status codes all have their own conventions. The identifiers are only unique within their own country.

The goal of this project is a single, queryable model of companies across six countries. Anyone should be able to ask "how many active companies per industry and country?" or put companies on a map, without knowing how each register is structured.

## Data sources

| Country | Register | Publisher | Format | Business key |
|---|---|---|---|---|
| France | Base SIRENE, establishments | INSEE via data.gouv.fr | CSV (zip) | SIRET, falling back to SIREN |
| Ireland | Companies register | Companies Registration Office (CRO) | CSV | Company number |
| United Kingdom | Basic Company Data | Companies House | CSV (zip) | Company number |
| Norway | Enhetsregisteret | Brønnøysund Register Centre | JSON (gzip) | Organisasjonsnummer |
| Estonia | Business register, basic data | Centre of Registers and Information Systems (RIK) | CSV (zip, `;`-delimited) | Registry code |
| Spain | Establishments of Navarra | Government of Navarra open data | CSV | Tax ID (DNI/CIF) |

<div class="callout"><p><strong>A data reality, not a bug:</strong> Spain has no free bulk download of its national register, so the Spanish slice comes from Navarra's regional open-data portal. France and Navarra also publish <em>establishments</em> (sites) rather than legal entities, so their grain differs from the other four sources. The model keeps track of this instead of hiding it.</p></div>

## Architecture

<ol class="pipeline"><li><strong>Ingest</strong><span>One generic Lambda downloads each register, unzips it and lands raw files in S3, partitioned by country.</span><span class="tool">AWS Lambda · S3</span></li><li><strong>Bronze</strong><span>Raw files are read with explicit schemas and stored 1:1 as Delta tables.</span><span class="tool">PySpark · Delta Lake</span></li><li><strong>Staging</strong><span>Each source is mapped to one canonical model, cleaned, and given Data Vault hash keys.</span><span class="tool">PySpark</span></li><li><strong>Raw Vault</strong><span>Hubs, links and satellites integrate all six countries in one model.</span><span class="tool">Data Vault 2.0 · Delta</span></li><li><strong>Gold</strong><span>Latest state per company, incremental geocoding, and an analytics dimension and fact table.</span><span class="tool">PySpark · AWS Location Service</span></li><li><strong>Serve</strong><span>Map and dashboard over the gold tables. A prototype exists and is in progress.</span><span class="tool">Leaflet · JavaScript</span></li></ol>

Everything runs on **Databricks serverless compute on AWS**, reading from and writing to S3. There are no clusters to size or keep alive for a batch workload that runs occasionally.

## Key decisions and why

1. **One config-driven ingestion function.** A single Lambda handles every country. Each source is a small JSON request (URL, country, target file), so adding a country means adding a config file, not new code. Downloads stream to disk in 64 KB chunks, so memory stays flat even for multi-gigabyte registers, and ZIP archives are detected and extracted on the fly.
2. **Explicit schemas, stored next to the data.** Every source has a Spark `StructType` schema in JSON, so nothing relies on `inferSchema`. That avoids an extra full scan of large files, gives the same types on every run, and makes schema drift fail loudly at the bronze layer instead of silently corrupting downstream tables.
3. **Layered Delta Lake storage.** Landing keeps the untouched files, and bronze, staging, vault and gold are Delta tables. Each layer can be rebuilt from the one before it, and when a value looks wrong I can find the exact layer where it changed.
4. **A canonical staging model.** All six sources are mapped to the same 14 business columns (identifier, name, legal form, status, industry, employees, address…) plus lineage columns (`source_country`, `record_source`, `load_timestamp`). Source-specific logic lives in one `select` per country, and everything after staging is country-agnostic.
5. **Country-scoped business keys.** National identifiers are only unique inside their own register. A UK company number can collide with an Irish one, so the company hash key is built from the country *and* the identifier.
6. **Data Vault 2.0 for integration.** Six sources with different attributes and change rates fit naturally into hubs (business keys), links (relationships) and satellites (descriptive attributes with a `hash_diff`). A new source adds rows, not a schema migration.
7. **Geocoding as an incremental satellite.** Calling a geocoding API is the only part of the pipeline that costs money per record. New addresses are found with a `left_anti` join against the coordinates already stored, geocoded through AWS Location Service (with an OpenStreetMap fallback), and appended to a satellite. No address is geocoded twice.

```python
# Country-scoped Data Vault keys, built in the staging layer
.withColumn("hk_company", md5(concat_ws("||", col("source_country"), col("national_id"))))
.withColumn("hk_location", md5(concat_ws("||",
    coalesce(col("address_line"), lit("")),
    coalesce(col("postal_code"), lit("")),
    col("source_country"),
)))
```

## Data cleaning

| Problem in the source data | Example | Rule applied |
|---|---|---|
| Four different date formats | `2024-03-01`, `01/03/2024`, `01.03.2024` | Try each pattern in turn with `coalesce(to_date(...))` |
| Junk in address fields | URLs, e-mails, phone numbers, map coordinates | Regex filter turns them into `NULL` |
| Employee counts published as ranges | `de 20 a 49` | Midpoint of the range (34.5), so it can be summed |
| Status published as booleans | Norway's `konkurs`, `underAvvikling` | Mapped to `BANKRUPT`, `LIQUIDATION`, `ACTIVE` |
| Fields shifted by stray delimiters | Estonian rows with `;` inside the key | Split and recover the key and the name |
| Missing or placeholder business keys | empty, `NONE` | Filtered out *before* hashing |
| Inconsistent casing and whitespace | names, cities | Trimmed and upper-cased |

## Data Vault model

<div class="vault"><div class="vault-entity vault-hub"><p class="kind">Hub</p><p class="name">hub_company</p><p class="cols">hk_company · national_id · source_country</p></div><div class="vault-entity vault-link"><p class="kind">Link</p><p class="name">link_company_location</p><p class="cols">hk_link · hk_company · hk_location</p></div><div class="vault-entity vault-hub"><p class="kind">Hub</p><p class="name">hub_location</p><p class="cols">hk_location · address_line · postal_code · city</p></div><div class="vault-entity vault-sat"><p class="kind">Satellite</p><p class="name">sat_company_profile</p><p class="cols">name · legal form · status · registration date · VAT</p></div><div class="vault-entity vault-sat"><p class="kind">Satellite</p><p class="name">sat_company_metrics</p><p class="cols">industry code · description · employee count</p></div><div class="vault-entity vault-sat"><p class="kind">Satellite</p><p class="name">sat_location_geocodes</p><p class="cols">latitude · longitude · geocoder source</p></div></div>

Profile and metrics are separate satellites because they change at different rates. A company's name and status rarely change, while employee counts are updated every year.

## Deduplication

Duplicates show up at several levels, and each is handled where it occurs:

- **Within a register:** hubs are deduplicated on their hash key, so a company appears once however many times the source repeats it.
- **Across loads:** satellites keep every version. The gold layer selects the latest one per company with a point-in-time window (`row_number()` over `load_timestamp`).
- **Across companies sharing an address:** `hub_location` is keyed on the normalised address, so an office building shared by fifty companies is stored and geocoded once.
- **Join fan-out:** gold keeps one current location per company, so joining dimensions never multiplies rows.

```python
# Point-in-time: latest satellite record per company
latest = Window.partitionBy("hk_company").orderBy(col("load_timestamp").desc())
latest_profile = (
    sat_profile.withColumn("rn", row_number().over(latest))
    .filter(col("rn") == 1)
    .drop("rn")
)
```

## Gold tables

**`dim_companies`**: one row per company, with its current profile, metrics, address and coordinates.

| Column | Description |
|---|---|
| `company_key` | Hash key from the vault (country + national ID) |
| `national_id`, `source_country`, `record_source` | Identity and lineage |
| `company_name`, `legal_form_code`, `company_status`, `registration_date` | Latest profile |
| `industry_code`, `employee_count` | Latest metrics |
| `address_line`, `postal_code`, `city`, `latitude`, `longitude` | Current location, geocoded |

**`fact_country_industry_metrics`**: an aggregate by `source_country`, `industry_code` and `company_status`, with `total_companies` and `total_employees`. It is ready for dashboards without scanning millions of rows.

<!-- bars: companies_by_country.csv -->

<!-- table: fact_country_industry_metrics_sample.csv -->

## Next steps

- **History-preserving loads.** Vault tables are currently rebuilt on each run. The next step is insert-only satellites with a `MERGE` on `hash_diff`, so every change in a register is kept over time.
- **Shared vocabularies.** Map every source's status codes to one set of values, and roll industry codes up to NACE Rev. 2 sections. UK SIC 2007, French NAF, Norwegian SN2007 and Spanish CNAE-2009 are all derived from NACE, so they can be aligned.
- **Cross-border entity resolution.** Match the same group across countries by fuzzy matching on name and address, since VAT numbers are only published by some registers.
- **Production hardening.** Data-quality expectations on each layer, orchestration as a Databricks job, and the AWS resources described as code with Terraform.
- **Dashboard.** Finish the Leaflet map and filters over the gold tables.
