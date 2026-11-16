#!/usr/bin/env python3
"""Durable, offline authoring of the Shashi Tharoor research snapshot."""
import json, hashlib
from pathlib import Path
from author_sources import sources, retrievals, ASOF
ROOT=Path(__file__).resolve().parent
tables={}; claims=[]; evidence=[]
S={s['Source ID']:s for s in sources}; R={r['id']:r for r in retrievals}
phases=['P1 | International civil service and writing, 1978–2008','P2 | Congress entry and UPA ministries, 2009–2014','P3 | Parliamentary opposition and party reform, 2014–2024','P4 | Fourth term and cross-party diplomacy, 2024–2026']
gender_items=['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time']
era_items=['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']
layouts={
 'Overview':['Overview ID','Topic','Finding / value'],
 'Context & Constraints':['Context ID','Career phase','Coverage item','Finding'],
 'Career Timeline':['Timeline ID','Period','Event','Finding'],
 'Elections':['Election ID','Year','Constituency / jurisdiction','Result','Finding'],
 'Offices & Party':['Position ID','Title','Period','Finding'],
 'Policy & Governance':['Policy ID','Initiative','Finding'],
 'Ideas & Political Method':['Idea ID','Topic','Finding'],
 'Controversies':['Matter ID','Matter','Finding'],
 'Legacy & Assessments':['Assessment ID','Theme','Finding']}
for name,lead in layouts.items(): tables[name]={'lead_columns':lead,'date_columns':['Start date','End date','Election date'],'rows':[]}

def ids(nums): return [f'S{n:03d}' if isinstance(n,int) else n for n in nums]
def add(sheet,rid,fields,nums=(),kind='Recorded fact',proof=None,status='Supported',priority='Medium',phase=None,note='',independent=False):
    """Evidence is bound only to explicitly selected fields, never all citations."""
    row={layouts[sheet][0]:rid,**fields,'Claim type':kind,'Source IDs':'; '.join(ids(nums))}
    if phase: row['Career phase']=phases[phase-1]
    if note: row['Research note']=note
    tables[sheet]['rows'].append(row)
    if kind=='Method / scope': return row
    if proof is None:
        field='Finding / value' if sheet=='Overview' else 'Finding'
        proof={field:nums}
        if sheet=='Controversies':
            for extra in ['Subject response / defence','Procedural status']:
                if extra in row: proof[extra]=nums
    for ix,(field,nums_for_field) in enumerate(proof.items(),1):
        candidates=ids(nums_for_field); available=[sid for sid in candidates if S[sid]['Access status']=='Passage inspected']
        cstatus=status if available or status!='Supported' else 'Not reviewed'
        cid=f'{rid}.{ix:02d}'
        c={'id':cid,'sheet':sheet,'record_id':rid,'field':field,'statement':row[field],
           'fingerprint':hashlib.sha256(json.dumps(row[field],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
           'claim_type':kind,'status':cstatus,'priority':priority,'candidate_source_ids':candidates,'evidence_ids':[],
           'contradictions':[],'review_note':note or ('Interpretation grounded in listed passages; not a causal estimate.' if kind=='Analysis' else 'Full field wording checked against the linked passage; attributed positions remain attributed.')}
        if independent and cstatus=='Supported': c['requires_independent_corroboration']=True
        if cstatus in ['Supported','Partially supported']:
            for j,sid in enumerate(available,1):
                ret=R['R'+sid[1:]]; eid=f'E-{cid}-{j}'
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':ret['id'],
                  'locator':ret['locator'],'passage_paraphrase':ret['passage_paraphrase'],
                  'relation':'Supports','reviewed_by':'Codex passage review','reviewed_at':ASOF,
                  'note':'This passage supports the relevant portion of this field. Combined fields require the listed evidence together; no claim of personal causation follows from holding office.'})
                c['evidence_ids'].append(eid)
        claims.append(c)
    return row

OV=[
('Identity and background','Shashi Tharoor, born 9 March 1956 in London; educated at St Stephen’s College, Delhi, and the Fletcher School, Tufts; PhD completed in 1978.',[1,2],'Recorded fact'),
('Career pathway','International civil servant and author before entering Congress electoral politics in 2009; subsequently junior Union minister, committee chair and party reform challenger.',[1,2,10,44],'Analysis'),
('Current public role','Fourth-term INC Lok Sabha MP for Thiruvananthapuram. External Affairs committee chair confirmed by a report signed in September 2026; his current biography also lists CWC membership.',[3,5,9,23],'Recorded fact'),
('Electoral durability','Won Thiruvananthapuram in 2009, 2014, 2019 and 2024. Margins varied sharply: 99,998; 15,470; 99,989; 16,077. These are four constituency wins, not national leadership mandates.',[6,7,8,9],'Analysis'),
('Party leadership contest','Lost the 2022 Congress presidential ballot to Mallikarjun Kharge: 1,072 versus 7,897 votes. His 11.95% share here uses valid delegate ballots, excluding 416 invalid ballots.',[10],'Recorded fact'),
('Executive record','Minister of State for External Affairs in 2009–2010 and Human Resource Development in 2012–2014. A documented education contribution was chairing the teachers-and-teaching mission committee.',[2,11],'Recorded fact'),
('Policy and parliamentary contribution','Equality and women’s-rights proposals, platform scrutiny and foreign-affairs reports show agenda-setting and oversight. The evidence is stronger for these activities than for personally attributable implementation outcomes.',[12,13,15,18,5,42],'Analysis'),
('Ideas and public argument','Advocates pluralism, institutional checks and a stronger Congress; combines criticism of colonial rule with support for private investment in local infrastructure. His religious writing attracts praise and caste-based critique.',[44,27,19,28,29],'Analysis'),
('Political method','Combines books, speeches and digital reach with committee work, professional-network outreach and constituency representation. Public prominence has not translated into control of the Congress organisation.',[27,22,10,23],'Analysis'),
('Major legal distinction','Discharged before trial in the Sunanda Pushkar case on 18 August 2021. Police later challenged discharge; no final revision disposition was verified. It would be inaccurate to describe an acquittal after trial or a conviction.',[33,34],'Recorded fact'),
('Other accountability issues','The IPL episode produced ministerial resignation and a denial of wrongdoing. Defamation proceedings and the women-MP selfie controversy require separate treatment of allegations, court procedure and political criticism.',[31,32,35,36,37,38,39],'Analysis'),
('Latest political context','Appointed Kerala PCC campaign co-chairman in February 2026. UDF’s subsequent Assembly victory and Satheesan’s chief ministership are alliance/state outcomes, not a personal Assembly election or executive office for Tharoor.',[24,26],'Analysis'),
('Important chronology correction','Chemicals committee service belongs to 2022–2024, not 2021–2024 as his biography says. September versus October 2022 start remains unresolved. UN interim DPI leadership in 2001 differs from confirmed USG appointment in June 2002.',[1,3,4,42,43],'Uncertainty or dispute'),
('Interpretive limits','A national communicator and persistent constituency winner with substantial parliamentary activity; independent audits of local delivery, the causal effect of his advocacy, and several current case outcomes remain incomplete.',[6,7,8,9,16,17,34,35,37],'Analysis')]
for i,(topic,finding,ns,kind) in enumerate(OV,1):
    add('Overview',f'OV{i:02d}',{'Topic':topic,'Finding / value':finding},ns,kind,status='Partially supported' if i==13 else 'Supported',priority='High' if i in [1,3,4,5,10,13] else 'Medium')
