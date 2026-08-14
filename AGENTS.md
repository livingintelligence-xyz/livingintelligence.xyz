<!-- AGENTS.md and CLAUDE.md are identical mirrors. Apply every instruction change to both files and verify them with `cmp -s AGENTS.md CLAUDE.md`. -->

# Living Intelligence website agent instructions

## Project

This repository contains the static website for Living Intelligence at `livingintelligence.xyz`.

- Deployable site: `www/`
- Main page: `www/index.html`
- Static assets: `www/assets/`
- Search files: `www/robots.txt` and `www/sitemap.xml`
- Web app metadata: `www/site.webmanifest`
- Hosting plan: `docs/cloudflare-pages.md`
- Production branch: `main`

The site is intentionally dependency-free. Do not introduce a framework, package manager, build system, client-side application runtime, or analytics service unless the user explicitly asks for it.

## Brand and copy

Living Intelligence is an independent technology company exploring how intelligence can improve the way people live, work, create, and interact with their environments.

Preserve the central lockup and idea:

> Living Intelligence
>
> Intelligence for living, that lives.

The work should feel useful, humane, calm, legible, privacy-conscious, technically rigorous, and worthy of trust. Preserve human agency and avoid reducing the company to an AI lab, generic software studio, or conventional startup.

Avoid generic AI imagery and language: glowing brains, neural-network diagrams, purple cyberpunk gradients, particle fields, robots, chat bubbles, excessive glass, abstract 3D blobs, or claims that exist mainly to signal “AI.”

Keep public claims grounded in information the user has confirmed. Do not invent products, customers, partnerships, team members, addresses, awards, launch dates, or capabilities.

## Working agreement

Before editing:

- Read `README.md`, this file, and any task-relevant document under `docs/`.
- Inspect `git status --short --branch` and the relevant files.
- Preserve unrelated user changes and stage only the files that belong to the task.
- Treat documentation marked “planned” as intent, not evidence of deployed infrastructure.

For scoped repository work, direct commits and pushes to `main` are allowed. Do not create a feature branch or pull request unless the user asks for one. When publishing is in scope:

1. Validate the intended files.
2. Review the exact diff.
3. Commit with a concise message.
4. Push `main` directly.
5. Verify that local `main`, `origin/main`, and the remote branch SHA agree.

Never force-push, rewrite public history, delete the repository, or remove deployed infrastructure as an automatic recovery action.

Do not commit secrets, API tokens, credentials, private keys, account identifiers that are meant to remain private, or local environment files.

## Browser QA policy

Do not open or use the browser for visual QA after every change.

For small, targeted changes—especially copy, metadata, CSS, typography, spacing, or static HTML edits:

- Make the requested change.
- Run lightweight source validation.
- Summarize what changed.
- Do not launch a browser unless explicitly asked.

Use browser QA when:

- The user explicitly asks for it.
- A layout, responsive, animation, or interaction change has meaningful visual-regression risk.
- A visual problem cannot be diagnosed from source.
- The change is broad enough that browser verification is proportionate.

When browser QA is not performed, say:

> Browser QA skipped per project instructions.

## Deployment

Read `docs/cloudflare-pages.md` before changing hosting, deployment workflows, GitHub environments or secrets, Cloudflare Pages settings, DNS, redirects, or custom domains.

The intended behavior is:

- Initially, the Git-connected Cloudflare Pages project automatically deploys `main` to its Cloudflare-provided `*.pages.dev` URL.
- No custom preview, staging, or alpha subdomain is planned.
- Before `livingintelligence.xyz` is attached, automatic production-branch deployments are disabled.
- Production is then released only through a guarded, manually dispatched GitHub Actions workflow.
- Pull-request and non-production-branch preview deployments may remain enabled.

The hosting plan is not proof of provider state. Before any deployment work, inspect the current GitHub workflow, Cloudflare Pages project, deployment history, custom domains, DNS records, and production response. Do not claim that a push deployed the website without deployment evidence.

Do not create a second Pages project, attach a custom domain, add GitHub secrets, enable analytics, or deploy production unless the user explicitly asks for that state change.

## SEO

The canonical public origin is `https://livingintelligence.xyz`. Production SEO surfaces currently live in:

- `www/index.html`: title, description, canonical URL, robots directive, Open Graph metadata, and Twitter/X card metadata.
- `www/robots.txt`: crawler policy and sitemap location.
- `www/sitemap.xml`: canonical page inventory and modification date.
- `www/assets/og-1200x627.png`: social preview image.

Keep ordinary page metadata and social-preview metadata separate. If asked to change only an Open Graph or Twitter/X field, do not silently change the page title, visible copy, or normal meta description.

When changing a public URL or canonical policy, audit every relevant surface together: canonical link, `og:url`, absolute social-image URLs, robots sitemap declaration, sitemap locations, redirects, and structured data if it is later added.

Preserve these requirements:

- One canonical URL for the landing page.
- Absolute HTTPS URLs for canonical and social metadata.
- Accurate Open Graph image type, dimensions, and alternative text.
- A sitemap containing only canonical, indexable URLs.
- A robots file that references the production sitemap.
- Meaningful link text, heading order, document language, and image or SVG accessibility labels.
- Metadata and structured data that describe only content visibly supported by the page.

Do not change canonical URLs to a temporary `*.pages.dev` hostname. Before exposing a temporary or preview hostname to crawlers, decide whether it should be protected or marked non-indexable using a host-appropriate mechanism that cannot accidentally apply `noindex` to the production domain.

IndexNow is not configured for this repository. Do not add a key file, submit URLs, or claim indexing success unless the user explicitly requests it and the production key file and canonical URLs have been verified live.

## Validation

For ordinary static-site or documentation changes, prefer:

```sh
jq empty www/site.webmanifest
xmllint --noout www/sitemap.xml www/assets/li-icon.svg
git diff --check
```

Also verify that every changed local `href`, `src`, manifest icon, sitemap URL, and documentation link resolves to the intended file or canonical URL.

For deployment-related changes, add checks appropriate to the workflow and verify the deployed commit, HTTP status, redirects, content types, TLS, and required root assets. A green GitHub workflow alone does not prove the custom domain is serving the intended commit.
