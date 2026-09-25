"""Reproducible, passage-reviewed political research; internal authoring file."""
import hashlib
import json
from pathlib import Path
from author_sources import ASOF, sources, retrievals

tables, claims, evidence, gaps = {}, [], [], []
R = {r['source_id']:r for r in retrievals if r['access_status']=='Passage inspected'}
P1='P1 | Public life and party entry (2003–May 2014)'
P2='P2 | Commerce and Defence (May 2014–May 2019)'
P3='P3 | Finance, pandemic and recovery (May 2019–June 2024)'
P4='P4 | Finance in coalition government (June 2024–September 2026)'
phases=[P1,P2,P3,P4]

def table(name, lead, dates=()):
    tables[name]={'lead_columns':lead,'date_columns':list(dates),'rows':[]}

def add(name, rid, fields, nums, typ='Recorded fact', phase=None, context='', checked=None, note='', status='Supported', priority='Normal'):
    ids=[f'S{n:03d}' if isinstance(n,int) else n for n in nums]
    idcol={'Overview':'Overview ID','Context & Constraints':'Context ID','Career Timeline':'Timeline ID','Elections':'Election ID','Offices & Party':'Position ID','Controversies':'Matter ID','Legacy & Assessments':'Assessment ID'}.get(name,'Record ID')
    row={idcol:rid,**fields,'Claim type':typ,'Source IDs':'; '.join(ids)}
    if phase: row['Career phase']=phase
    if context: row['Context IDs']=context
    if note: row['Research note']=note
    tables[name]['rows'].append(row)
    if typ=='Method / scope': return row
    if checked is None:
        checked={k:ids for k in fields if k in ['Finding / value','Finding','Description','Assessment','Documented role','Stage','Start date','End date','Election date','Candidate votes','Response','Procedural status'] and fields[k] is not None}
    for field,support in checked.items():
        support=[f'S{n:03d}' if isinstance(n,int) else n for n in support]
        val=row[field]; cid=f'C-{rid}-{sum(c["record_id"]==rid for c in claims)+1:02d}'
        evs=[]
        if status in ('Supported','Partially supported','Disputed'):
            for sid in support:
                eid=f'EV-{len(evidence)+1:04d}'; evs.append(eid)
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':R[sid]['id'],
                    'locator':R[sid]['locator'],'passage_paraphrase':R[sid]['passage_paraphrase'],
                    'relation':'Supports','reviewed_by':'Codex: inspected-passage review','reviewed_at':ASOF,
                    'note':'Combined support where multiple passages are cited. Analysis is an inference; source assertions and allegations remain attributed.'})
        claims.append({'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':val,
            'fingerprint':hashlib.sha256(json.dumps(val,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            'claim_type':typ,'status':status,'priority':priority,'candidate_source_ids':support,
            'evidence_ids':evs,'contradictions':[],'review_note':note or ('Inference bounded by the cited records.' if typ=='Analysis' else 'Entire field checked against indicated passages; qualifications retained.')})
    return row

table('Overview',['Overview ID','Topic','Finding / value'])
table('Context & Constraints',['Context ID','Career phase','Coverage item','Finding'])
table('Career Timeline',['Timeline ID','Period','Event','Description'],['Start date'])
table('Elections',['Election ID','Year','Constituency','Result','Candidate votes'],['Election date'])
table('Offices & Party',['Position ID','Position / institution','Period','Finding'],['Start date','End date'])
table('Policy & Governance',['Record ID','Initiative / decision','Finding','Stage'])
table('Ideas & Political Method',['Record ID','Topic','Finding'])
table('Controversies',['Matter ID','Matter','Finding','Procedural status'])
table('Legacy & Assessments',['Assessment ID','Theme','Assessment'])

def ov(n,topic,finding,ids,typ='Recorded fact',**kw):
    return add('Overview',f'OV{n:02d}',{'Topic':topic,'Finding / value':finding},ids,typ,**kw)

ov(1,'Identity','Nirmala Sitharaman; BJP politician, born 18 August 1959 in Madurai, Tamil Nadu; living.',[1])
ov(2,'Current office','Union Minister of Finance and Corporate Affairs; resumed charge on 12 June 2024. BJP Rajya Sabha member for Karnataka, third parliamentary term from 1 July 2022.',[3,4,5,22],priority='High')
ov(3,'Education and professional formation','Economics graduate in Tiruchirappalli; MA at JNU. Parliamentary biography lists MPhil. Worked in research in London and public-policy work in Hyderabad before party prominence.',[1,2],note='Do not describe an unfinished doctoral project or PRS classification as a completed PhD.')
ov(4,'Entry into public and party life','NCW member in 2003–05; said in a 2010 interview that she joined BJP in 2006. National executive from 2008 and national spokesperson in 2010–14.',[1,7],note='Later official profiles say joined in 2008. Retain the conflict; executive membership and party entry are different events.')
ov(5,'Political geography','Tamil Nadu origins; first parliamentary seat through Andhra Pradesh in 2014, then Karnataka elections in 2016 and 2022. These were Rajya Sabha routes, not personal Lok Sabha victories.',[1,6,8,9],typ='Analysis')
ov(6,'Career in brief','Moved from professional research and women’s commission service into national party communications, then Commerce, Defence and Finance. Advancement depended on party selection and Cabinet responsibility rather than a direct-election base.',[1,2,30],typ='Analysis')
ov(7,'Major ministerial contributions','Her documented record includes the 2014 WTO stockholding negotiation, 2015 trade policy, 2019 corporate-tax cut, pandemic relief, tax-law reform and GST Council leadership.',[12,13,18,21,14,35],typ='Analysis')
ov(8,'Policy approach','Combines private-investment incentives, public capital spending, targeted welfare and economic self-reliance. Individual decisions are implemented through ministries, Cabinet, Parliament and, for GST, a collective council.',[10,13,14,18,34],typ='Analysis')
ov(9,'Limits of attribution','An announcement, legal adoption, expenditure and measured outcome are separate stages. Growth, employment and household welfare cannot be assigned to one minister from budget speeches alone.',[10,11,16],typ='Analysis')
ov(10,'Political and legal challenges','Rafale, pandemic support, Coimbatore GST and an electoral-bonds complaint generated scrutiny. SC dismissed the challenge to Kateel’s relief in February 2025; no personal guilt finding against Sitharaman is established by the reviewed records.',[23,24,26,31,16,42],typ='Analysis',priority='High')
ov(11,'Gender significance','First full-time woman Defence Minister in 2017 and Finance Minister in 2019. These milestones establish access to major portfolios; they do not alone demonstrate wider gains for women.',[2,33],typ='Analysis')
ov(12,'Historical assessment','An enduring senior minister across the transition from BJP parliamentary majorities to dependence on allies after 2024. Her legacy remains open while reforms and their distributional consequences continue to develop.',[3,29,21],typ='Analysis')
ov(13,'Research cutoff','Snapshot checked 24 September 2026. Latest MP dataset covers through 13 August 2026; recent ministry records cover the April 2026 tax-law commencement. This is a thematic career study, not an exhaustive daily chronicle.',[],typ='Method / scope')
ov(14,'Reading this workbook','Open All citations for every source on a row; Claims and Evidence show reviewed fields and passages. Expand grouped columns for policy roles, limits and context. Supported describes field review, not certainty about causation.',[],typ='Method / scope')
ov(15,'Principal unresolved questions','Original Rajya Sabha count sheets; definitive early BJP entry record; Sitharaman-specific final disposal of the electoral-bonds complaint; systematic gender treatment and independent outcomes of recent reforms.',[],typ='Method / scope')
ov(16,'Election and financial units','Rajya Sabha votes are legislators’ ballots; no popular vote share or single-opponent margin is calculated. Rs1 lakh crore = Rs100,000 crore. BE means budget estimate; RE means revised estimate; neither is audited actual spending.',[],typ='Method / scope')
ov(17,'Application and coverage checks','Four era phases and ten gender topics are reviewed. Evidence-not-found entries describe bounded research gaps. Spreadsheet structure, numerical checks, application recalculation and visual inspection are tested separately.',[],typ='Method / scope')

timeline=[
('1959','Birth','Born in Madurai on 18 August 1959.',[1],'1959-08-18',None),
('Before public office','Education and research','Economics studies in Tamil Nadu and JNU; research roles in London and policy work in Hyderabad preceded national party prominence.',[1,2],None,None),
('2003–2005','National Commission for Women','Served as an NCW member.',[1,2],None,P1),
('2006 / 2008','Party entry and executive role','In 2010 she dated joining BJP to 2006; parliamentary biography places national executive membership from 2008.',[7,1],None,P1),
('March 2010','National spokesperson','Joined BJP’s national spokesperson team under Nitin Gadkari; parliamentary biography records service through 2014.',[7,1],None,P1),
('May 2014','First Union ministerial appointments','From 26 May held Commerce and Industry independent charge alongside junior Finance and Corporate Affairs portfolios.',[1],'2014-05-26',P2),
('June 2014','First Rajya Sabha election','Declared elected unopposed from Andhra Pradesh on 26 June, according to a contemporaneous report citing an official release.',[6],'2014-06-26',P2),
('November 2014','WTO stockholding agreement','Reported to Parliament on 28 November after the WTO decision extending conditional stockholding protection.',[28,35],'2014-11-28',P2),
('April 2015','Foreign Trade Policy','Unveiled Foreign Trade Policy 2015–20 on 1 April.',[12],'2015-04-01',P2),
('June–July 2016','Shift to Karnataka','Won Karnataka Rajya Sabha election on 11 June; resigned AP seat effective 17 June; second parliamentary term began in July.',[8,1],None,P2),
('September 2017','Defence portfolio','Parliamentary tenure starts 3 September; PIB announced taking charge on 7 September. First full-time woman in the post.',[1,2],None,P2),
('September 2018','India–US 2+2 dialogue','Participated with Sushma Swaraj on 6 September; COMCASA signed during the ministerial visit.',[36],'2018-09-06',P2),
('May 2019','Finance and Corporate Affairs','Parliamentary tenure starts 30 May; assumed charge on 31 May as first full-time woman Finance Minister.',[1,33],None,P3),
('September 2019','Corporate-tax reduction','Announced an ordinance offering reduced corporate-tax rates subject to conditions.',[13],'2019-09-20',P3),
('March 2020','Pandemic relief','Announced the Rs1.70 lakh crore Garib Kalyan package on 26 March.',[18],'2020-03-26',P3),
('August 2021','Retrospective-tax reversal','Introduced amendment bill on 5 August; both Houses passed it by 9 August.',[19],'2021-08-05',P3),
('January 2022','Air India transfer','Finance Ministry recorded completion of the transfer to Tata’s Talace on 27 January.',[20],'2022-01-27',P3),
('June–July 2022','Third parliamentary term','Elected again from Karnataka on 10 June; third Rajya Sabha term began 1 July.',[9,5],None,P3),
('March 2024','Declined Lok Sabha contest','Said she had declined a party offer, citing campaign resources and winnability; planned to campaign for others.',[30],None,P3),
('June 2024','Retained Finance portfolio','Resumed charge of Finance and Corporate Affairs on 12 June following formation of the new government.',[3],'2024-06-12',P4),
('September 2024–February 2025','Electoral-bonds complaint and challenge','Named in a September FIR; December orders quashed proceedings for Kateel and Vijayendra. SC dismissed Iyer’s challenge to Kateel’s relief on 3 February 2025.',[23,24,32,42],None,P4),
('February 2025','Income-tax rebate announcement','Budget proposed a larger new-regime rebate; Rs12 lakh normal income threshold was distinct from the basic nil slab.',[17],'2025-02-01',P4),
('September 2025','GST rate overhaul','Chaired the 56th Council; recommendations on 3 September followed by goods-rate notifications on 17 September.',[14,15],None,P4),
('February–April 2026','Budget and new tax statute','Presented 2026–27 Budget; launched PRARAMBH awareness campaign in March; Income-tax Act 2025 commenced 1 April.',[10,22,21],None,P4),
]
for n,(period,event,desc,ids,day,phase) in enumerate(timeline,1):
    ctx={P1:'E101',P2:'E202',P3:'E304',P4:'E401'}.get(phase,'')
    add('Career Timeline',f'T{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':day},ids,phase=phase,context=ctx)

elections=[
('EL01',2014,'Andhra Pradesh','Elected unopposed',None,'2014-06-26',[6,44],'Rajya Sabha / indirect',P2,'Unopposed by-election; TDP support. Parliament’s annual report independently confirms entry through the AP by-election.'),
('EL02',2016,'Karnataka','Elected',47,'2016-06-11',[8,45],'Rajya Sabha / indirect',P2,'47 legislator votes reported independently by IANS and Indian Express. Date is polling day; formal declaration was delayed at the latter report’s publication.'),
('EL03',2022,'Karnataka','Elected',46,'2022-06-10',[9,5],'Rajya Sabha / indirect',P3,'Reported first-preference votes; parliamentary term began 1 July 2022.'),
('EL04',2024,'AP / Tamil Nadu offer','Declined',None,None,[30],'Lok Sabha / not contested',P3,'Her account of declining an offer, not a filed nomination or electoral defeat.'),
]
for rid,year,seat,result,votes,day,ids,route,phase,finding in elections:
    add('Elections',rid,{'Year':year,'Constituency':seat,'Result':result,'Candidate votes':votes,'Election date':day,
        'House / route':route,'Party':'BJP','Opponent votes':None,'Vote share':None,'Principal opponent':'Not applicable: multi-seat indirect election or no contest',
        'Finding':finding,'Vote unit':'Legislator ballots' if route=='Rajya Sabha / indirect' else 'Not applicable'},ids,phase=phase,context='E203' if phase==P2 else 'E303',
        checked={k:ids for k,v in {'Result':result,'Candidate votes':votes,'Election date':day,'Finding':finding}.items() if v is not None},
        note='Original returning-officer declarations/count sheets remain a gap. 2014 parliamentary entry has primary corroboration. Blank shares and margins are intentionally inapplicable.')

offices=[
('OF01','Member, National Commission for Women','2003–2005','Statutory commission service preceded national party office.',[1,2],None,None,P1,'Commission appointment'),
('OF02','BJP national executive member','From 2008; historical record through 2020','Parliamentary biography records executive membership beginning 2008; this is distinct from joining BJP.',[1],None,None,P1,'Party selection'),
('OF03','BJP national spokesperson','2010–2014','National communication role; introduced in Gadkari’s spokesperson team.',[1,7],None,None,P1,'Party selection'),
('OF04','MoS, Commerce and Industry (independent charge)','26 May 2014–3 September 2017','Led the Commerce portfolio with independent charge at Minister of State rank.',[1],'2014-05-26','2017-09-03',P2,'Union ministerial appointment'),
('OF05','MoS, Finance','26 May–9 November 2014','Junior Finance portfolio concurrent with Commerce and Corporate Affairs.',[1],'2014-05-26','2014-11-09',P2,'Union ministerial appointment'),
('OF06','MoS, Corporate Affairs','26 May–9 November 2014','Junior Corporate Affairs portfolio during first Union appointment.',[1],'2014-05-26','2014-11-09',P2,'Union ministerial appointment'),
('OF07','Rajya Sabha member, Andhra Pradesh','June 2014–17 June 2016','Entered through unopposed by-election; resignation effective 17 June 2016.',[1,6],None,'2016-06-17',P2,'Indirect election'),
('OF08','Rajya Sabha member, Karnataka: second term','July 2016–2022','Second parliamentary term followed Karnataka election in June 2016.',[1,8,5],None,None,P2,'Indirect election'),
('OF09','Union Minister of Defence','3 September 2017–30 May 2019','Cabinet Defence portfolio. Charge-taking was scheduled for 7 September from Arun Jaitley, who held additional charge.',[1,2],'2017-09-03','2019-05-30',P2,'Union Cabinet appointment'),
('OF10','Union Minister of Finance and Corporate Affairs','May 2019–June 2024 government','Tenure recorded from 30 May 2019; took charge 31 May. Reappointed in the next government.',[1,33,3],'2019-05-30',None,P3,'Union Cabinet appointment'),
('OF11','Rajya Sabha member, Karnataka: third term','From 1 July 2022; in office at cutoff','PRS records third term beginning 1 July 2022; ministers’ parliamentary activity metrics are not comparable with backbench MPs.',[5],'2022-07-01',None,P4,'Indirect election'),
('OF12','Union Minister of Finance and Corporate Affairs','From June 2024; in office at cutoff','Took charge again on 12 June 2024. Ministry records identify both portfolios in March 2026; DFS lists her as Finance Minister.',[3,22,4],None,None,P4,'Union Cabinet reappointment'),
('OF13','Chair, GST Council','Finance-minister role; September 2025 meeting verified','Chaired the 56th GST Council meeting, a collective Union–state policy forum.',[14],None,None,P4,'Ex officio ministerial function'),
]
for rid,title,period,finding,ids,start,end,phase,route in offices:
    add('Offices & Party',rid,{'Position / institution':title,'Period':period,'Finding':finding,'Start date':start,'End date':end,'Selection route':route},ids,phase=phase,context='G04' if rid in ('OF09','OF10','OF12') else {P1:'E107',P2:'E202',P3:'E302',P4:'E402'}[phase])

def policy(n,title,period,domain,finding,role,stage,ids,phase,limit,context=''):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':title,'Finding':finding,'Stage':stage,'Period':period,'Policy domain':domain,
        'Documented role':role,'Attribution / outcome limit':limit},ids,phase=phase,context=context or {P2:'E204',P3:'E304',P4:'E404'}[phase])

