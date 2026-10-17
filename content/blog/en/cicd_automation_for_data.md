## CI/CD and Automation for Data: What Matters, with GitHub Actions Examples

##### Published on {{PUBLISH_DATE}}

<!-- TITLE_IMAGE -->

![CI/CD and automation for data pipelines](../../images/cicd_automation_for_data_title_img.png)

*Technical article*

## Why data teams need CI/CD

Ten years ago, deploying a data pipeline often meant copying a script to a server, editing a cron line and hoping. I've seen emergency fixes typed directly into production, jobs that worked in one environment and not in another, and Monday mornings spent finding out which of Friday's changes broke the dashboards. None of that is a tooling problem. It's what happens when changes reach production without a repeatable, automated path.

CI/CD gives every change the same path: it's versioned, reviewed, tested automatically, deployed by a machine with the same steps every time, and traceable afterwards. For data teams it brings the same benefits as for application teams (fewer incidents, faster delivery, easy rollbacks), but data adds some considerations of its own. This article covers what I think matters most, then shows concrete GitHub Actions workflows, several of them taken from the pipelines behind this site and my [EU company registry lakehouse](../projects/eu-company-registry.html).

## What makes data CI/CD different

Four differences shape everything else:

1. **Pipelines have state.** Deploying new code doesn't replace the tables it wrote. A schema change needs a migration; a logic change may need a backfill; a bad deployment may need data restored, not just code rolled back.
2. **Correctness depends on data, not only code.** Tests on fixtures prove the logic. Only data quality checks on real data prove next month's file is sane. CI/CD has to include both.
3. **Deployments can be expensive.** A change to a core model can trigger a full recomputation of years of history. Cost and timing are part of the release plan.
4. **Several systems are involved.** A typical data platform spans a code repository, a cloud account, a compute platform (Databricks, Snowflake, Glue) and an orchestrator. Each needs credentials, and none should hold another's secrets.

## The considerations that matter

### Version everything

Code, SQL models, orchestration definitions (DAGs, Databricks Asset Bundles, job specs), infrastructure (Terraform, CloudFormation, SAM), permissions, data quality rules and CI workflows all belong in Git. If something can only be changed by clicking in a console, it can't be reviewed, tested or rolled back. Real data and secrets are the two things that never go in.

### Test in layers, and make the fast layers really fast

Linting and unit tests should run in seconds; an end-to-end run on synthetic fixtures in minutes; data quality checks in production on every run. If the pull request checks take 45 minutes, developers will find ways around them. I wrote about the test layers in detail in [Testing and Performance in Big Data Pipelines](testing_and_performance_big_data.html).

### Separate environments, promote the same artifact

At least development, a staging or pre-production environment, and production, ideally in separate accounts, workspaces or catalogs, so a mistake in dev can't touch production data. Build once (a wheel, an image, a bundle), stamp it with the commit, and promote that same artifact. Configuration differs per environment; code doesn't.

### Identity, not keys

The single biggest security improvement in CI/CD over the last few years is **workload identity federation (OIDC)**. Instead of storing long-lived cloud access keys as repository secrets, the workflow requests a short-lived token from GitHub and exchanges it for temporary credentials of a role that only trusts that repository and environment. Nothing to leak, nothing to rotate. Databricks, Snowflake (key pair or OAuth) and the major clouds all support machine identities; deploy as service principals, never as a person.

### Make deployments safe to repeat

Deployments are retried, re-run and occasionally triggered twice. Infrastructure as code is declarative (applying it twice changes nothing), bundles and jobs are updated in place, and pipelines themselves must be idempotent (`MERGE` or overwrite by partition, never blind appends). Never let two deployments to the same environment run at the same time.

### Plan data changes, not just code changes

For every pull request, ask: does this change a schema consumers depend on? Does it require reprocessing history? Use backward-compatible schema changes (add, migrate, then remove: *expand and contract*), data contracts checked in CI, versioned models for breaking changes, and an explicit backfill plan with cost and timing. Write-audit-publish (write new data to a staging location, check it, then swap) keeps bad data away from consumers.

### Gate production, but keep the gate light

A required approval before production is cheap insurance for data platforms, where one bad deployment can corrupt tables consumers read. Keep everything before the gate automatic, so the approval is a quick look at a green pipeline, not a manual checklist.

### Watch what happens after the deployment

