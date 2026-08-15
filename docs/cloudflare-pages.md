# Cloudflare Pages deployment behavior

Status: **Continuous `pages.dev` deployment active; independent domain release specified, not implemented**

Last reviewed: **2026-08-15**

This document is the repository source of truth for the continuous Cloudflare Pages deployment and the intended production-domain behavior for `livingintelligence.xyz`. Provider state can change independently, so future deployment work must still inspect the current GitHub, Cloudflare Pages, deployment, custom-domain, and DNS state before making changes.

## Required behavior

- Keep the existing Git-connected Cloudflare Pages project dedicated to continuous `pages.dev` deployment.
- Every push to `main` automatically deploys to `https://livingintelligence-xyz.pages.dev` through the standard Cloudflare Pages Git integration, indefinitely.
- Never disable automatic production-branch deployments on the continuous project as part of a domain release.
- Do not create a Living Intelligence preview or alpha custom subdomain.
- Do not attach `livingintelligence.xyz` or `www.livingintelligence.xyz` to the continuous project. A production-branch deployment updates both a Pages project's production `pages.dev` URL and any custom domains attached to that project.
- Use a separate, non-Git-connected Pages project for the production custom domain.
- Deploy the custom-domain project only through a manually dispatched GitHub Actions workflow.
- Allow the workflow to deploy any commit verified as belonging to `main`; do not require a release branch, a production-branch cutoff, or a branch-control change.
- Keep normal pull-request and non-production-branch preview deployments enabled unless there is a specific reason to restrict them.
- Never treat a Git push to the continuous project, a successful preview deployment, or repository visibility as proof that `livingintelligence.xyz` changed.

## Continuous `pages.dev` project

The verified continuous-deployment configuration is:

| Setting | Value |
| --- | --- |
| GitHub repository | `livingintelligence-xyz/livingintelligence.xyz` |
| Pages project name | `livingintelligence-xyz` |
| Pages URL | `https://livingintelligence-xyz.pages.dev` |
| Production branch | `main` |
| Framework preset | None |
| Repository root | `/` |
| Build command | Blank |
| Build output directory | `www` |
| Custom domains | None, permanently |
| Automatic production deployments | Enabled permanently |
| Preview deployments | Enabled |

The website is dependency-free static HTML, CSS, SVG, JSON, XML, and image assets. It has no install or build step. Cloudflare should publish the contents of `www/` directly.

Official references:

