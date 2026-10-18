## CI/CD for Data Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![CI/CD for data study guide: about 200 questions](../../images/cicd_data_study_guide_title_img.png)

About 200 interview-style questions on CI/CD and automation for data platforms: Git workflows, testing strategies for pipelines and data, code quality, environments, infrastructure as code, deployment patterns, GitHub Actions in depth, CI/CD for dbt, Databricks, Airflow and warehouses, security of the delivery pipeline, and operations. Examples use GitHub Actions, with notes on GitLab CI and Azure DevOps.

The guide follows a learning path in six stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections.

<!-- QA -->
<!-- stage: Foundations -->

### Fundamentals

<!-- unit: CI/CD and DataOps -->

<!-- goals -->

- Explain CI/CD and DataOps and why data teams need them.
- Describe what makes CI/CD for data different from applications.

<!-- concept -->

Data pipelines are software, and they break in the same ways: a typo in a join, an untested change, a manual deploy on a Friday. CI/CD turns every change into a routine: it is merged often, checked automatically and delivered the same way each time. DataOps extends that habit to the data itself, with tests and monitoring on what the pipelines produce.

The extra difficulty is state. An application can be replaced; a table with five years of history has to be migrated, backfilled and kept consistent for consumers.

<!-- example -->

| Step | Manual way | CI/CD way |
|---|---|---|
| Change a dbt model | Edit in prod, hope | PR, CI builds and tests it |
| Deploy | Copy files on the server | Pipeline deploys a versioned artifact |
| Find what broke | Ask around | Git history and deployment log |

#### What is CI/CD?

Continuous integration (CI) means merging code changes frequently into a shared branch, with automated builds and tests on every change. Continuous delivery (CD) keeps the code always deployable and automates releases to environments; continuous deployment goes further and deploys every passing change to production automatically.

#### Why does CI/CD matter for data teams?

Data pipelines are software: without automation, changes are deployed by hand, break production tables, and are hard to roll back. CI/CD catches errors before they reach consumers, makes deployments repeatable and auditable, and lets teams change pipelines quickly and safely.

#### What is DataOps?

Applying DevOps and agile practices to data: version control, automated testing (code and data), CI/CD, environment management, monitoring and observability, and collaboration between data engineers, analysts and operations, with the goal of reliable data delivered quickly.

#### How is CI/CD for data different from CI/CD for applications?

Data pipelines have state (tables, history, schemas) that must be migrated, not just replaced; tests need representative data; correctness depends on the data as much as the code; deployments can trigger expensive recomputations; and rollback of data is harder than rollback of code.

#### How do you explain CI/CD for data to a non-technical stakeholder?

It's an automatic quality check and delivery line for our data pipelines: every change is tested before it can affect the reports, and approved changes reach production the same safe way every time, so numbers stay trustworthy while we improve them quickly.

<!-- challenge -->

A team says "our SQL is simple, we don't need CI". Give two concrete failures CI would catch in a SQL-only project.

<!-- solution -->

A model referencing a renamed column (caught by compiling and building in a CI schema), and a join that duplicates rows (caught by a uniqueness test on the output key). Both would otherwise reach dashboards.

<!-- takeaways -->

- CI/CD makes changes small, checked and repeatable.
- DataOps adds tests and monitoring of the data itself.
- Data has state: changes need migrations and backfills.

<!-- unit: Pipelines and stages -->

<!-- goals -->

- Describe the stages of a deployment pipeline and what each automates.
- Distinguish continuous delivery, continuous deployment and releases.

<!-- concept -->

A deployment pipeline is an assembly line from commit to production. Build produces artifacts, test verifies them, and deploy installs the same artifacts in each environment in turn. Each stage is a gate: a failure stops the line before damage spreads.

How far automation goes is a choice. Continuous delivery keeps every change ready to deploy; continuous deployment ships it automatically. Releases, when users actually see a change, can be decoupled from deployments with flags.

<!-- example -->

```text
commit ─► lint + unit tests ─► build wheel/image/manifest ─► deploy staging
       ─► integration + data tests ─► [approval] ─► deploy prod ─► smoke test
```

#### What should be automated in a data CI/CD pipeline?

Linting and formatting, unit tests, building artifacts (wheels, images, dbt manifests), static validation (SQL compilation, bundle or DAG validation), integration and data tests against test data, security scans, infrastructure changes, deployments to each environment, smoke tests after deployment, and notifications.

#### What is a deployment pipeline?

The automated sequence that takes a commit to production: build, test, package, deploy to lower environments, run checks, approve, deploy to production, verify. It's the path every change follows.

#### What is the difference between a build, a test and a deployment stage?

The build stage produces artifacts (packages, images, compiled models); the test stage verifies them (unit, integration, data tests); the deployment stage installs them into an environment and runs post-deployment checks. Separating them makes failures easy to locate.

#### What is the difference between continuous delivery and continuous deployment?

With continuous delivery, every change is deployable and production deployment is one click or approval away. With continuous deployment, every change that passes the pipeline goes to production automatically, without a manual step.

#### What is a "release" versus a "deployment"?

A deployment installs a version into an environment; a release makes new functionality available to users. With feature flags or blue-green switches, you can deploy without releasing and release without redeploying.

<!-- challenge -->

A new revenue model must ship this week but only go live for finance at month end. How do you separate deployment from release?

<!-- solution -->

Deploy the model now behind a flag or to a new table that dashboards don't use yet, validate it in production, then switch the finance dashboard to it at month end (flip the flag or the view).

<!-- takeaways -->

- Pipelines build, test and deploy the same artifacts.
- Delivery keeps changes deployable; deployment ships them automatically.
- Releases can be decoupled from deployments.

<!-- unit: Principles of delivery -->

<!-- goals -->

- Apply everything as code, small changes and shift-left quality.
- Measure delivery with DORA metrics and ownership.

<!-- concept -->

A few principles explain why CI/CD works. Everything that defines the platform lives in code, so it can be reviewed and rebuilt. Changes are small, so each is easy to understand and undo. Problems are caught as early as possible, where they're cheapest. Pipelines are deterministic, so reruns give the same result.

Ownership and measurement keep it honest: the team that builds a pipeline runs it, and DORA metrics show whether delivery is getting faster and safer.

<!-- example -->

| DORA metric | Healthy data team |
|---|---|
| Deployment frequency | Several times a week |
| Lead time for changes | Hours to a day |
| Change failure rate | Below 15% |
| Time to restore | Under an hour |

#### What is "everything as code"?

Defining pipelines, transformations, infrastructure, permissions, schedules, data quality rules and even documentation in version-controlled files, so every change is reviewed, tested, reproducible and traceable.

#### What are the benefits of small, frequent deployments?

Each change is easier to review, test and understand, failures are easier to diagnose and roll back, and feedback from production comes sooner. Large, infrequent releases bundle many risks together.

#### What is "shift left" in data quality?

Catching problems as early as possible: in the IDE (linters), at commit (pre-commit hooks), in pull requests (CI tests, contract checks), rather than in production dashboards where they're expensive and visible.

#### Why should pipelines be deterministic?

Given the same code, configuration and inputs, a deterministic pipeline produces the same outputs, which makes testing, debugging, backfills and audits possible. Avoid hidden dependencies on current time, random seeds or unpinned versions.

#### What does "you build it, you run it" mean for data teams?

The team that builds a pipeline also operates it: receives its alerts, fixes its incidents and improves its reliability, which creates strong incentives for good tests, monitoring and automation.

#### What are DORA metrics?

Four measures of delivery performance: deployment frequency, lead time for changes, change failure rate and time to restore service. They apply to data teams too and help measure whether CI/CD improves delivery.

<!-- challenge -->

A team deploys once a month in a big batch of 40 changes, and each release has incidents. Which two changes help most?

<!-- solution -->

Deploy small changes continuously (trunk-based, automated pipeline) so each release is small and diagnosable, and add automated tests and checks earlier (shift left) so fewer defects reach production.

<!-- takeaways -->

- Everything as code makes platforms reviewable and rebuildable.
- Small, frequent changes reduce risk.
- DORA metrics track speed and stability.

### Version control and Git workflows

<!-- unit: What goes in Git -->

<!-- goals -->

- Decide what belongs in a data repository and what never does.
- Version notebooks and large files properly.

<!-- concept -->

Git is the source of truth for everything that defines a pipeline: code, SQL, configuration, tests, infrastructure and documentation. If it isn't in Git, it can't be reviewed, reproduced or rolled back.

Some things must stay out: secrets, real personal data, large datasets and generated files. Notebooks and binaries need special handling, because their default formats produce unreadable diffs or bloat the repository.

<!-- example -->

```gitignore
.env
*.parquet
data/
target/            # dbt build output
.venv/
**/.ipynb_checkpoints/
```

#### Why must data code be in Git?

Version control gives history (who changed what and why), collaboration through branches and pull requests, the ability to revert, a single source of truth for deployments, and the trigger for CI/CD.

#### What belongs in a data repository?

Pipeline and transformation code (Python, SQL, dbt models), tests and fixtures, configuration per environment (without secrets), infrastructure as code, orchestration definitions (DAGs, bundles, job specs), CI/CD workflows, documentation and data contracts.

#### What should never be committed?

Secrets (passwords, keys, tokens), real personal or sensitive data, large data files, local environment files and build outputs. Use `.gitignore`, secret scanning and pre-commit hooks to prevent accidents.

#### How should notebooks be handled in Git?

Store them as source files (Databricks `.py` format, Jupytext) rather than JSON with outputs, strip outputs before commit, keep logic in importable modules and notebooks thin, so diffs are reviewable.

#### What is a `.gitattributes` or LFS needed for in data repos?

Git LFS stores large binary files (small reference datasets, test fixtures, images) outside the normal Git history; large production data shouldn't be in Git at all.

<!-- challenge -->

A data scientist commits notebooks with output cells containing customer records. What do you put in place?

<!-- solution -->

Strip outputs automatically (nbstripout or a pre-commit hook), store notebooks as source files (Jupytext or Databricks `.py`), remove the leaked data from history, and treat it as a data incident.

<!-- takeaways -->

- Code, SQL, config, tests and infrastructure belong in Git.
- Secrets, personal data and large files never do.
- Store notebooks as source; use LFS for necessary binaries.

<!-- unit: Branching workflows -->

<!-- goals -->

- Compare trunk-based development and GitFlow.
- Keep branches short and handle hotfixes and repo layout.

<!-- concept -->

Branching strategy decides how long changes live apart. Long-lived branches drift from main, and merging them becomes a project of its own. Trunk-based development keeps branches to a day or two and merges small pieces often, which is why it pairs naturally with CI/CD.

Short branches need techniques for unfinished work, such as flags and disabled code paths, and a clear path for urgent fixes. Repository layout is a related choice: one repo for everything or one per component.

<!-- example -->

```text
main ──●──●──●──●──●──●──   (always deployable)
        \  /    \ /
  feat/orders-dedupe   fix/null-country   (hours to 2 days each)
```

#### What is trunk-based development?

A workflow where developers integrate small changes into the main branch frequently (at least daily), using short-lived feature branches and feature flags, with the main branch always releasable. It suits CI/CD well.

#### What is GitFlow, and why is it less popular now?

A branching model with long-lived `develop` and `main` branches plus feature, release and hotfix branches. It adds ceremony and merge pain; most teams practicing CI/CD prefer trunk-based development or a simple feature-branch flow.

#### How do you keep feature branches short-lived?

Break work into small, independently mergeable changes, merge behind feature flags or disabled schedules, rebase often on main, and aim to merge within a day or two.

#### How do you handle hotfixes in trunk-based development?

Fix on a short-lived branch from main, merge through the normal (possibly expedited) pipeline and deploy; if a release branch is in production, cherry-pick the fix there too. Avoid patching production by hand.

#### What is a monorepo versus a polyrepo for data?

A monorepo keeps all pipelines, models and infrastructure in one repository (easy cross-cutting changes, shared tooling, needs path-based CI); a polyrepo splits them by domain or component (clear ownership and access, harder coordination). Both work with good CI.

<!-- challenge -->

A developer has a three-week branch rewriting the customer pipeline, and merging it now conflicts everywhere. How should the work have been organized?

<!-- solution -->

In small, mergeable steps: add the new pipeline alongside the old one behind a flag or writing to a new table, merge each part to main as it's ready, then switch consumers and remove the old code.

<!-- takeaways -->

- Trunk-based development merges small changes daily.
- Flags and parallel paths keep unfinished work mergeable.
- Hotfixes go through main and the normal pipeline.

<!-- unit: Reviews and protections -->

<!-- goals -->