policy(1,'WTO stockholding and trade facilitation','2014','Trade / agriculture','India obtained continuation of conditional protection for qualifying food-stockholding support until a permanent solution. The WTO decision also required continued negotiations.','Negotiating minister; reported the settlement to Parliament and credited Modi and wider support.','Multilateral decision, 27 November 2014',[28,35],P2,'Shared diplomatic result; not permanent removal of all agricultural subsidy disciplines. Farmers’ realised gains not measured.','E205')
policy(2,'Foreign Trade Policy 2015–20','2015','Trade','MEIS and SEIS consolidated merchandise and service export incentives through duty-credit scrips.','Unveiled policy as Commerce Minister.','Policy launched 1 April 2015',[12],P2,'Design and launch established; export growth cannot be attributed without exchange-rate, demand and comparator analysis.')
policy(3,'India–US COMCASA','2018','Defence / diplomacy','Agreement signed during first 2+2 dialogue involving Sitharaman and Swaraj; intended to improve use of US-origin defence systems.','Participating Defence Minister alongside foreign-policy and US counterparts.','Agreement signed 6 September 2018',[36],P2,'Shared bilateral achievement; operational capability outcomes not evaluated.','E205')
policy(4,'Defence planning and procurement','2017–2019','Defence','Ministry credited her with constituting the Defence Planning Committee and accelerating procurement decisions.','Responsible Defence Minister; official assessment of her tenure.','Committee creation reported in 2019 official profile',[33],P2,'Attributed government assessment; no independent readiness audit supports a general performance ranking.')
policy(5,'Corporate-tax reduction','2019','Tax / investment','Optional base rate of 22% for domestic companies foregoing specified incentives; 15% for qualifying new manufacturing. Ordinary effective rate including surcharge and cess: 25.17%.','Announced ordinance as Finance Minister.','Ordinance announced 20 September 2019',[13],P3,'Government estimated Rs1,45,000 crore revenue forgone for package; this is not an audited cost or demonstrated investment gain.')
policy(6,'Ten public-sector banks consolidated into four','2020','Banking','Cabinet approved combinations into PNB, Canara, Union Bank and Indian Bank, aiming at scale and technology benefits.','Finance Ministry responsibility; Cabinet chaired by Modi approved.','Approved 4 March; effective date 1 April 2020',[34],P3,'Approval record supports institutional change; efficiency, access and integration costs require separate evaluation.')
policy(7,'Pradhan Mantri Garib Kalyan relief','March 2020','Welfare / crisis response','Announced Rs1.70 lakh crore in food, cash and insurance measures during the pandemic.','Finance Minister announcing government package.','Relief package announced 26 March 2020',[18],P3,'Package size and intended coverage do not demonstrate universal receipt or net additional spending.')
policy(8,'Women’s cash support and SHG credit','March 2020','Gender / welfare','Women Jan Dhan account holders were promised Rs500 monthly for three months; SHG collateral-free lending limit rose from Rs10 lakh to Rs20 lakh.','Announced targeted components of government relief.','Announced programme and credit-limit change',[18],P3,'Accounts, eligibility, actual access and control of funds must be measured separately.','G07')
policy(9,'Pandemic package accounting and adequacy','2020–2021','Fiscal policy','IMF distinguished announced direct fiscal support of 4.1% GDP from below-line measures of 6.2%; recommended additional near-term support around 1% GDP above baseline.','Finance Minister during government-wide response; IMF assessment is of India’s fiscal stance.','Historical staff assessment, August 2021',[16,1],P3,'Figures are a dated estimate; guarantees and liquidity are not the same as cash expenditure. Recommendation is not a finding of personal misconduct.')
policy(10,'Bringing food subsidies onto budget','2021','Fiscal transparency','IMF welcomed recognition of off-budget food subsidies in the budget as a transparency improvement.','Finance Ministry budget responsibility.','Budget-accounting change assessed by IMF in 2021',[16,1],P3,'Improved reporting should not be confused with an equal increase in newly delivered food support.')
policy(11,'Reversal of retrospective indirect-transfer taxation','2021','Tax / investment','Parliament passed reversal for pre-28 May 2012 transactions, conditional on ending specified disputes and claims; refunds excluded interest.','Introduced amendment bill on 5 August 2021.','Passed both Houses by 9 August 2021',[19],P3,'Policy correction and passage verified; completion of individual settlements needs separate evidence.')
policy(12,'Air India privatisation','2022','Public enterprises','Transfer to Talace completed: Rs2,700 crore cash and Rs15,300 crore debt retained in transferred airline entities.','Finance Ministry’s disinvestment responsibility; shared government transaction.','Transfer completed 27 January 2022',[20,1],P3,'Enterprise value is not cash proceeds. Retained legacy liabilities and a net fiscal evaluation are outside this source.')
policy(13,'2025 personal income-tax rebate','2025 Budget','Tax / households','Budget proposed a rebate eliminating normal-rate tax up to Rs12 lakh under the new regime; salary illustration Rs12.75 lakh included the standard deduction.','Finance Minister presenting tax proposals.','Budget proposal inspected',[17],P4,'Special-rate income excluded; Rs12 lakh is not the basic nil slab. Subsequent statutory detail and consumption effects not audited here.')
policy(14,'GST rate rationalisation','September 2025','Indirect tax / federalism','Council recommended main 5% and 18% rates with a special 40% rate for selected supplies; most changes scheduled from 22 September, with specified tobacco exceptions.','Chaired GST Council; collective recommendations followed by government notifications.','Council decision plus goods-rate notification record',[14,15],P4,'Do not describe every supply as having only two rates. Price pass-through, revenue and compliance outcomes need independent study.','E402')
policy(15,'Individual life and health insurance GST','September 2025','Insurance / households','56th Council recommended exemption for individual life and health insurance policies.','Council chair; shared Union–state decision.','Recommendation inspected; general implementation timetable announced',[14],P4,'Specific service notification not separately retrieved. Lower tax does not automatically establish equal premium reduction.')
policy(16,'Income-tax Act 2025','2025–2026','Tax administration','New statute replaced the 1961 Act from 1 April 2026. Ministry described the recast as structural simplification without changing underlying tax policy.','Finance Ministry legislative and administrative responsibility.','Commenced 1 April 2026; assent 21 August 2025',[21],P4,'Commencement established; compliance savings and dispute reduction are not yet demonstrated in this study.')
policy(17,'PRARAMBH tax awareness campaign','March 2026','Administration / communication','Launched multimedia and multilingual tax-law awareness campaign; urged empathetic administration and fewer frequent amendments.','Personally launched campaign and articulated administrative approach.','Launch on 20 March 2026',[22],P4,'Public outreach is an output; taxpayer understanding or service improvement is not measured.','E406')
policy(18,'SHE-Marts','2026–27 Budget','Women / enterprise','Proposed community-owned retail outlets through cluster-level federations to connect women’s enterprise with market access.','Budget proposer.','Budget proposal, February 2026',[10],P4,'Rollout and income effects not independently verified.','G07')
policy(19,'Fiscal consolidation and debt path','2026–27 Budget','Fiscal policy','Deficit: 4.4% GDP in 2025–26 RE and 4.3% in 2026–27 BE; central debt target 50±1% GDP by 2030–31.','Finance Minister presenting fiscal framework.','Estimates and medium-term target',[10,11],P4,'These are not audited outcomes; central-government debt is distinct from combined Centre–state debt.')
policy(20,'Public capital expenditure','2026–27 Budget','Infrastructure / public investment','PRS identifies planned capital spending of Rs12.2 lakh crore for 2026–27; interest consumes 26% of budgeted expenditure and 40% of revenue receipts.','Budget presenter within government spending process.','Budget allocation / estimates',[11],P4,'Execution is shared with departments and states; allocation does not establish asset quality or employment gains.')
policy(21,'Tax devolution to states','2026–27 Budget','Federal finance','Budget accepted retaining 41% vertical tax devolution and provided Rs1.4 lakh crore in Finance Commission grants for 2026–27.','Presented government’s response to Finance Commission recommendations.','Budget provision and acceptance statement',[10],P4,'41% concerns the divisible tax pool, not all Union revenue. State-by-state fiscal effects not evaluated.','E409')
policy(22,'Atmanirbhar Bharat and ECLGS','2020','Business credit / crisis response','Sitharaman detailed the package in May and reviewed implementation. Initial ECLGS guarantee envelope was Rs3 lakh crore; ministry reported Rs1,32,246 crore loan disbursement by 29 September 2020.','Explained and monitored the package announced by Modi.','Guarantee scheme operational; dated administrative output reported',[39],P3,'Headline package totals included different instruments. Guaranteed bank loans are not equivalent to government expenditure or proven jobs saved.')
policy(23,'Employment, skilling and internships','2024–25 Budget','Employment','Budget announced EPFO-linked employment incentives, skilling and internships; this signals an explicit employment-policy emphasis.','Presented Budget on 23 July 2024.','Budget announcements inspected',[38],P4,'Targets are not jobs created. Subsequent implementation and additionality require separate programme evidence.')
policy(24,'Andhra Pradesh capital assistance','2024–25 Budget','Federal development','Budget proposed Rs15,000 crore support for Andhra Pradesh’s new capital.','Presented government’s state-assistance proposal.','Budget proposal inspected',[38],P4,'Amount is announced financial support, not verified spending. Coalition motive cannot be established from allocation alone.','E409')

