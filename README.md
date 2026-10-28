# Indian Political Research

Source-backed Excel research workbooks on Indian political figures, covering their careers, elections, governance, political ideas, controversies, and legacy.

## Workbooks

| Figure | Workbook | Research date |
| --- | --- | --- |
| Atal Bihari Vajpayee | [Vajpayee political research](Atal_Bihari_Vajpayee_Political_Research.xlsx) | 24 September 2026 |
| Jyotiraditya Scindia | [Scindia political research](Jyotiraditya_Scindia_Political_Research.xlsx) | 4 October 2026 |
| J. Jayalalithaa | [Jayalalithaa political research](J_Jayalalithaa_Political_Research.xlsx) | 26 October 2026 |
| K. Chandrashekar Rao (KCR) | [KCR political research](KCR_Political_Research.xlsx) | 15 September 2026 |
| L. K. Advani | [Advani political research](L_K_Advani_Political_Research.xlsx) | 21 October 2026 |
| M. G. Ramachandran (MGR) | [MGR political research](M_G_Ramachandran_Political_Research.xlsx) | 25 October 2026 |
| M. Karunanidhi | [Karunanidhi political research](M_Karunanidhi_Political_Research.xlsx) | 14 September 2026 |
| Mamata Banerjee | [Banerjee political research](Mamata_Banerjee_Political_Research.xlsx) | 30 September 2026 |
| Narendra Modi | [Modi political research](Narendra_Modi_Political_Research.xlsx) | 24 September 2026 |
| Nirmala Sitharaman | [Sitharaman political research](Nirmala_Sitharaman_Political_Research.xlsx) | 24 September 2026 |
| Pinarayi Vijayan | [Vijayan political research](Pinarayi_Vijayan_Research.xlsx) | 15 September 2026 |
| Rahul Gandhi | [Rahul Gandhi political research](Rahul_Gandhi_Political_Research.xlsx) | 24 September 2026 |
| Sushma Swaraj | [Swaraj political research](Sushma_Swaraj_Political_Research.xlsx) | 5 October 2026 |

Research dates indicate each workbook's stated cutoff or evidence-access date, not the date of every underlying event or dataset. The Karunanidhi workbook's historical coverage runs through 7 August 2018.

## How to use

1. Download a workbook and open it in an application that supports `.xlsx` files, such as Microsoft Excel or LibreOffice Calc.
2. Start with **Overview**, then use the detailed worksheets and table filters to explore a topic or career phase.
3. Follow each record's source IDs to **Sources** for citations, links, and evidence limitations. Source IDs are local to each workbook. In the Vajpayee, Rahul Gandhi, Nirmala Sitharaman, Mamata Banerjee, Jyotiraditya Scindia, Sushma Swaraj, L. K. Advani, M. G. Ramachandran and J. Jayalalithaa workbooks, **All citations** opens every cited source link and **Claims** shows which fields have passage evidence.
4. Read claim types, procedural status, and qualification notes alongside the findings. In those nine workbooks, expand the **+** column group for supporting fields; the initial view prioritizes findings and review status.

## Workbook structure

All thirteen workbooks contain these worksheets; column layouts and depth vary by subject.

| Worksheet | Coverage |
| --- | --- |
| Overview | Identity, scope, key findings, and reading guide |
| Context & Constraints | Historical era, institutions, social conditions, and gender context |
| Career Timeline | Major events and career transitions |
| Elections | Contests, constituencies, results, and electoral context |
| Offices & Party | Governmental, legislative, and organizational roles |
| Policy & Governance | Initiatives, implementation, outcomes, and attribution |
| Ideas & Political Method | Ideology, communication, organization, and leadership |
| Controversies | Criticism, responses, accountability, and legal status |
| Legacy & Assessments | Attributed interpretations and competing assessments |
| Sources | Citation register and source-quality notes |

## Evidence and limitations

The workbooks distinguish documented facts, attributed positions, analysis, and uncertainty. Official records, scholarship, journalism, and interested accounts serve different evidentiary roles; consult the source notes before treating a claim as independently established.

An allegation is not a conviction, a policy announcement is not an implemented outcome, and a change during a leader's tenure does not by itself establish personal causal responsibility.

These are research snapshots, not exhaustive biographies or live datasets. Coverage gaps, conflicting records, and access limitations are noted within the workbooks. Verify time-sensitive claims against the cited records before relying on them, and distinguish publication dates from the periods the data describe.

The revised Vajpayee workbook adds **Claims**, **Evidence**, **Citations**, and **Research Queue**. Its 823 field-level assertions include 18 with newly recorded passage checks; the remaining 805 retain their earlier citations but are marked **Not reviewed** under the new evidence register. This describes documented review coverage, not the number of true or false historical claims. Compound fields require all their propositions to be checked before support is recorded. Methodology rows no longer cite the entire source list.

## Rebuilding and checking

The Vajpayee research is preserved in [research.json](research/atal-bihari-vajpayee/research.json), with inspected passages and unsuccessful retrievals in [retrievals.json](research/atal-bihari-vajpayee/retrievals.json). Rahul Gandhi's [research records](research/rahul-gandhi/research.json) and [retrieval register](research/rahul-gandhi/retrievals.json) use the same format: 210 registered fields, 201 supported passage checks or bounded syntheses, and nine unreviewed context gaps. These are review units, not a completeness or truth score. The reusable [research skill](workflow/indian-political-figure-research/SKILL.md) includes the builder and [pipeline instructions](workflow/indian-political-figure-research/references/pipeline.md). The remaining four workbooks have not been migrated.

