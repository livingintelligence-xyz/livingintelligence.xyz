# Living Intelligence

**Intelligence for living, that lives.**

Living Intelligence is an independent technology company in San Francisco. We explore how intelligence can improve the way people live, work, create, and interact with their environments—while remaining useful, humane, legible, privacy-conscious, and worthy of trust.

This repository contains the source for [livingintelligence.xyz](https://livingintelligence.xyz/). The first version is intentionally small: a dependency-free static landing page built with HTML, CSS, and SVG.

## Project status

- The initial landing page and brand assets are ready in `www/`.
- Cloudflare Pages and DNS are not configured yet.
- The LinkedIn URL in the page is provisional and should be confirmed before launch.
- No open-source license has been selected. Public visibility does not grant permission to reuse the source or brand assets.

## Repository structure

```text
.
├── README.md
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

The intended production host is Cloudflare Pages, connected to this repository with `main` as the production branch and `www/` as the deployable static site. Hosting, DNS, redirects, and analytics are deliberately not configured in this initial repository setup.

## Contact

[hello@livingintelligence.xyz](mailto:hello@livingintelligence.xyz)
