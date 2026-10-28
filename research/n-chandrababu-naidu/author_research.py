"""Rebuild Naidu's research records; run research_workbook.py afterwards."""
import hashlib, json
from pathlib import Path
from author_sources import ASOF, sources, retrievals

P1='P1 | Formation and party organisation (1950–1994)'
P2='P2 | Reform governments (1995–2004)'
P3='P3 | Opposition in undivided AP (2004–2014)'
P4='P4 | Successor-state government (2014–2019)'
P5='P5 | Opposition and legal conflict (2019–2024)'
P6='P6 | Coalition return (2024–2026)'
phases=[P1,P2,P3,P4,P5,P6]
tables, claims, evidence, gaps = {}, [], [], []
R={r['source_id']:r for r in retrievals if r['access_status']=='Passage inspected'}
def table(name,lead,dates=()): tables[name]={'lead_columns':lead,'date_columns':list(dates),'rows':[]}
def add(name,rid,fields,nums,typ='Recorded fact',phase=None,context='',checked=None,note='',status='Supported',priority='Normal',independent=False):
    ids=[f'S{n:03d}' if isinstance(n,int) else n for n in nums]
    idcol={'Overview':'Overview ID','Context & Constraints':'Context ID','Career Timeline':'Timeline ID','Elections':'Election ID','Offices & Party':'Position ID','Controversies':'Matter ID','Legacy & Assessments':'Assessment ID'}.get(name,'Record ID')
    row={idcol:rid,**fields,'Claim type':typ,'Source IDs':'; '.join(ids)}
    if phase: row['Career phase']=phase
    if context: row['Context IDs']=context
    if note: row['Research note']=note
    if typ!='Method / scope': row['Corroboration']='Primary record' if all(sources[int(s[1:])-1]['Primary / secondary']=='Primary' for s in ids) else ('Multiple origins / inspect evidence' if independent else 'See field evidence and source limitations')
    tables[name]['rows'].append(row)
    if typ=='Method / scope': return row
    if checked is None: checked={k:ids for k in fields if k in ('Finding / value','Finding','Description','Assessment')}
    for field,support in checked.items():
        support=[f'S{s:03d}' if isinstance(s,int) else s for s in support]
        cid=f'C-{rid}-{sum(c["record_id"]==rid for c in claims)+1:02d}'
        actual=status if all(s in R for s in support) else 'Not reviewed'
        evs=[]
        if actual=='Supported':
            for sid in support:
                ret=R[sid]; eid=f'EV-{len(evidence)+1:04d}'; evs.append(eid)
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':ret['id'],'locator':ret['locator'],'passage_paraphrase':ret['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex: inspected-passage review','reviewed_at':ASOF,'note':'Support is limited to the registered field. Analytical wording is synthesis; qualifications and source limitations remain operative.'})
        value=row[field]
        c={'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':value,'fingerprint':hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':typ,'status':actual,'priority':priority,'candidate_source_ids':support,'evidence_ids':evs,'contradictions':[],'review_note':note or ('Bounded analytical synthesis; no exclusive causal claim.' if typ=='Analysis' else 'Checked only to the scope and qualifications of this field.')}
        if independent and len(support)>1: c['requires_independent_corroboration']=True
        claims.append(c)
    return row

table('Overview',['Overview ID','Topic','Finding / value'])
table('Context & Constraints',['Context ID','Career phase','Coverage item','Finding'])
table('Career Timeline',['Timeline ID','Period','Event','Description'],['Start date'])
table('Elections',['Election ID','Year','House / route','Constituency','Result','Candidate votes'])
table('Offices & Party',['Position ID','Position / institution','Period','Finding'],['Start date','End date'])
table('Policy & Governance',['Record ID','Initiative / decision','Finding','Stage'])
table('Ideas & Political Method',['Record ID','Topic','Finding'])
table('Controversies',['Matter ID','Matter','Finding','Procedural status'])
table('Legacy & Assessments',['Assessment ID','Theme','Assessment'])

def ov(n,topic,value,ids,typ='Recorded fact',**kw): return add('Overview',f'OV{n:02d}',{'Topic':topic,'Finding / value':value},ids,typ,**kw)
ov(1,'Identity','Nara Chandrababu Naidu; commonly N. Chandrababu Naidu or CBN. Born 20 April 1950 in Naravaripalle; living at the research cutoff.',[1,3],priority='High')
ov(2,'Current status','Chief Minister of Andhra Pradesh; current spell began 12 June 2024. Four ministries across three continuous spells: 1995–2004, 2014–2019 and 2024 onward.',[2,3,5,6,7,8],'Analysis',priority='High')
ov(3,'Geography and party','Congress(I) legislator from Chandragiri in 1978; joined Telugu Desam Party after the 1983 defeat. Kuppam became his enduring electoral base from 1989.',[4,13],'Analysis')
ov(4,'Education','Official district profile lists M.A.; university, subject and year have not been reconciled against an original education record.',[2],note='Government-conference search excerpt mentions economics at Sri Venkateswara University, but the document could not be retrieved.')
ov(5,'Career in brief','Congress minister, TDP organiser, successor to N.T. Rama Rao after the 1995 revolt, reform-oriented CM, long-serving opposition leader and post-bifurcation state builder.',[2,4,5,17,42],'Analysis')
ov(6,'Electoral record','Ten personal Assembly contests are recorded: nine wins and the 1983 Chandragiri loss; eight consecutive Kuppam wins from 1989 through 2024. The 2004 and 2019 statewide defeats did not remove his constituency seat.',[4,9,10,11,12,13,14,15],'Analysis',priority='High')
ov(7,'Development record','Associated with technology-led investment promotion, e-governance and stakeholder programmes; later governments centred on Amaravati and infrastructure. Implementation and distributional effects require separate evaluation.',[17,19,20],'Analysis')
ov(8,'Welfare evolution','Farm-debt relief, higher pensions, school assistance through mothers and free bus travel show the continued importance of welfare within his development agenda.',[22,34,35,36],'Analysis')
ov(9,'Coalition method','Moved from United Front coordination to BJP partnership; left NDA in 2018 and returned as an influential partner in 2024, when TDP won 16 Lok Sabha seats.',[4,32,33],'Analysis')
ov(10,'2026 capital update','Act 7 of 2026 names Amaravati as Andhra Pradesh’s capital, with deemed effect from 2 June 2024. Statutory designation and completion of city construction are distinct.',[21],'Analysis',priority='High')
ov(11,'Legal update','The skill-development case was reported closed on 12 January 2026 after acceptance of a CID report. This follows the 2023 arrest and the Supreme Court’s split 2024 procedural ruling; no conviction is recorded in these sources.',[23,24,25],'Analysis',priority='High',independent=True,note='Latest inspected closure reporting; original order and any subsequent challenge remain open. Closure is not described as a trial acquittal.')
ov(12,'Accountability','Basheerbagh firing, disputed party succession, capital-land issues and the Tirupati allegation require different evidentiary tests. Investigations, oral observations and political criticism are kept separate.',[5,20,26,29,31],'Analysis')
ov(13,'Gender and power','Family networks mattered to party access and succession. Women were addressed through self-help groups, welfare and kinship language; these do not establish women’s equal authority inside the party.',[4,17,18,34,35],'Analysis',context='G03; G07; G09')
ov(14,'Historical significance','His career illustrates the durability of a regional party leader across liberalisation, national coalitions, territorial division and repeated electoral reversals. Technocratic leadership and competitive welfare coexist.',[4,17,32,33,42],'Analysis')
ov(15,'Scope and cutoff','Research snapshot: 28 October 2026. Six career phases; English-language primary records, scholarship and reporting. This is a structured profile, not a complete archive or live legal-status service.',[],'Method / scope')
ov(16,'Reading the evidence','Read the initial finding and review status; expand the + column group for qualifications. All citations opens every source link. Claims identifies reviewed fields; neighbouring cells are not automatically certified.',[],'Method / scope')
ov(17,'Numerical conventions','Votes are individual ballots. Signed margins are candidate minus principal opponent. Blank votes or shares are gaps, not zero. Post-2008 boundaries and NOTA mean shares across years are not strictly comparable.',[],'Method / scope')
ov(18,'Open priorities','Original early/recent election returns; exact party and opposition-office boundaries; original 2026 closure order and laddu chargesheet; policy audits; Telugu archives; and independent gender/outcome studies.',[],'Method / scope')

events=[
('20 April 1950','Birth','Born in Naravaripalle.',[1],P1,'1950-04-20'),
('1978','First Assembly election','Won Chandragiri on a Congress(I) ticket.',[4],P1,None),
('1980','Ministerial entry','Inducted as a minister under T. Anjaiah; official profile lists Archives and Cinematography.',[4,2],P1,None),
('1983','Defeat and party change','Lost Chandragiri and subsequently joined TDP.',[4],P1,None),
('1984','NTR restoration campaign','Organising during the removal of NTR helped consolidate his position in TDP.',[4],P1,None),
('1985–1989','Party organisation','Served as TDP general secretary and an adviser to NTR.',[4],P1,None),
('1989','Kuppam base','Won Kuppam, beginning the sequence of victories recorded in Elections.',[13],P1,None),
('1994–1995','Finance and Revenue','Held these portfolios in NTR’s government.',[2,4],P1,None),
('1 September 1995','First ministry','Sworn CM after the party revolt; proved a floor majority on 7 September.',[5],P2,'1995-09-01'),
('1996','United Front','Served as United Front convenor, extending influence beyond state executive office.',[4],P2,None),
('1997','Janmabhoomi','Stakeholder-based local-development programme became a flagship initiative.',[17],P2,None),
('1999','Vision 2020','Government articulated a long-term development strategy; targets were not realised-outcome measurements.',[17],P2,None),
('11 October 1999','Second ministry','Took a fresh oath after the election victory.',[6],P2,'1999-10-11'),
('28 August 2000','Basheerbagh firing','Police firing during tariff protests later prompted judicial directions for investigation.',[26,27],P2,'2000-08-28'),
('1 October 2003','Alipiri attack','Official-report search excerpt records an attempt on his life; the full passage remains unreviewed.',[41],P2,'2003-10-01'),
('2004','Opposition transition','Retained Kuppam but moved into opposition after the state government changed.',[11,2,18],P3,None),
('2009','Grand Alliance','TDP, TRS and the Left combined against Congress; Naidu retained Kuppam and remained opposition leader.',[39,12,2],P3,None),
('2014','State reorganisation','Division into Andhra Pradesh and Telangana changed the territorial and capital framework.',[42],P4,None),
('8 June 2014','Third ministry','Began his first government of successor Andhra Pradesh.',[2],P4,'2014-06-08'),
('2014–2015','Amaravati assembly of land','Land pooling became a major instrument in the proposed capital region.',[20],P4,None),
('December 2014','Farm-debt relief','Announced the phased waiver roadmap.',[22],P4,None),
('16 March 2018','NDA withdrawal','TDP left the alliance over special-status and reorganisation demands.',[32],P4,'2018-03-16'),
('2019','Statewide defeat','TDP fell to 23 Assembly seats; Naidu retained Kuppam.',[16,14],P5,None),
('July 2019','Earlier capital financing withdrawn','World Bank appraisal records withdrawal of India’s financing request for the earlier Amaravati project.',[20],P5,None),
('9 September 2023','Arrest','Arrested in the skill-development matter; allegations were denied.',[24,25],P5,'2023-09-09'),
('16 January 2024','Split Supreme Court decision','Section 17A issue referred for constitution of a larger bench.',[23],P5,'2024-01-16'),
('June 2024','Electoral return','TDP-led alliance won 164 Assembly seats; TDP won 16 Lok Sabha seats.',[8,33],P6,None),
('12 June 2024','Fourth ministry','Sworn in as Chief Minister.',[7],P6,'2024-06-12'),
('13 June 2024','Pension order','Government enhanced specified pensions and restored NTR Bharosa branding.',[36],P6,'2024-06-13'),
('19 December 2024','Amaravati financing','World Bank Board approved an $800 million programme.',[40],P6,'2024-12-19'),
('12 June 2025','School assistance','Talliki Vandanam rollout approved.',[35],P6,'2025-06-12'),
('15 August 2025','Free bus programme','Stree Shakti launched.',[34],P6,'2025-08-15'),
('14 October 2025','AI investment commitment','Google announced a Visakhapatnam hub and a five-year investment commitment.',[45],P6,'2025-10-14'),
('12 January 2026','Skill-case closure reported','Two reports say the ACB court accepted the CID closure report.',[24,25],P6,'2026-01-12'),
('January 2026','Laddu investigative update','Reporting on the chargesheet described synthetic adulteration and challenged the animal-fat claim.',[29,30],P6,None),
('6 April 2026','Capital amendment enacted','Amaravati designation received Presidential assent.',[21],P6,'2026-04-06'),
('28 April 2026','AI hub construction milestone','Google reported groundbreaking; completion and realised economic benefits remain prospective.',[46],P6,'2026-04-28'),
('August 2026','Polavaram target','Minister reiterated a March 2027 completion target.',[38],P6,None)]
for n,(period,event,desc,ids,phase,dt) in enumerate(events,1):
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':dt,'Date precision':'Day' if dt else 'Year/range as displayed'},ids,'Recorded fact' if n not in (5,12,35,37,38) else 'Analysis',phase,f'E{phases.index(phase)+1}01',priority='High' if n in (9,18,25,26,34,35,36) else 'Normal')

elections=[
(1978,'Chandragiri','Congress(I)','Won',None,None,None,None,None,[4],P1,'Original counts not retrieved.'),
(1983,'Chandragiri','Congress(I)','Lost',None,None,None,None,None,[4],P1,'Original counts not retrieved; electoral defeat preceded TDP entry.'),
(1989,'Kuppam','TDP','Won',50098,'B.R. Doraswamy Naidu','INC',43180,None,[13],P1,'Secondary table; primary return unavailable.'),
(1994,'Kuppam','TDP','Won',81210,'R. Gopinath','INC',24622,107582,[9],P1,'Primary return; valid candidate votes denominator.'),
(1999,'Kuppam','TDP','Won',93288,'M. Subramanya Reddy','INC',27601,125357,[10],P2,'Primary return; valid candidate votes denominator.'),
(2004,'Kuppam','TDP','Won',98123,'M. Subramanyam Reddy','INC',38535,140297,[11],P3,'Primary return; personal victory despite government defeat.'),
(2009,'Kuppam','TDP','Won',89952,'M. Subramanyam Reddy','INC',43886,145287,[12,13],P3,'Primary winner/denominator; opponent count also in secondary table. Post-delimitation seat.'),
(2014,'Kuppam','TDP','Won',102952,'K. Chandramouli','YSRCP',55831,None,[13,14],P4,'Secondary counts. Share withheld without inspected final denominator.'),
(2019,'Kuppam','TDP','Won',100146,'Krishna Chandra Mouli','YSRCP',69424,None,[14],P5,'Secondary counts. Personal victory despite statewide TDP defeat.'),
(2024,'Kuppam','TDP','Won',121929,'K.R.J. Bharath','YSRCP',73923,203367,[15],P6,'ADR reproduction: denominator includes 2,115 NOTA. Elector/turnout conflict excluded.')]
for n,(year,seat,party,result,votes,opp,oparty,ovotes,denom,ids,phase,note) in enumerate(elections,1):
    fields={'Year':year,'House / route':'Assembly / direct','Constituency':seat,'Result':result,'Candidate votes':votes,'Party':party,'Opponent':opp,'Opponent party':oparty,'Opponent votes':ovotes,'Signed vote margin':None,'Vote share':votes/denom if denom else None,'Share denominator':denom,'Finding':f'{result} {seat} in {year}; see numerical fields and source notes.','Candidate status':'Personal contestant','Geography':'Undivided Andhra Pradesh' if year<=2009 else 'Successor Andhra Pradesh','Counting unit':'Votes; single-member constituency','Result scope':'Personal seat, not party-wide mandate'}
    checked={'Finding':ids}
    if year == 2014:
        fields['Geography']='Undivided AP at polling; seat in successor Andhra Pradesh'
        note += ' Polling preceded the effective state division; the seat formed part of the successor-state Assembly.'
    if votes is not None: checked.update({'Candidate votes':ids,'Opponent votes':ids})
    if denom: checked['Share denominator']=ids
    add('Elections',f'EL{n:02d}',fields,ids,phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,note=note,priority='High')
for n,year,partyseats,alliance,ids,phase in [(11,2019,23,None,[16],P5),(12,2024,135,164,[8],P6)]:
    add('Elections',f'EL{n:02d}',{'Year':year,'House / route':'Assembly / party result','Constituency':'Andhra Pradesh statewide','Result':'Party tally','Candidate votes':None,'Opponent votes':None,'Vote share':None,'Signed vote margin':None,'TDP seats':partyseats,'Alliance seats':alliance,'Total seats':175,'Finding':f'TDP won {partyseats} of 175 seats'+(f'; TDP–Jana Sena–BJP alliance won {alliance}.' if alliance else '; YSRCP won 151.'),'Candidate status':'Party/campaign leader; separate from personal contest'},ids,phase=phase,context=f'E{phases.index(phase)+1}03')

offices=[
('MLA, Chandragiri','1978–1983','Elected for Congress(I); term ended with the 1983 defeat.',[4],P1,None,None,'Elected'),
('Minister, Andhra Pradesh','1980–1982/83','Congress ministry role; Archives and Cinematography are listed in the official profile.',[4,2],P1,None,None,'Ministerial'),
('General secretary / coordinator, TDP','1980s–1994','Party organisational responsibilities preceded chief-ministerial office.',[2,4],P1,None,None,'Party'),
('Deputy legislative leader, TDP','1989–1994','Deputy leader while TDP was in opposition; do not confuse this with sole Leader of Opposition.',[4],P1,None,None,'Legislative'),
('Minister for Finance and Revenue','1994–1995','Held portfolios in NTR’s government.',[2,4],P1,None,None,'Ministerial'),
('Chief Minister, first ministry','1 Sep 1995–Oct 1999','Assumed office after the legislative-party revolt; floor majority established.',[5,6],P2,'1995-09-01',None,'Executive'),
('Chief Minister, second ministry','11 Oct 1999–May 2004','Fresh ministry after 1999 victory; government changed after the 2004 election.',[6,2,18],P2,'1999-10-11',None,'Executive'),
('United Front convenor','From 1996','National coalition coordination, not a Union ministerial or parliamentary seat held by Naidu.',[4],P2,None,None,'Coalition'),
('TDP president / national president','Leadership from 1995; current leadership confirmed 2024','Organisational succession was disputed in 1995; later reporting identifies him as TDP chief.',[5,7],P2,None,None,'Party'),
('Leader of Opposition, Andhra Pradesh','2004–2014','Official profile records opposition leadership during the two Assembly periods.',[2],P3,None,None,'Legislative'),
('Chief Minister, third ministry','8 Jun 2014–29 May 2019','First ministry of successor Andhra Pradesh.',[2],P4,'2014-06-08','2019-05-29','Executive'),
('Opposition leader, TDP','2019–2024','Led TDP in opposition after the statewide defeat; precise formal Assembly-office dates remain a gap.',[16,25,33],P5,None,None,'Party / legislative'),
('Chief Minister, fourth ministry','12 Jun 2024–present at cutoff','Sworn on 12 June; current institutional page confirms incumbency.',[7,3],P6,'2024-06-12',None,'Executive')]
for n,(pos,period,finding,ids,phase,start,end,category) in enumerate(offices,1):
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':pos,'Period':period,'Finding':finding,'Position category':category,'Start date':start,'End date':end,'Boundary note':'Exact unfilled dates are not inferred; concurrent party and legislative responsibilities are distinct.'},ids,phase=phase,context=f'E{phases.index(phase)+1}02',priority='High' if category=='Executive' else 'Normal')
for n,e in enumerate(elections[2:],14):
    year,seat,party,result,votes,opp,oparty,ovotes,denom,ids,phase,note=e
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':'MLA, Kuppam','Period':f'Elected {year}; Assembly term','Finding':f'Returned from Kuppam in {year}.','Position category':'Elected','Selection route':'Direct constituency election','Boundary note':'Election year is not an exact oath or dissolution date.'},ids,phase=phase,context=f'E{phases.index(phase)+1}03')

policies=[
('Technology and investment promotion','Reform-era government promoted IT, knowledge industries and investor-facing infrastructure.','Implemented initiatives',[17],P2,'Led / promoted','Role shared with firms, administrators and prior/later governments; Hyderabad’s whole subsequent economy is not attributed to one CM.'),
('e-Seva and administrative targets','One-stop citizen-service counters and performance-oriented administration formed part of the reform programme.','Implementation described',[17],P2,'Government leadership','Scholarship distinguishes useful e-seva services from other digital initiatives that did not take off; no universal efficiency claim.'),
('Vision 2020','Government adopted a long-term development vision in 1999.','Strategy / targets',[17],P2,'Led','Targets and marketing do not establish realised growth or distributional success.'),
('Janmabhoomi','Stakeholder-based local works and participation became a flagship programme from 1997.','Implemented programme',[17,18],P2,'Led','Competing accounts concern local mobilisation and weakened elected panchayats; participation is not identical to devolved authority.'),
('Women’s self-help groups','Self-help groups were integrated into rural development; the successor budget reported substantial coverage.','Administrative scale reported',[17,18],P2,'Expanded / associated','Groups predated and outlasted his government. Participation, credit access and empowerment are distinct outcomes.'),
('Power-sector reform','Tariff changes and restructuring generated organised resistance and an accountability crisis.','Reform and contestation',[17,26],P2,'Led state policy','Financial viability, agricultural livelihoods and policing must be evaluated separately; no single-cause explanation of the 2004 defeat.'),
('Farm loan waiver','2014 roadmap proposed phased relief for eligible agricultural borrowing.','Announced / rollout described',[22],P4,'Announced and directed','Eligibility and instalments mattered; full discharge, credit discipline and farm-income effects remain unverified.'),
('Amaravati land pooling','Government assembled land through pooling in exchange for serviced plots and benefits.','Implementation with complaints',[20],P4,'State government / APCRDA','Landowners and landless workers face different risks. Livelihood restoration, consultation and future plot values require independent assessment.'),
('Amaravati relaunch and finance','World Bank approved $800 million in December 2024 for institutional and infrastructure development.','Financing approved',[19,40],P6,'Government sponsorship / negotiated support','Funding is shared with Union institutions and lenders; approval is not construction completion.'),
('Capital’s legal designation','2026 amendment names Amaravati and defines its notified area.','Enacted',[21],P6,'State advocacy; Union legislation','Parliament and President effected the amendment. It does not certify physical completion or settle every land grievance.'),
('Polavaram','Renewed Union funding and state review accompanied a March 2027 completion target.','Funded / ongoing',[37,38],P6,'Reviewed / implemented inherited project','Multiple governments, Union agencies, contractors and rehabilitation obligations matter. No completed-project claim as of cutoff.'),
('NTR Bharosa pensions','June 2024 order raises specified pensions from ₹3,000 to ₹4,000.','Order issued',[36],P6,'Government approval','Coverage, timely payment and poverty effects require separate evidence. Disability-related categories have different rates.'),
('Talliki Vandanam','June 2025 rollout routes educational support through mothers.','Approved rollout',[35],P6,'Approved','No audited universal disbursement or effect on attendance/learning established; headline budget-beneficiary arithmetic withheld.'),
('Stree Shakti buses','Free travel scheme launched on 15 August 2025 with zero-fare ticketing and APSRTC reimbursement.','Launched',[34],P6,'Launched','Potential mobility gains and auto-driver effects need measurement; launch promises are not evaluated outcomes.'),
('Visakhapatnam AI hub','Google announced approximately $15 billion across 2026–2030 and subsequently reported groundbreaking.','Commitment / construction milestone',[45,46],P6,'State partner / associated','Company, Union government and infrastructure partners share roles. Do not present the commitment as funds already spent or jobs already created.'),
('Pattiseema irrigation','Official audit search excerpt locates Pattiseema within a lift-irrigation review; full audit findings remain unread.','Evidence gap',[43],P4,'Associated with state programme','No detailed cost, environmental-compliance or agricultural-benefit assertion is certified from the unavailable audit.')]
for n,(topic,finding,stage,ids,phase,role,limit) in enumerate(policies,1):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':topic,'Finding':finding,'Stage':stage,'Documented role':role,'Outcome / attribution limit':limit},ids,'Analysis',phase,f'E{phases.index(phase)+1}04',priority='High' if n in (8,10,11,16) else 'Normal')

ideas=[
('Managerial leadership','Administrative targets, digital services and investment promotion linked a managerial image to government practice.',[17],P2),
('Regional party and national bargaining','United Front coordination, BJP alliance and later realignments show repeated use of regional-party strength in national coalitions.',[4,32,33],P6),
('Telangana and changing alliances','The 2009 alliance brought TDP together with TRS and the Left; agreement for an election did not remove underlying territorial tensions.',[39,42],P3),
('Special-category status','TDP framed its 2018 NDA withdrawal through unmet state demands; BJP disputed its account.',[32],P4),
('Development and welfare','Debt relief and recent transfers/transport benefits complicate any timeless label of a leader concerned only with markets or technology.',[22,34,35,36],P6),
('Family and organisation','Marriage into NTR’s family and independent organisational work both mattered. The 1995 succession remains politically disputed.',[4,5],P1),
('Constituency versus statewide mandate','Repeated Kuppam wins coexisted with statewide government losses, demonstrating different scales of electoral support.',[11,14,16],P5),
('Women as a political constituency','Self-help-group mobilisation and elder-brother language connect benefits with political identity; women’s autonomous views require independent research.',[18,34],P6),
('Religion and public claims','Tirupati rhetoric shows that technical-development branding can coexist with religious political mobilisation; the specific animal-fat claim requires separate evidence.',[29,30,31],P6),
('Investment communication','Large commitments and construction milestones are central to the development narrative; they must be distinguished from realised output.',[45,46],P6)]
for n,(topic,finding,ids,phase) in enumerate(ideas,1): add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding,'Evidence type':'Documented action, attributed rhetoric or bounded synthesis'},ids,'Analysis',phase,f'E{phases.index(phase)+1}07')

