# Cloudflare Pages deployment behavior

Status: **planned, not implemented**

Last reviewed: **2026-08-13**

This document is the repository source of truth for the intended Cloudflare Pages behavior for `livingintelligence.xyz`. Future implementation work must inspect the current GitHub, Cloudflare Pages, and DNS state before making changes; the status recorded here is a planning snapshot, not proof of live provider state.

## Required behavior

- Use one Cloudflare Pages project for both the Cloudflare-provided URL and the eventual production custom domain.
- Initially, every push to `main` automatically deploys to the project's `*.pages.dev` URL through the standard Cloudflare Pages Git integration.
- Do not create a Living Intelligence preview or alpha custom subdomain.
- Do not attach `livingintelligence.xyz` during the initial `*.pages.dev` phase.
- Before attaching the production domain, disable automatic production-branch deployments.
- After production cutover, deploy the Pages production environment only through a guarded, manually dispatched GitHub Actions workflow.
- Keep normal pull-request and non-production-branch preview deployments enabled unless there is a specific reason to restrict them.
- Never treat a Git push, a successful preview deployment, or repository visibility as proof that `livingintelligence.xyz` changed.

## Pages project configuration

The intended initial configuration is:

| Setting | Value |
| --- | --- |
| GitHub repository | `livingintelligence-xyz/livingintelligence.xyz` |
| Preferred Pages project name | `livingintelligence-xyz` (confirm availability before creation) |
| Expected Pages URL | `https://livingintelligence-xyz.pages.dev` if the preferred name is available |
| Production branch | `main` |
| Framework preset | None |
| Repository root | `/` |
| Build command | Blank |
| Build output directory | `www` |
| Initial custom domains | None |
| Initial automatic production deployments | Enabled |
| Preview deployments | Enabled |

The website is dependency-free static HTML, CSS, SVG, JSON, XML, and image assets. It has no install or build step. Cloudflare should publish the contents of `www/` directly.

Official references:

