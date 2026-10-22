"""Reproducible L. K. Advani research with field-specific evidence review."""
import hashlib, json
from pathlib import Path
from author_sources import ASOF, sources, retrievals
P1='P1 | Formation, opposition and Janata (1942–1979)'
P2='P2 | BJP construction and mobilisation (1980–1997)'
P3='P3 | NDA government (1998–May 2004)'
P4='P4 | Opposition and succession (May 2004–2013)'
P5='P5 | Elder status and legacy (2014–2026)'
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
def ov(n,t,f,ids,typ='Recorded fact',**kw): return add('Overview',f'OV{n:02d}',{'Topic':t,'Finding / value':f},ids,typ,**kw)
ov(1,'Identity','Lal Krishna Advani, commonly L. K. Advani; born 8 November 1927 in Karachi, then British India and now Pakistan.',[1,2])
ov(2,'Name variant','The 2024 Bharat Ratna Gazette uses Lal Kishinchand Advani; this workbook retains the commonly used parliamentary name Lal Krishna Advani.',[1,3])
ov(3,'Education and formation','Law graduate; the party biography identifies Government Law College, Bombay. RSS participation from 1942, Partition migration and subsequent Rajasthan organisation work shaped his early political route.',[1,2,5],'Analysis',context='E107')
ov(4,'Organisations','RSS, Bharatiya Jana Sangh, Janata Party and BJP were successive or overlapping organisational settings. BJP general secretary from 1980 and recurrent party presidencies anchored his national role.',[1,2,20,41],'Analysis')
ov(5,'Principal offices','Delhi Metropolitan Council chairman; four Rajya Sabha terms; seven Lok Sabha terms; Union I&B and Home Minister; Deputy Prime Minister, 2002–2004; parliamentary opposition leader.',[1,15,19])
ov(6,'Personal election record','Eight Lok Sabha constituency victories across seven general elections: New Delhi in 1989 and 1991; Gandhinagar in 1991, 1998, 1999, 2004, 2009 and 2014. The two 1991 wins count as two contests but one parliamentary term.',[1,6,7,8,9,10],'Analysis',priority='High')
ov(7,'Geography','Karachi and Partition migration; organisational work in Rajasthan and Delhi; national parliamentary career, with Gandhinagar the sustained direct-election base.',[2,5,6,7,8,9,10],'Analysis',context='E209')
ov(8,'Career in brief','Moved from cadre organisation and parliamentary opposition to religious-nationalist mobilisation, coalition government and later opposition leadership. After succession conflicts, his influence increasingly operated through elder status and public memory.',[2,5,15,27,31],'Analysis')
ov(9,'Most consequential political contribution','Helped construct the BJP as a national contender through organisation, the Ayodhya movement and partnership with Vajpayee. The scale and desirability of that transformation are contested, and were not his work alone.',[5,29,30],'Analysis',context='E201')
ov(10,'Governance domains','Broadcasting autonomy proposals; internal security and POTA; state reorganisation; policing, citizenship administration and talks with a Hurriyat faction. Legislative action, ministry outputs and demonstrated social outcomes are separated.',[1,15,16,17,24,25],'Analysis')
ov(11,'Principal controversy','The Ayodhya campaign and Babri demolition remain central to assessments. The Liberhan inquiry’s attribution of responsibility, the 2020 criminal acquittal and the 2022 standing-based appeal dismissal are different proceedings.',[12,13,14,40],'Analysis',priority='High')
ov(12,'Other disputed episodes','The hawala case ended at the charge stage on insufficient evidence; Gujarat 2002 raised political accountability questions; Kandahar produced conflicting participant recollections; the Jinnah remarks triggered an internal ideological dispute.',[11,20,21,22,35],'Analysis')
ov(13,'Political method','Combined cadre networks, parliamentary work, symbolic public journeys, ideological argument and coalition bargaining. In later statements he stressed expression, internal democracy and respect for political opponents.',[2,5,26,41],'Analysis')
ov(14,'Gender synthesis','His 1997 speech supports women’s reservation and more female candidates; the 2008 BJP organisational quota is a separate party decision. Neither establishes his personal effect on women’s nominations, power or welfare.',[33,41],'Analysis',context='G07; G09')
ov(15,'Era synthesis','The relevant settings change from opposition under Congress and the Emergency, through Mandal–Ayodhya mobilisation and coalition government, to succession conflicts and the Modi-era remembrance of an earlier leadership.',[2,5,20,27,31],'Analysis')
ov(16,'Current status and cutoff','Research cutoff: 21 October 2026. Last verified Lok Sabha term ended in 2019; Bharat Ratna was conferred in March 2024. PTI reported his discharge from hospital on 19 October. A 25 September report records clearance after electoral-roll field verification; final publication was still scheduled for 4 November.',[1,3,4,42,43],'Analysis',phase=P5)
ov(17,'Evidence limits','Primary evidence is strongest for early election returns, Parliament, the hawala judgment and selected ministry actions. Original 2004–2014 constituency returns, full Babri trial and Liberhan records, some office dates and independent policy outcomes remain priorities.',[1,6,7,8,9,10,11,12,14,15],'Analysis')

