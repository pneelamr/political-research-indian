"""Reproducible, passage-reviewed political research; internal authoring file."""
import hashlib
import json
from pathlib import Path
from author_sources import ASOF, sources, retrievals

tables, claims, evidence, gaps = {}, [], [], []
R = {r['source_id']:r for r in retrievals if r['access_status']=='Passage inspected'}
P1='P1 | Congress formation and Parliament (1970s–1997)'
P2='P2 | Party building and movements (1998–May 2011)'
P3='P3 | First two state governments (May 2011–May 2021)'
P4='P4 | Third state government (May 2021–May 2026)'
P5='P5 | Defeat and party dispute (May–September 2026)'
phases=[P1,P2,P3,P4,P5]

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

ov(1,'Identity','Mamata Banerjee; Bengali: মমতা বন্দ্যোপাধ্যায়; also known as Didi. Official birth date: 5 January 1955, Kolkata, West Bengal.',[1,14,45])
ov(2,'Status at cutoff','Former West Bengal Chief Minister (2011–May 2026). Lost Bhabanipur in 2026; Suvendu Adhikari took oath as successor on 9 May. September 28 court reporting records a timetable for ECI to decide her faction’s party-name and symbol dispute.',[10,11,55],priority='High')
ov(3,'Education and cultural work','Official biography lists MA, BEd and LLB qualifications, and writing in Bengali and English. Cultural work became part of her public persona.',[1,14],typ='Analysis')
ov(4,'Party trajectory','Congress activist and MP; broke away in 1997 and publicly launched Trinamool Congress on 1 January 1998. Party organisation and legal recognition are under dispute after the 2026 defeat.',[1,45,46,56],note='1997 organisational formation and 1998 launch are distinct milestones; avoid assigning both the same meaning.')
ov(5,'Principal political geography','Her elected base moved from Jadavpur to Calcutta South, later named Kolkata Dakshin, and then Bhabanipur. Nandigram was both a formative movement site and the constituency where she lost in 2021.',[3,8,9,15,35],typ='Analysis')
ov(6,'Career in brief','Congress organiser and seven-time Lok Sabha winner became a regional party founder, Union minister and three-term state leader; 2026 brought electoral defeat and a struggle over party identity.',[1,32,33,34,11,12],typ='Analysis')
ov(7,'Movement contribution','Singur and Nandigram land struggles helped build a wider anti-Left coalition. Gupta’s biography stresses participation by peasants, intellectuals and former Left supporters.',[15],typ='Attributed assessment')
ov(8,'Governance record','Her governments made girls’ education, women’s transfers, health cover, bicycles and service-access camps prominent. Programme design is well documented; independent outcome evidence is uneven.',[17,18,28,39,49],typ='Analysis')
ov(9,'Leadership method','Chaudhury interprets her Didi persona as gendered political kinship combined with austerity and personalised leadership. This is a scholarly interpretation, not a voter-level causal estimate.',[14],typ='Attributed assessment')
ov(10,'Principal challenges','Recruitment invalidation, political violence, corruption investigations and failures of safety at RG Kar generated serious scrutiny of institutions under her government. These matters have different defendants, evidence and procedural outcomes.',[20,23,26,41],typ='Analysis',priority='High')
ov(11,'Gender significance','West Bengal’s first woman CM combined a landmark in representation with women-focused welfare. Critical episodes concerning sexual violence prevent a simple equation between a woman leader and institutional gender equality.',[32,17,47,23],typ='Analysis')
ov(12,'Fiscal assessment','The record combines expanded transfers with constraints on investment execution and state finances. PRS reports are used with their estimate vintages; successor-government spending plans are not attributed to her.',[18,19,43],typ='Analysis')
ov(13,'Personal elections covered','Thirteen personal contests: eight Lok Sabha contests (seven wins, one loss) and five Assembly contests (three wins, two losses). Party-wide performances are recorded separately in the timeline.',[3,4,5,6,7,8,9,10,35,36,37],typ='Analysis')
ov(14,'Research cutoff','30 September 2026. Court status is dated to the latest inspected record for each case; absence of a later order in this study is not proof that no later order exists.',[],typ='Method / scope')
ov(15,'Reading guide','Use All citations to open every source for a row. Claims and Evidence expose reviewed fields and passage notes. Expand the + columns for roles, dates, limitations and context. Review counts are not completeness scores.',[],typ='Method / scope')
ov(16,'Election definitions','Signed margin equals Banerjee votes minus the principal opponent’s votes. Negative means defeat. Shares are stored as fractions and displayed as percentages; historical denominators vary. Blank shares are unresolved, not zero.',[],typ='Method / scope')
ov(17,'Policy and financial definitions','Rs1 crore = Rs10 million. BE is budget estimate; RE is revised estimate. Sanction, enrolment, expenditure and impact are distinct. State outcomes reflect governments, institutions and external conditions.',[],typ='Method / scope')
ov(18,'Main open questions','Signed September 2026 party orders; older primary election returns; exact dates of short ministerial appointments; subsequent case outcomes; and independent long-run welfare, investment and employment effects.',[],typ='Method / scope')