- Write and review pull requests for data code.
- Enforce reviews with branch protection and CODEOWNERS.

<!-- concept -->

Pull requests are where a second person sees a change before it reaches production. For data code, good reviews look past style: grain and fan-out in joins, null and duplicate handling, idempotency, performance and the impact on downstream consumers.

Repository settings make reviews non-optional: protected branches need passing checks and approvals, and code owners are added automatically for the paths they know.

<!-- example -->

```text
# .github/CODEOWNERS
/models/finance/        @acme/finance-data
/infra/                 @acme/platform
/.github/workflows/     @acme/platform
```

#### What is a pull request (merge request), and what should a good one include?

A request to merge a branch, with a description of what and why, linked ticket, testing done, impact on data (schemas, backfills, consumers), screenshots or query results if relevant, and passing checks. It's the place for review and automated validation.

#### What should reviewers look for in data code reviews?

Correctness of logic and joins (grain, fan-out), handling of nulls and duplicates, idempotency, performance (partition filters, full scans), tests covering the change, schema and contract changes, backfill needs, security (no secrets, proper permissions) and readability.

#### What are branch protection rules?

Repository settings that prevent direct pushes to important branches and require pull requests, passing status checks, a number of approvals, code owner reviews, up-to-date branches or signed commits before merging.

#### What is a CODEOWNERS file?

A file mapping paths to responsible teams or people, who are automatically requested as reviewers and can be required to approve changes to their areas, for example `/models/finance/ @org/finance-data`.

<!-- challenge -->

A PR changes a join from `customer_id` to `email` and all tests pass. What would a good reviewer ask?

<!-- solution -->

Whether `email` is unique per customer (if not, the join fans out and duplicates rows), how nulls and case differences are handled, and which downstream models and dashboards change. Ask for a uniqueness test on the output.

<!-- takeaways -->

- Review joins, grain, nulls, idempotency and impact.
- Branch protection makes checks and approvals mandatory.
- CODEOWNERS routes reviews to the right people.

<!-- unit: Versions and history -->

<!-- goals -->

- Apply semantic versioning to code and data contracts.
- Use conventional commits and tags in releases.

<!-- concept -->

Versions communicate what a change means. Semantic versioning says it in three numbers: a major bump breaks something, a minor adds, a patch fixes. That applies to libraries, and also to data contracts: renaming a column is a major change for consumers.

Commit messages and tags make this automatic. Conventional commits encode the type of change, so tools can compute the next version and changelog, and tags mark exactly what was released.

<!-- example -->

```text
fix(orders): exclude test customers from revenue      → 2.3.1
feat(orders): add refund_amount column                → 2.4.0
feat!(orders): rename amount to gross_amount          → 3.0.0
git tag v3.0.0 && git push origin v3.0.0              # triggers the release workflow
```

#### What is semantic versioning, and does it apply to data?

Versioning as MAJOR.MINOR.PATCH, where major versions signal breaking changes. It applies to libraries and also to data products and contracts: a removed column or changed meaning is a major version, a new optional column a minor one.

#### What are conventional commits?

A commit message convention (`feat:`, `fix:`, `chore:`, `docs:`, `feat!:` for breaking changes) that makes history readable and lets tools generate changelogs and version numbers automatically.

#### What are Git tags used for in deployments?

Marking release points (`v1.4.0`) that trigger release workflows, identify exactly what was deployed and allow rollback by redeploying a previous tag.

<!-- challenge -->

A team renames a column in a shared table as a "small fix". Three dashboards break. How would versioning have helped?

<!-- solution -->

Treating the table as a contract, the rename is a major change: publish it as a new version (or new column) alongside the old one, announce a deprecation date, and remove the old name only after consumers migrate.

<!-- takeaways -->

- MAJOR.MINOR.PATCH signals breaking, additive and fixing changes.
- Data contracts deserve versions too.
- Conventional commits and tags automate releases.

<!-- stage: Quality -->

### Testing strategy for data

<!-- unit: The testing pyramid -->

<!-- goals -->

- Describe unit, integration, end-to-end and smoke tests for pipelines.
- Structure code so logic is unit-testable.

<!-- concept -->

Tests trade speed for realism. Unit tests check small pieces of logic in milliseconds; integration tests check components against real dependencies; end-to-end tests run the whole pipeline on small data; smoke tests confirm a deployment works. A healthy suite has many of the first and few of the last.

Unit tests are only cheap if logic is separated from I/O. Functions that take and return DataFrames can be tested without a cluster or a warehouse.

<!-- example -->

```python
def add_net_amount(df):                         # pure: DataFrame in, DataFrame out
    return df.withColumn("net", F.col("gross") - F.coalesce(F.col("discount"), F.lit(0)))

def test_add_net_amount(spark):
    df = spark.createDataFrame([(100, 10), (50, None)], "gross int, discount int")
    assert [r.net for r in add_net_amount(df).collect()] == [90, 50]
```

#### What does the testing pyramid look like for data pipelines?

Many fast unit tests of transformation logic, fewer integration tests of components with real engines (Spark, a test database, dbt against a test schema), a few end-to-end tests running the whole pipeline on sample data, plus data quality tests that run in production on real data.

#### What is a unit test in a data pipeline?

A fast test of a small piece of logic with controlled inputs and expected outputs, such as a PySpark function on a tiny DataFrame, a parsing function, or a dbt macro or model with mocked inputs.

```python
def test_dedupe_keeps_latest(spark):
    df = spark.createDataFrame(
        [(1, "a", "2026-10-01"), (1, "b", "2026-10-02"), (2, "c", "2026-10-01")],
        ["id", "value", "updated_at"])
    result = dedupe_latest(df, key="id", order_col="updated_at")
    assert sorted(result.collect()) == sorted(
        spark.createDataFrame([(1, "b", "2026-10-02"), (2, "c", "2026-10-01")],
                              ["id", "value", "updated_at"]).collect())
```

#### How do you structure code so it's unit-testable?

Separate pure transformation functions (DataFrame in, DataFrame out; rows in, rows out) from I/O (reading sources, writing tables) and configuration; inject dependencies like paths and dates; keep notebooks or entry scripts thin.

#### What is an integration test for data?

A test that runs components together with real (or realistic) dependencies: reading and writing actual tables in a test schema, running SQL on a warehouse sandbox, or calling an API mock, verifying that pieces fit together.

#### What is an end-to-end test for a pipeline?

Running the whole pipeline (ingestion to final tables) on a small, representative synthetic dataset in an isolated environment and asserting on the outputs (row counts, key values, invariants). It catches wiring errors unit tests miss.

#### What is a smoke test after deployment?

A quick check right after deploying that the system works: jobs are registered, a small run succeeds, key tables are readable, dashboards load. It catches configuration and permission errors early.

<!-- challenge -->

A pipeline's only tests run the full job on a staging cluster and take 50 minutes. How do you rebalance the suite?

<!-- solution -->

Extract transformation logic into pure functions and cover them with fast unit tests on local Spark, keep a few integration tests for I/O, and run the full end-to-end job nightly or before releases rather than on every PR.

<!-- takeaways -->

- Many fast unit tests, fewer slow realistic ones.
- Separate pure logic from I/O to test it cheaply.
- Smoke tests confirm each deployment works.

<!-- unit: Code tests versus data tests -->

<!-- goals -->

- Distinguish tests of logic from tests of data.
- Add contract, regression and data quality gates to delivery.

<!-- concept -->

Code tests ask "does the logic do what I meant on inputs I chose?" Data tests ask "is the data that actually arrived what we expect?" Both are needed: perfect code still fails on a source that changed overnight.

Contract tests sit between teams, checking that a producer still delivers the agreed schema. Regression tests compare a new version's output with the old one. Data quality gates stop publishing when expectations fail.

<!-- example -->

```yaml
# dbt data tests on the output of a model
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: status
        tests:
          - accepted_values: {values: [placed, shipped, returned]}
```

#### What are data tests, and how do they differ from code tests?

Code tests check that logic behaves as expected on controlled inputs; data tests check that real data meets expectations (uniqueness, not null, accepted values, referential integrity, freshness, volume). Both are needed: correct code can still produce wrong data from bad inputs.

#### What is a contract test for data?

A test verifying that a producer's output matches the agreed schema and semantics of a data contract (columns, types, nullability, allowed values), run in the producer's CI so breaking changes fail before release.

#### What is regression testing for data pipelines?

Comparing outputs of the new version with the previous version on the same input (row counts, aggregates, row-level diffs), so unintended changes are detected; tools include `datacompy`, dbt audit helper and data-diff approaches.

#### How would you add data quality gates to an existing CI/CD pipeline?

Add data tests to the transformation project (uniqueness, not null, relationships, accepted values), run them in CI on test data and in production after each build, block publishing (write-audit-publish or failing the job) on critical failures, and alert owners.

<!-- challenge -->

A refactor of a revenue model passes all unit tests. How do you check it didn't change results?

<!-- solution -->

Run a regression comparison: build the new version in a CI or staging schema on the same inputs and compare row counts, aggregates and a row-level diff by key against production. Investigate any difference before merging.

<!-- takeaways -->

- Code tests check logic; data tests check real data.
- Contracts protect consumers from producer changes.
- Regression diffs catch unintended result changes.

<!-- unit: Test data and tooling -->

<!-- goals -->

- Manage test data, preferring synthetic fixtures in CI.
- Use pytest fixtures, DataFrame comparisons and golden files.

<!-- concept -->

Tests are only as good as their inputs. Small synthetic datasets designed around edge cases are fast, deterministic and free of personal data, which makes them the default for CI. Production-like samples, masked, belong in staging.

Tooling keeps tests short: fixtures share setup such as a Spark session, comparison helpers give readable diffs, and golden files store expected outputs for larger cases. Speed matters, because slow suites get skipped.

<!-- example -->

```python
import pytest
from pyspark.testing import assertDataFrameEqual

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").getOrCreate()

def test_dedupe(spark):
    actual = dedupe(spark.read.json("tests/fixtures/orders_dupes.json"))
    expected = spark.read.json("tests/golden/orders_deduped.json")
    assertDataFrameEqual(actual, expected)
```

#### What is test data management?

Creating and maintaining datasets for tests: small synthetic fixtures for unit tests, anonymized or synthetic samples for integration tests, and production-like data (masked) for performance tests, versioned with the code where possible.

#### Why prefer synthetic data in CI?

It's safe (no personal data), small (fast tests), deterministic, and can include edge cases deliberately (nulls, duplicates, late records, unicode, extreme values) that might be rare in real samples.

#### What are fixtures in pytest, and how are they useful for data tests?

Reusable setup functions (a SparkSession, a temporary database, sample DataFrames) injected into tests by name, with scopes (function, module, session) so expensive resources like Spark are created once.

```python
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (SparkSession.builder.master("local[2]")
               .config("spark.sql.shuffle.partitions", "2")
               .getOrCreate())
    yield session
    session.stop()
```

#### How do you compare DataFrames in tests?

Use `pyspark.testing.assertDataFrameEqual` (Spark 3.5+) or `chispa` for PySpark, `pandas.testing.assert_frame_equal` for pandas, with options to ignore row order and handle approximate floats.

#### What are "golden files" or snapshot tests?

Stored expected outputs (CSV, JSON, Parquet) that test results are compared against; when outputs change intentionally, the golden files are updated in the same pull request, making changes visible in review.

#### How do you keep test suites fast?

Use small fixtures, share one SparkSession per test session, mark slow tests and run them separately or only on main, parallelize with `pytest-xdist`, cache dependencies in CI, and avoid hitting real cloud services in unit tests.

<!-- challenge -->

Each test creates its own SparkSession and the suite takes 12 minutes for 80 tests. What is the quickest fix?

<!-- solution -->

Share one SparkSession per test session through a session-scoped pytest fixture, and set `spark.sql.shuffle.partitions` low for tiny data. Start-up overhead then happens once.

<!-- takeaways -->

- Synthetic fixtures are safe, small and deterministic.
- Share expensive setup with fixtures.
- Golden files store expected outputs for bigger cases.

<!-- unit: What to test in a pipeline -->

<!-- goals -->

- Cover edge cases, idempotency and schema evolution.
- Test SQL transformations and Airflow DAGs.

<!-- concept -->

Pipelines rarely fail on the happy path. They fail on empty inputs, nulls in keys, duplicates, late records, a new column, or a rerun that appends twice. Tests that deliberately feed those cases catch most production incidents in advance.

Each tool has its own entry points: SQL models are built on seeded inputs, DAGs are loaded and inspected, and idempotency is tested by running a step twice.

<!-- example -->