timeline=[
('1942','Joins RSS','Party biography dates RSS entry to 1942, before the Partition migration.',[2],P1,'E107',None),
('1947–1951','Partition and Rajasthan organisation','Migrated from Sindh in 1947; party biography records organisational work in Rajasthan during 1947–1951.',[2,5],P1,'E108',None),
('1952–1957','Jana Sangh state work','Served as joint secretary of the Rajasthan Jana Sangh, according to the party record.',[2],P1,'E107',None),
('1957–1967','Delhi parliamentary and editorial work','Assisted Jana Sangh MPs from 1957; worked at Organiser from 1960 to 1967 while building Delhi organisational connections.',[2,5],P1,'E106',None),
('1966–1970','Delhi Metropolitan Council','Member from 1966; chairman from 1967 to 1970. This was a metropolitan institution, not the later Delhi chief ministership.',[1],P1,'E109',None),
('3 April 1970','Enters Rajya Sabha','First of four consecutive Upper House terms began on 3 April 1970.',[1],P1,'E102','1970-04-03'),
('1973–1977, broad period','National Jana Sangh leadership','Party biography records election as president in February 1973 and re-elections in 1974 and 1975; exact appointment and end boundaries differ across summaries.',[1,2],P1,'E107',None),
('June 1975–January 1977','Emergency detention','Party record reports detention in Bangalore under MISA from June 1975 until 18 January 1977.',[2],P1,'E102',None),
('1977–1979','Janata government','Became I&B Minister in the Janata government; the broadcasting-autonomy process culminated in a 1979 bill that did not become law then.',[1,17],P1,'E106',None),
('1980–1986','BJP organisation','Served as BJP general secretary in its early years.',[1,2],P2,'E207',None),
('May 1986','BJP presidency','Returned the party presidency to an organiser associated with a more assertive ideological campaign; the office itself is documented, its strategic significance is an interpretation.',[2,5,29],P2,'E201',None),
('June 1989','Palampur and Ayodhya','BJP endorsed the Ram temple demand at Palampur; religious mobilisation became central to the national campaign.',[5],P2,'E208',None),
('November 1989','First Lok Sabha victory','Won New Delhi with 129,256 votes; the official return records a 31,841-vote margin.',[6],P2,'E203','1989-11-22'),
('25 September 1990','Rath Yatra begins','Launched the Somnath-to-Ayodhya mobilisation; it connected temple politics, national visibility and pressure on the V. P. Singh government.',[5],P2,'E206','1990-09-25'),
('October–November 1990','Arrest and support withdrawal','Arrest in Bihar was followed by BJP withdrawal of support from V. P. Singh. Exact arrest-day precision is withheld because accounts differ.',[5],P2,'E202',None),
('1991','Two constituency victories','Won New Delhi narrowly and Gandhinagar by a much larger margin in the same general election.',[7],P2,'E203',None),
('6 December 1992','Babri Masjid demolition','Demolition at Ayodhya led to prolonged inquiry and criminal proceedings involving Advani; the later criminal case resulted in acquittal.',[12,14,40],P2,'E202','1992-12-06'),
('1993–1998','Second BJP presidency','Resumed the presidency; party record dates this period from July 1993 to May 1998.',[2],P2,'E207',None),
('1996','Hawala-related withdrawal','Resigned his Lok Sabha seat and did not contest the 1996 election; later described the decision as necessary for public credibility while denying wrongdoing.',[39],P2,'E202',None),
('19 December 1997','Coalition and campaign preparation','Bhubaneswar speech linked good governance and national consensus with basic services, decentralisation, broader candidate selection and women’s reservation.',[41],P2,'E204','1997-12-19'),
('2 March 1998','Hawala appeal dismissed','Supreme Court dismissed CBI appeals after finding no prima facie case against Advani and Shukla on the presented evidence.',[11],P3,'E302','1998-03-02'),
('1998–2004','Home Ministry','Home leadership spanned NDA governments; exact first appointment is an indexed official lead, while later tenure is directly confirmed in parliamentary and ministry records.',[1,15,16,18],P3,'E302',None),
('December 1999','IC-814 hijacking','The hostage crisis ended with release of three prisoners; Advani’s later memoir defended the resolution, while Cabinet recollections became disputed.',[21,22],P3,'E305',None),
('July–August 2000','State reorganisation bill','Introduced the Uttar Pradesh Reorganisation Bill on 25 July; Lok Sabha passed it on 1 August. Passage and subsequent state commencement are different dates.',[24,25],P3,'E309',None),
('26 March 2002','POTA joint sitting','Moved the anti-terror bill at the joint sitting; the debate exposed disagreement over necessity, rights and safeguards.',[16],P3,'E302','2002-03-26'),
('29 June 2002','Deputy Prime Minister','Appointment announced while he retained Home Affairs.',[19],P3,'E307','2002-06-29'),
('23 July 2002','Gujarat accountability debate','Defended the state government against claims of state-sponsored violence and defended its election decision; acknowledged possible official failures and Election Commission authority.',[35],P3,'E302','2002-07-23'),
('January–March 2004','Hurriyat dialogue','Met an Ansari-led Hurriyat delegation twice; ministry report describes detention reviews and confidence-building discussions.',[15],P3,'E305',None),
('October 2004','Returns to party presidency','His 27 October National Council speech followed Naidu’s resignation and analysed the BJP’s general-election defeat.',[41],P4,'E401',None),
('June–December 2005','Jinnah dispute and departure','Pakistan remarks triggered RSS/BJP criticism, a withdrawn resignation and eventual departure from the presidency at year-end.',[20],P4,'E405',None),
('2009','Prime-ministerial campaign','Led the BJP’s national campaign, but Congress won 206 seats and BJP 116. His own Gandhinagar victory is separately recorded.',[28,10],P4,'E403',None),
('10–11 June 2013','Succession protest','Resigned from key party posts after Modi’s campaign elevation, then withdrew after RSS intervention.',[27],P4,'E407',None),
('2014–2019','Final Lok Sabha term','Re-elected from Gandhinagar in 2014; BJP selected Amit Shah for that constituency in 2019.',[1,10,26],P5,'E503',None),
('4 April 2019','Public democratic principles','Published a statement emphasising diversity, free expression and respect for political adversaries.',[26],P5,'E506','2019-04-04'),
('30 September 2020','Babri criminal acquittal','Special CBI court acquitted all 32 accused, including Advani, for lack of conclusive evidence.',[12],P5,'E502','2020-09-30'),
('9 November 2022','Appeal dismissed for standing','Allahabad High Court dismissed two appellants’ challenge on standing grounds, as reported the next day.',[13],P5,'E502','2022-11-09'),
('31 March 2024','Bharat Ratna conferred','President conferred the award at his New Delhi residence; Gazette names Lal Kishinchand Advani.',[3,4],P5,'E501','2024-03-31')]
for n,(period,event,desc,ids,phase,ctx,date) in enumerate(timeline,1):
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':date,'Date precision':'Day' if date else 'Period; see description'},ids,'Analysis',phase,ctx,status='Not reviewed' if n==22 else 'Supported',priority='High' if n==22 else 'Normal')

