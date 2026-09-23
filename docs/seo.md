# Search discoverability plan

Reviewed: 2026-09-23. The repository implementation is approved. Release and submission evidence is recorded separately when those actions run.

## Findings and implemented changes

The public homepage returned HTTPS 200 without an `X-Robots-Tag: noindex` header during this review. Its public robots.txt allowed all crawlers and referenced the canonical sitemap. This is a single public-request observation, not proof that every crawler can reach the site through Cloudflare. Search Console coverage, Bing coverage, provider bot rules, and crawler logs were not available in this review.

Sample web searches for the brand and domain returned unrelated uses of “living intelligence,” other organizations, and third-party domain/business listings. The sample did not establish the website's Google position or prove that it is absent from an index. No search-volume or authenticated performance data was available. Prioritize queries that identify this particular company before broader category searches.

The proposed implementation:

- Keep the established name and tagline. State the company category and San Francisco location directly in homepage text and descriptions.
- Add the existing public legal name, Living Intelligence LLC, to Organization `legalName`. Retain the canonical domain as an alternative name, with stable organization, founder, and website identifiers.
- Add a linked `/about/` page with the company identity, founder, approach, project context, and contact information in static HTML. Give it a unique title, description, canonical URL, and AboutPage markup.
- Expand the canonical sitemap to include the About page and update modification dates to the content-edit date. Keep Pages provider hostnames non-indexable.
- Preserve the existing broad crawler permissions. Additional bot-specific Allow groups would not improve the current policy. Training permissions have not been changed.

## Query map

These are target query hypotheses, not measured search-volume claims. Related phrases share useful pages; do not create a separate thin page for every spelling.

| Priority | Query family | Target page and supporting content |
| --- | --- | --- |
| Primary | living intelligence; livingintelligence; living intelligence official website | `/`: brand heading, company description, canonical domain, WebSite markup |
| Primary | living intelligence xyz; livingintelligence.xyz; living intelligence website | `/` and `/about/`: canonical domain and visible official-site identity |
| Primary | living intelligence studio; living intelligence technology studio; living intelligence independent studio | `/`: studio description; `/about/`: studio approach and background |
| Primary | living intelligence llc; living intelligence company | `/about/`: visible legal name; Organization `legalName` on both pages |
| Secondary | living intelligence san francisco; living intelligence sf; living intelligence california | `/about/`: confirmed San Francisco identity and existing CA organization address |
| Secondary | living intelligence founder; living intelligence alex filipe; living intelligence álex filipe santos | `/about/`: founder attribution and link to the founder's website |
| Secondary | living intelligence contact; living intelligence email | `/about/`: contact heading and public email |
| Secondary | living intelligence projects; living intelligence aetherloom; living intelligence home intelligence | `/about/`: project descriptions and primary-source links |
| Exploratory | independent technology studio san francisco; privacy conscious technology studio; human centered technology studio | `/about/`: approach, supported by concrete project work; broader competition and intent need measurement |

Do not present “Living Intelligence Studio” or “Living Intelligence XYZ” as additional registered/trading names merely to match queries. The studio description and real domain support those searches naturally. Do not invent services, locations, clients, reviews, or product availability to target broader keywords.

## Google, ChatGPT, and Gemini

Google's guidance emphasizes indexable text, internal links, crawl access, and structured data that matches visible content. AI Overviews and AI Mode use the same foundations. There is no required AI-specific schema or text file. See [Google's AI features guidance](https://developers.google.com/search/docs/appearance/ai-features).

The homepage's WebSite name and domain alternative support recognition of the site name. Organization details help distinguish the company. They do not guarantee a knowledge panel, rich result, or ranking. See [site names](https://developers.google.com/search/docs/appearance/site-names) and [Organization markup](https://developers.google.com/search/docs/appearance/structured-data/organization).

ChatGPT search uses OAI-SearchBot. It is allowed by the current wildcard robots rule. OpenAI also recommends permitting its published crawler IP ranges through hosting controls. A successful request with a spoofed user-agent would not prove access for the actual crawler IPs. GPTBot controls potential model-training use separately and is not a prerequisite for search visibility. See [OpenAI crawler documentation](https://developers.openai.com/api/docs/bots).

Googlebot controls Google Search crawling. Google-Extended controls training and grounding uses in Gemini Apps and certain other Google systems; it is not a Google Search ranking signal. The existing wildcard policy permits it. This review makes no promise about Gemini citations or model recall. See [Google's crawler controls](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended).

No keyword meta tag, hidden keyword block, fabricated schema, doorway pages, or speculative `llms.txt` ranking mechanism is included. IndexNow uses the root verification file and `scripts/submit_indexnow.py`; a successful API response confirms receipt, not indexing or ranking.

## Highest-impact work after review

1. Release the approved commit through the existing manual production-domain workflow, following [the hosting procedure](cloudflare-pages.md). A push to `main` updates the separate `pages.dev` project only. Verify both canonical pages, sitemap, redirects, headers, and intended content on the public domain before requesting indexing.
2. In Google Search Console, verify ownership if needed, submit `https://livingintelligence.xyz/sitemap.xml`, and inspect `/` and `/about/`. Check live crawl results, selected canonical, indexing exclusions, manual actions, and security issues. Request indexing after the production release. Record any specific exclusion and address its cause. See [Google's recrawl instructions](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).
3. Verify the site in [Bing Webmaster Tools](https://www.bing.com/webmasters/) and submit the same sitemap. Inspect indexing diagnostics. Do not assume that Google indexing establishes Bing indexing or AI inclusion.
4. Inspect Cloudflare bot and WAF settings and logs for verified Googlebot, Bingbot, and OAI-SearchBot requests. Correct demonstrated blocks with narrowly scoped rules. Preserve security protections and preview-host noindex rules. This requires provider access and is not implemented in the website files.
5. Confirm the exact LinkedIn company URL, still marked provisional in README.md. Ensure the company-owned LinkedIn and GitHub profiles use the same brand, description, and website. The founder and project pages already link to the studio; keep those real relationships accurate. Do not buy links or create artificial profiles.
6. Publish substantive project progress, technical case studies, and release notes as real work becomes available. Explain the problem, design choices, status, and evidence. Link from relevant project repositories and genuine professional profiles. Avoid duplicating project websites or publishing generic AI articles solely to capture the ambiguous phrase.

Account verification and external profile edits have not been performed. Production releases and IndexNow submissions must be recorded when run. Rankings and AI citations remain controlled by the respective services.

## Measurement

Capture a pre-release baseline and review weekly after release. In Search Console, group queries by brand, studio, domain, legal name, location, founder, and project. Record impressions, clicks, CTR, average position, landing page, date range, country, and device. Treat `site:` queries as spot checks rather than coverage reports.

For ChatGPT and Gemini, periodically test the same small set of prompts, such as “What is Living Intelligence, the technology studio in San Francisco?” and “What is the official website of Living Intelligence LLC?” Record the date, product/mode, exact prompt, whether web search was used, linked URL, and factual accuracy. These are variable observations, not stable rankings. Existing referrals and platform reports can supplement this without adding website analytics.

Success means the correct company and canonical website become easier to find and identify. Technical validation confirms eligibility and consistency; it cannot certify index inclusion, a first-page placement, or a particular AI answer.