ideas=[
('BJP alignment','She explained joining BJP through agreement with its ideology. That establishes self-described affiliation; a separate personal political philosophy cannot be inferred solely from Cabinet office.',[7],P1,'G01'),
('Professional communication route','Research training, English and southern-language fluency and a national spokesperson role formed an identifiable route to prominence; the 2010 profile also discussed learning Hindi.',[2,7],P1,'E106'),
('Trade openness with policy protection','The WTO negotiation and export policy show support for international market access alongside defence of domestic food-security policy space.',[12,28,35],P2,'E205'),
('Strategic cooperation and autonomy','In her 2018 interview she defended stronger US cooperation while maintaining Russian ties; COMCASA supplies an institutional example.',[27,36],P2,'E205'),
('Private incentives and public investment','Corporate-tax reductions and later capital-spending budgets combine private-investment incentives with active government investment. This is synthesis of policies, not a claim of ideological consistency in every case.',[13,11],P4,'E404'),
('Targeted welfare and enterprise','Women’s account transfers, SHG credit and proposed SHE-Marts use financial access and enterprise instruments; beneficiary empowerment remains an outcome question.',[18,10],P4,'G07'),
('Reform continuity and political trust','On resuming office in 2024 she thanked Modi and pledged reform continuity. Reappointment supports an inference of sustained leadership confidence; it does not reveal internal Cabinet bargaining.',[3],P4,'E407'),
('Administrative predictability','Her 2026 tax-campaign remarks advocated stable law, empathy, regional-language communication and technology-assisted administration.',[22],P4,'E406'),
('Campaigning without a personal Lok Sabha contest','Her stated 2024 decision combined declining candidacy with willingness to campaign for others. Treat personal resources and community winnability as her explanation, not proven electoral incapacity.',[30],P3,'E303'),
('Cultural and national framing','Budget 2026 placed policy in an Atmanirbharta framework; the 2025 tax announcement invoked the Thirukkural. National and Tamil cultural references coexist in her public economic presentation.',[10,17],P4,'G08'),
]
for n,(topic,finding,ids,phase,ctx) in enumerate(ideas,1):
    add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding},ids,'Analysis',phase,ctx)