# Four indirect elections are kept distinct from eight constituency wins.
for n,(year,start,end,phase) in enumerate([(1970,'1970-04-03','1976-04-02',P1),(1976,'1976-04-03','1982-04-02',P1),(1982,'1982-04-03','1988-04-02',P2),(1988,'1988-04-03','1989-11-27',P2)],1):
    add('Elections',f'EL{n:02d}',{'Year':year,'House / route':'Rajya Sabha / indirect','Constituency':'State allocation pending original return','Result':'Elected','Candidate votes':None,'Opponent votes':None,'Vote share':None,'Signed vote margin':None,'Election date':None,'Finding':f'Upper House term {start} to {end}; term-start date is not asserted as polling date.','Seat / comparison note':'State allocation and indirect-election vote detail await election notifications.'},[1],phase=phase,context='E102' if n<3 else 'E202')
direct=[
(1989,'New Delhi',129256,'V. Mohini Giri',97415,232744,6,'1989-11-22',P2),
(1991,'New Delhi',93662,'Rajesh Khanna',92073,215834,7,'1991-05-20',P2),
(1991,'Gandhinagar',356902,'G. I. Patel',231223,615690,7,None,P2),
(1998,'Gandhinagar',541340,'P. K. Datta',264639,904339,8,'1998-02-28',P3),
(1999,'Gandhinagar',453229,'T. N. Seshan',264285,741260,9,None,P3),
(2004,'Gandhinagar',516120,'Gabhaji Mangaji Thakor',298982,845576,10,None,P3),
(2009,'Gandhinagar',434044,'Sureshkumar Chaturdas Patel',312297,790737,10,None,P4),
(2014,'Gandhinagar',773539,'Kiritbhai Ishvarbhai Patel',290418,1135495,10,None,P5)]
for n,(year,seat,votes,opponent,opp,total,sid,date,phase) in enumerate(direct,5):
    note=('2014 denominator includes 12,777 NOTA votes; other listed denominators are valid candidate votes.' if year==2014 else ('Official Assembly-segment votes plus postal ballots sum to 453,229; a circulated 453,299 total is rejected.' if year==1999 else 'Secondary table; original constituency return still needed.' if year>=2004 else 'Official constituency table.'))
    if year==1991 and seat=='Gandhinagar': note+=' Exact polling date withheld: published field requires reconciliation with postponed polling.'
    fields={'Year':year,'House / route':'Lok Sabha / direct','Constituency':seat,'Result':'Won','Candidate votes':votes,'Opponent votes':opp,'Vote share':votes/total,'Signed vote margin':votes-opp,'Election date':date,'Party':'BJP','Principal opponent':opponent,'Opponent party':'INC','Share denominator':total,'Denominator definition':'Total including NOTA' if year==2014 else 'Valid candidate votes','Finding':f'Won {seat}; {votes:,} votes against {opp:,}, margin {votes-opp:,}.','Seat / comparison note':note,'Candidate status':'Personal contestant'}
    checked={f:[sid] for f in ['Finding','Candidate votes','Opponent votes','Share denominator','Vote share','Signed vote margin']}
    if date: checked['Election date']=[sid]
    add('Elections',f'EL{n:02d}',fields,[sid],phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,priority='High',note=note)

