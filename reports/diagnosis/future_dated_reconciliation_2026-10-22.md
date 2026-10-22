# Future-dated URL counts — reconciliation (2026-10-22)
Rule used: a page directory whose path contains a year 2027–2099. Full list: `future_dated_urls_2026-10-22.csv` (561 rows; column `is_redirect_stub`, `in_proposal`, `in_sitemap`, `future_year`).

| Count | What it is |
|---|---|
| **561** | all page folders with a future year in the path |
| 332 | of those are `<title>Redirected</title>` meta-refresh stubs (all in `/blog/`; 0 in the sitemap) |
| **229** | real (non-redirect) pages with a future year |
| 98 / 93 / 38 | the 229 split: `/blog/` / `/experiences/` / top-level (35 root + 3 `/spoke/`) |
| **191** | = 98 blog + 93 experiences (the figure used in the 2026-10-22 diagnosis; it omitted the 38 top-level pages) |
| **149** | real pages with year **≥ 2030**: the pending proposal `future_dated_pages_proposal.{md,json}` (58 rename-to-canonical, 91 redirect) |
| **80** | real pages with year **2027–2029** (37 / 23 / 20): **not covered by the proposal** (it only took ≥ 2030) |
| 219 | of the 229 are in `sitemap.xml` |
So 98 vs 191 differ only by scope (blog-only vs blog+experiences); 149 is the year ≥ 2030 subset; the true total of real future-year pages is 229. Nothing was changed. The 80 pages dated 2027–2029 need an explicit decision, as does anything bulk. Note: the proposal files existed only on the local machine until now; they are added to the repo so the cloud routine can see them.
