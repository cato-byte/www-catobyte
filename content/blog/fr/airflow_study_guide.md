## Fiche d'étude Apache Airflow

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![Fiche d'étude Apache Airflow : environ 200 questions](../../images/airflow_study_guide_title_img.png)

Environ 200 questions d'entretien sur Apache Airflow, des DAG et opérateurs à la planification, aux sensors, aux assets, aux executors, aux tests, au déploiement et au dépannage. Les réponses suivent Airflow 3 et signalent ce qui a changé depuis Airflow 2, car beaucoup d'entreprises utilisent encore les deux. Ouvrez une question pour voir sa réponse, ou utilisez le filtre pour chercher dans toute la fiche.

<!-- QA -->

### Fondamentaux

#### Qu'est-ce qu'Apache Airflow ?

Une plateforme open source pour écrire, planifier et superviser des workflows sous forme de code. Les workflows sont des DAG de tâches définis en Python ; Airflow les exécute selon un planning ou sur événement, dans l'ordre des dépendances, avec relances, journaux, alertes et une interface web. Né chez Airbnb en 2014, c'est un projet Apache de premier niveau.

#### À quoi sert Airflow, et à quoi ne sert-il pas ?

Il sert à orchestrer des workflows batch : ETL/ELT, déclenchement de jobs dans d'autres systèmes (Spark, dbt, Databricks, Snowflake, Glue), pipelines de ML, rapports et maintenance. Ce n'est pas un moteur de traitement de données (le calcul lourd doit se faire dans les systèmes qu'il déclenche), ni un moteur de streaming, et il n'est pas conçu pour des planifications à très haute fréquence, sous la seconde.

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

#### Qu'apporte l'écriture des workflows sous forme de code ?

Le contrôle de version, la revue de code, les tests, la génération dynamique de tâches, la réutilisation via des fonctions et bibliothèques Python, et la possibilité de déployer les workflows en CI/CD comme n'importe quel logiciel.

#### Quels sont les principaux composants d'un déploiement Airflow ?

Le scheduler (décide quoi exécuter et quand), le DAG processor (analyse les fichiers de DAG), l'API server (sert l'interface et l'API REST ; c'était le webserver dans Airflow 2), l'executor et ses workers (exécutent les tâches), le triggerer (exécute les tâches différées) et la base de métadonnées (stocke l'état).

#### Qu'est-ce que la base de métadonnées ?

Une base relationnelle (PostgreSQL ou MySQL en production ; SQLite seulement pour les tests) qui stocke les DAG runs, les task instances, les connexions, les variables, les XCom, les utilisateurs et les DAG sérialisés. C'est la source de vérité de l'état d'Airflow : il faut la sauvegarder et l'entretenir.

#### Quels sont les principaux changements d'Airflow 3 ?

Une nouvelle interface React, le versionnage des DAG (chaque exécution est liée à la version du DAG avec laquelle elle a tourné), le Task SDK et une Task Execution API pour que les workers ne parlent plus directement à la base de métadonnées, `airflow api-server` à la place du webserver, les datasets renommés en assets avec une planification par événements, les backfills gérés par le scheduler, la suppression des SubDAG et des SLA, et `schedule` à la place de `schedule_interval`.

#### Qu'est-ce que le Task SDK ?

L'interface publique et stable pour écrire des DAG dans Airflow 3 (`from airflow.sdk import dag, task, DAG, Asset, Variable`). Elle découple le code des DAG des mécanismes internes d'Airflow et permet d'exécuter les tâches à distance via la Task Execution API, voire dans d'autres langages à l'avenir.

#### Qu'est-ce qu'un provider Airflow ?

Un paquet versionné séparément qui ajoute opérateurs, hooks, sensors et connexions pour un système externe : `apache-airflow-providers-amazon`, `-google`, `-databricks`, `-snowflake`, `-postgres`, `-standard` (les opérateurs de base comme `BashOperator` et `PythonOperator` dans Airflow 3) et bien d'autres.

#### Qu'est-ce qu'un hook ?

Une classe qui encapsule la connexion à un système externe et expose des méthodes utilitaires, comme `S3Hook.load_file()` ou `PostgresHook.get_records()`. Les opérateurs utilisent des hooks en interne ; vous pouvez aussi les utiliser dans vos propres tâches Python.

#### Qu'est-ce qu'une connexion ?

Un ensemble enregistré d'identifiants et de paramètres pour un système externe (hôte, utilisateur, mot de passe, schéma, port, JSON extra), référencé par un `conn_id`. Elle peut être stockée dans la base de métadonnées, dans des variables d'environnement (`AIRFLOW_CONN_<ID>`) ou dans un secrets backend.

#### Que sont les Variables Airflow ?

