# Living Intelligence

**Intelligence for living, that lives.**

Living Intelligence is an independent technology company in San Francisco. We explore how intelligence can improve the way people live, work, create, and interact with their environments—while remaining useful, humane, legible, privacy-conscious, and worthy of trust.

This repository contains the source for [livingintelligence.xyz](https://livingintelligence.xyz/). The first version is intentionally small: a dependency-free static landing page built with HTML, CSS, and SVG.

## Project status

- The initial landing page and brand assets are ready in `www/`.
- The Git-connected Cloudflare Pages project is active at [livingintelligence-xyz.pages.dev](https://livingintelligence-xyz.pages.dev/), with `main` publishing `www/` automatically.
- No separate production Pages project, custom domain, production DNS, analytics, or manually dispatched domain-release workflow is configured yet.
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
├── scripts/
│   ├── build_og.py          Generates the Open Graph SVG and PNG artwork
│   └── build_social.py      Generates the broader social artwork kit
└── www/
    ├── assets/             Favicons, app icons, vector mark, and social preview
    ├── index.html          Landing page, styles, and inline Fold animation
    ├── robots.txt          Search crawler policy
    ├── site.webmanifest    Web app metadata and icons
    └── sitemap.xml         Production sitemap
```

The Fold used in the hero is an inline SVG in `index.html`. The standalone `li-icon.svg` and PNG variants are used for browser, device, and social metadata.

## Brand asset generators

The source generators for the checked-in Open Graph and social artwork live in `scripts/`. They are optional design-time utilities, not dependencies of the deployed site. Each script documents its setup and outputs; `build_social.py` additionally requires Pillow for PNG rendering.

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

The deployment policy uses two independent Cloudflare Pages targets, with `www/` as the deployable static site:

1. The existing Git-connected project automatically publishes every commit to `main` at [livingintelligence-xyz.pages.dev](https://livingintelligence-xyz.pages.dev/). That automation stays enabled permanently, including after the custom domain launches.
2. A future separate Pages project will serve `livingintelligence.xyz` and will not use Git-triggered deployments. A manually dispatched GitHub Actions workflow may deploy any commit verified as belonging to `main`, using Wrangler, serialized runs, Cloudflare credentials stored as GitHub environment secrets, and post-deploy checks.

The automatic `pages.dev` project is active. The independent custom-domain project and its manual release workflow are specified but remain unimplemented; DNS, redirects, custom domains, and analytics are not configured.

See [the Cloudflare Pages deployment plan](docs/cloudflare-pages.md) for the independent deployment targets, manual domain-release workflow, verification, and rollback behavior.

## Contact

[hello@livingintelligence.xyz](mailto:hello@livingintelligence.xyz)
