# Living Intelligence

**Intelligence for living, that lives.**

Living Intelligence is an independent technology company in San Francisco. We explore how intelligence can improve the way people live, work, create, and interact with their environments—while remaining useful, humane, legible, privacy-conscious, and worthy of trust.

This repository contains the source for [livingintelligence.xyz](https://livingintelligence.xyz/). The first version is intentionally small: a dependency-free static landing page built with HTML, CSS, and SVG.

## Project status

- The initial landing page and brand assets are ready in `www/`.
- The Git-connected Cloudflare Pages project is active at [livingintelligence-xyz.pages.dev](https://livingintelligence-xyz.pages.dev/), with `main` publishing `www/` automatically.
- The separate Direct Upload production project is live at [livingintelligence.xyz](https://livingintelligence.xyz/), with releases controlled by the manually dispatched domain-release workflow and `www` permanently redirected to the apex.
- The LinkedIn URL in the page remains provisional and should be confirmed.
- No open-source license has been selected. Public visibility does not grant permission to reuse the source or brand assets.

## Repository structure

```text
.
├── AGENTS.md              Repository instructions for coding agents
├── CLAUDE.md              Mirror of AGENTS.md for compatible tools
├── README.md
├── .github/workflows/
│   └── deploy-production.yml  Manual production-domain release workflow
├── docs/
│   └── cloudflare-pages.md  Intended Pages environments and release behavior
├── scripts/
│   ├── build_og.py          Generates the Open Graph SVG and PNG artwork
│   └── build_social.py      Generates the broader social artwork kit
└── www/
    ├── _headers            Host-specific crawler policy for Pages hostnames
    ├── 404.html            Branded not-found response for unknown paths
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

The page self-hosts IBM Plex Sans and IBM Plex Mono as WOFF2 files under `www/assets/fonts/`. Their SIL Open Font License is stored alongside the font files. No font request leaves the site at runtime.

## Validate

The lightweight preflight for this static site is:

```sh
jq empty www/site.webmanifest
git diff --check
```

For production releases, also verify the canonical URL, social preview, icon responses, outbound links, responsive layout, reduced-motion behavior, and the custom-domain redirects.

## Deployment

The deployment policy uses two independent Cloudflare Pages targets, with `www/` as the deployable static site:

1. The existing Git-connected project automatically publishes every commit to `main` at [livingintelligence-xyz.pages.dev](https://livingintelligence-xyz.pages.dev/). That automation stays enabled permanently, including after the custom domain launches.
2. The separate Direct Upload project `livingintelligence-xyz-production` serves `livingintelligence.xyz` and does not use Git-triggered deployments. The manually dispatched GitHub Actions workflow may deploy any commit verified as belonging to `main`, using Wrangler, serialized runs, Cloudflare credentials stored as GitHub environment secrets, and post-deploy checks.

Both deployment paths are active and independent. The production apex and `www` DNS records point only to the Direct Upload project, and `www` permanently redirects to the apex while preserving paths and query strings. Analytics is not configured.

See [the Cloudflare Pages deployment plan](docs/cloudflare-pages.md) for the independent deployment targets, manual domain-release workflow, verification, and rollback behavior.

## Contact

[hello@livingintelligence.xyz](mailto:hello@livingintelligence.xyz)