offices=[
('Rajasthan Jana Sangh joint secretary','1952–1957','State organisation and cadre work, recorded in the party biography.',[2],P1,'Party appointment',None,None),
('Delhi Jana Sangh secretary','1958–1963','Delhi organisational responsibility.',[2],P1,'Party appointment',None,None),
('Delhi Jana Sangh vice-president','1965–1967','Party leadership role distinct from metropolitan office.',[2],P1,'Party appointment',None,None),
('Delhi Metropolitan Council member','1966–1970','Metropolitan institutional service; not a Delhi Assembly or chief-ministerial tenure.',[1],P1,'Metropolitan Council membership',None,None),
('Delhi Metropolitan Council chairman','1967–1970','Presided over the Council.',[1],P1,'Council chairmanship',None,None),
('Delhi Jana Sangh president','1970–1972','State party presidency concurrent with early Rajya Sabha service.',[2],P1,'Party selection',None,None),
('Rajya Sabha member: first term','1970–1976','First of four Upper House terms.',[1],P1,'Indirect election','1970-04-03','1976-04-02'),
('National Jana Sangh president','1973–1977, broad period','Party record gives February 1973 election and 1974/1975 re-elections; parliamentary summary uses 1973–1976. Exact boundaries remain unresolved.',[1,2],P1,'Party election',None,None),
('Rajya Sabha member: second term','1976–1982','Second Upper House term, spanning Janata government and BJP formation.',[1],P1,'Indirect election','1976-04-03','1982-04-02'),
('Janata Party general secretary','1977–1980','Party record identifies this organisational role.',[2],P1,'Party appointment',None,None),
('Union Information and Broadcasting Minister','1977–1979','Broadcasting and media portfolio in the Janata government.',[1],P1,'Cabinet appointment',None,None),
('Leader of House, Rajya Sabha','March 1977–July 1979 in biography','Parliamentary summary records the government leadership role; final month requires reconciliation with detailed handbooks.',[1],P1,'Government parliamentary leadership',None,None),
('Leader of Opposition, Rajya Sabha','January–April 1980','Brief Upper House opposition leadership in the parliamentary biography.',[1],P2,'Parliamentary recognition',None,None),
('BJP general secretary','1980–1986','National organisation during the party’s early years.',[1,2],P2,'Party appointment',None,None),
('Rajya Sabha member: third term','1982–1988','Third consecutive Upper House term.',[1],P2,'Indirect election','1982-04-03','1988-04-02'),
('BJP president: first period','May 1986–1991','Party biography dates the first presidency from May 1986.',[2],P2,'Party election',None,None),
('Rajya Sabha member: fourth term','1988–1989','Term ended with transition to Lok Sabha.',[1],P2,'Indirect election','1988-04-03','1989-11-27'),
('Lok Sabha MP: New Delhi','1989–1991','First Lower House term following personal election victory.',[1,6],P2,'Direct election',None,None),
('Leader of Opposition, Lok Sabha: early period','1989/1990–1993; starting boundary unresolved','Parliamentary biography lists 1989–1991 and 1991–1993; these summary ranges do not settle the formal recognition day. Use this as a broad role description.',[1],P2,'Parliamentary party leadership / recognition',None,None),
('Lok Sabha MP: Gandhinagar','1991–1996','Second Lok Sabha term; he won both Gandhinagar and New Delhi in 1991.',[1,7],P2,'Direct election',None,None),
('BJP president: second period','July 1993–May 1998','Non-consecutive return to party leadership.',[2],P2,'Party election',None,None),
('Lok Sabha MP: Gandhinagar','1998–1999','Third Lok Sabha term.',[1,8],P3,'Direct election',None,None),
('Union Home Minister: first NDA government','1998–1999','First NDA Home appointment is identified in an indexed parliamentary journal; precise oath day remains a research lead.',[18],P3,'Cabinet appointment',None,None),
('Lok Sabha MP: Gandhinagar','1999–2004','Fourth Lok Sabha term.',[1,9],P3,'Direct election',None,None),
('Union Home Minister: renewed NDA government','1999–2004','Parliamentary biography and ministry annual report confirm the portfolio.',[1,15],P3,'Cabinet appointment',None,None),
('Deputy Prime Minister','29 June 2002–2004','Appointed Deputy PM while retaining Home; this title did not constitute a separate elected mandate.',[19,15],P3,'Presidential appointment','2002-06-29',None),
('Coal and Mines: additional responsibility','Documented 23 July 2002','Lok Sabha minister label identifies additional charge of Coal and Mines. Exact start and end notifications not collected.',[35],P3,'Additional portfolio',None,None),
('Personnel portfolio','2003–2004','Parliamentary biography records Personnel, Public Grievances and Pensions responsibilities; exact allocation dates not collected.',[1],P3,'Additional portfolio',None,None),
('Lok Sabha MP: Gandhinagar','2004–2009','Fifth Lok Sabha term; parliamentary biography also records opposition leadership in this period.',[1,10],P4,'Direct election',None,None),
('Leader of Opposition, Lok Sabha','2004–2009','Opposition leadership after NDA loss; day-level appointment and cessation notifications remain to be inspected.',[1],P4,'Parliamentary recognition',None,None),
('BJP president: third period','October 2004–31 December 2005','Returned after Naidu; left at the end of 2005 following the Jinnah controversy.',[41,20],P4,'Party selection',None,'2005-12-31'),
('Lok Sabha MP: Gandhinagar','2009–2014','Sixth Lok Sabha term; personal victory coexisted with the BJP’s national defeat.',[1,10,28],P4,'Direct election',None,None),
('Lok Sabha MP: Gandhinagar','2014–2019','Seventh and last verified Lok Sabha term.',[1,10,26],P5,'Direct election',None,None),
('Margdarshak / senior mentor role','Later Modi era','Scholarly commentary describes the advisory elder role; exact appointment notice and powers not inspected.',[31],P5,'Party advisory / informal influence',None,None)]
for n,(title,period,finding,ids,phase,route,start,end) in enumerate(offices,1):
    ck={'Finding':ids}
    if start: ck['Start date']=[19] if n==26 else [1]
    if end: ck['End date']=[20] if n==31 else [1]
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':title,'Period':period,'Finding':finding,'Selection route':route,'Start date':start,'End date':end},ids,phase=phase,context=f'E{phases.index(phase)+1}02',checked=ck,status='Not reviewed' if n==23 else 'Supported',priority='High' if n==23 else 'Normal')

