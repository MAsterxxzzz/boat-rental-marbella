# Google Business Profile + reviews playbook (set up 2026-10-22)
- Profile: "Boat Rental Marbella", ID 04776167351325622283, owner account andra.kiirkivi@gmail.com. Verified by SMS 2026-10-22. Edits pending Google review: categories (Boat Hire Service + Boat tour agency), 4 services, logo, 4 photos. Hours 08:00-22:00 live.
- Review link (HTTP-tested; resolves to search.google.com/local/writereview?placeid=ChIJ-4RoRehj4CkRJFBrpxEnNZ4): https://g.page/r/CSRQa6cRJzWeEBM/review
- Kit handed to owner: QR code, printable card, WhatsApp/email templates (EN/ES/DE/NL/FR), after-trip routine. No incentives, no review gating, no fake reviews.

## Pending (do not skip; routine/owner)
1. Owner confirms the profile is public (Maps search "Boat Rental Marbella" shows it) and that the review link opens a working review box on a phone. As of 2026-10-22 12:30 UTC it was NOT public yet (listing still "Only managers of this profile can see this").
2. THEN add to `/reviews/` hero actions (existing class `btn-hero-ghost`): `<a class="btn-hero-ghost" href="https://g.page/r/CSRQa6cRJzWeEBM/review" rel="noopener" target="_blank">Review us on Google</a>` (1-line diff, `site/reviews/index.html`; 14-day rule applies).
3. THEN add the Google profile URL (Maps place link) to `sameAs` in the Organization JSON-LD and the footer — needs the public Maps URL from the owner.
4. Reviews page wording ("verified charters", "no paid reviews") still needs owner confirmation (see reports/proposals/claims_wording_for_approval_2026-10-22.md).
