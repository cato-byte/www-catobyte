# Deployment setup (AWS + GitHub Actions)

The site is served from a private S3 bucket through CloudFront. GitHub Actions deploys it on every push to `master` after the tests pass (see `.github/workflows/ci.yml`).

GitHub authenticates to AWS with **OIDC**: each run gets short-lived credentials for one IAM role, so no AWS access keys are stored in GitHub. Account ID, bucket and distribution ID are kept out of this public repo. They live in GitHub environment variables.

## One-time AWS setup (needs an admin user)

1. **Add GitHub as an identity provider.** In IAM, go to Identity providers → Add provider → OpenID Connect.
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`
2. **Create the deploy role.** In IAM, go to Roles → Create role → Custom trust policy.
   - Paste `github-oidc-trust-policy.json`, replacing `<ACCOUNT_ID>`.
   - The trust policy only accepts jobs that run in this repo's `production` environment.
3. **Attach the permissions.** Add an inline policy from `deploy-permissions-policy.json`, replacing `<ACCOUNT_ID>`, `<BUCKET>` and `<DISTRIBUTION_ID>`. It can only list and upload to the site bucket and invalidate the site's distribution.
4. **Update the CloudFront distribution:**
   - **General → Default root object:** `index.html`
   - **Error pages:** create custom error responses for 403 and 404, with response page `/404.html` and response code 404. S3 answers 403 for missing files.

## One-time GitHub setup

In the `www-catobyte` repo:

1. **Settings → Environments → New environment:** name it `production`.
   - Optional: add yourself as a required reviewer, so each deploy waits for one click.
   - Under deployment branches, allow only `master`.
2. **In that environment, add these Variables** (not Secrets; none of them are credentials):

   | Name | Value |
   |---|---|
   | `AWS_DEPLOY_ROLE_ARN` | ARN of the role from step 2 |
   | `AWS_REGION` | `eu-west-3` |
   | `S3_BUCKET` | the site bucket name |
   | `CLOUDFRONT_DISTRIBUTION_ID` | the distribution ID |

3. **Settings → Branches → Add rule for `master`:** require the `test` status check to pass before merging.

Until the variables exist, the deploy job is skipped with a warning and only the tests run.

## Branching

`master` is production. Work happens on short-lived feature branches merged through pull requests. Pull requests run the tests; merging deploys. No separate `dev` branch is needed for a single maintainer. To preview a change, run `python -m sitegen serve` locally, or download the `site` artifact from the pull request's CI run.

## Manual deploy (fallback)

```bash
DRY_RUN=1 BUCKET=<bucket> ./scripts/deploy.sh                       # preview
BUCKET=<bucket> DISTRIBUTION_ID=<id> ./scripts/deploy.sh            # deploy
```