matters=[
('1995 party succession','Naidu displaced NTR through a party revolt and legislative majority; the organisational legitimacy was contested.','Party/institutional dispute; oath and majority recorded','NTR alleged disloyalty and invalid party proceedings; Naidu asserted majority support and a valid leadership change.',[4,5],P2,'1995','No personal criminal finding inferred from the party dispute.'),
('Basheerbagh police firing','Three deaths were reported after the 28 August 2000 tariff protest; High Court ordered investigation of justification and excessive force.','Judicial investigation directions; final accountability outcome not obtained','Petitioners alleged unnecessary force. State described CID/magisterial investigation; the court required scrutiny of police conduct.',[26,27],P2,'2000–2004','Do not convert petitioners’ narrative into adjudicated fact or infer a personal firing order.'),
('Amaravati land and livelihoods','World Bank appraisal records complaints and a recommended investigation before India withdrew the earlier financing request.','Land-policy criticism / institutional review; later programme redesigned','Government programme offered serviced plots and support; complainants raised livelihood, compensation and consultation concerns.',[19,20],P4,'2014–2024','Funding withdrawal is not proof of corruption; later loan approval is not proof every grievance was resolved.'),
('Skill-development prosecution','Arrested in September 2023; judges split on section 17A in January 2024; court acceptance of CID closure was reported for 12 January 2026.','Closure report accepted, according to January 2026 reporting','Naidu/TDP denied wrongdoing and called the case political. CID later reported no substance concerning his role.',[23,24,25],P6,'2023–2026','Original closure order and any appeal remain unverified. Closure is neither a conviction nor a merits acquittal after trial.'),
('2015 cash-for-vote allegations','LiveLaw reports that the Supreme Court declined the challenge seeking a probe and that the separate CBI-inquiry writ was withdrawn on 21 August 2024.','Special-leave challenge dismissed; writ withdrawn (reported)','Naidu had challenged the private-complaint-based investigation direction in the High Court; allegations arose from Council-election voting.',[28],P6,'2015–2024','Original Supreme Court order not obtained; no conviction or acquittal of Naidu inferred. Separate proceedings against others are not his procedural status.'),
('Tirupati laddu allegation','Court questioned the public allegation in 2024; 2026 reporting on the chargesheet described synthetic adulteration and undermined the animal-fat claim.','Oral judicial criticism; investigative chargesheet reporting','State defended laboratory material; YSRCP denied the allegation and later demanded an apology. Later Naidu response not established in inspected passages.',[29,30,31],P6,'2024–2026','Original chargesheet and later trial orders not inspected. Adulteration, particular substances and political attribution are distinct claims.'),
('Reform priorities and local democracy','Scholarly and successor-government accounts question the distribution of reform benefits and the role of elected panchayats.','Political / academic criticism, not criminal adjudication','Government promoted participation and efficiency; successor budget argued the nodal-officer model weakened elected local bodies.',[17,18],P2,'1995–2004','Interpretations are attributed. No quantified causal share of the 2004 defeat or statewide distress is assigned to one policy.')]
for n,(matter,finding,procedure,response,ids,phase,period,caution) in enumerate(matters,1):
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Procedural status':procedure,'Response / competing account':response,'Period / latest checked evidence':period,'Scope / caution':caution},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',priority='High',independent=n in (1,2,4,6,7))

