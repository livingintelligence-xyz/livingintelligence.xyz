# Living Intelligence

**Intelligence for living, that lives.**

Living Intelligence is an independent technology company in San Francisco. We explore how intelligence can improve the way people live, work, create, and interact with their environments—while remaining useful, humane, legible, privacy-conscious, and worthy of trust.

This repository contains the source for [livingintelligence.xyz](https://livingintelligence.xyz/). The first version is intentionally small: a dependency-free static landing page built with HTML, CSS, and SVG.

## Project status

- The initial landing page and brand assets are ready in `www/`.
- The Git-connected Cloudflare Pages project is active at [livingintelligence-xyz.pages.dev](https://livingintelligence-xyz.pages.dev/), with `main` publishing `www/` automatically.
- No custom domain, production DNS, analytics, or guarded GitHub Actions release workflow is configured yet.
- The LinkedIn URL in the page is provisional and should be confirmed before launch.
- No open-source license has been selected. Public visibility does not grant permission to reuse the source or brand assets.

## Repository structure

```text
.
├── AGENTS.md              Repository instructions for coding agents
├── CLAUDE.md              Mirror of AGENTS.md for compatible tools
├── README.md
├── docs/
│   └── cloudflare-pages.md  Intended Pages environments and release behavior
└── www/
    ├── assets/             Favicons, app icons, vector mark, and social preview
    ├── index.html          Landing page, styles, and inline Fold animation
    ├── robots.txt          Search crawler policy
    ├── site.webmanifest    Web app metadata and icons
    └── sitemap.xml         Production sitemap
```

The Fold used in the hero is an inline SVG in `index.html`. The standalone `li-icon.svg` and PNG variants are used for browser, device, and social metadata.

## Run locally

No install or build step is required. From the repository root, run:

```sh
python3 -m http.server 8000 --directory www
```

Then open `http://localhost:8000/`.

The page currently loads IBM Plex Sans and IBM Plex Mono from Google Fonts. Self-hosting those font files is a possible follow-up if eliminating that runtime dependency becomes a launch requirement.

## Validate

The lightweight preflight for this static site is:

```sh
jq empty www/site.webmanifest
git diff --check
```

Before production launch, also verify the canonical URL, social preview, icon responses, outbound links, responsive layout, reduced-motion behavior, and the final custom-domain redirects.

## Deployment

The deployment plan follows Cloudflare Pages' standard Git integration, with `main` as the production branch and `www/` as the deployable static site:

1. Initially, automatic production deployments remain enabled and no custom domain is attached. Every push to `main` updates the project's Cloudflare-provided `*.pages.dev` site without introducing a separate preview subdomain.
2. At production cutover, `livingintelligence.xyz` is attached to the same Pages project and automatic production-branch deployments are disabled. A guarded, manually dispatched GitHub Actions workflow then deploys the selected `main` commit with Wrangler, using a typed `livingintelligence.xyz` confirmation, serialized deployment runs, Cloudflare credentials stored as GitHub environment secrets, and post-deploy checks. Preview deployments for pull requests and other branches can remain enabled.

The initial Cloudflare Pages project and Git deployment are active. The guarded custom-domain workflow is specified but deliberately remains unimplemented until production cutover; DNS, redirects, custom domains, and analytics are not configured.

See [the Cloudflare Pages deployment plan](docs/cloudflare-pages.md) for the intended environments, production release gate, verification, and rollback behavior.

## Contact

[hello@livingintelligence.xyz](mailto:hello@livingintelligence.xyz)
