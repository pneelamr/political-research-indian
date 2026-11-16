# M. Venkaiah Naidu research — completed checkpoint

Research cutoff and completion date: 2026-11-08. The continuous research run is complete. No subagents used.

## Delivered workbook

`M_Venkaiah_Naidu_Political_Research.xlsx` in the repository root: 14 sheets, 44 sources, 298 registered fields, 496 evidence bindings and 431 citation rows. Six career phases have 60 era-context items, with 10 additional gender-context items. Of the registered fields, 282 are supported, 15 are explicitly unreviewed and one is disputed. These counts describe review units, not completeness or historical truth.

SHA-256: `2ec535c1a323b7ea6e8630bad8a9b4f9d957d16634cc2f271065914dfd4b1d70`.

## Checks completed

- Structural and provenance integrity checks passed; all 4,127 workbook hyperlinks were checked for valid internal destinations where applicable.
- Independent arithmetic confirmed six direct contests, two victories and four defeats; the unverified 1991 contest is excluded. Candidate shares and turnout use different denominators.
- Numbers Creator Studio recalculated all 11 formulas correctly. Its exported workbook contains no spreadsheet error cells.
- Actual Numbers PDF exports were rendered and visually inspected on all 14 sheets, with dense evidence/context sections and seven expanded-column regions checked separately. The expanded QA copy has identical values and formulas. Visual inspection is sampled, not a claim that every cell was individually viewed.
- `validation.json` records the delivered workbook hash and checks; `qa_review.json` records render hashes, inspected image regions and substantive review boundaries. Disposable exports are in `/private/tmp/venkaiah-research-qa/` and can expire.

## Resolved research issues

- The official 1977 Ongole result predates the commonly asserted maiden 1978 contest. Preserve the ECI's BLD and JNP labels for 1977 and 1978 respectively.
- The 1978 Udayagiri margin is 9,660. The 1985 defeat was at Atmakur by 830 votes. The 1996 Hyderabad valid-vote denominator is 928,704; the preceding constituency's total must not be reused.
- The complete Rajya Sabha member book was downloaded and inspected at printed pages 8 and 317 (PDF pages 25 and 334). Terms are 3 April 1998–2 April 2004; 1 July 2004–30 June 2010; 1 July 2010–23 June 2016; 5 July 2016–10 August 2017. G02 is resolved; do not flatten these into continuous service.
- Housing and Urban Affairs was created on 6 July 2017 and his tenure ended on 17 July. Earlier Urban Development and HUPA portfolios remain separate, as do Parliamentary Affairs and Information and Broadcasting.
- UN-Habitat office is the Governing Council presidency, not executive leadership of the agency.
- Procedural distinctions are retained for the Bhopal land judgment, CJI removal notice, NDTV broadcast order, and parliamentary suspensions. Harivansh chaired the 20 September 2020 farm-bill passage; Naidu's subsequent ruling is a separate event.

## Future research queue

Nine open questions remain explicit in the workbook. Highest priority: reconcile the alleged 1991 personal contest against complete candidate lists and contemporary reporting. Other gaps include the original 1983 return and denominator; underlying land, FCRA and procurement records; tenure-bounded policy outcomes; committee contributions; comparative gender/media evidence; the full 2002 presidential speech; some era dimensions; and precise BJP/UN-Habitat tenure endpoints. These gaps are not silently treated as supported facts.

## Rebuild and resume

`author_sources.py` contains source and retrieval records. `author_research.py` creates the normalized research records. With Python 3.10+ and the repository research dependencies installed, run:

```sh
python research/m-venkaiah-naidu/build.py
```

This rebuild resets application recalculation and visual validation. Rerun the shared Numbers QA export, `check_recalculation.py`, and rendering workflow before delivering a rebuilt workbook. `prepare_qa.py` produces the disposable expanded-column copy; `render_regions.swift` crops actual rendered pages without reflow. Do not reuse the old visual-review PASS for a new workbook hash.

Future sessions should start with this checkpoint and the workbook's Research Queue, preserve existing source/claim IDs, and add newly inspected evidence before changing review status. No required delivery work remains from this run.
