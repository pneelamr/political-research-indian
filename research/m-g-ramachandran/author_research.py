"""Reproducible M. G. Ramachandran research with field-specific evidence review."""
import hashlib, json
from pathlib import Path
from author_sources import ASOF, sources, retrievals
P1='P1 | Formation, cinema and DMK (1917–1966)'
P2='P2 | Legislator and party founder (1967–1976)'
P3='P3 | First government (1977–February 1980)'
P4='P4 | Return and welfare expansion (June 1980–1984)'
P5='P5 | Final government (1985–1987)'
phases=[P1,P2,P3,P4,P5]
tables,claims,evidence,gaps={},[],[],[]
R={r['source_id']:r for r in retrievals if r['access_status']=='Passage inspected'}
def table(name,lead,dates=()): tables[name]={'lead_columns':lead,'date_columns':list(dates),'rows':[]}
def add(name,rid,fields,nums,typ='Recorded fact',phase=None,context='',checked=None,note='',status='Supported',priority='Normal'):
    ids=[f'S{n:03d}' if isinstance(n,int) else n for n in nums]
    idcol={'Overview':'Overview ID','Context & Constraints':'Context ID','Career Timeline':'Timeline ID','Elections':'Election ID','Offices & Party':'Position ID','Controversies':'Matter ID','Legacy & Assessments':'Assessment ID'}.get(name,'Record ID')
    row={idcol:rid,**fields,'Claim type':typ,'Source IDs':'; '.join(ids)}
    if phase: row['Career phase']=phase
    if context: row['Context IDs']=context
    if note: row['Research note']=note
    if typ!='Method / scope':
        cited=[s for s in sources if s['Source ID'] in ids]
        row['Corroboration']='Unresolved' if status!='Supported' else ('Primary record / attributed statement' if any(s['Primary / secondary']=='Primary' for s in cited) else ('Single secondary source' if len(cited)==1 else 'Multiple sources; inspect shared origins'))
    tables[name]['rows'].append(row)
    if typ=='Method / scope': return row
    if checked is None:
        checked={k:ids for k,v in fields.items() if k in ('Finding / value','Finding','Description','Assessment','Response','Procedural status') and v is not None}
    for field,support in checked.items():
        support=[f'S{s:03d}' if isinstance(s,int) else s for s in support]
        cid=f'C-{rid}-{sum(c["record_id"]==rid for c in claims)+1:02d}'
        evs=[]
        if status=='Supported':
            for sid in support:
                r=R[sid]; eid=f'EV-{len(evidence)+1:04d}';evs.append(eid)
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':r['id'],'locator':r['locator'],'passage_paraphrase':r['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex: inspected-passage review','reviewed_at':ASOF,'note':'Evidence supports the registered field jointly. Interpretations remain bounded; self-statements remain attributed. Shared origins are not independent corroboration.'})
        val=row[field]
        claims.append({'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':val,'fingerprint':hashlib.sha256(json.dumps(val,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':typ,'status':status,'priority':priority,'candidate_source_ids':support,'evidence_ids':evs,'contradictions':[],'review_note':note or ('Bounded interpretation of the identified evidence.' if typ=='Analysis' else 'Registered field checked against the specified passages; qualifications apply.')})
    return row

table('Overview',['Overview ID','Topic','Finding / value'])
table('Context & Constraints',['Context ID','Career phase','Coverage item','Finding'])
table('Career Timeline',['Timeline ID','Period','Event','Description'],['Start date'])
table('Elections',['Election ID','Year','House / route','Constituency','Result','Candidate votes'],['Election date'])
table('Offices & Party',['Position ID','Position / institution','Period','Finding'],['Start date','End date'])
table('Policy & Governance',['Record ID','Initiative / decision','Finding','Stage'])
table('Ideas & Political Method',['Record ID','Topic','Finding'])
table('Controversies',['Matter ID','Matter','Finding','Procedural status'])
table('Legacy & Assessments',['Assessment ID','Theme','Assessment'])
def ov(n,topic,finding,ids,typ='Recorded fact',**kw):
    return add('Overview',f'OV{n:02d}',{'Topic':topic,'Finding / value':finding},ids,typ,**kw)
ov(1,'Identity','M. G. Ramachandran (MGR), commonly expanded as Marudur Gopalan Ramachandran; actor, party founder and Tamil Nadu Chief Minister. Born 17 January 1917 in British Ceylon; died 24 December 1987.',[1,24])
ov(2,'Formation','Family hardship, limited formal schooling and theatre preceded a Tamil cinema career. Film success and DMK association provided intersecting routes into politics.',[1,23],'Analysis',context='E106')
ov(3,'Party trajectory','Congress association preceded joining DMK in 1953. After the 1972 split, founded Anna Dravida Munnetra Kazhagam, subsequently known as AIADMK.',[1,2,23],'Analysis')
ov(4,'Principal offices','Legislative Council entry in 1962; five Assembly victories; DMK treasurer and founder-leader of ADMK/AIADMK; Chief Minister across three governments between 1977 and 1987.',[1,2,6,10],'Analysis')
ov(5,'Chief-ministerial chronology','First sworn 30 June 1977; government dismissed in February 1980. Returned on 9 June 1980; next ministry sworn 10 February 1985 after the December 1984 election. Died in office on 24 December 1987.',[6,10],'Analysis',priority='High')
ov(6,'Personal elections','Won St. Thomas Mount in 1967 and 1971, Aruppukkottai in 1977, Madurai West in 1980 and Andipatti in 1984. Party defeats in parliamentary elections are separate from these personal Assembly results.',[17,18,19,20,21,10],'Analysis',priority='High')
ov(7,'Political geography','Cinema and fan networks supplied statewide reach; his Assembly seats moved from the Madras area to southern Tamil Nadu. Vote shares across these different seats are not a continuous constituency trend.',[5,17,18,19,20,21],'Analysis')
ov(8,'Signature welfare contribution','The 1982 nutritious-meal expansion is a central documented initiative, with subsequent urban and age-group extensions. School feeding had earlier roots; later programme changes belong to later governments.',[3,4,32],'Analysis')
ov(9,'Governance beyond meals','University creation, backward-class reservation changes, liquor wholesale administration and abolition of the Legislative Council broaden the record. Enactment, implementation and independent outcomes are kept separate.',[7,11,12,13,15,25],'Analysis')
ov(10,'Political method','Scholarship connects his protective screen persona, fan associations and targeted welfare with a paternalist form of populism. Supporters also retained capacity to demand concessions from leaders.',[5,23],'Analysis')
ov(11,'Major controversies','The research examines the 1979–80 quota reversal, press privilege proceedings, Council abolition, 1987 Vanniyar agitation and disputed accounts of assistance associated with the LTTE.',[7,8,9,15,16],'Analysis')
ov(12,'Gender synthesis','Women were a significant constituency in scholarly accounts; meals and women’s higher education offered substantive policy routes. These do not establish equal access to party authority or a measured personal empowerment effect.',[4,5,13],'Analysis',context='G07; G09')
ov(13,'Competing legacy','Durable party-building and institutionalised welfare coexist with concerns about concentrated leadership, coercive accountability practices and unresolved distributional effects. Assessments require more than either celebratory biography or a single adverse episode.',[3,5,8,16],'Analysis')
ov(14,'Posthumous recognition','Awarded Bharat Ratna posthumously in 1988. The medical university’s 1987 legislation, July 1988 functioning and 1991 naming are distinct milestones.',[11,24],'Analysis')
ov(15,'Scope and evidence limits','Research snapshot: 25 October 2026. Strong records include legislation, court decisions and programme histories. Several election tables are labelled secondary fallbacks; original returns, inquiry exhibits and independent policy evaluations remain open.',[6,7,8,17,18,19,20,21],'Analysis')

timeline=[
('17 January 1917','Birth','Born in British Ceylon; institutional biographies identify Kandy. Exact locality variants have not been reconciled.',[1],P1,None,'1917-01-17'),
('Childhood','Schooling and theatre','Family hardship and relocation to Kumbakonam preceded limited schooling and entry into theatre.',[1],P1,'E108',None),
('1936','Film debut','Sathi Leelavathi marked his film debut.',[2,23],P1,'E106',None),
('1947–1950','Film breakthrough','Rajakumari and Manthiri Kumari were major stages in his emergence as a leading actor; Karunanidhi wrote the latter.',[23],P1,'E106',None),
('1953','Joins DMK','Joined the Dravida Munnetra Kazhagam, connecting cinema work with party mobilisation.',[1,23],P1,'E107',None),
('1962','Legislative Council entry','Entered the Madras Legislative Council. Exact election or nomination route and end date remain unverified.',[1],P1,'E102',None),
('1967','Shooting and first Assembly win','Survived a shooting by actor M.R. Radha; subsequently won St. Thomas Mount. No numerical causal effect of sympathy on the result is inferred.',[23,17],P2,'E206',None),
('After Annadurai’s death','DMK treasurership','Became party treasurer during the period following Annadurai; exact appointment boundary needs an original party record.',[2],P2,'E207',None),
('1971','Re-elected','Won St. Thomas Mount again as a DMK candidate.',[18],P2,'E203',None),
('17 October 1972','New party','Founded ADMK following expulsion and a public dispute with DMK leadership over accountability.',[2,10],P2,'E201','1972-10-17'),
('1973–1974','Early party victories','The university history records party victories in Dindigul’s 1973 parliamentary by-election and a 1974 Coimbatore Assembly by-election. These were not personal MGR contests.',[10],P2,'E203',None),
('1975–1977','Emergency alignment','The university history records AIADMK support for the Emergency and closer ties with Congress. The DMK state government was dismissed in 1976.',[10,6],P2,'E202',None),
('1977','Assembly victory','Won Aruppukkottai; AIADMK came to power in the state.',[19,10],P3,'E303',None),
('30 June 1977','First ministry','Sworn in as Chief Minister, with portfolios including administration and police.',[10],P3,'E302','1977-06-30'),
('1979','Quota restriction','Government imposed a Rs 9,000 annual-income ceiling for backward-class reservation benefits.',[15],P3,'E308',None),
('1979','Union coalition participation','Two AIADMK MPs joined the short-lived Charan Singh ministry; this was party participation, not a Union ministerial appointment for MGR.',[10],P3,'E301',None),
('January–February 1980','Reversal and dismissal','After AIADMK’s parliamentary setback, the income ceiling was withdrawn and BC quota raised. Assembly was dissolved on 17 February; his government was dismissed.',[15,6,10],P3,'E302',None),
('9 June 1980','Return to government','Following victory in the state election, sworn Chief Minister for a second time; personally won Madurai West.',[10,20],P4,'E403','1980-06-09'),
('15 September 1981','Tamil University','Tamil University established at Thanjavur for advanced Tamil research.',[12],P4,'E408','1981-09-15'),
('1 July 1982','Nutritious-meal expansion','Launched the programme at Pappakurichi; urban expansion followed in September.',[3],P4,'E404','1982-07-01'),
('1982','Jayalalithaa enters party','Jayalalithaa’s entry supplied a later leadership pathway associated with MGR; eventual succession was contested.',[2],P4,'G03',None),
('1983','Liquor wholesale administration','TASMAC emerged as the state-owned wholesale channel; the state’s later court account places takeover in July.',[25],P4,'E404',None),
('1984','Women’s university','Mother Teresa Women’s University established under Tamil Nadu Act 15.',[13],P4,'G07',None),
('December 1984','Victory during illness','AIADMK-Congress won the Assembly election despite MGR’s hospitalisation; he won Andipatti.',[10,21],P4,'E406',None),
('10 February 1985','Third ministry','Sworn in again as Chief Minister following the 1984 election.',[6],P5,'E502','1985-02-10'),
('1 November 1986','Legislative Council abolished','Council abolition took effect after the Assembly resolution and subsequent legislative process.',[6,7],P5,'E502','1986-11-01'),
('April 1987','Press privilege and Sri Lankan aid','Assembly imprisoned and released Ananda Vikatan’s editor. Separately, Sri Lankan Tamil assistance later generated conflicting evidence before the Jain Commission.',[6,8,9],P5,'E506; E505',None),
('September 1987','Caste mobilisation and policing','Vanniyar reservation agitation led to deaths in police firing and clashes; no immediate settlement followed.',[16],P5,'E508',None),
('24 December 1987','Death in office','MGR died; succession conflict between Janaki and Jayalalithaa followed.',[1,2,6],P5,'E507','1987-12-24'),
('1988','National honour','Bharat Ratna awarded posthumously; notification dated 26 January, Gazette published in March.',[24],None,None,'1988-01-26')]
for n,(period,event,desc,ids,phase,ctx,date) in enumerate(timeline,1):
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':date,'Date precision':'Day' if date else 'Year or period'},ids,'Analysis',phase,ctx or '')

add('Elections','EL01',{'Year':1962,'House / route':'Madras Legislative Council / route unresolved','Constituency':None,'Result':'Membership recorded','Candidate votes':None,'Opponent votes':None,'Vote share':None,'Signed vote margin':None,'Finding':'Institutional biography records Council entry in 1962; election versus nomination, constituency and exact term boundaries require the original record.','Candidate status':'Indirect route not established; excluded from direct-election totals'},[1],phase=P1,context='E103')
direct=[
    (1967,'St. Thomas Mount',54106,'T.L. Raghupathy',26432,'INC',81151,17,'DMK','1967-02-21',P2),
    (1971,'St. Thomas Mount',65405,'T.L. Raghupathy',40773,'NCO',107028,18,'DMK',None,P2),
    (1977,'Aruppukkottai',43065,'M. Muthuvel Servai',13687,'JNP',76582,19,'AIADMK',None,P3),
    (1980,'Madurai West',57019,'Pon. Muthuramalingam',35953,'DMK',95646,20,'AIADMK',None,P4),
    (1984,'Andipatti',60510,'Thangaraj alias Vallarasu',28026,'DMK',None,21,'AIADMK',None,P4)]
for n,(year,seat,votes,opponent,opp,opparty,total,sid,party,date,phase) in enumerate(direct,2):
    note=('ECI table inspected through identified reproduction; original download unavailable.' if year==1967 else 'Secondary historical table; original constituency return remains a priority gap.')
    if year==1984: note+=' Full valid-vote total unverified; share is intentionally blank.'
    if year>=1977: note+=' Source abbreviation ADK is normalized to AIADMK.'
    fields={'Year':year,'House / route':'State Legislative Assembly / direct','Constituency':seat,'Result':'Won','Candidate votes':votes,'Opponent votes':opp,'Vote share':votes/total if total else None,'Signed vote margin':votes-opp,'Party':party,'Principal opponent':opponent,'Opponent party':opparty,'Share denominator':total,'Denominator definition':'Valid candidate votes' if total else 'Not established','Election date':date,'Finding':f'Won {seat} with {votes:,} votes; runner-up {opp:,}; margin {votes-opp:,}.','Seat / comparison note':note,'Candidate status':'Personal contestant'}
    checked={f:[sid] for f in ['Finding','Candidate votes','Opponent votes','Signed vote margin']}
    if total: checked.update({'Share denominator':[sid],'Vote share':[sid]})
    if date: checked['Election date']=[sid]
    add('Elections',f'EL{n:02d}',fields,[sid],phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,priority='High',note=note)

offices=[
('DMK member','1953–1972','Party affiliation preceded direct electoral office; ended with the 1972 split.',[1,2],P1,'Party membership',None,None),
('Madras Legislative Council member','Entry in 1962','Upper House service recorded; exact route and end boundary remain open.',[1],P1,'Legislative office',None,None),
('Assembly member: St. Thomas Mount','1967 and 1971 mandates','Two victories under the DMK label; party affiliation later changed during the second mandate.',[17,18,2],P2,'Direct election',None,None),
('DMK treasurer','After Annadurai; until 1972 split','Organisational role recorded; appointment day and competing summary years require reconciliation.',[2],P2,'Party office',None,None),
('ADMK / AIADMK founder-leader','1972–1987','Founded party on 17 October 1972 and led it to government. Exact formal general-secretary intervals are not equated with continuous founder leadership.',[10,1],P2,'Party leadership','1972-10-17',None),
('Chief Minister: first government','30 June 1977–17 February 1980','First government ended with dismissal and Assembly dissolution; a President’s Rule interval separates the next government.',[6,10],P3,'Executive office','1977-06-30','1980-02-17'),
('Assembly member: Aruppukkottai','1977–1980','Won Aruppukkottai; sixth Assembly dissolved 17 February 1980.',[19,6],P3,'Direct election',None,'1980-02-17'),
('Chief Minister: second government','9 June 1980–February 1985 reappointment','Returned after Assembly victory. The 1984 election and 1985 oath are distinct; Assembly dissolution is not treated as automatic termination of the caretaker ministry.',[10,6],P4,'Executive office','1980-06-09',None),
('Assembly member: Madurai West','1980–1984 mandate','Won Madurai West in 1980 before shifting constituency in the next election.',[20,21],P4,'Direct election',None,None),
('Assembly member: Andipatti','1984 election–24 December 1987','Won the December 1984 contest; death created a vacancy in the eighth Assembly.',[21,6],P5,'Direct election',None,'1987-12-24'),
('Chief Minister: third government','10 February 1985–24 December 1987','Third ministry began on 10 February 1985; death in office ended his tenure.',[6],P5,'Executive office','1985-02-10','1987-12-24'),
('Administration and police portfolios','1977 and 1985 ministries','Ministry lists place general administration, police and corruption-prevention responsibilities with the Chief Minister. Portfolio possession is distinct from proof of personal direction of every police action.',[10,6],P5,'Ministerial portfolio',None,None)]
for n,(position,period,finding,ids,phase,route,start,end) in enumerate(offices,1):
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':position,'Period':period,'Finding':finding,'Office type / route':route,'Start date':start,'End date':end},ids,'Analysis',phase,f'E{phases.index(phase)+1}02')

policies=[
('Nutritious-meal expansion','Rural launch on 1 July 1982 followed by urban extension on 15 September. This expanded an older school-feeding tradition.','Implemented programme',[3,32],P4,'Chief Minister launched expansion','Nutrition and school participation were stated objectives; causal outcome estimate not supplied.'),
('Expanded meal eligibility','Pensioners included from January 1983; students aged 10–15 from September 1984. Pregnancy coverage began in 1995 and belongs to a later government.','Implementation stages',[4],P4,'Government expansion during tenure','Age-group and calendar distinctions prevent crediting every later feature to MGR.'),
('Meal outcomes and workforce','A 2004 assessment reports improved retention, girls’ participation and women’s employment, but warns that data cannot isolate the programme’s enrolment effect and notes insecure worker conditions.','Retrospective evaluation',[4],P4,'Institutional legacy; no sole causal attribution','Later findings are not contemporaneous MGR-era measurements.'),
('Backward-class reservation','1979 income ceiling was withdrawn in 1980; BC quota rose to 50%, with the combined allocation then 68%.','Implemented change; primary orders pending',[15,5],P3,'Government decision and reversal','Political pressure is documented in scholarship; exact GO chronology remains open.'),
('Tamil University','Established at Thanjavur on 15 September 1981 for Tamil research; statutory basis Act 9 of 1982.','Institution established',[12],P4,'Created during government','Institutional existence and stated mission are supported; educational impact not measured.'),
('Women’s higher education','Mother Teresa Women’s University established in 1984 under Act 15 to expand education and employment prospects for women across communities.','Institution established',[13],P4,'Government institution-building','No enrolment-based estimate of MGR’s personal contribution to empowerment collected.'),
('Medical university','Act 37 of 1987 received presidential assent on 24 September; functioning began July 1988, after MGR’s death. Naming after him followed in 1991.','Enacted; later implementation',[11],P5,'Legislation during tenure','Do not describe the institution as operational under MGR.'),
('Liquor wholesale administration','State’s court account places government wholesale takeover in July 1983 through TASMAC; arrack sales stopped on 1 January 1987.','Administrative implementation',[25],P4,'State policy during tenure','Wholesale arrangements and later retail monopoly are different; no blanket claim of continuous total prohibition.'),
('Legislative Council abolition','Assembly passed its resolution on 14 May 1986; judicial challenge to it failed. Abolition took effect on 1 November 1986.','Institutional change implemented',[7,6],P5,'Government-backed resolution and legislation','Court validity ruling does not settle political merit or alleged motive.'),
('Sri Lankan Tamil assistance','Inquiry text records Rs 4 crore in 1987 aid. State described rehabilitation grants; several witnesses described assistance reaching LTTE.','Disputed recipient/character of assistance',[9],P5,'Government grants; personal donation totals not verified','Original inquiry exhibits and independent corroboration remain a high-priority gap.'),
('Vanniyar demands and response','1986–87 reservation mobilisation culminated in deadly September 1987 protests. The later 20% MBC arrangement was introduced under the DMK in 1989.','Unresolved during tenure; later reform',[16],P5,'Political and policing accountability','No inspected inquiry establishes MGR’s individual operational responsibility for each death.'),
('Village-administration reform: lead','A Supreme Court case concerning village-office abolition has been located, but its full reasoning and disposition were not retrieved. No reform outcome is certified here.','Research lead; not reviewed',[30],P4,'Personal role and implementation pending','Obtain the judgment and original 1980 enactment before evaluating this reform.')]
for n,(initiative,finding,stage,ids,phase,role,limit) in enumerate(policies,1):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':initiative,'Finding':finding,'Stage':stage,'Personal role / attribution':role,'Outcome / limitation':limit},ids,'Analysis',phase,f'E{phases.index(phase)+1}04',status='Not reviewed' if n==12 else 'Supported',priority='High' if n in (4,10,11,12) else 'Normal')

ideas=[
('Cinema and political credibility','Protector roles, film dialogue and visual performance helped connect a screen persona with political claims; reception varied and cannot be reduced to deception or uncritical fandom.',[23,5],P2,'E206'),
('Fan clubs as organisation','Fan associations supplied local mobilisation capacity when he established a separate party. Celebrity and organisation worked together.',[5,23],P2,'E207'),
('Annadurai’s inheritance','The new party’s name and public promise to recover Annadurai’s ideals formed a claim to Dravidian legitimacy after the split.',[23,2],P2,'E201'),
('Accountability as opposition language','Demands for asset disclosure and accusations against DMK leadership helped frame the 1972 rupture. Allegations are evidence of political strategy, not proof of each charge.',[2,23],P2,'E202'),
('Paternalist populism','Subramanian interprets AIADMK as promising protection and benefits to weaker groups, while showing that supporters could still press independent demands.',[5],P4,'E407'),
('Tamil and Indian belonging','Scholarship treats MGR’s success as evidence that cultural participation could outweigh exclusion based on ancestry, alongside accommodation with Indian national identity.',[5],P3,'E308'),
('Alliance flexibility','Participation in the Charan Singh coalition and the 1984 Congress alliance show changing national partnerships. Alliances did not erase competition within Tamil Nadu.',[10],P4,'E401'),
('Welfare and institutional power','Meals and university creation are concrete initiatives. The press-privilege ruling and Council abolition separately raise questions about checks on political authority.',[3,13,7,8],P5,'E502')]
for n,(topic,finding,ids,phase,ctx) in enumerate(ideas,1):
    add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding},ids,'Analysis',phase,ctx)

controversies=[
('1972 split and corruption allegations','MGR publicly challenged DMK leadership over financial accountability and was expelled before founding a new party.','Political accusation and organisational split; no judicial determination asserted','Asset-disclosure demands form part of his public challenge; a complete contemporaneous DMK reply has not been collected.',[2,23],P2,'Party conflict'),
('1979–80 reservation reversal','Income-based restriction on BC benefits provoked resistance; government withdrew it and increased quota after the parliamentary setback.','Policy reversal; exact original GO chronology remains open','Withdrawal and increased quota were the observable response; sole private motive is not established.',[15,5],P3,'Policy and social representation'),
('Legislative Council abolition','Petitioner alleged political motives for abolishing a chamber where the opposition was influential. Court upheld the Assembly resolution.','Resolution challenge dismissed 21 July 1986; abolition effective 1 November','Government defended validity; subsequent abolition is separately documented.',[7,6],P5,'Institutional restructuring'),
('Ananda Vikatan editor’s imprisonment','Assembly sentenced editor S. Balasubramanian to three months’ imprisonment over a cartoon in April 1987; released after two days. In 1994 the High Court found the punishment unconstitutional.','Full Bench judgment 28 September 1994; Rs 1,000 token compensation; not a conviction of MGR','Assembly record credits MGR with requesting reconsideration and release. That intervention did not erase the constitutional violation later found.',[6,8],P5,'Press freedom / legislative privilege'),
('Sri Lankan aid and LTTE connection','Jain inquiry reproduction contains witness descriptions of aid reaching LTTE and the state’s denial that rehabilitation grants financed militant groups.','Conflicting evidence before an inquiry; no criminal finding against MGR asserted','State affidavit identified rehabilitation organisations and humanitarian purposes. A direct contemporaneous MGR explanation and original exhibits remain uncollected.',[9],P5,'Cross-border militancy / aid'),
('1987 Vanniyar agitation','Reporting records at least 21 deaths, mostly from police firing and also caste clashes, during September mobilisation.','Political and policing accountability; original inquiry findings not collected','No complete contemporaneous MGR response has been inspected. The later MBC reservation settlement belongs to the 1989 DMK government.',[16],P5,'Caste conflict / policing')]
for n,(matter,finding,proc,response,ids,phase,cat) in enumerate(controversies,1):
    checked={'Finding':ids,'Procedural status':ids}
    if n in (2,3,4,5): checked['Response']=[6] if n==4 else ids
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Procedural status':proc,'Response':response,'Category':cat,'Latest-status limit':'Latest relevant inspected record; no exhaustive claim about all later litigation.'},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',checked=checked,priority='High',note='Keep allegation, recorded response and institutional finding distinct.')

legacy=[
('Durable party alternative','The 1972 organisation won government in 1977 and survived its founder. Scholarship assigns fan networks and welfare commitments important roles, alongside leadership.',[5,10],'Historical synthesis'),
('Welfare institution-building','The nutritious-meal expansion became an enduring programme. Its scale and institutional survival are different questions from an independently identified effect on nutrition or enrolment.',[3,4],'Administrative history and critical evaluation'),
('Supporter agency','Subramanian’s account complicates a purely leader-centred explanation: beneficiaries and social organisations could press demands and force policy revision.',[5],'Attributed scholarly interpretation'),
('Limits of concentrated authority','The 1994 press-privilege ruling establishes a concrete institutional violation during his final government, while the Assembly records his release intervention. Both belong in the assessment.',[8,6],'Court finding and legislative account'),
('Social inclusion and unresolved conflict','Women-focused education and meal access coexisted with caste mobilisation and disputed policing. A single welfare label cannot establish equal outcomes across groups.',[13,4,16],'Bounded comparison'),
('Succession and women’s leadership','The Janaki–Jayalalithaa struggle shows the importance of access through family, cinema and party work, and the uncertainty of succession after a dominant founder’s death.',[2,10],'Posthumous institutional consequence'),
('Honours and public memory','Posthumous Bharat Ratna in 1988 and the January 2026 ministerial tribute document continuing recognition. They do not settle competing judgments of his government.',[24,22],'Official recognition / attributed tribute'),
('Names versus operating institutions','The medical university is a useful chronology test: 1987 law, 1988 functioning and 1991 name change prevent retrospective credit from collapsing separate decisions.',[11],'Institutional chronology')]
for n,(theme,assessment,ids,basis) in enumerate(legacy,1):
    add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor / basis':basis},ids,'Analysis')

from author_context import populate_context, coverage
populate_context(add,phases)
def gap(n,topic,detail,action,records,priority='Normal'):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':detail,'next_action':action,'status':'Open','record_ids':records})
gap(1,'Original constituency returns','1967 uses an ECI reproduction; 1971–84 use secondary tables. 1984 valid-vote denominator remains unverified.','Obtain ECI/CEO original returns; reconcile candidate totals, rejected votes and exact polling days.',['EL02','EL03','EL04','EL05','EL06'],'High')
gap(2,'Council and party-office boundaries','1962 Council route/end and exact DMK treasurership/general-secretary intervals remain unresolved.','Inspect Council member register, election notifications and original party records.',['EL01','OF02','OF04','OF05'],'High')
gap(3,'Original Assembly record','Review was inspected on a third-party host after official archive timeout.','Obtain archival scan and compare office chronology, women’s representation and privilege proceedings.',['OF06','OF11','CV04'])
gap(4,'Reservation orders','Income-ceiling reversal and quota increase rely on reporting and scholarship; primary GO retrieval failed.','Retrieve 1979–80 orders and complete Mandal/Ambasankar records; separate notification and effect dates.',['PG04','CV02'],'High')
gap(5,'Independent policy outcomes','Programme histories establish implementation; retrospective data cannot isolate MGR’s contribution.','Collect contemporaneous audits, budgets and independent evaluations of nutrition, schooling and fiscal tradeoffs.',['PG01','PG02','PG03','PG05','PG06','PG07'],'High')
gap(6,'Sri Lankan assistance','Inquiry reproduced on advocacy archive; conflicting testimony and state response; original exhibits absent.','Retrieve original Jain report, grants and contemporary Assembly debate; seek independent evidence of recipients and use.',['PG10','CV05'],'High')
gap(7,'Vanniyar agitation accountability','Death count and chronology use retrospective reporting; original inquiry and MGR response not collected.','Obtain police/inquiry records, legislative debate and accounts of Dalit communities affected by violence.',['PG11','CV06'],'High')
gap(8,'Village-administration reform','Judgment located but not read; implementation and distributional effects remain unreviewed.','Obtain K. Rajendran judgment, 1980 law and administrative follow-up.',['PG12'],'High')
gap(9,'Gender mechanisms','Women’s support and policy pathways documented; matched access, media treatment and authority outcomes remain unmeasured.','Add gender scholarship, candidate-selection records, worker studies and comparable media samples.',['G01','G04','G05','G06','G09'])
gap(10,'Early economic and international context','No source collected isolates links between broad conditions and early personal choices.','Use period studies and correspondence; avoid projecting later welfare or Sri Lankan policy backwards.',['E104','E105','E205','E305'])
gap(11,'Chronology variants and originals','Birth locality, treasurer appointment, TASMAC incorporation versus operations and 1967 shooting judgment require reconciliation.','Prefer birth/party/company records and signed court judgment; retain broad dates until then.',['OV01','OF04','PG08','TL07'])
gap(12,'Contested personal responses','Full DMK response to 1972 charges and complete MGR statements on later disputes are missing.','Seek contemporaneous Tamil press, speeches and Assembly transcripts; do not treat missing responses as admissions.',['CV01','CV05','CV06'])

base=Path(__file__).parent
data={'schema_version':1,'subject':'M. G. Ramachandran','as_of':ASOF,'guidance':'Ten gender dimensions cover the career; ten era dimensions are examined in each of five phases. Context informs interpretation without excusing conduct or assuming causation. Supported means the registered field has inspected-passage support or bounded synthesis; it is not a completeness score. Blank election numbers mean unavailable, not zero. See Research Queue.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
