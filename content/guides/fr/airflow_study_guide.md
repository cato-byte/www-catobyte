## Fiche d'étude Apache Airflow

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Apache Airflow : environ 200 questions](../../images/airflow_study_guide_title_img.png)

Environ 200 questions d'entretien sur Apache Airflow, des DAG et opérateurs à la planification, aux sensors, aux assets, aux executors, aux tests, au déploiement et au dépannage. Les réponses suivent Airflow 3 et signalent ce qui a changé depuis Airflow 2, car beaucoup d'entreprises utilisent encore les deux.

La fiche suit un parcours d'apprentissage en cinq étapes. Chaque section est découpée en unités courtes : objectifs d'apprentissage, explication du concept et exemple commenté, puis questions (d'abord de mémorisation, ensuite d'application), un exercice pratique et les points à retenir. Pour **apprendre**, lisez chaque unité du début à la fin. Pour **réviser**, passez en mode révision ou utilisez « Aller aux questions », marquez les réponses à revoir et essayez une révision mixte entre les sections.

<!-- QA -->
<!-- stage: Fondamentaux -->

### Fondamentaux

<!-- unit: À quoi sert Airflow -->

<!-- goals -->

- Expliquer ce que fait un orchestrateur et ce qu'il laisse à d'autres systèmes.
- Comparer Airflow avec cron, Dagster, Prefect et les services managés.

<!-- concept -->

Une plateforme de données compte de nombreux jobs interdépendants : extraire avant de charger, charger avant de transformer, transformer avant de publier. Il faut lancer chaque job au bon moment, dans l'ordre, et réagir quand l'un échoue. C'est l'orchestration, distincte du traitement, ce calcul lourd que font Spark ou un entrepôt.

Airflow est un orchestrateur. Comme les pipelines s'écrivent en Python, ils héritent des pratiques de revue, de test et de déploiement du logiciel. Ses alternatives diffèrent surtout par leur philosophie et par qui opère les serveurs.

<!-- example -->

| Besoin | cron | Airflow |
|---|---|---|
| Lancer une commande à 06:00 | Oui | Oui |
| Charger seulement si l'extraction a réussi | Non | Oui |
| Relancer, alerter, voir historique et logs | Non | Oui |
| Rejouer mars dernier pour une table | Manuel | Backfill |

#### Qu'est-ce qu'Apache Airflow ?

Une plateforme open source pour écrire, planifier et superviser des workflows sous forme de code. Les workflows sont des DAG de tâches définis en Python ; Airflow les exécute selon un planning ou sur événement, dans l'ordre des dépendances, avec relances, journaux, alertes et une interface web. Né chez Airbnb en 2014, c'est un projet Apache de premier niveau.

#### À quoi sert Airflow, et à quoi ne sert-il pas ?

Il sert à orchestrer des workflows batch : ETL/ELT, déclenchement de jobs dans d'autres systèmes (Spark, dbt, Databricks, Snowflake, Glue), pipelines de ML, rapports et maintenance. Ce n'est pas un moteur de traitement de données (le calcul lourd doit se faire dans les systèmes qu'il déclenche), ni un moteur de streaming, et il n'est pas conçu pour des planifications à très haute fréquence, sous la seconde.

#### Que signifie « orchestration », par opposition à « traitement » ?

L'orchestration décide de ce qui s'exécute, quand, dans quel ordre et ce qui se passe en cas d'échec. Le traitement est le calcul effectif sur les données. Airflow orchestre ; Spark, les moteurs SQL et dbt traitent.

#### Qu'apporte l'écriture des workflows sous forme de code ?

Le contrôle de version, la revue de code, les tests, la génération dynamique de tâches, la réutilisation via des fonctions et bibliothèques Python, et la possibilité de déployer les workflows en CI/CD comme n'importe quel logiciel.

#### Quelle est la différence entre Airflow et cron ?

Cron ne fait que lancer des commandes à heure fixe. Airflow ajoute les dépendances entre tâches, les relances, les backfills, l'historique, des journaux centralisés, les alertes, le paramétrage, une interface et l'intégration avec des systèmes externes.

#### Comment Airflow se compare-t-il à Dagster et Prefect ?

Tous trois orchestrent des workflows Python. Airflow est le plus déployé, avec le plus grand écosystème de providers. Dagster est centré sur les assets (on déclare les actifs de données et leur lignage), avec un typage fort et des tests locaux. Prefect mise sur des flux Python dynamiques avec peu de code répétitif. Airflow 3 s'est rapproché des idées de Dagster avec les assets et le versionnage.

#### Quels services Airflow managés existent ?

Amazon MWAA (Managed Workflows for Apache Airflow), Google Cloud Composer, Astronomer (Astro) et l'offre Airflow d'Azure dans Data Factory/Fabric. Ils gèrent le scheduler, les workers, la base de données et les mises à jour.

#### Comment expliquer Airflow à un interlocuteur non technique ?

C'est le planificateur et le régulateur de trafic des traitements de données de l'entreprise : il lance chaque étape au bon moment et dans le bon ordre, réessaie quand quelque chose coince momentanément, et prévient l'équipe quand une intervention humaine est nécessaire.

<!-- challenge -->

Une équipe fait tourner 30 jobs cron sur une VM, et chaque script attend 20 minutes « au cas où » que le précédent ait fini. Citez deux problèmes qu'Airflow résoudrait et un qu'il ne résoudrait pas.

<!-- solution -->

Airflow remplacerait les attentes par de vraies dépendances, les jobs démarrant dès que leurs entrées sont prêtes, et ajouterait relances, alertes et historique. Il ne rendrait pas les scripts plus rapides : le traitement lourd reste dans les moteurs que les tâches appellent.

<!-- takeaways -->

- L'orchestration décide quoi lancer et quand ; le traitement fait le travail.
- Les workflows en code apportent revue, tests et CI/CD aux pipelines.
- Airflow a le plus grand écosystème ; les alternatives diffèrent par le style et l'hébergement.

<!-- unit: DAG, tâches et exécutions -->

<!-- goals -->

- Distinguer DAG, tâches, opérateurs, task instances et DAG runs.
- Lire les états des exécutions et des tâches, dont `upstream_failed`.

<!-- concept -->

Airflow sépare la définition de l'exécution. Dans le code, on définit un DAG : des tâches et leurs dépendances. À chaque planification, Airflow crée un DAG run et, dedans, une task instance par tâche. Les états vivent sur ces objets d'exécution, pas dans le code : la même tâche peut être verte hier et rouge aujourd'hui.

Les dépendances commandent les états : une tâche ne démarre que si ses tâches amont sont dans les états attendus par sa trigger rule. Un échec en amont apparaît donc en aval comme `upstream_failed`, et l'état final du DAG run découle de ses dernières tâches.

<!-- example -->

```text
DAG daily_sales (code)         DAG run 2026-10-17 (runtime)
 extract >> transform >> load   extract    success
                                transform  failed
                                load       upstream_failed  → run: failed
```

#### Qu'est-ce qu'un DAG ?

Un graphe orienté acyclique (Directed Acyclic Graph) : un ensemble de tâches avec des dépendances et sans cycle. Dans Airflow, un DAG porte aussi son planning, sa date de début, ses arguments par défaut, ses tags et d'autres réglages. Chaque exécution crée un DAG run.

#### Qu'est-ce qu'une tâche ?

L'unité d'exécution de base d'un DAG : une instance d'opérateur, une fonction Python décorée (`@task`) ou un sensor. Chaque tâche de chaque DAG run devient une task instance avec son propre état, ses journaux et ses relances.

#### Qu'est-ce qu'un opérateur ?

Un modèle pour une unité de travail, comme `BashOperator`, `PythonOperator`, `SQLExecuteQueryOperator`, `DatabricksRunNowOperator` ou `S3ToRedshiftOperator`. On l'instancie avec des paramètres dans un DAG pour créer une tâche.

#### Qu'est-ce qu'une task instance ?

Une exécution précise d'une tâche pour un DAG run précis (et un index de mapping, pour les tâches mappées). Elle a un état (`scheduled`, `queued`, `running`, `success`, `failed`, `up_for_retry`, `skipped`, `upstream_failed` et d'autres), un numéro de tentative et des journaux.

#### Qu'est-ce qu'un DAG run ?

Une exécution d'un DAG, identifiée par un run ID et une date logique, créée par le planning, un déclenchement manuel, un événement d'asset ou un backfill. Les exécutions planifiées ont un intervalle de données.

#### Quels états un DAG run peut-il avoir ?

`queued`, `running`, `success` et `failed`. L'état d'un DAG run découle de ses tâches finales : il réussit si elles réussissent toutes ou sont ignorées.

#### Que signifie `upstream_failed` ?

Que la tâche ne s'est pas exécutée parce qu'une tâche amont a échoué et que sa trigger rule (par défaut `all_success`) ne pouvait pas être satisfaite.

#### Que fait la mise en pause d'un DAG ?

Un DAG en pause ne crée plus de nouvelles exécutions planifiées ; les tâches en cours se terminent. Les nouveaux DAG sont en pause par défaut (`dags_are_paused_at_creation`) pour ne pas démarrer dès leur déploiement.

<!-- challenge -->

Vous déployez un nouveau DAG quotidien, mais le lendemain matin aucune exécution n'apparaît. Quelle est la raison la plus probable, et que vérifiez-vous ?

<!-- solution -->

Les nouveaux DAG sont en pause par défaut : le scheduler ne crée aucune exécution. Réactivez-le dans l'UI ou avec `airflow dags unpause`. Vérifiez aussi l'absence d'erreurs d'import et un `start_date` dans le passé.

<!-- takeaways -->

- Un DAG est du code ; DAG runs et task instances sont ses exécutions.
- Les états appartiennent aux task instances et DAG runs, pas aux tâches.
- `upstream_failed` désigne un échec plus haut dans le graphe.

<!-- unit: Architecture et Airflow 3 -->

<!-- goals -->

- Décrire les composants d'un déploiement Airflow et ce que chacun stocke ou exécute.
- Résumer ce qu'Airflow 3 a changé pour les auteurs de DAG et les opérateurs.

<!-- concept -->

Airflow est un ensemble de services autour d'une base de données. Le DAG processor transforme les fichiers en DAG sérialisés, le scheduler décide ce qui est dû, executors et workers exécutent les tâches, le triggerer gère les attentes et l'API server sert l'UI et l'API REST. La base de métadonnées est la mémoire commune : la perdre, c'est perdre tout l'état.

Airflow 3 a durci ces frontières : les workers ne touchent plus la base directement mais passent par une API, et les auteurs importent depuis un SDK stable. Les mises à jour sont plus sûres et l'exécution à distance devient possible.

<!-- example -->

```python
# Airflow 3: import everything from the stable Task SDK
from airflow.sdk import dag, task, Asset, Variable
```
```bash
airflow dags list-import-errors     # CLI for debugging
curl -X POST "$AIRFLOW/api/v2/dags/daily_sales/dagRuns" -d '{"logical_date": null}'
```

#### Quels sont les principaux composants d'un déploiement Airflow ?

Le scheduler (décide quoi exécuter et quand), le DAG processor (analyse les fichiers de DAG), l'API server (sert l'interface et l'API REST ; c'était le webserver dans Airflow 2), l'executor et ses workers (exécutent les tâches), le triggerer (exécute les tâches différées) et la base de métadonnées (stocke l'état).

#### Qu'est-ce que la base de métadonnées ?

Une base relationnelle (PostgreSQL ou MySQL en production ; SQLite seulement pour les tests) qui stocke les DAG runs, les task instances, les connexions, les variables, les XCom, les utilisateurs et les DAG sérialisés. C'est la source de vérité de l'état d'Airflow : il faut la sauvegarder et l'entretenir.

#### Quels sont les principaux changements d'Airflow 3 ?

Une nouvelle interface React, le versionnage des DAG (chaque exécution est liée à la version du DAG avec laquelle elle a tourné), le Task SDK et une Task Execution API pour que les workers ne parlent plus directement à la base de métadonnées, `airflow api-server` à la place du webserver, les datasets renommés en assets avec une planification par événements, les backfills gérés par le scheduler, la suppression des SubDAG et des SLA, et `schedule` à la place de `schedule_interval`.

#### Qu'est-ce que le Task SDK ?

L'interface publique et stable pour écrire des DAG dans Airflow 3 (`from airflow.sdk import dag, task, DAG, Asset, Variable`). Elle découple le code des DAG des mécanismes internes d'Airflow et permet d'exécuter les tâches à distance via la Task Execution API, voire dans d'autres langages à l'avenir.

#### À quoi sert la CLI `airflow` ?

À gérer et déboguer Airflow : `airflow dags list|trigger|pause|test`, `airflow tasks test|clear`, `airflow db migrate|clean`, les commandes `airflow connections` et `variables`, `airflow config get-value`, et le démarrage des composants (`scheduler`, `api-server`, `dag-processor`, `triggerer`, `celery worker`).

#### Qu'offre l'API REST ?

Une API stable et versionnée (servie par l'API server) pour déclencher et gérer des DAG runs, lire l'état et les journaux des task instances, gérer connexions, variables et pools, et effacer des tâches. Les pipelines de CI et d'autres systèmes l'utilisent pour s'intégrer à Airflow.

<!-- challenge -->

Un système externe doit lancer un DAG run à la fin d'un export nocturne. Quelle interface proposez-vous, et de quoi l'appelant a-t-il besoin ?

<!-- solution -->

L'API REST pour créer un DAG run, avec les paramètres dans le corps de la requête. L'appelant a besoin d'identifiants autorisés à déclencher ce DAG, idéalement un compte de service dédié, et d'un accès réseau à l'API server.

<!-- takeaways -->

- La base de métadonnées contient tout l'état ; sauvegardez-la.
- Airflow 3 isole les workers derrière une API et expose un Task SDK stable.
- La CLI pour déboguer, l'API REST pour les intégrations.

<!-- unit: Se connecter aux autres systèmes -->

<!-- goals -->

- Expliquer comment s'articulent providers, hooks et connections.
- Décider quand utiliser les Variables et quand s'en passer.

<!-- concept -->

Airflow parle au monde par couches. Un provider apporte tout le nécessaire pour un système. Dedans, les hooks savent ouvrir une session et appeler le système, et les opérateurs utilisent des hooks pour une unité de travail. Les hooks prennent hôte et identifiants dans des connections, retrouvées par `conn_id` : le code ne contient aucun secret et le même DAG marche dans chaque environnement.

Les Variables couvrent le reste de la configuration. Pratiques, mais chaque lecture peut interroger la base : elles vont dans les tâches, pas au niveau supérieur du fichier de DAG.

<!-- example -->

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@task
def list_new_files(prefix: str) -> list[str]:
    hook = S3Hook(aws_conn_id="aws_data")       # credentials come from the connection
    return hook.list_keys(bucket_name="landing", prefix=prefix)
```

#### Qu'est-ce qu'un provider Airflow ?

Un paquet versionné séparément qui ajoute opérateurs, hooks, sensors et connexions pour un système externe : `apache-airflow-providers-amazon`, `-google`, `-databricks`, `-snowflake`, `-postgres`, `-standard` (les opérateurs de base comme `BashOperator` et `PythonOperator` dans Airflow 3) et bien d'autres.

#### Qu'est-ce qu'un hook ?

Une classe qui encapsule la connexion à un système externe et expose des méthodes utilitaires, comme `S3Hook.load_file()` ou `PostgresHook.get_records()`. Les opérateurs utilisent des hooks en interne ; vous pouvez aussi les utiliser dans vos propres tâches Python.

#### Qu'est-ce qu'une connexion ?

Un ensemble enregistré d'identifiants et de paramètres pour un système externe (hôte, utilisateur, mot de passe, schéma, port, JSON extra), référencé par un `conn_id`. Elle peut être stockée dans la base de métadonnées, dans des variables d'environnement (`AIRFLOW_CONN_<ID>`) ou dans un secrets backend.

#### Que sont les Variables Airflow ?

Des valeurs de configuration clé-valeur stockées dans Airflow (base de métadonnées, variables d'environnement `AIRFLOW_VAR_<NOM>` ou secrets backend) et lues avec `Variable.get()`. Les lire au niveau supérieur d'un fichier de DAG provoque un appel à la base ou au backend à chaque analyse : lisez-les dans les tâches ou via les templates.

<!-- challenge -->

Un DAG contient en dur un mot de passe Postgres et lit cinq Variables au niveau supérieur du fichier. Que changez-vous ?

<!-- solution -->

Mettre le mot de passe dans une connection (stockée dans un secrets backend) et utiliser le hook Postgres avec son `conn_id`. Lire les Variables dans les tâches qui en ont besoin, ou via des templates, pour que le parsing n'interroge pas la base.

<!-- takeaways -->

- Les providers regroupent hooks, opérateurs et sensors d'un système.
- Les connections sortent les identifiants du code ; les hooks les utilisent.
- Lisez les Variables à l'exécution, pas au parsing.

### Écrire des DAG

<!-- unit: Définir DAG et tâches -->

<!-- goals -->

- Écrire un DAG avec des tâches TaskFlow et des opérateurs classiques.
- Exprimer dépendances, fan-out et regroupements.

<!-- concept -->

Il existe deux façons de créer des tâches, librement combinables. Les opérateurs classiques sont des objets configurés ; les fonctions TaskFlow sont du Python décoré par `@task`. Avec TaskFlow, passer la valeur de retour d'une tâche à une autre transmet la donnée et crée la dépendance : le graphe suit le code. Sans donnée à transmettre, on trace les arêtes soi-même avec `>>`.

Les task groups gardent lisibles les grands graphes sans changer l'exécution des tâches.

<!-- example -->

```python
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False)
def daily_sales():
    @task
    def extract() -> list[dict]: ...
    @task
    def load(rows: list[dict]): ...
    notify = BashOperator(task_id="notify", bash_command="echo done")
    load(extract()) >> notify       # data edge + explicit edge

