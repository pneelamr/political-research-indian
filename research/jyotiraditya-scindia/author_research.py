"""Reproducible Scindia research. Authoring metadata is not evidence certification."""
import hashlib, json, re
from pathlib import Path
from author_sources import ASOF, sources, retrievals
P1='P1 | Entry and UPA-I (2001–May 2009)'
P2='P2 | UPA-II ministries (May 2009–May 2014)'
P3='P3 | Congress opposition and rupture (May 2014–March 2020)'
P4='P4 | BJP, Rajya Sabha and aviation (March 2020–June 2024)'
P5='P5 | Guna return, Communications and DoNER (June 2024–October 2026)'
phases=[P1,P2,P3,P4,P5]
tables,claims,evidence,gaps={},[],[],[]
R={r['source_id']:r for r in retrievals if r['access_status']=='Passage inspected'}

def tidy(text):
    text=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])',' ',text)
    for word in ('January','February','March','April','May','June','July','August','September','October','November','December'):
        text=re.sub(r'(?<=[a-z])'+word,' '+word,text)
    text=re.sub(r'\b([45]) G\b',r'\1G',text)
    text=re.sub(r'([,;:])(?=\S)',r'\1 ',text)
    return text.replace('lakhcrore','lakh crore')

def table(name,lead,dates=()): tables[name]={'lead_columns':lead,'date_columns':list(dates),'rows':[]}
def add(name,rid,fields,nums,typ='Recorded fact',phase=None,context='',checked=None,note='',status='Supported',priority='Normal',independent=False):
    fields={k:(tidy(v) if isinstance(v,str) and k != "Career phase" else v) for k,v in fields.items()}
    note=tidy(note)
    ids=[f'S{n:03d}' if isinstance(n,int) else n for n in nums]
    idcol={'Overview':'Overview ID','Context & Constraints':'Context ID','Career Timeline':'Timeline ID','Elections':'Election ID','Offices & Party':'Position ID','Controversies':'Matter ID','Legacy & Assessments':'Assessment ID'}.get(name,'Record ID')
    row={idcol:rid,**fields,'Claim type':typ,'Source IDs':'; '.join(ids)}
    if phase: row['Career phase']=phase
    if context: row['Context IDs']=context
    if note: row['Research note']=note
    tables[name]['rows'].append(row)
    if typ=='Method / scope': return row
    if checked is None:
        checked={k:ids for k,v in fields.items() if k in ('Finding / value','Finding','Description','Assessment','Documented role','Response','Procedural status','Start date','End date','Election date','Candidate votes','Opponent votes','Vote share') and v is not None}
    for field,support in checked.items():
        support=[f'S{s:03d}' if isinstance(s,int) else s for s in support]
        cid=f'C-{rid}-{sum(c["record_id"]==rid for c in claims)+1:02d}'; evs=[]
        if status=='Supported':
            for sid in support:
                r=R[sid]; eid=f'EV-{len(evidence)+1:04d}'; evs.append(eid)
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':r['id'],'locator':r['locator'],'passage_paraphrase':r['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex: inspected-passage review','reviewed_at':ASOF,'note':'Combined passage support where several sources are listed. Analysis is a bounded inference; institutional estimates and criticism remain attributed.'})
        val=row[field]
        claim={'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':val,'fingerprint':hashlib.sha256(json.dumps(val,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':typ,'status':status,'priority':priority,'candidate_source_ids':support,'evidence_ids':evs,'contradictions':[],'review_note':note or ('Inference limited to the cited evidence.' if typ=='Analysis' else 'Registered field checked against identified passages; surrounding qualifications apply.')}
        if independent: claim['requires_independent_corroboration']=True
        claims.append(claim)
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
def ov(n,t,f,ids,typ='Recorded fact',**kw): return add('Overview',f'OV{n:02d}',{'Topic':t,'Finding / value':f},ids,typ,**kw)
ov(1,'Identity','Jyotiraditya Madhavrao Scindia; institutional records also use Jyotiraditya M. Scindia. Born 1 January 1971 in Mumbai.',[1,3])
ov(2,'Status at cutoff','BJP Lok Sabha member elected from Guna in 2024; Union Minister of Communications and Development of North Eastern Region. NEC roster also lists him as vice-chairman.',[17,3,43],priority='High',context='E502')
ov(3,'Formation and entry','Educated at Doon, Harvard and Stanford; BA and MBA. Entered Congress in December 2001 after his father Madhavrao’s death, with national party sponsorship and a family constituency connection.',[1,4],typ='Analysis',context='G01')
ov(4,'Party trajectory','Congress from December 2001 to March 2020; joined BJP on 11 March 2020. His ministerial career crosses Congress-led UPA and BJP-led governments.',[4,9,1,5],typ='Analysis',context='E301')
ov(5,'Principal geography','Guna is his recurring Lok Sabha constituency; Gwalior–Chambal is a wider arena of reported political influence. Neither family association nor regional campaign activity means every local result is his personal result.',[14,17,12],typ='Analysis',context='E409')
ov(6,'Career in brief','Progressed from family succession into Parliament and junior economic ministries; the 2019 defeat preceded a party switch, Rajya Sabha return and Cabinet roles, followed by the 2024 Guna comeback.',[1,16,9,18,5,17],typ='Analysis')
ov(7,'Personal elections covered','Seven contests: six direct Lok Sabha elections, with five wins and one loss, plus the successful indirect Rajya Sabha election in 2020. Assembly-party and supporter results are treated separately.',[14,16,17,18],typ='Analysis')
ov(8,'Governance evidence','Postal modernisation, grid integration, aviation digitisation, steel incentives and telecom deployment show administrative activity across portfolios. Independent evidence of his separate contribution to durable outcomes is limited.',[19,22,24,28,30],typ='Analysis')
ov(9,'Defining political controversy','The 2020 break and allied MLA departures preceded the collapse of Kamal Nath’s government. Scindia framed his move as a response to Congress failures; opponents saw betrayal.',[9,10],typ='Analysis',context='E302',priority='High')
ov(10,'Technology and consent','Digi Yatra enrolment complaints and the short-lived mandatory Sanchar Saathi installation policy exposed tensions between service digitisation and user choice. The later mandate was withdrawn in December 2025.',[25,33,34,35],typ='Analysis',context='E506')
ov(11,'Gender assessment','His public advocacy for women in aviation is documented. It does not establish a career-wide gender-equality record or demonstrate that representation targets were achieved.',[29],typ='Analysis',context='G09')
ov(12,'Historical significance','A case of dynastic entry, national-party realignment and ministerial continuity across governments. Electoral recovery is documented; explanations based only on charisma, family or ideology remain insufficient.',[4,9,16,17],typ='Analysis')
ov(13,'Research cutoff','4 October 2026. Current office rosters were inspected; each legal or administrative status retains its own evidence date. No later court disposition is inferred from an unsuccessful search.',[],typ='Method / scope')
ov(14,'Reading guide','Expand the + columns for dates, roles, caveats and context. All citations opens every row reference; Claims and Evidence identify the fields actually reviewed. Source presence alone is not verification.',[],typ='Method / scope')
ov(15,'Election units','Signed margin = Scindia votes minus principal opponent votes. Negative means defeat. Rajya Sabha votes are MLA ballots, with no popular vote share or single-opponent margin. Blank values are unresolved or inapplicable, never zero.',[],typ='Method / scope')
ov(16,'Policy units and attribution','Rs1 crore = Rs10 million; Rs1 lakh crore = Rs1 trillion. Targets, MoUs, grounded projects, installations and independently measured impacts are distinct. Portfolio overlap is not sole authorship.',[],typ='Method / scope')
ov(17,'Main remaining gaps','Original historical and 2024 detailed election returns; 2024 share denominator; export-cost estimate; later election-petition developments; full UDAN audit replies; independent outcomes and gender-treatment evidence.',[],typ='Method / scope')
ov(18,'Review scope','The register checks the substantive finding fields, dated office boundaries, election quantities, and controversy responses/status. Titles, phase labels, row cautions and coding fields organise the evidence; review counts are not a completeness score.',[],typ='Method / scope')

timeline=[
('1 January 1971','Birth','Born in Mumbai; family background is politically relevant to later entry.',[1],'1971-01-01',P1,'G01'),
('18 December 2001','Congress entry','Admitted by Sonia Gandhi after his father’s death; Guna succession anticipated.',[4],'2001-12-18',P1,'E107'),
('February 2002','First Lok Sabha election','Won the Guna by-election as a Congress candidate.',[1,14],None,P1,'E103'),
('2004','First general-election return','Retained Guna for Congress.',[14],None,P1,'E103'),
('6 April 2008','First Union ministry','Became Minister of State for Communications and Information Technology.',[1],'2008-04-06',P1,'E102'),
('2009','Commerce portfolio','Won Guna again and entered the Commerce and Industry ministry as Minister of State.',[14,1],'2009-05-28',P2,'E204'),
('28 October 2012','Independent charge of Power','Moved to Power as Minister of State with independent charge.',[1],'2012-10-28',P2,'E202'),
('2013','National grid milestone','Southern integration completed during his Power tenure; the network had developed over decades.',[22,1],None,P2,'E204'),
('2014','Congress opposition role','Retained Guna and became Congress chief whip in Lok Sabha.',[14,2],None,P3,'E301'),
('2019','AICC responsibility','Named Congress general secretary for western Uttar Pradesh.',[2],None,P3,'E307'),
('2019','Guna defeat','Lost to BJP’s Krishna Pal Singh, commonly identified as Dr K.P. Yadav.',[16],None,P3,'E303'),
('6 August 2019','Jammu and Kashmir position','Backed integration while qualifying that constitutional process should have been followed.',[13],'2019-08-06',P3,'E302'),
('11 March 2020','Joined BJP','Public Congress resignation on10 March was followed by formal BJP joining the next day.',[9],'2020-03-11',P4,'E401'),
('20 March 2020','Madhya Pradesh government falls','Kamal Nath resigned before the ordered confidence vote after the MLA departures.',[10,11],'2020-03-20',P4,'E402'),
('19 June 2020','Rajya Sabha election','Elected from Madhya Pradesh by the Assembly electorate.',[18],'2020-06-19',P4,'E403'),
('9 July 2021','Civil Aviation charge','Assumed ministerial charge; date denotes taking charge, not the oath.',[5],'2021-07-09',P4,'E404'),
('7 July 2022','Additional Steel charge','Took Steel while retaining Civil Aviation.',[6],'2022-07-07',P4,'E402'),
('1 December 2022','Digi Yatra launch','Launched passenger facial-recognition processing at three airports.',[24],'2022-12-01',P4,'E406'),
('2023','Supporters and regional elections','PTI reported seven wins and six losses among13 nominated supporters in its2020-switch cohort; BJP won18 of34 regional seats.',[12],None,P4,'E407'),
('2024','Guna return','Returned to Lok Sabha as BJP candidate with923302 votes.',[17],None,P5,'E503'),
('11–12 June 2024','New portfolios','Took Communications charge on11 June and DoNER charge on12 June.',[7,8],None,P5,'E502'),
('December 2025','Sanchar Saathi mandate withdrawn','Direction publicised1 December, ministerial clarification2 December and withdrawal3 December.',[33,34,35],'2025-12-03',P5,'E506'),
('January–June 2026','Implementation reporting','Government reported BSNL live-site numbers and Northeast investment follow-through; the indicators have different definitions and dates.',[30,32],None,P5,'E504'),
('September 2026','Guna road dispute','Reporting recorded a contentious resident exchange, opposition criticism and a prospective road-work announcement.',[37,38],None,P5,'E508')]
for n,(period,event,desc,ids,start,phase,ctx) in enumerate(timeline,1):
    checked={'Description':ids}
    if start: checked['Start date']=[35] if n==22 else ([1] if n in (1,5,6,7) else [ids[0]])
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':start,'Date precision':'Exact date for named action' if start else 'Month / year or period'},ids,phase=phase,context=ctx,checked=checked)

# Numeric counts use the inspected source's units; shares are intentionally sparse.
elections=[
(2002,'INC','Won',535728,'Rao Deshraj Singh Yadav','BJP',129160,None,[14],P1,'By-election; primary ECI page inaccessible.'),
(2004,'INC','Won',333954,'Harivallabh Shukla','BJP',247594,None,[14],P1,'General election; secondary historical result table.'),
(2009,'INC','Won',413297,'Dr Narottam Mishra','BJP',163560,None,[14],P2,'General election; boundary changes across decades limit direct geographic comparison.'),
(2014,'INC','Won',517036,'Jaibhansingh Pawaiya','BJP',396244,None,[14],P3,'Counts include the reported candidate total; do not substitute lower EVM-only totals.'),
(2019,'INC','Lost',488500,'Krishna Pal Singh (Dr K.P. Yadav)','BJP',614049,.4145,[16],P3,'ADR reports41.45%, rounded; original CEO result book not inspected.'),
(2020,'BJP','Won',56,None,None,None,None,[18],P4,'Indirect Rajya Sabha election: judgment reports5600 value units at100 per MLA ballot;56 ballots. Three seats filled; no unique opponent margin.'),
(2024,'BJP','Won',923302,'Yadvendra Rao Deshraj Singh','INC',382373,None,[17],P5,'Final official return unavailable; shares in indexed records use differing denominators/vintages, so no share is imported.')]
for n,(year,party,result,votes,opp,oparty,ovotes,share,ids,phase,note) in enumerate(elections,1):
    indirect=year==2020
    fields={'Year':year,'Constituency':'Madhya Pradesh' if indirect else 'Guna','Result':result,'Candidate votes':votes,'House / route':'Rajya Sabha / indirect' if indirect else 'Lok Sabha / direct','Election type':'Indirect multi-seat election' if indirect else ('By-election' if year==2002 else 'General election'),'Party':party,'Principal opponent':opp,'Opponent party':oparty,'Opponent votes':ovotes,'Signed vote margin':None if ovotes is None else votes-ovotes,'Vote share':share,'Vote-share basis':'Reported by ADR; rounded percentage of polled votes' if share else ('Not applicable: MLA electoral college' if indirect else 'Unresolved; no checked denominator'),'Election date':'2020-06-19' if indirect else None,'Date meaning':'Poll and count' if indirect else 'Year only; exact poll day not verified','Vote unit':'MLA ballots; source vote-value divided by100' if indirect else 'Individual candidate votes','Finding':f'{party} candidate Scindia {result.lower()} this contest; see numeric fields and unit notes.'}
    checked={k:ids for k in ('Finding','Candidate votes','Opponent votes','Vote share','Election date') if fields.get(k) is not None}
    add('Elections',f'EL{n:02d}',fields,ids,phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,note=note,priority='High')

offices=[
('Congress membership','December2001–March2020','Formal entry18 December2001; resignation made public10 March2020.',[4,9],'2001-12-18',None,P1,'Party admission / resignation'),
('Lok Sabha MP, Guna: Congress','February2002–May2019','Won2002 by-election and2004,2009,2014 general elections; lost2019.',[1,14,16],None,None,P1,'Direct election, four successive wins'),
('MoS, Communications and IT','6 April2008–22 May2009','Junior Union minister in UPA-I.',[1],'2008-04-06','2009-05-22',P1,'Union executive appointment'),
('MoS, Commerce and Industry','28 May2009–28 October2012','Junior economic ministry in UPA-II.',[1],'2009-05-28','2012-10-28',P2,'Union executive appointment'),
('MoS (independent charge), Power','28 October2012–26 May2014','Headed Power as independent-charge MoS, not Cabinet Minister.',[1],'2012-10-28','2014-05-26',P2,'Union executive appointment'),
('Congress chief whip, Lok Sabha','From2014; exact end not established','Official institutional biography identifies chief-whip appointment in2014.',[2],None,None,P3,'Parliamentary party appointment'),
('AICC general secretary, western UP','2019–Congress departure2020','National organisational assignment before the BJP switch; not an elected office in Uttar Pradesh.',[2,9],None,None,P3,'Party appointment'),
('Congress Working Committee','Before March2020; exact boundaries uncollected','CWC service is listed by the institutional biography.',[2],None,None,P3,'Party organisation'),
('BJP membership','11 March2020–cutoff','Joined BJP in2020; elected its Guna candidate in2024.',[9,17],'2020-03-11',None,P4,'Party admission'),
('Rajya Sabha MP, Madhya Pradesh','June2020–2024 Lok Sabha return','Won2020 indirect election and returned to Lok Sabha in2024; precise vacancy notification not collected.',[18,17],None,None,P4,'Election by MLAs'),
('Union Cabinet Minister, Civil Aviation','July2021–June2024 portfolio transition','Assumed charge9 July2021; byJune2024 he took Communications and DoNER.',[5,7,8],'2021-07-09',None,P4,'Cabinet appointment; start field is charge-taking'),
('Union Cabinet Minister, Steel','July2022–June2024 portfolio transition','Additional charge taken7 July2022 alongside Civil Aviation.',[6,7,8],'2022-07-07',None,P4,'Additional Cabinet portfolio; exact cessation uncollected'),
('Lok Sabha MP, Guna: BJP','2024–cutoff','Won2024 general election, his fifth Lok Sabha victory.',[14,17],None,None,P5,'Direct election'),
('Union Minister, Communications','June2024–cutoff','Took charge11 June2024; current Posts roster lists him as minister.',[7,3],'2024-06-11',None,P5,'Cabinet appointment; start field is charge-taking'),
('Union Minister, DoNER','June2024–cutoff','Took charge12 June2024; current NEC roster confirms DoNER minister and vice-chairman.',[8,43],'2024-06-12',None,P5,'Cabinet appointment; start field is charge-taking'),
('Parliamentary committees','2002–2020: selected recorded service','Rajya Sabha biography lists Finance, External Affairs, Privileges and Home Affairs committee work at different times.',[1],None,None,P3,'Parliamentary committee membership; not executive control')]
for n,(title,period,finding,ids,start,end,phase,route) in enumerate(offices,1):
    checked={'Finding':ids}
    if start: checked['Start date']=[ids[0]]
    if end: checked['End date']=[ids[0]]
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':title,'Period':period,'Finding':finding,'Start date':start,'End date':end,'Selection route':route},ids,phase=phase,context=f'E{phases.index(phase)+1}02',checked=checked)

def policy(n,title,period,finding,role,stage,ids,phase,limit,ctx=None,status='Supported'):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':title,'Finding':finding,'Stage':stage,'Period':period,'Documented role':role,'Attribution / outcome limits':limit},ids,'Analysis',phase,ctx or f'E{phases.index(phase)+1}04',note=limit,status=status)
policy(1,'Project Arrow','2008 onward','Postal services were modernised in successive phases; the2010 reply records1000 offices across the first three phases.','Institutional biography credits involvement during his Communications/IT tenure.','Implemented multiyear programme',[19,2],P1,'The2010 description extends beyond his2009 exit; office counts are outputs, not independently measured service improvements.')
policy(2,'Export facilitation','2009–2012','His official biography credits efforts to reduce export transaction costs.','Commerce and Industry MoS associated with facilitation efforts.','Attributed institutional assessment',[2],P2,'The Rs2100crore savings estimate in an indexed parliamentary answer is withheld pending original-document inspection.')
policy(3,'National synchronous grid','2013','Southern-region connection completed the synchronous national grid in2013.','Power minister during final integration; discussed planned connection inMay2013.','Infrastructure milestone',[21,22],P2,'POWERGRID, regional institutions and earlier governments built preceding stages; reliability and welfare effects need distinct measures.')
policy(4,'Green-energy corridors','2013','Ministry described a master plan for renewable-power evacuation infrastructure.','Scindia presented the programme to a parliamentary consultative committee.','Planning and proposed investment',[21],P2,'Master-plan announcement is not proof that every line was financed or completed during his tenure.')
policy(5,'Air India divestment','January2022','Government completed transfer of its Air India/Air India Express stakes and the specified AISATS holding.','Civil Aviation portfolio holder at transaction completion.','Completed ownership transaction',[23,5],P4,'Finance, DIPAM, Cabinet and buyer roles matter. Employment, fares and service quality are not established by the sale record.')
policy(6,'Digi Yatra','December2022 onward','Passenger facial-recognition processing launched at three airports and officially expanded to13 byDecember2023.','Scindia launched the initial three-airport service.','Launch and reported rollout',[24,39],P4,'Consent complaints later required clarification; adoption counts do not establish convenience, privacy or equal access for all travellers.','E406')
policy(7,'UDAN expansion and sustainability','2021–2024','Ministry reported60 new routes commencing in2023. CAG separately found sustainability and control problems in earlier award cohorts.','Minister administering an inherited programme launched in2016.','Administrative outputs and retrospective audit',[39,27,5],P4,'Current starts and earlier audited concessions are different cohorts; neither source isolates his causal contribution.')
policy(8,'Women in aviation','March2022','Encouraged women’s aviation careers and expressed a50% pilot-representation aspiration.','Minister speaking at an event recognising women professionals.','Public advocacy / aspiration',[29],P4,'Not an enacted quota or proof of achieved representation; cohort and career-progression effects unmeasured.','G07')
policy(9,'Specialty-steel incentives','March2023','Government signed57 MoUs with27 companies under PLI; announced investment and capacity expectations.','Steel minister presiding with MoS Kulaste.','Agreements; projected outcomes',[28],P4,'Rs30000crore investment and25million tonnes are prospective five-year expectations, not realised output.')
policy(10,'BSNL indigenous4G','September2023–January2026','Government reported97672 installed sites,95511 live, as of15 January2026.','Communications minister during later deployment; equipment supply began before hisJune2024 charge.','Reported operational infrastructure',[30,7],P5,'5G-upgradable does not mean5G deployed. Site totals do not prove coverage quality, commercial viability or sole ministerial authorship.')
policy(11,'Sanchar Saathi mandate and reversal','November–December2025','Preinstallation direction dated28 November was publicised1 December, then withdrawn3 December.','Scindia defended voluntary activation and removability in a2 December clarification.','Direction, clarification and withdrawal',[33,34,35],P5,'App continued; withdrawal concerns compulsory preinstallation. Anti-fraud objectives and privacy assurances require independent evaluation.','E506')
policy(12,'Northeast investment mobilisation','2025–2026','Ministry reported Rs4.48lakhcrore investment interest in2025 and nearly Rs40000crore grounded byJune2026.','DoNER minister promoting investment; states responsible for project follow-through.','MoUs/leads and attributed implementation claim',[31,32],P5,'No verified conversion rate: denominators and grounded definition are not harmonised; no claim of fully disbursed or completed projects.','E509')
policy(13,'NEC coordination and value chains','June2026','Eight chief-minister-led task forces presented recommendations, with further steering arrangements proposed.','NEC vice-chairman under chairman Amit Shah.','Recommendations and coordination proposals',[32,43],P5,'Regional development also depends on state governments, other ministries and implementation agencies.','E509')
policy(14,'Guna road commitment','September2026','Local report describes a Rs3crore road announcement with estimates, tenders and post-monsoon work still ahead.','Constituency representative announcing a response after resident complaints.','Reported commitment; completion unverified',[37],P5,'Funding provenance not reconciled; no claim that the road was completed by the research cutoff.','E508')

ideas=[
('Family succession and party sponsorship','His entry combined Madhavrao’s constituency connection with Sonia Gandhi’s formal admission. This demonstrates a pathway to access, not an automatic explanation of every later win.',[4],P1,'G01'),
('Administrative modernisation','Official profiles and programme records emphasise service technology and infrastructure. Treat that as a recurring policy emphasis, not proof of technocratic superiority.',[2,24,30],P5,'E504'),
('Economic orientation','Export facilitation, private ownership transfer and investment promotion recur across portfolios. This supports a limited economic-policy comparison; it does not establish a complete or unchanging doctrine.',[2,23,31],P5,'E504'),
('Position beyond party line','His2019 integration statement preceded joining BJP and included a constitutional-process caveat. It should not be simplified into unqualified support or a recorded legislative vote.',[13],P3,'E302'),
('Party change: stated reasons','In2020 he criticised Congress direction and MP governance while endorsing Modi. Ambition, exclusion or ideological conversion are competing interpretations unless independently evidenced.',[9],P4,'E401'),
('Network power has limits','The2023 supporter cohort had mixed results. Regional campaign activity and nomination influence coexist with dependence on party structures and local candidates.',[12],P4,'E407'),
('Constituency responsiveness and authority','The2026 road exchange places demands for local services alongside dispute over the tone citizens should use. Two reports support the episode, but a short video cannot establish a permanent leadership trait.',[37,38],P5,'E508'),
('Public technology assurances','Responses to Digi Yatra and Sanchar Saathi criticism stressed consent and user choice. These establish his stated position; implementation and privacy protections require independent scrutiny.',[25,34],P5,'E506'),
('Federal coordination','The DoNER/NEC role uses intergovernmental coordination and investment promotion across multiple states; it is institutionally different from governing any one state as chief minister.',[31,32,43],P5,'E509')]
for n,(topic,finding,ids,phase,ctx) in enumerate(ideas,1): add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding},ids,'Analysis',phase,ctx)

controversies=[
('2020 break and state-government collapse','Congress described the departures as betrayal; Scindia linked his exit to party and governance failures. Nath resigned before the floor test.','Scindia defended the change on public-welfare grounds; rebels disputed claims their decisions were involuntary.','Political controversy, March2020; SC upheld floor-test direction in its13 April reasons.',[9,10,11],P4,'No criminal inducement finding is inferred. Confidence, resignations and disqualification are distinct legal questions.'),
('Rajya Sabha election-disclosure challenge','Govind Singh challenged the2020 election over omission of FIR176/2018; the High Court rejected the election petition.','Scindia disputed knowledge and a disclosure obligation; court reasoned no cognizance had been taken on the facts before it.','Election petition dismissed15 February2024; later appeal and underlying FIR status not established.',[18],P4,'This is not a criminal acquittal or blanket exoneration. The judicial record supports the dated disposition, not independent proof of every pleaded allegation.'),
('UDAN audit','CAG identified weak route sustainability, delays and financial controls in the first three bidding rounds.','The ministry separately reported60 route starts in2023; the full audit’s detailed agency replies were not retrieved.','Audit tabled10 August2023; sustainability update refers toMarch2023.',[27,39],P4,'Later output reporting is context, not a direct rebuttal. Award cohorts largely predate his charge; aggregate findings do not establish personal misconduct.'),
('Digi Yatra consent complaints','Reports recorded complaints that some passengers were enrolled without meaningful choice, alongside digital-rights concerns.','Scindia said passenger consent was necessary and airports should secure informed consent.','Administrative clarification inJanuary2024; subsequent compliance not independently established.',[25,26,24],P4,'Complaints are attributed, not judicial findings. Two reports share the same ministerial-letter origin and are not independent corroboration of its contents.'),
('Sanchar Saathi mandatory installation','Mandatory preinstallation drew privacy and choice objections before government withdrew the requirement.','Scindia said activation was voluntary, the app removable and surveillance concerns unfounded.','Direction publicised1 December2025; clarification2 December; mandate withdrawn3 December.',[33,34,35,36],P5,'The withdrawal is documented; the security properties of the app are not verified by official assurances.'),
('Guna road-protest exchange','Opposition criticism followed his response to a resident linking road provision to electoral support.','Reported reply objected to the manner of the demand; local reporting also records a road-work commitment.','Public criticism reported18–19 September2026; road delivery unverified at cutoff.',[37,38],P5,'Political accountability episode, not a judicial proceeding. Funding provenance remains unresolved.')]
for n,(matter,finding,response,proc,ids,phase,note) in enumerate(controversies,1):
    support={'Finding':ids,'Response':ids,'Procedural status':ids}
    if n==1: support={'Finding':[9,10],'Response':[9,10],'Procedural status':[10,11]}
    if n==3: support={'Finding':[27],'Response':[39],'Procedural status':[27]}
    if n==4: support={'Finding':[25,26],'Response':[25],'Procedural status':[25,26]}
    if n==5: support={'Finding':[33,35,36],'Response':[34],'Procedural status':[33,34,35]}
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Response':response,'Procedural status':proc},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',checked=support,note=note,priority='High')