- [Git integration guide](https://developers.cloudflare.com/pages/get-started/git-integration/)
- [Git integration configuration](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Branch deployment controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Preview deployments](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [Wrangler configuration for Pages](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)

## Phase 1: automatic `pages.dev` deployment

1. Give the Cloudflare Pages GitHub application access to this repository. Limit organization access to this repository when possible.
2. Create the Git-connected Pages project using the configuration above.
3. Leave automatic production deployments enabled for `main`.
4. Do not attach `livingintelligence.xyz` or another custom hostname.
5. Verify that the initial `main` commit deploys to the assigned `*.pages.dev` URL.
6. Verify that later pushes to `main` automatically update that URL.
7. Confirm that pull requests or other included branches receive Cloudflare preview deployment URLs without affecting the production `*.pages.dev` deployment.

During this phase, the Cloudflare-provided production URL is the only published website target. This matches the automatic Git-connected behavior used for Aetherloom and the `alpha.alexfili.pe` environment, but Living Intelligence will not add a custom alpha hostname.

## Phase 2: guarded production cutover

Use the same Pages project. Do not create a second production project.

The safe cutover order is:

1. Add and validate the guarded GitHub Actions production workflow while no custom domain is attached.
2. Configure a GitHub `production` environment with the least-privilege Cloudflare credentials required to deploy this Pages project.
3. Disable automatic production-branch deployments in Cloudflare Pages. Leave desired preview-branch deployments enabled.
4. Manually dispatch the workflow for the selected commit on `main`.
5. Verify that the workflow deployed the intended commit to the project's production `*.pages.dev` URL.
6. Attach `livingintelligence.xyz` to the Pages project.
7. Add `www.livingintelligence.xyz` and configure a permanent redirect to the apex that preserves the path and query string.
8. Verify the apex, the `www` redirect, TLS, static assets, metadata, and the deployed commit.

This order ensures that the first version exposed at `livingintelligence.xyz` was selected and deployed through the guarded workflow. After cutover, an ordinary push to `main` must not change the Pages production environment or the custom domain.

## Intended GitHub Actions release gate

The future workflow should live at `.github/workflows/deploy-production.yml` and follow the established `alexfili.pe` production-release pattern:

- Trigger only through `workflow_dispatch`.
- Require a string input named `confirm` whose value must exactly equal `livingintelligence.xyz`.
- Run against the explicitly selected Git ref and record its full commit SHA.
- Use a `production` environment in GitHub.
- Serialize releases with a production concurrency group and `cancel-in-progress: false`.
- Grant only the GitHub permissions required to read the repository and record the deployment.
- Store the Cloudflare account ID and API token as GitHub environment secrets; never commit credentials.
- Validate the static site before deployment.
- Deploy `www/` to the existing Pages project with a pinned Wrangler version.
- Fail if the deployed commit cannot be reconciled with the selected GitHub SHA.
- Run post-deploy HTTP verification and fail closed on an ambiguous or partial result.

The planned Wrangler operation is equivalent to:

```sh
wrangler pages deploy www \
  --project-name livingintelligence-xyz \
  --branch main \
  --commit-hash <selected-github-sha>
```

Confirm the final project name before authoring the workflow. If Cloudflare assigns a different project name, use the provider's exact project name everywhere rather than silently creating another project.

## Pre-deploy validation

At minimum, the workflow should verify:

```sh
jq empty www/site.webmanifest
xmllint --noout www/sitemap.xml www/assets/li-icon.svg
git diff --check
```

It should also fail if any required deployment artifact is missing:

- `www/index.html`
- `www/robots.txt`
- `www/site.webmanifest`
- `www/sitemap.xml`
- `www/assets/li-icon.svg`
- `www/assets/li-icon-16.png`
- `www/assets/li-icon-32.png`
- `www/assets/li-icon-180.png`
- `www/assets/li-icon-192.png`
- `www/assets/li-icon-512.png`
- `www/assets/og-1200x627.png`

## Post-deploy verification

For the initial `pages.dev` phase, verify the assigned hostname rather than assuming the preferred project name was available.

After production cutover, verify at least:

- `https://livingintelligence.xyz/` returns the intended page over HTTPS.
- `https://www.livingintelligence.xyz/` permanently redirects to the apex while preserving path and query data.
- `/site.webmanifest`, `/robots.txt`, `/sitemap.xml`, and `/assets/og-1200x627.png` return successful responses with appropriate content types.
- The HTML canonical URL and Open Graph URL remain `https://livingintelligence.xyz/`.
- The deployed source can be tied to the selected GitHub commit.
- An unknown path follows the explicitly chosen 404 or redirect policy; do not add Aetherloom's unknown-path redirect behavior without a separate decision.

Browser visual QA remains a user-run step unless explicitly requested in a future task.

## Rollback

- Before custom-domain cutover, disable automatic deployments or disconnect the Git integration if a bad build repeatedly publishes to `*.pages.dev`.
- For production, use Cloudflare Pages' previous known-good deployment or redeploy a known-good Git commit through the guarded workflow.
- If the custom domain or certificate is unhealthy, detach or redirect the domain only after confirming the exact DNS and Pages state.
- Do not rewrite Git history, force-push, delete the Pages project, or delete DNS records as an automatic recovery action.
- Report whether rollback restored only the Pages deployment, the custom domain, or both.

## Current implementation status

As of the review date above:

- The public GitHub repository and `main` branch exist.
- The deployable static site is in `www/`.
- No Cloudflare Pages project has been created by this repository setup work.
- No GitHub Actions deployment workflow has been added.
- No Cloudflare credentials or GitHub environment secrets have been configured by this repository setup work.
- No DNS record or custom domain has been changed by this repository setup work.

Future agents must re-verify every provider-side status item before implementation because this section can become stale.
