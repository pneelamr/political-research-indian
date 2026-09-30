---
name: indian-political-figure-research
description: Research one or more figures in Indian politics and produce a source-backed Excel workbook covering biography, offices, elections, governance, political ideas and methods, controversies, and legacy. Use for substantial political profiles or comparisons; do not use for a quick factual answer or an uncited opinion piece.
---

# Indian Political Figure Research

Create a rigorous, readable `.xlsx` research workbook about an Indian political figure. Support multiple figures in one comparative workbook only when the user asks for comparison or a cohort study; otherwise create one workbook per figure.

## Establish the Scope

Identify the figure unambiguously, including common initials, name variants, party or parties, principal jurisdiction, and career period. Record an `As of` date for living or politically current figures.

Infer a standard research scope unless the user requests a narrower emphasis. A standard scope covers:

- formative background and entry into public life;
- elected, governmental, parliamentary, party, movement, and opposition roles;
- election history and political geography;
- policies, administrative record, legislation, diplomacy, movements, and institution-building;
- ideology, stated positions, constituency or social base, alliances, rivals, and political method;
- crises, criticism, controversies, and legal or institutional accountability;
- leadership, communication, cultural or intellectual work when politically relevant;
- gender and other identity-related opportunities, constraints, treatment, strategies, and representative significance;
- the changing party system, institutions, economy, international order, media environment, social conditions, and evidence environment across each career phase;
- historical significance, competing assessments, and legacy.

Do not force equal depth across every category. Allocate space according to the figure's actual career. For example, a movement founder needs movement-building and state-formation coverage; a foreign minister may need diplomacy and parliamentary work rather than a chief-ministerial scorecard.

Before researching, read [references/research-standards.md](references/research-standards.md). Before building the workbook, read [references/workbook-schema.md](references/workbook-schema.md).

## Research

Browse for current and historical evidence. Prefer primary institutional records for dates, offices, votes, election results, statutes, judgments, commission findings, speeches, and official actions. Use high-quality scholarship and independent reporting to establish context, consequences, disputes, and retrospective assessment. Treat party publications, memoirs, campaign material, and the subject's own statements as attributed primary evidence, not neutral validation.

Build the source register and claim register while researching, with stable IDs. Every substantive record must cite candidate sources; mark a claim supported only after checking its complete wording against an inspected passage and recording the locator, access status, review result and any contradiction. Citation presence is not verification. Use at least two independent, credible sources for a materially contested claim when reasonably available; mirrors and syndicated copies of one record count as one origin.

Prioritize identity, office chronology, election results and major contested claims before expanding narrative coverage. Keep an ordered queue of unresolved core facts. Report reviewed coverage and open gaps separately from record counts. Cache retrieval outcomes and short relevant excerpts or paraphrases, including unsuccessful attempts. For access failures, try the canonical record, an official mirror, then a credible reproduction; record the remaining gap rather than repeatedly searching equivalent URLs. Revisit a stopped search only when new evidence or a better route appears. See [references/pipeline.md](references/pipeline.md) for durable records and executable build support.

Separate these layers throughout the research:

1. **Recorded fact** — dates, office, vote, law, order, documented action.
2. **Attributed position** — what the figure, party, critic, court, scholar, or institution said.
3. **Analysis** — a reasoned synthesis supported by identified evidence.
4. **Uncertainty or dispute** — unresolved chronology, causation, attribution, or interpretation.

Never convert praise, criticism, a nickname, an allegation, or a popular narrative into an unattributed fact. Do not infer caste, religious, linguistic, regional, or ideological identity beyond reliable evidence.

## Gender and Era Context

Research gender and historical era for every figure. Use one common evidentiary standard and core schema for all figures, then document whether and how these contexts affected political access, conduct, reception, power, and legacy. Do not assume that gender was politically decisive in every event, or that a career spanning decades belongs to one static era.

Complete every coverage item in the `Gender` and `Era` checklists in [references/research-standards.md](references/research-standards.md). Capture the resulting evidence in the `Context & Constraints` table defined in [references/workbook-schema.md](references/workbook-schema.md). When a point is not materially relevant or reliable evidence is unavailable, record that research disposition explicitly rather than silently omitting it.

Apply equal relevance tests. Do not examine marriage, children, appearance, dress, family responsibilities, patronage, or dynastic access more intensively for women than for men unless the evidence establishes political significance. Do not assume that a woman represented women substantively, prioritized gender policy, or derived political support from gender. Distinguish symbolic representation from policy and institutional effects.