policies=[
('Broadcasting autonomy','The Janata-era process produced the 1979 Prasar Bharati bill, which retained more government direction than the Verghese group proposed and did not become law then.','Proposal / bill; lapsed with government','I&B Minister during the process; personal bill speech still awaiting full access','Do not credit him with establishing the later Prasar Bharati corporation.',[1,17],P1,'E106'),
('POTA','Moved the Prevention of Terrorism Bill in the 26 March 2002 joint sitting, defending exceptional powers against terrorism.','Parliamentary sponsorship / passage','Home Minister; leading sponsor','Opposition challenged safeguards and selective use; debate does not establish security effectiveness.',[16],P3,'E302'),
('POTA repeal and durability','The Prevention of Terrorism (Repeal) Act was enacted on 21 December 2004, after the NDA left office.','Later statutory repeal','Outcome of a later government; limits durability of his policy','Metadata establishes title and enactment date, not detailed savings provisions or case disposal.',[23],P4,'E402'),
('Uttar Pradesh reorganisation','Introduced the bill on 25 July 2000; Lok Sabha passed it on 1 August. The debate addressed Uttaranchal and disputed boundaries.','Introduction and Lower House passage','Ministerial sponsor of a collective legislative process','Regional movements, Parliament and other institutions also mattered; exact commencement not inferred.',[24,25],P3,'E309'),
('Central police modernisation','Ministry reported a five-year plan approved in February 2002 with an outlay of Rs 3,470 crore and Rs 1,080 crore spent by 31 March 2004.','Approved expenditure programme / reported spending','Home Minister responsible for the department','Expenditure is an input, not an independently evaluated improvement in security or rights.',[15],P3,'E304'),
('State police modernisation','The ministry described the inherited scheme, operating since 1969–1970, and revised arrangements approved in October 2003.','Revision of inherited programme','Minister overseeing a continuing scheme','Do not claim he originated state police modernisation; state implementation and outcomes require audits.',[15],P3,'E309'),
('Citizen registration and ID-card pilot','MHA reported an April 2003 pilot in 13 states/UTs and registration rules notified on 10 December 2003.','Pilot / rules','Home Minister; departmental programme','Planned coverage and expected completion are not verified completion. Later nationwide exercises are not backdated.',[15],P3,'E308'),
('Overseas citizenship framework','Ministry report records citizenship amendment notification on 8 January 2004 and related rules on 26 March 2004.','Legal and rules framework','Home portfolio responsibility','Overseas citizenship status is not full dual citizenship or parliamentary voting rights; implementation scope changed later.',[15],P3,'E305'),
('Hurriyat dialogue','Held talks with the Ansari-led faction on 22 January and 27 March 2004; ministry reported detention review recommendations, including 43 recommended releases by 31 March.','Meetings / confidence-building recommendations','Direct participant in talks','Recommendations are not confirmed releases; dialogue did not itself prove a durable Kashmir settlement.',[15],P3,'E305'),
('Disaster preparedness','The ministry described a shift toward preparedness, a programme across 17 states and 169 districts, and a proposed national emergency-management authority.','Programme / proposed institution','Home Minister associated with departmental reform','Do not describe the proposed authority as an already established statutory NDMA or infer reduced disaster mortality.',[15],P3,'E304'),
('Women’s political representation','In his December 1997 address, supported 33% reservation for women and said the commitment required more women candidates.','Advocacy / candidate-selection direction','Party president making a public commitment','No inspected nomination series measures implementation or isolates his effect.',[41],P2,'G07'),
('Post-Kargil national-security review','An official report associated with Advani’s Group of Ministers has been located, but its detailed recommendations and implementation have not been passage-reviewed.','Research lead','Role and follow-through require the full report','Do not claim that he implemented all review recommendations.',[37],P3,'E310'),
('2009 campaign programme','IPU describes the Advani-led BJP campaign as favouring tax reductions and stronger security.','Election proposals','National campaign leader','BJP did not form the Union government after this election; proposals are not government outcomes.',[28],P4,'E404')]
for n,(title,finding,stage,role,limit,ids,phase,ctx) in enumerate(policies,1):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':title,'Finding':finding,'Stage':stage,'Documented role':role,'Outcome / attribution limit':limit},ids,'Analysis',phase,ctx,status='Not reviewed' if n==12 else 'Supported',priority='High' if n==12 else 'Normal')