daily_sales()
```

#### Comment définir un DAG ?

Avec le décorateur `@dag` sur une fonction, ou avec un gestionnaire de contexte `DAG`. Les tâches créées à l'intérieur appartiennent au DAG.

```python
from datetime import datetime
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False, tags=["sales"])
def daily_sales():
    @task
    def extract() -> list[dict]:
        return [{"id": 1, "amount": 10}]

    @task
    def load(rows: list[dict]) -> None:
        print(f"chargement de {len(rows)} lignes")

    load(extract())

daily_sales()
```

#### Qu'est-ce que la TaskFlow API ?

La façon d'écrire des tâches avec des décorateurs (`@task`, `@task.bash`, `@task.virtualenv`, `@task.docker`, `@task.kubernetes` et d'autres), où les valeurs renvoyées passent automatiquement aux tâches en aval via XCom et où les dépendances sont déduites des appels de fonctions.

#### Quelle est la différence entre `@task` et `PythonOperator` ?

Les deux exécutent une fonction Python. `@task` (TaskFlow) est plus concis, passe les valeurs renvoyées via XCom automatiquement et déduit les dépendances. `PythonOperator` est la forme classique ; on câble XCom et dépendances à la main. On peut mélanger les deux dans un DAG.

#### Comment mélanger tâches TaskFlow et opérateurs classiques ?

Les opérateurs classiques exposent `.output` (un `XComArg`) qu'on peut passer à des fonctions TaskFlow, et les sorties TaskFlow peuvent être passées aux champs templatés des opérateurs classiques. Les dépendances sont déduites de ces liens.

#### Comment définir les dépendances entre tâches ?

Avec les opérateurs de décalage de bits (`extract >> transform >> load`), des listes pour l'éventail et la convergence (`start >> [a, b] >> end`), les fonctions `chain()` et `cross_downstream()`, ou implicitement en passant les sorties TaskFlow en arguments.

#### Qu'est-ce qu'un task group ?

Un moyen de regrouper visuellement et logiquement des tâches dans l'interface (`@task_group` ou `TaskGroup`), avec un préfixe commun pour les identifiants de tâches et des arguments par défaut partagés. Il a remplacé les SubDAG, supprimés dans Airflow 3.

<!-- challenge -->

Dix tables sont chargées par des paires identiques extraire-puis-charger, et toutes doivent finir avant une tâche de synthèse. Esquissez les dépendances.

<!-- solution -->

Un task group par table (extract >> load), puis `[group_1, ..., group_10] >> summary`. Générer les groupes dans une boucle sur la liste des tables tient en quelques lignes.

<!-- takeaways -->

- TaskFlow transmet données et dépendances en un seul appel.
- Utilisez `>>`, des listes et `chain()` quand il n'y a pas de donnée à passer.
- Les task groups organisent le graphe sans changer l'exécution.

<!-- unit: Réglages au niveau du DAG -->

<!-- goals -->

- Définir valeurs par défaut, responsables et documentation pour toutes les tâches.
- Bien choisir `start_date`, `catchup` et les paramètres.

<!-- concept -->

La plupart des réglages sont communs à toutes les tâches d'un DAG : ils vont au même endroit. `default_args` porte relances, responsable et alertes ; le DAG porte calendrier, date de début et catchup. Ces choix décident du premier déploiement : une date passée avec catchup peut lancer des centaines d'exécutions d'un coup.

Responsable, tags et documentation ne coûtent rien et paient lors des incidents, quand quelqu'un qui n'a pas écrit le DAG doit savoir ce qu'il fait et qui appeler. Les params sécurisent les exécutions manuelles en validant l'entrée.

<!-- example -->

```python
default_args = {"owner": "sales-data", "retries": 2, "retry_delay": timedelta(minutes=5)}

@dag(schedule="0 6 * * *", start_date=datetime(2026, 1, 1), catchup=False,
     default_args=default_args, tags=["sales"], doc_md=__doc__,
     params={"full_refresh": Param(False, type="boolean")})
def sales_load(): ...
```

#### Que sont les `default_args` ?

Un dictionnaire d'arguments appliqué à toutes les tâches d'un DAG, comme `owner`, `retries`, `retry_delay`, `email_on_failure` ou `execution_timeout`. Les tâches peuvent les surcharger.

#### Comment définir un owner, et pourquoi est-ce important ?

Avec `owner` dans `default_args`. Il apparaît dans l'interface et les alertes, pour contacter la bonne équipe quand le DAG échoue.

#### Qu'est-ce que `email_on_failure` ?

Un argument de tâche qui envoie un e-mail quand la tâche échoue, via la configuration SMTP. La plupart des équipes préfèrent des callbacks ou notifiers vers Slack ou PagerDuty, pour des alertes plus riches et routables.

#### À quoi servent les tags et `doc_md` ?

Les tags regroupent et filtrent les DAG dans l'interface. `doc_md` attache une documentation Markdown au DAG ou à une tâche, visible dans l'interface, ce qui aide la personne d'astreinte à comprendre ce que fait un DAG.

#### Que signifie `start_date` ?

La date à partir de laquelle le DAG peut être planifié. Ce doit être une date fixe dans le passé, jamais `datetime.now()`, qui changerait à chaque analyse et empêcherait la création d'exécutions.

#### Qu'est-ce que `catchup` ?

Le fait que le scheduler crée ou non des exécutions pour tous les intervalles manqués entre `start_date` (ou la dernière exécution) et maintenant. Dans Airflow 3, la valeur par défaut est `False` ; dans Airflow 2, c'était `True`. Laisser catchup actif sur un DAG avec une date de début ancienne peut lancer des centaines d'exécutions d'un coup.

#### Comment passer des paramètres à un DAG run ?

Avec des `params` déclarés sur le DAG (avec valeurs par défaut et validation JSON Schema optionnelle), présentés sous forme de formulaire lors d'un déclenchement manuel, et lus avec `{{ params.nom }}` ou depuis le contexte.

<!-- challenge -->

Un DAG utilise `start_date=datetime.now()`. Les exécutions n'apparaissent jamais, ou à des heures bizarres. Pourquoi, et quelle correction ?

<!-- solution -->

La date de début change à chaque parsing : le scheduler ne voit jamais d'intervalle complet après elle. Utilisez une date fixe dans le passé, `catchup=False` sauf besoin d'historique, et laissez le calendrier décider.

<!-- takeaways -->

- Mettez les réglages communs des tâches dans `default_args`.
- Utilisez un `start_date` fixe passé ; décidez de `catchup` délibérément.
- Responsables, tags, docs et params facilitent l'exploitation.

<!-- unit: Contrôler le flux -->

<!-- goals -->

- Utiliser trigger rules, branches et short-circuits pour choisir ce qui s'exécute.
- Garantir le nettoyage avec des tâches de setup et teardown.

<!-- concept -->

Par défaut, une tâche ne s'exécute que si tout l'amont a réussi. Les vrais pipelines demandent plus : sauter le travail sans données, choisir un chemin parmi plusieurs, nettoyer même après un échec. Chaque outil change soit les tâches sautées, soit les états amont qu'une tâche accepte.

Le piège : les sauts se propagent. Après une branche, la tâche de jonction doit avoir une trigger rule qui tolère des parents sautés, sinon elle sera sautée aussi. Les paires setup/teardown rendent le nettoyage explicite pour qu'un échec ne laisse pas de clusters allumés.

<!-- example -->

```python
@task.branch
def choose(**context):
    return "full_load" if context["params"]["full_refresh"] else "incremental_load"

join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")
choose() >> [full_load, incremental_load] >> join
```

#### Que sont les trigger rules ?

Des règles qui décident quand une tâche s'exécute selon l'état de ses tâches amont. La règle par défaut est `all_success`. Il existe aussi `all_failed`, `all_done`, `one_success`, `one_failed`, `none_failed`, `none_failed_min_one_success`, `none_skipped` et `always`. Par exemple, une tâche de nettoyage utilise `all_done`.

#### Comment créer des branches dans un DAG ?

Avec `@task.branch` (ou `BranchPythonOperator`), qui renvoie le ou les identifiants des tâches à suivre ; les autres sont ignorées. Une tâche de jonction en aval a besoin d'une trigger rule comme `none_failed_min_one_success` pour ne pas être ignorée elle aussi.

```python
@task.branch
def choose(**context):
    return "full_load" if context["logical_date"].day == 1 else "incremental_load"
```

#### Qu'est-ce que `ShortCircuitOperator` ?

Un opérateur (ou `@task.short_circuit`) qui ignore toutes les tâches en aval quand sa fonction renvoie une valeur fausse, par exemple quand il n'y a pas de nouvelles données.

#### Qu'est-ce que `LatestOnlyOperator` ?

Un opérateur qui ignore ses tâches en aval sauf si l'exécution est la plus récente planifiée, utile pour des tâches comme l'envoi d'un rapport, qui n'ont pas de sens pendant un backfill.

#### Que sont `@setup` et `@teardown` ?

Des décorateurs qui marquent les tâches créant et nettoyant des ressources (un cluster, une table temporaire). Un teardown s'exécute même si le travail intermédiaire échoue, et effacer une tâche relance aussi son setup et son teardown.

<!-- challenge -->

Un DAG crée un cluster temporaire, y exécute trois jobs puis le supprime. Quand un job échoue, le cluster reste allumé. Corrigez.

<!-- solution -->

Marquez la tâche de création avec `@setup` et celle de suppression avec `@teardown`, liées. Le teardown s'exécute quoi qu'il arrive aux jobs, et le DAG run signale toujours l'échec.

<!-- takeaways -->

- Les trigger rules décident quels états amont laissent passer une tâche.
- Les jonctions après une branche exigent une règle tolérant les sauts.
- Setup et teardown garantissent le nettoyage.

<!-- unit: Limites d'exécution et isolation -->

<!-- goals -->

- Borner la durée et la fréquence des tâches et des exécutions.
- Isoler les dépendances et éviter les commandes shell dangereuses.

<!-- concept -->

Une tâche qui se fige, chevauche l'exécution d'hier ou entre en conflit avec les bibliothèques d'Airflow peut faire plus de dégâts qu'une tâche qui échoue. Les timeouts transforment les blocages en échecs clairs. Les limites d'exécutions et `depends_on_past` empêchent le chevauchement d'exécutions qui modifient les mêmes données. Les environnements isolés permettent des bibliothèques qu'Airflow ne peut pas installer.

Les commandes shell sont l'endroit le plus facile pour l'injection et la logique cachée : gardez-les courtes et n'y injectez jamais d'entrée non fiable.

<!-- example -->

```python
@task.virtualenv(requirements=["pandas==2.2.3"], system_site_packages=False,
                 execution_timeout=timedelta(minutes=30))
def score(path: str):
    import pandas as pd       # imports inside the function
    ...
```

#### Comment fixer un timeout sur une tâche ?

Avec `execution_timeout` (un `timedelta`) ; la tâche échoue si elle dure plus longtemps. Un `dagrun_timeout` au niveau du DAG fait échouer toute l'exécution après une durée donnée.

#### Que fait `max_active_runs` ?

Il limite le nombre d'exécutions actives simultanées d'un DAG. Le fixer à 1 garantit des exécutions séquentielles, important pour les pipelines qui dépendent de la sortie de l'exécution précédente.

#### Qu'est-ce que `depends_on_past` ?

Un argument de tâche : s'il vaut `True`, une task instance ne s'exécute que si la même tâche a réussi (ou a été ignorée) dans le DAG run précédent. Il impose un traitement séquentiel au niveau de la tâche.

#### Comment exécuter une tâche dans un environnement Python isolé ?

Avec `@task.virtualenv` (crée un virtualenv avec les dépendances indiquées), `@task.external_python` (utilise un interpréteur existant), `@task.docker` ou `@task.kubernetes` (exécution dans un conteneur). On évite ainsi les conflits de dépendances avec Airflow lui-même.

#### À quoi sert le `BashOperator`, et quel est le risque ?

À exécuter des commandes ou des scripts shell. Le risque est d'injecter dans la commande des entrées non fiables via les templates, et de cacher une logique complexe dans du shell, difficile à tester.

<!-- challenge -->

Un DAG quotidien met à jour des totaux cumulés à partir de la veille. L'exécution d'hier a été lente, celle d'aujourd'hui a démarré quand même et les totaux sont faux. Quels deux réglages l'évitent ?

<!-- solution -->

`max_active_runs=1` pour que les exécutions ne se chevauchent jamais, et `depends_on_past=True` sur la tâche de mise à jour pour qu'elle attende la réussite de la veille. Ajoutez `execution_timeout` pour qu'un blocage échoue au lieu de tout bloquer.

<!-- takeaways -->

- Les timeouts transforment les blocages silencieux en échecs visibles.
- `max_active_runs` et `depends_on_past` imposent l'ordre entre exécutions.
- Isolez les dépendances conflictuelles ; gardez les commandes shell courtes.

<!-- unit: Garder des fichiers de DAG sains -->

<!-- goals -->

- Garder le parsing des DAG rapide et prévisible.
- Générer DAG et tâches dynamiquement sans mauvaises surprises.

<!-- concept -->

Airflow relit les fichiers de DAG en permanence : un fichier de DAG est du code qui s'exécute bien plus souvent que ses tâches. Tout ce qui est au niveau supérieur (une requête, un appel d'API, un import lourd) s'exécute à chaque parsing et ralentit l'ordonnancement pour tous.

La génération dynamique est puissante si ses entrées sont peu coûteuses et stables, comme un YAML dans le dépôt. La stabilité compte car les identifiants sont l'identité : renommer une tâche ou un DAG démarre un nouvel historique.

<!-- example -->

```python
# tables.yaml lives next to the DAG: cheap to read at parse time
for table in yaml.safe_load(open(CONFIG))["tables"]:
    @task(task_id=f"load_{table}")
    def load(name=table): ...
    load()