legacy=[
('Dynasty and democratic uncertainty','Family succession eased entry, yet2019 defeat and2024 recovery show that the seat was electorally contestable. Evidence does not identify the separate effects of surname, party and personal work.',[4,16,17],'Workbook synthesis','G01'),
('Consequences of realignment','The2020 switch was connected to a change of government in Madhya Pradesh and his return to national office. His welfare-based account and opponents’ betrayal criticism remain competing interpretations.',[9,10,5],'Competing contemporary political accounts','E401'),
('Cross-government administrative career','Service modernisation and infrastructure recur in his portfolios. Institutional biographies offer a favourable account, while shared authorship and limited evaluation constrain personal credit.',[2,22,30],'Official self-presentation and bounded synthesis','E504'),
('Outputs versus durable outcomes','New routes and digitised services coexisted with audited sustainability problems and consent complaints. A balanced record requires both implementation measures and consequences for users.',[39,27,25],'CAG, ministry reporting and journalism','E410'),
('Digital governance accountability','The Sanchar Saathi reversal is a documented policy correction following criticism. It does not by itself settle whether the app’s remaining operation protects privacy adequately.',[33,35,36],'Documented reversal; outcome question open','E506'),
('Women’s representation','Advocacy for women pilots is part of the record; no independent longitudinal evaluation here links his interventions to recruitment, retention or leadership gains.',[29],'Attributed advocacy; evidence limitation','G10'),
('Regional development legacy still forming','DoNER investment interest and reported grounding are early-stage indicators. Lasting employment, ecological effects and distribution across states remain open evaluation questions.',[31,32],'Provisional assessment','E510')]
for n,(theme,assessment,ids,assessor,ctx) in enumerate(legacy,1): add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor':assessor,'Assessment status':'Provisional as of4 October2026'},ids,'Analysis',context=ctx)