for i,(topic,finding) in enumerate([
('Scope and cutoff','Research snapshot as of 16 November 2026. Four career phases; ten era dimensions per phase and ten gender dimensions. Contemporary reporting, primary records and later assessments are distinguished.'),
('Reading and navigation','Read the initial finding and review columns, then expand grouped columns for dates, votes and caveats. All citations opens every source linked to a record; Claims and Evidence show the checked passages.'),
('Evidence meaning','Supported means the registered field has inspected passage support. A supported attribution does not establish that the allegation, prediction or opinion is true. Research limitations are explicit; unavailable values are blank, not zero.'),
('Election share definitions','2009 uses valid candidate votes; 2014 and 2024 use counted candidate votes plus NOTA; 2019 uses ADR’s published denominator. These shares are not an entirely uniform time series. Congress ballots use valid delegate votes.'),
('Confirmed direct contests (calculated)',4),('Direct victories (calculated)',4)],15):
    add('Overview',f'OV{i:02d}',{'Topic':topic,'Finding / value':finding},kind='Method / scope')

TIMELINE=[
('1956-03-09','Birth','Born in London; later education in India and the United States.',[2],1),
('1978','Doctorate and UN entry','Completed Fletcher PhD and joined UNHCR; academic and international-service experience preceded electoral politics.',[1],1),
('1981–1984','Refugee work','Headed UNHCR office in Singapore during the Indochinese refugee crisis.',[1],1),
('1989–1996','Peacekeeping headquarters','Special assistant in peacekeeping; led the headquarters Yugoslavia team in 1991–1996, with liaison and briefing responsibilities.',[1],1),
('1989','Literary visibility','Published The Great Indian Novel; literary work developed alongside international civil service.',[2],1),
('1997–2001','Secretary-General’s office','Director of Communications and Special Projects under the Secretary-General.',[1],1),
('2001; 2002-06-01','UN public information leadership','Interim head from January 2001; confirmed Under-Secretary-General for Communications and Public Information from 1 June 2002.',[1],1),
('2006','Secretary-General candidature','India nominated him; his biography describes finishing runner-up. This was an international institutional selection, not a public election.',[1,3],1),
('2009','Congress and first Lok Sabha victory','Won Thiruvananthapuram as INC candidate and entered the UPA ministry as Minister of State for External Affairs.',[2,6],2),
('2009-09','Social-media controversy','Apologised after the cattle-class tweet was criticised during the austerity campaign.',[40],2),
('2010-04-18','Ministerial resignation','Left the ministry amid IPL-related allegations, which he denied.',[31,32],2),
('2012-10-28','Return to government','Appointed Minister of State for Human Resource Development.',[2],2),
('2013-10-10','Teacher-policy committee','CABE noted recommendations of the teachers-and-teaching mission committee he chaired.',[11],2),
('2014','Second term and opposition role','Re-elected narrowly; became External Affairs committee chair. Congress removed him from spokesperson list in October.',[7,2,41],3),
('2015-05; 2015-12','Public history and rights advocacy','Oxford reparations speech gained wide circulation; proposed Section 377 amendment failed at the introduction stage in Lok Sabha.',[27,14],3),
('2017','Equality bill and professional outreach','Introduced broad anti-discrimination proposal and led the new All India Professionals Congress.',[12,13,22],3),
('2018-12-28','Women’s rights bill','Introduced proposal on sexual, reproductive and menstrual rights, including marital consent protections.',[13,15],3),
('2019','Third term and literary award','Re-elected, became IT committee chair, and received Sahitya Akademi recognition for An Era of Darkness.',[8,2,30],3),
('2020','Committee scrutiny and party reform','IT panel summoned Facebook; contemporary political retrospective records participation in the Congress G23 reform group.',[18,25],3),
('2021-08-18','Discharge in Sunanda Pushkar case','Trial court found no prima facie case under IPC 498A or 306 and discharged him before trial.',[33],3),
('2022','Party election and committee transition','Lost Congress presidency to Kharge; moved from IT to Chemicals and Fertilizers chairmanship during the year.',[10,42,43],3),
('2023-08-20','CWC nomination','Kharge included him as a member of the Congress Working Committee.',[23],3),
('2024','Fourth Lok Sabha term','Defeated BJP’s Rajeev Chandrasekhar and returned to External Affairs committee leadership.',[9,5],4),
('2025-05–2025-06','All-party diplomatic delegation','Led parliamentary outreach to five countries in the Americas after Operation Sindoor.',[21,25],4),
('2026-02; 2026-05','Kerala campaign role','Appointed PCC campaign co-chairman; UDF subsequently returned to state power with Satheesan as CM.',[24,26],4),
('2026-09','Sri Lanka report','Signed the committee’s report on bilateral relations, connectivity and fisheries, presented to the Speaker on 25 September.',[5],4)]
for i,(period,event,finding,ns,phase) in enumerate(TIMELINE,1):
    add('Career Timeline',f'T{i:02d}',{'Period':period,'Event':event,'Finding':finding},ns,phase=phase)