```python
def test_load_is_idempotent(spark, tmp_path):
    load_day(spark, "tests/fixtures/day.json", tmp_path, day="2026-10-17")
    first = spark.read.parquet(str(tmp_path)).count()
    load_day(spark, "tests/fixtures/day.json", tmp_path, day="2026-10-17")
    assert spark.read.parquet(str(tmp_path)).count() == first
```

#### What edge cases should data pipeline tests cover?

Empty inputs, nulls in keys and values, duplicates, late and out-of-order records, schema changes (extra or missing columns), invalid formats, time zones and daylight saving, very large values, special characters, and reruns of the same input (idempotency).

#### How do you test idempotency?

Run the pipeline step twice on the same input and assert the output is identical (same row count, no duplicates, same aggregates).

#### How do you test schema evolution handling?

Feed fixtures with an added column, a removed column and a changed type, and assert the pipeline behaves as designed (accepts additive changes, fails loudly or quarantines incompatible ones).

#### How do you test SQL transformations?

Compile and parse SQL in CI, run models against small seeded inputs in a test schema and compare to expected outputs (dbt unit tests), apply data tests on results, and lint SQL for style and anti-patterns.

#### How do you test Airflow DAGs?

Load all DAGs with `DagBag` and fail on import errors, check conventions (owners, retries, tags, no cycles), unit test the Python logic used by tasks, and run integration tests in a staging Airflow.

<!-- challenge -->

A source added a column and the pipeline silently dropped a different column because of a positional select. What test would have caught it?

<!-- solution -->

A schema evolution test: feed a fixture with an extra column inserted in the middle and assert the output schema and values are unchanged. Then fix the code to select by name.

<!-- takeaways -->

- Test empty, null, duplicate, late and changed inputs.
- Run steps twice to prove idempotency.
- Build SQL on seeds; load DAGs with `DagBag`.

<!-- unit: Advanced testing techniques -->

<!-- goals -->

- Use property-based and mutation testing where they pay off.
- Track performance without slowing every PR.

<!-- concept -->

Example-based tests only check cases someone thought of. Property-based testing generates many inputs and checks rules that must always hold, such as "deduplication never increases row count". Mutation testing checks the tests themselves by breaking the code on purpose and seeing whether anything fails.

Performance needs its own rhythm: benchmarks on realistic volumes are too slow for each PR, but run regularly they show regressions before users do.

<!-- example -->

```python
from hypothesis import given, strategies as st

@given(st.lists(st.tuples(st.integers(1, 5), st.integers())))
def test_dedupe_never_adds_rows(rows):
    assert len(dedupe_by_key(rows)) <= len(rows)
```

#### What is property-based testing, and is it useful for data?

Generating many random inputs that satisfy constraints and checking properties that should always hold (for example, deduplication output has unique keys and is a subset of input). Tools like Hypothesis find edge cases hand-written tests miss.

#### What is mutation testing?

Introducing small changes to the code (mutants) and checking whether tests fail; surviving mutants reveal weak tests. It's rarely used in data teams but useful for critical libraries.

#### How do you test performance in CI?

Usually not on every PR, but with periodic benchmarks on representative data volumes, tracking runtime, shuffle sizes and cost, and alerting on regressions; lint rules can catch known performance anti-patterns cheaply.

<!-- challenge -->

A team has 95% coverage, yet bugs keep reaching production. How could mutation testing help?

<!-- solution -->

It shows whether tests actually check behavior: if mutants (flipped conditions, changed constants) survive, those tests execute code without asserting the right things. Strengthen the assertions where mutants survive.

<!-- takeaways -->

- Property tests check invariants on generated inputs.
- Mutation testing measures how strong tests are.
- Benchmark performance on a schedule, not per PR.

### Code quality and static checks

<!-- unit: Linters and formatting -->

<!-- goals -->

- Set up linters, formatters and type checks for data code.
- Run them early with pre-commit and custom rules.

<!-- concept -->

Static checks find problems without running anything. Formatters end style arguments; linters catch bugs and bad patterns; type checkers find wrong arguments and `None` handling. Running them on every commit keeps reviews focused on logic.

Data teams benefit from custom rules too: a check that flags `collect()` on large DataFrames or `SELECT *` in models encodes lessons the team learned the hard way.

<!-- example -->

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks: [{id: ruff, args: [--fix]}, {id: ruff-format}]
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.2.0
    hooks: [{id: sqlfluff-lint}]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks: [{id: gitleaks}]
```

#### What linters are used in data projects?

Ruff (Python linting and formatting), mypy or pyright (type checking), SQLFluff (SQL linting and formatting for many dialects, dbt aware), yamllint, shellcheck, hadolint for Dockerfiles, and tool-specific checks (dbt project evaluator, Airflow `AIR` rules).

#### What is pre-commit?

A framework that runs configured hooks (formatters, linters, secret scanners, checks for large files) on each commit locally, catching issues before they reach CI; the same hooks can run in CI for consistency.

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.2.0
    hooks:
      - id: sqlfluff-lint
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks:
      - id: gitleaks
```

#### Why enforce formatting automatically?

It ends style debates in reviews, makes diffs smaller and readable, and lets reviewers focus on logic. Formatters like Ruff and SQLFluff fix formatting automatically.

#### Why add type hints to data code?

They document interfaces, let type checkers catch mistakes (wrong argument types, `None` handling) before runtime, and improve IDE support, which matters for shared libraries used by many pipelines.

#### What are custom lint rules for data code?

Project-specific checks for anti-patterns, such as `collect()` on large DataFrames, Python UDFs where built-ins exist, `SELECT *` in production models, hard-coded paths or credentials, missing partition filters, or `withColumn` in loops.

<!-- challenge -->

Code reviews keep turning into debates about SQL style. What do you introduce?

<!-- solution -->

A formatter and linter for SQL (SQLFluff) with an agreed configuration, run in pre-commit and enforced in CI. Style becomes automatic and reviews focus on logic.

<!-- takeaways -->

- Formatters, linters and type checks catch issues early.
- Pre-commit runs them before code leaves the laptop.
- Custom rules encode team-specific lessons.

<!-- unit: Checks beyond style -->

<!-- goals -->

- Add security analysis and coverage to CI.
- Validate dbt projects, YAML and workflow files.

<!-- concept -->

Static analysis also covers security and structure. Security scanners flag risky code and insecure infrastructure definitions. Coverage shows untested areas, as a signal rather than a goal.

Configuration deserves checks as much as code: dbt projects can be parsed and evaluated against conventions, YAML validated against schemas, and CI workflow files linted before they run.

<!-- example -->

```yaml
- run: dbt deps && dbt parse
- run: sqlfluff lint models/
- run: checkov -d infra/
- run: actionlint
- run: pytest --cov=src --cov-report=xml
```

#### What is static analysis for security?

Tools like Bandit (Python security issues), Semgrep (custom rules), Checkov or tfsec (infrastructure misconfigurations) and dependency scanners that find vulnerabilities and risky patterns before deployment.

#### What is code coverage, and how should you use it?

The percentage of code executed by tests. It's a useful signal for untested areas but not a goal in itself; aim for meaningful tests of critical logic rather than a number, and watch coverage trends on changed files.

#### How do you check dbt projects in CI?

`dbt deps`, `dbt parse` or `compile` to catch syntax and reference errors, SQLFluff linting, dbt project evaluator for conventions, and `dbt build` on modified models with tests in a CI schema.

#### What is the dbt project evaluator?

A dbt package that checks a project against best practices (model naming, layering, direct source references from marts, missing tests or documentation, fan-out patterns) and can fail CI on violations.

#### How do you check YAML and configuration files?

With schema validation (JSON Schema for configs, `databricks bundle validate`, `actionlint` for GitHub workflows), yamllint for syntax and style, and tests that load every config file the pipeline uses.

#### What is actionlint?

A static checker for GitHub Actions workflow files that catches syntax errors, invalid expressions, unknown inputs and shell script issues before workflows run.

<!-- challenge -->

A manager wants to require 90% coverage on all PRs. What do you advise?

<!-- solution -->

Use coverage to find untested critical code and to prevent large drops, not as a hard target: a high number with weak assertions gives false comfort. Require tests for new logic and review their quality instead.

<!-- takeaways -->

- Security scanners check code and infrastructure.
- Coverage is a signal, not a goal.
- Validate dbt, YAML and workflow files in CI.

<!-- stage: Platform -->

### Environments and configuration

<!-- unit: Environments and isolation -->

<!-- goals -->

- Define the environments a data platform needs and how to isolate them.
- Promote artifacts across environments with consistent naming.

<!-- concept -->

Environments give changes a safe path to production. Development is for building, staging for proving, production for consumers. Isolation, by account, workspace or catalog, keeps a mistake in one from reaching the others and lets permissions differ.

Parity makes staging meaningful: the closer it is to production, the more a passing test means. And promotion moves the same artifact through each environment rather than rebuilding it.

<!-- example -->

```text
dev:     catalog dev_sales,  workspace dev,  role developer (read prod)
staging: catalog stg_sales,  workspace stg,  role ci-deployer
prod:    catalog sales,      workspace prod, role prod-deployer (no humans)
artifact etl-2.4.1.whl  ──► dev ──► staging ──► prod
```

#### Which environments does a data platform need?

At least development (individual or shared sandboxes), a staging or pre-production environment mirroring production, and production. Some add test/QA environments or ephemeral environments per pull request.

#### Why separate environments by account, workspace or catalog?

