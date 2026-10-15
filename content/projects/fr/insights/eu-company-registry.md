---
title: Ce que disent 52 millions de lignes de registres sur les entreprises européennes
summary: Les résultats en direct du lakehouse des registres d'entreprises. Où sont les entreprises, combien exercent vraiment, où la pêche compte, combien de temps survivent les entreprises nouvelles et quelle est la qualité des données, à partir de six registres nationaux.
data_url: /en/projects/eu-company-registry/data/
---

<div data-viz="kpis"></div>

Chaque graphique de cette page lit les petits fichiers JSON que publie la dernière tâche du pipeline après chaque exécution mensuelle. Les chiffres du texte sont remplis à partir des mêmes fichiers : rien n'est saisi à la main. Seuls des agrégats sortent du lakehouse : aucune donnée d'entreprise ligne à ligne, et aucun nom.

## Où sont les entreprises

La carte place <span data-stat="on_map">50,9 M</span> d'entreprises et d'établissements, soit <span data-stat="on_map_share">97 %</span> des unités courantes. Passez à la couche pêche, filtrez par secteur ou par registre, et cliquez sur une commune pour voir le détail. Pour garder des fichiers légers, le pipeline publie les 5 000 plus grandes communes et toutes celles qui comptent au moins une entreprise de pêche.

<div data-viz="map"></div>

<div data-viz="industry_mix"></div>

Les registres ne décrivent pas la même chose. La France et la Navarre publient des *établissements* (chaque boutique, bureau ou site), les quatre autres des personnes morales. La France conserve aussi ses établissements fermés : sa table bronze est donc bien plus grande que son registre vivant. Le fichier de données de base estonien n'a aucun code d'activité, c'est pourquoi l'Estonie manque à la répartition sectorielle.

## Une entreprise immatriculée n'est pas une entreprise en activité

Le constat le plus utile est aussi le moins visible. Un registre indique où les entreprises sont *immatriculées*, et beaucoup le sont chez un domiciliataire, un expert-comptable ou dans un bureau virtuel.

<div data-viz="activity"></div>

Au Royaume-Uni, seules <span data-stat="gb_operating">59 %</span> des entreprises actives semblent exercer là où elles sont immatriculées : <span data-stat="gb_mass">27 %</span> sont à une adresse partagée par 50 entreprises ou plus, <span data-stat="gb_dormant">12 %</span> déposent des comptes de société dormante et <span data-stat="gb_strike_off">8 %</span> sont déjà en voie de radiation. Sans cette correction, une carte montre surtout où sont les domiciliataires.

<div data-viz="hotspots"></div>

L'adresse la plus chargée, <span data-stat="top_hotspot_address">71-75 Shelton Street, London</span>, héberge <span data-stat="top_hotspot_companies">76 065</span> entreprises actives. L'option *Entreprises en activité* de la carte les écarte.

## Pôles de pêche

Les chiffres bruts placent d'abord les grandes villes, qui ont beaucoup d'entreprises de toutes sortes. Le quotient de localisation pose une meilleure question : à quel point la pêche est-elle plus fréquente parmi les entreprises d'une commune qu'à l'échelle du pays ? Les ports apparaissent alors : Shetland et Orcades, les Hébrides, la côte nord-est de l'Écosse (Fraserburgh, Buckie, Macduff) et, côté français, la côte ostréicole et mytilicole de Charente-Maritime, la baie du Mont-Saint-Michel et l'étang de Thau.

<div data-viz="fishing_hubs"></div>

<div data-viz="fishing_jobs"></div>

La Navarre n'a pas de littoral : ses seules unités de pêche sont quelques piscicultures de truites. L'Estonie ne peut pas être incluse, faute de codes d'activité dans son fichier.

## Créations, fermetures et survie

<div data-viz="demography"></div>

Les fichiers complets du Royaume-Uni, de la Norvège et de l'Estonie ne listent que les entreprises vivantes. Une entreprise créée en 2005 et fermée en 2010 a tout simplement disparu : les années anciennes paraissent donc plus petites qu'elles ne l'étaient. Le pipeline signale ce biais du survivant au lieu de le cacher.

La France et l'Irlande conservent les unités fermées avec leur date de fermeture, ce qui permet de mesurer la survie correctement : pour les entreprises nées chaque année, la part encore en vie un, trois, cinq et dix ans plus tard.

<div data-viz="survival"></div>

Parmi les établissements français créés en <span data-stat="fr_survival_10y_cohort">2016</span>, <span data-stat="fr_survival_10y">38 %</span> étaient encore ouverts dix ans plus tard. En Irlande, la survie à un an est proche de 100 % pour toutes les cohortes. Cela en dit sans doute plus sur le registre que sur les entreprises : une société ne quitte le registre qu'au terme d'une procédure de radiation ou de liquidation, qui dure des mois.

<div data-viz="survival_sections"></div>

## Difficultés par secteur

Quatre registres publient si une entreprise est en liquidation, insolvable ou en cours de radiation. Ils n'utilisent pas le même vocabulaire : silver les ramène d'abord à un ensemble commun de statuts.

<div data-viz="distress"></div>

## Des emplois, pas seulement des entreprises

Un comptage d'entreprises traite de la même façon un auto-entrepreneur et une usine. La Norvège publie des effectifs exacts. La France et la Navarre publient des tranches (*20 à 49 salariés*) : le pipeline garde les deux bornes et les graphiques montrent l'intervalle au lieu d'inventer un point médian.

<div data-viz="employment"></div>

## Les données sont-elles propres ?

<div data-viz="funnel"></div>

<div data-viz="precision"></div>

<span data-stat="fr_address_share">65 %</span> des établissements français sont placés à leur adresse exacte, parce que l'INSEE publie des coordonnées Lambert-93 que le pipeline convertit en latitude et longitude avec des expressions Spark natives. Le reste est placé au code postal ou à la commune par des jointures hors ligne avec GeoNames, et un processus en arrière-plan fait passer les plus utiles à la précision de l'adresse, quelques centaines à la fois, grâce à des géocodeurs publics gratuits.

<div data-viz="dq"></div>

Deux règles ressortent. La plupart des sociétés irlandaises n'ont pas de code postal valide dans le fichier du CRO : l'Irlande est donc placée au district (clé de routage de l'Eircode) ou à la commune. Au Royaume-Uni, quelques milliers de numéros de société ne correspondent à aucun format connu du registre (huit chiffres, ou deux lettres et six chiffres). Le pipeline ne devine pas : ces lignes partent en quarantaine avec l'enregistrement complet et la règle en échec, prêtes à être examinées et rejouées.

<div data-viz="coverage"></div>

## Sources et licences

INSEE SIRENE (Licence Ouverte 2.0), Companies House Basic Company Data (OGL v3), CRO Irlande (CC BY 4.0), Brønnøysund Enhetsregisteret (NLOD 2.0), RIK Estonie (CC BY 4.0), Gouvernement de Navarre (CC BY 4.0). Centroïdes des codes postaux et des communes : GeoNames (CC BY 4.0). Fonds de carte : © contributeurs OpenStreetMap.
