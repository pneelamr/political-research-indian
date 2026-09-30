# Reproducible research and validation

Keep research records alongside the workbook when the user authorizes internal build material. The `.xlsx` remains the main deliverable. Use stable record IDs rather than subject-specific row indexes, and retain source and claim IDs across rebuilds.

## Bundled builder

Requires Python 3.10+ and openpyxl 3.1. Use an existing compatible environment, or install the dependency through the normal permission flow.

```sh
python scripts/research_workbook.py /path/research.json --output /path/Profile.xlsx
```

The script reads adjacent `retrievals.json` and writes adjacent `validation.json` unless `--report` specifies another path. It performs no network requests, GUI automation or source verification. It never manufactures formula caches. Rebuilding resets application/visual results to `NOT RUN`, so an old pass cannot silently certify a new workbook.

`research.json` version 1 contains:

- `subject`, `as_of`, `guidance`, and `schema_version: 1`.
- `tables`: sheet name to `lead_columns`, `date_columns` and `rows`. Each row is an ordered object whose first field is its stable ID; substantive rows have explicit semicolon-separated `Source IDs`. `Overview` uses `Topic`, `Finding / value` and `Claim type`. Method rows use `Method / scope` and need no external citations.
- `sources`: stable `Source ID`, title, institution, dates, URL, source class, limitations, locator, `Access status` and `Origin ID`. Existing row schemas are described in workbook-schema.md.
- `claims`: `id`, `sheet`, `record_id`, `field`, exact `statement`, SHA-256 `fingerprint` of the JSON value (`ensure_ascii=False`, `sort_keys=True`), `claim_type`, `status`, `priority`, `candidate_source_ids`, `evidence_ids`, `contradictions`, and `review_note`. Dates are ISO strings. A changed statement invalidates its old fingerprint and requires re-review; updating the hash alone does not revalidate evidence.
- `evidence`: `id`, `claim_id`, `source_id`, `retrieval_id`, `locator`, `passage_paraphrase`, `relation`, `reviewed_by`, `reviewed_at`, and `note`. A `Supported` claim requires recorded support and no unresolved contradiction. For a disputed claim requiring multiple independent origins, set `requires_independent_corroboration: true`.
- `coverage`: the full expected `Era` and `Gender` item names; `phases`: expected era phases. The builder checks checklist equality and context references. These configured lists must reflect the complete standards, not be shortened to fit incomplete research.
- `gaps`: `id`, `priority`, `topic`, `gap`, `next_action`, `record_ids`, and `status`.

This builder supports the standard workbook fields and configurable subjects, row counts and presentation columns. It is not an arbitrary spreadsheet generator. Optional sections may be empty, but Overview and the required context table should exist. The repository's Vajpayee dataset is a complete example of this format; a new project should supply its own records, not copy historical assertions.

## Retrieval cache and stopping rule

`retrievals.json` is an array of retrieval attempts with stable `id`, source ID, exact attempted URL or query, access date, route, access status, underlying `origin_id`, locator, short relevant passage/paraphrase, method, result and next action. Retain failed attempts. `Passage inspected` means the relevant text was actually read, not that the entire document was inspected or that every claim citing it is supported.

Before a new retrieval, consult this cache. Reuse inspected historical material unless the claim or source changed. For a failed record, try one promising route at each of canonical institution, official mirror and credible reproduction, stopping when further attempts repeat the same obstacle. Leave the claim pending if no inspected passage supports it. Save small extracts rather than unnecessary full-text copies; retain a checksum and local path when an original document is downloaded legitimately.

## Application validation

Structural checks do not prove factual accuracy, recalculation or layout quality. `validation.json` records those categories independently, the workbook hash and Python-derived expected formula results.

On a Mac with Numbers Creator Studio, `scripts/numbers_qa.applescript` opens an explicitly supplied disposable copy, exports recalculated Excel and rendered PDF copies, then closes without saving. Running GUI automation may require filesystem or macOS permission. Use existing authorization; do not infer a separate publication approval requirement. It never uploads or publishes the workbook.

```sh
osascript scripts/numbers_qa.applescript /absolute/input-copy.xlsx /absolute/recalculated.xlsx /absolute/rendered.pdf
```

Use `scripts/check_recalculation.py` to compare engine-produced values with the recorded expectations. Numbers can reposition tables, so the comparison resolves headers and stable record IDs instead of assuming original cell coordinates. Keep the delivery workbook's formatting intact. A successful export alone is not a recalculation pass or a visual check. Inspect actual PDF/app renderings for each worksheet and dense regions; record precisely what was inspected and any import warnings. Expanded detail columns also need inspection when relying on their layout. State untested applications and regions.

The original workbook retains formulas with empty caches and recalculates on opening. Applications that display only cached values may show blank formula results; report this if applicable. Never insert independently computed values and call them engine verification.