counts2014=[297806,282336,248941,14153,4820,4229,3260,2448,2103,1851,1716,1689,1271,902,843,447,371,356,292,261]
counts2024=[388,1109,1365,247648,599,420,2352,358155,342078,400,233,1483]
def election(rid,year,place,route,result,votes,opp,oppvotes,denom,ns,phase,note,nota=None,invalid=None,polled=None):
    fields={'Year':year,'Constituency / jurisdiction':place,'Result':result,'Finding':f'{result}: {votes:,} votes; principal opponent {opp} received {oppvotes:,}.','House / route':route,'Party / alliance':'INC / Congress-led UDF' if route.endswith(' / direct') else 'INC internal election','Candidate votes':votes,'Principal opponent':opp,'Opponent votes':oppvotes,'Share denominator':denom,'Vote share':votes/denom,'Signed vote margin':votes-oppvotes,'NOTA votes':nota,'Invalid ballots':invalid,'Total polled':polled,'Unit':'Individual votes' if route.endswith(' / direct') else 'Party delegate ballots','Denominator / comparison caution':note}
    fields['Finding']+=f' Signed margin {votes-oppvotes:+,}; share {votes/denom:.2%} on the stated denominator.'
    proof={f:ns for f in ['Finding','Candidate votes','Opponent votes','Share denominator','Vote share']}
    add('Elections',rid,fields,ns,proof=proof,phase=phase,priority='High',note=note)
election('EL01',2009,'Thiruvananthapuram (20), Kerala','Lok Sabha / direct','Won',326725,'P. Ramachandran Nair (CPI)',226727,737641,[6],2,'Valid candidate votes; NOTA did not exist in this return. Postal votes included. Margin 99,998.',invalid=276,polled=737917)
election('EL02',2014,'Thiruvananthapuram (20), Kerala','Lok Sabha / direct','Won',297806,'O. Rajagopal (BJP)',282336,sum(counts2014)+3346,[7],3,'Denominator is sum of 20 candidate totals plus 3,346 NOTA. Excludes 21 invalid ballots. Correct margin 15,470, not 15,700.',nota=3346,invalid=21,polled=sum(counts2014)+3346+21)
election('EL03',2019,'Thiruvananthapuram (20), Kerala','Lok Sabha / direct','Won',416131,'Kummanam Rajasekharan (BJP)',316142,1010180,[8],3,'ADR published denominator 1,010,180. Its printed 41.20% differs from 41.19% calculated from integers. Original consolidated CEO return remains a gap; NOTA/invalid breakdown not reconstructed.')
election('EL04',2024,'Thiruvananthapuram (20), Kerala','Lok Sabha / direct','Won',358155,'Rajeev Chandrasekhar (BJP)',342078,sum(counts2024)+6753,[9],4,'37.19% is share of counted votes including NOTA. Excluding NOTA gives 37.45%. Do not substitute a share using all votes polled without relabelling denominator.',nota=6753)
election('EL05',2022,'Indian National Congress delegates','Congress president / internal','Lost',1072,'Mallikarjun Kharge',7897,8969,[10],3,'Valid delegate ballots: 8,969. Share 11.95%; 11.42% would use all 9,385 ballots, including 416 invalid. Not a public popular-vote share.',invalid=416,polled=9385)
add('Elections','EL06',{'Year':2006,'Constituency / jurisdiction':'United Nations','Result':'Not selected','Finding':'India nominated Tharoor for Secretary-General; his own biography describes a runner-up finish. No popular electorate or comparable vote-share denominator.','House / route':'UN Secretary-General / institutional selection','Party / alliance':'Nomination by India','Candidate votes':None,'Opponent votes':None,'Vote share':None,'Signed vote margin':None,'Selection caution':'Security Council straw-poll endorsements are not a direct election. Exact poll rounds and veto attribution were not reconstructed.'},[1,3],'Attributed position',phase=1)

OFFICES=[
('UNHCR official; Singapore office head','United Nations','1978 onward; Singapore 1981–1984',None,None,1,[1],'International civil service','Refugee protection and resettlement work; nomination account is not an independent outcome audit.'),
('Special assistant and Yugoslavia headquarters team lead','UN peacekeeping','1989–1996; team lead 1991–1996',None,None,1,[1],'International civil service','Headquarters liaison and briefings; not field military command.'),
('Director, Communications and Special Projects','UN Secretary-General’s office','1997–2001',None,None,1,[1],'International civil service','Communications and coordination responsibilities under the Secretary-General.'),
('Head of Public Information; Under-Secretary-General','United Nations','Interim January 2001; confirmed June 2002; UN career ended 2007','2002-06-01',None,1,[1,2],'International civil service','Distinguish interim leadership from confirmed rank. Exact departure day not established in this register.'),
('Member, Lok Sabha — first term','Thiruvananthapuram, Kerala','2009–2014',None,None,2,[2,6],'Directly elected','INC candidate; first of four successive constituency mandates.'),
('Minister of State for External Affairs','Government of India, UPA','May 2009–18 April 2010',None,'2010-04-18',2,[2,31,32],'Ministerial','Junior minister; resignation followed IPL allegations, denied. Day of initial appointment retained as a chronology gap.'),
('Member, External Affairs committee; Defence consultative committee','Lok Sabha / ministries','From 30 April and 4 May 2010 respectively','2010-04-30',None,2,[2],'Parliamentary','Committee work after leaving ministry; exact endpoints not reconstructed.'),
('Minister of State for Human Resource Development','Government of India, UPA','28 October 2012–2014','2012-10-28',None,2,[2,11],'Ministerial','Teachers-and-teaching committee role documented separately; no claim he independently controlled all education policy.'),
('Member, Lok Sabha — second term','Thiruvananthapuram, Kerala','2014–2019',None,None,3,[2,7],'Directly elected','Re-elected with a much narrower margin than in 2009.'),
('Chairperson, Standing Committee on External Affairs','Parliament of India','1 September 2014–25 May 2019','2014-09-01','2019-05-25',3,[2],'Parliamentary','Committee chairmanship, not foreign ministership.'),
('AICC spokesperson — removal documented','Indian National Congress','Until 13 October 2014',None,'2014-10-13',3,[41],'Party','Beginning of appointment not established. Removed after Kerala party complaint; remained in Congress.'),
('Leader, All India Professionals Congress','Indian National Congress','From 2017; endpoint not established here',None,None,3,[22],'Party','Aimed to recruit professional participation; no assumption of present chairmanship.'),
('Member, Lok Sabha — third term','Thiruvananthapuram, Kerala','2019–2024',None,None,3,[2,8],'Directly elected','Third consecutive win, before losing a separate internal party ballot in 2022.'),
('Chairperson, IT / Communications and IT committee','Parliament of India','September 2019–2022','2019-09-13',None,3,[2,18,43],'Parliamentary','The live indexed bio gives 12 September 2022 endpoint; accepted register uses year precision because canonical text is inaccessible.'),
('Chairperson, Chemicals and Fertilizers committee','Parliament of India','2022–2024',None,None,3,[42,43,4,3],'Parliamentary','Primary reports confirm 2022–23 and 2023–24. September versus October 2022 effective start is unresolved; 2021 start in own biography is rejected.'),
('Member, Congress Working Committee','Indian National Congress','Appointed 20 August 2023; current biography lists membership','2023-08-20',None,3,[23,3],'Party','Nominated by party president Kharge after the 2022 contest.'),
('Member, Lok Sabha — fourth term','Thiruvananthapuram, Kerala','2024–present',None,None,4,[9,17,3],'Directly elected','Current as of workbook cutoff; ongoing term, not four completed terms.'),
('Chairperson, Standing Committee on External Affairs','Parliament of India','2024–present; dated confirmation September 2026',None,None,4,[5,3],'Parliamentary','Live indexed profile gives 26 September 2024 start, but exact day is not promoted from excerpt to verified fact.'),
('Leader, all-party parliamentary delegation, Group 5','Government-organised international outreach','25 May–5 June 2025','2025-05-25','2025-06-05',4,[21],'Temporary diplomatic assignment','Led INC and other-party representatives to five countries in the Americas; not appointment as Union minister.'),
('Co-chairman, Kerala PCC campaign committee','Indian National Congress','Appointed 12 February 2026 for Assembly campaign','2026-02-12',None,4,[24],'Party campaign','Campaign assignment, not PCC presidency or chief ministership.')]
for i,(title,inst,period,start,end,phase,ns,role,caution) in enumerate(OFFICES,1):
    finding=f'{title}, {inst}; {period}.'
    add('Offices & Party',f'OF{i:02d}',{'Title':title,'Period':period,'Finding':finding,'Institution / jurisdiction':inst,'Role category':role,'Start date':start,'End date':end,'Boundary / authority note':caution},ns,phase=phase,status='Partially supported' if i==15 else 'Supported',note=caution)