Segment long careers into historically defensible phases. Interpret choices against contemporaneous institutions, norms, information, and feasible alternatives, while allowing later scholarship to assess their consequences. Flag presentism rather than treating current standards as the only baseline.

## Build the Workbook

Use an available spreadsheet skill or library. Check tool availability once; if no spreadsheet skill is installed, use a supported library such as openpyxl without an exhaustive filesystem search. Keep normalized records and a parameterized builder in the working research directory so the workbook can be reproduced without temporary files or conversation history. The bundled [scripts/research_workbook.py](scripts/research_workbook.py) is one option; read [references/pipeline.md](references/pipeline.md) before using it. Follow the schema reference as a modular design rather than an inflexible tab quota. Preserve the main analytical distinctions even when combining sparse sections.

Default tab order:

1. `Overview`
2. `Context & Constraints`
3. `Career Timeline`
4. `Elections`
5. `Offices & Party`
6. `Policy & Governance`
7. `Ideas & Political Method`
8. `Controversies`
9. `Legacy & Assessments`
10. `Sources`

Put concise, decision-useful synthesis on `Overview` and evidence-rich records on the supporting tabs. Use sortable Excel tables, frozen headers, filters, restrained professional formatting, readable column widths, wrapped text where necessary, and real date and numeric values. Do not add decorative charts. Add a chart only when it clarifies a genuine time series or comparison, such as vote share across elections.

Keep the finding, review status and evidence navigation in the initial view; group supplementary columns for expansion. Make every citation navigable, using a citation table when a cell has several sources. Derive source usage from actual substantive citations, not blanket source ranges on methodology or calculated-count rows. Put shared methodological guidance once in Overview and reserve row cautions for specific historical risks; retain every required gender and era coverage item.

For comparative workbooks, add a `Comparison` tab first and keep a `Figure` field in every shared data table. Apply the same definitions and evidence standard to all figures. Do not produce a composite greatness ranking unless the user explicitly asks for a rubric; if asked, expose the criteria, weights, evidence, uncertainty, and sensitivity to the weights.

## Analytical Discipline

- Distinguish an initiative the figure personally led from one merely enacted during their tenure.
- Distinguish announced policy, enacted policy, implementation, measurable output, observed outcome, and disputed causal attribution.
- Distinguish party office, legislative office, ministerial office, movement leadership, and informal influence.
- For alliances and party changes, record dates, participants, stated rationale, strategic context, and consequences without treating inferred motive as fact.
- For elections, preserve constituency names as used at the time and note delimitation or indirect-election rules when relevant.
- For controversies, use precise procedural status: allegation, inquiry, charge, trial, acquittal, conviction, appeal, court finding, commission finding, legislative action, administrative action, or political criticism.
- For legacy, attribute assessments and present serious competing interpretations. Do not manufacture false balance where the evidence is one-sided.
- Record missing or unavailable evidence explicitly. Blank cells must not silently mean zero, no event, or exoneration.

## Completion Checks

Before delivery, verify that:

- the subject, name variants, dates, offices, party affiliations, and jurisdictions are internally consistent;
- overlapping tenures and party transitions are represented rather than flattened;
- every gender and era coverage item has a finding, a supported `Not materially relevant` disposition, or an explicit evidence gap;
- long careers are divided into phases and each major record can be interpreted against the applicable political, institutional, economic, international, media, social, and electoral context;
- gender-related claims distinguish observed treatment, the figure's own strategy, symbolic representation, and substantive effects without applying asymmetric personal-life scrutiny;
- comparisons use contemporaneous peers and institutions where appropriate, and material presentism risks are identified;
- election numbers use the correct contest, constituency, unit, and source;
- policy rows distinguish role, implementation, evidence, and attribution;
- controversy rows distinguish claims from findings and include the subject's response when available;
- every substantive row has traceable source IDs and every source ID resolves in `Sources`;
- the overview summarizes the evidence without introducing uncited claims;
- report structural integrity, arithmetic checks, passage review, application recalculation and visual inspection as separate results; do not label the whole workbook verified because structural checks pass;
- test formulas in a real spreadsheet engine when available and inspect its rendering of each sheet, including dense or long-text regions; record the engine, workbook hash and inspected regions. A custom redraw or independently reflowed preview is a layout estimate, not proof of the saved workbook's appearance. Synthetic formula caches are not evidence of recalculation. When application checks cannot run, report `Not run` with the reason and deliver that limitation explicitly;
- the final `.xlsx` is the only user-facing deliverable unless the user asks for the underlying research notes.
