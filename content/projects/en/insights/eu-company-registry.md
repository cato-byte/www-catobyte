---
title: What 52 million register rows say about Europe's companies
summary: Live results from the company-registry lakehouse. Where companies are, how many really operate, where fishing matters, how long new companies survive, and how clean the data is, from six national registers.
data_url: /en/projects/eu-company-registry/data/
---

<div data-viz="kpis"></div>

Every chart on this page reads the small JSON files the pipeline's last task publishes after each monthly run. The figures in the text are filled in from the same files, so nothing here is typed by hand. Only aggregates leave the lakehouse: no row-level company data, and no names.

## Where companies are

The map places <span data-stat="on_map">50.9M</span> companies and establishments, <span data-stat="on_map_share">97%</span> of the current ones. Switch to the fishing layer, filter by industry or register, and click a town for its breakdown. To keep the files small, the pipeline publishes the 5,000 largest towns and every town with at least one fishing company.

<div data-viz="map"></div>

<div data-viz="industry_mix"></div>

The registers don't describe the same thing. France and Navarra publish *establishments* (every shop, office or site), the other four publish legal entities. France also keeps its closed establishments, so its bronze table is much larger than its live register. Estonia's basic-data file has no activity code at all, which is why it's missing from the industry mix.

## A registered company is not an operating company

The most useful finding is also the least visible one. A company register lists where companies are *registered*, and a lot of them are registered at a formation agent, an accountant or a virtual office.

<div data-viz="activity"></div>

In the UK only <span data-stat="gb_operating">59%</span> of active companies look like they operate where they are registered: <span data-stat="gb_mass">27%</span> sit at an address shared by 50 or more companies, <span data-stat="gb_dormant">12%</span> file dormant accounts, and <span data-stat="gb_strike_off">8%</span> are already on the way to being struck off. A map without this correction mostly shows where company-formation agents are.

<div data-viz="hotspots"></div>

The busiest address, <span data-stat="top_hotspot_address">71-75 Shelton Street, London</span>, hosts <span data-stat="top_hotspot_companies">76,065</span> active companies. The map's *Operating companies* option removes them.

## Fishing hubs

Raw counts rank big cities first, because big cities have many companies of every kind. The location quotient asks a better question: how much more common is fishing among a town's companies than in the country as a whole? It surfaces the ports: Shetland and Orkney, the Hebrides, the north-east coast of Scotland (Fraserburgh, Buckie, Macduff), and on the French side the oyster and mussel coast of Charente-Maritime, the Bay of Mont-Saint-Michel and the Thau lagoon.

<div data-viz="fishing_hubs"></div>

<div data-viz="fishing_jobs"></div>

Navarra is landlocked, so its only fishing units are a few trout farms. Estonia can't take part because its file has no activity codes.

## Births, closures and survival

<div data-viz="demography"></div>

The UK, Norwegian and Estonian bulk files list live companies only. A company created in 2005 and closed in 2010 has simply disappeared, so older years look smaller than they were. The pipeline flags these series as survivorship-biased instead of hiding the problem.

France and Ireland keep closed units with their closure date, so survival can be measured properly: for every year's new companies, the share still alive one, three, five and ten years later.

<div data-viz="survival"></div>

Of the French establishments created in <span data-stat="fr_survival_10y_cohort">2016</span>, <span data-stat="fr_survival_10y">38%</span> were still open ten years later. Irish one-year survival is close to 100% for every cohort. That most likely says more about the register than about the companies: a company leaves the register only at the end of a strike-off or liquidation procedure, which takes months.

<div data-viz="survival_sections"></div>

## Distress by industry

Four registers publish whether a company is in liquidation, insolvent or being struck off. They don't use the same vocabulary, so silver maps them to one shared set of statuses first.

<div data-viz="distress"></div>

## Jobs, not just companies

A company count treats a sole trader and a factory the same way. Norway publishes exact headcounts. France and Navarra publish bands (*20 to 49 employees*), so the pipeline keeps both bounds and the charts show the range instead of inventing a midpoint.

<div data-viz="employment"></div>

## How clean is the data?

<div data-viz="funnel"></div>

<div data-viz="precision"></div>

<span data-stat="fr_address_share">65%</span> of French establishments are placed at their exact address, because INSEE publishes Lambert-93 coordinates and the pipeline converts them to latitude and longitude with native Spark expressions. Everything else is placed at postcode or town level with offline joins against GeoNames, and a background worker upgrades the most useful ones to address precision a few hundred at a time, with free government geocoders.

<div data-viz="dq"></div>

Two rules stand out. Most Irish companies have no valid postcode in the CRO file, so Ireland is placed at district level (Eircode routing key) or town level instead. In the UK, a few thousand company numbers match none of the register's known formats (eight digits, or a two-letter prefix and six digits). The pipeline doesn't guess: those rows go to quarantine with the full record and the failed rule, ready to be inspected and replayed.

<div data-viz="coverage"></div>

## Sources and licences

INSEE SIRENE (Licence Ouverte 2.0), Companies House Basic Company Data (OGL v3), CRO Ireland (CC BY 4.0), Brønnøysund Enhetsregisteret (NLOD 2.0), RIK Estonia (CC BY 4.0), Government of Navarra (CC BY 4.0). Postcode and town centroids: GeoNames (CC BY 4.0). Map tiles: © OpenStreetMap contributors.
