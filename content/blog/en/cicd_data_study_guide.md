## CI/CD for Data Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![CI/CD for data study guide: about 200 questions](../../images/cicd_data_study_guide_title_img.png)

About 200 interview-style questions on CI/CD and automation for data platforms: Git workflows, testing strategies for pipelines and data, code quality, environments, infrastructure as code, deployment patterns, GitHub Actions in depth, CI/CD for dbt, Databricks, Airflow and warehouses, security of the delivery pipeline, and operations. Examples use GitHub Actions, with notes on GitLab CI and Azure DevOps. Open a question to see its answer, or use the filter to search the whole guide.

<!-- QA -->

### Fundamentals

#### What is CI/CD?

Continuous integration (CI) means merging code changes frequently into a shared branch, with automated builds and tests on every change. Continuous delivery (CD) keeps the code always deployable and automates releases to environments; continuous deployment goes further and deploys every passing change to production automatically.

#### Why does CI/CD matter for data teams?

Data pipelines are software: without automation, changes are deployed by hand, break production tables, and are hard to roll back. CI/CD catches errors before they reach consumers, makes deployments repeatable and auditable, and lets teams change pipelines quickly and safely.

#### What is DataOps?

Applying DevOps and agile practices to data: version control, automated testing (code and data), CI/CD, environment management, monitoring and observability, and collaboration between data engineers, analysts and operations, with the goal of reliable data delivered quickly.

#### How is CI/CD for data different from CI/CD for applications?

Data pipelines have state (tables, history, schemas) that must be migrated, not just replaced; tests need representative data; correctness depends on the data as much as the code; deployments can trigger expensive recomputations; and rollback of data is harder than rollback of code.

#### What should be automated in a data CI/CD pipeline?

Linting and formatting, unit tests, building artifacts (wheels, images, dbt manifests), static validation (SQL compilation, bundle or DAG validation), integration and data tests against test data, security scans, infrastructure changes, deployments to each environment, smoke tests after deployment, and notifications.

#### What is the difference between continuous delivery and continuous deployment?

With continuous delivery, every change is deployable and production deployment is one click or approval away. With continuous deployment, every change that passes the pipeline goes to production automatically, without a manual step.

#### What is "everything as code"?

Defining pipelines, transformations, infrastructure, permissions, schedules, data quality rules and even documentation in version-controlled files, so every change is reviewed, tested, reproducible and traceable.

#### What are the benefits of small, frequent deployments?

Each change is easier to review, test and understand, failures are easier to diagnose and roll back, and feedback from production comes sooner. Large, infrequent releases bundle many risks together.

#### What is a deployment pipeline?

The automated sequence that takes a commit to production: build, test, package, deploy to lower environments, run checks, approve, deploy to production, verify. It's the path every change follows.

#### What are DORA metrics?

Four measures of delivery performance: deployment frequency, lead time for changes, change failure rate and time to restore service. They apply to data teams too and help measure whether CI/CD improves delivery.

#### What is the difference between a build, a test and a deployment stage?

The build stage produces artifacts (packages, images, compiled models); the test stage verifies them (unit, integration, data tests); the deployment stage installs them into an environment and runs post-deployment checks. Separating them makes failures easy to locate.

#### What is "shift left" in data quality?

Catching problems as early as possible: in the IDE (linters), at commit (pre-commit hooks), in pull requests (CI tests, contract checks), rather than in production dashboards where they're expensive and visible.

#### What is a "release" versus a "deployment"?

A deployment installs a version into an environment; a release makes new functionality available to users. With feature flags or blue-green switches, you can deploy without releasing and release without redeploying.

#### Why should pipelines be deterministic?

Given the same code, configuration and inputs, a deterministic pipeline produces the same outputs, which makes testing, debugging, backfills and audits possible. Avoid hidden dependencies on current time, random seeds or unpinned versions.

#### What does "you build it, you run it" mean for data teams?

The team that builds a pipeline also operates it: receives its alerts, fixes its incidents and improves its reliability, which creates strong incentives for good tests, monitoring and automation.

### Version control and Git workflows

#### Why must data code be in Git?

Version control gives history (who changed what and why), collaboration through branches and pull requests, the ability to revert, a single source of truth for deployments, and the trigger for CI/CD.

#### What belongs in a data repository?

Pipeline and transformation code (Python, SQL, dbt models), tests and fixtures, configuration per environment (without secrets), infrastructure as code, orchestration definitions (DAGs, bundles, job specs), CI/CD workflows, documentation and data contracts.

#### What should never be committed?

Secrets (passwords, keys, tokens), real personal or sensitive data, large data files, local environment files and build outputs. Use `.gitignore`, secret scanning and pre-commit hooks to prevent accidents.

#### What is trunk-based development?