controversies=[
('CV01','Rafale procurement scrutiny','Petitioners challenged procedure, pricing and offsets; she defended the 36-aircraft procurement. SC dismissed review on 14 November 2019 within Article32 limits; Joseph’s concurrence preserved a lawful CBI route subject to prior approval.','Defended procurement urgency and infrastructure rationale in the inspected 2018 interview.','Review dismissed; this was not a personal criminal adjudication of Sitharaman.',[27,26,43],P2,'Official review judgment inspected. Joseph paragraphs 85–87 refer to section17A approval. No subsequent investigation or comprehensive procurement audit is inferred.'),
('CV02','Pandemic support: size and adequacy','Government announced substantial relief; IMF separated direct fiscal measures from financing support and argued for additional near-term fiscal help in 2021.','Government’s announced food, cash and credit measures are documented; no direct reply to this IMF recommendation was inspected.','Policy disagreement and fiscal assessment, not litigation.',[18,16],P3,'The critique concerns design and adequacy of the national response. Do not treat all headline support as budget spending.'),
('CV03','Coimbatore GST exchange and apology video','In September 2024 a business owner’s GST questions and a purported apology video prompted Congress and DMK criticism. NDTV could not authenticate the second video; TOI reported removal of the party functionary who circulated it.','Sitharaman had said she would consider the GST issue; Annamalai apologised for party functionaries sharing the private exchange.','Political controversy; coercion or intent not established in reviewed evidence.',[31,40],P4,'Do not state as fact that the minister forced an apology. Specific current GST rates are not established by the anecdote.'),
('CV04','Electoral-bonds extortion allegation','Adarsh Iyer’s complaint led to a September 2024 FIR naming Sitharaman and others; coercion allegations are unproven. HC granted Kateel and Vijayendra relief separately; SC dismissed Iyer’s challenge to Kateel’s relief on 3 February 2025.','Allied leader Kumaraswamy rejected resignation demands by disputing personal benefit; BJP’s Ashoka promised legal action. No direct ministerial merits response inspected.','SC: SLP(Crl)1183/2025 dismissed, with recourse preserved for material evidence. Sitharaman-specific operative disposal not verified.',[23,24,32,41,42],P4,'Courts found missing prima-facie material in this complaint. Do not infer a personal acquittal or a continuing active prosecution from incomplete docket access.'),
('CV05','Broad electoral-bonds headlines versus court orders','A Bar & Bench headline described relief against Sitharaman and others. The later Vijayendra order explicitly explains that Kateel’s earlier operative relief covered Kateel alone.','Use the court’s operative wording to qualify the broader news description.','Reporting discrepancy resolved for order scope; latest personal case status remains open.',[25,23,24],P4,'Do not label Sitharaman acquitted, convicted or personally discharged on the strength of these two orders.'),
('CV06','Biography discrepancies','A contemporaneous 2010 interview gives BJP entry as 2006; later ministry profiles say 2008. PRS labels education Doctorate, while Parliament lists MA and MPhil.','No direct clarification of these discrepancies was retrieved.','Conflicting biographical records; no misconduct allegation is made.',[7,2,5,1],P1,'Prefer explicit qualifications in parliamentary biography and attribute the joining-year claim. A draft doctoral thesis is not evidence of completion.'),
]
for rid,title,finding,response,stage,ids,phase,note in controversies:
    add('Controversies',rid,{'Matter':title,'Finding':finding,'Response':response,'Procedural status':stage},ids,'Analysis',phase,{P1:'E110',P2:'E210',P3:'E304',P4:'E410'}[phase],note=note,priority='High' if rid in ('CV01','CV04','CV05') else 'Normal')