timeline=[
('1955','Birth','Official profile records birth in Kolkata on 5 January 1955.',[1],'1955-01-05',None),
('1970s–1980s','Congress organisation','Worked in Congress women’s and youth organisations before entering Parliament.',[1],None,P1),
('1984','First Lok Sabha victory','Defeated Somnath Chatterjee in Jadavpur as Congress candidate.',[3],None,P1),
('1989','First parliamentary defeat','Lost Jadavpur to Malini Bhattacharya of CPM.',[4],None,P1),
('1990','Hazra assault','Retrospective reporting describes a serious head injury in an assault at Hazra, later central to her fighter image.',[46],None,P1),
('1991','Return and junior ministry','Won Calcutta South and entered the Union HRD ministry.',[1,5],None,P1),
('21 July 1993','Youth Congress demonstration','Thirteen died in police firing during a Youth Congress demonstration; a later commission criticised the firing.',[44],'1993-07-21',P1),
('1997–1998','Congress split and party launch','Break from Congress in 1997 preceded Trinamool’s public foundation on 1 January 1998.',[45,46],None,P2),
('1999–2001','First Railways term in NDA','Railways tenure ran from 13 October 1999 to 16 March 2001 in the BJP-led NDA. She left the alliance amid the Tehelka controversy and allied with Congress for the 2001 state election.',[1,54],'1999-10-13',P2),
('2003–2004','Return to Union executive','Historical CMO profile lists a short period without portfolio before Coal and Mines; PIB confirms the latter portfolio.',[1,2],None,P2),
('2006–2009','Land movements','Singur, Nandigram and Lalgarh struggles broadened her opposition coalition in Gupta’s account.',[15],None,P2),
('26 May 2009','Second Railways charge in UPA-II','Assumed Railway charge again following her seventh Lok Sabha victory and her party’s entry into Congress-led UPA-II.',[1,54],'2009-05-26',P2),
('16 November 2010','Dankuni freight corridor','Railways announced commencement of initial corridor work at Dankuni under her ministerial leadership.',[48],'2010-11-16',P2),
('20 May 2011','First Chief Minister oath','Became first woman CM of West Bengal after the end of 34 years of Left Front government.',[32],'2011-05-20',P3),
('18 July 2011','GTA agreement','Union government, West Bengal and GJM signed the territorial-administration agreement.',[29],'2011-07-18',P3),
('September 2011','Bhabanipur bypoll','Won the by-election after taking office as CM; result announced 28 September.',[37],None,P3),
('18 September 2012','UPA withdrawal announcement','Announced withdrawal of support over retail FDI, diesel prices and LPG restrictions.',[30],'2012-09-18',P3),
('27 May 2016','Second Chief Minister oath','Began her second government after re-election.',[33],'2016-05-27',P3),
('31 August 2016','Singur judgment','Supreme Court invalidated the earlier land acquisition and ordered restoration.',[16],'2016-08-31',P3),
('December 2020','Service access expansion','Duare Sarkar camps began; Swasthya Sathi scope expanded under its stated eligibility rules.',[28,39],None,P3),
('May 2021','Third government, personal defeat','Took oath on 5 May after TMC’s victory despite losing Nandigram to Adhikari.',[34,35],'2021-05-05',P4),
('October 2021','Return to Assembly','Won Bhabanipur by-election, restoring her personal Assembly mandate.',[9],None,P4),
('2024 Lok Sabha election','Party victory in Bengal','TMC won 29 of 42 Bengal seats, seven more than 2019. She led the party but was not a Lok Sabha candidate.',[51],None,P4),
('August 2024–January 2025','RG Kar crisis and sentence','Supreme Court intervened on institutional safety; trial court later sentenced Roy to whole-life imprisonment.',[23,24],None,P4),
('April–August 2025','Recruitment litigation','Supreme Court maintained cancellation of the recruitment process and dismissed review; separate Cabinet-investigation relief had narrower scope.',[20,21],None,P4),
('May 2026','Defeat and succession','Lost Bhabanipur; Adhikari took oath as CM on 9 May. BJP later won delayed Falta, adding to its initial 207-seat result.',[10,11,52],None,P5),
('23 June 2026','Election petition admitted','High Court admitted her Bhabanipur challenge and protected election materials; did not overturn the result in this order.',[22],'2026-06-23',P5),
('17–28 September 2026','Party identity dispute','Reports describe interim party-name/symbol arrangements. September 28 hearing reports give parties four weeks for pleadings and ECI three months thereafter for its decision.',[13,55,56],None,P5),
]
for n,(period,event,desc,ids,day,phase) in enumerate(timeline,1):
    pending=n==10
    add('Career Timeline',f'T{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':day},ids,
        phase=phase,context=f'E{phases.index(phase)+1}01' if phase else '',status='Not reviewed' if pending else 'Supported',
        note='Short no-portfolio tenure is cached-only; primary chronology pending.' if pending else '')

