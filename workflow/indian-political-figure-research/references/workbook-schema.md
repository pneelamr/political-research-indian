# Workbook Schema

Use these fields as a modular schema. Omit genuinely inapplicable fields and combine sparse tabs, but do not erase distinctions needed for accuracy. Each record should have a stable row ID and `Source IDs`.

## Overview

Create a compact profile and synthesis, not a duplicate of the detail tabs.

Profile fields:

- Full name
- Common name and initials
- Name variants
- Birth and death dates, or living status
- Birthplace and principal political geography
- Main party or parties with periods
- Principal elected and governmental offices
- Years active
- Current status and `As of` date when relevant
- Education, profession, languages, or cultural work when politically relevant
- Gender and other identity details when politically relevant
- Career phases and defining era transitions

Analytical sections:

- Career in brief
- Political identity and principal constituencies
- Most consequential contributions
- Principal limitations, failures, or controversies
- Leadership and political method
- Historical significance
- Open or disputed questions
- Gender and era synthesis

Use formulas to show defensible counts or summaries from supporting sheets, such as elections contested, elections won, years in selected offices, and policy-domain counts. Do not create a pseudo-precise overall score.

## Context & Constraints

This table is required. It records the gender and era coverage review even when a finding is `Not materially relevant` or `Evidence not found`. Use one row per coverage item per applicable career phase; do not compress all historical context into one lifetime label.

Recommended columns:

- Context ID
- Career phase
- Start date
- End date
- Coverage dimension
- Coverage question or item
- Research disposition: Material finding, Not materially relevant, Evidence not found, Conflicting evidence, or Research limitation
- Finding
- Mechanism or pathway of effect
- Political-system context
- Economic and international context
- Media and campaign environment
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary conditions or norm
- Contemporary comparison group
- Contemporary assessment
- Retrospective assessment
- Presentism caution
- Evidence-environment limitation
- Claim type
- Corroboration
- Context source IDs
- Research note

The table must collectively cover every item in the `Gender Coverage` and `Era Coverage` sections of the research standards. `Not materially relevant` requires a brief basis; `Evidence not found` describes a research gap and must not be presented as proof of absence.

Use `Gender relevance` to record whether gender affected access, advancement, role allocation, treatment, strategy, security, policy, representation, or legacy. Use `Other identity relevance` for evidenced intersections involving caste, religion, language, region, class, age, disability, sexuality, or another identity; do not infer identity or causal importance without support.

Where context varies within a phase or event, add another row rather than writing an internally contradictory summary. Major records on the other sheets should carry `Career phase` and reference the applicable `Context ID` or `Context source IDs` when context materially affects interpretation.

## Career Timeline

Recommended columns:

- Timeline ID
- Start date
- End date
- Date precision
- Phase or event
- Event type
- Office, organization, movement, or institution
- Location or jurisdiction
- Description
- Significance
- Claim type
- Corroboration
- Source IDs
- Research note
- Career phase
- Context ID

Include formative events only when they illuminate the political career. Prefer one consequential event per row.

## Elections

Recommended columns:

- Election ID
- Election date or year
- Election type and house
- Direct or indirect
- State or jurisdiction
- Constituency as named at the time
- Constituency or seat notes, including delimitation
- Party or alliance
- Candidate status: contestant, elected by legislature, nominee, campaign leader, or not personally contesting
- Result
- Votes
- Vote share
- Principal opponent
- Opponent party
- Opponent votes or vote share
- Margin and margin unit
- Turnout when relevant
- Government-formation result or post-election role
- Source IDs
- Research note
- Career phase
- Political-system context
- Media and campaign environment
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary comparison group
- Presentism caution
- Context source IDs

Never record a party-wide victory as the figure's personal electoral victory without a separate role field.

## Offices & Party

Recommended columns:

- Position ID
- Position category: elected, executive, ministerial, legislative, party, movement, diplomatic, constitutional, or informal
- Exact title
- Institution or organization
- Jurisdiction
- Start date
- End date
- Selection route
- Predecessor
- Successor
- Party or alliance during tenure
- Concurrent positions
- Main responsibilities or political function
- Exit reason
- Source IDs
- Research note
- Career phase
- Political-system context
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary comparison group
- Presentism caution
- Context source IDs

Preserve short, interrupted, acting, and non-consecutive tenures as separate rows.

## Policy & Governance

Recommended columns:

- Record ID
- Policy domain
- Initiative, decision, law, negotiation, institution, movement demand, or administrative action
- Jurisdiction
- Period
- Figure's documented role
- Role strength: initiated, led, sponsored, negotiated, approved, implemented, opposed, inherited, or associated
- Stated objective
- Mechanism or intervention
- Adoption status
- Implementation evidence
- Outputs
- Outcomes and indicators
- Indicator geography and period
- Attribution assessment
- Beneficiaries or affected groups
- Criticism, trade-offs, or unintended effects
- Current or final status
- Claim type
- Corroboration
- Source IDs
- Research note
- Career phase
- Political-system context
- Economic and international context
- Media and campaign environment
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary comparison group
- Presentism caution
- Context source IDs

For national and state economic indicators, avoid crediting or blaming one individual without an explicit attribution assessment.

## Ideas & Political Method

Recommended columns:

- Record ID
- Category: ideology, federalism, economy, welfare, social policy, language, religion, foreign policy, organization, coalition, movement, campaigning, communication, or constituency
- Topic
- Period
- Documented position or method
- Evidence type: speech, manifesto, vote, policy, alliance, organizational action, interview, or scholarly analysis
- Change over time
- Allies, rivals, institutions, or social coalition involved
- Strategic or historical context
- Consequence
- Claim type
- Corroboration
- Source IDs
- Research note
- Career phase
- Political-system context
- Economic and international context
- Media and campaign environment
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary comparison group
- Presentism caution
- Context source IDs