A workflow where developers integrate small changes into the main branch frequently (at least daily), using short-lived feature branches and feature flags, with the main branch always releasable. It suits CI/CD well.

#### What is GitFlow, and why is it less popular now?

A branching model with long-lived `develop` and `main` branches plus feature, release and hotfix branches. It adds ceremony and merge pain; most teams practicing CI/CD prefer trunk-based development or a simple feature-branch flow.

#### What is a pull request (merge request), and what should a good one include?

A request to merge a branch, with a description of what and why, linked ticket, testing done, impact on data (schemas, backfills, consumers), screenshots or query results if relevant, and passing checks. It's the place for review and automated validation.

#### What should reviewers look for in data code reviews?

Correctness of logic and joins (grain, fan-out), handling of nulls and duplicates, idempotency, performance (partition filters, full scans), tests covering the change, schema and contract changes, backfill needs, security (no secrets, proper permissions) and readability.

#### What are branch protection rules?

Repository settings that prevent direct pushes to important branches and require pull requests, passing status checks, a number of approvals, code owner reviews, up-to-date branches or signed commits before merging.

#### What is a CODEOWNERS file?

A file mapping paths to responsible teams or people, who are automatically requested as reviewers and can be required to approve changes to their areas, for example `/models/finance/ @org/finance-data`.

#### What is semantic versioning, and does it apply to data?

Versioning as MAJOR.MINOR.PATCH, where major versions signal breaking changes. It applies to libraries and also to data products and contracts: a removed column or changed meaning is a major version, a new optional column a minor one.

#### What are conventional commits?

A commit message convention (`feat:`, `fix:`, `chore:`, `docs:`, `feat!:` for breaking changes) that makes history readable and lets tools generate changelogs and version numbers automatically.

#### How do you handle hotfixes in trunk-based development?

Fix on a short-lived branch from main, merge through the normal (possibly expedited) pipeline and deploy; if a release branch is in production, cherry-pick the fix there too. Avoid patching production by hand.

#### What is a monorepo versus a polyrepo for data?

A monorepo keeps all pipelines, models and infrastructure in one repository (easy cross-cutting changes, shared tooling, needs path-based CI); a polyrepo splits them by domain or component (clear ownership and access, harder coordination). Both work with good CI.

#### How do you keep feature branches short-lived?

Break work into small, independently mergeable changes, merge behind feature flags or disabled schedules, rebase often on main, and aim to merge within a day or two.

#### What are Git tags used for in deployments?

Marking release points (`v1.4.0`) that trigger release workflows, identify exactly what was deployed and allow rollback by redeploying a previous tag.

#### How should notebooks be handled in Git?

Store them as source files (Databricks `.py` format, Jupytext) rather than JSON with outputs, strip outputs before commit, keep logic in importable modules and notebooks thin, so diffs are reviewable.

#### What is a `.gitattributes` or LFS needed for in data repos?

Git LFS stores large binary files (small reference datasets, test fixtures, images) outside the normal Git history; large production data shouldn't be in Git at all.

### Testing strategy for data

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

#### What are data tests, and how do they differ from code tests?

Code tests check that logic behaves as expected on controlled inputs; data tests check that real data meets expectations (uniqueness, not null, accepted values, referential integrity, freshness, volume). Both are needed: correct code can still produce wrong data from bad inputs.

#### What is test data management?

Creating and maintaining datasets for tests: small synthetic fixtures for unit tests, anonymized or synthetic samples for integration tests, and production-like data (masked) for performance tests, versioned with the code where possible.

#### Why prefer synthetic data in CI?

It's safe (no personal data), small (fast tests), deterministic, and can include edge cases deliberately (nulls, duplicates, late records, unicode, extreme values) that might be rare in real samples.

#### What is a contract test for data?

A test verifying that a producer's output matches the agreed schema and semantics of a data contract (columns, types, nullability, allowed values), run in the producer's CI so breaking changes fail before release.

#### What is regression testing for data pipelines?

Comparing outputs of the new version with the previous version on the same input (row counts, aggregates, row-level diffs), so unintended changes are detected; tools include `datacompy`, dbt audit helper and data-diff approaches.

#### What is a smoke test after deployment?

A quick check right after deploying that the system works: jobs are registered, a small run succeeds, key tables are readable, dashboards load. It catches configuration and permission errors early.

#### How do you test SQL transformations?

Compile and parse SQL in CI, run models against small seeded inputs in a test schema and compare to expected outputs (dbt unit tests), apply data tests on results, and lint SQL for style and anti-patterns.

#### How do you test Airflow DAGs?

Load all DAGs with `DagBag` and fail on import errors, check conventions (owners, retries, tags, no cycles), unit test the Python logic used by tasks, and run integration tests in a staging Airflow.

#### What is property-based testing, and is it useful for data?