elections=[
(1984,'Jadavpur','INC',331618,'Somnath Chatterjee','CPM',311958,'Won',3,'1984-12-24',P1,331618/651905,'Valid votes: 651905; rejected ballots excluded.'),
(1989,'Jadavpur','INC',410288,'Malini Bhattacharya','CPM',441188,'Lost',4,'1989-11-24',P1,410288/879040,'Valid votes: 879040; personal defeat.'),
(1991,'Calcutta South','INC',367896,'Biplab Das Gupta','CPM',274233,'Won',5,None,P1,None,'Secondary count table; original ECI PDF and denominator not inspected.'),
(1996,'Calcutta South','INC',438252,'Bharati Mukherjee','CPM',334991,'Won',5,None,P1,None,'Secondary count table; original ECI PDF and denominator not inspected.'),
(1998,'Calcutta South','WBTC',503551,'Prasanta Sur','CPM',279470,'Won',6,None,P2,None,'Preserves WBTC abbreviation in the historical ECI return.'),
(1999,'Calcutta South','AITC',469103,'Subhankar Chakraborty','CPM',255095,'Won',5,None,P2,None,'Secondary count table; primary return remains a gap.'),
(2004,'Calcutta South','AITC',393561,'Rabin Deb','CPM',295132,'Won',7,None,P2,None,'Contemporaneous secondary return; conflicting published shares omitted.'),
(2009,'Kolkata Dakshin','AITC',576045,'Rabin Deb','CPM',356474,'Won',8,None,P2,.5719,'ECI share; votes polled 1007225. Later constituency boundaries differ.'),
(2011,'Bhabanipur (Bhowanipore)','AITC',73635,'Nandini Mukherjee','CPM',19422,'Won',37,'2011-09-25',P3,None,'By-election; result September 28. Poll date shown.'),
(2016,'Bhabanipur','AITC',65520,'Deepa Dasmunshi','INC',40219,'Won',36,None,P3,None,'Secondary result; primary Form20 located but not readable.'),
(2021,'Nandigram','AITC',108808,'Suvendu Adhikari','BJP',110764,'Lost',35,None,P4,None,'General election; no share until denominator reconciled. Petition status separately recorded.'),
(2021,'Bhabanipur','AITC',85263,'Priyanka Tibrewal','BJP',26428,'Won',9,'2021-09-30',P4,.719,'By-election; result October 3. Reported share rounded to one decimal percent.'),
(2026,'Bhabanipur','AITC',58812,'Suvendu Adhikari','BJP',73917,'Lost',10,None,P5,.4219,'All 20 rounds; result page May 5. ECI-derived margin -15105; court admission has not annulled this result.'),
]
for n,(year,seat,party,votes,opp,oparty,ovotes,result,sid,day,phase,share,note) in enumerate(elections,1):
    row={'Year':year,'Constituency':seat,'Result':result,'Candidate votes':votes,'Election date':day,
        'House / route':'Lok Sabha / direct' if n<=8 else 'Assembly / direct','Party':party,
        'Principal opponent':opp,'Opponent party':oparty,'Opponent votes':ovotes,'Vote share':share,
        'Signed vote margin':None,'Finding':note,'Candidate status':'Personal contestant','Vote unit':'Elector ballots'}
    checked={k:[sid] for k in ['Result','Candidate votes','Opponent votes','Principal opponent','Party']}
    if day: checked['Election date']=[sid]
    if share is not None: checked['Vote share']=[sid]
    add('Elections',f'EL{n:02d}',row,[sid],phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,
        note='Shares are source-specific; differences in boundaries and ballot definitions limit comparisons. Margin is calculated, not an independent source claim.')