Treat motive as analysis unless the figure or a reliable source explicitly establishes it. Family and dynastic networks belong here only when they materially affected organization, succession, governance, or political conflict.

## Controversies

Recommended columns:

- Matter ID
- Matter
- Start date
- End date or latest status date
- Category
- Neutral description
- Allegation or criticism
- Alleging or reviewing party
- Subject's response
- Authority or forum
- Procedural status
- Finding or disposition
- Political, legal, administrative, or social consequence
- Degree of dispute
- Claim type
- Corroboration
- Source IDs
- Research note
- Career phase
- Political-system context
- Media and campaign environment
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary comparison group
- Presentism caution
- Context source IDs

Use exact procedural language. Do not mix unrelated matters merely because they occurred in the same tenure.

## Legacy & Assessments

Recommended columns:

- Assessment ID
- Theme
- Period being assessed
- Assessment or interpretation
- Assessor type: scholar, institution, contemporary ally, contemporary opponent, journalist, later political actor, or public-memory source
- Assessor
- Evidence basis
- Supporting view
- Competing view
- Consensus or dispute status
- Later influence or institutional legacy
- Claim type
- Source IDs
- Research note
- Career phase
- Political-system context
- Economic and international context
- Media and campaign environment
- Contemporary institutional constraints
- Gender relevance
- Other identity relevance
- Contemporary comparison group
- Presentism caution
- Context source IDs

Attributed assessments can be sharply critical or admiring. The workbook's own synthesis must remain evidence-based and should identify uncertainty.

## Sources

Recommended columns:

- Source ID
- Full citation
- Title
- Author or issuing institution
- Publisher or site
- Publication date
- URL
- Access date
- Source class: official record, court or commission, speech or primary statement, academic, book, reference, journalism, party or campaign, memoir, dataset, or other
- Primary or secondary
- Geographic or language scope
- Standpoint or interest note
- Claims or sheets supported
- Archive or document locator, including page, chapter, table, or constituency where useful
- Reliability or limitation note

Use clickable URLs. One source may support multiple rows; cite its stable source ID rather than duplicating the full citation in every data table.

Add access status separately from access date: a failed retrieval or located-only document is not an inspected source. Distinguish the underlying origin from the host domain, and derive `Used in` from actual substantive record links.

## Claim and Evidence Navigation

For substantial workbooks, add supporting `Claims`, `Evidence`, `Citations` and `Research Queue` tables when useful. Claims hold stable IDs, record/field references, precise statements, types, review status, priority, candidate source IDs, contradictions and review notes. Evidence links an individual claim to an inspected passage, with source ID, locator, short excerpt or paraphrase, access record, relation and reviewer/date. Citations provides one clickable source URL per record-source pair so no citation is hidden behind the first link in a multi-source cell. The research queue states unresolved core facts and the next useful retrieval route.

Counts of registered fields describe review workload, not complete atomic-claim coverage or the probability that the biography is correct. Show supported, pending and disputed work separately. Keep method/scope rows outside substantive evidence counts, and keep reusable guidance out of repeated row caveats. Preserve all gender and era coverage dispositions.

## Optional Comparison Tab

Add only for a multi-figure request. Compare like with like and show scope differences explicitly.

Possible fields:

- Figure
- Career period and political level
- Principal offices
- Electoral base and political geography
- Party-building or movement role
- Governance domains
- Coalition and opposition role
- Major crises
- Distinctive political method
- Enduring institutional or ideological legacy
- Evidence coverage and unresolved gaps
- Gender-related opportunities, constraints, treatment, strategy, and representative effects
- Era-specific institutions, party system, economy, international context, media environment, social conditions, and evidence limitations

Avoid a one-dimensional ranking of figures whose opportunities, offices, jurisdictions, and eras differ. If the user asks for scores, define the rubric before scoring and preserve qualitative explanation beside every score.

Comparative claims must use historically appropriate denominators. Compare gender-related treatment with relevant contemporaries and compare performance under materially similar offices, jurisdictions, institutions, and periods. When no defensible comparison exists, state that limitation rather than normalizing unlike cases.

## Example Coverage Probes

Use these examples to test the schema; they are prompts for coverage, not prewritten conclusions.

| Figure | Coverage the schema must accommodate |
| --- | --- |
| Atal Bihari Vajpayee | Jana Sangh-to-BJP career, parliamentary opposition, coalition construction, non-consecutive prime-ministerial terms, foreign and security policy, oratory, and competing assessments of moderation and party ideology |
| M. Karunanidhi | Dravidian movement and ideology, repeated chief-ministerial tenures, party organization, Centre-state politics, welfare and governance, Tamil cultural and media work, family succession, and controversies |
| K. Chandrashekar Rao (KCR) | party formation, Telangana statehood movement, alliance shifts, state formation, chief-ministerial governance, welfare and irrigation claims, party renaming or national expansion, electoral reversal, and current status |
| Sushma Swaraj | state and national roles, Parliament and opposition leadership, party organization, ministerial portfolios, external affairs and consular diplomacy, public communication, and gendered barriers or milestones |
| Indira Gandhi | rise within Congress, prime-ministerial phases, centralization, war and diplomacy, economic and social policy, the Emergency and institutional consequences, electoral defeat and return, Punjab crisis, assassination, and polarized legacy |
| P. V. Narasimha Rao | state and Union experience, minority-government management, economic reform, foreign-policy change, party leadership, Ayodhya and accountability debates, language and scholarship, later marginalization, and retrospective reassessment |