Nirmala Sitharaman's [research records](research/nirmala-sitharaman/research.json) and [retrieval register](research/nirmala-sitharaman/retrievals.json) contain 45 sources and 242 reviewed fields, including explicitly bounded analysis. The research queue records eight open questions and one resolved document gap. Rajya Sabha counts are legislator votes; popular vote shares and single-opponent margins are inapplicable. Her [validation report](research/nirmala-sitharaman/validation.json) records the checks on the delivered workbook.

Mamata Banerjee's [research records](research/mamata-banerjee/research.json) and [retrieval register](research/mamata-banerjee/retrievals.json) cover five career phases, 13 personal elections and a 56-source register. Of 319 registered fields, 308 have passage support or bounded synthesis and 11 remain unreviewed. Ten research-queue entries preserve gaps in original returns, short ministerial tenures, recent legal outcomes and policy effects. The cutoff includes the 2026 government transition and September 28 reporting on the party-name dispute; the reported timetable and interim arrangements are distinguished from final decisions. See her [validation report](research/mamata-banerjee/validation.json) for workbook checks.

Jyotiraditya Scindia’s [research records](research/jyotiraditya-scindia/research.json) and [retrieval register](research/jyotiraditya-scindia/retrievals.json) cover five career phases, six Lok Sabha contests, one Rajya Sabha election and 45 sources. Of 221 registered fields, 212 have inspected-passage support or bounded synthesis; nine context fields remain unreviewed. The research queue contains ten open gaps and one resolved chronology discrepancy. Older vote counts use identified secondary fallbacks; the 2024 vote share is withheld pending a checked primary denominator. Policy records distinguish ministerial involvement, reported outputs and unestablished causal effects. See his [validation report](research/jyotiraditya-scindia/validation.json) for actual workbook checks.

Sushma Swaraj’s [research records](research/sushma-swaraj/research.json) and [retrieval register](research/sushma-swaraj/retrievals.json) cover four career phases, 11 direct contests, three Rajya Sabha elections and 47 sources. Of 230 registered fields, 222 have inspected-passage support or bounded synthesis; eight remain unreviewed. Twelve research-queue entries retain gaps in original returns, office boundaries, inaccessible diplomatic records and policy outcomes. Vote shares use inspected valid-vote denominators; unresolved shares remain blank. See her [validation report](research/sushma-swaraj/validation.json) for actual workbook checks.

L. K. Advani’s [research records](research/l-k-advani/research.json) and [retrieval register](research/l-k-advani/retrievals.json) cover five career phases, eight Lok Sabha constituency victories across seven general elections, four Rajya Sabha elections and 43 sources. Of 272 registered fields, 261 have inspected-passage support or bounded synthesis; 11 remain unreviewed. Fifteen research-queue entries preserve gaps in primary returns, office boundaries, complete judicial and commission records, and policy outcomes. The 1999 result uses the official segment-and-postal total of 453,229; the 2014 share denominator explicitly includes NOTA. Criminal outcomes, commission findings and political assessments are kept distinct. See his [validation report](research/l-k-advani/validation.json) for actual workbook checks.

M. G. Ramachandran’s [research records](research/m-g-ramachandran/research.json) and [retrieval register](research/m-g-ramachandran/retrievals.json) cover five career phases, five personal Assembly victories and a separately qualified 1962 Council entry. The 32-source register includes 26 inspected sources and six unresolved primary leads. Of 191 registered fields, 183 have inspected-passage support or bounded synthesis; eight remain unreviewed. Twelve research-queue entries preserve gaps in original election returns, office boundaries, inquiry exhibits, gender mechanisms and policy outcomes. The 1984 vote share is withheld pending a verified denominator. The 1980 interruption in government, later university operation and distinct press-privilege proceedings are preserved. See his [validation report](research/m-g-ramachandran/validation.json) for workbook checks.

J. Jayalalithaa’s [research records](research/j-jayalalithaa/research.json) and [retrieval register](research/j-jayalalithaa/retrievals.json) cover four career phases, nine personal Assembly contests, a Rajya Sabha election and the separately classified rejected 2001 nominations. The workbook has 43 sources and 211 registered fields: 198 supported by inspected passages or bounded synthesis and 13 unreviewed. Fifteen research-queue entries retain gaps in original returns, office boundaries, inquiry documents and policy outcomes. The six ministries are separate; the assets appeal against her abated on death, while the surviving co-accused’s convictions were restored. See her [validation report](research/j-jayalalithaa/validation.json) for the independent workbook checks.

With Python 3.10+ and the dependencies in `requirements-research.txt` installed:

```sh
python workflow/indian-political-figure-research/scripts/research_workbook.py research/atal-bihari-vajpayee/research.json --output Atal_Bihari_Vajpayee_Political_Research.xlsx
python -m unittest discover -s tests -v
```

The [validation report](research/atal-bihari-vajpayee/validation.json) separates structural checks, arithmetic, evidence review, application recalculation and visual inspection. A rebuild resets the last two checks until they are rerun on that workbook. The optional Numbers script exports disposable QA copies; the recalculation checker compares actual engine values against independent expectations. Formula caches are not fabricated: spreadsheet applications calculate the delivery workbook on opening, while viewers relying exclusively on stored caches may show blank formula cells.

## Repository scope

This repository contains research workbooks, reproducible research records, a maintained workflow skill, and its validation tests. Machine-specific QA exports, Python caches and the original skill ZIP archive are excluded. The archive itself is left unchanged.