offices=[
('Congress organiser','1970s–1997','Women’s and youth-party work preceded and accompanied Parliament; exact early Mahila Congress dates differ across profiles.',[1],None,None,P1,'Party roles'),
('Lok Sabha MP, Jadavpur','1984–1989','First parliamentary term ended with personal defeat in the 1989 election.',[1,3,4],None,None,P1,'Direct election'),
('Lok Sabha MP, Calcutta South: 1991 term','1991–1996','Returned to Parliament from Calcutta South.',[1,5],None,None,P1,'Direct election'),
('Minister of State, Human Resource Development','1991–1993; precise dates to verify','PIB confirms the 1991 appointment; Indian Express records junior HRD and youth/sports service ending in 1993.',[1,54],None,None,P1,'Union appointment'),
('Lok Sabha MP, Calcutta South: 1996 term','1996–1998','Elected as Congress candidate; party split followed during this parliamentary period.',[1,5,46],None,None,P1,'Direct election'),
('Trinamool founder and leader','Public launch January 1998; later identity contested','Built a separate party after Congress exit; September 2026 institutional identity is provisional and disputed.',[45,46,12],None,None,P2,'Party founding and leadership'),
('Lok Sabha MP, Calcutta South: 1998 term','1998–1999','Historical ECI return labels her party WBTC.',[1,6],None,None,P2,'Direct election'),
('Lok Sabha MP, Calcutta South: 1999 term','1999–2004','Returned as AITC candidate.',[1,5],None,None,P2,'Direct election'),
('Union Minister of Railways: first term','13 October 1999–16 March 2001','PIB records the dates of this non-consecutive ministerial tenure.',[1],'1999-10-13','2001-03-16',P2,'Union Cabinet appointment'),
('Union Cabinet minister without portfolio','8 September 2003–8 January 2004: provisional','Dates and no-portfolio designation appear in cached CMO history; accessible appointment orders were not found.',[2],None,None,P2,'Union Cabinet appointment'),
('Union Minister of Coal and Mines','2004; precise boundaries to verify','PIB confirms she held Coal and Mines. Cached CMO profile places tenure from 9 January to May 2004.',[1,2],None,None,P2,'Union Cabinet appointment'),
('Lok Sabha MP, Calcutta South: 2004 term','2004–2009','Retained constituency in the 2004 general election.',[1,7],None,None,P2,'Direct election'),
('Lok Sabha MP, Kolkata Dakshin: 2009 term','2009–2011 transition to state office','Seventh Lok Sabha victory; subsequently became Chief Minister.',[1,8,32],None,None,P2,'Direct election'),
('Union Minister of Railways: second term','Charge taken 26 May 2009; until 2011 transition','Second Railways period; commencement date refers to taking charge, not oath.',[1,32],'2009-05-26',None,P2,'Union Cabinet appointment'),
('Chief Minister of West Bengal: first government','20 May 2011–2016 government transition','First woman to lead West Bengal government; initially entered office before winning the Bhabanipur bypoll.',[32,37,33],'2011-05-20',None,P3,'Governor appointment; legislative majority'),
('Chief Minister of West Bengal: second government','27 May 2016–2021 government transition','Second oath on 27 May 2016; third followed in May 2021.',[33,34],'2016-05-27',None,P3,'Governor appointment; legislative majority'),
('Chief Minister of West Bengal: third government','5 May 2021–May 2026','Third government ended following defeat; Adhikari took oath on 9 May 2026. Exact cessation instrument remains uncollected.',[34,11],'2021-05-05',None,P4,'Governor appointment; legislative majority'),
('MLA, Bhabanipur: first period','September 2011–2021 elections','Won 2011 bypoll and 2016 general election; contested Nandigram instead in 2021.',[37,36,35],None,None,P3,'Direct election'),
('MLA, Bhabanipur: second period','October 2021–2026 elections','Returned in the 2021 bypoll and lost the seat in 2026.',[9,10],None,None,P4,'Direct election'),
('Leader of Mamata’s TMC faction','September 2026 interim arrangement','Press reports provisional Mamata All India Trinamool Congress name and Football Player symbol pending substantive determination; September 28 reporting says the interim electoral arrangement was not disturbed.',[13,56],None,None,P5,'Contested party leadership / interim electoral arrangement'),
]
for n,(title,period,finding,ids,start,end,phase,route) in enumerate(offices,1):
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':title,'Period':period,'Finding':finding,
        'Start date':start,'End date':end,'Selection route':route},ids,phase=phase,
        context=f'E{phases.index(phase)+1}02',status='Not reviewed' if n in (10,11) else 'Supported',
        note='Compound chronology includes cached-only detail; retained provisionally rather than marked supported.' if n in (10,11) else 'Years without exact dates denote period-level chronology, not verified daily tenure boundaries.')

def policy(n,title,period,domain,finding,role,stage,ids,phase,limit,ctx=''):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':title,'Finding':finding,'Stage':stage,
        'Period':period,'Policy domain':domain,'Documented role':role,'Attribution / outcome limits':limit},ids,
        'Analysis',phase,ctx or f'E{phases.index(phase)+1}04',note=limit)