legacy=[
('Reform-era significance','Mooij interprets the reform programme through class change, political organisation and deliberate promotion, while noting uneven implementation.',[17],'Jos Mooij, scholarly working paper',P2),
('Digital administrative institutions','e-Seva offers a concrete service-delivery mechanism; its success cannot be extended to every digitisation initiative or all later IT growth.',[17],'Scholarly assessment with attribution limits',P2),
('Regional coalition leverage','The 2024 parliamentary arithmetic restored leverage to TDP; influence over national government differs from Naidu holding a Union office.',[33],'Reuters reporting; bounded institutional interpretation',P6),
('Territorial discontinuity','Hyderabad-era achievements and successor-state performance must be evaluated on different geographical and fiscal bases.',[42,19],'Research synthesis of institutional framework',P4),
('Capital-building legacy','Amaravati now has explicit statutory designation and renewed financing, while delivery and fair treatment of affected people remain continuing tests.',[21,19,20,40],'Legal record and lender programme assessed separately',P6),
('Welfare and gender','Women-centred delivery mechanisms are visible; substantive empowerment and women’s authority within TDP remain less well evidenced.',[18,34,35],'Research synthesis; outcomes not presumed',P6),
('Electoral resilience','Eight Kuppam victories and repeated government returns coexist with serious statewide defeats; resilience is not a measure of uniform public approval.',[13,14,15,16,8],'Election evidence',P6),
('Accountability and reputation','Skill-case closure, police-accountability questions and the laddu controversy must retain their different procedures and evidentiary limits.',[24,25,26,29,30],'Procedural synthesis',P6)]
for n,(theme,assessment,ids,assessor,phase) in enumerate(legacy,1): add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor / basis':assessor,'Competing view / limit':'Read linked policy and controversy records; no overall greatness score or exclusive causal attribution.'},ids,'Analysis',phase,f'E{phases.index(phase)+1}10')