- [Git integration guide](https://developers.cloudflare.com/pages/get-started/git-integration/)
- [Git integration configuration](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Branch deployment controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)
- [Preview deployments](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
- [Custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [Wrangler configuration for Pages](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)

## Future custom-domain project

The production domain requires a distinct deployment target because Cloudflare Pages does not independently pin a custom domain while continuing to advance the same project's production `pages.dev` URL.

| Setting | Planned value |
| --- | --- |
| Preferred project name | `livingintelligence-xyz-production` (verify availability before creation) |
| Project type | Direct Upload; no Git integration |
| Deployable source | `www/` from a selected commit belonging to `main` |
| Automatic deployments | None |
| Deployment method | Manually dispatched GitHub Actions workflow using Wrangler |
| Custom domains | `livingintelligence.xyz`, then `www.livingintelligence.xyz` with a permanent apex redirect |

The production project will also receive a Cloudflare-provided `pages.dev` hostname, but it is an implementation endpoint for manual release verification, not the continuously updated preview target or the canonical public origin.

## Continuous `pages.dev` deployment

State: **active**

The Git-connected project was created on 2026-08-14. Its initial production deployment succeeded from `main` at commit `6f44a8e35fccd202ae126a10c8bea5f0c62b2495`, and the assigned hostname serves the contents of `www/` over HTTPS. A later GitHub push at commit `f9a398cd0e2d48fda60dac2c63eecf0a79579758` triggered and completed a production deployment, verifying the automatic `main` deployment path.

1. Give the Cloudflare Pages GitHub application access to this repository. Limit organization access to this repository when possible.
2. Create the Git-connected Pages project using the configuration above.
3. Leave automatic production deployments enabled for `main`.
4. Do not attach `livingintelligence.xyz` or another custom hostname.
5. Verify that the initial `main` commit deploys to the assigned `*.pages.dev` URL.
6. Verify that later pushes to `main` automatically update that URL.
7. Confirm that pull requests or other included branches receive Cloudflare preview deployment URLs without affecting the production `*.pages.dev` deployment.

This automatic deployment path remains active after the custom domain launches. Living Intelligence will not add a custom preview, staging, or alpha hostname.

## Manually triggered custom-domain releases

State: **specified; production project and workflow not configured**

Use a separate Pages project. Never attach the custom domain to `livingintelligence-xyz`, because every automatic `main` deployment to that project would also update the domain.

The implementation order is:

1. Confirm the exact name for the separate Direct Upload production project and create it without attaching a custom domain.
2. Configure a GitHub `production` environment only to scope the least-privilege Cloudflare credentials required for that project; do not add an approval requirement unless the user requests one.
3. Add and validate the manually dispatched GitHub Actions domain-release workflow.
4. Dispatch the workflow for a selected commit and verify that the commit belongs to `main`.
5. Verify that the workflow deployed the intended commit to the production project's Cloudflare-provided URL.
6. Attach `livingintelligence.xyz` to the production project.
7. Add `www.livingintelligence.xyz` and configure a permanent redirect to the apex that preserves the path and query string.
8. Verify the apex, the `www` redirect, TLS, static assets, metadata, and deployed commit.

There is no cutoff of the continuous `main` deployment path. After the domain launches, every push to `main` continues updating `livingintelligence-xyz.pages.dev`, while `livingintelligence.xyz` changes only after the domain-release action is manually dispatched.

## Intended GitHub Actions release gate

The future workflow should live at `.github/workflows/deploy-production.yml` and use a manual domain-release pattern:

- Trigger only through `workflow_dispatch`.
- Require a commit input, resolve it to a full SHA, and fail unless that SHA belongs to the history of `origin/main`.
- Permit any commit belonging to `main`, including an older known-good commit for rollback.
- Use a `production` environment in GitHub to scope secrets, without an additional approval gate unless requested.
- Serialize releases with a production concurrency group and `cancel-in-progress: false`.
- Grant only the GitHub permissions required to read the repository and record the deployment.
- Store the Cloudflare account ID and API token as GitHub environment secrets; never commit credentials.
- Validate the static site before deployment.
- Deploy `www/` to the separate Direct Upload production project with a pinned Wrangler version.
- Fail if the deployed commit cannot be reconciled with the selected GitHub SHA.
- Run post-deploy HTTP verification and fail closed on an ambiguous or partial result.

The planned Wrangler operation is equivalent to:

```sh
wrangler pages deploy www \
  --project-name livingintelligence-xyz-production \
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

For the continuous deployment target, verify `https://livingintelligence-xyz.pages.dev` and reconcile its deployment to the latest pushed `main` commit.

For every manually triggered domain release, verify at least:

- `https://livingintelligence.xyz/` returns the intended page over HTTPS.
- `https://www.livingintelligence.xyz/` permanently redirects to the apex while preserving path and query data.
- `/site.webmanifest`, `/robots.txt`, `/sitemap.xml`, and `/assets/og-1200x627.png` return successful responses with appropriate content types.
- The HTML canonical URL and Open Graph URL remain `https://livingintelligence.xyz/`.
- The deployed source can be tied to the selected GitHub commit.
- An unknown path follows the explicitly chosen 404 or redirect policy; do not add catch-all redirect behavior without a separate decision.

Browser visual QA remains a user-run step unless explicitly requested in a future task.

## Rollback

- If a bad commit publishes to the continuous `pages.dev` project, fix or revert it on `main`; do not disable the standing automatic-deployment policy as a routine release step.
- For the custom domain, redeploy a known-good commit belonging to `main` through the manual workflow.
- If the custom domain or certificate is unhealthy, detach or redirect the domain only after confirming the exact DNS and Pages state.
- Do not rewrite Git history, force-push, delete the Pages project, or delete DNS records as an automatic recovery action.
- Report whether rollback restored only the Pages deployment, the custom domain, or both.

## Current implementation status

As of the review date above:

- The public GitHub repository and `main` branch exist.
- The deployable static site is in `www/`.
- The Git-connected Cloudflare Pages project `livingintelligence-xyz` exists and publishes `www/` from every `main` commit to `https://livingintelligence-xyz.pages.dev`.
- The initial production deployment succeeded and was reconciled to Git commit `6f44a8e35fccd202ae126a10c8bea5f0c62b2495`.
- Automatic production deployments and preview deployments are enabled. A GitHub push to `main` was observed triggering a successful production deployment.
- The project has only its Cloudflare-provided `pages.dev` hostname; no custom domain is attached and Web Analytics is disabled.
- The live root page and required metadata assets return successful HTTPS responses, and the deployed HTML matches `www/index.html` exactly.
- An unknown path currently returns the homepage with HTTP `200`; an explicit production 404 policy remains a separate decision.
- No separate Direct Upload production project or GitHub Actions domain-release workflow has been added.
- No Cloudflare credentials or GitHub environment secrets have been configured by this repository setup work.
- No DNS record or custom domain has been changed by this repository setup work.

Future agents must re-verify every provider-side status item before implementation because this section can become stale.