```

#### Pourquoi le niveau supérieur des fichiers de DAG doit-il rester léger ?

Le DAG processor analyse chaque fichier de DAG à répétition (toutes les 30 secondes par défaut pour les fichiers modifiés). Le code de niveau supérieur, comme des requêtes en base, des appels d'API, `Variable.get()` ou des imports lourds, s'exécute à chaque analyse, ralentit tout le scheduler et sollicite les systèmes externes. Ce travail doit aller dans les tâches.

#### Comment générer des DAG ou des tâches dynamiquement ?

Avec une boucle Python sur une configuration (une liste, un YAML lu sur disque) pour créer des tâches ou plusieurs DAG à l'analyse, ou avec le mapping dynamique de tâches pour l'éventail à l'exécution. Gardez la configuration statique et rapide à lire pour que l'analyse reste rapide et déterministe.

#### Que se passe-t-il quand on renomme une tâche ou un DAG ?

Airflow le traite comme une nouvelle tâche ou un nouveau DAG : l'historique reste sous l'ancien nom. Dans Airflow 3, le versionnage des DAG montre le changement, mais renommer casse toujours la continuité des métriques et de `depends_on_past`.

<!-- challenge -->

Un fichier de DAG construit sa liste de tâches en interrogeant l'entrepôt sur toutes ses tables au niveau supérieur. L'ordonnancement est devenu lent. Que changez-vous ?

<!-- solution -->

Sortir la requête du parsing : écrire la liste des tables dans un fichier de configuration pendant la CI ou dans une tâche séparée, lire ce fichier au parsing, ou utiliser le dynamic task mapping pour qu'une tâche récupère la liste à l'exécution.

<!-- takeaways -->

- Le code de niveau supérieur s'exécute à chaque parsing ; gardez-le trivial.
- Générez les tâches depuis une configuration légère et versionnée.
- Les identifiants sont l'identité ; renommer démarre un autre historique.

<!-- stage: Planification et flux de données -->

### Planification et temps

<!-- unit: Calendriers et timetables -->

<!-- goals -->

- Exprimer des calendriers avec cron, presets, timedeltas et timetables.
- Gérer fuseaux horaires et changements d'heure.

<!-- concept -->

Un calendrier répond à une question : quand créer une nouvelle exécution ? Cron et presets couvrent l'essentiel. Quand la règle dépend d'un calendrier (jours ouvrés, fériés, mois fiscaux), un timetable l'exprime en Python, plutôt qu'une exécution qui démarre puis se saute elle-même.

Les fuseaux ajoutent une subtilité. Airflow stocke tout en UTC, mais les gens pensent en heure locale. Un DAG à fuseau local suit l'horloge locale : certaines heures locales arrivent deux fois ou pas du tout les jours de changement d'heure.

<!-- example -->

```python
import pendulum
@dag(schedule="0 6 * * 1-5",                     # 06:00 Monday to Friday
     start_date=pendulum.datetime(2026, 1, 1, tz="America/Bogota"),
     catchup=False)
def weekday_report(): ...
```

#### Comment planifier un DAG ?

Avec l'argument `schedule` : une expression cron (`"0 6 * * *"`), un preset (`"@daily"`, `"@hourly"`), un `timedelta`, un timetable, une liste d'assets (par événements) ou `None` pour les DAG manuels ou déclenchés de l'extérieur.

#### Qu'est-ce que le preset `@once` ?

Un planning qui crée une seule exécution, utile pour des DAG ponctuels comme des migrations.

#### Comment exécuter un DAG uniquement les jours ouvrés ?

Avec une expression cron comme `0 6 * * 1-5`, ou un timetable personnalisé si les jours fériés comptent. Une tâche de branchement ou de court-circuit peut aussi sauter le traitement les jours fériés d'après une table calendrier.

#### Qu'est-ce qu'un timetable ?

Une classe qui définit un planning personnalisé quand cron ne suffit pas : jours ouvrés seulement, plusieurs horaires selon les jours, calendriers fiscaux. Les timetables fournis sont `CronDataIntervalTimetable`, `CronTriggerTimetable`, `DeltaDataIntervalTimetable` et `MultipleCronTriggerTimetable`.

#### Comment Airflow gère-t-il les fuseaux horaires ?

En interne, tout est stocké en UTC. On peut donner à un DAG une `start_date` avec fuseau (via `pendulum`), et les plannings cron suivent alors ce fuseau, y compris les changements d'heure. L'interface peut afficher l'heure locale.

#### Comment les changements d'heure affectent-ils les plannings ?

Avec une date de début munie d'un fuseau, un cron quotidien à 02 h 30 peut être sauté ou exécuté deux fois les jours de changement, selon l'horloge locale. Planifiez les jobs critiques hors de la plage 01 h–03 h, ou en UTC.

<!-- challenge -->

Une équipe européenne planifie un rapport à 02:30 heure locale. Deux fois par an, il se comporte mal. Que se passe-t-il et que suggérez-vous ?

<!-- solution -->

Au passage à l'heure d'été, 02:30 n'existe pas ; à l'automne, cette heure revient deux fois : l'exécution est sautée ou doublée. Planifiez hors de cette fenêtre (par exemple 04:00) ou en UTC si le métier l'accepte.

<!-- takeaways -->

- Cron et presets pour l'essentiel ; timetables pour les calendriers.
- Airflow stocke en UTC ; un start_date avec fuseau suit l'heure locale.
- Évitez de planifier dans les heures de changement d'heure.

<!-- unit: Dates logiques et intervalles de données -->

<!-- goals -->

- Expliquer pourquoi une exécution quotidienne démarre après le jour qu'elle traite.
- Utiliser l'intervalle de données plutôt que l'heure courante dans les tâches.

<!-- concept -->

Les exécutions planifiées portent sur des périodes de données, pas des instants d'horloge. Une exécution quotidienne couvre une journée complète : elle ne peut démarrer qu'une fois la journée finie, d'où son air d'avoir « un jour de retard ». La date logique et l'intervalle de données disent à la tâche quelle période lui revient.

C'est ce qui rend les relances correctes : une tâche qui lit son intervalle dans le contexte traite les mêmes données quel que soit le moment. Une tâche qui demande l'heure courante traite une période différente à chaque relance ou backfill.

<!-- example -->

```sql
-- templated SQL: always the run's own day
DELETE FROM sales_daily WHERE sale_date = '{{ ds }}';
INSERT INTO sales_daily
SELECT * FROM raw_sales
WHERE sold_at >= '{{ data_interval_start }}' AND sold_at < '{{ data_interval_end }}';
```

#### Qu'est-ce que la date logique ?

La date qui identifie la place d'une exécution dans le planning (anciennement `execution_date`). Pour les plannings par intervalles, c'est le début de l'intervalle de données : une exécution quotidienne du 2026-10-15 démarre une fois cette journée terminée, le 2026-10-16. Dans Airflow 3, les exécutions manuelles peuvent ne pas avoir de date logique.

#### Qu'est-ce qu'un intervalle de données ?

La période de données dont une exécution planifiée est responsable, de `data_interval_start` à `data_interval_end`. L'utiliser dans les requêtes (plutôt que « maintenant ») rend les exécutions reproductibles et les backfills corrects.

```sql
SELECT * FROM orders
WHERE created_at >= '{{ data_interval_start }}' AND created_at < '{{ data_interval_end }}'
```

#### Pourquoi un DAG quotidien s'exécute-t-il « avec un jour de retard » ?

Parce qu'avec la planification par intervalles, une exécution démarre à la fin de son intervalle : elle traite une journée complète, donc ne peut démarrer qu'une fois la journée terminée. Dans Airflow 3, les plannings cron utilisent par défaut `CronTriggerTimetable`, qui s'exécute à l'heure du cron sans sémantique d'intervalle, ce qui surprend moins.

#### Pourquoi les tâches ne doivent-elles pas utiliser `datetime.now()` ?

Parce que les relances et les backfills traiteraient la mauvaise période. Utilisez la date logique ou l'intervalle de données du contexte ou des templates.

#### Comment passer à une tâche la date de la dernière exécution réussie ?

Avec les variables de template `prev_data_interval_start_success` et `prev_data_interval_end_success` (ou `prev_start_date_success`), utiles pour des chargements incrémentaux qui doivent reprendre au dernier point réussi.

#### Que se passe-t-il si une exécution dure plus longtemps que l'intervalle de planification ?

L'exécution suivante démarre à son heure si `max_active_runs` le permet, donc les exécutions peuvent se chevaucher. Fixez `max_active_runs=1` (et éventuellement `depends_on_past=True`) quand elles ne doivent pas se chevaucher.

<!-- challenge -->

Un DAG horaire filtre `WHERE updated_at > now() - interval '1 hour'`. Après une panne, les relances ne chargent rien. Réécrivez la logique du filtre.

<!-- solution -->

Filtrez sur l'intervalle de l'exécution : `updated_at >= data_interval_start AND updated_at < data_interval_end`, passé par templates. Chaque relance recharge exactement son heure, quel que soit le moment où elle tourne.

<!-- takeaways -->

- Une exécution traite son intervalle de données, une fois celui-ci terminé.
- Prenez les dates dans le contexte, jamais dans l'horloge.
- Les exécutions longues peuvent se chevaucher ; limitez-les si besoin.

<!-- unit: Backfills, relances et idempotence -->

<!-- goals -->

- Choisir entre catchup, backfills, nettoyage de tâches et déclenchements manuels.
- Rendre les tâches idempotentes pour retraiter sans risque.

<!-- concept -->

Les pipelines sont relancés en permanence : bugs, pannes, données tardives, changements de logique. Airflow offre plusieurs moyens, du nettoyage d'une tâche au backfill de plusieurs mois, mais tous supposent la même chose : exécuter deux fois une tâche pour le même intervalle laisse le même résultat.

Cette propriété, l'idempotence, dépend de l'écriture du chargement, pas d'Airflow. Écrasez ou fusionnez la tranche de l'intervalle au lieu d'ajouter, et utilisez l'intervalle plutôt que l'horloge. Le retraitement devient une routine et non un chantier de nettoyage.

<!-- example -->

```bash
# reprocess Q1 with at most 4 concurrent runs
airflow backfill create --dag-id sales_load \
  --from-date 2026-01-01 --to-date 2026-03-31 --max-active-runs 4