policy(1,'Singur land opposition and restitution','2006–2016','Land / industry','Opposition to acquisition formed a central movement; Supreme Court later quashed the acquisition and ordered land restoration.','Movement leader, then head of state government.','Movement followed by 2016 judicial remedy',[15,16],P3,'Judgment concerns the earlier acquisition; neither land return nor a lost factory proves an aggregate employment effect.')
policy(2,'Dankuni freight corridor commencement','2010','Rail infrastructure','Railways announced work on an initial 25.41-km line and sanction of Rs190.46 crore.','Railway Minister inaugurating work and sanctioning supplementary provision.','Commencement and sanction',[48],P2,'Do not credit completion of the full corridor or subsequent freight outcomes to this announcement.')
policy(3,'Gorkhaland Territorial Administration','2011','Regional autonomy','Tripartite agreement established a framework for territorial administration in the hills.','State-government signatory alongside Union government and GJM.','Agreement signed 18 July 2011',[29],P3,'Administrative autonomy within West Bengal; enduring conflict resolution is not demonstrated.','E309')
policy(4,'Teesta sharing negotiations','2011','Federalism / international rivers','Contemporaneous reporting links her objections and withdrawal from the delegation to postponement of the proposed pact.','State leader objecting to draft sharing arrangements.','Agreement not signed during September 2011 visit',[31],P3,'Historical episode only; no claim about current treaty status or optimum water allocation.','E305')
policy(5,'Kanyashree design','From 2013','Girls’ education / marriage','Conditional support links adolescent girls’ education with remaining unmarried; the IGC study examines programme reach and outcomes.','Chief Minister of the adopting government; delivery through state institutions.','Implemented programme evaluated in selected districts',[17],P3,'Eligibility and receipt differ. Later 2026 coverage or payment rates are not inferred from this evaluation.','G07')
policy(6,'Kanyashree independent assessment','Study published 2020','Programme evaluation','Dutta and Sen report reductions in underage marriage and dropout, with continuing costs and social barriers.','Government programme subject to external evaluation.','Nonrandomised study of 1021 households in three selected districts',[17],P3,'Matching and difference-in-differences depend on assumptions; findings are not an all-state 2026 impact estimate.','G09')
policy(7,'Sabooj Sathi bicycles','From 2015','Education / mobility','Bicycles for classes IX–XII in eligible government-sector schools aim to reduce dropout and ease school access.','Government initiative; district account credits CM with name and logo.','Programme design and administrative delivery described',[49],P3,'Target totals are not audited unique deliveries; causal attendance and safety effects require evaluation.')
policy(8,'Swasthya Sathi','2016–2020 expansion','Health','Report describes cashless secondary and tertiary care up to Rs5 lakh per family per year, expanded in December 2020 subject to exclusions.','Head of adopting and expanding state government.','Operational scheme; January 2021 report inspected',[39],P3,'Coverage ceiling is not reimbursement received; financial protection, hospital access and quality require independent evidence.')
policy(9,'Duare Sarkar','From December 2020','Service delivery','Local camps and a digital management system support applications and access to multiple schemes.','State-government outreach initiative under her leadership.','Camps operational; NIC implementation account',[28],P3,'Visits, registrations, approved benefits and unique people are different measures.')
policy(10,'Lakshmir Bhandar initial design','2021–22 Budget','Women / transfers','Budget announced Rs500 monthly for general-category women and Rs1000 for SC/ST beneficiaries.','Head of government introducing the programme; budget and delivery are institutional.','Budget announcement',[42],P4,'Historical introductory rates, not current entitlements.','G07')
policy(11,'Lakshmir Bhandar expansion','2024–25 Budget','Women / transfers','Budget increased monthly rates to Rs1000 general and Rs1200 SC/ST.','Government policy during third term.','Budgeted rate change',[43],P4,'Rates must retain their budget date; no unsupported claim about subsequent 2026 rates.','G07')
policy(12,'Lakshmir Bhandar fiscal scale','2025–26 Budget','Welfare / public finance','PRS reports provision above Rs26000 crore, around one-tenth of revenue receipts.','Government budget presented by Finance Minister Chandrima Bhattacharya.','Budget provision',[18],P4,'Allocation is not audited expenditure; recipients’ control over money and opportunity cost need separate study.')
policy(13,'Karmasree work proposal','2024–25 Budget','Employment / federal finance','Budget proposed 50 days of work, amid a period when the Union had stopped MGNREGA releases citing noncompliance.','State government proposer; Union’s reason for withholding is attributed to its ministry.','Proposal and dated Union account of funding stoppage',[43,40],P4,'Not proof that every eligible household received work or that all disputed irregularities were established.','E409')
policy(14,'Capital-outlay execution','2015–16 to 2021–22','Investment / administration','PRS calculated average capital-outlay underspending of 33%, compared with 19% across states.','State-government execution responsibility, shared with departments and implementing bodies.','Retrospective actual-versus-budget comparison',[43],P3,'Does not establish causes, project quality, private investment levels or personal causal responsibility.')
policy(15,'Fiscal position near end of tenure','2024–25 actual; 2025–26 RE','Public finance','Latest PRS analysis reports fiscal deficit 3.4% of GSDP in both 2024–25 actuals and 2025–26 RE; 2025–26 liabilities 38.3% of GSDP.','Government led during these fiscal years; estimates later reported by successor.','Actual and revised-estimate figures clearly separated',[19],P4,'Do not compare unreconciled data vintages; structural liabilities cannot be wholly assigned to one leader.')
policy(16,'Transfer-policy legacy under successor','June 2026 Budget','Welfare continuity','PRS records successor government’s Annapurna Bhandar replacing Lakshmir Bhandar.','Predecessor associated with earlier scheme, not author of successor proposal.','Successor budget announcement',[19],P5,'Continuity of a transfer instrument does not mean unchanged eligibility, financing or political ownership.')
add('Policy & Governance','PG17',{'Initiative / decision':'Khadya Sathi: source gap','Finding':'Indexed programme note dates subsidised-grain expansion beyond NFSA to January 2016; canonical PDF is account-gated.','Stage':'Provisional historical design; original document not inspected','Period':'2016','Policy domain':'Food security','Documented role':'Government programme associated with Banerjee; exact design pending primary retrieval'},[50],phase=P3,context='E308',status='Not reviewed',note='Do not use indexed coverage totals as verified outcomes.')