Des valeurs de configuration clé-valeur stockées dans Airflow (base de métadonnées, variables d'environnement `AIRFLOW_VAR_<NOM>` ou secrets backend) et lues avec `Variable.get()`. Les lire au niveau supérieur d'un fichier de DAG provoque un appel à la base ou au backend à chaque analyse : lisez-les dans les tâches ou via les templates.

#### Quelle est la différence entre Airflow et cron ?

Cron ne fait que lancer des commandes à heure fixe. Airflow ajoute les dépendances entre tâches, les relances, les backfills, l'historique, des journaux centralisés, les alertes, le paramétrage, une interface et l'intégration avec des systèmes externes.

#### Comment Airflow se compare-t-il à Dagster et Prefect ?

Tous trois orchestrent des workflows Python. Airflow est le plus déployé, avec le plus grand écosystème de providers. Dagster est centré sur les assets (on déclare les actifs de données et leur lignage), avec un typage fort et des tests locaux. Prefect mise sur des flux Python dynamiques avec peu de code répétitif. Airflow 3 s'est rapproché des idées de Dagster avec les assets et le versionnage.

#### Quels services Airflow managés existent ?

Amazon MWAA (Managed Workflows for Apache Airflow), Google Cloud Composer, Astronomer (Astro) et l'offre Airflow d'Azure dans Data Factory/Fabric. Ils gèrent le scheduler, les workers, la base de données et les mises à jour.

#### Que signifie « orchestration », par opposition à « traitement » ?

L'orchestration décide de ce qui s'exécute, quand, dans quel ordre et ce qui se passe en cas d'échec. Le traitement est le calcul effectif sur les données. Airflow orchestre ; Spark, les moteurs SQL et dbt traitent.

#### À quoi sert la CLI `airflow` ?

À gérer et déboguer Airflow : `airflow dags list|trigger|pause|test`, `airflow tasks test|clear`, `airflow db migrate|clean`, les commandes `airflow connections` et `variables`, `airflow config get-value`, et le démarrage des composants (`scheduler`, `api-server`, `dag-processor`, `triggerer`, `celery worker`).

#### Qu'offre l'API REST ?

Une API stable et versionnée (servie par l'API server) pour déclencher et gérer des DAG runs, lire l'état et les journaux des task instances, gérer connexions, variables et pools, et effacer des tâches. Les pipelines de CI et d'autres systèmes l'utilisent pour s'intégrer à Airflow.

#### Que fait la mise en pause d'un DAG ?

Un DAG en pause ne crée plus de nouvelles exécutions planifiées ; les tâches en cours se terminent. Les nouveaux DAG sont en pause par défaut (`dags_are_paused_at_creation`) pour ne pas démarrer dès leur déploiement.

#### Quels états un DAG run peut-il avoir ?

`queued`, `running`, `success` et `failed`. L'état d'un DAG run découle de ses tâches finales : il réussit si elles réussissent toutes ou sont ignorées.

#### Que signifie `upstream_failed` ?

Que la tâche ne s'est pas exécutée parce qu'une tâche amont a échoué et que sa trigger rule (par défaut `all_success`) ne pouvait pas être satisfaite.

### Écrire des DAG

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

#### Comment définir les dépendances entre tâches ?

Avec les opérateurs de décalage de bits (`extract >> transform >> load`), des listes pour l'éventail et la convergence (`start >> [a, b] >> end`), les fonctions `chain()` et `cross_downstream()`, ou implicitement en passant les sorties TaskFlow en arguments.

#### Que sont les `default_args` ?

Un dictionnaire d'arguments appliqué à toutes les tâches d'un DAG, comme `owner`, `retries`, `retry_delay`, `email_on_failure` ou `execution_timeout`. Les tâches peuvent les surcharger.

#### Que signifie `start_date` ?

La date à partir de laquelle le DAG peut être planifié. Ce doit être une date fixe dans le passé, jamais `datetime.now()`, qui changerait à chaque analyse et empêcherait la création d'exécutions.

#### Qu'est-ce que `catchup` ?

Le fait que le scheduler crée ou non des exécutions pour tous les intervalles manqués entre `start_date` (ou la dernière exécution) et maintenant. Dans Airflow 3, la valeur par défaut est `False` ; dans Airflow 2, c'était `True`. Laisser catchup actif sur un DAG avec une date de début ancienne peut lancer des centaines d'exécutions d'un coup.

#### À quoi servent les tags et `doc_md` ?

Les tags regroupent et filtrent les DAG dans l'interface. `doc_md` attache une documentation Markdown au DAG ou à une tâche, visible dans l'interface, ce qui aide la personne d'astreinte à comprendre ce que fait un DAG.

#### Pourquoi le niveau supérieur des fichiers de DAG doit-il rester léger ?

Le DAG processor analyse chaque fichier de DAG à répétition (toutes les 30 secondes par défaut pour les fichiers modifiés). Le code de niveau supérieur, comme des requêtes en base, des appels d'API, `Variable.get()` ou des imports lourds, s'exécute à chaque analyse, ralentit tout le scheduler et sollicite les systèmes externes. Ce travail doit aller dans les tâches.

#### Comment générer des DAG ou des tâches dynamiquement ?

Avec une boucle Python sur une configuration (une liste, un YAML lu sur disque) pour créer des tâches ou plusieurs DAG à l'analyse, ou avec le mapping dynamique de tâches pour l'éventail à l'exécution. Gardez la configuration statique et rapide à lire pour que l'analyse reste rapide et déterministe.

#### Qu'est-ce qu'un task group ?

Un moyen de regrouper visuellement et logiquement des tâches dans l'interface (`@task_group` ou `TaskGroup`), avec un préfixe commun pour les identifiants de tâches et des arguments par défaut partagés. Il a remplacé les SubDAG, supprimés dans Airflow 3.

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

#### Comment exécuter une tâche dans un environnement Python isolé ?

Avec `@task.virtualenv` (crée un virtualenv avec les dépendances indiquées), `@task.external_python` (utilise un interpréteur existant), `@task.docker` ou `@task.kubernetes` (exécution dans un conteneur). On évite ainsi les conflits de dépendances avec Airflow lui-même.

#### Comment passer des paramètres à un DAG run ?

Avec des `params` déclarés sur le DAG (avec valeurs par défaut et validation JSON Schema optionnelle), présentés sous forme de formulaire lors d'un déclenchement manuel, et lus avec `{{ params.nom }}` ou depuis le contexte.

#### À quoi sert le `BashOperator`, et quel est le risque ?

À exécuter des commandes ou des scripts shell. Le risque est d'injecter dans la commande des entrées non fiables via les templates, et de cacher une logique complexe dans du shell, difficile à tester.

#### Comment fixer un timeout sur une tâche ?

Avec `execution_timeout` (un `timedelta`) ; la tâche échoue si elle dure plus longtemps. Un `dagrun_timeout` au niveau du DAG fait échouer toute l'exécution après une durée donnée.

#### Que fait `max_active_runs` ?

Il limite le nombre d'exécutions actives simultanées d'un DAG. Le fixer à 1 garantit des exécutions séquentielles, important pour les pipelines qui dépendent de la sortie de l'exécution précédente.

#### Qu'est-ce que `depends_on_past` ?

Un argument de tâche : s'il vaut `True`, une task instance ne s'exécute que si la même tâche a réussi (ou a été ignorée) dans le DAG run précédent. Il impose un traitement séquentiel au niveau de la tâche.

#### Quelle est la différence entre `@task` et `PythonOperator` ?

Les deux exécutent une fonction Python. `@task` (TaskFlow) est plus concis, passe les valeurs renvoyées via XCom automatiquement et déduit les dépendances. `PythonOperator` est la forme classique ; on câble XCom et dépendances à la main. On peut mélanger les deux dans un DAG.

#### Comment mélanger tâches TaskFlow et opérateurs classiques ?

Les opérateurs classiques exposent `.output` (un `XComArg`) qu'on peut passer à des fonctions TaskFlow, et les sorties TaskFlow peuvent être passées aux champs templatés des opérateurs classiques. Les dépendances sont déduites de ces liens.

#### Qu'est-ce que `@task.sensor` ?

Un décorateur qui transforme une fonction Python en sensor : elle renvoie `True` (ou un `PokeReturnValue`) quand la condition est remplie, avec les options habituelles `poke_interval`, `timeout` et `mode`.

#### Que sont `@setup` et `@teardown` ?

Des décorateurs qui marquent les tâches créant et nettoyant des ressources (un cluster, une table temporaire). Un teardown s'exécute même si le travail intermédiaire échoue, et effacer une tâche relance aussi son setup et son teardown.

#### Comment définir un owner, et pourquoi est-ce important ?

Avec `owner` dans `default_args`. Il apparaît dans l'interface et les alertes, pour contacter la bonne équipe quand le DAG échoue.

#### Qu'est-ce que `email_on_failure` ?

Un argument de tâche qui envoie un e-mail quand la tâche échoue, via la configuration SMTP. La plupart des équipes préfèrent des callbacks ou notifiers vers Slack ou PagerDuty, pour des alertes plus riches et routables.

#### Que se passe-t-il quand on renomme une tâche ou un DAG ?

Airflow le traite comme une nouvelle tâche ou un nouveau DAG : l'historique reste sous l'ancien nom. Dans Airflow 3, le versionnage des DAG montre le changement, mais renommer casse toujours la continuité des métriques et de `depends_on_past`.

### Planification et temps

#### Comment planifier un DAG ?

Avec l'argument `schedule` : une expression cron (`"0 6 * * *"`), un preset (`"@daily"`, `"@hourly"`), un `timedelta`, un timetable, une liste d'assets (par événements) ou `None` pour les DAG manuels ou déclenchés de l'extérieur.

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

#### Qu'est-ce qu'un timetable ?

Une classe qui définit un planning personnalisé quand cron ne suffit pas : jours ouvrés seulement, plusieurs horaires selon les jours, calendriers fiscaux. Les timetables fournis sont `CronDataIntervalTimetable`, `CronTriggerTimetable`, `DeltaDataIntervalTimetable` et `MultipleCronTriggerTimetable`.

#### Comment Airflow gère-t-il les fuseaux horaires ?

En interne, tout est stocké en UTC. On peut donner à un DAG une `start_date` avec fuseau (via `pendulum`), et les plannings cron suivent alors ce fuseau, y compris les changements d'heure. L'interface peut afficher l'heure locale.

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

#### Pourquoi les tâches ne doivent-elles pas utiliser `datetime.now()` ?

Parce que les relances et les backfills traiteraient la mauvaise période. Utilisez la date logique ou l'intervalle de données du contexte ou des templates.

#### Comment exécuter un DAG uniquement les jours ouvrés ?

Avec une expression cron comme `0 6 * * 1-5`, ou un timetable personnalisé si les jours fériés comptent. Une tâche de branchement ou de court-circuit peut aussi sauter le traitement les jours fériés d'après une table calendrier.

#### Qu'est-ce que le preset `@once` ?

Un planning qui crée une seule exécution, utile pour des DAG ponctuels comme des migrations.

#### Que se passe-t-il si une exécution dure plus longtemps que l'intervalle de planification ?

L'exécution suivante démarre à son heure si `max_active_runs` le permet, donc les exécutions peuvent se chevaucher. Fixez `max_active_runs=1` (et éventuellement `depends_on_past=True`) quand elles ne doivent pas se chevaucher.

#### Comment passer à une tâche la date de la dernière exécution réussie ?

Avec les variables de template `prev_data_interval_start_success` et `prev_data_interval_end_success` (ou `prev_start_date_success`), utiles pour des chargements incrémentaux qui doivent reprendre au dernier point réussi.

#### Comment les changements d'heure affectent-ils les plannings ?

Avec une date de début munie d'un fuseau, un cron quotidien à 02 h 30 peut être sauté ou exécuté deux fois les jours de changement, selon l'horloge locale. Planifiez les jobs critiques hors de la plage 01 h–03 h, ou en UTC.

### Opérateurs, sensors et tâches différables

#### Qu'est-ce qu'un sensor ?

Un opérateur spécial qui attend une condition : un fichier dans S3 (`S3KeySensor`), une partition, une tâche externe, une requête SQL qui renvoie des lignes, un endpoint HTTP, une heure. Il vérifie périodiquement jusqu'à ce que la condition soit vraie ou que le timeout expire.

#### Quelle est la différence entre les modes `poke` et `reschedule` ?

En mode `poke`, le sensor occupe un slot de worker pendant toute l'attente, en dormant entre les vérifications. En mode `reschedule`, il libère le slot entre les vérifications et est replanifié plus tard, ce qui convient mieux aux longues attentes. Le mode différable est encore meilleur.

#### Que sont les opérateurs différables ?

Des opérateurs qui, pendant qu'ils attendent quelque chose d'externe (un job, un fichier, une heure), se suspendent et confient l'attente à un trigger asynchrone exécuté dans le processus triggerer, libérant le slot du worker. Quand le trigger se déclenche, la tâche reprend sur un worker. De nombreux opérateurs de providers ont `deferrable=True`.

#### Qu'est-ce que le triggerer ?

Un composant qui exécute les triggers asyncio des tâches différées. Un seul triggerer peut gérer des milliers d'attentes simultanées avec peu de ressources.

#### Qu'est-ce qu'`ExternalTaskSensor` ?

Un sensor qui attend qu'une tâche ou un DAG run d'un autre DAG atteigne un état, pour la même date logique par défaut. Il crée des dépendances entre DAG mais couple les plannings ; les assets sont souvent une alternative plus propre.

#### Qu'est-ce que `TriggerDagRunOperator` ?

Un opérateur qui déclenche un autre DAG, éventuellement en lui passant une configuration et en attendant sa fin. C'est une dépendance de type « push », par opposition au « pull » de l'`ExternalTaskSensor`.

#### Qu'est-ce que le timeout d'un sensor, et pourquoi le fixer ?

La durée maximale d'attente d'un sensor avant échec (`timeout`, sept jours par défaut). Donnez-lui une valeur réaliste pour qu'un fichier amont manquant soit remarqué vite au lieu de bloquer des ressources pendant des jours. `soft_fail=True` marque le sensor comme ignoré au lieu d'échoué.

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

#### Comment appeler une base SQL depuis Airflow ?

Avec `SQLExecuteQueryOperator` (provider common SQL) et une connexion, ou avec le hook spécifique du provider dans une tâche Python. Gardez le SQL dans des fichiers `.sql` séparés, référencés via les templates.

#### Comment déclencher un job Databricks depuis Airflow ?

Avec `DatabricksRunNowOperator` (exécute un job existant par son identifiant, avec des paramètres) ou `DatabricksSubmitRunOperator` (soumet une exécution ponctuelle), du provider Databricks, généralement en mode différable pour que l'attente n'occupe pas de worker. `DatabricksWorkflowTaskGroup` peut définir un job Databricks depuis Airflow.

#### Comment exécuter dbt depuis Airflow ?

Avec un `BashOperator` qui appelle `dbt build`, avec un opérateur dbt Cloud (`DbtCloudRunJobOperator`), ou avec Astronomer Cosmos, qui transforme chaque modèle dbt en tâche Airflow avec les dépendances du graphe dbt.

#### Comment exécuter du travail sur Kubernetes depuis Airflow ?

Avec `KubernetesPodOperator` ou `@task.kubernetes`, qui démarrent un pod avec une image, une commande, des ressources et des secrets donnés pour chaque tâche. Chaque tâche a ses propres dépendances et ressources.

#### À quoi sert `PythonVirtualenvOperator` ?

À exécuter une fonction dont les dépendances entrent en conflit avec celles d'Airflow, dans un virtualenv neuf à chaque exécution (plus lent) ou mis en cache. La fonction doit être autonome car elle s'exécute dans un autre interpréteur.

#### Que sont les opérateurs de transfert ?

Des opérateurs qui déplacent des données entre deux systèmes en une seule tâche, comme `S3ToRedshiftOperator`, `GCSToBigQueryOperator`, `SqlToS3Operator` ou `S3ToSnowflakeOperator`. Ils délèguent généralement le travail au système cible (par exemple une commande `COPY`).

#### À quoi sert `HttpOperator` ?

À appeler des API HTTP avec une connexion définissant l'URL de base et les identifiants, avec contrôles de réponse et pagination optionnels. `HttpSensor` attend qu'un endpoint renvoie une condition.

#### Comment lancer un job AWS Glue depuis Airflow ?

Avec `GlueJobOperator` du provider Amazon, en passant le nom du job et les arguments du script, de préférence avec `deferrable=True` ou `wait_for_completion` et un `GlueJobSensor`.

#### Comment lancer une requête Athena depuis Airflow ?

Avec `AthenaOperator`, qui soumet la requête, attend sa fin et écrit les résultats à l'emplacement de sortie S3 configuré. Utilisez des dates templatées dans la requête pour traiter l'intervalle de données.

#### Qu'est-ce que `on_execute_callback` ?

Un callback appelé juste avant l'exécution d'une tâche, utilisé pour la journalisation ou des notifications. Comme les autres callbacks, il doit être rapide et ne doit pas faire échouer la tâche.

### XCom et passage de données

#### Qu'est-ce que XCom ?

« Cross-communication » : un mécanisme pour passer de petites valeurs entre tâches. Une tâche publie une valeur (les valeurs renvoyées en TaskFlow sont publiées automatiquement) et les tâches en aval la lisent. Par défaut, les valeurs sont stockées dans la base de métadonnées.

#### Pourquoi ne pas faire passer de gros volumes par XCom ?

Le backend par défaut stocke les valeurs dans la base de métadonnées, qui n'est pas faite pour de gros contenus, et les valeurs sérialisées ont des limites de taille. Passez des références (un chemin S3, un nom de table, une partition) et laissez les données dans le stockage.

#### Qu'est-ce qu'un backend XCom personnalisé ?

Un backend interchangeable qui stocke les valeurs XCom ailleurs (S3, GCS, Azure Blob) et ne garde qu'une référence en base. Le provider Common IO fournit un backend de stockage objet avec un seuil de taille.

#### Comment lire un XCom dans un template ?

```
{{ ti.xcom_pull(task_ids='extract', key='return_value') }}
```

Avec TaskFlow, il suffit de passer la sortie d'une fonction de tâche en argument d'une autre.

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

#### Que fait `multiple_outputs=True` ?

Sur un `@task` qui renvoie un dictionnaire, il publie chaque clé comme un XCom séparé, pour que les tâches en aval puissent utiliser `result["cle"]` individuellement.

#### Les XCom sont-ils supprimés après une exécution ?

Ils restent en base (et sont effacés quand une tâche est effacée et relancée) jusqu'à leur purge avec `airflow db clean` ou une politique de rétention. Raison de plus pour les garder petits.

#### Qu'est-ce que `XComArg` ?

L'objet obtenu en appelant une fonction TaskFlow ou en accédant à `.output` d'un opérateur. Il représente une valeur future et porte la dépendance : le passer à une autre tâche relie les deux.

#### Comment éviter les erreurs de sérialisation avec XCom ?

En renvoyant des valeurs sérialisables en JSON (ou des types qu'Airflow sait sérialiser, comme les dataclasses et les DataFrames pandas avec le bon sérialiseur) ; évitez les connexions ouvertes, les générateurs et les gros objets. Renvoyez plutôt des chemins ou des identifiants.

### Assets et planification par événements

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

#### Que sont les asset watchers ?

Une fonction d'Airflow 3 pour la planification par événements venant de systèmes externes : un `AssetWatcher` associe un trigger (par exemple sur une file de messages comme SQS ou Kafka) à un asset, pour qu'un DAG s'exécute à l'arrivée d'un événement externe, et pas seulement quand une autre tâche Airflow met à jour l'asset.

#### Qu'est-ce que le décorateur `@asset` ?

Un raccourci d'Airflow 3 qui définit un asset avec le DAG à une seule tâche qui le matérialise, pour une écriture centrée sur les assets, à la manière de Dagster.

#### Les assets savent-ils si les données ont réellement changé ?

Non. Airflow sait seulement qu'une tâche productrice a réussi ; il n'inspecte pas les données. Si une tâche peut réussir sans rien écrire, elle ne doit pas émettre l'événement, ou le consommateur doit vérifier.

#### Peut-on attacher des métadonnées à un événement d'asset ?

Oui. Une tâche productrice peut ajouter des informations (par exemple le nombre de lignes ou la partition écrite) à l'événement via les outlet events, et les consommateurs peuvent les lire dans les événements déclencheurs de leur contexte.

#### Comment voir le lignage des assets dans l'interface ?

La vue des assets montre chaque asset avec ses DAG producteurs et consommateurs et l'historique des événements, ce qui rend visibles les dépendances entre DAG.

#### Qu'est-ce qu'un asset alias ?

Un substitut utilisé quand l'URI exacte de l'asset n'est connue qu'à l'exécution : la tâche émet des événements pour un alias en y attachant l'asset concret, et les consommateurs peuvent se planifier sur l'alias.

#### Un DAG peut-il être déclenché à la fois par un planning et par des assets ?

Oui, avec `AssetOrTimeSchedule`, qui s'exécute selon un timetable et aussi chaque fois que la condition sur les assets est remplie.

### Executors et architecture

#### Qu'est-ce qu'un executor ?

Le composant qui décide comment et où les task instances s'exécutent. Le scheduler envoie les tâches en file à l'executor, qui les exécute localement ou les répartit sur des workers.

#### Quels executors sont disponibles ?

`LocalExecutor` (processus parallèles sur la machine du scheduler), `CeleryExecutor` (un ensemble de workers alimentés par un broker de messages comme Redis ou RabbitMQ), `KubernetesExecutor` (un pod par tâche) et des executors de providers comme ceux d'AWS ECS et Batch et l'Edge executor pour des workers distants. Depuis Airflow 2.10, on peut utiliser plusieurs executors à la fois.

#### Quand choisir le CeleryExecutor ?

Pour de nombreuses tâches courtes avec une charge régulière : des workers persistants démarrent les tâches rapidement. Il faut exploiter un broker et dimensionner les workers soi-même (ou avec KEDA).

#### Quand choisir le KubernetesExecutor ?

Quand les tâches ont besoin de ressources ou d'images différentes, que l'isolation compte et que la charge est irrégulière : chaque tâche tourne dans son propre pod et les ressources sont libérées ensuite. Le démarrage du pod ajoute quelques secondes de latence par tâche.

#### Que fait le scheduler ?

Il lit les DAG sérialisés, crée les DAG runs à échéance, vérifie quelles task instances ont leurs dépendances satisfaites, respecte les limites de concurrence et les pools, et envoie les tâches à l'executor. Plusieurs schedulers peuvent tourner en même temps pour la haute disponibilité.

#### Que fait le DAG processor ?

Il analyse les fichiers de DAG et stocke les DAG sérialisés en base. Dans Airflow 3, c'est un composant séparé : le code des utilisateurs ne s'exécute jamais dans le scheduler.

#### Quels réglages de concurrence existent ?

`parallelism` (maximum de tâches en cours par scheduler), `max_active_tasks_per_dag`, `max_active_runs_per_dag`, les slots des pools, `max_active_tis_per_dag` par tâche, et les réglages propres à l'executor comme la concurrence des workers Celery.

#### Qu'est-ce qu'un pool ?

Une limite nommée sur les slots de tâches concurrentes, utilisée pour protéger une ressource partagée : par exemple un pool de 4 slots pour les tâches qui interrogent une base de production. Les tâches sont affectées à un pool et peuvent consommer plusieurs slots.

#### Qu'est-ce que le priority weight ?

Un nombre qui détermine quelles tâches en file passent en premier quand les slots manquent. La règle de poids (`downstream`, `upstream`, `absolute`) contrôle la façon dont il se cumule dans le graphe.

#### Que sont les files dans le CeleryExecutor ?

Des files nommées auxquelles les workers s'abonnent. Affecter des tâches à une file (`queue="gpu"`) les envoie vers des workers disposant des ressources adaptées.

#### Comment les workers obtiennent-ils leurs identifiants dans Airflow 3 ?

Via la Task Execution API : les tâches demandent connexions, variables et XCom à l'API server au lieu de lire la base de métadonnées, ce qui améliore la sécurité et permet des workers distants.

#### Quel est le rôle du broker de messages avec Celery ?

Redis ou RabbitMQ contient la file des tâches envoyées par le scheduler ; les workers Celery la consomment. Un backend de résultats (généralement la base de données) stocke l'état des tâches.

#### Qu'est-ce que le `pod_template_file` ?

Une spécification de pod Kubernetes utilisée par le KubernetesExecutor (et le KubernetesPodOperator) comme base des pods de tâches : image, ressources, volumes, sélecteurs de nœuds, service account. Les tâches peuvent en surcharger une partie avec `executor_config`.

#### Peut-on utiliser plusieurs executors à la fois ?

Oui, depuis Airflow 2.10 : on configure une liste d'executors et on affecte chaque tâche à l'un d'eux avec l'argument `executor`, par exemple la plupart des tâches sur Celery et les tâches lourdes et isolées sur Kubernetes.

#### Qu'est-ce que l'Edge executor ?

Un executor (du provider Edge3) qui exécute les tâches sur des workers distants connectés à l'API d'Airflow en HTTP, par exemple dans un autre réseau ou centre de données, sans accès direct à la base.

#### Comment rendre le scheduler hautement disponible ?

En exécutant deux schedulers ou plus sur la même base PostgreSQL ou MySQL ; ils se coordonnent par verrous au niveau ligne. On exécute plusieurs API servers derrière un répartiteur de charge et plusieurs triggerers.

### Configuration, sécurité et secrets

#### Comment configure-t-on Airflow ?

Avec `airflow.cfg`, surchargé par des variables d'environnement nommées `AIRFLOW__SECTION__CLE` (par exemple `AIRFLOW__CORE__PARALLELISM`). Les variables d'environnement sont l'approche habituelle en conteneur.

#### Qu'est-ce qu'un secrets backend ?

Une intégration qui lit les connexions et variables dans un gestionnaire de secrets externe : AWS Secrets Manager ou SSM Parameter Store, HashiCorp Vault, Google Secret Manager, Azure Key Vault. Les secrets n'ont plus à être stockés dans la base de métadonnées.

#### Comment Airflow évite-t-il d'afficher des secrets dans les journaux et l'interface ?

Il masque les mots de passe des connexions, les variables dont le nom contient des mots comme `password`, `secret` ou `token`, et les valeurs enregistrées avec `mask_secret()`. Le masquage n'est pas infaillible : n'affichez pas de secrets.

#### Qu'est-ce que la clé Fernet ?

La clé utilisée pour chiffrer les mots de passe des connexions et les valeurs des variables dans la base de métadonnées. Elle doit être définie, gardée secrète et identique sur tous les composants ; la changer impose un rechiffrement.

#### Comment contrôle-t-on l'accès à l'interface ?

Avec un auth manager. Airflow 3 fournit un auth manager simple pour le développement ; l'auth manager FAB offre un contrôle d'accès par rôles (Admin, Op, User, Viewer et rôles personnalisés), et les services managés s'intègrent à l'IAM du cloud.

#### Comment le code des DAG doit-il accéder aux ressources cloud ?

Avec l'identité du worker (IAM roles for service accounts sur Kubernetes, rôle d'exécution MWAA, workload identity) chaque fois que possible, plutôt qu'avec des clés de longue durée stockées dans des connexions.

#### Comment définir des connexions en variables d'environnement ?

Avec `AIRFLOW_CONN_<CONN_ID>` contenant une URI ou un JSON, par exemple `AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'`. Elles n'apparaissent pas dans l'interface et ont priorité sur une connexion de même identifiant en base (un secrets backend configuré est toutefois consulté en premier).

#### Comment restreindre qui peut déclencher un DAG ?

Avec le contrôle d'accès par rôles : on donne aux rôles des droits sur des DAG précis (par identifiant ou via `access_control` dans le DAG), pour qu'une équipe ne puisse déclencher et effacer que ses propres DAG.

#### Pourquoi est-il risqué de laisser beaucoup de personnes modifier le code des DAG ?

Le code des DAG s'exécute avec les droits des workers et peut lire les connexions : quiconque peut déployer des DAG a de fait accès à toutes les connexions. La revue de code et les contrôles de CI sur le dépôt de DAG font partie de la sécurité.

### Tests et qualité du code

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

#### Comment tester unitairement la logique des tâches ?

En gardant la logique métier dans des fonctions ou modules Python ordinaires, hors du fichier de DAG, en les testant avec pytest sans Airflow, et en faisant des tâches de simples enveloppes. Pour les opérateurs, on teste `execute()` avec des hooks simulés (mocks).

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

#### Comment tester des opérateurs personnalisés qui utilisent des systèmes externes ?

En simulant le hook dans les tests unitaires pour vérifier la logique et les paramètres de l'opérateur, et en lançant des tests d'intégration contre des conteneurs locaux (Postgres, LocalStack pour AWS, MinIO pour S3) en CI.

#### Comment vérifier le rendu des champs templatés ?

En les rendant pour un contexte donné dans un test (`ti.render_templates()`), ou avec `airflow tasks render dag_id task_id date`, puis en contrôlant le SQL ou la commande obtenus.

#### Que doit exécuter un pipeline de CI pour un dépôt Airflow ?

Le linting (Ruff avec les règles `AIR`), les tests unitaires de la logique métier, les tests d'intégrité des DAG (erreurs d'import du `DagBag`, conventions, cycles), des contrôles de durée d'analyse, la construction de l'image et le déploiement en staging, la production étant déployée après le merge ou une approbation.

#### Comment tester qu'un DAG a la bonne structure ?

En le chargeant depuis un `DagBag` et en vérifiant les identifiants de tâches, les dépendances (`task.downstream_task_ids`), les plannings et les réglages, pour détecter les modifications accidentelles du graphe.

### Déploiement et exploitation

#### Comment déployer les DAG ?

La plupart des équipes construisent une image Docker avec Airflow, les providers, les dépendances et le code des DAG, et la déploient en CI/CD sur Kubernetes (chart Helm) ou sur un service managé. Alternatives : synchroniser les DAG depuis Git avec git-sync ou vers un bucket S3 (MWAA). Les DAG bundles d'Airflow 3 peuvent lire les DAG directement depuis Git avec versionnage.

#### Qu'est-ce qu'un DAG bundle ?

Un concept d'Airflow 3 désignant un ensemble de fichiers de DAG issus d'une source comme un dossier local ou un dépôt Git, qui permet à Airflow de suivre les versions du code et d'exécuter chaque DAG run avec la version avec laquelle il a démarré.

#### Comment mettre à jour Airflow en sécurité ?

Lire les notes de version, mettre à jour d'abord un environnement de test, utiliser les fichiers de contraintes pour figer des dépendances compatibles, lancer `airflow db migrate`, vérifier les DAG pour les dépréciations (règles `AIR` de Ruff pour Airflow 3) et sauvegarder la base de métadonnées avant de migrer la production.

#### Que sont les fichiers de contraintes ?

Des listes de dépendances figées publiées pour chaque version d'Airflow et de Python, utilisées avec `pip install "apache-airflow==X" --constraint <url>` pour obtenir un ensemble de paquets dont on sait qu'il fonctionne.

#### Comment garder la base de métadonnées en bonne santé ?

Utiliser un PostgreSQL managé avec sauvegardes, surveiller sa taille et lancer régulièrement `airflow db clean` pour purger les anciennes task instances, métadonnées de journaux et XCom. Une base énorme ralentit le scheduler et l'interface.

#### Où vont les journaux des tâches ?

Par défaut dans des fichiers locaux sur les workers, affichés dans l'interface. En production, configurez la journalisation distante vers S3, GCS, Azure Blob, Elasticsearch ou CloudWatch pour que les journaux survivent aux redémarrages de pods.

#### Comment superviser Airflow ?

Avec les métriques StatsD ou OpenTelemetry (heartbeat du scheduler, durée d'analyse des DAG, tâches en file et en cours, durées des tâches, usage des pools) dans Prometheus/Grafana ou Datadog, des endpoints de santé, et des alertes sur les échecs et les exécutions trop longues.

#### Comment être alerté des échecs de tâches ?

Avec des callbacks (`on_failure_callback`, `on_retry_callback`, `on_success_callback`) qui envoient vers Slack, l'e-mail ou PagerDuty, les classes notifier des providers ou la configuration e-mail. Alertez au niveau du DAG pour des messages actionnables et sans doublons.

#### Qu'est-ce qui a remplacé les SLA dans Airflow 3 ?

Les SLA (`sla` et `sla_miss_callback`) ont été supprimés car peu fiables. Airflow 3.1 a introduit les deadline alerts, qui déclenchent un callback quand un DAG run n'est pas terminé avant une échéance relative à une heure de référence. Avant cela, les équipes utilisaient `execution_timeout`, `dagrun_timeout` et une supervision externe.

#### Quelles sont les causes fréquentes de tâches bloquées en `queued` ?

Pas de slot libre (limites de parallelism, de pool ou de concurrence du DAG), workers arrêtés ou ne consommant pas la file, executor incapable de démarrer des pods (quotas, erreurs de téléchargement d'image) ou problème de scheduler. Vérifiez les pools, les journaux des workers et les événements de l'executor.

#### Que sont les tâches zombies ?

Des task instances marquées en cours dont le processus est mort sans le signaler (plantage du worker, OOM kill, éviction du pod). Le scheduler détecte l'absence de heartbeat et les fait échouer ou les relance.

#### Comment faire monter Airflow en charge ?

Avec plusieurs schedulers, en dimensionnant les workers (autoscaling des workers Celery avec KEDA, ou executor Kubernetes), en utilisant des opérateurs différables pour libérer des slots, en réduisant la durée d'analyse des DAG, en réglant `parallelism` et les pools, et en gardant le calcul lourd hors d'Airflow.

#### Pourquoi la durée d'analyse des DAG est-elle importante ?

Une analyse lente retarde la planification de tous les DAG et consomme du CPU. On la mesure avec `airflow dags report` ; on la corrige en supprimant le travail de niveau supérieur, en évitant les imports lourds au niveau du module et en découpant les fichiers de DAG générés géants.

#### Qu'est-ce que le chart Helm officiel ?

Le chart Helm d'Apache Airflow, qui déploie tous les composants sur Kubernetes avec des options pour les executors, git-sync, PgBouncer, l'autoscaling KEDA, la journalisation et les secrets. C'est le déploiement auto-hébergé standard sur Kubernetes.

#### Pourquoi utiliser PgBouncer avec Airflow ?

Chaque tâche et composant ouvre des connexions à la base ; de nombreuses tâches concurrentes peuvent épuiser la limite de connexions de PostgreSQL. PgBouncer les mutualise. Dans Airflow 3, la Task Execution API réduit les connexions directes depuis les workers.

#### Comment déployer sur Amazon MWAA ?

En téléversant les DAG dans le bucket S3 de l'environnement (généralement depuis la CI avec `aws s3 sync`) et en gérant `requirements.txt`, les plugins et un script de démarrage dans S3 ; la version d'Airflow et la taille de l'environnement se règlent dans sa configuration. Le rôle d'exécution donne l'accès à AWS.

#### Que doit contenir un runbook pour un DAG en échec ?

Ce que fait le DAG et qui en est responsable, les dépendances amont, comment consulter les journaux et les entrées, quelles tâches peuvent être effacées et relancées sans risque, comment faire un backfill, qui prévenir, et les pannes connues avec leurs corrections.

#### Comment revenir en arrière après un mauvais déploiement de DAG ?

En redéployant l'image ou le commit Git précédent via la CI. Avec le versionnage des DAG d'Airflow 3, les exécutions existantes gardent leur version. On efface ensuite les exécutions en échec si nécessaire.

### Bonnes pratiques

#### Airflow doit-il faire lui-même le traitement des données ?

Non. Airflow doit orchestrer : déclencher Spark, des moteurs SQL, dbt, Databricks ou des conteneurs qui font le traitement, et passer des références. Un traitement pandas lourd sur les workers Airflow concurrence les autres tâches et passe mal à l'échelle.

#### Quelle est une bonne granularité de tâches ?

Chaque tâche doit être une unité porteuse de sens et relançable (extraire une source, charger une table, exécuter un groupe de modèles). Trop grosse, elle oblige à relancer beaucoup de travail ; trop fine, elle ajoute de la surcharge de planification et rend le graphe illisible.

#### Comment rendre les relances sûres ?

En rendant les tâches idempotentes, en fixant `retries` et `retry_delay` (avec `retry_exponential_backoff`) pour les erreurs transitoires, et en échouant vite (sans relance) pour les erreurs qu'une relance ne corrige pas, comme des identifiants invalides ou un échec de qualité des données.

#### Où doit vivre la configuration ?

Dans le code (versionné) pour la structure, dans des variables d'environnement ou des Variables pour les valeurs propres à chaque environnement, et dans un secrets backend pour les identifiants. Évitez de lire de nombreuses Variables à l'analyse des DAG.

#### Comment nommer les DAG et les tâches ?

De façon cohérente et descriptive : `domaine__objectif` pour les DAG (`sales__daily_load`), des verbes pour les tâches (`extract_orders`, `load_orders`), avec des owners et des tags pour les équipes et les domaines de données.

#### Comment gérer le code partagé entre DAG ?

En le plaçant dans un paquet Python (dans le dossier `include/` ou `plugins/` du dépôt, ou installé dans l'image) avec ses propres tests, plutôt qu'en copiant du code d'un fichier de DAG à l'autre.

#### À quoi servent les plugins dans Airflow ?

À étendre Airflow avec des vues d'interface, des liens de menu, des macros, des listeners, des timetables et, dans Airflow 3, des applications FastAPI et des vues React. Les opérateurs et hooks personnalisés n'ont pas besoin d'être des plugins ; de simples modules Python suffisent.

#### Que sont les listeners ?

Des points d'accroche sur les événements d'Airflow (début ou fin d'un DAG run, changements d'état des task instances) implémentés avec pluggy, utilisés pour le lignage (OpenLineage), l'audit ou des notifications personnalisées.

#### Qu'est-ce qu'OpenLineage dans Airflow ?

Un standard de métadonnées de lignage. Le provider OpenLineage émet des événements décrivant les entrées et sorties des tâches vers un backend comme Marquez ou un catalogue de données, pour voir quels jobs lisent et écrivent quels jeux de données.

#### Comment faire des contrôles de qualité des données dans Airflow ?

Avec les opérateurs de contrôle SQL (`SQLColumnCheckOperator`, `SQLTableCheckOperator`, `SQLCheckOperator`), les opérateurs Great Expectations ou Soda, ou les tests dbt, placés après les chargements pour arrêter les tâches en aval quand les données sont fausses.

#### Pourquoi les DAG ne doivent-ils pas s'appuyer sur des fichiers locaux entre tâches ?

Les tâches peuvent tourner sur des workers ou des pods différents : un fichier écrit par une tâche peut ne pas exister pour la suivante. Utilisez un stockage objet, un volume partagé ou une base de données.

#### En combien de DAG découper un pipeline ?

Un DAG par planning et par périmètre de responsabilité indépendants. Découpez quand les parties ont des plannings, des responsables ou des domaines de panne différents, et reliez-les par des assets ; gardez dans un seul DAG les étapes fortement couplées.

#### Comment garder un DAG lisible ?

Des tâches petites et bien nommées, des task groups pour les blocs logiques, aucune logique métier dans le fichier du DAG, une documentation avec `doc_md`, un usage cohérent de TaskFlow ou des opérateurs, et peu de génération dynamique.

#### Pourquoi figer les versions des providers et des dépendances ?

Des mises à jour non figées peuvent changer le comportement des opérateurs ou casser des imports silencieusement. Figez les versions avec le fichier de contraintes et mettez à jour délibérément, avec des tests.

### Mises en situation

#### Un DAG quotidien doit charger les fichiers de la veille depuis S3 dans Snowflake, puis lancer dbt. Concevez-le.

Un DAG quotidien avec `catchup=False` (ou true si l'historique compte), un `S3KeySensor` différable sur le préfixe attendu pour l'intervalle de données, un `CopyFromExternalStageToSnowflakeOperator` ou une tâche SQL lançant `COPY INTO`, puis dbt via Cosmos ou un opérateur dbt Cloud, des contrôles de qualité et des callbacks d'échec vers Slack. Tous les chemins et filtres viennent de l'intervalle de données.

#### Des centaines de DAG sont lents à planifier. Qu'examinez-vous ?

La durée d'analyse des DAG (`airflow dags report`), le code et les imports de niveau supérieur, le nombre de fichiers de DAG, le CPU du scheduler et les performances de la base, le nombre de task instances en base (lancer `db clean`), et si le scheduler et le DAG processor ont assez de ressources ou de réplicas.

#### Un sensor attend un fichier qui parfois n'arrive jamais. Comment le gérez-vous ?

Je rends le sensor différable ou j'utilise le mode `reschedule`, je lui donne un timeout réaliste, je décide si l'absence doit échouer (prévenir quelqu'un) ou être ignorée (`soft_fail`), et je préviens le responsable de la source. Je documente l'heure d'arrivée attendue.

#### Une tâche échoue aléatoirement à cause de la limite de débit d'une API. Que faites-vous ?

J'ajoute des relances avec backoff exponentiel, je place les appels d'API dans un pool qui limite la concurrence, je respecte `Retry-After` dans le hook et je réduis les appels (regroupement, extraction incrémentale).

#### Il faut retraiter six mois de données après une correction. Comment ?

Je m'assure que les tâches sont idempotentes et utilisent l'intervalle de données, puis je crée un backfill pour la plage de dates avec une concurrence limitée (`max_active_runs`) pour ne pas affamer la production, ou j'efface les DAG runs concernés. Je surveille et valide les sorties ensuite.

#### Deux DAG écrivent dans la même table et entrent parfois en conflit. Comment corriger ?

En les sérialisant : un pool à un seul slot pour les écritures dans cette table, ou leur fusion en un seul DAG à l'ordre explicite, ou une dépendance de l'un sur l'autre via un asset. Mieux encore, donner à chaque table un seul processus propriétaire.

#### Comment migrer d'Airflow 2 à Airflow 3 ?

Passer d'abord à la dernière 2.x et corriger les avertissements de dépréciation, lancer les règles `AIR3` de Ruff pour trouver le code à modifier (imports vers `airflow.sdk`, `schedule_interval` vers `schedule`, `execution_date` vers `logical_date`, SubDAG et SLA supprimés, pas d'accès direct à la base depuis les tâches), tester en staging, migrer la base, et adapter le déploiement pour l'API server et le DAG processor.

#### Comment orchestrer un pipeline combinant AWS Glue, Databricks et un projet dbt ?

Un DAG (ou des DAG reliés par des assets) utilisant `GlueJobOperator` du provider Amazon, `DatabricksRunNowOperator` du provider Databricks et Cosmos ou l'opérateur dbt Cloud, tous en mode différable, en passant des noms de tables ou des chemins, avec des contrôles de qualité entre les étapes et une configuration d'alerte unique.

#### Votre personne d'astreinte est réveillée chaque nuit par la même tâche instable. Que changez-vous ?

Je cherche la cause racine dans les journaux (timeouts, limites de ressources, retard en amont), j'ajoute des relances avec backoff seulement pour les erreurs transitoires, j'ajoute un sensor ou une dépendance d'asset si la tâche démarre avant que son entrée soit prête, j'augmente les ressources ou la déplace dans un pool dédié, et je fais en sorte que les alertes ne partent qu'une fois les relances épuisées.

#### Un DAG fonctionne en local mais les tâches échouent en production avec « module not found ». Pourquoi ?

L'image ou les workers de production n'ont pas la dépendance, ou le module n'est pas dans le chemin (par exemple du code hors du dossier des DAG ou des plugins). Ajoutez-le aux dépendances de l'image ou à un paquet, et construisez le local et la production à partir de la même image.

#### Des tâches sont souvent tuées sans erreur dans les journaux. Que soupçonnez-vous ?

Des arrêts pour manque de mémoire (OOM) du worker ou du pod, des évictions ou des timeouts. Vérifiez les événements des pods et les métriques des workers, augmentez les limites de mémoire et sortez le traitement lourd d'Airflow.

#### Votre backfill a créé des doublons dans la table cible. Qu'est-ce qui n'allait pas ?

Les tâches n'étaient pas idempotentes : elles ajoutaient des données ou utilisaient « maintenant » au lieu de l'intervalle de données. Réécrivez le chargement pour écraser la partition de l'intervalle ou faire un `MERGE` par clé, supprimez les doublons et relancez.

#### Un utilisateur métier veut recevoir un rapport par e-mail seulement si les ventes de la veille sont complètes. Comment ?

Je planifie le DAG du rapport sur l'asset des ventes (ou un sensor sur le chargement), j'ajoute un contrôle de qualité (nombre de lignes et complétude par rapport aux sources attendues), je court-circuite l'e-mail si les contrôles échouent, et j'alerte alors l'équipe data.

#### Comment déclencher un DAG Airflow à l'arrivée d'un fichier dans S3, sans scrutation ?

Avec un asset watcher sur une file SQS qui reçoit les notifications d'événements S3 (Airflow 3), ou avec un événement S3 qui lance une fonction Lambda appelant l'API REST d'Airflow pour déclencher le DAG avec le chemin du fichier en configuration.

#### Le CPU de votre scheduler est à 100 %. Quelles sont les corrections habituelles ?

Réduire la charge d'analyse des DAG (fichiers moins nombreux et plus légers, `min_file_process_interval` plus long, DAG processor séparé), abandonner les sensors en mode poke, nettoyer la base, ajouter des réplicas du scheduler et examiner les DAG comportant un nombre énorme de tâches mappées.

#### Comment expliquer Airflow à un interlocuteur non technique ?

C'est le planificateur et le régulateur de trafic des traitements de données de l'entreprise : il lance chaque étape au bon moment et dans le bon ordre, réessaie quand quelque chose coince momentanément, et prévient l'équipe quand une intervention humaine est nécessaire.