```

#### Qu'est-ce qu'un backfill ?

L'exécution d'un DAG pour des intervalles passés, par exemple après l'ajout d'un DAG ou la correction d'un bug. Dans Airflow 3, les backfills sont créés via l'interface, l'API ou `airflow backfill create` et exécutés par le scheduler, avec des options de retraitement et de concurrence.

#### Quelle est la différence entre catchup et backfill ?

Le catchup est automatique : le scheduler crée les exécutions manquées depuis la dernière. Un backfill est une demande explicite pour une plage de dates, qui peut aussi réexécuter des intervalles déjà réussis.

#### Comment effacer et relancer des tâches ?

Dans l'interface ou la CLI, effacer (clear) une task instance réinitialise son état pour que le scheduler la relance, éventuellement avec les instances en aval, en amont, passées ou futures. C'est la manière habituelle de retraiter après une correction.

#### Qu'est-ce qu'un déclenchement manuel, et comment le faire ?

Démarrer un DAG run en dehors de son planning depuis l'interface, la CLI (`airflow dags trigger`) ou l'API REST, éventuellement avec une configuration ou des paramètres.

#### Que signifie « tâche idempotente » dans Airflow ?

Une tâche qui produit le même résultat qu'elle s'exécute une ou plusieurs fois pour le même intervalle. On l'obtient en traitant l'intervalle de données plutôt que « le dernier », en écrivant par écrasement d'une partition ou `MERGE` plutôt qu'en ajout, et en utilisant des noms de fichiers déterministes.

#### Il faut retraiter six mois de données après une correction. Comment ?

Je m'assure que les tâches sont idempotentes et utilisent l'intervalle de données, puis je crée un backfill pour la plage de dates avec une concurrence limitée (`max_active_runs`) pour ne pas affamer la production, ou j'efface les DAG runs concernés. Je surveille et valide les sorties ensuite.

#### Votre backfill a créé des doublons dans la table cible. Qu'est-ce qui n'allait pas ?

Les tâches n'étaient pas idempotentes : elles ajoutaient des données ou utilisaient « maintenant » au lieu de l'intervalle de données. Réécrivez le chargement pour écraser la partition de l'intervalle ou faire un `MERGE` par clé, supprimez les doublons et relancez.

<!-- challenge -->

Une tâche ajoute les commandes de chaque jour à une table avec `INSERT INTO`. Vous devez rejouer la semaine dernière. Que changez-vous d'abord ?

<!-- solution -->

Rendre le chargement idempotent : supprimer les lignes de l'intervalle puis insérer dans une transaction, faire un `MERGE` sur la clé de commande ou écraser la partition de la date. Puis lancer le backfill de la semaine avec une concurrence limitée.

<!-- takeaways -->

- Le catchup est automatique ; backfills et clears sont explicites.
- L'idempotence vient de l'écrasement ou de la fusion par intervalle.
- Rendez les chargements idempotents avant tout backfill.

### Opérateurs, sensors et tâches différables

<!-- unit: Sensors et attentes entre DAG -->

<!-- goals -->

- Configurer des sensors avec le bon mode et le bon timeout.
- Choisir entre dépendances pull et push entre DAG.

<!-- concept -->

Les pipelines attendent souvent des choses hors de leur contrôle : un fichier, une partition, le DAG d'une autre équipe. Les sensors transforment cette attente en tâche avec une condition de réussite. Le prix : un slot de worker pendant toute l'attente, sauf si le sensor le libère entre deux vérifications.

Entre DAG, on peut attendre (un sensor dans le DAG aval tire) ou déclencher (un opérateur dans le DAG amont pousse). Le pull garde les équipes indépendantes mais couple les calendriers ; le push supprime l'attente mais oblige l'amont à connaître ses consommateurs.

<!-- example -->

```python
wait = S3KeySensor(
    task_id="wait_for_orders",
    bucket_key="s3://landing/orders/{{ ds }}/_SUCCESS",
    mode="reschedule", poke_interval=300, timeout=6 * 3600,
)
```

#### Qu'est-ce qu'un sensor ?

Un opérateur spécial qui attend une condition : un fichier dans S3 (`S3KeySensor`), une partition, une tâche externe, une requête SQL qui renvoie des lignes, un endpoint HTTP, une heure. Il vérifie périodiquement jusqu'à ce que la condition soit vraie ou que le timeout expire.

#### Quelle est la différence entre les modes `poke` et `reschedule` ?

En mode `poke`, le sensor occupe un slot de worker pendant toute l'attente, en dormant entre les vérifications. En mode `reschedule`, il libère le slot entre les vérifications et est replanifié plus tard, ce qui convient mieux aux longues attentes. Le mode différable est encore meilleur.

#### Qu'est-ce que le timeout d'un sensor, et pourquoi le fixer ?

La durée maximale d'attente d'un sensor avant échec (`timeout`, sept jours par défaut). Donnez-lui une valeur réaliste pour qu'un fichier amont manquant soit remarqué vite au lieu de bloquer des ressources pendant des jours. `soft_fail=True` marque le sensor comme ignoré au lieu d'échoué.

#### Qu'est-ce que `@task.sensor` ?

Un décorateur qui transforme une fonction Python en sensor : elle renvoie `True` (ou un `PokeReturnValue`) quand la condition est remplie, avec les options habituelles `poke_interval`, `timeout` et `mode`.

#### Qu'est-ce qu'`ExternalTaskSensor` ?

Un sensor qui attend qu'une tâche ou un DAG run d'un autre DAG atteigne un état, pour la même date logique par défaut. Il crée des dépendances entre DAG mais couple les plannings ; les assets sont souvent une alternative plus propre.

#### Qu'est-ce que `TriggerDagRunOperator` ?

Un opérateur qui déclenche un autre DAG, éventuellement en lui passant une configuration et en attendant sa fin. C'est une dépendance de type « push », par opposition au « pull » de l'`ExternalTaskSensor`.

<!-- challenge -->

Vingt sensors en mode `poke` attendent jusqu'à sept jours chacun des fichiers de partenaires. Les workers sont souvent saturés. Que changez-vous ?

<!-- solution -->

Passer les sensors en mode deferrable, ou au moins `reschedule`, pour libérer les slots pendant l'attente. Réduire le timeout à une fenêtre réaliste, par exemple six heures, et alerter à son expiration.

<!-- takeaways -->

- Les sensors attendent des conditions ; leur mode fixe le coût en slots.
- Fixez toujours un timeout réaliste.
- Les liens entre DAG peuvent tirer (sensor) ou pousser (déclenchement).

<!-- unit: Différer plutôt qu'attendre -->

<!-- goals -->

- Expliquer comment les opérateurs deferrable libèrent les slots des workers.
- Gérer des entrées qui risquent de ne jamais arriver.

<!-- concept -->

La plupart des attentes n'ont pas besoin de CPU : vérifier l'état d'un job chaque minute est peu coûteux, mais y consacrer un processus de worker ne l'est pas. Les opérateurs deferrable confient l'attente au triggerer, un service asynchrone qui surveille des milliers de conditions à la fois, et reviennent sur un worker seulement quand quelque chose s'est produit.

Différer règle le coût, pas la sémantique. C'est toujours à vous de décider ce que signifie l'absence : échouer et alerter, ou sauter parce qu'aucune donnée est un résultat valide.

<!-- example -->

```python
run = DatabricksRunNowOperator(
    task_id="run_job", job_id=1234,
    deferrable=True,          # waits in the triggerer, not on a worker
)
```

#### Que sont les opérateurs différables ?

Des opérateurs qui, pendant qu'ils attendent quelque chose d'externe (un job, un fichier, une heure), se suspendent et confient l'attente à un trigger asynchrone exécuté dans le processus triggerer, libérant le slot du worker. Quand le trigger se déclenche, la tâche reprend sur un worker. De nombreux opérateurs de providers ont `deferrable=True`.

#### Qu'est-ce que le triggerer ?

Un composant qui exécute les triggers asyncio des tâches différées. Un seul triggerer peut gérer des milliers d'attentes simultanées avec peu de ressources.

#### Un sensor attend un fichier qui parfois n'arrive jamais. Comment le gérez-vous ?

Je rends le sensor différable ou j'utilise le mode `reschedule`, je lui donne un timeout réaliste, je décide si l'absence doit échouer (prévenir quelqu'un) ou être ignorée (`soft_fail`), et je préviens le responsable de la source. Je documente l'heure d'arrivée attendue.

<!-- challenge -->

Après une mise à jour, des tâches deferrable restent indéfiniment à l'état `deferred`. Quel composant vérifiez-vous d'abord ?

<!-- solution -->

Le triggerer. Les tâches différées ne reprennent que lorsqu'un triggerer actif déclenche leur trigger : vérifiez que le service est déployé, en bonne santé et doté des providers nécessaires, puis consultez ses logs.

<!-- takeaways -->

- Différer déplace les attentes des workers vers le triggerer.
- Sans triggerer actif, les tâches différées ne reprennent pas.
- Décidez explicitement si l'absence de données échoue ou saute.

<!-- unit: Opérateurs de données et d'API -->

<!-- goals -->

- Exécuter du SQL et des appels HTTP depuis Airflow avec des connections.
- Savoir quand les opérateurs de transfert aident et quand ils nuisent.

<!-- concept -->

Beaucoup de tâches sont de fines enveloppes autour d'un appel à un autre système : exécuter ce SQL, appeler cette API, copier ce fichier. Les opérateurs des providers font l'appel et réutilisent une connection pour les identifiants : la tâche n'a besoin que de paramètres, souvent templatés avec les dates de l'exécution.

Le risque est de faire transiter les données par le worker. Les opérateurs de transfert conviennent aux volumes modestes ; les gros déplacements doivent se faire dans les systèmes eux-mêmes, comme un `COPY` dans l'entrepôt ou un `UNLOAD` Athena.

<!-- example -->

```python
SQLExecuteQueryOperator(
    task_id="build_daily",
    conn_id="warehouse",
    sql="sql/build_daily.sql",                 # templated with {{ ds }}
)
```

#### Comment appeler une base SQL depuis Airflow ?

Avec `SQLExecuteQueryOperator` (provider common SQL) et une connexion, ou avec le hook spécifique du provider dans une tâche Python. Gardez le SQL dans des fichiers `.sql` séparés, référencés via les templates.

#### Que sont les opérateurs de transfert ?

Des opérateurs qui déplacent des données entre deux systèmes en une seule tâche, comme `S3ToRedshiftOperator`, `GCSToBigQueryOperator`, `SqlToS3Operator` ou `S3ToSnowflakeOperator`. Ils délèguent généralement le travail au système cible (par exemple une commande `COPY`).

#### À quoi sert `HttpOperator` ?

À appeler des API HTTP avec une connexion définissant l'URL de base et les identifiants, avec contrôles de réponse et pagination optionnels. `HttpSensor` attend qu'un endpoint renvoie une condition.

#### Comment lancer une requête Athena depuis Airflow ?

Avec `AthenaOperator`, qui soumet la requête, attend sa fin et écrit les résultats à l'emplacement de sortie S3 configuré. Utilisez des dates templatées dans la requête pour traiter l'intervalle de données.

<!-- challenge -->

Un `SqlToS3Operator` exporte chaque nuit une table de 200 Go et le worker manque de mémoire. Que changez-vous ?

<!-- solution -->

Laisser la base faire l'export : utiliser sa commande native d'unload ou d'export (par exemple `UNLOAD` dans Redshift ou `COPY INTO` vers un emplacement dans Snowflake) via un opérateur SQL. Le worker émet seulement la commande et attend.

<!-- takeaways -->

- Opérateurs et connections réduisent les tâches à des paramètres.
- Gardez le SQL dans des fichiers versionnés et templatés.
- Les gros déplacements de données se font dans les systèmes de données.

<!-- unit: Déclencher des moteurs externes -->

<!-- goals -->

- Lancer du travail Databricks, dbt, Glue et Kubernetes depuis Airflow.
- Combiner plusieurs moteurs dans un pipeline.

<!-- concept -->

Airflow excelle comme chef d'orchestre d'autres moteurs. Chaque moteur a un opérateur qui soumet le travail, attend (idéalement en différé) et signale succès ou échec : le DAG se lit comme un plan pendant que le calcul se fait ailleurs.

Quand le travail a des dépendances que l'environnement d'Airflow ne supporte pas, l'exécuter dans un conteneur (un pod ou un virtualenv) l'isole. La question de conception reste la même : quelle est l'unité de relance, et où vont les logs ?

<!-- example -->

```python
glue = GlueJobOperator(task_id="ingest", job_name="orders_ingest", deferrable=True)
spark = DatabricksRunNowOperator(task_id="enrich", job_id=1234, deferrable=True)
dbt = DbtTaskGroup(group_id="marts", project_config=ProjectConfig(DBT_DIR))  # Cosmos
glue >> spark >> dbt
```

#### Comment déclencher un job Databricks depuis Airflow ?

Avec `DatabricksRunNowOperator` (exécute un job existant par son identifiant, avec des paramètres) ou `DatabricksSubmitRunOperator` (soumet une exécution ponctuelle), du provider Databricks, généralement en mode différable pour que l'attente n'occupe pas de worker. `DatabricksWorkflowTaskGroup` peut définir un job Databricks depuis Airflow.

#### Comment exécuter dbt depuis Airflow ?

Avec un `BashOperator` qui appelle `dbt build`, avec un opérateur dbt Cloud (`DbtCloudRunJobOperator`), ou avec Astronomer Cosmos, qui transforme chaque modèle dbt en tâche Airflow avec les dépendances du graphe dbt.

#### Comment lancer un job AWS Glue depuis Airflow ?

Avec `GlueJobOperator` du provider Amazon, en passant le nom du job et les arguments du script, de préférence avec `deferrable=True` ou `wait_for_completion` et un `GlueJobSensor`.

#### Comment exécuter du travail sur Kubernetes depuis Airflow ?

Avec `KubernetesPodOperator` ou `@task.kubernetes`, qui démarrent un pod avec une image, une commande, des ressources et des secrets donnés pour chaque tâche. Chaque tâche a ses propres dépendances et ressources.

#### À quoi sert `PythonVirtualenvOperator` ?

À exécuter une fonction dont les dépendances entrent en conflit avec celles d'Airflow, dans un virtualenv neuf à chaque exécution (plus lent) ou mis en cache. La fonction doit être autonome car elle s'exécute dans un autre interpréteur.

#### Comment orchestrer un pipeline combinant AWS Glue, Databricks et un projet dbt ?

Un DAG (ou des DAG reliés par des assets) utilisant `GlueJobOperator` du provider Amazon, `DatabricksRunNowOperator` du provider Databricks et Cosmos ou l'opérateur dbt Cloud, tous en mode différable, en passant des noms de tables ou des chemins, avec des contrôles de qualité entre les étapes et une configuration d'alerte unique.

<!-- challenge -->

Un projet dbt tourne dans un seul `BashOperator` qui appelle `dbt build`. Un modèle en échec oblige à relancer deux heures de travail. Que suggérez-vous ?

<!-- solution -->

Exécuter dbt avec Cosmos, qui transforme les modèles en tâches, ou découper `dbt build` par sélecteurs en plusieurs tâches. Un échec ne relance alors que les modèles concernés et leurs descendants, et chaque modèle a ses logs dans sa tâche.

<!-- takeaways -->

- Les opérateurs de moteurs soumettent, attendent et rendent compte ; Airflow ne calcule pas.
- Utilisez le mode deferrable pour les longs jobs externes.
- Choisissez la granularité pour que les relances restent petites.

<!-- unit: Écrire ses propres opérateurs -->

<!-- goals -->

- Écrire un opérateur personnalisé avec des champs templatés.
- Utiliser tâches auxiliaires et callbacks sans effets de bord.

<!-- concept -->

Quand un même patron revient dans de nombreux DAG, un opérateur personnalisé l'encapsule : paramètres dans le constructeur, travail dans `execute` et une liste de champs qu'Airflow rend avec Jinja. Tout ce qui touche des systèmes externes va dans `execute`, pas dans le constructeur, car les constructeurs s'exécutent au parsing.

De petits outils complètent le tableau : les tâches vides rendent les graphes lisibles et les callbacks ajoutent logs ou notifications autour de l'exécution, à condition d'être rapides et de ne jamais décider du résultat de la tâche.

<!-- example -->

```python
class PartitionCheckOperator(BaseOperator):
    template_fields = ("table", "partition")

    def __init__(self, table: str, partition: str, **kwargs):
        super().__init__(**kwargs)
        self.table, self.partition = table, partition

    def execute(self, context):
        rows = WarehouseHook().count(self.table, self.partition)
        if rows == 0:
            raise AirflowException(f"{self.table}/{self.partition} is empty")
```

#### Comment écrire un opérateur personnalisé ?

En héritant de `BaseOperator`, en déclarant les paramètres dans `__init__`, en listant les champs templatables dans `template_fields` et en implémentant `execute(self, context)`, avec des hooks pour les connexions externes. Gardez `__init__` léger car il s'exécute à l'analyse du DAG.

```python
from airflow.sdk import BaseOperator