# Context authoring is separate so all ten items remain visible for every phase.
from author_context import populate_context, coverage
populate_context(add,phases)

def gap(n,priority,topic,text,action,records,status='Open'):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':text,'next_action':action,'status':status,'record_ids':records})
gap(1,'High','Primary election returns','2002/2004/2009/2014 counts use a secondary table;2019 uses ADR. Original CEO/ECI pages failed.','Obtain ECI statistical returns or CEO mirrors; reconcile candidate totals and denominators.',['EL01','EL02','EL03','EL04','EL05'])
gap(2,'High','2024 detailed result and share','TOI result table supports counts; ECI PDF returned406 and CEO host failed. Indexed shares differ by denominator/vintage.','Inspect final Guna Form20 or ECI detailed return before adding vote share.',['EL07'])
gap(3,'Normal','Exact office boundaries','Oath/appointment dates differ from charge-taking. RS vacancy and short party-role end dates not collected.','Retrieve appointment and vacancy gazettes; retain present action-specific dates.',['OF06','OF08','OF10','OF11','OF12'])
gap(4,'Normal','Export transaction-cost estimate','Legacy parliamentary PDF returned HTML; search-only Rs2100crore estimate not admitted as supported.','Obtain question4366 dated16 May2012 or original task-force report and inspect definitions.',['PG02'])
gap(5,'High','Election-petition follow-up','15 February2024 judgment inspected; later appeal and FIR procedural history unknown.','Check MPHC/Supreme Court docket and relevant criminal record without inferring acquittal.',['CV02'])
gap(6,'Normal','UDAN detailed replies','Official audit summary read; full report timed out. No detailed department rebuttal inspected.','Retrieve full report, management replies and later remedial evidence for matched cohorts.',['CV03','PG07'])
gap(7,'Normal','Programme effects','Independent causal estimates absent for digital services, BSNL quality, steel PLI realisation and Northeast investments.','Collect implementation audits and beneficiary/firm outcome studies with dates and counterfactual limits.',['PG06','PG09','PG10','PG12'])
gap(8,'Normal','Gender pathways and treatment','No reliable matched study found on male gender advantage, portfolio allocation or gender-specific threats in this career.','Seek scholarship or comparative reporting; do not interpret noncoverage as absence.',['G01','G04','G05','G06','G09'])
gap(9,'Normal','Guna road delivery','September commitment recorded; source of funds, tender and completion unverified.','Inspect district sanction, tender and completion documents.',['PG14','CV06'])
gap(10,'Normal','International and social context','Some phase-specific context items have limited directly linked evidence; no systematic voter-coalition dataset.','Add contemporary economic/diplomatic and constituency studies before making causal claims.',['E105','E205','E208','E305','E405','E505'])
gap(11,'Normal','First ministerial year discrepancy','Aviation2021 biography says2007; precise Rajya Sabha2020 chronology and Steel2022 biography support2008.','Use6 April2008; preserve discrepancy for any future gazette check.',['TL05','OF03'],'Resolved for this edition')

for claim in claims:
    if claim['record_id'] in ('CV01','CV05','CV06') and claim['field']=='Finding':
        claim['requires_independent_corroboration']=True
for src in sources:
    for key in ('Title','Reliability / limitation','Locator'):
        src[key]=tidy(src[key])
for ret in retrievals:
    for key in ('passage_paraphrase','locator','result','next_action'):
        ret[key]=tidy(ret[key])
for ev in evidence:
    ev['passage_paraphrase']=tidy(ev['passage_paraphrase'])
    ev['locator']=tidy(ev['locator'])
for g in gaps:
    g['gap']=tidy(g['gap']);g['next_action']=tidy(g['next_action'])
base=Path(__file__).parent
data={'schema_version':1,'subject':'Jyotiraditya Madhavrao Scindia','as_of':ASOF,'guidance':'Context findings distinguish demonstrated pathways from open questions. Ten gender items cover the career; ten era items are reviewed in each of five phases. Repeated source facts support different analytical questions, not independent corroboration.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