ideas=[
('Cadre and parliamentary organisation','RSS and Jana Sangh work, Delhi organisation, editorial activity and parliamentary office provided complementary channels of influence.',[1,2,5],P1,'E107'),
('Religious-nationalist mobilisation','The temple campaign and Rath Yatra joined symbolic religious geography to national party mobilisation. Violence and polarisation are central to critical assessments of this method.',[5,29],P2,'E208'),
('Coalition priorities and ideology','In October 2004, distinguished enduring ideology from immediate coalition priorities and acknowledged that Article 370 repeal, the temple and uniform civil code had not been in the NDA governance agenda.',[41],P4,'E407'),
('Integral humanism and economic language','His 2004 speech invoked Upadhyaya’s integral humanism while supporting decentralisation, deregulation, social justice and ecological restraint; these are stated principles, not an outcome evaluation.',[41],P4,'E404'),
('Basic services and federalism','In December 1997 urged attention to education, health, water, housing, maternal welfare and decentralisation, beyond a narrow markets-versus-state argument.',[41],P2,'E204'),
('Security and state capacity','POTA advocacy presented terrorism as an exceptional threat needing stronger powers; opposition warnings about rights and misuse constitute the contemporaneous competing position.',[16],P3,'E302'),
('Negotiation within a security agenda','The 2004 Hurriyat meetings show that direct political dialogue operated alongside policing and exceptional legislation; neither route alone captures his Home Ministry approach.',[15,16],P3,'E305'),
('Public credibility and resignation','In 2015 described his 1996 resignation and electoral absence as a conscience-driven choice. That is his account of motive, separate from the court’s evidentiary ruling.',[39,11],P2,'E202'),
('Learning from electoral defeat','His October 2004 speech warned the party against assuming a direct link between its claimed good governance and electoral success.',[41],P4,'E403'),
('Jinnah and ideological flexibility','The 2005 praise of Jinnah’s secular-state ideal generated resistance inside his political family. Scholarship reads the episode through tensions between coalition expansion and RSS ideology.',[20],P4,'E405'),
('Civil liberties and political opponents','The April 2019 blog advocated diversity, expression, internal democracy and respect for adversaries. Its claim that the BJP had always followed these principles is an attributed self-description.',[26],P5,'E506'),
('Gender and candidate selection','The December 1997 speech linked a reservation demand to a practical obligation to increase women nominees; actual selection and advancement still require independent data.',[41],P2,'G07')]
for n,(topic,finding,ids,phase,ctx) in enumerate(ideas,1):
    add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding,'Evidence type':'Identified records or attributed speech; see Evidence'},ids,'Analysis',phase,ctx)