legacy=[
('Portfolio milestones','Her Defence and Finance appointments widened the documented history of women holding major full-time Union portfolios. Symbolic representation is established; wider institutional equality requires separate evidence.',[2,33],'Workbook synthesis','G02'),
('Institutional rather than constituency power','Her professional, spokesperson and indirect-election route illustrates national executive influence without a personal Lok Sabha victory. This differs from measuring leadership by constituency margins.',[1,6,8,9,30],'Workbook synthesis','E303'),
('Reform record','Tax-rate changes, retrospective-tax reversal and the new tax statute show sustained intervention in the tax framework. Adoption is better evidenced than net investment, compliance or distributional gains.',[13,19,21],'Workbook synthesis','E404'),
('Fiscal transparency and adequacy','IMF’s 2021 assessment welcomed on-budget food subsidies while recommending further near-term support. Positive accounting reform and criticism of fiscal adequacy can coexist.',[16],'IMF assessment and workbook synthesis','E304'),
('Defence record in contemporary government memory','The Finance Ministry’s 2019 profile praised her procurement and planning work. Her own interview stressed operational urgency. These are contemporary supportive accounts, not independent military-performance evaluations.',[33,27],'Government and subject','E210'),
('Public reception and accountability','The Coimbatore episode shows how taxpayer interaction, regional self-respect and online circulation can turn a technical tax discussion into political criticism. The evidence does not establish compelled apology.',[31],'Contemporary opponents and workbook synthesis','E406'),
('Durability across political eras','She retained Finance after BJP lost its single-party majority in 2024. Continuity amid coalition dependence is a significant career fact; her personal share in electoral or macroeconomic results remains unquantified.',[3,29],'Workbook synthesis','E401'),
('Legacy still developing','The 2025 GST changes and April 2026 income-tax-law commencement are recent institutional changes. A durable legacy judgment needs implementation, incidence and administrative evidence over time.',[14,15,21],'Provisional workbook synthesis','E410'),
]
for n,(theme,assessment,ids,assessor,ctx) in enumerate(legacy,1):
    add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor':assessor,'Assessment status':'Provisional; subject remains in office'},ids,'Analysis',context=ctx)