class RowCountCheckOperator(BaseOperator):
    template_fields = ("table",)

    def __init__(self, *, table: str, conn_id: str, min_rows: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.table, self.conn_id, self.min_rows = table, conn_id, min_rows

    def execute(self, context):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        count = PostgresHook(self.conn_id).get_first(f"SELECT count(*) FROM {self.table}")[0]
        if count < self.min_rows:
            raise ValueError(f"{self.table} contient {count} lignes")
        return count
```

#### À quoi sert `EmptyOperator` ?

Une tâche qui ne fait rien, utilisée comme marqueur de début ou de fin ou comme point de jonction dans le graphe pour clarifier les dépendances.

#### Qu'est-ce que `on_execute_callback` ?

Un callback appelé juste avant l'exécution d'une tâche, utilisé pour la journalisation ou des notifications. Comme les autres callbacks, il doit être rapide et ne doit pas faire échouer la tâche.

<!-- challenge -->

Un opérateur personnalisé ouvre une connexion à la base dans `__init__`. Le scheduler ralentit et la base affiche des centaines de connexions inactives. Pourquoi ?

<!-- solution -->

`__init__` s'exécute à chaque parsing du fichier de DAG : chaque parsing ouvre une connexion. Déplacez la connexion dans `execute`, via un hook, pour qu'elle ne s'ouvre qu'à l'exécution réelle de la tâche.

<!-- takeaways -->

- Les appels externes vont dans `execute`, jamais dans `__init__`.
- Listez les paramètres templatés dans `template_fields`.
- Gardez les callbacks rapides et sans logique métier.

### XCom et passage de données

<!-- unit: Passer des valeurs avec XCom -->

<!-- goals -->

- Passer de petites valeurs entre tâches avec XCom et TaskFlow.
- Lire des XCom dans des templates et découper des sorties de type dictionnaire.

<!-- concept -->

Les tâches ont souvent besoin d'une petite information d'une tâche précédente : un chemin, un compte, un identifiant de job. XCom stocke cette valeur avec la task instance pour que les tâches suivantes la lisent. TaskFlow masque la mécanique : appeler une fonction de tâche renvoie un substitut de sa valeur future, et le transmettre relie donnée et dépendance.

Les opérateurs classiques lisent les mêmes valeurs via des templates : les deux styles partagent un mécanisme.

<!-- example -->

```python
@task(multiple_outputs=True)
def extract() -> dict:
    return {"path": "s3://lake/orders/2026-10-17.parquet", "rows": 18233}

out = extract()
load(out["path"])                                   # TaskFlow
SQLExecuteQueryOperator(task_id="log", conn_id="wh",
    sql="INSERT INTO audit VALUES ({{ ti.xcom_pull(task_ids='extract', key='rows') }})")
```

#### Qu'est-ce que XCom ?

« Cross-communication » : un mécanisme pour passer de petites valeurs entre tâches. Une tâche publie une valeur (les valeurs renvoyées en TaskFlow sont publiées automatiquement) et les tâches en aval la lisent. Par défaut, les valeurs sont stockées dans la base de métadonnées.

#### Qu'est-ce que `XComArg` ?

L'objet obtenu en appelant une fonction TaskFlow ou en accédant à `.output` d'un opérateur. Il représente une valeur future et porte la dépendance : le passer à une autre tâche relie les deux.

#### Comment lire un XCom dans un template ?

```jinja2
{{ ti.xcom_pull(task_ids='extract', key='return_value') }}
```

Avec TaskFlow, il suffit de passer la sortie d'une fonction de tâche en argument d'une autre.

#### Que fait `multiple_outputs=True` ?

Sur un `@task` qui renvoie un dictionnaire, il publie chaque clé comme un XCom séparé, pour que les tâches en aval puissent utiliser `result["cle"]` individuellement.

<!-- challenge -->

Une tâche renvoie une liste de 2 millions d'identifiants que la suivante lit. L'UI est lente et la base grossit vite. Que changez-vous ?

<!-- solution -->

Écrire les identifiants dans un stockage objet ou une table de staging et ne renvoyer par XCom que le chemin ou le nom de la table. La tâche suivante lit les données à cet endroit.

<!-- takeaways -->

- XCom transporte de petites valeurs entre tâches.
- TaskFlow transmet XCom et dépendances en un appel.
- Les templates lisent les mêmes valeurs pour les opérateurs classiques.

<!-- unit: Limites de XCom et backends -->

<!-- goals -->

- Garder les gros volumes hors de la base de métadonnées.
- Éviter les problèmes de sérialisation et de rétention.

<!-- concept -->

Le backend XCom par défaut est la base de métadonnées, faite pour l'état, pas pour les données. De grosses valeurs ralentissent scheduler et UI et finissent par heurter des limites de taille. Un backend personnalisé déplace les valeurs vers un stockage objet en ne gardant qu'une référence, ce qui aide, mais la meilleure habitude est de passer soi-même des références.

Les valeurs doivent aussi survivre à la sérialisation, et elles restent jusqu'à ce qu'on les nettoie : la rétention fait partie de l'hygiène de la base.

<!-- example -->

```ini
# airflow.cfg: store XCom values above 1 MB in S3, keep a reference in the database
[common.io]
xcom_objectstorage_path = s3://airflow-xcom/
xcom_objectstorage_threshold = 1048576
```

#### Pourquoi ne pas faire passer de gros volumes par XCom ?

Le backend par défaut stocke les valeurs dans la base de métadonnées, qui n'est pas faite pour de gros contenus, et les valeurs sérialisées ont des limites de taille. Passez des références (un chemin S3, un nom de table, une partition) et laissez les données dans le stockage.

#### Qu'est-ce qu'un backend XCom personnalisé ?

Un backend interchangeable qui stocke les valeurs XCom ailleurs (S3, GCS, Azure Blob) et ne garde qu'une référence en base. Le provider Common IO fournit un backend de stockage objet avec un seuil de taille.

#### Comment éviter les erreurs de sérialisation avec XCom ?

En renvoyant des valeurs sérialisables en JSON (ou des types qu'Airflow sait sérialiser, comme les dataclasses et les DataFrames pandas avec le bon sérialiseur) ; évitez les connexions ouvertes, les générateurs et les gros objets. Renvoyez plutôt des chemins ou des identifiants.

#### Les XCom sont-ils supprimés après une exécution ?

Ils restent en base (et sont effacés quand une tâche est effacée et relancée) jusqu'à leur purge avec `airflow db clean` ou une politique de rétention. Raison de plus pour les garder petits.

<!-- challenge -->

Une tâche renvoie un curseur de base de données et échoue avec une erreur de sérialisation. Que devrait-elle renvoyer ?

<!-- solution -->

Récupérer les résultats dans la tâche et renvoyer des données sérialisables en JSON, comme une liste de dicts si elle est petite. Si elle est grosse, l'écrire dans un stockage et renvoyer le chemin. Les ressources ouvertes comme les curseurs ne traversent pas les tâches.

<!-- takeaways -->

- La base de métadonnées n'est pas un entrepôt de données.
- Passez des références (chemins, noms de table) pour les gros volumes.
- Renvoyez des valeurs sérialisables et nettoyez les vieux XCom.

<!-- unit: Contexte, templates et mapping -->

<!-- goals -->

- Utiliser le contexte de tâche et les templates Jinja pour les valeurs de l'exécution.
- Créer des tâches à l'exécution avec le dynamic task mapping.

<!-- concept -->

Chaque task instance sait où elle en est : son exécution, son intervalle, son numéro de tentative. Ce savoir arrive dans votre code par le contexte en Python et par les templates Jinja dans les champs des opérateurs, rendus juste avant l'exécution.

Le dynamic task mapping applique la même idée à la forme du graphe. Au lieu de fixer le nombre de tâches au parsing, une tâche mappée se déploie sur une liste produite à l'exécution, comme les fichiers arrivés aujourd'hui, et chaque élément devient sa propre instance relançable.

<!-- example -->

```python
@task
def list_files(ds=None) -> list[str]:
    return S3Hook().list_keys("landing", prefix=f"orders/{ds}/")

@task(max_active_tis_per_dagrun=5)
def load(key: str): ...

load.expand(key=list_files())
```

#### Qu'est-ce que le contexte de la tâche ?

Un dictionnaire d'informations d'exécution disponibles pour les tâches : `ti` (task instance), `dag_run`, `logical_date`, `data_interval_start`, `data_interval_end`, `params`, `run_id`, etc. En TaskFlow, on l'obtient avec `get_current_context()` ou en déclarant `**context`.

#### Qu'est-ce que le templating Jinja dans Airflow ?

De nombreux champs d'opérateurs (listés dans `template_fields`) sont rendus avec Jinja juste avant l'exécution, avec des variables de contexte comme `{{ ds }}`, `{{ data_interval_start }}`, `{{ params.x }}`, des macros comme `{{ macros.ds_add(ds, -1) }}` et des Variables (`{{ var.value.nom }}`). Les valeurs rendues sont visibles dans l'interface.

#### Qu'est-ce que `ds` ?

Une variable de template contenant la date logique au format `YYYY-MM-DD`. `ds_nodash` donne `YYYYMMDD`. Elles sont pratiques pour les noms de partitions et les chemins de fichiers.

#### Qu'est-ce que le mapping dynamique de tâches ?

La création, à l'exécution, d'un nombre variable de task instances à partir de la sortie d'une tâche amont, avec `.expand()`. Par exemple, une tâche par fichier trouvé dans un bucket. `.partial()` fixe les arguments communs à toutes les instances.

```python
@task
def list_files() -> list[str]:
    return ["a.csv", "b.csv", "c.csv"]

@task
def process(path: str) -> int:
    return len(path)

process.expand(path=list_files())
```

#### Comment limiter le parallélisme des tâches mappées ?

Avec `max_active_tis_per_dag` ou `max_active_tis_per_dagrun` sur la tâche mappée, ou en l'affectant à un pool aux slots limités.

<!-- challenge -->

Une tâche mappée sur 300 fichiers surcharge la base cible. Comment garder le mapping tout en protégeant la base ?

<!-- solution -->

Limiter la concurrence avec `max_active_tis_per_dagrun`, ou affecter la tâche mappée à un pool de quelques slots. Chaque fichier garde sa propre task instance et ses relances.

<!-- takeaways -->

- Le contexte et les templates donnent aux tâches les dates et identifiants de leur exécution.
- Le mapping dimensionne le graphe à l'exécution avec `.expand()`.
- Limitez la concurrence mappée avec des limites de tâche ou des pools.

### Assets et planification par événements

<!-- unit: Planification pilotée par les données -->

<!-- goals -->

- Planifier des DAG sur des mises à jour d'assets plutôt que sur des horaires.
- Combiner assets et timetables dans un même calendrier.

<!-- concept -->

Les calendriers horaires devinent quand les données seront prêtes. Les assets suppriment la devinette : une tâche productrice déclare qu'elle met à jour une donnée, et les DAG consommateurs s'exécutent quand cela arrive. Les dépendances décrivent des données, pas des horloges, et l'UI montre qui alimente qui.

Les conditions peuvent combiner plusieurs assets avec une logique and/or, ou mêler assets et timetable quand les consommateurs veulent fraîcheur et exécution quotidienne garantie.

<!-- example -->

```python
orders = Asset("s3://lake/silver/orders/")

@task(outlets=[orders])
def build_orders(): ...

@dag(schedule=[orders])                 # runs after each successful build
def orders_report(): ...
```

#### Qu'est-ce qu'un asset (anciennement dataset) ?

Une référence logique à un ensemble de données, identifiée par une URI (par exemple `s3://bucket/sales/`), déclarée comme sortie (outlet) d'une tâche productrice. Quand la tâche réussit, Airflow enregistre un événement d'asset et les DAG planifiés sur cet asset sont déclenchés.

```python
from airflow.sdk import Asset, dag, task

sales = Asset("s3://lake/silver/sales/")

@dag(schedule="@daily", start_date=datetime(2026, 1, 1))
def produce():
    @task(outlets=[sales])
    def build_sales(): ...
    build_sales()

@dag(schedule=[sales], start_date=datetime(2026, 1, 1))
def consume():
    @task
    def report(): ...
    report()
```

#### Pourquoi utiliser des assets plutôt qu'`ExternalTaskSensor` ?

Les assets expriment directement les dépendances de données (« exécuter quand sales est mis à jour ») sans aligner les plannings ni occuper de slots avec des sensors, et l'interface montre le lignage entre DAG producteurs et consommateurs.

#### Un DAG peut-il dépendre de plusieurs assets ?

Oui. Une liste signifie que tous doivent avoir été mis à jour depuis la dernière exécution ; on peut aussi combiner les assets avec des expressions `&` (et) et `|` (ou). `AssetOrTimeSchedule` combine un planning horaire et des déclenchements par assets.

#### Un DAG peut-il être déclenché à la fois par un planning et par des assets ?

Oui, avec `AssetOrTimeSchedule`, qui s'exécute selon un timetable et aussi chaque fois que la condition sur les assets est remplie.

#### Qu'est-ce que le décorateur `@asset` ?

Un raccourci d'Airflow 3 qui définit un asset avec le DAG à une seule tâche qui le matérialise, pour une écriture centrée sur les assets, à la manière de Dagster.

<!-- challenge -->

Un DAG de rapport tourne à 07:00 avec un `ExternalTaskSensor` sur le DAG de chargement de 06:00. Les chargements glissent parfois à 06:30. Comment les découpler ?

<!-- solution -->

Déclarer la table de la tâche de chargement comme outlet d'un asset et planifier le rapport sur cet asset. Le rapport tourne dès que le chargement réussit, sans alignement de calendriers ni sensor qui occupe un slot.

<!-- takeaways -->

- Les assets planifient les consommateurs sur les mises à jour de données.
- Les conditions combinent les assets en and/or, ou avec un timetable.
- La vue des assets rend visible le lignage entre DAG.

<!-- unit: Événements d'assets et déclencheurs externes -->

<!-- goals -->

- Comprendre ce qu'un événement d'asset garantit et ne garantit pas.
- Déclencher des DAG depuis des événements externes sans polling.

<!-- concept -->

Un événement d'asset signifie qu'une tâche productrice a réussi, rien de plus. Airflow ne regarde jamais les données : une tâche capable de réussir sans rien écrire doit éviter d'émettre l'événement, et les événements peuvent porter des métadonnées comme la partition écrite pour que les consommateurs sachent ce qui a changé.

Les événements peuvent aussi venir de l'extérieur. Les asset watchers attachent un trigger à une file de messages : un fichier déposé dans le stockage peut lancer un DAG en quelques secondes, sans aucun sensor.

<!-- example -->

```python
queue = MessageQueueTrigger(queue="https://sqs.eu-west-1.amazonaws.com/123/landing-events")
landing = Asset("s3://landing/orders/", watchers=[AssetWatcher(name="sqs", trigger=queue)])

@dag(schedule=[landing])
def ingest_orders(): ...
```

#### Les assets savent-ils si les données ont réellement changé ?

Non. Airflow sait seulement qu'une tâche productrice a réussi ; il n'inspecte pas les données. Si une tâche peut réussir sans rien écrire, elle ne doit pas émettre l'événement, ou le consommateur doit vérifier.

#### Peut-on attacher des métadonnées à un événement d'asset ?

Oui. Une tâche productrice peut ajouter des informations (par exemple le nombre de lignes ou la partition écrite) à l'événement via les outlet events, et les consommateurs peuvent les lire dans les événements déclencheurs de leur contexte.

#### Comment voir le lignage des assets dans l'interface ?

La vue des assets montre chaque asset avec ses DAG producteurs et consommateurs et l'historique des événements, ce qui rend visibles les dépendances entre DAG.

#### Qu'est-ce qu'un asset alias ?

Un substitut utilisé quand l'URI exacte de l'asset n'est connue qu'à l'exécution : la tâche émet des événements pour un alias en y attachant l'asset concret, et les consommateurs peuvent se planifier sur l'alias.

#### Que sont les asset watchers ?

Une fonction d'Airflow 3 pour la planification par événements venant de systèmes externes : un `AssetWatcher` associe un trigger (par exemple sur une file de messages comme SQS ou Kafka) à un asset, pour qu'un DAG s'exécute à l'arrivée d'un événement externe, et pas seulement quand une autre tâche Airflow met à jour l'asset.

#### Comment déclencher un DAG Airflow à l'arrivée d'un fichier dans S3, sans scrutation ?

Avec un asset watcher sur une file SQS qui reçoit les notifications d'événements S3 (Airflow 3), ou avec un événement S3 qui lance une fonction Lambda appelant l'API REST d'Airflow pour déclencher le DAG avec le chemin du fichier en configuration.

<!-- challenge -->

Une tâche productrice réussit même quand sa source est vide, et les DAG aval se relancent pour rien. Comment l'éviter ?

<!-- solution -->

Vérifier le nombre de lignes dans la tâche et la sauter (lever une exception de skip) quand il n'y a rien de nouveau, pour qu'aucun événement ne soit émis. Éventuellement joindre le nombre de lignes aux événements pour les consommateurs.

<!-- takeaways -->

- Un événement d'asset signifie seulement que le producteur a réussi.
- Les métadonnées d'événement disent aux consommateurs ce qui a changé.
- Les watchers déclenchent des DAG depuis des files sans polling.

<!-- stage: Exploiter Airflow -->

### Executors et architecture

<!-- unit: Choisir un executor -->

<!-- goals -->

- Comparer les executors Local, Celery, Kubernetes et Edge.
- Adapter l'executor à la forme de la charge et aux compétences de l'équipe.

<!-- concept -->

L'executor décide où s'exécute physiquement le code des tâches. Le choix arbitre entre rapidité de démarrage et isolation. Des workers de longue durée démarrent vite les tâches mais partagent un environnement et doivent être dimensionnés pour le pic. Un pod par tâche démarre plus lentement mais donne à chaque tâche son image et ses ressources, et ne coûte rien au repos.

Comme les executors se combinent, le choix n'est plus tout ou rien : la plupart des tâches sur des workers rapides, les cas particuliers dans des pods ou sur des workers edge distants.

<!-- example -->

```ini
[core]
executor = CeleryExecutor,KubernetesExecutor
```
```python
@task(executor="KubernetesExecutor")      # this task alone runs in its own pod
def train_model(): ...
```

#### Qu'est-ce qu'un executor ?

Le composant qui décide comment et où les task instances s'exécutent. Le scheduler envoie les tâches en file à l'executor, qui les exécute localement ou les répartit sur des workers.

#### Quels executors sont disponibles ?

`LocalExecutor` (processus parallèles sur la machine du scheduler), `CeleryExecutor` (un ensemble de workers alimentés par un broker de messages comme Redis ou RabbitMQ), `KubernetesExecutor` (un pod par tâche) et des executors de providers comme ceux d'AWS ECS et Batch et l'Edge executor pour des workers distants. Depuis Airflow 2.10, on peut utiliser plusieurs executors à la fois.

#### Quand choisir le CeleryExecutor ?

Pour de nombreuses tâches courtes avec une charge régulière : des workers persistants démarrent les tâches rapidement. Il faut exploiter un broker et dimensionner les workers soi-même (ou avec KEDA).

#### Quand choisir le KubernetesExecutor ?

Quand les tâches ont besoin de ressources ou d'images différentes, que l'isolation compte et que la charge est irrégulière : chaque tâche tourne dans son propre pod et les ressources sont libérées ensuite. Le démarrage du pod ajoute quelques secondes de latence par tâche.

#### Quel est le rôle du broker de messages avec Celery ?

Redis ou RabbitMQ contient la file des tâches envoyées par le scheduler ; les workers Celery la consomment. Un backend de résultats (généralement la base de données) stocke l'état des tâches.

#### Qu'est-ce que le `pod_template_file` ?

Une spécification de pod Kubernetes utilisée par le KubernetesExecutor (et le KubernetesPodOperator) comme base des pods de tâches : image, ressources, volumes, sélecteurs de nœuds, service account. Les tâches peuvent en surcharger une partie avec `executor_config`.

#### Peut-on utiliser plusieurs executors à la fois ?

Oui, depuis Airflow 2.10 : on configure une liste d'executors et on affecte chaque tâche à l'un d'eux avec l'argument `executor`, par exemple la plupart des tâches sur Celery et les tâches lourdes et isolées sur Kubernetes.

#### Qu'est-ce que l'Edge executor ?

Un executor (du provider Edge3) qui exécute les tâches sur des workers distants connectés à l'API d'Airflow en HTTP, par exemple dans un autre réseau ou centre de données, sans accès direct à la base.

<!-- challenge -->

Votre plateforme exécute 5 000 courtes tâches SQL par jour et quelques entraînements GPU par semaine. Quelle configuration d'executors proposez-vous ?

<!-- solution -->

CeleryExecutor pour les courtes tâches SQL, qui démarrent vite sur des workers chauds, plus KubernetesExecutor affecté par tâche aux entraînements, pour n'utiliser les nœuds GPU qu'en cas de besoin.

<!-- takeaways -->

- Les workers démarrent vite ; les pods isolent et descendent à zéro.
- Celery exige un broker ; Kubernetes, des modèles de pod.
- Plusieurs executors laissent chaque tâche tourner où elle convient.

<!-- unit: Scheduler et DAG processor -->

<!-- goals -->

- Décrire ce que font scheduler et DAG processor à chaque cycle.
- Rendre la couche d'ordonnancement hautement disponible et sûre.

<!-- concept -->

L'ordonnancement est une boucle sur la base : trouver les exécutions dues, les task instances dont les dépendances sont satisfaites, et les confier à l'executor dans les limites. Parser le code est un autre travail, celui du DAG processor, pour qu'un fichier lent ou cassé ne bloque pas l'ordonnancement.

L'état vivant dans la base, la haute disponibilité est simple : plusieurs schedulers qui se coordonnent par verrous de ligne. Avec Airflow 3, les workers cessent aussi de lire la base et demandent ce dont ils ont besoin à l'API server, ce qui réduit ce qu'une tâche peut voir.

<!-- example -->

```text
DAG files ─► DAG processor ─► serialized DAGs ─┐
                                               ▼
 scheduler ×2 ─ row locks ─► metadata DB ◄─ API server ◄─ workers (Task Execution API)
```

#### Que fait le scheduler ?

Il lit les DAG sérialisés, crée les DAG runs à échéance, vérifie quelles task instances ont leurs dépendances satisfaites, respecte les limites de concurrence et les pools, et envoie les tâches à l'executor. Plusieurs schedulers peuvent tourner en même temps pour la haute disponibilité.

#### Que fait le DAG processor ?

Il analyse les fichiers de DAG et stocke les DAG sérialisés en base. Dans Airflow 3, c'est un composant séparé : le code des utilisateurs ne s'exécute jamais dans le scheduler.

#### Comment rendre le scheduler hautement disponible ?

En exécutant deux schedulers ou plus sur la même base PostgreSQL ou MySQL ; ils se coordonnent par verrous au niveau ligne. On exécute plusieurs API servers derrière un répartiteur de charge et plusieurs triggerers.

#### Comment les workers obtiennent-ils leurs identifiants dans Airflow 3 ?

Via la Task Execution API : les tâches demandent connexions, variables et XCom à l'API server au lieu de lire la base de métadonnées, ce qui améliore la sécurité et permet des workers distants.

<!-- challenge -->

La VM du scheduler unique est tombée la nuit et rien n'a tourné jusqu'au matin. Que proposez-vous pour que cela ne se reproduise pas ?

<!-- solution -->

Faire tourner au moins deux schedulers (sur des nœuds différents) sur un PostgreSQL managé sauvegardé, et alerter sur la métrique de heartbeat du scheduler. Exécuter le DAG processor à part pour que les problèmes de parsing n'arrêtent pas les schedulers.

<!-- takeaways -->

- Le scheduler boucle sur la base ; le DAG processor parse le code.
- Plusieurs schedulers assurent la haute disponibilité par verrous de ligne.
- Avec Airflow 3, les workers parlent à l'API server, pas à la base.

<!-- unit: Concurrence, pools et priorités -->

<!-- goals -->

- Utiliser réglages de concurrence, pools et priorités pour partager la capacité.
- Protéger les systèmes partagés des surcharges et des écritures concurrentes.

<!-- concept -->

La capacité est limitée à plusieurs niveaux : l'installation, chaque DAG, chaque tâche et chaque pool. Quand les tâches se disputent les slots, les priority weights décident qui passe en premier. Ces réglages n'ajustent pas seulement la vitesse ; ils expriment des règles sur les systèmes touchés par les tâches.

Un pool de quelques slots est la façon la plus simple de dire « pas plus de quatre requêtes sur la production à la fois », et un pool d'un slot sérialise des écrivains qui ne doivent jamais se chevaucher.

<!-- example -->

```python
# pool "orders_table" created with 1 slot: writers take turns
MERGE_A = SQLExecuteQueryOperator(task_id="merge_a", pool="orders_table", ...)
MERGE_B = SQLExecuteQueryOperator(task_id="merge_b", pool="orders_table", ...)
```

#### Quels réglages de concurrence existent ?

`parallelism` (maximum de tâches en cours par scheduler), `max_active_tasks_per_dag`, `max_active_runs_per_dag`, les slots des pools, `max_active_tis_per_dag` par tâche, et les réglages propres à l'executor comme la concurrence des workers Celery.

#### Qu'est-ce qu'un pool ?

Une limite nommée sur les slots de tâches concurrentes, utilisée pour protéger une ressource partagée : par exemple un pool de 4 slots pour les tâches qui interrogent une base de production. Les tâches sont affectées à un pool et peuvent consommer plusieurs slots.

#### Qu'est-ce que le priority weight ?

Un nombre qui détermine quelles tâches en file passent en premier quand les slots manquent. La règle de poids (`downstream`, `upstream`, `absolute`) contrôle la façon dont il se cumule dans le graphe.

#### Que sont les files dans le CeleryExecutor ?

Des files nommées auxquelles les workers s'abonnent. Affecter des tâches à une file (`queue="gpu"`) les envoie vers des workers disposant des ressources adaptées.

#### Deux DAG écrivent dans la même table et entrent parfois en conflit. Comment corriger ?

En les sérialisant : un pool à un seul slot pour les écritures dans cette table, ou leur fusion en un seul DAG à l'ordre explicite, ou une dépendance de l'un sur l'autre via un asset. Mieux encore, donner à chaque table un seul processus propriétaire.

<!-- challenge -->

Un lot nocturne de 200 tâches retarde le DAG critique de la finance du matin. Comment garantir que la finance passe en premier ?

<!-- solution -->

Donner aux tâches de la finance un `priority_weight` plus élevé (avec la règle `absolute`) pour qu'elles gagnent les slots en file, et placer le lot dans un pool limité pour qu'il ne prenne pas tous les workers.

<!-- takeaways -->

- Des limites existent par installation, DAG, tâche et pool.
- Les pools protègent les systèmes partagés et sérialisent les écritures concurrentes.
- Les priority weights décident qui obtient les slots rares.

### Configuration, sécurité et secrets

<!-- unit: Configuration et secrets -->

<!-- goals -->

- Configurer Airflow avec des fichiers et des variables d'environnement.
- Garder les identifiants dans un secrets backend, chiffrés et masqués.

<!-- concept -->

La configuration d'Airflow a des couches : le fichier de configuration, des variables d'environnement qui le surchargent, et des secrets qui ne devraient vivre dans aucun des deux. Connections et variables peuvent venir de la base, de variables d'environnement ou d'un gestionnaire de secrets ; Airflow consulte ces sources dans l'ordre, si bien que la production garde ses secrets dans un coffre et le développement des variables locales.

La défense va plus loin : les valeurs en base sont chiffrées avec la clé Fernet, et logs et UI masquent ce qui ressemble à un secret.

<!-- example -->

```bash
export AIRFLOW__CORE__PARALLELISM=64
export AIRFLOW__SECRETS__BACKEND=airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
export AIRFLOW__SECRETS__BACKEND_KWARGS='{"connections_prefix": "airflow/connections"}'
```

#### Comment configure-t-on Airflow ?

Avec `airflow.cfg`, surchargé par des variables d'environnement nommées `AIRFLOW__SECTION__CLE` (par exemple `AIRFLOW__CORE__PARALLELISM`). Les variables d'environnement sont l'approche habituelle en conteneur.

#### Comment définir des connexions en variables d'environnement ?

Avec `AIRFLOW_CONN_<CONN_ID>` contenant une URI ou un JSON, par exemple `AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'`. Elles n'apparaissent pas dans l'interface et ont priorité sur une connexion de même identifiant en base (un secrets backend configuré est toutefois consulté en premier).

#### Qu'est-ce qu'un secrets backend ?

Une intégration qui lit les connexions et variables dans un gestionnaire de secrets externe : AWS Secrets Manager ou SSM Parameter Store, HashiCorp Vault, Google Secret Manager, Azure Key Vault. Les secrets n'ont plus à être stockés dans la base de métadonnées.

#### Qu'est-ce que la clé Fernet ?

La clé utilisée pour chiffrer les mots de passe des connexions et les valeurs des variables dans la base de métadonnées. Elle doit être définie, gardée secrète et identique sur tous les composants ; la changer impose un rechiffrement.

#### Comment Airflow évite-t-il d'afficher des secrets dans les journaux et l'interface ?

Il masque les mots de passe des connexions, les variables dont le nom contient des mots comme `password`, `secret` ou `token`, et les valeurs enregistrées avec `mask_secret()`. Le masquage n'est pas infaillible : n'affichez pas de secrets.

<!-- challenge -->

Le mot de passe d'une connection apparaît en clair dans le log d'une tâche, car la tâche a affiché une URL qui le contenait. Comment l'éviter ?

<!-- solution -->

Ne plus afficher l'URL, enregistrer la valeur auprès du masqueur de secrets si elle est construite à l'exécution et changer le mot de passe divulgué. Préférer les secrets backends pour que les valeurs ne soient pas copiées dans des variables aux noms que le masqueur ne reconnaît pas.

<!-- takeaways -->

- Les variables d'environnement surchargent `airflow.cfg`.
- Les secrets backends gardent les identifiants dans un coffre.
- Chiffrement et masquage protègent, mais le code peut encore divulguer.

<!-- unit: Accès et identité -->

<!-- goals -->

- Contrôler qui peut voir et déclencher quels DAG.
- Donner aux tâches un accès cloud sans clés de longue durée.

<!-- concept -->

Deux identités comptent dans Airflow : les personnes qui utilisent l'UI et le code qui tourne sur les workers. Les personnes reçoivent des rôles qui limitent les DAG qu'elles voient ou déclenchent. Le code tourne avec les permissions des workers, le problème le plus délicat, car quiconque peut déployer un DAG peut lui faire lire n'importe quelle connection.

Contrôlez donc l'accès au déploiement (revues, déploiements séparés par équipe) et donnez aux workers des identités cloud de courte durée plutôt que des clés stockées.

<!-- example -->

```python
@dag(access_control={"finance-ops": {"DAGs": {"can_read", "can_edit"}}},
     schedule="@daily", start_date=datetime(2026, 1, 1))
def finance_close(): ...
```

#### Comment contrôle-t-on l'accès à l'interface ?

Avec un auth manager. Airflow 3 fournit un auth manager simple pour le développement ; l'auth manager FAB offre un contrôle d'accès par rôles (Admin, Op, User, Viewer et rôles personnalisés), et les services managés s'intègrent à l'IAM du cloud.

#### Comment restreindre qui peut déclencher un DAG ?

Avec le contrôle d'accès par rôles : on donne aux rôles des droits sur des DAG précis (par identifiant ou via `access_control` dans le DAG), pour qu'une équipe ne puisse déclencher et effacer que ses propres DAG.

#### Comment le code des DAG doit-il accéder aux ressources cloud ?

Avec l'identité du worker (IAM roles for service accounts sur Kubernetes, rôle d'exécution MWAA, workload identity) chaque fois que possible, plutôt qu'avec des clés de longue durée stockées dans des connexions.