Generating many random inputs that satisfy constraints and checking properties that should always hold (for example, deduplication output has unique keys and is a subset of input). Tools like Hypothesis find edge cases hand-written tests miss.

#### What is mutation testing?

Introducing small changes to the code (mutants) and checking whether tests fail; surviving mutants reveal weak tests. It's rarely used in data teams but useful for critical libraries.

#### How do you keep test suites fast?

Use small fixtures, share one SparkSession per test session, mark slow tests and run them separately or only on main, parallelize with `pytest-xdist`, cache dependencies in CI, and avoid hitting real cloud services in unit tests.

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

#### What edge cases should data pipeline tests cover?

Empty inputs, nulls in keys and values, duplicates, late and out-of-order records, schema changes (extra or missing columns), invalid formats, time zones and daylight saving, very large values, special characters, and reruns of the same input (idempotency).

#### How do you test idempotency?

Run the pipeline step twice on the same input and assert the output is identical (same row count, no duplicates, same aggregates).

#### How do you test schema evolution handling?

Feed fixtures with an added column, a removed column and a changed type, and assert the pipeline behaves as designed (accepts additive changes, fails loudly or quarantines incompatible ones).

#### What are "golden files" or snapshot tests?

Stored expected outputs (CSV, JSON, Parquet) that test results are compared against; when outputs change intentionally, the golden files are updated in the same pull request, making changes visible in review.

#### How do you test performance in CI?

Usually not on every PR, but with periodic benchmarks on representative data volumes, tracking runtime, shuffle sizes and cost, and alerting on regressions; lint rules can catch known performance anti-patterns cheaply.

### Code quality and static checks

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

#### What are custom lint rules for data code?

Project-specific checks for anti-patterns, such as `collect()` on large DataFrames, Python UDFs where built-ins exist, `SELECT *` in production models, hard-coded paths or credentials, missing partition filters, or `withColumn` in loops.

#### What is static analysis for security?

Tools like Bandit (Python security issues), Semgrep (custom rules), Checkov or tfsec (infrastructure misconfigurations) and dependency scanners that find vulnerabilities and risky patterns before deployment.

#### What is code coverage, and how should you use it?

The percentage of code executed by tests. It's a useful signal for untested areas but not a goal in itself; aim for meaningful tests of critical logic rather than a number, and watch coverage trends on changed files.

#### How do you check dbt projects in CI?

`dbt deps`, `dbt parse` or `compile` to catch syntax and reference errors, SQLFluff linting, dbt project evaluator for conventions, and `dbt build` on modified models with tests in a CI schema.

#### Why add type hints to data code?

They document interfaces, let type checkers catch mistakes (wrong argument types, `None` handling) before runtime, and improve IDE support, which matters for shared libraries used by many pipelines.

#### What is the dbt project evaluator?

A dbt package that checks a project against best practices (model naming, layering, direct source references from marts, missing tests or documentation, fan-out patterns) and can fail CI on violations.

#### How do you check YAML and configuration files?

With schema validation (JSON Schema for configs, `databricks bundle validate`, `actionlint` for GitHub workflows), yamllint for syntax and style, and tests that load every config file the pipeline uses.

#### What is actionlint?

A static checker for GitHub Actions workflow files that catches syntax errors, invalid expressions, unknown inputs and shell script issues before workflows run.

### Environments and configuration

#### Which environments does a data platform need?

At least development (individual or shared sandboxes), a staging or pre-production environment mirroring production, and production. Some add test/QA environments or ephemeral environments per pull request.

#### Why separate environments by account, workspace or catalog?