controversies=[
('Ayodhya mobilisation and communal polarisation','Critics link the temple mobilisation to communal polarisation and violence; supporters regard it as political and cultural mobilisation. These assessments are distinct from proof of criminal conspiracy.','Political and historical assessment; contested','Advani’s 2004 speech reaffirmed the temple commitment and defended its political significance.',[5,29,41],P2,'E208','Political / social'),
('Liberhan Commission findings','The 2009 inquiry attributed political and ideological responsibility to Advani and other senior leaders. Reproduced conclusions reject the assumption that they were unaware of the movement’s plans.','Commission findings; not a criminal conviction','A complete contemporaneous personal response to the report has not been collected; his later trial response belongs to the separate criminal proceeding.',[14,40],P4,'E410','Commission inquiry'),
('Babri demolition criminal prosecution','Advani was among 32 accused acquitted by the special CBI court on 30 September 2020 for lack of conclusive evidence. The report records the judge’s rejection of a proven preplanned conspiracy.','Trial acquittal, 30 September 2020; full judgment not inspected','Accused denied wrongdoing; Advani welcomed the verdict as vindication of his commitment to the temple movement.',[12],P5,'E502','Criminal prosecution'),
('Appeal against Babri acquittal','Two appellants’ challenge was dismissed by Allahabad High Court because they lacked the required standing as victims.','Standing-based dismissal, 9 November 2022; not a fresh merits verdict','No new Advani response collected. This procedural outcome does not reclassify the inquiry’s findings as a criminal judgment.',[13],P5,'E502','Appeal procedure'),
('Jain hawala allegations','The prosecution relied on alleged payment entries. Supreme Court found no prima facie case against Advani on the material presented and dismissed CBI appeals on 2 March 1998.','Charge-stage disposition for evidentiary insufficiency; not a trial acquittal','Denied wrongdoing; resigned his Lok Sabha seat in 1996 and later said credibility motivated the decision.',[11,39],P2,'E202','Corruption allegation / court'),
('Gujarat 2002 accountability','Opposition and some NDA allies demanded stronger central action and Modi’s removal. The July parliamentary debate challenged relief, rehabilitation and the early-election decision.','Political and parliamentary scrutiny; no judicial finding about Advani is asserted here','Advani expressed shame over violence, rejected the state-sponsored characterization, allowed possible official errors and defended the election decision subject to the Election Commission.',[35,36],P3,'E302','Governance accountability'),
('Kandahar Cabinet recollections','Jaswant Singh’s 2009 account disputed Advani’s recollection about knowledge of the minister’s travel to Kandahar. The accounts do not resolve closed Cabinet deliberations.','Conflicting retrospective participant accounts; no adjudication asserted','Advani’s memoir portrayed the hostage release and prisoner exchange as a satisfactory resolution. This does not itself settle the separate knowledge dispute.',[21,22],P3,'E305','Security decision / recollection'),
('Jinnah remarks and BJP presidency','His 2005 Pakistan remarks praising Jinnah’s secular-state ideal provoked opposition within the RSS/BJP network and contributed to leadership conflict.','Political dispute; presidency ended 31 December 2005','Initially tendered a resignation that was withdrawn; later announced he would leave and did so at year-end.',[20],P4,'E405','Ideology / party leadership'),
('2013 succession protest','His resignation from key posts followed Modi’s elevation as campaign chief; RSS intervention and assurances preceded withdrawal.','Resignation 10 June; withdrawn 11 June 2013','Withdrew the resignation after intervention; the report does not establish all private motives.',[27],P4,'E407','Party succession')]
for n,(matter,finding,proc,response,ids,phase,ctx,cat) in enumerate(controversies,1):
    # Missing responses are explicit gaps rather than claims of silence or admissions.
    checked={'Finding':ids,'Procedural status':ids}
    if n not in (2,4): checked['Response']=([41] if n==1 else [12] if n==3 else [39] if n==5 else [35] if n==6 else [22] if n==7 else ids)
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Procedural status':proc,'Response':response,'Category':cat,'Latest-status limit':'Latest inspected event; not an exhaustive claim that no later proceedings exist.'},ids,'Analysis',phase,ctx,checked=checked,priority='High')

legacy=[
('Building a national alternative','Former associate Sudheendra Kulkarni credits the Vajpayee–Advani partnership with building a durable alternative to Congress. This is a favourable political assessment, qualified by collective agency and later party-system change.',[30],'Former associate / opinion','E501'),
('Organisation and democratic competition','Parliamentary service and party organisation provide an institutional basis for assessments of his influence; they do not establish that every strategy strengthened democratic practice.',[1,2,29],'Record-based synthesis','E201'),
('Polarisation and the temple movement','The Indian Express editorial links organisational success with communal polarisation. The inquiry and criminal case address different responsibility standards and cannot substitute for a social-impact study.',[29,14,12],'Critical editorial plus procedural distinction','E508'),
('Government and security legacy','Home Ministry records establish legislation, administration and talks. Independent evaluations are still needed to weigh security effects against rights costs and implementation failures.',[15,16,23],'Bounded governance synthesis','E310'),
('Coalition flexibility and its limits','The 2004 speech defends coalition priorities; the 2005 dispute shows limits imposed by ideological networks. Flexibility and ideological persistence coexist in the record.',[41,20],'Primary statement and scholarly assessment','E407'),
('Elder status and succession','Vinay Sitapati interprets later honouring of Advani as organisational respect despite succession conflict. Recognition does not measure his continuing control over party decisions.',[31,27],'Political scholar’s commentary','E507'),
('Democratic language in later life','The 2019 statement offers evidence of his expressed commitment to plural political debate; it is insufficient by itself to settle evaluations of his earlier mobilisation.',[26,29],'Primary statement and critical comparison','E506'),
('Institutional honours','Parliamentary biography records the Outstanding Parliamentarian award for 1999; the President conferred Bharat Ratna in March 2024. Honours record recognition, not consensus on the whole career.',[1,3,4],'Official recognition','E501'),
('Gender-related assessment','The women’s-reservation commitment and party organisational quota are identifiable evidence; nomination outcomes and the distribution of real authority remain unmeasured here.',[41,33],'Research limitation','G10')]
for n,(theme,assessment,ids,basis,ctx) in enumerate(legacy,1):
    add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor / basis':basis},ids,'Analysis',context=ctx)