ideas=[
('Regional party construction','A separate organisation converted anti-Left mobilisation into a durable electoral vehicle; 2026 factional conflict raises a distinct question about institutional survival beyond government.',[15,45,12],P5,'E507'),
('Protest as political method','Street mobilisation, bodily endurance and confrontation figure prominently in biographies. These describe methods and public presentation, not proof that every protest achieved its stated goal.',[15,46],P2,'E206'),
('Didi and political kinship','Chaudhury analyses elder-sister imagery as a way to make female authority familiar and accessible while retaining a commanding leadership role.',[14],P3,'G08'),
('Ascetic public persona','Simple dress and restrained personal presentation are central to the scholarly account. An austerity image is not an audit of assets or institutional integrity.',[14],P3,'G05'),
('Economic bargaining with allies','The 2012 withdrawal announcement linked coalition support to objections over retail FDI and household fuel costs.',[30],P3,'E304'),
('Bengali regional framing','The 2024 campaign report describes welfare appeals and the portrayal of BJP as anti-Bengali. Reported messaging should be separated from measured persuasion.',[51],P4,'E406'),
('National alliance, state competition','TMC belonged to the national INDIA opposition grouping in 2024 while contesting all Bengal Lok Sabha seats independently.',[51],P4,'E401'),
('Personalised organisation','Scholarship describes centralised leadership; Gupta’s later criticism links welfare delivery to continued dependence on a cadre network. The accounts are interpretive.',[14,46],P3,'E307'),
('Family and succession','Abhishek Banerjee’s rise as all-India general secretary placed a nephew in a central organisational role. Reporting records both old-guard resentment and a supportive generational-renewal account.',[46],P4,'G03'),
('Courts as political institutions','Election petitions and the party-symbol challenge show legal remedies operating alongside electoral mobilisation; filing a claim does not establish its merits.',[22,38,12],P5,'E502'),
('Social coalition through movements','Gupta connects peasant struggles and intellectual support with the broadening of her coalition. This interpretation does not quantify support by caste, class or religion.',[15],P2,'E208'),
('Cultural production','Official biography records Bengali and English writing; scholarly work examines the use of cultural and religious symbols in political self-presentation.',[1,14],P3,'G08'),
('Changing coalition partners','Her party participated in BJP-led NDA and later Congress-led UPA-II, withdrawing from both at different points. Coalition bargaining and state-level rivalry changed over time; present opposition to BJP should not be projected across her whole career.',[54],P2,'E201'),
]
for n,(topic,finding,ids,phase,ctx) in enumerate(ideas,1):
    add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding},ids,'Analysis',phase,ctx)