from author_context import populate_context, coverage
populate_context(add,phases)

def gap(n,topic,detail,action,records,priority='Normal'):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':detail,'next_action':action,'status':'Open','record_ids':records})
gap(1,'Original election returns','1978/1983 vote counts withheld; 1989, 2014, 2019 and 2024 rely on labelled secondary evidence.','Retrieve ECI/CEO originals or certified Form 20 returns; reconcile seat boundaries and postal votes.',['EL01','EL02','EL03','EL08','EL09','EL10'],'High')
gap(2,'Vote-share denominators','Five personal contests lack a fully inspected share denominator; 2024 denominator includes NOTA.','Use complete candidate and NOTA tables; keep shares blank until checked.',['EL01','EL02','EL03','EL08','EL09'],'High')
gap(3,'Exact office boundaries','Ministerial, party-office and opposition-office days and 2004 end boundary remain uncertain.','Inspect appointment notifications, Assembly bulletins, resignations and party resolutions.',['OF02','OF03','OF07','OF09','OF10','OF12'],'High')
gap(4,'Skill-case finality','Closure reported 12 January 2026, but original order and later challenges not obtained.','Obtain ACB closure order, High Court docket and any connected ED disposition.',['CV04','OV11'],'High')
gap(5,'Laddu investigative record','Original chargesheet, full laboratory reports, subsequent trial orders and later Naidu response are uncollected.','Retrieve filed documents and response; distinguish rejected tanker samples from prasadam actually distributed.',['CV06'],'High')
gap(6,'Cash-for-vote order','Detailed reporting distinguishes dismissal and withdrawal; original order remains missing.','Retrieve Supreme Court orders of 21 August 2024 and separate proceedings against other accused.',['CV05'],'High')
gap(7,'Police accountability','2000 investigation directions inspected; final reports and sanctions uncollected.','Locate CID/magisterial outcomes and follow-up litigation; do not infer personal responsibility.',['CV02'],'High')
gap(8,'Alipiri full record','MHA PDF inaccessible; attack entry remains a limited search-excerpt lead.','Obtain official mirror or full contemporaneous report; separate attack facts and later trial findings.',['TL15','G06'],'High')
gap(9,'Pattiseema and other infrastructure','Audit PDF returned 404; project costs, environmental proceedings and benefits need dedicated review.','Retrieve full CAG chapter and relevant NGT orders; add Polavaram rehabilitation and interstate evidence.',['PG16','PG11'],'High')
gap(10,'Independent policy outcomes','Capital, farm-debt relief, pensions, buses, education and AI investment evidence is stronger on design/actions than outcomes.','Collect audited expenditure, beneficiaries’ experience and independent impact assessments.',['PG07','PG08','PG09','PG12','PG13','PG14','PG15'],'High')
gap(11,'Gender mechanisms','No matched recruitment, portfolio, media-treatment or decision-making study collected.','Compare contemporaneous male/female TDP and rival-party leaders; add women’s organisations and survey evidence.',['G01','G04','G05','G09','G10'])
gap(12,'Regional-language and opposition phases','Telugu archives, 2012–13 padayatra, 2018 Congress alliance and exact Telangana-position changes require expansion.','Use dated party resolutions, speeches and contemporaneous Telugu reporting.',['E306','E507','IM03'])
gap(13,'Education and identity','Exact qualification subject/year and reliable caste-specific political mechanisms not fully established.','Consult original affidavit/university record and scholarship; do not infer caste from surname.',['OV04','G03'])
gap(14,'Other major governance and crises','Hudhud recovery, manufacturing investments, RTG/FiberNet, fiscal outcomes and other investigations are not comprehensively covered.','Add official audits, budgets and court records with matter-specific current status.',['OV18'],'High')
gap(15,'2014 statutory original','India Code download timed out and MHA mirror failed; PRS summary used for basic reorganisation context.','Retrieve original act plus commencement notification; check section-specific claims before adding them.',['TL18','E409'])

base=Path(__file__).parent
data={'schema_version':1,'subject':'N. Chandrababu Naidu','as_of':ASOF,'guidance':'Six phases; all ten era dimensions in each phase and all ten gender dimensions. Distinguish undivided and successor Andhra Pradesh. Registered-field support does not certify every cell or establish causal impact. Source gaps remain explicit.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
