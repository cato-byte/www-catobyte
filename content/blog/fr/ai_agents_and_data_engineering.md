## Agents IA et data engineering en 2026 : ce que font vraiment les équipes, ce que cela coûte et ce qui change

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![Agents IA et data engineering en 2026](../../images/ai_agents_and_data_engineering_title_img.png)

*Article technique*

## De l'autocomplétion aux agents

Il y a deux ans, « l'IA pour les développeurs » voulait surtout dire autocomplétion et fenêtre de chat. En 2026, l'outil par défaut est un **agent** : Claude Code, OpenAI Codex, le mode agent de GitHub Copilot, Cursor, Gemini CLI et des outils similaires qui lisent un dépôt, lancent des commandes et des tests, modifient de nombreux fichiers et ouvrent des pull requests, en bouclant jusqu'à ce que la tâche soit terminée ou qu'ils restent bloqués.

L'adoption a été rapide. Dans l'[enquête Stack Overflow 2026 auprès des développeurs](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) (plus de 30 000 réponses), 66 % des développeurs qui utilisent des outils d'IA utilisent des agents de code, Claude Code (66 %) et GitHub Copilot (59 %) sont les agents les plus utilisés, et 73 % des utilisateurs de ces outils s'en servent tous les jours. L'étude Developer Ecosystem 2026 de JetBrains, menée auprès de plus de 15 000 développeurs professionnels, indique que [l'usage professionnel de Claude Code a doublé au premier semestre et que Codex a été multiplié par cinq environ](https://dev.to/jamilxt/claude-code-overtakes-github-copilot-what-jetbrains-survey-of-15000-developers-says-about-ai-3nhc). Les chiffres exacts varient d'une enquête à l'autre, mais pas la tendance.

Les plateformes de données ont suivi. Snowflake, Databricks et Google intègrent désormais des agents dans leurs produits ([Cortex Code de Snowflake](https://www.snowflake.com/en/blog/cortex-code-governed-agent-data-stack/), [les fonctionnalités agentiques de Databricks dans Lakeflow](https://www.databricks.com/blog/lakeflow-new-era-agentic-data-engineering) et l'agent de data engineering de BigQuery), qui écrivent du SQL, construisent des pipelines et expliquent le lignage en s'appuyant sur le catalogue et les permissions de la plateforme.

Cet article porte sur ce que cela signifie pour le data engineering en particulier : ce que les équipes délèguent vraiment aux agents, les compromis, les risques de sécurité et de confidentialité, ce que les entreprises attendent désormais et les pratiques que je recommande pour les adopter. J'utilise des agents tous les jours dans mon propre travail, y compris sur le [lakehouse des registres d'entreprises européens](../projects/eu-company-registry.html) et sur ce site, donc certains exemples sont de première main.

## À quoi les équipes data utilisent vraiment les agents

Les enquêtes auprès des développeurs en général indiquent que l'essentiel de l'usage de l'IA reste l'écriture de code dans des domaines familiers (67 % dans l'enquête Stack Overflow) et le débogage (61 %), et que seulement 20 % utilisent l'IA pour déployer, exploiter ou diagnostiquer des systèmes en production. Dans le travail sur les données, les tâches qui rapportent régulièrement sont celles-ci :

**Écrire et refactoriser du code de transformation.** Les jobs PySpark, les modèles dbt, les migrations SQL et les DAG Airflow conviennent bien aux agents : les modèles sont connus, le code est testable et la boucle de retour (lancer les tests, lire l'erreur, corriger) est exactement ce que les agents font bien. Des refactorisations qui prenaient une semaine, comme passer quarante modèles à une nouvelle convention de nommage ou remplacer une API dépréciée dans tout le code, prennent désormais un après-midi plus la relecture.

**Écrire des tests et des jeux de test.** Les agents sont bons pour générer des tests unitaires, des données synthétiques qui reproduisent les particularités d'une source et les cas limites qu'un humain fatigué oublie (nulls, fichiers vides, clés en double, fuseaux horaires). C'est là que j'ai vu le meilleur retour : plus de tests, ce sont des changements plus sûrs, ce qui rend aussi plus sûre chaque tâche suivante confiée à l'agent.

**Analyser les pannes.** « Le job de nuit a échoué ; voici le log » est un excellent prompt pour un agent. Il peut lire la trace d'erreur, ouvrir le code, consulter les commits récents, interroger la table en cause et proposer un correctif en quelques minutes. C'est particulièrement utile pour les pannes fastidieuses : problèmes d'encodage, ordre des colonnes modifié dans un fichier source, erreur de type après un changement de schéma.

**Comprendre du code et des données inconnus.** Demander à un agent d'expliquer le fonctionnement d'un pipeline existant, de retrouver d'où vient une colonne ou de résumer une procédure stockée de 3 000 lignes économise des heures de lecture. Avec un accès au catalogue (via l'agent d'une plateforme ou un serveur MCP), il peut aussi profiler des tables, trouver des clés de jointure et repérer des distributions suspectes.

**Infrastructure et CI/CD.** Les modules Terraform, les workflows GitHub Actions, les politiques IAM et les Dockerfiles contiennent beaucoup de code répétitif, que les agents écrivent vite. Ce sont aussi ceux qui demandent la relecture la plus attentive, car une erreur ici est un incident de sécurité, pas un mauvais chiffre.

**Documentation et contrats de données.** Descriptions de modèles, documentation des colonnes, runbooks, ADR et README que personne ne voulait écrire sont désormais écrits, et maintenus plus près du code.

**Analytique en langage naturel.** Les interfaces texte vers SQL construites sur une couche sémantique permettent aux utilisateurs métier de poser leurs questions directement. Cela fonctionne bien quand les indicateurs sont définis une seule fois (dans une couche sémantique ou des vues de métriques gouvernées) et mal quand l'agent doit deviner à partir de tables brutes ce que signifie « client actif ».

Ce que les équipes ne confient généralement *pas encore* aux agents : des modifications non supervisées des données de production, les décisions de modélisation et d'architecture sans relecture, tout ce qui touche aux données personnelles sans contrôles stricts, et le dernier mot sur la justesse d'un chiffre.

## Pourquoi le travail sur les données est différent pour les agents

La plupart des discussions publiques sur les agents de code concernent le code applicatif. Le data engineering ajoute des problèmes qu'un agent ne voit pas en lisant le dépôt :

- **La justesse se trouve dans les données, pas dans le code.** Un agent peut écrire une jointure qui compile, passe les tests unitaires et duplique silencieusement des lignes en production parce qu'une clé n'est pas unique dans les données réelles. La relecture de code ne le détecte pas ; les tests de données et le rapprochement, si.
- **État et rayon d'impact.** Un mauvais déploiement d'un service web se défait. Un mauvais `MERGE` dans une table d'historique écrit des données fausses qu'il faut réparer, et les tables en aval les ont peut-être déjà consommées.
- **Coût.** Un agent qui itère sur une requête contre un entrepôt ou un cluster dépense de l'argent réel à chaque tentative. Une boucle qui relance vingt fois une lecture complète d'une table peut coûter plus cher que le temps d'ingénieur économisé.
- **Données sensibles.** Les data engineers travaillent au plus près des données clients. Un agent qui peut interroger des tables de production peut aussi lire des informations personnelles (et les envoyer à un fournisseur de modèles, ou les laisser dans un log).
- **Sémantique.** Les définitions métier, les problèmes de qualité connus et les raisons de filtres étranges vivent souvent dans la tête des gens ou dans des documents épars. Sans ce contexte, un agent produira une logique sûre d'elle, plausible et fausse.

Le fil conducteur : les agents excellent dans les parties du data engineering qui ressemblent au génie logiciel, et ont besoin de beaucoup plus d'encadrement et de vérification pour les parties qui concernent les données.

## Les compromis

### Vitesse contre compréhension

Les agents produisent du code plus vite que les gens ne peuvent le comprendre. Le risque n'est pas le mauvais code en soi ; c'est le code que personne dans l'équipe ne comprend vraiment, ce qui devient un problème la première fois qu'il casse à 3 heures du matin. Les équipes qui s'en sortent bien gardent une règle : vous êtes responsable de ce que vous fusionnez, et vous devez pouvoir l'expliquer.

### Productivité ressentie contre productivité mesurée

Les preuves sur la productivité sont plus nuancées que le marketing. Dans l'[étude randomisée de METR en 2025](https://scienceblog.com/t-a-randomized-trial-by-metr-found-that-experienced-developers-completed-real-coding-tasks-19-slower-when-allowed-to-use-ai-tools-yet-afterwards-they-estimated-on-average-that-ai-had-made-them-20-fast/), des développeurs open source expérimentés étaient 19 % plus lents avec des outils d'IA sur leurs propres projets, tout en pensant avoir été environ 20 % plus rapides. METR qualifie désormais ce résultat d'historique : quand l'organisation a tenté de refaire l'expérience avec des outils plus récents en 2026, beaucoup de développeurs ont refusé de travailler sans IA, ce qui a rendu la nouvelle mesure peu fiable. Les deux faits sont instructifs. Les outils ont beaucoup progressé, mais les gens jugent mal leur propre vitesse : mesurez les résultats (délai de livraison, incidents, reprises), pas les impressions.

### Un amplificateur, pas une solution

Le [rapport DORA 2025 de Google sur le développement logiciel assisté par l'IA](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/), fondé sur près de 5 000 professionnels, décrit l'IA comme un **amplificateur** : elle amplifie les forces des équipes qui ont de bonnes plateformes, des processus clairs et des tests solides, et les dysfonctionnements de celles qui n'en ont pas. Cela correspond à ce que je vois dans les équipes data. Avec une suite de tests rapide, de la CI, de la relecture de code et des conventions claires, les agents multiplient la production. Sans cela, les agents produisent plus de code non testé, plus vite.

### Coût

Les agents ne sont pas gratuits : abonnements ou coûts par token, plus les coûts de calcul quand les agents lancent des requêtes et des jobs. L'enquête Stack Overflow 2026 a constaté que 38 % des organisations fixent déjà des limites d'usage et que 21 % déclarent dépenser davantage pour l'IA. Pour les équipes data, le calcul est le levier principal : donnez aux agents de petits jeux de données de développement et des entrepôts bon marché, pas des environnements à la taille de la production.

### Dépendance

Les équipes qui construisent leur façon de travailler autour de l'agent d'un seul fournisseur, de son format de configuration et de ses intégrations s'exposent à l'enfermement, aux hausses de prix et aux pannes. Gardez la connaissance (conventions, fichiers de contexte, tests, CI) dans le dépôt, dans des formats utilisables par n'importe quel outil, et conservez la capacité de travailler sans l'agent.

## Les risques de sécurité

Les agents combinent trois choses que les spécialistes de la sécurité séparent depuis des décennies : l'accès à des données privées, l'exposition à des contenus non fiables et la capacité d'agir et de communiquer vers l'extérieur. Simon Willison appelle cette combinaison la **triade mortelle** ; la « règle de deux pour les agents » de Meta suggère qu'un agent agissant sans approbation humaine n'en réunisse que deux sur trois au maximum. Le [rapport 2026 de l'OWASP GenAI Security Project](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/) note que les risques liés aux agents sont passés de la théorie aux incidents documentés, l'injection de prompts intervenant dans six des dix catégories de son Top 10 pour les applications agentiques.

Les principaux risques, avec des exemples réels :

**L'injection de prompts.** Tout ce qu'un agent lit peut contenir des instructions : le titre d'une pull request, un ticket, le README d'une dépendance, une page web, une valeur dans une table. En avril 2026, des chercheurs ont montré qu'[un titre de pull request malveillant amenait des agents de relecture d'Anthropic, de Google et de GitHub à divulguer leurs propres clés d'API](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) dans un workflow GitHub Actions. Les data engineers ont une surface d'attaque supplémentaire : les données elles-mêmes. Un champ texte libre dans un système source peut contenir des instructions destinées à un agent qui profilera plus tard cette table.

**L'exposition des secrets.** Les agents s'exécutent avec votre environnement : identifiants cloud, mots de passe de bases de données, tokens dans des fichiers `.env`. Tout ce qui se trouve dans leur contexte peut finir dans un log, un commit, un commentaire ou une requête au fournisseur du modèle. Des logiciels malveillants voleurs d'identifiants ont aussi commencé à [cibler les fichiers de configuration et les tokens des agents](https://botmonster.com/ai/ai-coding-agent-insider-threat-prompt-injection-mcp-exploits/) sur les postes des développeurs.

**Les actions destructrices.** L'exemple le plus connu est l'incident Replit de 2025, où un agent de code a supprimé la base de production d'une entreprise pendant un gel du code. Pour les équipes data, l'équivalent est un agent avec un accès en écriture à la production qui lance `DROP`, `TRUNCATE`, un `DELETE` sans filtre ou `terraform destroy`.

**Les risques liés aux outils et à la chaîne d'approvisionnement.** Les serveurs MCP, plugins et extensions d'agents sont du code qui s'exécute avec les permissions de l'agent. En juin 2026, des chercheurs ont démontré l'[« agentjacking »](https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/) : des instructions glissées dans des événements d'erreur que des agents de code (Claude Code, Cursor, Codex) lisaient via le serveur MCP officiel de Sentry puis exécutaient, en lançant des commandes avec les privilèges du développeur. La même année a vu des paquets malveillants et une faille critique d'exécution de code à distance dans l'infrastructure MCP. Pour les équipes data, la leçon est directe : les logs, les messages d'erreur et le contenu des tables sont des entrées qu'un attaquant peut contrôler. Les agents suggèrent aussi des dépendances, y compris certaines qui n'existent pas (et dont des attaquants enregistrent les noms).

**Le code généré non sécurisé.** Du SQL construit par concaténation de chaînes, des politiques IAM trop larges (`"Action": "*"`), des buckets publics et des vérifications TLS désactivées sont ce que produisent les agents quand ils cherchent avant tout à « faire marcher ».

## Confidentialité du code et des données

Utiliser un agent, c'est envoyer du code, et souvent des données, à un fournisseur de modèles. Voici les questions auxquelles toute équipe devrait répondre avant l'adoption :

- **Nos données servent-elles à l'entraînement ?** Les conditions professionnelles et API des principaux fournisseurs excluent généralement par défaut les données clients de l'entraînement, ce qui n'est pas forcément le cas des offres grand public. Vérifiez les conditions de l'offre exacte que vous utilisez, pas le discours général du fournisseur.
- **Combien de temps sont-elles conservées, et où ?** Les durées de conservation, les options de non-conservation et la localisation des données (traitement dans l'UE, par exemple) varient selon l'offre et le fournisseur. Pour des données soumises au RGPD, il vous faut un accord de traitement des données et savoir où le traitement a lieu.
- **Que voit réellement l'agent ?** Un agent qui exécute `SELECT * ... LIMIT 10` sur une table clients envoie au fournisseur les données personnelles de dix clients. Donnez-lui accès à des données de développement, à des échantillons anonymisés ou synthétiques et à des métadonnées (schémas, statistiques) plutôt qu'à des lignes brutes de production.
- **L'outil est-il approuvé ?** L'« IA fantôme », des ingénieurs qui utilisent des comptes personnels sur du code de l'entreprise, est fréquente. Le rapport de l'OWASP cite des données d'IBM selon lesquelles seulement 37 % des organisations disposent d'une politique pour la détecter. Fournir un outil autorisé avec des règles claires fonctionne mieux qu'interdire des outils que les gens utiliseront de toute façon.
- **Faut-il héberger les modèles nous-mêmes ?** Pour les environnements très sensibles, les options sont des modèles hébergés dans votre propre compte cloud (Amazon Bedrock, Azure, Vertex AI) sous vos accords existants, les agents intégrés aux plateformes qui respectent les permissions du catalogue, ou des modèles à poids ouverts sur votre propre infrastructure, avec des capacités moindres en contrepartie.

## Ce que cela change pour le métier

Le métier évolue, il ne disparaît pas. Écrire du code répétitif ne coûte presque plus rien ; ce qui coûte, c'est de savoir quoi construire, de le spécifier clairement, de le vérifier et de l'exploiter de façon fiable. En pratique, le temps d'un data engineer se déplace vers :

- **La spécification et le découpage :** transformer une demande floue en tâches bien définies, avec des entrées, des sorties et des critères d'acceptation clairs. C'est ce qui rend les agents utiles, et cela a toujours été la partie difficile.
- **La relecture et la vérification :** lire les diffs d'un œil critique, vérifier les plans de requête et, surtout, valider les résultats sur les données. Les tests au niveau des données deviennent plus importants, pas moins.
- **L'ingénierie de plateforme et de contexte :** construire l'environnement dans lequel travaillent les agents, avec des tests rapides, de la CI, des conventions, des couches sémantiques, de la documentation et des limites de permissions. Les équipes data dotées d'une bonne plateforme tirent davantage des agents.
- **La modélisation des données et l'architecture :** les agents savent écrire un schéma en étoile, mais choisir le grain, la stratégie d'historisation et les frontières entre domaines exige toujours de comprendre le métier.
- **La gouvernance :** le contrôle d'accès, le lignage, la confidentialité et la maîtrise des coûts comptent davantage quand des acteurs non humains interrogent et modifient les données.

La partie inconfortable concerne les débutants. Les agents font désormais beaucoup des tâches sur lesquelles les juniors apprenaient, et plusieurs analyses du recrutement font état d'embauches de débutants plus faibles depuis 2023. Les compétences qui permettent d'être recruté changent en conséquence : montrer son jugement (des projets avec des tests, des compromis clairs, des décisions documentées) compte plus que montrer qu'on sait écrire un `GROUP BY`. Les équipes qui cessent complètement de former des juniors découvriront dans quelques années que les seniors n'apparaissent pas de nulle part.

## Ce qu'attendent désormais les entreprises

D'après les offres d'emploi, les entretiens et des échanges avec des responsables du recrutement, les attentes envers les data engineers en 2026 ressemblent à ceci :

- **La maîtrise des agents va de soi.** Plusieurs entreprises ont fait de l'usage de l'IA une attente explicite dès 2025 (le PDG de Shopify a écrit que le recours réflexe à l'IA était une attente de base ; Coinbase a exigé que ses ingénieurs adoptent les outils d'IA). Ne pas les utiliser est de plus en plus perçu comme ne pas utiliser de gestion de versions.
- **Plus de livraisons, avec la même exigence de qualité.** Les équipes attendent davantage de chaque ingénieur, mais les pannes et les chiffres faux sont jugés aussi sévèrement qu'avant. « C'est l'agent qui l'a écrit » n'est pas une excuse.
- **Le jugement plutôt que la syntaxe.** Les entretiens évaluent de plus en plus la conception, le débogage et la relecture de code (souvent généré par l'IA) plutôt que l'écriture d'algorithmes de mémoire.
- **La conscience de la sécurité et des coûts.** Savoir donner à un agent un accès au moindre privilège, garder les secrets hors de sa portée et l'empêcher de brûler du calcul fait désormais partie du métier.
- **La communication.** Rédiger des spécifications précises, des ADR et des commentaires de relecture est devenu une compétence de productivité, car c'est ainsi que l'on délègue le travail, aux personnes comme aux agents.

## Bonnes pratiques pour adopter les agents

Voici les pratiques que je recommanderais à une équipe data qui adopte des agents, à peu près dans cet ordre :

1. **Commencez par la plateforme, pas par l'outil.** Une suite de tests rapide, de la CI sur chaque pull request, la relecture de code et une exécution de bout en bout sur des données synthétiques rendent fiable ce que produit un agent. Si vous ne faites qu'une chose, faites celle-ci.
2. **Écrivez le contexte.** Gardez dans le dépôt un fichier de contexte (`CLAUDE.md`, `AGENTS.md` ou équivalent) avec les conventions, l'architecture, les commandes pour lancer les tests et ce que l'agent ne doit jamais faire. Faites le lien vers les ADR et les contrats de données. Les agents suivent bien mieux les conventions écrites que les conventions implicites.
3. **Moindre privilège par défaut.** Les agents travaillent avec des identifiants, des catalogues et de petits jeux de données de développement. Pas d'accès en écriture à la production, pas de rôle administrateur, pas de clés cloud longue durée dans l'environnement. Les changements en production passent par le même pipeline CI/CD que les changements humains.
4. **Isolez l'exécution.** Exécutez les agents dans des conteneurs, des dev containers ou des sandboxes cloud avec un accès réseau restreint quand c'est possible. Utilisez les modes de permissions de l'outil : laissez lire et tester librement, exigez une approbation pour les écritures, les suppressions, les appels réseau et tout ce qui touche à l'infrastructure.
5. **Traitez toute entrée comme non fiable.** Ne donnez pas aux agents en CI l'accès à des secrets dont ils n'ont pas besoin, évitez `pull_request_target` dans les workflows avec agents sur des dépôts publics, utilisez des tokens en lecture seule pour les agents de relecture, et exigez une approbation humaine pour toute action ayant des effets de bord.
6. **Contrôlez les outils et les dépendances.** N'installez des serveurs MCP et des extensions que depuis des sources de confiance, épinglez leurs versions, examinez les permissions qu'ils obtiennent et vérifiez chaque nouvelle dépendance ajoutée par un agent.
7. **Vérifiez avec les données, pas seulement par la relecture.** Chaque transformation écrite par un agent reçoit des tests de données (unicité, non-nullité, valeurs acceptées, rapprochement du nombre de lignes) et, pour les changements importants, une comparaison des sorties avant et après.
8. **Gardez des humains responsables.** Celui qui fusionne est responsable du changement. Les grosses pull requests générées par des agents sont découpées en morceaux relisibles ; un « LGTM » sur 2 000 lignes n'est pas une relecture.
9. **Maîtrisez les coûts.** Fixez des plafonds de dépense par utilisateur ou par équipe, donnez aux agents de petits entrepôts ou clusters avec arrêt automatique, et surveillez les boucles qui relancent des requêtes coûteuses.
10. **Mesurez.** Suivez le délai de livraison, le taux d'échec des changements, les incidents et les reprises avant et après l'adoption. Les sondages sur la vitesse ressentie ne sont pas des preuves.
11. **Décidez explicitement de la confidentialité.** Utilisez des offres professionnelles aux conditions claires sur les données, documentez quelles données peuvent être envoyées à quel fournisseur, fournissez des outils approuvés et formez les équipes à ce qu'il ne faut pas coller.

## Où cela nous mène

La direction est claire, même si le rythme ne l'est pas : des agents plus autonomes qui travaillent en arrière-plan sur des tâches bien définies (mises à jour de dépendances, couverture de tests, tri des pannes), des agents intégrés à toutes les plateformes de données avec un accès gouverné par le catalogue, et une part croissante du temps de chaque ingénieur consacrée à définir, relire et vérifier le travail plutôt qu'à le taper.

Pour le data engineering, je pense que les équipes qui en profiteront le plus seront celles qui ont déjà fait le travail ingrat : tests, CI, documentation, modèles clairs et gouvernance. Les agents ne remplacent pas ces fondations ; ils les récompensent. La meilleure préparation à la prochaine génération d'agents est la même que pour un nouveau collègue : un code et une plateforme qui rendent facile de bien faire et difficile de mal faire.