Isolation limits the blast radius of mistakes, allows different permissions (developers can't write production), separates costs, and makes promotion explicit.

#### What is environment parity?

Keeping environments as similar as possible (same code, versions, configurations, infrastructure templates) so tests in staging predict production behavior; differences should be limited to scale, data and credentials.

#### How do you name resources across environments?

With a consistent scheme that includes the environment (`sales_prod`, `catalog_dev`, `dbt_ci_pr_123`), derived from configuration rather than hard-coded, so code never accidentally points to production from dev.

#### What is promotion between environments?

Moving the same artifact from dev to staging to production after checks pass at each stage, rather than rebuilding, with approvals for production.

<!-- challenge -->

Staging uses a different Spark version and smaller clusters than production, and bugs keep appearing only in production. What do you change?

<!-- solution -->

Align staging with production: same runtime versions, configuration and infrastructure code, with smaller sizes only where they don't change behavior. Deploy both from the same IaC with environment variables.

<!-- takeaways -->

- Dev, staging and prod give changes a safe path.
- Isolate environments by account, workspace or catalog.
- Parity and promotion make staging results trustworthy.

<!-- unit: Configuration per environment -->

<!-- goals -->

- Keep configuration out of code with variables and files per environment.
- Use ephemeral environments for pull requests.

<!-- concept -->

The same artifact must run everywhere, so what differs between environments, such as paths, catalogs, sizes and endpoints, comes from configuration, not code. The twelve-factor rule puts it in the environment, with secrets in a secrets manager.

Ephemeral environments push the idea further: each pull request gets its own short-lived schema or workspace, created and destroyed automatically, so tests never collide.

<!-- example -->

```yaml
# databricks.yml targets
targets:
  dev:     {variables: {catalog: dev_sales,  workers: 2}}
  staging: {variables: {catalog: stg_sales,  workers: 4}}
  prod:    {variables: {catalog: sales,      workers: 16}}
```

#### How do you manage configuration per environment?

With configuration files or variables per environment (paths, catalogs, cluster sizes, schedules) injected at deploy time, keeping the code identical; secrets come from a secrets manager, never from files in the repo.

#### What is the twelve-factor principle about configuration?

Store configuration in the environment (variables), not in code, so the same build artifact runs in every environment with different settings.

#### What are ephemeral environments?

Short-lived environments created automatically for a pull request (a schema, a branch of the catalog, a clone of tables, a deployed copy of jobs) and destroyed after merge, letting reviewers test changes in isolation.

<!-- challenge -->

Two PRs run CI at the same time and their tests overwrite each other's tables in a shared CI schema. What do you change?

<!-- solution -->

Give each PR its own schema (for example `ci_pr_123`) created at the start of the run and dropped when the PR closes, with the name passed in as configuration.

<!-- takeaways -->

- Configuration varies; the artifact doesn't.
- Keep config in the environment, secrets in a vault.
- Ephemeral environments isolate each PR.

<!-- unit: Data for non-production -->

<!-- goals -->

- Provide realistic, safe data for staging and development.
- Use data versioning and write-audit-publish.

<!-- concept -->

Code can be copied freely between environments; data can't. Staging needs production-like data to catch real problems, but copying personal data everywhere is a risk. The usual answer is cloning or sampling with masking, and read-only access to production for development where policy allows.

Data versioning and write-audit-publish bring CI ideas to data itself: write new data to a branch or staging area, check it, then publish atomically.

<!-- example -->

```text
write:   INSERT INTO sales.orders_staging  (or Iceberg branch "audit")
audit:   row counts, uniqueness, freshness, reconciliation
publish: swap/fast-forward into sales.orders only if checks pass
```

#### How do you provide test data in staging?

Copy or clone production data with masking or anonymization of personal data, sample to reduce cost, use zero-copy clones (Snowflake, Delta shallow clones) where available, or generate synthetic data at production-like scale.

#### Should staging use production data?

Ideally staging uses production-like data (cloned, sampled or masked) to catch real-world issues, with strict controls on personal data; purely synthetic staging can miss problems that only real data reveals.

#### How do developers work without touching production data?

Personal schemas or catalogs, development targets that read from production read-only (or from clones) and write only to dev, sampled or masked data, and permissions that prevent writes to production from developer identities.

#### What is data versioning, and why is it useful in CI/CD?

Versioning datasets like code (lakeFS branches, Project Nessie for Iceberg, Delta and Iceberg snapshots, dbt snapshots) to reproduce runs, test changes on isolated branches of data and roll back bad writes.

#### What is the write-audit-publish (WAP) pattern?

Writing new data to a staging location or branch, auditing it with quality checks, and only then publishing it (swap, merge or fast-forward) so consumers never see bad data. Iceberg branches, lakeFS and table swaps implement it.

<!-- challenge -->

A nightly load once published half a day's data to dashboards before a failure, and executives saw wrong numbers. Which pattern prevents it?

<!-- solution -->

Write-audit-publish: load into a staging table or branch, run quality checks, and publish with an atomic swap only when checks pass, so consumers see either the old or the complete new data.

<!-- takeaways -->

- Staging needs production-like, masked data.
- Developers read production read-only or work on samples.
- WAP publishes data only after it passes checks.

### Infrastructure as code

<!-- unit: Declaring infrastructure -->

<!-- goals -->

- Explain infrastructure as code and the main tools.
- Structure IaC for several environments, including permissions.

<!-- concept -->

Clicking resources into existence leaves no record and can't be repeated. Infrastructure as code declares buckets, clusters, catalogs, jobs and permissions in files, so environments are built the same way every time and changes go through review.

Good structure keeps that manageable: reusable modules for common pieces, variables per environment, and immutable replacement instead of patching resources in place. Permissions belong in code too, since grants drift fastest.

<!-- example -->

```hcl
module "lake" {
  source      = "./modules/lake"
  environment = var.environment          # dev, staging, prod
  buckets     = ["raw", "curated"]
}

resource "databricks_grants" "sales" {
  catalog = "sales"
  grant { principal = "analysts"  privileges = ["USE_CATALOG", "SELECT"] }
}
```

#### What is infrastructure as code (IaC)?

Defining cloud resources (storage, compute, networks, permissions, catalogs, jobs) in declarative code that is versioned, reviewed and applied automatically, instead of creating them by hand in consoles.

#### Which IaC tools are common for data platforms?

Terraform/OpenTofu (multi-cloud), AWS CloudFormation, CDK and SAM, Azure Bicep, Pulumi, and platform-specific tools such as Databricks Asset Bundles, Snowflake's Terraform provider and Kubernetes manifests with Helm.

#### What is immutable infrastructure?

Replacing components with new versions instead of modifying them in place (new container images, new clusters), which makes deployments predictable and rollbacks simple.

#### How do you structure IaC for multiple environments?

Reusable modules for common components, with environment-specific variables or workspaces (dev, staging, prod), separate state per environment, and the same modules promoted through environments.

#### How do you manage data platform permissions as code?

Define roles, grants and catalog permissions in Terraform or platform tools (Snowflake provider, Databricks Terraform provider, Unity Catalog grants in bundles), reviewed in pull requests, so access changes are auditable and reversible.

<!-- challenge -->

Permissions on the warehouse were granted by hand over years, and nobody knows who has access to what. How do you move to code?

<!-- solution -->

Export current grants, model them as roles in IaC, review and remove what isn't needed, import existing objects into state, and from then on change grants only through pull requests. Detect drift on a schedule.

<!-- takeaways -->

- IaC makes infrastructure reviewable and repeatable.
- Modules plus per-environment variables keep it manageable.
- Permissions belong in code too.

<!-- unit: Plan, state and drift -->

<!-- goals -->

- Review infrastructure changes with plan and apply.
- Manage state, detect drift and enforce policies.

<!-- concept -->

IaC tools compare what the code declares with what exists, recorded in state, and compute a plan. Reviewing that plan is the main safety check: it shows what will be created, changed or destroyed before anything happens.

State must be stored remotely with locking, and manual changes create drift that the next apply may revert. Policy as code adds automatic rules on top of human review, such as forbidding public buckets or deletions of protected resources.

<!-- example -->

```hcl
resource "aws_s3_bucket" "raw" {
  bucket = "acme-lake-raw-prod"
  lifecycle { prevent_destroy = true }
}
```
```bash
terraform plan -out=tfplan && terraform show -no-color tfplan > plan.txt   # posted to the PR
```

#### What is the plan/apply workflow in Terraform?

`terraform plan` shows the changes that would be made; reviewers check the plan in the pull request; `terraform apply` executes it after approval, typically from CI with remote state and locking.

#### What is Terraform state, and how should it be stored?

A file mapping configuration to real resources. Store it remotely (S3 with locking, Terraform Cloud, Azure Storage) with encryption and access control, never in Git, and separate state per environment.

#### What is configuration drift?

Differences between the declared infrastructure and reality, caused by manual changes. Detect it with scheduled `terraform plan` runs or drift detection services, and fix by updating code or reverting manual changes.

#### How do you review infrastructure changes safely?

Post the `terraform plan` (or CDK diff, CloudFormation change set) as a pull request comment, require reviews from owners of affected resources, use policy checks (Checkov, OPA/Conftest, Sentinel), and apply only from CI.

#### What is policy as code?

Writing organizational rules (encryption required, no public buckets, tags mandatory, approved regions) as code evaluated automatically in CI or at deployment, for example with Open Policy Agent, Checkov or cloud-native policy services.

#### A Terraform apply in CI deleted a production resource. How do you prevent it from happening again?

Require plan review before apply, add `prevent_destroy` lifecycle rules on critical resources, run policy checks that block deletions of protected resources, separate state and permissions per environment, and restore from backups or re-import the resource now.

<!-- challenge -->

Someone changed a production cluster size in the console. What happens on the next Terraform apply, and what should the process be?

<!-- solution -->

Terraform sees drift and reverts the size to the code's value. The change should be made in code through a PR; run scheduled `terraform plan` to detect drift and alert on it.

<!-- takeaways -->

- Review the plan before every apply.
- Keep state remote and locked.
- Detect drift; enforce rules with policy as code.

### Packaging and artifacts

<!-- unit: Artifacts and versions -->

<!-- goals -->

- Build versioned artifacts once and deploy them everywhere.
- Store artifacts in registries and stamp versions in CI.

<!-- concept -->

An artifact is the exact thing that gets deployed: a wheel, an image, a compiled dbt project. Building it once and promoting the same bytes through every environment guarantees that what was tested is what runs in production.

Versions tie artifacts to source: semantic versions for libraries, commit SHAs for applications, both derived automatically in CI. Registries store them so any version can be redeployed.

<!-- example -->

```bash
python -m build                                   # version from setuptools-scm: 2.4.1
twine upload --repository codeartifact dist/*
docker build -t $ECR/etl:$(git rev-parse --short HEAD) . && docker push $ECR/etl:$(git rev-parse --short HEAD)
```

#### What is a build artifact in data projects?

The versioned output of a build that gets deployed: a Python wheel with pipeline code, a Docker image, a JAR, a compiled dbt manifest, a bundle, or a zip of SQL scripts. Build once, deploy the same artifact everywhere.

#### Why "build once, deploy many"?

Rebuilding for each environment can produce different artifacts (dependency changes, timing), so what was tested isn't what's deployed. Building one artifact and promoting it guarantees consistency.

#### How do you version artifacts?

With semantic versions for libraries, and commit SHAs or build numbers for applications (`0.2.145+g1a2b3c4`), stamped at build time so every deployment is traceable to a commit.

#### How do you stamp a version into a Python package in CI?

Derive it from Git (setuptools-scm, `git describe`) or set it explicitly in CI from a run number and short SHA, so every artifact maps to a commit; avoid reusing the same version for different code.

#### Where do you store artifacts?

In artifact repositories and registries: PyPI-compatible repositories (CodeArtifact, Artifactory, GitHub Packages), container registries (ECR, ACR, GHCR), S3 buckets for scripts, or platform stores (Databricks workspace files and volumes).

<!-- challenge -->

Production behaves differently from staging although "the code is the same". Each environment rebuilds the image at deploy time. Why is that a problem?

<!-- solution -->

Each rebuild can pull different dependency versions or base images, so staging and prod run different artifacts. Build the image once in CI, tag it with the commit SHA, and deploy that same tag everywhere.

<!-- takeaways -->

- Artifacts are the deployable units.
- Build once; promote the same artifact.
- Version from Git and store in registries.

<!-- unit: Dependencies and containers -->

<!-- goals -->

- Make Python dependencies reproducible with lock files.
- Package with containers and scan them with SBOMs.

<!-- concept -->

Unpinned dependencies make builds drift: the same code installs different libraries next month. Lock files fix exact versions, including transitive ones, so a build is reproducible.

Containers extend that to the whole runtime, operating system libraries included. The cost is responsibility for what's inside: base images carry vulnerabilities, so images are scanned and an SBOM records every component.

<!-- example -->

```dockerfile
FROM python:3.12.7-slim
COPY uv.lock pyproject.toml ./
RUN pip install uv && uv sync --frozen --no-dev
COPY src/ ./src/
```
```bash
trivy image --severity HIGH,CRITICAL --exit-code 1 $ECR/etl:abc123
```

#### How do you manage Python dependencies reproducibly?

Pin exact versions with lock files (`uv.lock`, `poetry.lock`, `pip-tools` requirements), separate runtime and dev dependencies, build in clean environments, and update dependencies deliberately (Dependabot or Renovate with tests).

#### Why use containers for data pipelines?

Containers package code with exact dependencies and OS libraries, making runs identical across laptops, CI and production, and fit orchestrators like Kubernetes, ECS, Airflow's KubernetesPodOperator and Cloud Run.

#### What is an SBOM?

A software bill of materials listing every component and dependency (with versions) in an artifact, generated in CI (Syft, CycloneDX) to track vulnerabilities and licenses.

#### Why scan container images in CI?

Base images and dependencies contain known vulnerabilities; scanners (Trivy, Grype, registry scanning) find them before deployment, and policies can block critical issues.

<!-- challenge -->

A nightly job broke because a dependency released a new major version overnight. Nothing in the repo changed. What do you change?

<!-- solution -->

Pin all dependencies with a lock file and install from it (`--frozen`), and let Dependabot or Renovate propose upgrades as PRs that run through CI.

<!-- takeaways -->

- Lock files make installs reproducible.
- Containers fix the whole runtime.
- Scan images and keep SBOMs.

<!-- stage: Delivery -->

### Deployment strategies

<!-- unit: Strategies for code and data -->

<!-- goals -->

- Apply blue-green, canary and shadow deployments to pipelines.
- Use feature flags to control new logic.

<!-- concept -->

Deployment strategies reduce the risk of a change by limiting who sees it until it's proven. For data, the same ideas apply to tables: build the new version next to the old one and switch (blue-green), run it on a slice first (canary), or run it on real inputs without consumers seeing it (shadow).

Feature flags give the same control inside code: new logic is deployed but off until someone flips it.

<!-- example -->

```sql
-- blue-green for a table: build v2, validate, then switch the view consumers use
CREATE TABLE marts.revenue_v2 AS SELECT ...;
-- validation queries comparing v1 and v2 ...
CREATE OR REPLACE VIEW marts.revenue AS SELECT * FROM marts.revenue_v2;
```

#### What deployment strategies exist?

Recreate (stop old, start new), rolling (replace instances gradually), blue-green (switch traffic between two full environments), canary (send a small share to the new version first), shadow (run new version in parallel without serving results) and feature flags (deploy dark, enable later).

#### How does blue-green deployment apply to data?

Build the new version of tables or pipelines alongside the current ones (new schema, table version or clone), validate, then switch consumers atomically (view swap, table rename, catalog pointer), keeping the old version for quick rollback.

#### What is a canary release for data pipelines?

Running the new version on a subset (one country, one partition, a sample of customers) or in parallel with the old version, comparing outputs and metrics, then expanding once confident.

#### What is shadow mode?

Running a new pipeline version in parallel on real inputs, writing to separate tables that nobody consumes, and comparing results with the production version before switching.

#### What are feature flags in data platforms?

Configuration switches that turn new logic or new outputs on or off without redeploying, allowing gradual rollout, quick disabling of problematic features and decoupling deployment from release.

<!-- challenge -->

A new attribution model will change marketing numbers. How do you release it without surprising the business?

<!-- solution -->

Run it in shadow mode for a few weeks, writing to separate tables, and compare results with the current model. Share the differences with stakeholders, then switch with a flag or view on an agreed date.

<!-- takeaways -->

- Blue-green, canary and shadow limit exposure.
- For data, build new tables alongside old ones.
- Feature flags decouple deploying from enabling.

<!-- unit: Schema changes -->

<!-- goals -->

- Make schema changes without breaking running code or consumers.
- Use expand-and-contract and migration tools.

<!-- concept -->

Schema changes are the riskiest part of data deployments: running jobs expect the old shape, consumers read the table directly, and some changes lock tables or are hard to undo. Doing them in one step forces every reader and writer to change at the same moment.

Expand-and-contract splits the change: add the new shape, migrate writers and readers, then remove the old shape. Migration tools apply ordered, tracked changes so every environment ends up the same.

<!-- example -->

```text
1. expand:   ADD COLUMN gross_amount; write both amount and gross_amount
2. migrate:  backfill gross_amount; move readers to gross_amount
3. contract: stop writing amount; DROP COLUMN amount (after deprecation date)
```

#### Why are database schema changes risky in deployments?

They can break running code, lock tables, require data migration and are hard to reverse. Use backward-compatible changes (expand and contract), migrations tested on clones, and deploy schema and code in compatible steps.

#### What is the expand-and-contract pattern?

Making schema changes in phases: expand (add new column or table, keep old), migrate (write both, backfill, switch readers), contract (remove the old column once nobody uses it). Each step is backward compatible.

#### What are database migration tools?

Tools that apply versioned, ordered schema changes and track which have run: Flyway, Liquibase, Alembic (SQLAlchemy), Sqitch, schemachange (Snowflake), and dbt for transformation-managed objects.

#### How do you deploy a change to a heavily used table without downtime?

Build the new version in parallel (new table or version), validate it, then switch atomically (swap, rename or update a view), and keep the old version for rollback; avoid in-place rewrites while consumers read.

<!-- challenge -->

You must rename `cust_id` to `customer_id` in a table read by 12 dashboards. Plan it.

<!-- solution -->

Add `customer_id` and populate it alongside `cust_id` (or expose it through a view), announce the deprecation, migrate dashboards, monitor that `cust_id` is no longer queried, then drop it.

<!-- takeaways -->

- Schema changes break running code and consumers.
- Expand, migrate, then contract.
- Migration tools keep schemas consistent across environments.

<!-- unit: Rollbacks, backfills and freezes -->

<!-- goals -->

- Roll back code and data after a bad deployment.
- Plan backfills, freezes and streaming deployments.

<!-- concept -->

Rolling back code is easy: redeploy the previous artifact. Rolling back data is not: tables already contain what the bad version wrote. Plans need both, using time travel, snapshots or a rerun of the previous logic.

Changes that require recomputing history are deployments with a cost and a schedule. Freezes protect critical periods, and streaming jobs add state that must survive the upgrade.

<!-- example -->

```sql
-- data rollback on Delta / Iceberg after a bad deploy at 09:40
RESTORE TABLE marts.revenue TO TIMESTAMP AS OF '2026-10-17 09:30:00';
```

#### How do you roll back a data deployment?

Redeploy the previous code artifact, and for data either restore tables with time travel or snapshots, switch views back to the previous version (blue-green), or rerun the old logic for affected partitions. Plan rollback before deploying risky changes.

#### How do you handle backfills in deployments?

Treat them as part of the release plan: estimate cost and duration, parameterize pipelines by date range, run in controlled batches (often off-peak), validate outputs, and communicate to consumers when historical data changes.

#### How do you deploy a change that requires recomputing history?

Plan a backfill: deploy the new logic writing to a new table or version, recompute history in batches, validate against the old outputs, switch consumers, and communicate restated numbers, rather than overwriting history in place without checks.

#### What is a deployment freeze, and when is it appropriate?

A period with no production deployments, for example during financial closing or peak sales, to reduce risk; it's better to make deployments safe and routine, keeping freezes short and for genuine high-risk periods.

#### How do you deploy streaming job changes?

Check state compatibility, stop the job gracefully (savepoint or checkpoint), deploy the new version from the same checkpoint if compatible, or start a new job with a new checkpoint and a backfill plan; run old and new in parallel for critical streams.

<!-- challenge -->

A logic change requires recomputing three years of a 4 TB table. How do you deploy it without disrupting consumers?

<!-- solution -->

Deploy the new logic writing to a new table version, backfill history in batches with limited concurrency and a cost estimate, validate against the old table, then switch consumers atomically (view or swap) and keep the old version for a while.

<!-- takeaways -->

- Plan data rollback, not just code rollback.
- Backfills are releases with cost and schedule.
- Streaming deploys must preserve state.

### GitHub Actions in depth

<!-- unit: Workflows, jobs and triggers -->

<!-- goals -->

- Read and write GitHub Actions workflows with jobs and steps.
- Choose triggers, including schedules, path filters and manual inputs.

<!-- concept -->

A workflow is a YAML file that says when to run and what to do. Triggers decide the when: pushes, pull requests, schedules, manual runs with inputs. Jobs run in parallel on separate machines unless they depend on each other; steps run in order inside a job.

Path filters keep workflows focused, so a documentation change doesn't run the Spark test suite.

<!-- example -->

```yaml
name: ci
on:
  pull_request:
    paths: ["src/**", "tests/**", "pyproject.toml"]
  workflow_dispatch:
    inputs:
      start_date: {description: "First date to backfill (YYYY-MM-DD)", required: true}
permissions: {contents: read}
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12", cache: pip}
      - run: pip install -e .[dev] && pytest -q
```

#### What is GitHub Actions?

GitHub's CI/CD and automation platform: workflows defined in YAML in `.github/workflows/` run on events (push, pull request, schedule, manual dispatch, releases) on GitHub-hosted or self-hosted runners.

#### What are workflows, jobs and steps?

A workflow is an automated process defined in a YAML file; it contains jobs that run on runners, in parallel by default or in order with `needs`; each job has steps that run commands (`run`) or actions (`uses`).

#### What does a basic CI workflow for a Python data project look like?

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: ruff check . && ruff format --check .
      - run: pytest -q --maxfail=1
```

#### What triggers can start a workflow?

`push`, `pull_request` (and `pull_request_target`), `schedule` (cron), `workflow_dispatch` (manual, with inputs), `workflow_call` (reusable), `release`, `repository_dispatch` (external API), `merge_group` (merge queue) and many other repository events.

#### How do you run a workflow only when certain files change?

With path filters on the trigger, for example `on: pull_request: paths: ["models/**", "dbt_project.yml"]`, or with a step that detects changed files and conditionally runs jobs, which saves CI time in monorepos.

#### How do you run scheduled jobs in GitHub Actions?

With `on: schedule: - cron: "0 5 * * *"` (UTC). It's handy for nightly drift checks, dependency audits or small data jobs, but not a replacement for a data orchestrator: schedules can be delayed and are disabled on inactive repositories.

#### What is `workflow_dispatch` used for?

Manual triggers with optional typed inputs, for example deploying a specific version, running a backfill for a date range or starting a production job after deployment.

#### How do you trigger a deployment manually with inputs?

```yaml
on:
  workflow_dispatch:
    inputs:
      start_date:
        description: First date to backfill (YYYY-MM-DD)
        required: true
      run_job:
        type: boolean
        default: false
```

Inputs are then available through the `inputs` context in jobs and steps.

<!-- challenge -->

A monorepo has dbt models and Python jobs, and every PR runs both test suites (30 minutes). How do you speed it up?

<!-- solution -->

Split into two workflows (or jobs) with path filters: dbt checks run on changes under `models/`, Python tests on `src/` and `tests/`. Shared files like CI config trigger both.

<!-- takeaways -->

- Workflows define triggers; jobs run in parallel; steps run in order.
- Path filters run only relevant checks.
- `workflow_dispatch` adds manual runs with inputs.

<!-- unit: Runners, caching and artifacts -->

<!-- goals -->

- Choose runners and pin their images.
- Speed up jobs with caching and matrices, and pass files and values between jobs.

<!-- concept -->

Each job runs on a fresh runner, which is safe but forgets everything between runs. Caching restores dependencies so installs don't start from zero; artifacts carry files from one job to another; outputs carry small values. Matrices run the same job across versions in parallel.

Runners themselves are a choice: hosted images change over time, so pinning a version avoids surprise breakages, and larger or self-hosted runners exist for heavy work.

<!-- example -->

```yaml
jobs:
  build:
    runs-on: ubuntu-24.04
    outputs: {version: "${{ steps.v.outputs.version }}"}
    steps:
      - uses: actions/checkout@v4
      - id: v
        run: echo "version=$(git describe --tags)" >> "$GITHUB_OUTPUT"
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with: {name: dist, path: dist/}
  deploy:
    needs: build
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/download-artifact@v4
        with: {name: dist}
      - run: echo "deploying ${{ needs.build.outputs.version }}"
```

#### What is a runner?

The machine that executes jobs: GitHub-hosted runners (Ubuntu, Windows, macOS, larger and GPU sizes) are fresh VMs per job; self-hosted runners are your own machines or Kubernetes pods, used for private network access, special hardware or cost.

#### Why pin the runner image version?

`ubuntu-latest` changes when GitHub moves to a new image, which can break builds unexpectedly. Pinning `ubuntu-24.04` gives reproducible builds; upgrade deliberately.

#### What is a matrix build?

Running the same job with different parameter combinations in parallel, for example several Python versions or several dbt adapters.

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        python: ["3.11", "3.12"]
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e ".[dev]" && pytest -q
```

#### How does caching work in GitHub Actions?

`actions/cache` (or built-in caching in `setup-python`, `setup-node`, `setup-java`) stores directories like pip or Maven caches keyed by a hash of lock files, restoring them in later runs to speed up dependency installation.

#### What are artifacts in GitHub Actions?

Files produced by a job (test reports, built wheels, the site, dbt manifests) uploaded with `actions/upload-artifact` and downloadable by later jobs or people, with a retention period.

#### How do jobs pass data to each other?

Through artifacts for files, and job outputs for small values: a step writes `name=value` to `$GITHUB_OUTPUT`, the job declares `outputs`, and dependent jobs read them via the `needs` context.

#### How do you pass outputs between jobs?

```yaml
jobs:
  version:
    runs-on: ubuntu-24.04
    outputs:
      tag: ${{ steps.v.outputs.tag }}
    steps:
      - id: v
        run: echo "tag=0.2.${{ github.run_number }}" >> "$GITHUB_OUTPUT"
  deploy:
    needs: version
    runs-on: ubuntu-24.04
    steps:
      - run: echo "Deploying ${{ needs.version.outputs.tag }}"
```

#### What are GitHub-hosted larger runners and self-hosted runners used for in data teams?

Larger runners help with heavy builds or Spark tests; self-hosted runners in your cloud network can reach private databases or warehouses for integration tests and avoid exposing them publicly, but they must be hardened and isolated (ephemeral runners are recommended).

#### How do you set default shell options and working directory?

With `defaults: run:` at workflow or job level, for example `shell: bash` and `working-directory: ./dbt`, so every `run` step uses them; bash steps run with `-e` (exit on error) by default in GitHub Actions.

<!-- challenge -->

The deploy job rebuilds the wheel that the test job already built, and sometimes deploys a slightly different version. Fix it.

<!-- solution -->

Build once in a build job, upload the wheel as an artifact, run tests against it, and have the deploy job download that same artifact (and version output) instead of rebuilding.

<!-- takeaways -->

- Runners start fresh; caches and artifacts carry things over.
- Outputs pass small values between jobs.
- Pin runner images; use larger or self-hosted runners for heavy work.

<!-- unit: Secrets, environments and OIDC -->

<!-- goals -->

- Store secrets and variables safely, including in public repositories.
- Deploy with environments, approvals and OIDC instead of long-lived keys.

<!-- concept -->

Workflows need credentials, and how you provide them decides your exposure. Secrets are encrypted and masked in logs; variables are not, so in public repositories anything identifying belongs in secrets. Environments scope secrets to a target and can require approval before a job runs.

OIDC removes stored cloud keys entirely: the workflow proves its identity with a short-lived token, and the cloud role trusts only specific repositories, branches or environments. The `GITHUB_TOKEN` should get the narrowest permissions possible.

<!-- example -->

```yaml
permissions: {id-token: write, contents: read}
jobs:
  deploy:
    environment: production          # required reviewers, prod-only secrets
    runs-on: ubuntu-24.04
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: eu-west-1
```

#### What are secrets and variables in GitHub Actions?

Secrets are encrypted values (tokens, passwords) available to workflows and masked in logs; variables are non-sensitive configuration values. Both can be defined at organization, repository or environment level and are referenced through the `secrets` and `vars` contexts.

#### Why should identifying values be secrets in public repositories?

Workflow logs of public repositories are public, and only secrets are masked. Hostnames, account IDs, bucket names or emails stored as plain variables can leak in logs, so treat them as secrets when the repository is public.

#### A public repository's workflow logs show a database hostname. What do you change?

Move the hostname and other identifying values to environment secrets so they're masked, rotate credentials if anything sensitive appeared, review past logs, and add a check that prevents printing configuration in logs.

#### What are GitHub environments?

Named deployment targets (dev, staging, production) with their own secrets and variables and protection rules: required reviewers, wait timers, branch restrictions and deployment history, which gate CD jobs.

```yaml
jobs:
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    environment:
      name: production
      url: https://data.example.com
    steps:
      - run: ./scripts/deploy.sh
```

#### What is OIDC authentication from GitHub Actions to the cloud?

The workflow requests a short-lived OpenID Connect token from GitHub, and the cloud provider (AWS, Azure, GCP) exchanges it for temporary credentials for a role that trusts the repository, branch or environment. No long-lived access keys are stored.

```yaml
permissions:
  contents: read
  id-token: write
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
      aws-region: eu-west-1
```

#### How do you restrict which workflows can assume a cloud role via OIDC?

In the role's trust policy, condition on the token's claims: audience (`sts.amazonaws.com`), repository and ref or environment in `sub` (for example `repo:org/repo:environment:production`), so only production deployments from that repository can assume it.

#### What is the `GITHUB_TOKEN`, and how should its permissions be set?

An automatically created token scoped to the repository for each run. Set `permissions:` at workflow or job level to the minimum needed (often `contents: read`), granting extra scopes like `pull-requests: write` or `id-token: write` only to jobs that need them.

#### How do you add a manual approval before production?

Configure the production environment with required reviewers; jobs referencing that environment pause until an approved reviewer approves the deployment in the GitHub UI.

<!-- challenge -->

A repository stores an AWS access key with admin rights as a secret for deployments. What do you replace it with?

<!-- solution -->

An IAM role assumed through GitHub OIDC, with a trust policy limited to this repository and the production environment (`sub` claim), and permissions limited to what deployment needs. Then delete the access key.

<!-- takeaways -->

- Secrets are masked; variables are visible.
- Environments scope secrets and add approvals.
- OIDC replaces stored cloud keys with short-lived tokens.

<!-- unit: Control flow and reuse -->

<!-- goals -->

- Control when jobs run with conditions, concurrency and timeouts.
- Reuse logic with reusable workflows and composite actions.

<!-- concept -->

As pipelines grow, two needs appear: deciding precisely when something runs, and not copying the same YAML into ten repositories. Conditions use expressions over contexts like the branch or event; concurrency stops two deployments from racing; timeouts stop hung jobs from burning minutes.

Reuse comes in two sizes: composite actions bundle steps, reusable workflows bundle whole jobs that other workflows call.

<!-- example -->

```yaml
concurrency: {group: deploy-prod, cancel-in-progress: false}
jobs:
  tests:
    uses: ./.github/workflows/ci.yml
  deploy:
    needs: tests
    if: github.ref == 'refs/heads/main' && github.event_name == 'push' && vars.DEPLOY_AWS == 'true'
    timeout-minutes: 30
    runs-on: ubuntu-24.04
    steps:
      - uses: ./.github/actions/setup-project      # composite action
      - run: make deploy
```

#### What are reusable workflows?

Workflows triggered with `workflow_call` that other workflows invoke with `uses: ./.github/workflows/ci.yml` (or from another repository), passing inputs and secrets, so CI logic is defined once and reused, for example running the full CI as a gate inside the CD workflow.

#### How do you call a reusable workflow?

```yaml
jobs:
  tests:
    uses: ./.github/workflows/ci.yml
  deploy:
    needs: tests
    runs-on: ubuntu-24.04
    environment: production
    steps:
      - run: echo "deploy after CI passed"
```

#### What are composite actions?

Custom actions defined with `runs: using: composite` that bundle several steps (setup, install, configure) into one reusable step, stored in the repository or a shared repository.

#### What does `concurrency` do?

It groups runs by a key and limits them to one at a time; with `cancel-in-progress: true` a new run cancels the older one (good for PR CI), with `false` new runs wait (essential for deployments so two never overlap).

```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

#### How do you make jobs conditional?

With `if:` expressions on jobs or steps, using contexts like `github.ref`, `github.event_name`, `needs.<job>.result`, variables (`vars.DEPLOY_AWS == 'true'`) or functions like `success()`, `failure()` and `always()`.

#### What are expressions and contexts in GitHub Actions?

Expressions are written as `${{ ... }}` in workflow YAML and access contexts like `github` (event and repository data), `env`, `vars`, `secrets`, `matrix`, `needs`, `steps`, `runner` and `inputs`, with functions like `contains`, `startsWith`, `format`, `hashFiles` and status checks.

#### How do you run a job only on the main branch after a push?

`if: github.ref == 'refs/heads/main' && github.event_name == 'push'`, which prevents deployments from pull requests or other branches.

#### How do you deploy only when a repository variable is set?

Gate the job with `if: vars.DEPLOY_AWS == 'true'`, so deployment jobs stay inactive until the environment's setup is complete, without failing CI in the meantime.

#### How do you add timeouts to jobs?

With `timeout-minutes` on jobs (and steps), so a hung job doesn't consume runner minutes for hours; the default job timeout is 360 minutes.

<!-- challenge -->

Two merges a minute apart start two production deployments that run at the same time and leave the job definitions in a mixed state. What do you add?

<!-- solution -->

A `concurrency` group for production deployments without `cancel-in-progress` (so they queue rather than overlap), plus a timeout so a stuck deployment doesn't block the queue forever.

<!-- takeaways -->

- Conditions and contexts decide when jobs run.
- Concurrency groups prevent racing deployments.
- Reuse with composite actions and reusable workflows.

<!-- unit: Safety, feedback and the ecosystem -->

<!-- goals -->

- Protect workflows from untrusted code and moving dependencies.
- Give reviewers clear feedback and keep dependencies current.

<!-- concept -->

Workflows run code, sometimes from strangers. Third-party actions can change under a tag, and triggers that run with secrets on pull requests from forks can be abused. Pinning actions to commits and choosing triggers carefully closes those gaps; merge queues make sure what lands in main was tested with main.

Good feedback keeps developers using CI: test reports, summaries and PR comments put results where people look. Dependency bots and other CI systems follow the same ideas.

<!-- example -->

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683   # v4.2.2, pinned
- run: |
    echo "### dbt build" >> "$GITHUB_STEP_SUMMARY"
    echo "| models | tests | failures |" >> "$GITHUB_STEP_SUMMARY"
    echo "| 42 | 180 | 0 |" >> "$GITHUB_STEP_SUMMARY"
- run: gh pr comment "$PR" --body-file plan.txt
  env: {GH_TOKEN: "${{ github.token }}", PR: "${{ github.event.number }}"}
```

#### Why pin third-party actions to a commit SHA?

Tags like `v4` can be moved, and a compromised action could exfiltrate secrets. Pinning to a full commit SHA (with the version as a comment) guarantees the exact code that runs; Dependabot can keep pinned actions updated.

#### What is the difference between `pull_request` and `pull_request_target`?

`pull_request` runs in the context of the merge commit with read-only token and no secrets for forks, which is safe. `pull_request_target` runs in the base repository context with secrets; checking out and running untrusted PR code in it is a well-known security hole.

#### What is a merge queue?

A GitHub feature that tests pull requests together with the latest main (and with each other) before merging them in order, preventing "green PR, broken main" when several PRs merge close together; CI must also run on the `merge_group` event.

#### How do you see test results nicely in GitHub Actions?

Upload JUnit XML reports as artifacts and publish them with a test reporter action, write a job summary to `$GITHUB_STEP_SUMMARY` (Markdown), or comment results on the pull request.

#### How do you write a job summary?

Append Markdown to the file in `$GITHUB_STEP_SUMMARY` (for example a table of row counts or a test report), which appears on the run's summary page.

#### How do you post a comment on a pull request from a workflow?

Use the GitHub CLI (`gh pr comment`) or an action with the `GITHUB_TOKEN` granted `pull-requests: write`, for example to share a Terraform plan or dbt CI results.

#### How do you build and push a Docker image in GitHub Actions?

With `docker/setup-buildx-action`, `docker/login-action` (to ECR, GHCR or another registry, ideally with OIDC) and `docker/build-push-action`, tagging images with the commit SHA and using layer caching.

#### How do Dependabot or Renovate help CI/CD?

They open pull requests to update dependencies and pinned GitHub Actions, which run through CI like any change, keeping the supply chain current with tested upgrades instead of large, risky updates.

#### How does GitHub Actions compare with GitLab CI and Azure DevOps?

All define pipelines in YAML with stages or jobs, runners/agents, variables and secrets, environments and approvals. GitLab CI uses `.gitlab-ci.yml` with stages and built-in registry; Azure DevOps uses `azure-pipelines.yml` with stages, service connections and tight Azure integration. Concepts transfer directly.

<!-- challenge -->

A workflow uses `pull_request_target` and checks out the PR's code to run tests with deployment secrets available. What is the risk, and what do you do?

<!-- solution -->

A fork's PR can change the test code to exfiltrate secrets, since `pull_request_target` runs with secrets. Use `pull_request` for untrusted code (no secrets), and keep secret-using jobs for trusted branches or after approval.

<!-- takeaways -->

- Pin actions to SHAs; be careful with `pull_request_target`.
- Merge queues test changes against the latest main.
- Summaries, reports and comments make CI results visible.

### CI/CD for dbt

<!-- unit: dbt CI -->

<!-- goals -->

- Build a CI pipeline for dbt with slim CI and defer.
- Isolate CI runs and keep connection settings out of code.

<!-- concept -->

Building every dbt model on every PR gets slow and expensive as projects grow. Slim CI builds only what changed and what depends on it, comparing with the production manifest. Defer fills the gaps by reading unchanged upstream models from production instead of rebuilding them.

Each PR writes to its own schema, and the profile reads all connection details from environment variables, so the same project runs in CI and production without edits.

<!-- example -->

```bash
dbt deps
sqlfluff lint models/
dbt build --select state:modified+ --defer --state prod-artifacts/ --target ci
# profiles.yml: schema: "dbt_ci_pr_{{ env_var('PR_NUMBER') }}", password: "{{ env_var('DBT_PASSWORD') }}"
```

#### What does a CI pipeline for dbt run?

Install dependencies (`dbt deps`), check SQL style (SQLFluff), compile or parse, build and test changed models and their children in an isolated CI schema, check documentation and conventions, and report results on the pull request.

#### What is slim CI in dbt?

Building and testing only modified models and their downstream dependencies, using state comparison with the production manifest: `dbt build --select state:modified+ --defer --state prod-artifacts/`, so CI is fast and cheap.

```yaml
- name: Download production manifest
  run: aws s3 cp s3://dbt-artifacts/prod/manifest.json prod-artifacts/manifest.json
- name: Build modified models
  run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci
```

#### What does `--defer` do?

When a model references an unmodified upstream model that wasn't built in the CI schema, dbt resolves the reference to the production relation instead, so CI doesn't need to rebuild the whole project.

#### How do you isolate dbt CI runs?

Use a CI target that writes to a schema unique per pull request (for example `dbt_ci_pr_123`), and drop it after the run or when the PR closes, so concurrent PRs don't collide.

#### What is the dbt "clone" command useful for in CI?

`dbt clone` creates zero-copy clones (or views) of production relations into the CI or dev schema, so incremental models and downstream tests can run against realistic state cheaply.

#### How do you handle dbt `profiles.yml` in CI?

Commit a profiles file that reads all connection settings from environment variables (`env_var('DBT_HOST')`), and set those variables from secrets in the workflow; never commit credentials.

<!-- challenge -->

Slim CI fails because a modified model references an upstream model that doesn't exist in the CI schema. What is missing?

<!-- solution -->

`--defer` with the production manifest (`--state`), so references to unmodified models resolve to production relations. Alternatively `dbt clone` the needed upstream models into the CI schema first.

<!-- takeaways -->

- Slim CI builds modified models and their children.
- Defer reads unchanged parents from production.
- One schema per PR; credentials from environment variables.

<!-- unit: Deploying dbt safely -->

<!-- goals -->

- Deploy dbt to production with tests, freshness and docs.
- Protect consumers with unit tests, contracts and versions.

<!-- concept -->

Production dbt runs build models and run tests in dependency order, so a failed test stops bad data from flowing downstream. Source freshness checks first make sure inputs are current, and docs are regenerated with each release.

Consumer safety comes from three features: unit tests check model logic on mock rows, contracts enforce column names and types, and versions let a breaking change live alongside the old shape until consumers move.

<!-- example -->

```yaml
models:
  - name: fct_orders
    config: {contract: {enforced: true}}
    columns:
      - {name: order_id, data_type: bigint, constraints: [{type: not_null}]}
      - {name: gross_amount, data_type: numeric(12,2)}
unit_tests:
  - name: test_refunds_are_negative
    model: fct_orders
    given: [{input: ref('stg_orders'), rows: [{order_id: 1, type: refund, amount: 10}]}]
    expect: {rows: [{order_id: 1, gross_amount: -10}]}
```

#### How do you deploy dbt to production?

On merge to main, run `dbt build` (or a job in dbt Cloud) with the production target from the orchestrator, store artifacts (manifest, run results) for the next slim CI comparison, generate docs, and alert on failures.

#### What are dbt unit tests?

Tests (dbt 1.8+) that define mock input rows for a model's refs and the expected output, run without real data, to verify complex SQL logic like case statements and window functions in CI.

#### How do you prevent breaking downstream consumers with dbt changes?

Model contracts (enforced column names and types), model versions for breaking changes, access levels for public models, exposures documenting dashboards that depend on models, and CI that builds downstream models (`state:modified+`).

#### How do you run dbt source freshness checks?

`dbt source freshness` in the production job (before building) or on a schedule, failing or warning when sources are older than thresholds, which prevents building on stale inputs.

#### How do you generate and publish dbt documentation?

Run `dbt docs generate` in the production pipeline and publish the static site (S3 with CloudFront, GitHub Pages, dbt Cloud) or push metadata to a catalog, so documentation matches what's deployed.

#### Design a CI/CD pipeline for a dbt project on Snowflake.

On pull requests: lint with SQLFluff, `dbt deps`, `dbt build --select state:modified+ --defer` against a PR-specific schema using a CI service user, post results, drop the schema at the end. On merge: deploy by triggering the production job (orchestrator or dbt Cloud), store artifacts for the next comparison, publish docs. Manage warehouses and roles with Terraform in the same or a separate pipeline.

<!-- challenge -->

A PR changes a column type in a model used by a BI tool, and the dashboard breaks after deploy. What would have stopped it?

<!-- solution -->

An enforced model contract: CI would fail when the column type changes. For an intended change, publish a new model version and let consumers migrate before removing the old one.

<!-- takeaways -->

- `dbt build` runs models and tests in order.
- Freshness checks guard inputs; docs ship with releases.
- Unit tests, contracts and versions protect consumers.

### CI/CD for Databricks, Airflow and warehouses

<!-- unit: Databricks -->

<!-- goals -->

- Set up CI/CD for Databricks with Asset Bundles and service principals.
- Test, deploy and run jobs from CI without teams colliding.

<!-- concept -->

Databricks Asset Bundles describe jobs, pipelines and their settings in files next to the code, with targets per environment. CI validates and tests them; CD deploys them as a service principal, so production never depends on a person's account.

Bundles also solve ownership: each bundle has a name and deployment path, so two teams deploying to one workspace don't overwrite each other's jobs.

<!-- example -->

```bash
databricks bundle validate -t staging
pytest tests/unit
databricks bundle deploy -t staging          # as the staging service principal
databricks bundle run -t staging smoke_test_job
databricks bundle deploy -t prod             # after approval
```

#### How do you set up CI/CD for Databricks?

Keep code and Databricks Asset Bundle definitions in Git; in CI run unit tests on local Spark, lint, and `databricks bundle validate`; in CD deploy with `databricks bundle deploy -t <target>` as a service principal authenticated with OAuth or workload identity federation, optionally running integration jobs in staging before production.

```yaml
- uses: databricks/setup-cli@main   # pin to a commit SHA in production
  with:
    version: ${{ vars.DATABRICKS_CLI_VERSION }}
- name: Validate and deploy bundle
  env:
    DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
    DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
    DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
  run: |
    databricks bundle validate -t prod
    databricks bundle deploy -t prod
```

#### Why deploy Databricks jobs as a service principal?

So production jobs don't depend on a person's account and permissions, access is limited to what the pipeline needs, and ownership survives people leaving.

#### How do you test Databricks code before deploying?

Unit tests on local Spark (or Databricks Connect), linting for patterns unsupported on serverless, `databricks bundle validate --strict`, deployment to a development or staging target with `mode: development`, and running integration jobs there.

#### How do you run a Databricks job from CI after deploying?

`databricks bundle run -t <target> <job_key>` (with `--no-wait` if you don't want CI to block), or trigger through the Jobs API; for production, often only on manual dispatch.

#### Design CI/CD for a PySpark lakehouse on Databricks and AWS.

CI on pull requests: secret scan, Ruff and custom Spark lint rules, unit tests on local Spark with Delta, end-to-end test on synthetic fixtures, bundle validation. CD on main: reuse CI as a gate (reusable workflow), then deploy AWS ingestion (SAM or Terraform) via OIDC and the Databricks bundle as a service principal, both in a protected production environment with concurrency set so deployments never overlap.

#### Two teams deploy to the same Databricks workspace and overwrite each other's jobs. How do you fix it?

Use bundles with distinct names and targets per team, deploy as each team's service principal with permissions limited to its resources, use development mode for personal deployments, and separate production deployments by repository and environment protections.

<!-- challenge -->

Production jobs fail after the engineer who created them left the company. What went wrong, and how do you fix it?

<!-- solution -->

The jobs ran as that person's identity, which was deactivated. Redeploy them through bundles with a service principal as owner and run-as identity, with permissions granted to the principal, not to people.

<!-- takeaways -->

- Bundles keep Databricks resources in code with targets.
- Deploy and run as service principals.
- Distinct bundle names and paths prevent collisions.

<!-- unit: Airflow, Glue and warehouses -->

<!-- goals -->

- Deploy Airflow DAGs and Glue jobs through CI/CD.
- Manage Snowflake and BigQuery changes as code.

<!-- concept -->

Every platform has its own deploy mechanics, but the pattern repeats: test in CI, build a versioned artifact, deploy it with infrastructure as code, keep secrets out of the artifact. For Airflow that's an image with DAGs; for Glue, scripts and wheels in versioned S3 paths; for warehouses, objects split between IaC for account-level things and migration tools or dbt for schemas.

Configuration and secrets follow the same rule everywhere: configuration from the environment, secrets from a manager.

<!-- example -->

| Platform | Artifact | Deploy with |
|---|---|---|
| Airflow | Image with DAGs and pinned providers | Helm / MWAA S3 sync |
| Glue | Script + wheel in `s3://artifacts/<sha>/` | Terraform / CDK |
| Snowflake | Roles, warehouses; schemas | Terraform; dbt or schemachange |
| BigQuery | Dataform release | Release configurations |

#### How do you deploy Airflow DAGs through CI/CD?

Run DAG integrity tests and unit tests in CI, build an image with DAGs and pinned dependencies (or sync DAG files to the DAG bucket for MWAA or Composer), deploy to staging, run smoke tests, then promote to production, with rollback by redeploying the previous image or commit.

#### How do you handle Airflow Variables and Connections in CI/CD?

Keep non-secret configuration in code or environment variables in the image, and secrets in a secrets backend; never create production connections by hand in the UI, so environments are reproducible.

#### How do you manage Snowflake changes through CI/CD?

Account objects (warehouses, roles, grants, integrations) with Terraform; schemas and tables with migration tools (schemachange, Flyway) or `CREATE OR ALTER` scripts; transformations with dbt; all deployed by a service user with key-pair or OAuth authentication from CI, tested first on a cloned database.

#### How do you deploy AWS Glue jobs through CI/CD?

Package shared code as a wheel, upload scripts and wheels to S3 with versioned paths, define jobs, triggers and catalog tables with CloudFormation, CDK or Terraform, and run tests locally with the Glue Docker image or Spark before deployment.

#### How do you deploy BigQuery or Dataform transformations?

Use Dataform's release configurations and workflow configurations with Git integration, or dbt with the BigQuery adapter, deploying through CI with a service account via workload identity federation.

<!-- challenge -->

Airflow connections are created by hand in each environment's UI, and staging points at production by mistake. What do you change?

<!-- solution -->

Define connections per environment in a secrets backend (or environment variables) managed as code, with names that are the same across environments and values that differ. Remove UI-created connections.

<!-- takeaways -->

- Same pattern everywhere: test, build, deploy as code.
- Version artifacts by commit.
- Configuration from the environment, secrets from a manager.

<!-- unit: Testing against cloud services -->

<!-- goals -->

- Test code that depends on cloud services without production access.
- Use service containers for integration tests.

<!-- concept -->

Code that calls S3, Glue or a database is hard to test in CI without touching real systems. Layers help: mock the service in unit tests, run local equivalents like LocalStack or a PostgreSQL container for integration tests, and keep a few tests against a real sandbox account.

Service containers in CI start those dependencies next to the job, so integration tests run on every PR with nothing to clean up.

<!-- example -->

```yaml
jobs:
  integration:
    runs-on: ubuntu-24.04
    services:
      postgres:
        image: postgres:16
        env: {POSTGRES_PASSWORD: test}
        ports: ["5432:5432"]
        options: --health-cmd "pg_isready" --health-interval 5s
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration --db-url postgresql://postgres:test@localhost:5432/postgres
```

#### How do you test pipelines that depend on cloud services in CI?

Mock services in unit tests (moto for AWS, LocalStack), use local equivalents (Spark with Delta, PostgreSQL containers, MinIO for S3) for integration tests, and run a small number of tests against a real sandbox account in staging.

#### What are service containers in GitHub Actions?

Docker containers started alongside a job (for example PostgreSQL or Redis) for integration tests, defined under `services:` with ports and health checks.

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_PASSWORD: postgres
    ports: ["5432:5432"]
    options: >-
      --health-cmd "pg_isready -U postgres"
      --health-interval 5s --health-retries 10
```

<!-- challenge -->

Integration tests write to a real S3 bucket in a shared dev account and sometimes delete each other's files. What do you change?

<!-- solution -->

Use moto or LocalStack for most S3 tests, and for the few real-service tests, use a unique prefix per CI run with automatic cleanup (and a lifecycle rule as backup).

<!-- takeaways -->

- Mock in unit tests; use local equivalents for integration.
- Service containers run dependencies next to the job.
- Isolate real-service tests per run.

<!-- stage: Operating safely -->

### Security of the delivery pipeline

<!-- unit: Secrets and leaks -->

<!-- goals -->

- Identify the main CI/CD security risks.
- Scan for secrets and respond when one leaks.

<!-- concept -->

A delivery pipeline holds the keys to production, which makes it a target. The most common failure is simple: a secret in code, history or logs. Scanning catches most of them before they leave a laptop.

When one leaks anyway, removing it from Git isn't enough, since copies may already exist. Revoke and rotate first, then clean up and check whether it was used.

<!-- example -->

```bash
gitleaks detect --source . --log-opts="--all"     # scan the full history
# leaked key? 1) revoke/rotate  2) check CloudTrail for use  3) purge history  4) add a pre-commit hook
```

#### What are the main security risks in CI/CD?

Leaked secrets in code or logs, overly broad credentials, compromised third-party actions or dependencies, untrusted code running with secrets (forks, `pull_request_target`), insecure self-hosted runners, and unreviewed changes reaching production.

#### What is secret scanning?

Detecting secrets in code and history with tools like gitleaks, TruffleHog or GitHub's built-in secret scanning and push protection, blocking commits and alerting on leaks so credentials can be revoked.

#### What should you do if a secret is committed?

Revoke and rotate it immediately (assume it's compromised), then remove it from history if needed; deleting the commit alone isn't enough because clones and caches may have it.

#### How do you handle sensitive data in CI logs?

Never print secrets or real data; rely on masking but don't trust it fully; use synthetic data in tests; review logs of public repositories; and restrict log retention.

<!-- challenge -->

A developer pushed a database password to a branch and force-pushed to remove it an hour later. Is the issue closed?

<!-- solution -->

No. Assume it's compromised: rotate the password, check database logs for access, and check whether forks, caches or CI logs captured it. Add secret scanning to pre-commit and push protection.

<!-- takeaways -->

- Leaked secrets are the most common CI/CD risk.
- Scan code and history continuously.
- Rotate first; deleting the commit isn't enough.

<!-- unit: Supply chain and least privilege -->

<!-- goals -->

- Apply least privilege and supply-chain controls to CI/CD.
- Protect CI configuration and runners from abuse.

<!-- concept -->

Everything the pipeline trusts can be a way in: dependencies, third-party actions, runners, and the CI configuration itself. Poisoned pipeline attacks change files that CI executes, so a malicious pull request can run code with the pipeline's permissions.

Least privilege limits the damage: read-only tokens by default, deploy permissions only in deploy jobs, production reachable only from protected branches with approvals. Self-hosted runners need extra isolation because they live inside your network.

<!-- example -->

```text
default GITHUB_TOKEN:       contents: read
deploy job:                 id-token: write, environment: production (approvers)
cloud role trust:           repo:acme/lake:environment:production only
.github/workflows/**:       CODEOWNERS = platform team
self-hosted runners:        ephemeral, no access from fork PRs
```

#### What is software supply chain security?

Protecting the path from source to production: pinned and verified dependencies and actions, dependency vulnerability scanning (Dependabot, pip-audit), SBOMs, signed artifacts and provenance (SLSA, Sigstore), and least-privilege build systems.

#### What is least privilege in CI/CD?

Each workflow and job gets only the permissions it needs: read-only tokens by default, deployment credentials only in deploy jobs, environment-scoped secrets, and cloud roles restricted to specific resources and branches.

#### How do you protect production from unauthorized deployments?

Branch protection on main, required reviews, environment protection rules with approvers, OIDC trust policies restricted to the production environment, and audit logs of deployments.

#### Why are self-hosted runners risky, and how do you secure them?

They run arbitrary workflow code inside your network; a malicious PR could attack internal systems. Use ephemeral runners (one job per runner), never run untrusted fork code on them, isolate networks, and restrict which repositories can use them.

#### What is a "poisoned pipeline execution" attack?

An attacker modifies CI configuration or files executed by CI (scripts, Makefiles) in a pull request so that the pipeline runs malicious code with access to secrets. Mitigate with least-privilege tokens, no secrets for untrusted PRs, and required reviews for CI changes.

#### How do you protect CI configuration itself?

Require code owner review for `.github/workflows/`, restrict who can modify environments and secrets, pin actions, and audit changes to workflows.

<!-- challenge -->

Any developer can edit workflow files, and the deploy job's role can deploy to production from any branch. Name three controls to add.

<!-- solution -->

CODEOWNERS review for `.github/workflows/`, an OIDC trust policy restricted to the production environment on main, and environment protection with required reviewers. Default tokens read-only.

<!-- takeaways -->

- Dependencies, actions, runners and CI config are attack surfaces.
- Least privilege per job and environment.
- Protect workflow files with code owners.

### Operations, monitoring and DataOps

<!-- unit: After the deployment -->

<!-- goals -->

- Check that a deployment didn't break data.
- Correlate incidents with deployments and practice failure.

<!-- concept -->

A green pipeline only says the code deployed. Whether the data is still right shows up later: in the next run's quality checks, freshness, volumes and the dashboards people use. Watching those signals after each deployment closes the loop.

When something does break, a deployment log answers the first question, what changed, and chaos testing in staging shows how pipelines behave when things fail before it happens for real.

<!-- example -->

```text
deploy 14:02  etl v2.4.1 (PR #318, approved by @ana)
14:05  smoke test: job registered, 1-day run OK
06:10  next run: row count -38% vs 7-day avg  ← alert
→ diff v2.4.0..v2.4.1 shows a changed join in orders_enriched
```

#### What should happen after a deployment?

Smoke tests, monitoring of job runs and data quality checks on the next run, comparison of key metrics with previous runs, and notifications to the team; rollback quickly if checks fail.

#### How do you know whether a data deployment broke something?

Data quality tests and observability (freshness, volume, schema and distribution changes), pipeline failure alerts, reconciliation with sources, and dashboards of key metrics compared with their recent history.

#### How do you correlate a data incident with a deployment?

Compare incident start time with deployment history, check which models or jobs changed (Git diff between versions), review lineage for affected tables, and look at data quality metrics before and after.

#### What is a deployment log, and why keep one?

A record of what version was deployed where and when, by whom and with which approvals (GitHub deployments, environment history, release notes), which is essential when correlating incidents with changes.

#### What is chaos testing for data pipelines?

Deliberately introducing failures in a test environment (killed jobs, missing files, delayed sources, schema changes) to verify that retries, alerts, idempotency and recovery procedures work as expected.

<!-- challenge -->

Revenue dropped 20% on a dashboard this morning. How do you check whether a deployment caused it?

<!-- solution -->

Compare the drop's start time with the deployment log, list models and jobs changed in those deployments (Git diff), check lineage from them to the revenue model, and run the previous version on the same inputs to compare.

<!-- takeaways -->

- Watch data quality after each deployment.
- A deployment log answers "what changed?".
- Practice failures in staging with chaos tests.

<!-- unit: Releases and communication -->

<!-- goals -->

- Document releases and communicate data changes to consumers.
- Apply GitOps and measure delivery success.

<!-- concept -->

Consumers can't read your pull requests, so changes need to reach them in their terms: what changes, when, and what they must do. Changelogs, release notes and deprecation notices with dates do that, generated from commit messages where possible.

GitOps makes Git the record of what should be deployed, with agents applying it. Success is measured not only in deployment frequency but in fewer incidents and faster recovery.

<!-- example -->

```markdown
## Release 3.0.0 – 2026-10-20
- **Breaking:** `fct_orders.amount` renamed to `gross_amount`. Old name available until 2026-11-30.
- Added `refund_amount` (nullable).
- Fixed: test customers excluded from revenue.
```

#### What is GitOps?

Using Git as the single source of truth for desired state, with automated agents applying it to the environment (Argo CD, Flux for Kubernetes), so every change is a commit and the system converges to what's in the repository.

#### How do you document a release?

Pull request descriptions, a changelog (often generated from conventional commits), release notes for consumers describing data impact (new columns, changed definitions, backfills), and ADRs for significant decisions.

#### How do you communicate data changes to consumers?

Through changelogs and release notes, deprecation notices with timelines, catalog updates, contract version bumps, and direct communication for breaking changes or historical restatements.

#### How do you measure the success of CI/CD in a data team?

DORA metrics (deployment frequency, lead time, change failure rate, time to restore), number of data incidents caused by changes, time spent on manual deployments, and CI duration and cost.

<!-- challenge -->

Analysts keep being surprised by column changes. What lightweight process do you introduce?

<!-- solution -->

Generate a changelog from conventional commits for each release, publish it in the data catalog and a channel analysts follow, and announce breaking changes with a deprecation period before removal.

<!-- takeaways -->

- Changelogs and notes translate changes for consumers.
- Deprecations need dates and alternatives.
- Measure delivery speed and stability.

<!-- unit: Fast and affordable CI -->

<!-- goals -->

- Keep CI fast as a project grows.
- Control CI costs without dropping checks.

<!-- concept -->

CI only works if people use it. When it takes too long, developers batch changes, skip checks or merge around it, and the safety net disappears. Speed comes from doing less work per run: only what changed, in parallel, with cached dependencies.

The same moves lower cost, together with cancelling superseded runs and reserving heavy jobs for merges or schedules.

<!-- example -->

```yaml
concurrency: {group: "ci-${{ github.ref }}", cancel-in-progress: true}
jobs:
  unit:   {runs-on: ubuntu-24.04, steps: [...]}        # every PR
  dbt:    {if: "contains(needs.changes.outputs.paths, 'models')", ...}
  e2e:    {if: "github.event_name == 'schedule'", ...}  # nightly only
```

#### How do you keep CI fast as the project grows?

Test only what changed (path filters, slim CI), parallelize jobs and tests, cache dependencies, use smaller synthetic data, split slow integration tests to run on main or nightly, and use larger runners where justified.

#### How do you control CI costs?

Cancel superseded runs, avoid running heavy jobs on every commit, cache dependencies, use slim CI against warehouses, auto-drop CI schemas, set timeouts on jobs, and watch minutes and warehouse spend per repository.

#### Your CI takes 45 minutes and developers bypass it. What do you do?

Profile the pipeline, parallelize independent jobs, cache dependencies, run only affected tests (path filters, slim CI), shrink test data, move slow end-to-end tests to the merge queue or main, and set a target (for example under 10 minutes for PR checks).

<!-- challenge -->

CI costs doubled after the team grew. Most minutes come from runs on commits that are pushed again minutes later. What do you change first?

<!-- solution -->

Add a `concurrency` group per branch with `cancel-in-progress: true`, so new pushes cancel the outdated run. Then cache dependencies and run heavy suites only when relevant paths change.

<!-- takeaways -->

- Slow CI gets bypassed; speed is safety.
- Run only what changed, in parallel, with caches.
- Cancel superseded runs to save cost.

<!-- stage: Putting it together -->

### Scenarios

<!-- unit: Recovering from a bad deployment -->

<!-- goals -->

- Recover a production table after a bad deployment.
- Identify which process gaps let the change through.

<!-- concept -->

Incident questions test two things: whether you restore service calmly, and whether you learn from it. Recovery comes first: roll back the code, restore or recompute the data, tell consumers. Then the review looks at the pipeline: which test, review or gate should have stopped this, and how to add it. Blameless reviews focus on the system, not the person.

<!-- example -->

```text
1. Stop the bleeding: pause downstream jobs, notify consumers
2. Roll back code (previous artifact); restore table (time travel) or rerun old logic
3. Verify: row counts, key metrics vs before the deploy
4. Review: missing regression test? missing data test? review skipped?
5. Add the check to CI; document in the postmortem
```

#### A deployment broke a production table. What should your process have caught, and how do you recover?

Recover first: roll back code, restore the table with time travel or rerun the old logic for affected partitions, and inform consumers. Then improve the pipeline: add a test for the failure case, a contract or schema check, a regression comparison in CI, or write-audit-publish so bad data isn't exposed.

<!-- challenge -->

The postmortem shows the bug would have been caught by comparing outputs before and after the change. How do you make that comparison part of every relevant PR?

<!-- solution -->

Add a regression step to CI for changed models: build them in the PR schema on the same inputs and diff key aggregates and row counts against production, posting the results as a PR comment and failing on unexpected differences.

<!-- takeaways -->

- Recover first: code, data, communication.
- Find the missing gate, not someone to blame.
- Turn every lesson into an automated check.

<!-- unit: Moving from manual to automated delivery -->

<!-- goals -->

- Plan a migration from manual deployments to CI/CD.
- Sequence the steps so value arrives early.

<!-- concept -->

Teams rarely go from manual deploys to full CI/CD in one step, and they shouldn't try. The path is incremental: first get everything into Git, then add checks that run on every change, then automate deployment to a non-production environment, and finally to production with approvals. Each step pays off on its own and builds trust for the next.

<!-- example -->

| Step | Outcome |
|---|---|
| 1. Everything in Git | History, reviews, no lost scripts |
| 2. CI: lint + unit tests | Fewer broken changes |
| 3. Automated deploy to staging | Repeatable deployments |
| 4. Prod deploy with approval | No manual copying, audit trail |
| 5. Data tests and monitoring | Problems caught before users |

#### How would you migrate from manual deployments to CI/CD?

Put everything in Git (code, configuration, infrastructure), add CI with linting and tests on pull requests, automate deployment to a staging environment, add smoke tests and approvals, then automate production deployment with the same artifacts, and remove manual access to production gradually.

<!-- challenge -->

Some engineers worry that automation will slow them down. How do you show value in the first two weeks?

<!-- solution -->

Start with what costs them time today: put scripts in Git with a basic CI that runs linting and a few tests in minutes, and automate one painful deployment. Show the saved time and the first bug CI caught.

<!-- takeaways -->

- Migrate incrementally: Git, CI, staging deploys, prod deploys.
- Each step should pay off by itself.
- Show early wins to build trust.