POLICY=[
('UN refugee administration','Singapore UNHCR leadership, 1981–1984','Managed refugee-related work in Singapore during the Indochinese refugee crisis. India’s nomination praises resettlement achievements; independent beneficiary evaluation was not assembled.','Office head','Administrative activity; attributed achievement','No personal causal estimate of resettlement outcomes.',[1],1,'Recorded fact'),
('UN peacekeeping support','Yugoslavia headquarters work, 1991–1996','Led the headquarters team and liaison/briefing work described in India’s nomination. This establishes responsibility within UN machinery, not personal control of field operations.','Headquarters team lead','Documented institutional role','Balkan mission outcomes require separate operational records and accountability analysis.',[1],1,'Recorded fact'),
('UN public information reform','2001–2007','India’s nomination credits him with information-centre restructuring and the UN Communications Group. These are attributed reform claims within a campaign document.','Department leadership','Institutional changes described by nominator','Do not convert efficiency praise into independently measured performance.',[1],1,'Attributed position'),
('Teacher education and teaching quality','CABE, October 2013','CABE noted recommendations of the National Mission on Teachers and Teaching committee chaired by Tharoor. The same meeting discussed RUSA; separate agenda items do not make him its sole architect.','Committee chair and HRD Minister of State','Recommendations; government programme development','Teacher quality, learning gains and later implementation were not independently evaluated by his tenure.',[11],2,'Recorded fact'),
('Decriminalisation of consensual same-sex relations','Lok Sabha, December 2015','Proposed Section 377 amendment failed at introduction, 71–24 with one abstention. The intervention documents rights advocacy and parliamentary resistance.','Private member sponsor','Introduction defeated','Do not credit him with judicial decriminalisation or enacted reform from this failed bill.',[14],3,'Recorded fact'),
('Anti-discrimination and equality framework','Bill introduced March 2017','Proposed protected-characteristic safeguards, central/state equality commissions and remedies. PRS dates introduction to 10 March 2017.','Private member sponsor','Introduced legislative proposal','No enacted Tharoor equality statute established; design is distinct from effect.',[12,13],3,'Recorded fact'),
('Women’s sexual, reproductive and menstrual rights','Bill introduced December 2018','Proposed greater agency and menstrual equity, including removal of the marital-rape exception. This is a legislative proposal, not evidence that the proposed protections took effect.','Private member sponsor','Introduced legislative proposal','Bill text link failed; design checked in contemporary legal commentary and introduction in PRS.',[13,15],3,'Recorded fact'),
('Platform accountability and digital safety','IT committee, 2020','Committee summoned Facebook and officials amid hate-speech-enforcement allegations; stated agenda included citizens’ rights and women’s online safety.','Committee chair','Scrutiny and proposed hearing','Summoning witnesses is not adjudication of allegations or measured reduction of platform harms.',[18],3,'Recorded fact'),
('Thiruvananthapuram airport investment','Privatisation debate, 2020','Supported private operation to expand airport potential and attract investment despite opposition from Left and some Congress colleagues.','Constituency advocate','Public position','Predicted connectivity and investment benefits are his argument; no causal outcome audit here.',[19],3,'Attributed position'),
('Vizhinjam port advocacy','Retrospective account, 2025','Tharoor said he helped bring Adani into the project at Oommen Chandy’s request. This is a claim about facilitation within a project involving governments, investors and other actors.','Self-described facilitator','Retrospective personal credit claim','Independent documentary confirmation of his decisive influence was not obtained.',[20],4,'Attributed position'),
('Medical-device industry scrutiny','Report presented February 2024','Chaired committee that recommended broader manufacturing incentives, more testing laboratories and regulatory training. Inquiry began under Kanimozhi in 2021 and continued under Tharoor.','Committee chair, inherited inquiry','Collective report and recommendations','National policy/PLI administration belonged to government; uptake and health outcomes not traced.',[42],3,'Recorded fact'),
('All-party international outreach','Americas delegation, May–June 2025','Led Group 5 visits to Guyana, Panama, Colombia, Brazil and USA during the post-Sindoor diplomatic outreach.','Delegation leader','Completed official visits','Diplomatic access and advocacy are documented; changes in foreign policy caused by visits are not.',[21,25],4,'Recorded fact'),
('India–Sri Lanka relations','External Affairs report, September 2026','Committee advocated stronger bilateral mechanisms and connectivity, attention to fisheries livelihoods and maritime-boundary problems, and expanded training cooperation.','Committee chair','Collective parliamentary recommendations','No claim that recommendations settled disputes or had been implemented by cutoff.',[5],4,'Recorded fact'),
('Constituency representation in Parliament','2019–2026','PRS entries document attention to coastal erosion, fishing harbours, rail services, ASHA wages and road-project compensation/environment. These are interventions, not a verified project-completion ledger.','MP','Recorded demands and questions','No MPLADS expenditure audit, beneficiary dataset or independent local-delivery counterfactual assembled.',[16,17],4,'Analysis'),
('Parliamentary participation','Sixteenth, seventeenth and current Lok Sabha','PRS records 86% attendance in its 2014–2019 window, 93% in 2019–2024, and 89% through 13 August 2026. Seventeenth-term activity: 101 debates, 275 questions, 13 private member bills.','MP','Measured activity counts','Counts do not measure legislative quality, constituency approval or the number of bills enacted.',[13,16,17],4,'Recorded fact')]
for i,(topic,period,finding,role,stage,caution,ns,phase,kind) in enumerate(POLICY,1):
    add('Policy & Governance',f'PG{i:02d}',{'Initiative':topic,'Finding':finding,'Period':period,'Personal role':role,'Stage / observed output':stage,'Attribution / outcome limit':caution},ns,kind,phase=phase,note=caution)