CI/CD doesn't end at "deploy succeeded". Smoke tests, the next run's data quality results, freshness and volume monitoring, and alerts on duration tell you whether the change actually works with real data.

### Be careful with public repositories

If the repository is public, so are its workflow logs. GitHub masks secrets in logs, but not plain variables. Hostnames, bucket names, account IDs and email addresses should be stored as **secrets** of a protected environment, even though they aren't passwords, so they never appear in a public log. Scan the history for secrets in CI, not just new commits.

## GitHub Actions in five minutes

Workflows are YAML files in `.github/workflows/`. Each workflow is triggered by events (`push`, `pull_request`, `schedule`, `workflow_dispatch` for manual runs, `workflow_call` to be reused by other workflows) and contains **jobs** that run on fresh virtual machines (runners). Jobs run in parallel unless one `needs` another; each job is a list of **steps** that run shell commands or reusable **actions**. **Environments** (for example `production`) hold their own secrets and variables and can require reviewers before a job that targets them starts. That's enough to read the examples below.

## Example 1: CI for a PySpark project

This is the shape of the CI in my lakehouse repository. It runs on every pull request and is reused as the first stage of the deployment workflow:

```yaml
name: ci

on:
  pull_request:
  workflow_call:      # cd.yml runs this as the gate before any deployment
  workflow_dispatch:

permissions:
  contents: read      # least privilege by default

jobs:
  checks:
    runs-on: ubuntu-24.04
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0              # full history, for the secret scan

      - name: Secret scan (full history)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - uses: actions/setup-java@v4   # Spark needs a JVM
        with:
          distribution: temurin
          java-version: "17"

      - name: Install
        run: pip install -e ".[local,dev]"

      - name: Lint (ruff + PySpark anti-patterns + sensitive data)
        run: |
          ruff check src tests tools
          python tools/spark_lint.py src
          git ls-files | xargs python tools/check_sensitive.py

      - name: Unit tests
        run: pytest tests -m "not e2e" --cov=registry_lakehouse --cov-report=term-missing

      - name: End-to-end pipeline on synthetic fixtures
        run: pytest tests -m e2e
```

A few choices worth noting:

- **`permissions: contents: read`** at the top: the automatically generated `GITHUB_TOKEN` gets read-only access unless a job explicitly asks for more.
- **The secret scan reads the full history**, because a key committed and then deleted is still in the repository.
- **Custom lint rules** encode lessons learned: no `collect()` on unbounded data, no Python UDFs, nothing that breaks on Databricks serverless, no hard-coded bucket paths.
- **Unit tests and the end-to-end run are separate steps**, so a failure tells you immediately which layer broke.
- **`workflow_call`** lets the deployment workflow reuse this exact file instead of duplicating it.

## Example 2: continuous deployment to AWS and Databricks

The deployment workflow runs on every push to `main`. It reuses the CI as a gate, then deploys two independent systems, each only after a manual approval in the `production` environment:

```yaml
# push to main ──► ci (all tests) ──► [production approval] ──► AWS ingestion (SAM)
#                                                          └──► Databricks job (bundle)
name: cd

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      run_job:
        description: Start a production run right after deploying
        type: boolean
        default: false

concurrency:
  group: deploy-production
  cancel-in-progress: false      # never interrupt a deployment halfway

permissions:
  contents: read

jobs:
  tests:
    uses: ./.github/workflows/ci.yml

  aws:
    needs: tests
    if: vars.DEPLOY_AWS == 'true'          # switched on once the AWS setup exists
    runs-on: ubuntu-24.04
    environment: production
    permissions:
      contents: read
      id-token: write                      # allows GitHub OIDC -> AWS role
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
        with:
          use-installer: true
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      - name: Build and deploy
        run: |
          sam build -t infra/template.yaml
          sam deploy --stack-name eu-registry-ingestion --resolve-s3 \
            --capabilities CAPABILITY_IAM \
            --no-confirm-changeset --no-fail-on-empty-changeset \
            --parameter-overrides "BucketName=${{ secrets.LANDING_BUCKET }}"

  databricks:
    needs: tests
    if: vars.DEPLOY_DATABRICKS == 'true'
    runs-on: ubuntu-24.04
    environment: production
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
      DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main      # pin to a commit SHA in production
      - name: Stamp a unique wheel version
        run: python tools/set_version.py "0.2.${{ github.run_number }}+g${GITHUB_SHA::7}"
      - name: Validate against the workspace
        run: databricks bundle validate -t prod --strict
      - name: Deploy
        run: databricks bundle deploy -t prod
      - name: Start a run (optional)
        if: github.event_name == 'workflow_dispatch' && inputs.run_job
        run: databricks bundle run -t prod registry_lakehouse --no-wait
```