#### Pourquoi est-il risqué de laisser beaucoup de personnes modifier le code des DAG ?

Le code des DAG s'exécute avec les droits des workers et peut lire les connexions : quiconque peut déployer des DAG a de fait accès à toutes les connexions. La revue de code et les contrôles de CI sur le dépôt de DAG font partie de la sécurité.

<!-- challenge -->

Dix équipes partagent un déploiement Airflow, et les DAG de l'une ont besoin des données de paie. Que proposez-vous ?

<!-- solution -->

Donner à la paie son propre déploiement (ou au moins ses propres workers avec un autre rôle cloud et un autre chemin de secrets), restreindre ses DAG par RBAC et exiger une revue de code sur ce dépôt. Des workers partagés exposeraient les identifiants de paie au code de toutes les équipes.

<!-- takeaways -->

- Le RBAC contrôle les personnes ; l'identité des workers contrôle le code.
- Déployer du code de DAG, c'est accéder à ses connections.
- Préférez les identités de workload aux clés cloud stockées.

<!-- stage: Production -->

### Tests et qualité du code

<!-- unit: Tester les DAG et la logique des tâches -->

<!-- goals -->

- Écrire des tests d'intégrité et de structure des DAG.
- Tester unitairement logique et opérateurs sans Airflow complet.

<!-- concept -->

Un DAG peut échouer à trois endroits : à l'import, dans sa structure ou dans la logique de ses tâches. Chacun appelle un test différent. Les tests d'import et de structure chargent les DAG et vérifient qu'ils se parsent et ont la forme attendue. Les tests de logique traitent le code des tâches comme n'importe quel module Python, ce qui n'est simple que si la logique vit hors du fichier de DAG.

Les opérateurs qui appellent des systèmes externes se testent deux fois : avec des hooks simulés pour leur logique et contre des conteneurs locaux pour le comportement réel.

<!-- example -->

```python
def test_dags_import():
    bag = DagBag(include_examples=False)
    assert bag.import_errors == {}

def test_sales_structure():
    dag = DagBag().get_dag("sales_load")
    assert dag.get_task("extract").downstream_task_ids == {"transform"}
```

#### Comment tester que les DAG se chargent correctement ?

Avec un test d'intégrité qui charge tous les fichiers de DAG via `DagBag` et vérifie l'absence d'erreurs d'import, plus des contrôles de conventions (tags, owners, relances, pas de cycle).

```python
from airflow.models import DagBag

def test_no_import_errors():
    bag = DagBag(dag_folder="dags/", include_examples=False)
    assert not bag.import_errors, bag.import_errors

def test_every_dag_has_retries():
    bag = DagBag(dag_folder="dags/", include_examples=False)
    for dag_id, dag in bag.dags.items():
        assert dag.default_args.get("retries", 0) >= 1, dag_id
```

#### Comment tester qu'un DAG a la bonne structure ?

En le chargeant depuis un `DagBag` et en vérifiant les identifiants de tâches, les dépendances (`task.downstream_task_ids`), les plannings et les réglages, pour détecter les modifications accidentelles du graphe.

#### Comment tester unitairement la logique des tâches ?

En gardant la logique métier dans des fonctions ou modules Python ordinaires, hors du fichier de DAG, en les testant avec pytest sans Airflow, et en faisant des tâches de simples enveloppes. Pour les opérateurs, on teste `execute()` avec des hooks simulés (mocks).

#### Comment vérifier le rendu des champs templatés ?

En les rendant pour un contexte donné dans un test (`ti.render_templates()`), ou avec `airflow tasks render dag_id task_id date`, puis en contrôlant le SQL ou la commande obtenus.

#### Comment tester des opérateurs personnalisés qui utilisent des systèmes externes ?

En simulant le hook dans les tests unitaires pour vérifier la logique et les paramètres de l'opérateur, et en lançant des tests d'intégration contre des conteneurs locaux (Postgres, LocalStack pour AWS, MinIO pour S3) en CI.

<!-- challenge -->

Toute la logique de transformation d'un DAG est écrite dans cinq fonctions `@task` et personne ne la teste. Comment la rendre testable ?

<!-- solution -->

Déplacer la logique dans un module de fonctions pures qui reçoivent et renvoient des données, les tester avec pytest, et garder les tâches comme fines enveloppes qui lisent les entrées, appellent les fonctions et écrivent les sorties.

<!-- takeaways -->

- Testez séparément import, structure et logique.
- La logique hors des fichiers de DAG se teste facilement.
- Simulez les hooks en test unitaire ; utilisez des conteneurs en intégration.

<!-- unit: Exécutions locales et CI -->

<!-- goals -->

- Exécuter DAG et tâches isolées en local pour déboguer.
- Construire un pipeline de CI pour un dépôt Airflow.

<!-- concept -->

Un retour rapide vient de l'exécution locale de petits morceaux : un DAG entier dans un processus avec débogueur, ou une tâche pour une date. Les environnements locaux doivent ressembler aux images de production, sinon les problèmes « ça marche chez moi » reviennent au déploiement.

La CI automatise les mêmes contrôles à chaque changement, du linting aux tests d'intégrité, et un environnement de staging exécute de vraies données sur une courte plage de dates avant la production.

<!-- example -->

```yaml
# CI steps for an Airflow repository
- run: ruff check dags/ --select AIR
- run: pytest tests/unit tests/dags
- run: docker build -t airflow:${{ github.sha }} .
```

#### Que fait `dag.test()` ?

Il exécute un DAG run complet dans un seul processus Python, sans scheduler, ce qui est utile pour déboguer en local dans un IDE avec des points d'arrêt.

#### Que fait `airflow tasks test` ?

Il exécute une task instance pour une date donnée sans enregistrer d'état en base ni vérifier les dépendances. Pratique pour contrôler rapidement les templates et la logique.

#### Comment exécuter Airflow en local pour le développement ?

Avec le Docker Compose officiel, `airflow standalone`, la CLI Astro (`astro dev start`) ou Breeze pour contribuer à Airflow. Utilisez la même image et les mêmes providers qu'en production.

#### Quel linting est utile pour le code des DAG ?

Ruff avec les règles Airflow (les règles `AIR` signalent les imports obsolètes et les points de migration vers Airflow 3), la vérification de types, et des contrôles maison sur le code de niveau supérieur, l'absence d'owners ou de tags et les identifiants codés en dur.