IDEAS=[
('Pluralism and Hindu identity','His religious writing presents an inclusive Hindu self-understanding and rejects exclusionary politics; reviewers disagree about how well it addresses hierarchy and caste.',[28,29],3,'Analysis'),
('Colonial history and reparations','The Oxford argument sought moral acknowledgement of colonial harm, accepting token compensation as symbolic. Contemporary coverage records praise across party lines.',[27],3,'Attributed position'),
('Constitutional opposition','Post-election essay argues for institutional checks and a rebuilt Congress as a credible alternative to BJP dominance; his account of government failures is partisan assessment.',[44],3,'Attributed position'),
('Party democracy and reform','Presented the 2022 contest as renewal rather than a personal grievance; claimed an uneven contest and pressure on supporters. The result nonetheless shows a large defeat among delegates.',[44,10],3,'Analysis'),
('Private enterprise and local development','Airport advocacy supports private investment as a means to improve local connectivity, creating disagreement with Left critics and parts of Congress. This is a specific policy position, not a complete economic doctrine.',[19],3,'Analysis'),
('Rights through legislative proposals','Section 377, equality and women’s-rights bills use private-member initiative to place social rights on the agenda; failure or non-enactment limits direct legal effects.',[14,12,15],3,'Analysis'),
('Professional recruitment','AIPC sought participation from professionals, matching his public-policy and communication profile. The launch record does not establish a new mass social base or membership-to-vote conversion.',[22],3,'Analysis'),
('Digital and literary communication','The delayed spread of his Oxford speech after online promotion illustrates how a live argument can gain a second audience. The 2009 tweet dispute shows risks of humour across audiences and languages.',[27,40],3,'Analysis'),
('Cross-party engagement and discipline','Selective praise and cooperation have coexisted with Congress membership: spokesperson removal in 2014, diplomatic delegation leadership in 2025, and campaign responsibility in 2026.',[41,21,24,25],4,'Analysis'),
('Federal concerns in representation debates','ThePrint reports his objection to linking women’s reservation with delimitation in April 2026. This is a reported federal-representation position; the full parliamentary argument was not independently reconstructed.',[25],4,'Attributed position')]
for i,(topic,finding,ns,phase,kind) in enumerate(IDEAS,1):
    add('Ideas & Political Method',f'IM{i:02d}',{'Topic':topic,'Finding':finding},ns,kind,phase=phase)

CONTROVERSIES=[
('Kochi IPL franchise and ministerial resignation','2010','Opposition alleged improper use of ministerial influence in a franchise involving equity held by Sunanda Pushkar. Tharoor resigned on 18 April; the reviewed record does not establish corruption.','Denied improper financial benefit and wrongdoing; requested investigation.','Political allegation and resignation','No final independent inquiry outcome established here.',[31,32],2,'Supported'),
('Sunanda Pushkar death proceedings','2014–2022; current revision outcome unverified','After prosecution sought action under IPC 498A/306, court discharged Tharoor on 18 August 2021 for lack of prima facie material. Police challenged discharge in 2022; no later final outcome was verified.','Contested prosecution; court found no prima facie case. Do not equate his defence with proof of an alternative cause of death.','Discharge before trial; later revision reported','Court’s conditional reasoning about suicide is not a finding that suicide was established. Current docket gap remains.',[33,34],3,'Supported'),
('Scorpion-metaphor criminal defamation complaint','2018–2025; later status unverified','Rajeev Babbar complained over a remark about Modi. Supreme Court stayed proceedings in September 2024 and continued relief in August 2025; inspected 15 September 2025 order adjourned the matter.','Tharoor said he quoted a metaphor already published in Caravan and attributed to an unnamed RSS figure.','Interim relief and adjournment','Oral remarks about closing the case do not amount to final quashing. No final disposal located.',[35,36],4,'Supported'),
('Chandrasekhar criminal defamation complaint','2024–2025; later status unverified','Trial court dismissed complaint on 4 February 2025. Delhi High Court issued notice on Chandrasekhar’s revision on 20 May. The allegation concerned implications of Tharoor’s April 2024 interviews.','The High Court order records the trial court’s view that imputations against the complainant were absent; full respondent defence not inspected.','Complaint dismissed; revision notice','Notice does not reverse dismissal or establish defamatory wrongdoing. Later hearing outcome not verified.',[37],4,'Supported'),
('Chandrasekhar civil defamation suit','2025; later status unverified','Separate civil suit alleged reputational damage from purported vote-buying accusations. Delhi High Court issued summons on 3 February 2025.','Complete written defence was not obtained in this research.','Civil summons','No liability or damages finding established. Allegations against either politician are not adopted as fact.',[38],4,'Supported'),
('Women-MP selfie caption','2021-11-29','NCW chair Rekha Sharma and lawyer Karuna Nundy criticised his caption as objectifying women MPs. Their criticism concerns representation and language, not an adjudicated offence.','Apologised to those offended and said women MPs initiated the selfie in good humour.','Public criticism and apology','Do not infer the women MPs’ agreement or disagreement from his explanation alone.',[39],3,'Supported'),
('Cattle-class tweet','2009-09','Tweet during austerity drive drew party and opposition criticism as insensitive to economy travellers.','Apologised and said he was criticising airlines’ crowding rather than passengers.','Political communication dispute','Humour, audience and translation context matter; no legal finding implied.',[40],2,'Supported'),
('Congress spokesperson removal','2014-10-13','Party leadership removed him from spokesperson list after Kerala complaint concerning his praise of Modi and Swachh Bharat participation.','Accepted decision while saying he would have welcomed an opportunity to answer complaint.','Party disciplinary action','Removal from spokesperson panel was not expulsion from Congress.',[41],3,'Supported'),
('Congress presidential election fairness','2022','Tharoor’s post-result essay alleged uneven pressure and irregularities, while recognising the official tally and urging party renewal. Party result confirms Kharge’s large victory.','His own account frames participation as reform within Congress.','Contested party-process assessment','No independent audit of alleged irregularities assembled; official result alone neither proves nor refutes them.',[44,10],3,'Partially supported'),
('Airport privatisation disagreement','2020','Left and some Congress figures criticised his support for private airport operation; Thomas Isaac challenged its corporate-benefit rationale.','Tharoor argued investment would expand connectivity and local opportunity.','Policy disagreement','Competing forecasts are not evidence of corruption or a completed outcome evaluation.',[19],3,'Supported'),
('Cooperation with Modi government and party tensions','2025–2026','Government-sponsored diplomatic outreach and praise of selected policies prompted Congress friction in ThePrint’s account. Official records still identify him with INC and show 2026 campaign appointment.','His subsequent campaign role demonstrates continuing formal party participation; inner motives cannot be inferred.','Political dispute and continued party role','No verified party switch or Union ministerial appointment follows from cooperation.',[21,24,25],4,'Supported')]
for i,(matter,period,finding,response,stage,caution,ns,phase,status) in enumerate(CONTROVERSIES,1):
    add('Controversies',f'CO{i:02d}',{'Matter':matter,'Finding':finding,'Period':period,'Subject response / defence':response,'Procedural status':stage,'Unresolved point / caution':caution},ns,'Recorded fact' if i!=9 else 'Uncertainty or dispute',phase=phase,status=status,priority='High',note=caution,independent=i in [1,2,3,11])

