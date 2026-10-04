# Proposal: apply the footer `</p>` fix to already-built pages

**Status:** awaiting your review — not applied. One at-most-one-change-per-run
policy and a hard boundary against unreviewed bulk edits across many files
both apply here, so this is written up for approval rather than run directly.

## What's wrong

`templates/page.html.template` generates every page's footer. The "Contact"
column's chip paragraph never got closed properly:

```html
<p class="footer-contact">
  ...WhatsApp / email / Instagram / Facebook chips...
</div>   <!-- should be </p> -->
</div>
</div>
<div class="container footer-legal">
```

This is a real, verified HTML-validity defect (confirmed by hand, not just
the linter): one closing tag has the wrong tag name. It does **not** change
anything visible (browsers already recover), but it means ~877 pages don't
parse as valid HTML.

**Already fixed:** the template source itself, in commit `778bf84`
(`templates/page.html.template`). That commit has no live effect by itself
— it only affects pages built from the template *in the future*. It did not
trigger a GitHub Pages deploy (the workflow only watches `site/**`).

**Not yet fixed:** the 877 already-built files under `site/` still have the
old, wrong markup, because they were generated before the template fix.

## The exact mechanical patch

In each affected file, replace:

```
        </a>

      </div>
    </div>
  </div>
  <div class="container footer-legal">
```

with:

```
        </a>

      </p>
    </div>
  </div>
  <div class="container footer-legal">
```

Only the **first** `</div>` after the last footer chip becomes `</p>`; the
other two closing `</div>`s are untouched. This was dry-run verified against
every matching file: exactly one match per file, same line count, one
character added, no other content touched (no prices, fleet details, text,
or links change).

## Scope: 728 files safe to fix now, 149 deliberately excluded

- **728 files** — regular pages, safe to patch immediately. Full list with
  URLs: `reports/proposals/footer-p-tag-fix-2026-10-04.json` →
  `safe_to_fix`.
- **149 files** — excluded because they are exactly the fabricated-future-year
  (2030+) pages that are already under a separate pending review (the
  future-dated-pages proposal). This footer bug exists on them too, but they
  are left untouched until that separate decision is made, per standing
  instructions. Full list: same JSON file → `excluded_future_dated_pending_separate_proposal`.

## If you approve

Say so and the next run will apply the exact substitution above to the 728
safe files in one commit, re-run `technical_crawl_check.py` to confirm the
HTML-validity count drops from 877 to 149 (only the excluded pages
remaining) with no new issues, push, and verify the live site. The 149
excluded pages would then be handled together with whatever you decide on
the future-dated-pages question.
