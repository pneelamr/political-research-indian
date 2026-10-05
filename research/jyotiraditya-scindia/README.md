# Jyotiraditya Madhavrao Scindia — research record

Completed research snapshot as of 4 October 2026. The user-facing artifact is `Jyotiraditya_Scindia_Political_Research.xlsx` in the repository root.

The workbook covers five career phases, six Lok Sabha contests and one Rajya Sabha election. It contains 45 source entries, 161 authored substantive/method records, 221 registered fields and 371 passage-evidence links. Of the registered fields, 212 are supported facts or bounded syntheses; nine context fields remain unreviewed. Ten research questions remain open and one date discrepancy is resolved for this edition. Counts describe review coverage, not exhaustive truth or completeness.

Source access: 38 inspected passages, four search-only candidates and three access failures. Unavailable sources cannot support reviewed fields. Several official HTML notices were retrieved directly after web-tool failure. The attempted parliamentary PDF for export costs returned HTML; its savings estimate remains provisional. Same-letter Digi Yatra reports and the CAG summary/full-report candidate share origin identifiers.

`author_sources.py`, `author_context.py` and `author_research.py` reproduce the normalized records. `research.json` contains tables, claims, evidence, coverage and gaps; `retrievals.json` preserves short passage paraphrases and unsuccessful retrieval outcomes. `validation.json` binds actual checks to the delivered workbook hash.

From the repository root, with the research dependencies installed:

```sh
python research/jyotiraditya-scindia/author_research.py
python workflow/indian-political-figure-research/scripts/research_workbook.py research/jyotiraditya-scindia/research.json --output Jyotiraditya_Scindia_Political_Research.xlsx
```

A rebuild resets application and visual QA. This edition passed structural/provenance checks, 3,075 internal/external hyperlink-format and destination checks, all eight actual Numbers formula results, and the 12 existing pipeline regression tests. External URL network availability is recorded in retrievals, not certified by the hyperlink checks.

All 14 Numbers-rendered sheets were visually sampled, along with dense regions and seven expanded-column regions. A final evidence-link correction was checked in a fresh Numbers export: 13 rendered pages retained identical text and dimensions; the altered Evidence passage was cropped and inspected. The final file was not replaced by Numbers’ export. Formula caches were not fabricated, so cache-only viewers can show blank formula cells until a spreadsheet engine recalculates them.

QA PDFs, screenshots and application exports remain in a disposable temporary directory; their hashes, region definitions and limits are preserved in validation.json. The final deliverable retains the reviewed dimensions and grouped detail columns.