LEGACY=[
('Diplomatic expertise as political capital','His UN background and repeated foreign-affairs responsibilities support a specialist profile. This does not establish that every diplomatic initiative succeeded or that expertise alone explains electoral victories.',[1,2,5,21],'Analysis'),
('Electoral resilience, uneven margins','Four consecutive wins establish sustained constituency success across different opponents. Narrow 2014 and 2024 margins caution against assuming an unassailable seat or converting online popularity into national support.',[6,7,8,9],'Analysis'),
('Parliamentary activity versus effectiveness','Attendance, questions, bills and reports provide evidence of participation and agenda-setting. Their causal influence on law, executive decisions and local welfare remains less fully measured.',[13,16,17,42,5],'Analysis'),
('Public intellectual and literary recognition','Sahitya Akademi’s 2019 award documents institutional recognition for An Era of Darkness; Oxford reception illustrates influence on public argument. Neither establishes consensus on all historical claims.',[30,27],'Analysis'),
('Competing readings of pluralism','Publishers Weekly admires the accessible personal account while criticising political campaigning; Kancha Ilaiah Shepherd challenges its treatment of caste and spiritual inequality. These are distinct critical standards, not interchangeable verdicts.',[28,29],'Attributed position'),
('Party reform ambition and organisational limits','The 2022 defeat reveals the gap between visibility and delegate support. Later CWC nomination and Kerala campaign responsibility show continued integration, without demonstrating control of Congress succession or policy.',[10,23,24],'Analysis'),
('Gender advocacy and reception','Women’s-rights proposals and the selfie controversy belong in the same assessment, but address different things: legislative advocacy versus treatment of colleagues in public communication. Neither alone settles substantive effects.',[15,39],'Analysis'),
('Accountability without procedural conflation','IPL resignation, discharge in the Pushkar case and interim defamation proceedings are separate events. A fair legacy account preserves responses and judicial stages instead of treating accusation, notice or stay as a verdict.',[31,32,33,34,35,36,37,38],'Analysis')]
for i,(theme,finding,ns,kind) in enumerate(LEGACY,1):
    add('Legacy & Assessments',f'LA{i:02d}',{'Theme':theme,'Finding':finding},ns,kind)