from author_context import populate_context, coverage
populate_context(add,phases)
def gap(n,topic,detail,action,records,priority='Normal'):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':detail,'next_action':action,'status':'Open','record_ids':records})
gap(1,'Original 2004–2014 election returns','Three Gandhinagar results use a labelled secondary table; derived shares use explicit denominators.','Obtain ECI/CEO constituency returns and reconcile valid votes, NOTA and rejected ballots.',['EL10','EL11','EL12'],'High')
gap(2,'1991 Gandhinagar polling date','Official table date may retain an original schedule affected by postponement.','Compare the election notification and revised polling calendar; preserve verified counts.',['EL07'])
gap(3,'Rajya Sabha election allocations','Four terms verified; state allocations, exact election days and indirect vote detail not collected.','Inspect Rajya Sabha election and allocation notifications for 1970, 1976, 1982 and 1988.',['EL01','EL02','EL03','EL04'])
gap(4,'Office boundaries','Jana Sangh presidency, early Lok Sabha opposition recognition and minor portfolio boundaries need reconciliation.','Retrieve appointment/recognition notifications rather than reconciling incompatible summary years by guesswork.',['OF08','OF12','OF19','OF27','OF28','OF30'])
gap(5,'First Home appointment','Official June 1998 journal passage indexed, but full retrieval timed out.','Use a working parliamentary mirror or appointment gazette for exact first oath and portfolio dates.',['OF23'],'High')
gap(6,'Babri primary judicial record','Trial and 2022 appeal outcomes rely on careful reporting; full judgments not inspected.','Retrieve signed trial judgment and High Court order; check subsequent docket developments.',['CV03','CV04'],'High')
gap(7,'Full Liberhan report and response','Commission excerpts have a shared origin; full report and complete Advani response absent.','Collect original report paragraphs and contemporaneous response; retain distinction from criminal case.',['CV02'],'High')
gap(8,'Security review implementation','2001 GoM report located but recommendations and implementation not read.','Obtain readable original report and subsequent implementation/audit records.',['PG12'],'High')
gap(9,'Broadcasting sponsorship','1979 bill history verified; Advani’s original Rajya Sabha speech retrieval returned HTML.','Use parliamentary archive scan to establish detailed sponsorship and responses.',['PG01'])
gap(10,'Independent governance outcomes','Ministry reports establish actions and inputs, not independent effectiveness.','Collect audits and contemporary evaluations of policing, POTA, citizenship pilots, disaster work and dialogue.',['PG02','PG05','PG06','PG07','PG08','PG09','PG10'],'High')
gap(11,'Gender mechanisms and outcomes','Reservation advocacy verified; personal effects on access, nominations and power unmeasured.','Compare contemporaneous candidate selection and advancement with appropriate male/female cohorts.',['G01','G04','G05','G06','G09','G10'])
gap(12,'Early economic and international context','Specific links from broad conditions to early decisions remain thin.','Add period scholarship and contemporary records before making causal claims.',['E104','E105','E205'])
gap(13,'Kandahar knowledge dispute','Conflicting retrospective accounts do not settle Cabinet discussions.','Retrieve contemporaneous records and complete interviews; keep participant accounts attributed.',['CV07'])
gap(14,'Social coalition and constituency comparison','No matched voter study or boundary-adjusted vote series collected.','Add delimitation maps and constituency studies before inferring changes in social-group support.',['E208','E209','E408','E509'])
gap(15,'2008 reservation speech lead','Financial Express index located but full passage failed; earlier 1997 primary advocacy is verified.','Revisit only with a working archive if exact 2008 wording is needed.',['G07'])

base=Path(__file__).parent
data={'schema_version':1,'subject':'L. K. Advani','as_of':ASOF,'guidance':'Ten gender dimensions cover the career; ten era dimensions are examined in each of five phases. Context informs interpretation without excusing conduct or assuming causation. A supported field is passage-reviewed, not a claim that every surrounding field is independently verified. See open research gaps.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