controversies=[
('School recruitment cancellation','Supreme Court maintained invalidation of a compromised recruitment process and dismissed review in August 2025.','The state and affected parties sought review; the Court held earlier consideration sufficient.','Review dismissed 5 August 2025; later implementation not audited.',[20],P4,'Process-level judicial findings do not amount to Banerjee’s personal criminal conviction.'),
('Cabinet decision on supernumerary posts','Supreme Court set aside the particular direction to investigate the 2022 Cabinet decision.','State successfully challenged this limited investigative direction.','Limited relief on 8 April 2025; other investigations expressly unaffected.',[21],P4,'Separate from recruitment cancellation; no blanket exoneration.'),
('RG Kar institutional safety','Supreme Court criticised state preparedness for vandalism and identified systemic risks to medical professionals after the doctor’s rape and murder.','Banerjee later demanded capital punishment when Roy received whole-life imprisonment.','SC safety order 20 August 2024; Roy sentenced 20 January 2025.',[23,24],P4,'Separate state accountability, offender conviction and safety reform. Later appeals or wider investigations require updated records.'),
('Sandeshkhali investigation','Allegations involving land grabbing and sexual assault prompted court-directed CBI investigation; state challenge failed.','State counsel argued the transfer was too broad and invoked federal autonomy.','Supreme Court rejected challenge on 8 July 2024.',[25],P4,'Allegations remain attributed; probe authorisation is not a conviction or proof of personal complicity.'),
('Saradha and related deposit schemes','Supreme Court transferred specified investigations to CBI, citing interstate reach, untraced money and public confidence.','State counsel questioned CBI credibility; Court rejected that objection while recognising work by state police.','Transfer ordered 9 May 2014; no final complicity finding in that order.',[26],P3,'Different defendants and proceedings cannot be collapsed into one case against the CM.'),
('Narada arrests and protest','May 2021 order records CBI concerns about pressure around arrests and Banerjee’s presence at its office.','State advocate did not deny her presence; extent and legal consequences of interference remained contested.','Initial bail stay 17 May; four accused received interim bail 28 May 2021.',[27,53],P4,'Interim findings and bail do not establish final guilt or acquittal; current merits status not verified.'),
('Post-election violence in 2021','High Court ordered CBI and SIT investigations into categories of post-poll violence and scrutinised police response.','At her third oath Banerjee appealed for peace. This is a contemporaneous response, not a later reply to the HC judgment.','Investigation directions reported 19 August 2021.',[41,34],P4,'Responsibility in individual incidents requires case-specific findings.'),
('Park Street remarks','Reporting records sharp criticism after she characterised the rape allegation as fabricated.','She said the remarks were misinterpreted and wanted guilty persons punished.','Public-response controversy documented February 2012.',[47],P3,'Do not endorse her characterisation, repeat unsupported medical claims or equate this episode with a final court finding.'),
('Nandigram result challenge','She challenged the 2021 defeat; March 2026 reporting described the petition as still pending.','Her party and public remarks alleged electoral wrongdoing; the result remains the recorded result in this study.','Pending as reported 18 March 2026; later disposition not established.',[38,9,35],P4,'Pending litigation is not proof that the election was rigged.'),
('Bhabanipur result challenge','High Court admitted her 2026 petition and ordered preservation of election material.','Her challenge seeks judicial scrutiny of the declared result.','Admission and preservation order 23 June 2026.',[22,10],P5,'No annulment or finding of fraud in the inspected order.'),
('TMC name and symbol dispute','Reports describe competing claims and interim freezing of the original name and symbol in September 2026.','Banerjee challenged the timing and arrangement; rival representatives defended the interim orders.','September 28 reports: four weeks for pleadings, then three months for ECI decision; interim electoral arrangement retained.',[12,13,55,56],P5,'Signed ECI and latest SC orders uncollected. Reported timetable does not decide faction entitlement. No fixed calendar deadline inferred; interim freeze is not dissolution.'),
]
for n,(matter,finding,response,status,ids,phase,note) in enumerate(controversies,1):
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Response':response,'Procedural status':status},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',note=note,priority='High')