# Each phase has all ten era items; limitations remain visible, not assumed away.
ERA=[[
('His principal institutional base was the UN rather than an Indian party. India’s 2006 nomination supplied state backing before his Congress electoral career.',[1,2],'M'),
('International civil-service hierarchy, member-state authority and a Secretary-General selection process shaped his powers. A headquarters role did not confer national executive or battlefield command.',[1],'M'),
('The 2006 candidature was an institutional selection, not a popular election; nomination and self-described runner-up status cannot be compared with Lok Sabha vote shares.',[1,3],'M'),
('Information-centre restructuring appears in the nomination, but a broader causal account linking the world economic regime to his career choices was not established.',[1],'L'),
('Indochinese refugee work and Yugoslavia peacekeeping placed him within Cold War displacement and post-Cold War conflict management; the nomination documents these assignments rather than their full historical consequences.',[1],'M'),
('UN communications leadership and book publication provided international public visibility. Later Twitter prominence should not be projected backward into the 1980s.',[1,2,27],'M'),
('Career advancement occurred through international administration and the Secretary-General’s office; the inspected evidence does not establish a prior Indian electoral organisation built around him.',[1,2],'M'),
('Refugees and conflict-affected populations were central to his work. No independent distributional or gender evaluation of his particular interventions was obtained.',[1],'L'),
('Singapore, UN headquarters and Yugoslavia-related duties were international assignments; London birthplace and Indian education are biographical facts, not evidence of a territorial Indian mandate.',[1,2],'M'),
('India’s nomination is rich in chronology but designed to promote a candidate. Its effectiveness claims require independent sources; later biographies can blur interim and confirmed appointments.',[1,2,3],'M')],[
('Entered Congress and UPA government after winning in 2009. His resignation and later return to ministry show both electoral access and dependence on party/executive decisions.',[2,6,31],'M'),
('Minister of State authority differed from Cabinet leadership; CABE committee recommendations were one component of education policymaking, not unilateral power to implement national reform.',[2,11],'M'),
('Thiruvananthapuram’s 2009 runner-up was CPI; in 2014 it was BJP. The changing contest and much narrower margin matter more than assuming a fixed two-party electorate.',[6,7],'M'),
('The 2009 austerity campaign formed the immediate context of his travel-class tweet. This documents a political constraint on ministerial communication, not his complete fiscal-policy programme.',[40],'M'),
('Diplomatic experience preceded External Affairs ministerial appointment. A tenure-bounded account of treaties, negotiations or international outcomes personally driven by him remains incomplete.',[1,2],'L'),
('Twitter accelerated both direct communication and controversy. The austerity tweet and IPL dispute moved across digital media, television and parliamentary politics.',[40,31,32],'M'),
('Congress and government leadership could require ministerial exit; electoral victory alone did not insulate him from organisational discipline.',[31,32,6],'M'),
('Teacher-policy discussions concerned educational capacity and quality. Beneficiary-level evidence establishing whose outcomes improved through his specific intervention was not obtained.',[11],'L'),
('A Kerala Lok Sabha constituency supplied his mandate, while his ministerial authority was national. The seven Assembly segments listed in 2014 mix city and surrounding areas; aggregate votes do not identify a caste or religious support bloc.',[6,7,2],'M'),
('Primary election counts and official committee announcements are strong for events; allegations, defence statements and institutional praise have different evidentiary functions.',[6,7,11,31,32],'M')],[
('After Congress lost national power in 2014, his work emphasised opposition argument, committees and party reform. The 2022 internal defeat illustrates limits to his organisational support.',[27,10,44],'M'),
('Private-member bills and committee scrutiny offered agenda-setting opportunities, constrained by voting and government control of implementation. Section 377 introduction was defeated; reports were recommendations.',[14,12,42],'M'),
('Two further wins in 2014 and 2019 came against BJP runners-up, with sharply different margins. The 2022 delegate ballot represents a different electorate and selection system.',[7,8,10],'M'),
('Airport privatisation exposed disagreements about private capital, public assets and regional development. Medical-device scrutiny addressed domestic industry and regulation; the committee was not the implementing ministry.',[19,42],'M'),
('Foreign-affairs chairmanship and colonial-history arguments gave him international-policy visibility. Detailed government uptake of the 2014–2019 committee’s recommendations was not reconstructed.',[2,27],'L'),
('Viral speeches, literary debate and platform-accountability hearings linked communication with politics. Attention and controversy should not be equated with persuasion or electoral conversion.',[27,28,18,39],'M'),
('AIPC professional outreach, G23 reform advocacy, the presidential contest and CWC nomination represent different organisational routes; none alone establishes command of the party.',[22,25,10,23],'M'),
('Equality, sexual autonomy and caste hierarchy became explicit subjects of bills and criticism of his writing. The evidence includes both rights advocacy and challenges to its social reach.',[12,15,29],'M'),
('Kerala’s constituency interests interacted with national party and parliamentary roles. Airport disagreement shows that state party positions and the MP’s development argument could diverge.',[19,16],'M'),
('PRS records measure activity, not effectiveness; self-authored reform accounts need attribution; court orders must be read at the actual procedural stage rather than through headlines.',[16,44,33,34],'M')],[
('Continued as an INC MP while leading government-sponsored diplomatic outreach; official 2026 campaign appointment and reported UDF victory show continuing Congress involvement.',[21,24,26],'M'),
('Committee chairmanship, delegation leadership and campaign office confer different powers. September 2026 Sri Lanka recommendations did not themselves change executive policy.',[5,21,24],'M'),
('Fourth Lok Sabha victory was by 16,077 over BJP’s Chandrasekhar. The 2026 Kerala Assembly result concerns his alliance and campaign role, not another personal constituency win.',[9,24,26],'M'),
('Current parliamentary interventions concern fisher costs, road-project compensation and ageing; independent estimates of their budgetary or livelihood effects are unavailable.',[17],'L'),
('Post-Sindoor outreach and Sri Lanka committee work placed him in diplomacy beyond party opposition. Official itineraries document contact; reports document recommendations, not negotiated outcomes.',[21,25,5],'M'),
('News narratives of reconciliation and future ambitions can outrun formal appointments. Dated party and parliamentary documents are used to establish current roles.',[25,24,5],'M'),
('Campaign co-chairmanship sat within a committee headed by Chennithala, alongside Kharge’s national leadership. It should not be relabelled state party presidency or executive government office.',[24,26],'M'),
('Fisheries livelihoods, community health workers and population ageing appear in current activity. Beneficiary and gender-disaggregated effects of his interventions are not yet established.',[17,5],'L'),
('His continuing seat is Thiruvananthapuram; reported delimitation objections concern federal representation, while the Assembly campaign concerned Kerala-wide party competition.',[9,24,25],'M'),
('Current-office evidence extends to September 2026; PRS counts stop 13 August. Latest retrieved court orders are older. Each timestamp is retained rather than projecting every source to the cutoff.',[5,17,35,37],'M')]]
comparison=['Senior international civil servants and Secretary-General candidates','First-term MPs and Ministers of State in UPA','Opposition MPs, private-member sponsors and committee chairs','Current MPs, committee chairs and party campaign leaders']
for pi,entries in enumerate(ERA,1):
    for i,(finding,ns,disp) in enumerate(entries,1):
        add('Context & Constraints',f'CT-P{pi}-{i:02d}',{'Career phase':phases[pi-1],'Coverage dimension':'Era','Coverage item':era_items[i-1],'Finding':finding,'Research disposition':'Research limitation' if disp=='L' else 'Material finding','Contemporary comparison group':comparison[pi-1],'Presentism caution':'Interpret available institutional powers and contemporary information; later prominence or litigation does not establish earlier motives.'},ns,'Analysis',status='Not reviewed' if disp=='L' else 'Supported')