Isolation limits the blast radius of mistakes, allows different permissions (developers can't write production), separates costs, and makes promotion explicit.

#### What is environment parity?

Keeping environments as similar as possible (same code, versions, configurations, infrastructure templates) so tests in staging predict production behavior; differences should be limited to scale, data and credentials.

#### How do you manage configuration per environment?

With configuration files or variables per environment (paths, catalogs, cluster sizes, schedules) injected at deploy time, keeping the code identical; secrets come from a secrets manager, never from files in the repo.

#### What is the twelve-factor principle about configuration?

Store configuration in the environment (variables), not in code, so the same build artifact runs in every environment with different settings.

#### What are ephemeral environments?

Short-lived environments created automatically for a pull request (a schema, a branch of the catalog, a clone of tables, a deployed copy of jobs) and destroyed after merge, letting reviewers test changes in isolation.

#### How do you provide test data in staging?

Copy or clone production data with masking or anonymization of personal data, sample to reduce cost, use zero-copy clones (Snowflake, Delta shallow clones) where available, or generate synthetic data at production-like scale.

#### What is data versioning, and why is it useful in CI/CD?

Versioning datasets like code (lakeFS branches, Project Nessie for Iceberg, Delta and Iceberg snapshots, dbt snapshots) to reproduce runs, test changes on isolated branches of data and roll back bad writes.

#### What is the write-audit-publish (WAP) pattern?

Writing new data to a staging location or branch, auditing it with quality checks, and only then publishing it (swap, merge or fast-forward) so consumers never see bad data. Iceberg branches, lakeFS and table swaps implement it.

#### How do you name resources across environments?

With a consistent scheme that includes the environment (`sales_prod`, `catalog_dev`, `dbt_ci_pr_123`), derived from configuration rather than hard-coded, so code never accidentally points to production from dev.

#### How do developers work without touching production data?

Personal schemas or catalogs, development targets that read from production read-only (or from clones) and write only to dev, sampled or masked data, and permissions that prevent writes to production from developer identities.

#### What is promotion between environments?

Moving the same artifact from dev to staging to production after checks pass at each stage, rather than rebuilding, with approvals for production.

#### Should staging use production data?

Ideally staging uses production-like data (cloned, sampled or masked) to catch real-world issues, with strict controls on personal data; purely synthetic staging can miss problems that only real data reveals.

### Infrastructure as code

#### What is infrastructure as code (IaC)?

Defining cloud resources (storage, compute, networks, permissions, catalogs, jobs) in declarative code that is versioned, reviewed and applied automatically, instead of creating them by hand in consoles.

#### Which IaC tools are common for data platforms?

Terraform/OpenTofu (multi-cloud), AWS CloudFormation, CDK and SAM, Azure Bicep, Pulumi, and platform-specific tools such as Databricks Asset Bundles, Snowflake's Terraform provider and Kubernetes manifests with Helm.

#### What is the plan/apply workflow in Terraform?

`terraform plan` shows the changes that would be made; reviewers check the plan in the pull request; `terraform apply` executes it after approval, typically from CI with remote state and locking.

#### What is Terraform state, and how should it be stored?

A file mapping configuration to real resources. Store it remotely (S3 with locking, Terraform Cloud, Azure Storage) with encryption and access control, never in Git, and separate state per environment.

#### What is configuration drift?

Differences between the declared infrastructure and reality, caused by manual changes. Detect it with scheduled `terraform plan` runs or drift detection services, and fix by updating code or reverting manual changes.

#### What is immutable infrastructure?

Replacing components with new versions instead of modifying them in place (new container images, new clusters), which makes deployments predictable and rollbacks simple.

#### How do you structure IaC for multiple environments?

Reusable modules for common components, with environment-specific variables or workspaces (dev, staging, prod), separate state per environment, and the same modules promoted through environments.

#### How do you review infrastructure changes safely?

Post the `terraform plan` (or CDK diff, CloudFormation change set) as a pull request comment, require reviews from owners of affected resources, use policy checks (Checkov, OPA/Conftest, Sentinel), and apply only from CI.

#### What is policy as code?

Writing organizational rules (encryption required, no public buckets, tags mandatory, approved regions) as code evaluated automatically in CI or at deployment, for example with Open Policy Agent, Checkov or cloud-native policy services.

#### How do you manage data platform permissions as code?

Define roles, grants and catalog permissions in Terraform or platform tools (Snowflake provider, Databricks Terraform provider, Unity Catalog grants in bundles), reviewed in pull requests, so access changes are auditable and reversible.

### Packaging and artifacts

#### What is a build artifact in data projects?

The versioned output of a build that gets deployed: a Python wheel with pipeline code, a Docker image, a JAR, a compiled dbt manifest, a bundle, or a zip of SQL scripts. Build once, deploy the same artifact everywhere.

#### Why "build once, deploy many"?

Rebuilding for each environment can produce different artifacts (dependency changes, timing), so what was tested isn't what's deployed. Building one artifact and promoting it guarantees consistency.

#### How do you version artifacts?

With semantic versions for libraries, and commit SHAs or build numbers for applications (`0.2.145+g1a2b3c4`), stamped at build time so every deployment is traceable to a commit.

#### Where do you store artifacts?

In artifact repositories and registries: PyPI-compatible repositories (CodeArtifact, Artifactory, GitHub Packages), container registries (ECR, ACR, GHCR), S3 buckets for scripts, or platform stores (Databricks workspace files and volumes).

#### How do you manage Python dependencies reproducibly?

Pin exact versions with lock files (`uv.lock`, `poetry.lock`, `pip-tools` requirements), separate runtime and dev dependencies, build in clean environments, and update dependencies deliberately (Dependabot or Renovate with tests).

#### Why use containers for data pipelines?

Containers package code with exact dependencies and OS libraries, making runs identical across laptops, CI and production, and fit orchestrators like Kubernetes, ECS, Airflow's KubernetesPodOperator and Cloud Run.

#### How do you stamp a version into a Python package in CI?

Derive it from Git (setuptools-scm, `git describe`) or set it explicitly in CI from a run number and short SHA, so every artifact maps to a commit; avoid reusing the same version for different code.

#### What is an SBOM?

A software bill of materials listing every component and dependency (with versions) in an artifact, generated in CI (Syft, CycloneDX) to track vulnerabilities and licenses.

#### Why scan container images in CI?

Base images and dependencies contain known vulnerabilities; scanners (Trivy, Grype, registry scanning) find them before deployment, and policies can block critical issues.

### Deployment strategies

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

#### How do you roll back a data deployment?

Redeploy the previous code artifact, and for data either restore tables with time travel or snapshots, switch views back to the previous version (blue-green), or rerun the old logic for affected partitions. Plan rollback before deploying risky changes.

#### Why are database schema changes risky in deployments?

They can break running code, lock tables, require data migration and are hard to reverse. Use backward-compatible changes (expand and contract), migrations tested on clones, and deploy schema and code in compatible steps.

#### What is the expand-and-contract pattern?

Making schema changes in phases: expand (add new column or table, keep old), migrate (write both, backfill, switch readers), contract (remove the old column once nobody uses it). Each step is backward compatible.

#### What are database migration tools?

Tools that apply versioned, ordered schema changes and track which have run: Flyway, Liquibase, Alembic (SQLAlchemy), Sqitch, schemachange (Snowflake), and dbt for transformation-managed objects.

#### How do you handle backfills in deployments?

Treat them as part of the release plan: estimate cost and duration, parameterize pipelines by date range, run in controlled batches (often off-peak), validate outputs, and communicate to consumers when historical data changes.

#### How do you deploy a change to a heavily used table without downtime?

Build the new version in parallel (new table or version), validate it, then switch atomically (swap, rename or update a view), and keep the old version for rollback; avoid in-place rewrites while consumers read.

#### How do you deploy a change that requires recomputing history?

Plan a backfill: deploy the new logic writing to a new table or version, recompute history in batches, validate against the old outputs, switch consumers, and communicate restated numbers, rather than overwriting history in place without checks.

#### What is a deployment freeze, and when is it appropriate?

A period with no production deployments, for example during financial closing or peak sales, to reduce risk; it's better to make deployments safe and routine, keeping freezes short and for genuine high-risk periods.

#### How do you deploy streaming job changes?

Check state compatibility, stop the job gracefully (savepoint or checkpoint), deploy the new version from the same checkpoint if compatible, or start a new job with a new checkpoint and a backfill plan; run old and new in parallel for critical streams.

### GitHub Actions in depth

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

#### What are secrets and variables in GitHub Actions?

Secrets are encrypted values (tokens, passwords) available to workflows and masked in logs; variables are non-sensitive configuration values. Both can be defined at organization, repository or environment level and are referenced through the `secrets` and `vars` contexts.

#### Why should identifying values be secrets in public repositories?

Workflow logs of public repositories are public, and only secrets are masked. Hostnames, account IDs, bucket names or emails stored as plain variables can leak in logs, so treat them as secrets when the repository is public.

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

#### What are reusable workflows?

Workflows triggered with `workflow_call` that other workflows invoke with `uses: ./.github/workflows/ci.yml` (or from another repository), passing inputs and secrets, so CI logic is defined once and reused, for example running the full CI as a gate inside the CD workflow.

#### What are composite actions?

Custom actions defined with `runs: using: composite` that bundle several steps (setup, install, configure) into one reusable step, stored in the repository or a shared repository.

#### What does `concurrency` do?

It groups runs by a key and limits them to one at a time; with `cancel-in-progress: true` a new run cancels the older one (good for PR CI), with `false` new runs wait (essential for deployments so two never overlap).

```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

#### How do you run scheduled jobs in GitHub Actions?

With `on: schedule: - cron: "0 5 * * *"` (UTC). It's handy for nightly drift checks, dependency audits or small data jobs, but not a replacement for a data orchestrator: schedules can be delayed and are disabled on inactive repositories.

#### What is `workflow_dispatch` used for?

Manual triggers with optional typed inputs, for example deploying a specific version, running a backfill for a date range or starting a production job after deployment.

#### How do you make jobs conditional?

With `if:` expressions on jobs or steps, using contexts like `github.ref`, `github.event_name`, `needs.<job>.result`, variables (`vars.DEPLOY_AWS == 'true'`) or functions like `success()`, `failure()` and `always()`.

#### Why pin third-party actions to a commit SHA?

Tags like `v4` can be moved, and a compromised action could exfiltrate secrets. Pinning to a full commit SHA (with the version as a comment) guarantees the exact code that runs; Dependabot can keep pinned actions updated.

#### What is the difference between `pull_request` and `pull_request_target`?

`pull_request` runs in the context of the merge commit with read-only token and no secrets for forks, which is safe. `pull_request_target` runs in the base repository context with secrets; checking out and running untrusted PR code in it is a well-known security hole.

#### How do you add a manual approval before production?

Configure the production environment with required reviewers; jobs referencing that environment pause until an approved reviewer approves the deployment in the GitHub UI.

#### What is a merge queue?

A GitHub feature that tests pull requests together with the latest main (and with each other) before merging them in order, preventing "green PR, broken main" when several PRs merge close together; CI must also run on the `merge_group` event.

#### How do you see test results nicely in GitHub Actions?

Upload JUnit XML reports as artifacts and publish them with a test reporter action, write a job summary to `$GITHUB_STEP_SUMMARY` (Markdown), or comment results on the pull request.

#### What are GitHub-hosted larger runners and self-hosted runners used for in data teams?

Larger runners help with heavy builds or Spark tests; self-hosted runners in your cloud network can reach private databases or warehouses for integration tests and avoid exposing them publicly, but they must be hardened and isolated (ephemeral runners are recommended).

#### How does GitHub Actions compare with GitLab CI and Azure DevOps?

All define pipelines in YAML with stages or jobs, runners/agents, variables and secrets, environments and approvals. GitLab CI uses `.gitlab-ci.yml` with stages and built-in registry; Azure DevOps uses `azure-pipelines.yml` with stages, service connections and tight Azure integration. Concepts transfer directly.

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

#### How do you set default shell options and working directory?

With `defaults: run:` at workflow or job level, for example `shell: bash` and `working-directory: ./dbt`, so every `run` step uses them; bash steps run with `-e` (exit on error) by default in GitHub Actions.

#### How do you write a job summary?

Append Markdown to the file in `$GITHUB_STEP_SUMMARY` (for example a table of row counts or a test report), which appears on the run's summary page.

#### How do you add timeouts to jobs?

With `timeout-minutes` on jobs (and steps), so a hung job doesn't consume runner minutes for hours; the default job timeout is 360 minutes.

#### What are expressions and contexts in GitHub Actions?

Expressions are written as `${{ ... }}` in workflow YAML and access contexts like `github` (event and repository data), `env`, `vars`, `secrets`, `matrix`, `needs`, `steps`, `runner` and `inputs`, with functions like `contains`, `startsWith`, `format`, `hashFiles` and status checks.

#### How do you run a job only on the main branch after a push?

`if: github.ref == 'refs/heads/main' && github.event_name == 'push'`, which prevents deployments from pull requests or other branches.

#### How do you deploy only when a repository variable is set?

Gate the job with `if: vars.DEPLOY_AWS == 'true'`, so deployment jobs stay inactive until the environment's setup is complete, without failing CI in the meantime.

#### How do you post a comment on a pull request from a workflow?

Use the GitHub CLI (`gh pr comment`) or an action with the `GITHUB_TOKEN` granted `pull-requests: write`, for example to share a Terraform plan or dbt CI results.

#### How do you build and push a Docker image in GitHub Actions?

With `docker/setup-buildx-action`, `docker/login-action` (to ECR, GHCR or another registry, ideally with OIDC) and `docker/build-push-action`, tagging images with the commit SHA and using layer caching.

#### How do Dependabot or Renovate help CI/CD?

They open pull requests to update dependencies and pinned GitHub Actions, which run through CI like any change, keeping the supply chain current with tested upgrades instead of large, risky updates.

### CI/CD for dbt

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

#### How do you deploy dbt to production?

On merge to main, run `dbt build` (or a job in dbt Cloud) with the production target from the orchestrator, store artifacts (manifest, run results) for the next slim CI comparison, generate docs, and alert on failures.

#### What are dbt unit tests?

Tests (dbt 1.8+) that define mock input rows for a model's refs and the expected output, run without real data, to verify complex SQL logic like case statements and window functions in CI.

#### How do you prevent breaking downstream consumers with dbt changes?

Model contracts (enforced column names and types), model versions for breaking changes, access levels for public models, exposures documenting dashboards that depend on models, and CI that builds downstream models (`state:modified+`).

#### How do you handle dbt `profiles.yml` in CI?

Commit a profiles file that reads all connection settings from environment variables (`env_var('DBT_HOST')`), and set those variables from secrets in the workflow; never commit credentials.

#### How do you run dbt source freshness checks?

`dbt source freshness` in the production job (before building) or on a schedule, failing or warning when sources are older than thresholds, which prevents building on stale inputs.

#### How do you generate and publish dbt documentation?

Run `dbt docs generate` in the production pipeline and publish the static site (S3 with CloudFront, GitHub Pages, dbt Cloud) or push metadata to a catalog, so documentation matches what's deployed.

#### What is the dbt "clone" command useful for in CI?

`dbt clone` creates zero-copy clones (or views) of production relations into the CI or dev schema, so incremental models and downstream tests can run against realistic state cheaply.

### CI/CD for Databricks, Airflow and warehouses

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

#### How do you deploy Airflow DAGs through CI/CD?

Run DAG integrity tests and unit tests in CI, build an image with DAGs and pinned dependencies (or sync DAG files to the DAG bucket for MWAA or Composer), deploy to staging, run smoke tests, then promote to production, with rollback by redeploying the previous image or commit.

#### How do you manage Snowflake changes through CI/CD?

Account objects (warehouses, roles, grants, integrations) with Terraform; schemas and tables with migration tools (schemachange, Flyway) or `CREATE OR ALTER` scripts; transformations with dbt; all deployed by a service user with key-pair or OAuth authentication from CI, tested first on a cloned database.

#### How do you deploy AWS Glue jobs through CI/CD?

Package shared code as a wheel, upload scripts and wheels to S3 with versioned paths, define jobs, triggers and catalog tables with CloudFormation, CDK or Terraform, and run tests locally with the Glue Docker image or Spark before deployment.

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

#### How do you test Databricks code before deploying?

Unit tests on local Spark (or Databricks Connect), linting for patterns unsupported on serverless, `databricks bundle validate --strict`, deployment to a development or staging target with `mode: development`, and running integration jobs there.

#### How do you run a Databricks job from CI after deploying?

`databricks bundle run -t <target> <job_key>` (with `--no-wait` if you don't want CI to block), or trigger through the Jobs API; for production, often only on manual dispatch.

#### How do you handle Airflow Variables and Connections in CI/CD?

Keep non-secret configuration in code or environment variables in the image, and secrets in a secrets backend; never create production connections by hand in the UI, so environments are reproducible.

#### How do you deploy BigQuery or Dataform transformations?

Use Dataform's release configurations and workflow configurations with Git integration, or dbt with the BigQuery adapter, deploying through CI with a service account via workload identity federation.

### Security of the delivery pipeline

#### What are the main security risks in CI/CD?

Leaked secrets in code or logs, overly broad credentials, compromised third-party actions or dependencies, untrusted code running with secrets (forks, `pull_request_target`), insecure self-hosted runners, and unreviewed changes reaching production.

#### What is secret scanning?

Detecting secrets in code and history with tools like gitleaks, TruffleHog or GitHub's built-in secret scanning and push protection, blocking commits and alerting on leaks so credentials can be revoked.

#### What should you do if a secret is committed?

Revoke and rotate it immediately (assume it's compromised), then remove it from history if needed; deleting the commit alone isn't enough because clones and caches may have it.

#### What is software supply chain security?

Protecting the path from source to production: pinned and verified dependencies and actions, dependency vulnerability scanning (Dependabot, pip-audit), SBOMs, signed artifacts and provenance (SLSA, Sigstore), and least-privilege build systems.

#### What is least privilege in CI/CD?

Each workflow and job gets only the permissions it needs: read-only tokens by default, deployment credentials only in deploy jobs, environment-scoped secrets, and cloud roles restricted to specific resources and branches.

#### How do you protect production from unauthorized deployments?

Branch protection on main, required reviews, environment protection rules with approvers, OIDC trust policies restricted to the production environment, and audit logs of deployments.

#### How do you handle sensitive data in CI logs?

Never print secrets or real data; rely on masking but don't trust it fully; use synthetic data in tests; review logs of public repositories; and restrict log retention.

#### Why are self-hosted runners risky, and how do you secure them?

They run arbitrary workflow code inside your network; a malicious PR could attack internal systems. Use ephemeral runners (one job per runner), never run untrusted fork code on them, isolate networks, and restrict which repositories can use them.

#### What is a "poisoned pipeline execution" attack?

An attacker modifies CI configuration or files executed by CI (scripts, Makefiles) in a pull request so that the pipeline runs malicious code with access to secrets. Mitigate with least-privilege tokens, no secrets for untrusted PRs, and required reviews for CI changes.

#### How do you protect CI configuration itself?

Require code owner review for `.github/workflows/`, restrict who can modify environments and secrets, pin actions, and audit changes to workflows.

### Operations, monitoring and DataOps

#### What should happen after a deployment?

Smoke tests, monitoring of job runs and data quality checks on the next run, comparison of key metrics with previous runs, and notifications to the team; rollback quickly if checks fail.

#### How do you know whether a data deployment broke something?

Data quality tests and observability (freshness, volume, schema and distribution changes), pipeline failure alerts, reconciliation with sources, and dashboards of key metrics compared with their recent history.

#### What is GitOps?

Using Git as the single source of truth for desired state, with automated agents applying it to the environment (Argo CD, Flux for Kubernetes), so every change is a commit and the system converges to what's in the repository.

#### How do you document a release?

Pull request descriptions, a changelog (often generated from conventional commits), release notes for consumers describing data impact (new columns, changed definitions, backfills), and ADRs for significant decisions.

#### How do you communicate data changes to consumers?

Through changelogs and release notes, deprecation notices with timelines, catalog updates, contract version bumps, and direct communication for breaking changes or historical restatements.

#### How do you measure the success of CI/CD in a data team?

DORA metrics (deployment frequency, lead time, change failure rate, time to restore), number of data incidents caused by changes, time spent on manual deployments, and CI duration and cost.

#### How do you keep CI fast as the project grows?

Test only what changed (path filters, slim CI), parallelize jobs and tests, cache dependencies, use smaller synthetic data, split slow integration tests to run on main or nightly, and use larger runners where justified.

#### How do you control CI costs?

Cancel superseded runs, avoid running heavy jobs on every commit, cache dependencies, use slim CI against warehouses, auto-drop CI schemas, set timeouts on jobs, and watch minutes and warehouse spend per repository.

#### What is a deployment log, and why keep one?

A record of what version was deployed where and when, by whom and with which approvals (GitHub deployments, environment history, release notes), which is essential when correlating incidents with changes.

#### How do you correlate a data incident with a deployment?

Compare incident start time with deployment history, check which models or jobs changed (Git diff between versions), review lineage for affected tables, and look at data quality metrics before and after.

#### What is chaos testing for data pipelines?

Deliberately introducing failures in a test environment (killed jobs, missing files, delayed sources, schema changes) to verify that retries, alerts, idempotency and recovery procedures work as expected.

### Scenarios

#### Design a CI/CD pipeline for a dbt project on Snowflake.

On pull requests: lint with SQLFluff, `dbt deps`, `dbt build --select state:modified+ --defer` against a PR-specific schema using a CI service user, post results, drop the schema at the end. On merge: deploy by triggering the production job (orchestrator or dbt Cloud), store artifacts for the next comparison, publish docs. Manage warehouses and roles with Terraform in the same or a separate pipeline.

#### Design CI/CD for a PySpark lakehouse on Databricks and AWS.

CI on pull requests: secret scan, Ruff and custom Spark lint rules, unit tests on local Spark with Delta, end-to-end test on synthetic fixtures, bundle validation. CD on main: reuse CI as a gate (reusable workflow), then deploy AWS ingestion (SAM or Terraform) via OIDC and the Databricks bundle as a service principal, both in a protected production environment with concurrency set so deployments never overlap.

#### A deployment broke a production table. What should your process have caught, and how do you recover?

Recover first: roll back code, restore the table with time travel or rerun the old logic for affected partitions, and inform consumers. Then improve the pipeline: add a test for the failure case, a contract or schema check, a regression comparison in CI, or write-audit-publish so bad data isn't exposed.

#### Your CI takes 45 minutes and developers bypass it. What do you do?

Profile the pipeline, parallelize independent jobs, cache dependencies, run only affected tests (path filters, slim CI), shrink test data, move slow end-to-end tests to the merge queue or main, and set a target (for example under 10 minutes for PR checks).

#### A public repository's workflow logs show a database hostname. What do you change?

Move the hostname and other identifying values to environment secrets so they're masked, rotate credentials if anything sensitive appeared, review past logs, and add a check that prevents printing configuration in logs.

#### How would you migrate from manual deployments to CI/CD?

Put everything in Git (code, configuration, infrastructure), add CI with linting and tests on pull requests, automate deployment to a staging environment, add smoke tests and approvals, then automate production deployment with the same artifacts, and remove manual access to production gradually.

#### How do you explain CI/CD for data to a non-technical stakeholder?

It's an automatic quality check and delivery line for our data pipelines: every change is tested before it can affect the reports, and approved changes reach production the same safe way every time, so numbers stay trustworthy while we improve them quickly.

#### How would you add data quality gates to an existing CI/CD pipeline?

Add data tests to the transformation project (uniqueness, not null, relationships, accepted values), run them in CI on test data and in production after each build, block publishing (write-audit-publish or failing the job) on critical failures, and alert owners.

#### Two teams deploy to the same Databricks workspace and overwrite each other's jobs. How do you fix it?

Use bundles with distinct names and targets per team, deploy as each team's service principal with permissions limited to its resources, use development mode for personal deployments, and separate production deployments by repository and environment protections.

#### A Terraform apply in CI deleted a production resource. How do you prevent it from happening again?

Require plan review before apply, add `prevent_destroy` lifecycle rules on critical resources, run policy checks that block deletions of protected resources, separate state and permissions per environment, and restore from backups or re-import the resource now.