What this workflow gets right, and why:

- **The CI is the gate.** `uses: ./.github/workflows/ci.yml` runs the same tests as pull requests; nothing deploys if they fail.
- **`concurrency` with `cancel-in-progress: false`** queues deployments instead of running two at once or killing one halfway.
- **No AWS keys anywhere.** `id-token: write` lets the job request an OIDC token; `configure-aws-credentials` exchanges it for a short-lived role. The role's trust policy only accepts tokens from this repository's `production` environment.
- **Databricks deploys as a service principal** over OAuth machine-to-machine. The bundle defines the job, its schedule, alerts and permissions as code.
- **Every artifact is traceable.** The wheel version contains the run number and short commit SHA.
- **Repository variables gate each deployment** (`vars.DEPLOY_AWS == 'true'`), so the workflow stays green while a target environment isn't set up yet.
- **Identifying values are secrets**, because the repository is public and only secrets are masked in logs.
- **Starting a production run is a separate, manual decision** through `workflow_dispatch` inputs.

On the AWS side, the role's trust policy is what makes OIDC safe. The important part is the condition on the token's subject:

```json
{
  "Effect": "Allow",
  "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
      "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:environment:production"
    }
  }
}
```

## Example 3: slim CI for dbt

For a dbt project, rebuilding everything on every pull request is slow and expensive. Slim CI builds only the models a pull request modified, plus everything downstream of them, in a schema unique to the pull request, deferring unchanged references to production:

```yaml
name: dbt-ci
on:
  pull_request:
    paths: ["models/**", "macros/**", "seeds/**", "dbt_project.yml", "packages.yml"]

permissions:
  contents: read
  id-token: write

concurrency:
  group: dbt-ci-${{ github.event.pull_request.number }}
  cancel-in-progress: true          # a new push supersedes the previous run

jobs:
  build:
    runs-on: ubuntu-24.04
    environment: ci
    env:
      DBT_TARGET_SCHEMA: dbt_ci_pr_${{ github.event.pull_request.number }}
      SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
      SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_CI_USER }}
      SNOWFLAKE_PRIVATE_KEY: ${{ secrets.SNOWFLAKE_CI_PRIVATE_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: dbt deps
      - name: Lint SQL
        run: sqlfluff lint models
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.ARTIFACTS_READ_ROLE_ARN }}
          aws-region: eu-west-1
      - name: Fetch the production manifest
        run: aws s3 cp s3://my-dbt-artifacts/prod/manifest.json prod-artifacts/manifest.json
      - name: Build and test modified models and their children
        run: dbt build --select state:modified+ --defer --state prod-artifacts --target ci
      - name: Drop the pull request schema
        if: always()
        run: dbt run-operation drop_schema --args "{schema: $DBT_TARGET_SCHEMA}"
```

The profile reads its connection settings from environment variables (`env_var('SNOWFLAKE_ACCOUNT')` and so on), so no credentials live in the repository. `drop_schema` is a small project macro; dropping the schema `if: always()` keeps the warehouse clean even when the build fails. On merge, the production job runs and uploads its new `manifest.json`, which becomes the comparison point for the next pull request.

## Example 4: Terraform plan on pull requests, apply on main

Infrastructure changes deserve the same review as code. The plan goes into the pull request; the apply happens only from `main`, behind the production environment:

```yaml
name: infra
on:
  pull_request:
    paths: ["infra/**"]
  push:
    branches: [main]
    paths: ["infra/**"]

permissions:
  contents: read
  id-token: write
  pull-requests: write          # to comment the plan

jobs:
  terraform:
    runs-on: ubuntu-24.04
    environment: ${{ github.event_name == 'push' && 'production' || 'plan' }}
    defaults:
      run:
        working-directory: infra
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.TERRAFORM_ROLE_ARN }}
          aws-region: eu-west-1
      - run: terraform init -input=false
      - run: terraform plan -input=false -out=tfplan -no-color | tee plan.txt
      - name: Comment the plan on the pull request
        if: github.event_name == 'pull_request'
        run: gh pr comment ${{ github.event.pull_request.number }} --body-file plan.txt
        env:
          GH_TOKEN: ${{ github.token }}
      - name: Apply
        if: github.event_name == 'push'
        run: terraform apply -input=false tfplan
```