#### Comment tester les DAG contre de vrais systèmes ?

Dans un Airflow de staging pointant vers des stockages de staging : déployer depuis une branche, déclencher des exécutions paramétrées sur une petite plage de dates et vérifier les sorties avec des tests de qualité. Évitez de lancer des tests contre les stockages de production.

#### Que doit exécuter un pipeline de CI pour un dépôt Airflow ?

Le linting (Ruff avec les règles `AIR`), les tests unitaires de la logique métier, les tests d'intégrité des DAG (erreurs d'import du `DagBag`, conventions, cycles), des contrôles de durée d'analyse, la construction de l'image et le déploiement en staging, la production étant déployée après le merge ou une approbation.

<!-- challenge -->

Un import cassé est arrivé en production et le DAG a disparu de l'UI. Quel contrôle de CI l'aurait détecté, et combien coûte-t-il ?

<!-- solution -->

Un test d'intégrité qui charge chaque fichier avec `DagBag` et vérifie l'absence d'erreurs d'import. Il tourne en quelques secondes en CI, dans la même image que la production, donc détecte aussi les paquets manquants.

<!-- takeaways -->

- `dag.test()` et `airflow tasks test` donnent un retour local rapide.
- Les règles `AIR` de Ruff repèrent le code obsolète et les problèmes Airflow 3.
- La CI lance lint, tests unitaires et d'intégrité à chaque changement.

### Déploiement et exploitation

<!-- unit: Déployer les DAG -->

<!-- goals -->

- Déployer code de DAG et dépendances de façon reproductible.
- Annuler vite un mauvais déploiement.

<!-- concept -->

Un déploiement a deux parties qui doivent concorder : l'environnement (Airflow, providers, paquets Python) et le code des DAG. Les construire dans une même image rend tous les environnements identiques. Envoyer les DAG à part, par git-sync, bundles ou bucket S3, va plus vite mais invite aux décalages entre code et paquets installés.

Quelle que soit la méthode, les déploiements doivent venir de la CI et pouvoir être annulés en redéployant la version précédente.

<!-- example -->

```dockerfile
FROM apache/airflow:3.1.0-python3.12
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt"
COPY dags/ /opt/airflow/dags/
```

#### Comment déployer les DAG ?

La plupart des équipes construisent une image Docker avec Airflow, les providers, les dépendances et le code des DAG, et la déploient en CI/CD sur Kubernetes (chart Helm) ou sur un service managé. Alternatives : synchroniser les DAG depuis Git avec git-sync ou vers un bucket S3 (MWAA). Les DAG bundles d'Airflow 3 peuvent lire les DAG directement depuis Git avec versionnage.

#### Qu'est-ce qu'un DAG bundle ?

Un concept d'Airflow 3 désignant un ensemble de fichiers de DAG issus d'une source comme un dossier local ou un dépôt Git, qui permet à Airflow de suivre les versions du code et d'exécuter chaque DAG run avec la version avec laquelle il a démarré.

#### Qu'est-ce que le chart Helm officiel ?

Le chart Helm d'Apache Airflow, qui déploie tous les composants sur Kubernetes avec des options pour les executors, git-sync, PgBouncer, l'autoscaling KEDA, la journalisation et les secrets. C'est le déploiement auto-hébergé standard sur Kubernetes.

#### Comment déployer sur Amazon MWAA ?

En téléversant les DAG dans le bucket S3 de l'environnement (généralement depuis la CI avec `aws s3 sync`) et en gérant `requirements.txt`, les plugins et un script de démarrage dans S3 ; la version d'Airflow et la taille de l'environnement se règlent dans sa configuration. Le rôle d'exécution donne l'accès à AWS.

#### Comment revenir en arrière après un mauvais déploiement de DAG ?

En redéployant l'image ou le commit Git précédent via la CI. Avec le versionnage des DAG d'Airflow 3, les exécutions existantes gardent leur version. On efface ensuite les exécutions en échec si nécessaire.

#### Un DAG fonctionne en local mais les tâches échouent en production avec « module not found ». Pourquoi ?

L'image ou les workers de production n'ont pas la dépendance, ou le module n'est pas dans le chemin (par exemple du code hors du dossier des DAG ou des plugins). Ajoutez-le aux dépendances de l'image ou à un paquet, et construisez le local et la production à partir de la même image.

<!-- challenge -->

Un déploiement a cassé trois DAG à 02:00. Écrivez les trois premières étapes de votre retour arrière.

<!-- solution -->

Redéployer l'image ou le commit précédent via la CI. Vérifier que la liste des erreurs d'import est vide et que les DAG sont revenus. Puis nettoyer les task instances en échec pour qu'elles tournent avec l'ancien code, et ouvrir un ticket de correction.

<!-- takeaways -->

- Déployez code et dépendances ensemble quand c'est possible.
- Déployez depuis la CI ; annulez en redéployant la version précédente.
- « Module not found » signifie souvent que l'image et le code ont divergé.

<!-- unit: Mises à jour et dépendances -->

<!-- goals -->

- Mettre à jour Airflow sans risque, y compris de 2 vers 3.
- Figer les dépendances avec les fichiers de constraints.

<!-- concept -->

Airflow repose sur des centaines de paquets Python, et un petit changement dans un provider peut modifier le comportement d'un opérateur. Les fichiers de constraints figent un ensemble éprouvé pour chaque version d'Airflow et de Python : les mises à jour deviennent des événements délibérés, pas des effets de bord d'une reconstruction.

Les versions majeures ajoutent migrations de base et changements d'API. Le chemin sûr est progressif : atteindre la dernière mineure, corriger les avertissements, tester en staging avec une sauvegarde de la base, puis franchir le pas.

<!-- example -->

```bash
pip install "apache-airflow[amazon,databricks]==3.1.0" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt"
ruff check dags/ --select AIR3     # find Airflow 3 incompatibilities
airflow db migrate
```

#### Comment mettre à jour Airflow en sécurité ?

Lire les notes de version, mettre à jour d'abord un environnement de test, utiliser les fichiers de contraintes pour figer des dépendances compatibles, lancer `airflow db migrate`, vérifier les DAG pour les dépréciations (règles `AIR` de Ruff pour Airflow 3) et sauvegarder la base de métadonnées avant de migrer la production.

#### Que sont les fichiers de contraintes ?

Des listes de dépendances figées publiées pour chaque version d'Airflow et de Python, utilisées avec `pip install "apache-airflow==X" --constraint <url>` pour obtenir un ensemble de paquets dont on sait qu'il fonctionne.

#### Pourquoi figer les versions des providers et des dépendances ?

Des mises à jour non figées peuvent changer le comportement des opérateurs ou casser des imports silencieusement. Figez les versions avec le fichier de contraintes et mettez à jour délibérément, avec des tests.

#### Comment migrer d'Airflow 2 à Airflow 3 ?

Passer d'abord à la dernière 2.x et corriger les avertissements de dépréciation, lancer les règles `AIR3` de Ruff pour trouver le code à modifier (imports vers `airflow.sdk`, `schedule_interval` vers `schedule`, `execution_date` vers `logical_date`, SubDAG et SLA supprimés, pas d'accès direct à la base depuis les tâches), tester en staging, migrer la base, et adapter le déploiement pour l'API server et le DAG processor.

<!-- challenge -->

Reconstruire l'image sans changement a mis à jour un provider tout seul, et un opérateur se comporte désormais autrement. Comment l'éviter ?

<!-- solution -->

Figer Airflow et tous les providers dans `requirements.txt` et installer avec le fichier de constraints correspondant, pour des reconstructions reproductibles. Mettre à jour les providers volontairement dans une branche, avec tests et notes de version relues.

<!-- takeaways -->

- Les constraints rendent les installations reproductibles.
- Figez les providers ; mettez-les à jour volontairement.
- Pour une majeure : dernière mineure, avertissements, tests, sauvegarde, migration.

<!-- unit: Surveillance et alertes -->

<!-- goals -->

- Collecter logs et métriques d'Airflow et de ses tâches.
- Concevoir des alertes qui atteignent les bonnes personnes avec le bon contexte.

<!-- concept -->

Deux types de signaux comptent. Ceux de la plateforme (heartbeat du scheduler, files, temps de parsing) disent si Airflow fonctionne. Ceux des pipelines (échecs de tâches, exécutions en retard) disent si les données arrivent. Chacun a son public : l'équipe plateforme et les propriétaires des données.

Une bonne alerte porte du contexte et pointe vers un runbook. Des alertes qui sonnent chaque nuit pour des tâches instables connues apprennent à les ignorer : corriger les causes profondes fait partie de l'alerting.

<!-- example -->

```python
def notify_failure(context):
    ti = context["ti"]
    send_slack(f":red_circle: {ti.dag_id}.{ti.task_id} failed ({context['ds']}) "
               f"owner={ti.task.owner} log={ti.log_url}")

default_args = {"on_failure_callback": notify_failure}
```

#### Où vont les journaux des tâches ?

Par défaut dans des fichiers locaux sur les workers, affichés dans l'interface. En production, configurez la journalisation distante vers S3, GCS, Azure Blob, Elasticsearch ou CloudWatch pour que les journaux survivent aux redémarrages de pods.

#### Comment superviser Airflow ?

