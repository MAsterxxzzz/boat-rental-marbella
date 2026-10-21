# Finding: "Sunseeker Predator 55" does not exist in the fleet

**Status:** new finding today — documented for your decision, not applied.
This affects 8 real content pages (bulk scope), so it is being filed as a
proposal rather than edited directly, consistent with the standing
one-page/one-evidenced-change-per-run rule and the requirement that bulk
edits need your explicit go-ahead.

## What's wrong

8 live, real-content comparison pages are built entirely around a boat
called "Sunseeker Predator 55," used 50+ times each in body copy, FAQs,
and JSON-LD. The actual fleet (`site/boats/`) has no Predator 55 — only
**Sunseeker Predator 58** and **Sunseeker Predator 72** exist as bookable
boats.

A visitor who finds one of these pages via search for "Sunseeker Predator
55 Marbella" cannot actually book that boat — it isn't offered. That's a
real risk to the stated goal (qualified enquiries that convert to
bookings), not just a cosmetic issue.

## Affected pages (8, all real content, all in scope for a future fix)

- `/azimut-39-vs-sunseeker-predator-55-marbella-comparison/`
- `/astondoa-40-vs-sunseeker-predator-55-marbella-comparison/`
- `/pershing-46-vs-sunseeker-predator-55-marbella-comparison/`
- `/blog/pershing-46-vs-sunseeker-predator-55-marbella/`
- `/blog/pershing-46-vs-sunseeker-predator-55-marbella-comparison/`
- `/blog/mangusta-80-vs-sunseeker-predator-55-marbella/`
- `/blog/mangusta-80-vs-pershing-46-vs-sunseeker-predator-55-marbella-comparison/`
- `/blog/azimut-39-vs-sunseeker-predator-55-marbella/`

**Excluded, do not touch without separate approval:**
- `/blog/astondoa-40-vs-sunseeker-predator-55-marbella-comparison-2036/` —
  real content but carries a fabricated future year (2036), covered by the
  existing standing exclusion for the ~149 future-dated pages pending your
  separate review.
- `pershing-46-vs-sunseeker-predator-55-marbella-comparison-{2026,2042,2043}/`
  under `/blog/` — these are `<title>Redirected</title>` stubs (512 bytes),
  not real content; nothing to fix.

## Options for you to choose between (not pre-decided)

1. **Rename "Predator 55" → "Predator 58" throughout the 8 pages** if the
   boat was simply renamed/renumbered at some point and the comparison
   intent still holds (specs would need re-checking against the real
   Predator 58 page — I have not assumed the numbers transfer).
2. **Retire/redirect these 8 pages** if Predator 55 was never actually in
   the fleet and the comparisons don't make sense for any real boat.
3. **Leave as-is** if there's a reason I'm not aware of (e.g. a boat that
   was removed from the fleet but customers still ask about).

I have not guessed which is correct and have not invented replacement
specs — that would violate the no-fabrication rule. Whichever direction
you pick, I can execute it as a reviewed bulk change once you confirm, the
same way the footer `</p>` rollout below is staged and waiting.

## Related, already-filed proposal (unchanged, still awaiting approval)

`reports/proposals/footer-p-tag-fix-2026-10-04.{md,json}` — the 728-file
rollout of the already-template-fixed footer `</p>` tag. Re-verified today:
proposal content is still byte-identical to 2026-10-04, repo HEAD has not
changed since, no approval marker found. Still valid, still waiting on you.