legacy=[
('Breaking Left dominance','Her 2011 accession ended a long governing order and established the state’s first woman Chief Minister. This institutional transition is more secure than a single-cause account of why voters changed sides.',[32],'Historical event and workbook synthesis','E301'),
('Broadening an opposition coalition','Gupta emphasises how land struggles changed the social reach of her politics. This locates her success within collective movements rather than treating it as purely personal charisma.',[15],'Monobina Gupta','E208'),
('Women’s education and welfare','Kanyashree offers evaluated evidence of beneficial outcomes in selected districts; women’s transfers widened policy attention. Generalising gains to every woman or all years would exceed the evidence.',[17,18],'Evaluation and workbook synthesis','G09'),
('Leadership and institutional limits','Chaudhury’s account of personalised authority and Gupta’s criticism of cadre continuity suggest a tension between a change-making leader and the institutions developed under her.',[14,46],'Scholarly and biographical interpretations','E307'),
('Fiscal and investment trade-offs','Transfer expansion coexisted with capital-outlay execution gaps and substantial liabilities. These provide questions for evaluation, not a complete balance sheet of her government’s welfare or growth effects.',[18,19,43],'PRS evidence and workbook synthesis','E404'),
('Institutional accountability','Recruitment and hospital-safety judgments provide serious findings about governance systems. Their specific legal scope is stronger evidence than claims that every scandal proves personal criminal responsibility.',[20,21,23],'Judicial record and workbook synthesis','E402'),
('Democratic reversal','The 2026 loss ended her government; the delayed Falta result brings the combined election tally to BJP208 and TMC80. This is an election tally, not the Assembly’s live composition.',[11,52],'Election records and derived count','E503'),
('Legacy beyond office','The successor’s replacement transfer scheme indicates continued political salience of household support. Institutional durability of Banerjee’s party remains unsettled during the September dispute.',[19,56],'Provisional workbook synthesis','E507'),
('Open causal questions','This study does not establish the separate effects of welfare, corruption allegations, identity appeals or electoral administration on the 2026 defeat. A defensible explanation needs voter and constituency-level analysis.',[10,12,18],'Research limitation','E510'),
]
for n,(theme,assessment,ids,assessor,ctx) in enumerate(legacy,1):
    add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor':assessor,
        'Assessment status':'Provisional; political and legal developments continue'},ids,'Analysis',context=ctx)

exec(Path(__file__).with_name('author_context.py').read_text())

gaprows=[
('High','September 2026 party orders','September 28 timetable supported by reporting; signed ECI freeze/allotment and latest Supreme Court orders not obtained. Final entitlement not established.','Retrieve signed September 28 SC order and ECI dispute docket; check pleading completion and subsequent decision.',['OV02','OF20','CV11','E510']),
('High','Historical primary election returns','1991, 1996, 1999, 2004, 2011 and 2016 counts use secondary reports; several original PDFs failed.','Seek signed results and Form20 from ECI, CEO archives or parliamentary statistical collections.',['EL03','EL04','EL06','EL07','EL09','EL10']),
('Normal','Unresolved vote shares','Eight personal contests have no inspected, reconciled denominator; Nandigram publishers disagree.','Inspect complete Form20; state whether share includes NOTA, postal votes and rejected ballots.',['EL03','EL04','EL05','EL06','EL07','EL09','EL10','EL11']),
('Normal','Short ministerial tenure boundaries','HRD service in 1991–93 is supported, but exact daily boundaries and some no-portfolio and Coal/Mines dates remain unverified; exact CM cessation instrument also uncollected.','Retrieve Gazette appointment/allocation notifications and parliamentary Who’s Who.',['OF04','OF10','OF11','OF17']),
('High','Latest legal outcomes','Several matters have dated procedural records but no inspected later merits disposal or final implementation audit.','Refresh each separate court docket; do not infer guilt, exoneration or indefinite pendency.',['CV01','CV03','CV04','CV05','CV06','CV07','CV09','CV10']),
('Normal','Khadya Sathi primary design','Indexed programme note is access-gated; launch/design retained provisionally.','Use Food and Supplies annual reports and original RKSY orders.',['PG17']),
('High','Independent welfare and development effects','Kanyashree has a bounded external evaluation; broad health, transfer, investment and employment effects are not causally established.','Compare independent household and enterprise data with actual expenditure and credible comparison groups.',['PG06','PG08','PG12','PG14','LA05']),
('Normal','Gendered security and promotion mechanisms','Political violence and gendered presentation are documented; gender-specific causes of threats and advancement are not isolated.','Seek contemporary incident records and matched studies of women and men in comparable party roles.',['G01','G06','G09']),
('Normal','Election-defeat explanation','This workbook records 2026 results and disputes without estimating reasons for vote changes.','Analyse constituency returns, credible voter surveys, demographic data and verified electoral-roll decisions.',['LA09','E503','E510']),
('Normal','Earlier international and economic views','Early career positions on international affairs and liberalisation are thinly evidenced in the collected sources.','Seek contemporaneous parliamentary debates, party documents and interviews.',['E104','E105','E205']),
]
for n,(priority,topic,gap,next_action,records) in enumerate(gaprows,1):
    gaps.append({'id':f'GAP{n:02d}','priority':priority,'topic':topic,'gap':gap,'next_action':next_action,'record_ids':records,'status':'Open'})

data={'schema_version':1,'subject':'Mamata Banerjee','as_of':ASOF,
    'guidance':'Read dated court status, policy stages and historical election definitions together with the findings. Gender milestones and leadership imagery do not by themselves establish causal effects.',
    'tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'coverage':coverage,'phases':phases,'gaps':gaps}
root=Path(__file__).parent
root.joinpath('research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
root.joinpath('retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(f'Authored {sum(len(t["rows"]) for t in tables.values())} records, {len(claims)} field claims, {len(sources)} sources.')