Avec les métriques StatsD ou OpenTelemetry (heartbeat du scheduler, durée d'analyse des DAG, tâches en file et en cours, durées des tâches, usage des pools) dans Prometheus/Grafana ou Datadog, des endpoints de santé, et des alertes sur les échecs et les exécutions trop longues.

#### Comment être alerté des échecs de tâches ?

Avec des callbacks (`on_failure_callback`, `on_retry_callback`, `on_success_callback`) qui envoient vers Slack, l'e-mail ou PagerDuty, les classes notifier des providers ou la configuration e-mail. Alertez au niveau du DAG pour des messages actionnables et sans doublons.

#### Qu'est-ce qui a remplacé les SLA dans Airflow 3 ?

Les SLA (`sla` et `sla_miss_callback`) ont été supprimés car peu fiables. Airflow 3.1 a introduit les deadline alerts, qui déclenchent un callback quand un DAG run n'est pas terminé avant une échéance relative à une heure de référence. Avant cela, les équipes utilisaient `execution_timeout`, `dagrun_timeout` et une supervision externe.

#### Que doit contenir un runbook pour un DAG en échec ?

Ce que fait le DAG et qui en est responsable, les dépendances amont, comment consulter les journaux et les entrées, quelles tâches peuvent être effacées et relancées sans risque, comment faire un backfill, qui prévenir, et les pannes connues avec leurs corrections.

#### Votre personne d'astreinte est réveillée chaque nuit par la même tâche instable. Que changez-vous ?

Je cherche la cause racine dans les journaux (timeouts, limites de ressources, retard en amont), j'ajoute des relances avec backoff seulement pour les erreurs transitoires, j'ajoute un sensor ou une dépendance d'asset si la tâche démarre avant que son entrée soit prête, j'augmente les ressources ou la déplace dans un pool dédié, et je fais en sorte que les alertes ne partent qu'une fois les relances épuisées.

<!-- challenge -->

Un DAG de la finance doit finir avant 08:00, mais personne ne remarque quand il est en retard sans échouer. Que mettez-vous en place ?

<!-- solution -->

Une deadline alert (Airflow 3.1+) sur le DAG run pour 08:00 qui prévient les responsables, ou un contrôle séparé qui alerte si l'exécution n'a pas réussi à cette heure. Incluez le lien de l'exécution et le runbook dans le message.

<!-- takeaways -->

- Envoyez les logs vers un stockage distant ; exportez les métriques.
- Alertez les responsables avec contexte et lien vers le runbook.
- Corrigez les tâches instables pour que les alertes gardent leur sens.

<!-- unit: Diagnostiquer les tâches bloquées et qui meurent -->

<!-- goals -->

- Diagnostiquer les tâches bloquées en `queued` et les zombie tasks.
- Trouver la cause quand des tâches meurent sans erreur.

<!-- concept -->

Quand une tâche ne démarre jamais ou meurt en silence, le problème est généralement sous votre code. Une tâche en file attend un slot qu'une limite ou un worker absent ne libère jamais. Une tâche qui disparaît sans traceback a presque toujours été tuée de l'extérieur, souvent pour la mémoire, et le scheduler remarque ensuite l'absence de heartbeat.

Le débogage commence donc par la plateforme : limites, workers, événements des pods et métriques mémoire, avant le code de la tâche.

<!-- example -->

```bash
kubectl get events -n airflow --field-selector reason=OOMKilling
kubectl describe pod sales-load-transform-abc12 | grep -A3 "Last State"
#   Last State: Terminated  Reason: OOMKilled  Exit Code: 137
```

#### Quelles sont les causes fréquentes de tâches bloquées en `queued` ?

Pas de slot libre (limites de parallelism, de pool ou de concurrence du DAG), workers arrêtés ou ne consommant pas la file, executor incapable de démarrer des pods (quotas, erreurs de téléchargement d'image) ou problème de scheduler. Vérifiez les pools, les journaux des workers et les événements de l'executor.

#### Que sont les tâches zombies ?

Des task instances marquées en cours dont le processus est mort sans le signaler (plantage du worker, OOM kill, éviction du pod). Le scheduler détecte l'absence de heartbeat et les fait échouer ou les relance.

#### Des tâches sont souvent tuées sans erreur dans les journaux. Que soupçonnez-vous ?

Des arrêts pour manque de mémoire (OOM) du worker ou du pod, des évictions ou des timeouts. Vérifiez les événements des pods et les métriques des workers, augmentez les limites de mémoire et sortez le traitement lourd d'Airflow.

<!-- challenge -->

Après une mise en production, beaucoup de tâches restent en `queued` alors que les workers semblent inactifs. Citez trois points à vérifier.

<!-- solution -->

Que les workers consomment la bonne file (une file renommée bloque des tâches), qu'aucun pool ni limite de concurrence du DAG ne soit plein, et que l'executor puisse démarrer des pods (quotas, erreurs de téléchargement d'image). Les logs du scheduler nomment souvent la limite.

<!-- takeaways -->

- `queued` signale un problème de limites ou de workers, pas de code.
- Les zombies viennent de processus morts sans prévenir.
- Code de sortie 137 ou pas de traceback : pensez mémoire.

<!-- unit: Passage à l'échelle et santé de la base -->

<!-- goals -->

- Faire évoluer schedulers, workers et base avec le nombre de DAG.
- Maîtriser temps de parsing et taille de la base.

<!-- concept -->

Les limites d'Airflow apparaissent généralement dans cet ordre : le parsing, puis la base, puis les workers. Le parsing croît avec chaque fichier de DAG et chaque import lourd. La base croît avec chaque exécution et chaque XCom, et chaque tâche y ouvre des connexions. Les workers sont le plus simple à faire évoluer : réglez les deux premiers avant d'ajouter des machines.

L'essentiel du passage à l'échelle est de l'hygiène : fichiers de DAG légers, connexions à la base mutualisées, nettoyage périodique et attentes deferrable.

<!-- example -->

```bash
airflow dags report                                # parse time per file
airflow db clean --clean-before-timestamp "$(date -d '-90 days' +%F)" --yes
```

#### Comment faire monter Airflow en charge ?

Avec plusieurs schedulers, en dimensionnant les workers (autoscaling des workers Celery avec KEDA, ou executor Kubernetes), en utilisant des opérateurs différables pour libérer des slots, en réduisant la durée d'analyse des DAG, en réglant `parallelism` et les pools, et en gardant le calcul lourd hors d'Airflow.

#### Pourquoi la durée d'analyse des DAG est-elle importante ?

Une analyse lente retarde la planification de tous les DAG et consomme du CPU. On la mesure avec `airflow dags report` ; on la corrige en supprimant le travail de niveau supérieur, en évitant les imports lourds au niveau du module et en découpant les fichiers de DAG générés géants.

#### Comment garder la base de métadonnées en bonne santé ?

Utiliser un PostgreSQL managé avec sauvegardes, surveiller sa taille et lancer régulièrement `airflow db clean` pour purger les anciennes task instances, métadonnées de journaux et XCom. Une base énorme ralentit le scheduler et l'interface.

#### Pourquoi utiliser PgBouncer avec Airflow ?

Chaque tâche et composant ouvre des connexions à la base ; de nombreuses tâches concurrentes peuvent épuiser la limite de connexions de PostgreSQL. PgBouncer les mutualise. Dans Airflow 3, la Task Execution API réduit les connexions directes depuis les workers.

#### Des centaines de DAG sont lents à planifier. Qu'examinez-vous ?

La durée d'analyse des DAG (`airflow dags report`), le code et les imports de niveau supérieur, le nombre de fichiers de DAG, le CPU du scheduler et les performances de la base, le nombre de task instances en base (lancer `db clean`), et si le scheduler et le DAG processor ont assez de ressources ou de réplicas.

#### Le CPU de votre scheduler est à 100 %. Quelles sont les corrections habituelles ?

Réduire la charge d'analyse des DAG (fichiers moins nombreux et plus légers, `min_file_process_interval` plus long, DAG processor séparé), abandonner les sensors en mode poke, nettoyer la base, ajouter des réplicas du scheduler et examiner les DAG comportant un nombre énorme de tâches mappées.

<!-- challenge -->

La base de métadonnées atteint 400 Go et l'UI met 30 secondes à charger. Que faites-vous d'abord, et que planifiez-vous ?

<!-- solution -->

Sauvegarder, puis lancer `airflow db clean` pour purger task instances, XCom et métadonnées de logs au-delà de votre rétention. Planifier ce nettoyage chaque semaine (DAG de maintenance) et repérer les gros XCom qui devraient être des références.

<!-- takeaways -->

- Réglez parsing et base avant d'ajouter des workers.
- PgBouncer mutualise les nombreuses connexions des tâches.
- Nettoyez les anciennes métadonnées de façon planifiée.

### Bonnes pratiques

<!-- unit: Orchestrer, pas traiter -->

<!-- goals -->

- Dimensionner les tâches pour qu'elles aient du sens et se relancent à faible coût.
- Découper les pipelines en DAG selon calendriers et responsables.

<!-- concept -->

Airflow fonctionne mieux comme une fine couche de contrôle sur des systèmes qui font le travail. Des tâches qui traitent les données sur le worker se disputent la mémoire et ne passent pas à l'échelle. La bonne taille d'une tâche est une unité qu'on voudrait relancer seule ; celle d'un DAG, un calendrier et un responsable.

Comme les tâches peuvent tourner sur des machines différentes, tout ce qui passe entre elles doit vivre dans un stockage partagé, pas sur le disque local.

<!-- example -->

| Trop gros | Bonne taille | Trop fin |
|---|---|---|
| `run_everything` (2 h, tout relancer) | `load_orders`, `build_orders_mart` | une tâche par instruction SQL |

#### Airflow doit-il faire lui-même le traitement des données ?

Non. Airflow doit orchestrer : déclencher Spark, des moteurs SQL, dbt, Databricks ou des conteneurs qui font le traitement, et passer des références. Un traitement pandas lourd sur les workers Airflow concurrence les autres tâches et passe mal à l'échelle.

#### Quelle est une bonne granularité de tâches ?

Chaque tâche doit être une unité porteuse de sens et relançable (extraire une source, charger une table, exécuter un groupe de modèles). Trop grosse, elle oblige à relancer beaucoup de travail ; trop fine, elle ajoute de la surcharge de planification et rend le graphe illisible.

#### Pourquoi les DAG ne doivent-ils pas s'appuyer sur des fichiers locaux entre tâches ?

Les tâches peuvent tourner sur des workers ou des pods différents : un fichier écrit par une tâche peut ne pas exister pour la suivante. Utilisez un stockage objet, un volume partagé ou une base de données.

#### En combien de DAG découper un pipeline ?

Un DAG par planning et par périmètre de responsabilité indépendants. Découpez quand les parties ont des plannings, des responsables ou des domaines de panne différents, et reliez-les par des assets ; gardez dans un seul DAG les étapes fortement couplées.

<!-- challenge -->

Un DAG charge à 06:00 des données marketing, finance et produit, et appartient à trois équipes. Les échecs de l'une bloquent les autres. Comment le restructurez-vous ?

<!-- solution -->

Le découper en un DAG par domaine, chacun avec son responsable et ses alertes. Quand un domaine a besoin des données d'un autre, relier les DAG par des assets pour qu'ils tournent quand les données sont prêtes.

<!-- takeaways -->

- Airflow orchestre ; les moteurs traitent.
- Une tâche est une unité relançable ; un DAG, un calendrier et un responsable.
- Partagez les données via un stockage, pas via les disques des workers.

<!-- unit: Relances sûres et contrôles de données -->

<!-- goals -->

- Configurer des relances utiles aux erreurs transitoires sans masquer les bugs.
- Ajouter des contrôles de qualité comme points de passage dans un DAG.

<!-- concept -->

Les relances sont une assurance peu coûteuse contre les réseaux instables et les API saturées, mais seulement si les tâches sont idempotentes et les erreurs transitoires. Relancer trois fois un bug ne fait que retarder l'alerte. Le backoff et les pools transforment les relances en attente polie plutôt qu'en ruée.

Les contrôles de données sont l'autre moitié de la fiabilité : une tâche peut réussir et produire des données fausses. Des contrôles entre chargement et publication arrêtent les mauvaises données avant les consommateurs.

<!-- example -->

```python
SQLColumnCheckOperator(
    task_id="check_orders", conn_id="warehouse", table="silver.orders",
    column_mapping={"order_id": {"null_check": {"equal_to": 0}, "unique_check": {"equal_to": 0}}},
)
```

#### Comment rendre les relances sûres ?

En rendant les tâches idempotentes, en fixant `retries` et `retry_delay` (avec `retry_exponential_backoff`) pour les erreurs transitoires, et en échouant vite (sans relance) pour les erreurs qu'une relance ne corrige pas, comme des identifiants invalides ou un échec de qualité des données.

#### Une tâche échoue aléatoirement à cause de la limite de débit d'une API. Que faites-vous ?

J'ajoute des relances avec backoff exponentiel, je place les appels d'API dans un pool qui limite la concurrence, je respecte `Retry-After` dans le hook et je réduis les appels (regroupement, extraction incrémentale).

#### Comment faire des contrôles de qualité des données dans Airflow ?

Avec les opérateurs de contrôle SQL (`SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLCheckOperator`), les opérateurs Great Expectations ou Soda, ou les tests dbt, placés après les chargements pour arrêter les tâches en aval quand les données sont fausses.

<!-- challenge -->

Une tâche de chargement se relance cinq fois sur une incompatibilité de schéma et finit par échouer deux heures plus tard. Que changez-vous ?

<!-- solution -->

Échouer vite sur les erreurs non transitoires : intercepter les erreurs de schéma et lever un échec sans relance, en gardant relances avec backoff pour les timeouts et le throttling. Ajouter un contrôle de schéma avant le chargement.

<!-- takeaways -->

- Relancez les erreurs transitoires avec backoff ; échouez vite sur les bugs.
- Pools et backoff protègent les systèmes limités en débit.
- Contrôlez la qualité avant de publier.

<!-- unit: Organiser code et configuration -->

<!-- goals -->

- Organiser code partagé, configuration et nommage entre DAG.
- Garder les DAG lisibles pour la prochaine personne d'astreinte.

<!-- concept -->

Un dépôt de cinquante DAG a besoin de la même structure que tout code. La logique partagée vit dans un paquet testé, pas copiée entre fichiers. La configuration se répartit selon sa fréquence de changement : la structure dans le code, les valeurs par environnement dans des variables, les identifiants dans des secrets.

La lisibilité est une question d'exploitation. La personne qui lit un DAG à 3 h du matin ne l'a pas écrit : noms cohérents, petites tâches et documentation décident de la vitesse à laquelle elle peut agir.

<!-- example -->

```text
dags/
  sales__daily_load.py      # thin: schedule, tasks, dependencies
  finance__month_close.py
include/
  common/warehouse.py       # shared, tested code
tests/
```

#### Où doit vivre la configuration ?

Dans le code (versionné) pour la structure, dans des variables d'environnement ou des Variables pour les valeurs propres à chaque environnement, et dans un secrets backend pour les identifiants. Évitez de lire de nombreuses Variables à l'analyse des DAG.

#### Comment nommer les DAG et les tâches ?

De façon cohérente et descriptive : `domaine__objectif` pour les DAG (`sales__daily_load`), des verbes pour les tâches (`extract_orders`, `load_orders`), avec des owners et des tags pour les équipes et les domaines de données.

#### Comment gérer le code partagé entre DAG ?

En le plaçant dans un paquet Python (dans le dossier `include/` ou `plugins/` du dépôt, ou installé dans l'image) avec ses propres tests, plutôt qu'en copiant du code d'un fichier de DAG à l'autre.

#### Comment garder un DAG lisible ?

Des tâches petites et bien nommées, des task groups pour les blocs logiques, aucune logique métier dans le fichier du DAG, une documentation avec `doc_md`, un usage cohérent de TaskFlow ou des opérateurs, et peu de génération dynamique.

<!-- challenge -->

Cinq DAG contiennent chacun une copie de la même fonction de 80 lignes pour charger des fichiers dans l'entrepôt, avec de petites différences. Que faites-vous ?

<!-- solution -->

Extraire une fonction paramétrée (ou un opérateur personnalisé) dans un paquet partagé et testé, remplacer les copies et exprimer les différences en paramètres. Les corrections futures se font une seule fois.

<!-- takeaways -->

- Le code partagé va dans un paquet testé.
- Structure dans le code, valeurs d'environnement en variables, identifiants en secrets.
- Des noms et docs cohérents accélèrent la réponse aux incidents.

<!-- unit: Étendre Airflow et lignage -->

<!-- goals -->

- Savoir ce que plugins et listeners ajoutent à Airflow.
- Émettre du lignage avec OpenLineage.

<!-- concept -->

Airflow offre des points d'extension pour ce que les opérateurs ne font pas. Les plugins ajoutent des vues d'UI, des macros ou des timetables. Les listeners réagissent à des événements comme la fin d'une tâche, ce qui en fait l'endroit naturel pour les sujets transverses : lignage, audit ou métriques maison.

OpenLineage s'appuie sur les listeners : les providers décrivent entrées et sorties de chaque tâche et un backend assemble un graphe de lignage entre outils, pas seulement dans Airflow.

<!-- example -->

```bash
pip install apache-airflow-providers-openlineage
export AIRFLOW__OPENLINEAGE__TRANSPORT='{"type": "http", "url": "http://marquez:5000"}'
```

#### À quoi servent les plugins dans Airflow ?

À étendre Airflow avec des vues d'interface, des liens de menu, des macros, des listeners, des timetables et, dans Airflow 3, des applications FastAPI et des vues React. Les opérateurs et hooks personnalisés n'ont pas besoin d'être des plugins ; de simples modules Python suffisent.

#### Que sont les listeners ?

Des points d'accroche sur les événements d'Airflow (début ou fin d'un DAG run, changements d'état des task instances) implémentés avec pluggy, utilisés pour le lignage (OpenLineage), l'audit ou des notifications personnalisées.

#### Qu'est-ce qu'OpenLineage dans Airflow ?

Un standard de métadonnées de lignage. Le provider OpenLineage émet des événements décrivant les entrées et sorties des tâches vers un backend comme Marquez ou un catalogue de données, pour voir quels jobs lisent et écrivent quels jeux de données.

<!-- challenge -->

La conformité demande quels tableaux de bord dépendent d'une table clients chargée par Airflow. Comment le lignage pourrait-il répondre automatiquement ?

<!-- solution -->

Activer le provider OpenLineage pour que les tâches émettent leurs datasets d'entrée et de sortie, envoyer les événements à un backend de lignage qui reçoit aussi ceux de dbt et des outils de BI, et interroger le graphe aval de la table clients.

<!-- takeaways -->

- Les plugins étendent l'UI et l'ordonnancement ; les listeners réagissent aux événements.
- OpenLineage émet automatiquement entrées et sorties des tâches.
- Le lignage répond aux questions d'impact entre outils.

<!-- stage: Tout assembler -->

### Mises en situation

<!-- unit: Concevoir un DAG ELT quotidien -->

<!-- goals -->

- Combiner sensors, chargements, dbt et contrôles dans un DAG quotidien.
- Justifier chaque choix dans une réponse d'entretien.

<!-- concept -->

Les questions de conception testent votre capacité à relier les pièces : quand les données sont prêtes, comment les charger de façon idempotente, comment exécuter les transformations, comment faire remonter les échecs. Une bonne réponse suit les données, nomme un outil par étape, puis explique ce qui se passe à la relance et qui est alerté. Citer attentes deferrable, chargements par intervalle et tâches dbt par modèle montre que vous connaissez les pièges de la production.

<!-- example -->

```text
wait_for_files (deferrable S3KeySensor, timeout 6h)
  ─► copy_into_snowflake (interval's prefix, idempotent)
  ─► dbt models (Cosmos task group)
  ─► data checks ─► asset event: marts.sales
```

#### Un DAG quotidien doit charger les fichiers de la veille depuis S3 dans Snowflake, puis lancer dbt. Concevez-le.

Un DAG quotidien avec `catchup=False` (ou true si l'historique compte), un `S3KeySensor` différable sur le préfixe attendu pour l'intervalle de données, un `CopyFromExternalStageToSnowflakeOperator` ou une tâche SQL lançant `COPY INTO`, puis dbt via Cosmos ou un opérateur dbt Cloud, des contrôles de qualité et des callbacks d'échec vers Slack. Tous les chemins et filtres viennent de l'intervalle de données.

<!-- challenge -->

L'équipe source prévient que les fichiers peuvent être corrigés et renvoyés jusqu'à trois jours plus tard. Adaptez la conception.

<!-- solution -->

Traiter les trois derniers intervalles à chaque exécution, ou déclencher des relances sur nouveaux fichiers avec des asset watchers. Faire remplacer par le chargement Snowflake la tranche de chaque jour (suppression puis insertion, ou `MERGE`) pour que les corrections écrasent, et laisser dbt reconstruire les jours concernés.

<!-- takeaways -->

- Suivez les données de l'arrivée aux consommateurs, un outil par étape.
- Des chargements idempotents par intervalle sécurisent les relances.
- Terminez par contrôles, alertes et ce que reçoivent les consommateurs.

<!-- unit: Conditionner un rapport à la qualité des données -->

<!-- goals -->

- Déclencher un rapport seulement quand ses entrées sont complètes et justes.
- Décider de ce qui se passe quand le contrôle échoue.

<!-- concept -->

Les utilisateurs métier tiennent davantage à un rapport juste qu'à un rapport ponctuel. Une bonne conception rend la complétude explicite : le rapport dépend des données, pas d'une horloge, et un contrôle compare ce qui est arrivé à ce qui était attendu avant tout envoi. Si le contrôle échoue, il faut prévenir quelqu'un et ne pas envoyer, plutôt que d'expédier un chiffre faux.

<!-- example -->

```python
@dag(schedule=[Asset("snowflake://analytics/sales_daily")])
def sales_report():
    check = SQLCheckOperator(task_id="complete",
        conn_id="warehouse",
        sql="SELECT count(*) >= 0.95 * expected FROM sales_completeness WHERE day = '{{ ds }}'")
    check >> send_report()
```

#### Un utilisateur métier veut recevoir un rapport par e-mail seulement si les ventes de la veille sont complètes. Comment ?

Je planifie le DAG du rapport sur l'asset des ventes (ou un sensor sur le chargement), j'ajoute un contrôle de qualité (nombre de lignes et complétude par rapport aux sources attendues), je court-circuite l'e-mail si les contrôles échouent, et j'alerte alors l'équipe data.

<!-- challenge -->

Un matin, le contrôle échoue parce qu'un seul magasin n'a pas envoyé ses données. Le métier veut quand même le rapport, signalé comme tel. Que changez-vous ?

<!-- solution -->

Faire renvoyer au contrôle la liste des magasins manquants et brancher : envoyer le rapport avec un bandeau « données partielles » qui les liste, et alerter les responsables. Garder un arrêt complet seulement si la complétude passe sous un seuil convenu.

<!-- takeaways -->

- Planifiez les rapports sur les données, pas sur l'horloge.
- Vérifiez la complétude avant d'envoyer.
- Convenez avec les utilisateurs de ce que doivent produire des données partielles.