# Context module adds the mandatory ten gender and ten era items per phase.
exec(Path(__file__).with_name('author_context.py').read_text())

gaprows=[
('High','Personal electoral-bonds case status','SC dismissal of Iyer’s Kateel challenge on 3 February 2025 is reported; signed SC order and a Sitharaman-specific operative disposal have not been verified.','Retrieve SLP(Crl)1183/2025 order and Karnataka HC docket by FIR224/2024, PCR4880/2024 and party name.', ['CV04','CV05']),
('High','Primary Rajya Sabha returns','Parliament confirms AP entry in 2014; two independent reports agree on 47 votes in 2016. Exact declaration/count records and 2022 primary count remain uncollected.','Retrieve Andhra Pradesh 2014 declaration and Karnataka 2016/2022 signed return/count sheets.',['EL01','EL02','EL03']),
('Normal','BJP entry and qualifications','Sources disagree on joining year; completed doctorate not established.','Locate party membership record and university credential confirmation; retain 2006 attribution and parliamentary MA/MPhil meanwhile.',['OV03','OV04','CV06']),
('Normal','Rafale primary review order','Resolved: official Supreme Court PDF inspected, including review dismissal and Joseph’s qualification on lawful investigation with prior approval.','No further retrieval required for this order; refresh if assessing subsequent proceedings.',['CV01']),
('High','Recent reform outcomes','GST, tax-code and SHE-Marts records establish different adoption stages; causal household, firm and revenue effects unresolved.','Use subsequent implementation reports, audit findings, household/firm data and credible comparison designs.',['PG14','PG15','PG16','PG18']),
('Normal','Gender mechanisms and security','Milestones and bounded treatment examples exist; systematic differential treatment, gender-specific threats and causal promotion evidence not established.','Build matched contemporary media sample and seek documented incidents or reliable biographical research.',['G01','G05','G06','G09']),
('Normal','Disinvestment net fiscal effects','Air India transfer terms do not capture all retained government liabilities or long-run fiscal consequences.','Compare DIPAM closing disclosures, AIAHL accounts, CAG analysis and subsequent liability servicing.',['PG12']),
('Normal','Women’s programme outcomes','Cash, credit and retail proposals are documented; recipient access and control over benefits not independently evaluated.','Review programme administrative reports and independent sex-disaggregated impact studies.',['PG08','PG18','G09']),
('Normal','Early context and network depth','Professional and party-entry sources are thin on specific pre-2014 policy views, organisational authority and international agenda.','Seek contemporaneous speeches, NCW annual reports and dated party organisational records.',['E104','E105','E107']),
]
for n,(priority,topic,gap,next_action,records) in enumerate(gaprows,1):
    gaps.append({'id':f'GAP{n:02d}','priority':priority,'topic':topic,'gap':gap,'next_action':next_action,'record_ids':records,'status':'Resolved' if gap.startswith('Resolved:') else 'Open'})

data={'schema_version':1,'subject':'Nirmala Sitharaman','as_of':ASOF,
    'guidance':'Assess gender and political era against contemporary institutions and comparators. Milestones are not causal proof; present-day electoral or media norms should not be projected backwards.',
    'tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'coverage':coverage,'phases':phases,'gaps':gaps}
root=Path(__file__).parent
root.joinpath('research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
root.joinpath('retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(f'Authored {sum(len(t["rows"]) for t in tables.values())} records, {len(claims)} field claims, {len(sources)} sources.')