Two roles are better than one here: a read-only role for plans on pull requests, and a role that can change resources, trusted only from the production environment. Add `prevent_destroy` lifecycle rules on resources that must never be deleted by accident.

## Example 5: a static site whose data is never redeployed

This website is deployed by a small workflow: every push runs the tests (which build the whole site and check links, translations and metadata), and pushes to `master` deploy to S3 and CloudFront through OIDC. One detail is specific to data products: the registry pipeline writes its JSON straight into the website bucket, so the deploy script **excludes the data path**. Publishing new data never requires a site deployment, and a site deployment never overwrites pipeline output.

```yaml
jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: pytest -q            # builds the site, checks links, metadata, translations

  deploy:
    needs: test
    if: github.ref == 'refs/heads/master' && github.event_name != 'pull_request'
    runs-on: ubuntu-24.04
    environment:
      name: production
      url: https://www.catobyte.co
    concurrency:
      group: production
      cancel-in-progress: false
    permissions:
      contents: read
      id-token: write
    env:
      BUCKET: ${{ vars.S3_BUCKET }}
      DISTRIBUTION_ID: ${{ vars.CLOUDFRONT_DISTRIBUTION_ID }}
      PYTHON: python
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: pip install -r requirements-dev.txt
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ vars.AWS_REGION }}
      # test, build, sync to S3 with --exclude "*/projects/*/data/*", then invalidate CloudFront
      - run: ./scripts/deploy.sh
```

## Example 6: manual backfills with inputs

Backfills shouldn't require someone's laptop. A `workflow_dispatch` with typed inputs gives a reviewed, logged way to reprocess a period:

```yaml
name: backfill
on:
  workflow_dispatch:
    inputs:
      start_date:
        description: First date to reprocess (YYYY-MM-DD)
        required: true
      end_date:
        description: Last date to reprocess (YYYY-MM-DD)
        required: true

jobs:
  backfill:
    runs-on: ubuntu-24.04
    environment: production          # same approval as a deployment
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
      DATABRICKS_CLIENT_SECRET: ${{ secrets.DATABRICKS_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - name: Run the backfill job for the requested period
        run: |
          databricks bundle run -t prod backfill_job \
            --params start_date=${{ inputs.start_date }},end_date=${{ inputs.end_date }}
```

The pipeline itself must accept date ranges and write idempotently; the workflow only makes running it safe, auditable and approved.

## Hardening checklist for GitHub Actions

- Set `permissions:` explicitly; default to `contents: read` and grant more per job.
- Use OIDC for cloud access; restrict role trust to the repository and environment.
- Store deployment secrets in **environments** with required reviewers and branch restrictions.
- In public repositories, store identifying values (hosts, buckets, account IDs, emails) as secrets so they're masked.
- Pin third-party actions to a full commit SHA for production workflows, and let Dependabot update them.
- Never check out and run pull request code in `pull_request_target` workflows.
- Use `concurrency` so deployments never overlap.
- Add `timeout-minutes` to jobs so a hung step can't run for six hours.
- Pin the runner image (`ubuntu-24.04`) for reproducible builds.
- Scan for secrets over the full history, and require code owner review for `.github/workflows/`.

## Common pitfalls

- **CI that only lints.** Without unit and end-to-end tests, CI gives a false sense of safety.
- **Deploying by rebuilding per environment.** What you tested isn't what you deployed.
- **Long-lived cloud keys in secrets.** They leak, they're shared, and nobody rotates them.
- **Treating schema changes like code changes.** Dropping a column consumers use breaks them, however green the pipeline is.
- **No plan for data rollback.** Rolling back code doesn't un-write tables; know how you'll restore (time travel, snapshots, previous table version) before you deploy.
- **Manual steps "just this once".** Every manual production change is drift the next deployment may overwrite.

CI/CD for data isn't about the YAML. It's about making every change follow the same path, so the platform can change quickly without the numbers changing by accident. Start small: put everything in Git, add a CI job that runs your tests on every pull request, then automate one deployment with OIDC and an approval. Each step pays for itself the first time it catches a problem before your users do.