GENDER=[
('Entry and advancement','Education and international administration supplied a documented pathway into Congress politics. No matched evidence isolates the causal role of male advantage in his recruitment or advancement.',[1,2,6],'Research limitation'),
('Milestones','The reviewed offices do not establish a gender-representational first. High rank and four electoral wins alone do not constitute evidence of a gender milestone.',[1,2,9],'Research limitation'),
('Networks and pathways','International and professional networks are documented. The IPL controversy made a personal relationship politically salient, but this does not establish a family-based route into his first candidature.',[1,22,31,32],'Material finding'),
('Role and portfolio allocation','Diplomacy, education and committee assignments fit a professional-specialist narrative, but evidence attributing the allocation specifically to gender expectations is unavailable.',[1,2,42],'Research limitation'),
('Campaign and media treatment','The 2021 women-MP selfie drew explicit objectification criticism. Tharoor apologised and offered a different account of intent; a systematic comparison of his media treatment with women politicians was not conducted.',[39],'Material finding'),
('Threats and security','This research did not establish a distinctive gendered threat or security constraint affecting his career. Legal proceedings and party criticism should not automatically be categorised as gender-based persecution.',[33,36,41],'Research limitation'),
('Gender-related policy and organizations','The 2018 bill proposed sexual/reproductive agency and menstrual equity, including marital-rape reform. The 2020 IT-panel agenda included women’s digital safety. These document advocacy and scrutiny, not measured improvements.',[15,18],'Material finding'),
('Political use of identity','The selfie episode involved gendered public language and contested intent. His stated explanation does not establish how every woman pictured understood it; no general campaign strategy based on masculinity is inferred.',[39],'Material finding'),
('Representation and effects','Rights proposals supply substantive policy content, while introduction, a committee summons or a supportive speech cannot establish implementation, safety gains or equal political opportunity.',[12,15,18],'Material finding'),
('Assessment over time','Rights proposals, public criticism of his language and reported federal objections to reservation-linked delimitation concern different periods and mechanisms. They should be evaluated separately; a longitudinal outcome study is missing.',[15,39,25],'Material finding')]
for i,(item,finding,ns,disp) in enumerate(GENDER,1):
    add('Context & Constraints',f'CT-G-{i:02d}',{'Career phase':'Across phases; event periods specified','Coverage dimension':'Gender','Coverage item':item,'Finding':finding,'Research disposition':disp,'Contemporary comparison group':'Men and women with comparable diplomatic, parliamentary and party responsibilities','Other identity relevance':'Religious self-description and criticism of caste hierarchy are attributed; no caste or religious voting base is inferred.','Presentism caution':'Apply equal relevance tests to family, appearance, networks and security. Advocacy does not alone demonstrate representative effects.'},ns,'Analysis',status='Not reviewed' if disp=='Research limitation' else 'Supported')

for sheet,t in tables.items():
    for row in t['rows']:
        if sheet!='Context & Constraints' and row.get('Career phase') in phases:
            pi=phases.index(row['Career phase'])+1
            row['Context IDs']=f'CT-P{pi}-01; CT-P{pi}-02; CT-P{pi}-03'

gapdefs=[
('High','Current litigation dispositions','Sunanda revision, scorpion defamation and Chandrasekhar civil/criminal matters have different last-verified dates; no later final dispositions established.','Retrieve latest case-status sheets and signed orders for each matter. Do not infer closure, liability or reversal from lack of later reporting.',['CO02','CO03','CO04','CO05']),
('High','Committee chronology discrepancy','Own biography incorrectly begins Chemicals chairmanship in 2021. Parliamentary report confirms 2022–23 and 2023–24; indexed bio gives September 2022, contemporary notification report October.','Obtain original appointment bulletin and effective-date text; retain year precision until then.',['OF15','OV13']),
('Medium','2019 original constituency return','ADR count table inspected; original consolidated CEO/ECI result and denominator components not obtained. Printed 41.20% differs from integer recalculation.','Retrieve consolidated Form 20 or ECI detailed return with postal/NOTA counts; keep current 41.19% transparently derived.',['EL03']),
('Medium','Executive and constituency outcomes','CABE role and parliamentary actions verified; independent MPLADS/project expenditure audit and tenure-bounded policy outcome studies not assembled.','Add official sanction/completion records, audit reports and independent beneficiary evaluation; test personal contribution separately from project timing.',['PG04','PG09','PG10','PG14']),
('Medium','Committee uptake','Medical-device and Sri Lanka reports inspected, but government action-taken reports and implementation outcomes not traced.','Pair each major recommendation with dated government responses and implementation evidence.',['PG11','PG13']),
('Medium','Party-election fairness','Official result and Tharoor’s allegations are available; independent adjudication of alleged irregularities was not assembled.','Add election-authority response and independent delegate/process reporting before assessing fairness.',['CO09','IM04']),
('Medium','Gender and social distribution','Four gender dimensions and several era items retain explicit limitations; no matched causal assessment of access, allocation or security.','Use comparable politicians, recruitment records and gender scholarship; do not treat missing evidence as absence of a mechanism.',['CT-G-01','CT-G-02','CT-G-04','CT-G-06']),
('Low','Precise minor tenure boundaries','May 2009 oath/profile discrepancy, UN departure day, AIPC endpoint and exact 2024 chair appointment day remain unverified in inspected primary text.','Retrieve appointment notifications and UN personnel releases rather than filling precision from indexed biographies.',['OF04','OF06','OF12','OF18']),
('Low','Earlier economic and social context','International-service and early ministerial phases lack independent distributional evaluation and a complete economic-context account.','Add UN administrative audits, operational histories and contemporary India policy studies.',['CT-P1-04','CT-P1-08','CT-P2-05','CT-P2-08'])]
gaps=[{'id':f'G{i:02d}','priority':p,'topic':t,'gap':g,'next_action':n,'record_ids':rs,'status':'Open'} for i,(p,t,g,n,rs) in enumerate(gapdefs,1)]
for cid in ['OV13.01','OF15.01']:
    c=next(c for c in claims if c['id']==cid)
    c['contradictions']=['S003 says 2021; S042 establishes 2022–23. S004 indexed September 2022 differs from October notification reporting in S043. Year accepted, exact day unresolved.']
data={'schema_version':1,'subject':'Shashi Tharoor','as_of':ASOF,'guidance':'Four career phases; 40 era items and 10 gender items. Facts, positions, analysis and uncertainty are labelled. An attributed allegation is not established wrongdoing. Election denominators and source cutoffs differ and are explicit. Some fields are compound review units rather than atomic claims.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'coverage':{'Era':era_items,'Gender':gender_items},'phases':phases,'gaps':gaps}
for name,obj in [('research.json',data),('sources.json',sources),('retrievals.json',retrievals)]:
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rows':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence)},indent=2))
