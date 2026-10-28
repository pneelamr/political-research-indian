"""Rebuild the Jayalalithaa research snapshot and field-level evidence register."""
import hashlib,json
from pathlib import Path
from author_sources import ASOF,sources,retrievals
P1='P1 | Formation and succession (1948–1988)'
P2='P2 | Opposition and first government (1989–1996)'
P3='P3 | Coalitions, return and opposition (1997–2010)'
P4='P4 | Welfare expansion and final governments (2011–2016)'
phases=[P1,P2,P3,P4]
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
    if typ!='Method / scope': row['Corroboration']='See field evidence; independent origins are identified in Sources.'
    tables[name]['rows'].append(row)
    if typ=='Method / scope': return row
    if checked is None: checked={k:ids for k in fields if k in ('Finding / value','Finding','Description','Assessment')}
    for field,support in checked.items():
        support=[f'S{s:03d}' if isinstance(s,int) else s for s in support]
        cid=f"C-{rid}-{sum(c['record_id']==rid for c in claims)+1:02d}"
        actual=status if all(s in R for s in support) else 'Not reviewed'
        evs=[]
        if actual=='Supported':
            for sid in support:
                ret=R[sid];eid=f'EV-{len(evidence)+1:04d}';evs.append(eid)
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':ret['id'],'locator':ret['locator'],'passage_paraphrase':ret['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex: inspected-passage review','reviewed_at':ASOF,'note':'Sources jointly support this registered field; interpretation remains attributed or explicitly analytical. Unregistered neighbouring fields are not certified.'})
        val=row[field]
        claims.append({'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':val,'fingerprint':hashlib.sha256(json.dumps(val,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':typ,'status':actual,'priority':priority,'candidate_source_ids':support,'evidence_ids':evs,'contradictions':[],'review_note':note or ('Bounded synthesis of inspected evidence.' if typ=='Analysis' else 'Support applies only to this registered field and its qualifications.')})
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
def ov(n,topic,finding,ids,typ='Recorded fact',**kw): return add('Overview',f'OV{n:02d}',{'Topic':topic,'Finding / value':finding},ids,typ,**kw)
ov(1,'Identity','J. Jayalalithaa; also Jayaram Jayalalithaa, Jayalalitha and Jaya. Born 24 February 1948; died 5 December 2016. “Amma” is a political honorific, not a formal office.',[1,5],checked={'Finding / value':[1,5]},note='Common aliases identify the subject. No separate legal-name certificate was inspected.')
ov(2,'Geography and formation','Born in the Mysore region, educated in Bengaluru and Chennai, and prominent in cinema before entering Tamil Nadu politics. Exact birth locality remains unresolved.',[1,3,4],'Analysis')
ov(3,'Party and political career','Joined AIADMK in 1982. MGR’s mentorship helped entry; the succession struggle after his death required her to establish a separate organisational and electoral claim.',[1,4,5],'Analysis',context='G01; G03')
ov(4,'Principal offices','Rajya Sabha member, April 1984–January 1989; Assembly member from several constituencies; twice Leader of Opposition; dominant AIADMK leader and Chief Minister across six ministries.',[2,3,4],'Analysis')
ov(5,'Six ministries, five continuous spells','The official Assembly list records six ministries beginning in 1991, 2001, 2002, 2011, 2015 and 2016. The last two were consecutive. The 2001 appointment was judicially invalidated.',[2,6],'Analysis',priority='High')
ov(6,'Personal electoral record','Nine Assembly constituency contests are recorded: eight wins and the 1996 Bargur defeat. The two 1991 victories count separately as contests. The 2001 rejected nominations are not polling defeats.',[23,24,25,26,27,28,29,42,6],'Analysis',priority='High')
ov(7,'Welfare and institutions','Cradle Baby Scheme, Amma canteens, drug procurement and rainwater-harvesting requirements provide distinct policy mechanisms. Their existence does not establish sole personal responsibility for statewide social gains.',[11,12,14,36],'Analysis')
ov(8,'Economy beyond welfare','Vision 2023 set infrastructure and growth ambitions. The workbook treats those as plans and targets, with implementation and independent outcome assessment still incomplete.',[37],'Analysis')
ov(9,'Social justice and federal claims','Her government defended the existing 69% reservation arrangement; Parliament supplied Ninth-Schedule protection. Water litigation and Sri Lankan Tamil demands show state-level pressure on wider institutions.',[16,21,33],'Analysis')
ov(10,'Political method','Cinema-derived recognition, centralised party authority, changing alliances and the maternal “Amma” identity combined with visible benefits. These mechanisms require separate evidence, rather than one personality-based explanation.',[4,5,19,38],'Analysis')
ov(11,'Gender and representation','First woman Leader of Opposition in Tamil Nadu, but not its first woman Chief Minister: Janaki preceded her. A 2016 survey found stronger AIADMK support among women; that is not proof of gender equality within the party.',[1,2,38],'Analysis',context='G02; G09')
ov(12,'Legal record','TANSI acquittal coexists with judicial criticism of conflicts of interest. The 2014 assets conviction and 2015 acquittal preceded the 2017 judgment: appeals against her abated on death; surviving co-accused were convicted.',[7,8,39],'Analysis',priority='High')
ov(13,'Governance and accountability','Mass employee dismissals, contested welfare spending and the 2015 floods raise distinct legal, fiscal and administrative questions. None should be collapsed into an undifferentiated corruption label.',[9,43,41],'Analysis')
ov(14,'Legacy and its limits','Electoral resilience and durable welfare institutions coexist with criticism of concentrated authority and inadequate succession. Supportive and critical assessments are attributed on the Legacy sheet.',[5,12,13,40],'Analysis')
ov(15,'Research scope','Snapshot dated 26 October 2026. Main career ends in 2016; the 2017 assets judgment is reviewed. The 2022 death-inquiry material remains a limited research lead, with later disposition unverified.',[],'Method / scope')
ov(16,'Evidence guide','Supported means the registered field has passage support or a bounded synthesis. It does not certify every cell, primary-source access, causation or completeness. Search excerpts remain unreviewed. Expand supporting columns and follow All citations and Claims.',[],'Method / scope')
ov(17,'Numerical guide','Election numbers are votes, not thousands. Negative signed margin means a loss. Blank shares mean no checked denominator; they do not mean zero. Different seats, boundaries and the 2015 opposition boycott limit comparisons.',[],'Method / scope')
ov(18,'Open priorities','Original election returns; precise party/opposition-office boundaries; full flood audit and death-inquiry records; Tamil-language archives; and independent policy outcomes remain on the Research Queue.',[],'Method / scope')

events=[
('24 February 1948','Birth','Born in the Mysore region; exact locality is not reconciled.',[1],P1,'1948-02-24'),
('School years–film career','Education and cinema','Schooling in Bengaluru and Chennai preceded a prolific screen career, which created a route to MGR and public recognition.',[1,4],P1,None),
('1982','Joins AIADMK','Entered AIADMK under MGR’s leadership.',[1],P1,None),
('1980s','Propaganda and campaigning','Served as a propaganda organiser and campaigned during MGR’s illness; exact appointment and removal boundaries remain open.',[4,5],P1,None),
('April 1984','Rajya Sabha','Began representing Tamil Nadu in the upper house.',[3],P1,None),
('1987–1989','Contested succession','MGR’s death was followed by rival Jayalalithaa and Janaki claims; electoral competition helped resolve leadership.',[4,5],P1,None),
('1989','First Assembly victory','Won Bodinayakkanur and became the state’s first woman opposition leader.',[1,23],P2,None),
('25 March 1989','Assembly violence','Clashes during the budget session became a defining political memory; the specific sari-pulling allegation remains disputed.',[22],P2,'1989-03-25'),
('June 1991','Two seat victories and first ministry','Won Bargur and Kangayam; first sworn as CM on 24 June.',[24,2],P2,'1991-06-24'),
('1992','Cradle Baby Scheme','Introduced in Salem as a surrender-and-adoption alternative to female infanticide.',[11],P2,None),
('1994–1995','Medical procurement institution','TNMSC incorporated in July 1994 and began drug procurement operations in January 1995.',[36],P2,None),
('1994','Reservation protection','State legislation and Union constitutional amendment protected the existing 69% arrangement.',[16],P2,None),
('1996','Electoral defeat','Lost Bargur to E.G. Sugavanam; her first ministry ended on 12 May.',[25,2],P2,None),
('14 April 1999','Withdraws national support','Submitted withdrawal of AIADMK support to the President; formal party influence, not a Union office held personally.',[19],P3,'1999-04-14'),
('May–September 2001','Invalidated appointment','Sworn CM on 14 May; Supreme Court quashed appointment on 21 September because she was disqualified.',[6],P3,'2001-05-14'),
('February–March 2002','Andipatti and return','Won the Andipatti by-election and began a new ministry on 2 March.',[26,2],P3,'2002-03-02'),
('2003','Rainwater harvesting','Compulsory harvesting provisions applied to old and new buildings; measured lasting effects require further study.',[14,15],P3,None),
('July–August 2003','Employee strike confrontation','Mass dismissals reached the Supreme Court; reinstatement and individual review arrangements followed.',[9],P3,None),
('24 November 2003','TANSI acquittal sustained','Supreme Court dismissed appeals against acquittal while criticising the transactions’ ethical implications.',[7],P3,'2003-11-24'),
('2006','Assembly win, government change','Retained Andipatti; CM term ended 12 May.',[27,2],P3,None),
('2011','Return to government','Won Srirangam and began the fourth ministry on 16 May.',[28,2],P4,'2011-05-16'),
('2012','Vision 2023','Government articulated a strategic infrastructure and economic-development plan.',[37],P4,None),
('19 February 2013','Amma canteens','First Chennai centres opened; subsequent expansion reached all 200 municipal wards that April.',[12],P4,'2013-02-19'),
('27 March 2013','Sri Lanka resolution','Moved Assembly demands for international investigation, sanctions and an Eelam referendum.',[33],P4,'2013-03-27'),
('7 May 2014','Mullaperiyar judgment','Supreme Court upheld Tamil Nadu’s position on restoration to 142 feet with supervision.',[21],P4,'2014-05-07'),
('27 September 2014','Conviction interrupts office','Trial conviction in the assets case cost her the CM post and Srirangam seat.',[2,39],P4,'2014-09-27'),
('May–June 2015','Acquittal and return','High Court acquittal preceded return as CM on 23 May and victory at RK Nagar.',[8,2,39],P4,'2015-05-23'),
('December 2015','Chennai floods','Disaster management later attracted adverse audit findings; the full audit remains an access gap.',[41],P4,None),
('May 2016','Consecutive election victory','AIADMK retained government; Jayalalithaa retained RK Nagar and took the oath again on 23 May.',[40,42,2],P4,'2016-05-23'),
('5 December 2016','Death in office','Died in Chennai; the formal official death date is used even though later inquiry narratives generated disputes.',[1],P4,'2016-12-05'),
('14 February 2017','Posthumous appellate disposition','Appeals against her abated; the Supreme Court restored conviction and sentence of surviving co-accused.',[8],P4,'2017-02-14')]
for n,(period,event,desc,ids,phase,day) in enumerate(events,1):
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':day,'Date precision':'Exact event date' if day else 'Year or range'},ids,'Analysis',phase,f'E{phases.index(phase)+1}02')

elections=[
(1984,'Rajya Sabha / indirect','Tamil Nadu','Elected',None,None,None,None,[3],P1,'Legislator-vote total unavailable; no popular vote share.'),
(1989,'Assembly / direct','Bodinayakkanur','Won',57603,'Muthu Manoharan','DMK',28872,[23],P2,'AIADMK Jayalalithaa faction, labelled ADK(JL). Secondary table has an erroneous gender field, not adopted.'),
(1991,'Assembly / direct','Bargur','Won',67680,'T. Rajhendher (T. Rajendar)','TMK',30465,[24],P2,'One of two simultaneous constituency wins; no checked valid-vote denominator.'),
(1991,'Assembly / direct','Kangayam','Won',69050,'N.S. Rajkumar Mandradiar','DMK',35759,[24],P2,'Second seat in same election; later by-election shown in source. Not a separate ministry.'),
(1996,'Assembly / direct','Bargur','Lost',50782,'E.G. Sugavanam','DMK',59148,[25],P2,'Margin is candidate minus opponent, hence negative.'),
(2001,'Assembly / nominations','Multiple seats','Nominations rejected',None,None,None,None,[6],P3,'Not a completed personal polling contest. The party could form government despite her disqualification.'),
(2002,'Assembly / by-election','Andipatti','Won',78437,'DMK nominee (Vaigai Sekar)','DMK',37236,[26],P3,'Opponent count derived: 78,437 minus reported margin 41,201. Published totals disagree; share withheld.'),
(2006,'Assembly / direct','Andipatti','Won',73927,'Seeman','DMK',48741,[27],P3,'Do not conflate this DMK opponent with the later NTK leader; primary return pending.'),
(2011,'Assembly / direct','Srirangam','Won',105328,'N. Anand','DMK',63480,[28],P4,'Post-delimitation constituency; secondary table misnumbers the seat. Only the named seat and candidate counts adopted.'),
(2015,'Assembly / by-election','Dr. Radhakrishnan Nagar','Won',160432,'C. Mahendran','CPI',9710,[29,39],P4,'Major parties including DMK stayed away. Share uses 181,420 total including NOTA.'),
(2016,'Assembly / direct','Dr. Radhakrishnan Nagar','Won',97218,'Shimla Muthuchozhan','DMK',57673,[42,30],P4,'2016-labelled result only; denominator not independently checked, share withheld.')]
for n,(year,route,seat,result,v,opp,party,ovotes,ids,phase,limit) in enumerate(elections,1):
    supported=[42] if year==2016 else ids
    fields={'Year':year,'House / route':route,'Constituency':seat,'Result':result,'Candidate votes':v,'Principal opponent':opp,'Opponent party':party,'Opponent votes':ovotes,'Signed vote margin':None,'Vote share':160432/181420 if year==2015 else None,'Share denominator':181420 if year==2015 else None,'Party / alliance':'AIADMK (Jayalalithaa faction)' if year==1989 else 'AIADMK','Counting and geography note':limit}
    check={k:supported for k in ('Result','Candidate votes','Opponent votes') if fields[k] is not None}
    if year==2015: check['Vote share']=[29]
    add('Elections',f'EL{n:02d}',fields,ids,'Recorded fact',phase,f'E{phases.index(phase)+1}03',checked=check,note=limit,priority='High')

offices=[
('Member, Rajya Sabha','April 1984–January 1989','Indirectly elected representative for Tamil Nadu; exact entry and resignation days need the membership register.',[3],P1,None,None,'Legislative'),
('AIADMK propaganda organiser','1980s','Propaganda secretary and campaigner under MGR; interrupted appointment boundaries have not been established.',[4,5],P1,None,None,'Party'),
('AIADMK leader / general secretary','Late 1980s–2016','Consolidated leadership after the succession conflict; party authority persisted through electoral and judicial setbacks. Exact formal appointment intervals remain open.',[4,5,39],P2,None,None,'Party'),
('Leader of Opposition, Tamil Nadu','1989','First opposition-leadership spell; exact boundaries within the ninth Assembly remain unverified.',[1,3],P2,None,None,'Legislative'),
('Chief Minister, first ministry','24 June 1991–12 May 1996','First executive term, after the 1991 election; ended in electoral defeat.',[2,25],P2,'1991-06-24','1996-05-12','Executive'),
('Chief Minister, second ministry','14 May–21 September 2001','Appointment quashed as constitutionally invalid; otherwise lawful governmental acts preserved by the court.',[2,6],P3,'2001-05-14','2001-09-21','Executive; appointment invalidated'),
('Chief Minister, third ministry','2 March 2002–12 May 2006','Returned following Andipatti victory; a distinct ministry after the Panneerselvam interlude.',[2,26],P3,'2002-03-02','2006-05-12','Executive'),
('Chief Minister, fourth ministry','16 May 2011–27 September 2014','Returned after 2011 election; assets conviction interrupted executive and legislative office.',[2,39],P4,'2011-05-16','2014-09-27','Executive'),
('Chief Minister, fifth ministry','23 May 2015–21 May 2016*','Returned after High Court acquittal. End date follows Assembly list; other summaries use 22 May or continuous service.',[2,8],P4,'2015-05-23','2016-05-21','Executive'),
('Chief Minister, sixth ministry','23 May–5 December 2016','New oath following re-election; died in office.',[2,1,40],P4,'2016-05-23','2016-12-05','Executive'),
('Member, Tamil Nadu Assembly','1989–1991','Bodinayakkanur seat in the ninth Assembly; exact membership boundaries need the official register.',[23],P2,None,None,'Legislative'),
('Member, Tamil Nadu Assembly','1991–1996','Won Bargur and Kangayam; subsequent Kangayam by-election and Bargur recontest establish the retained electoral base. Seat-vacation day remains open.',[24,25],P2,None,None,'Legislative'),
('Member, Tamil Nadu Assembly','2002–2006','Andipatti by-election restored membership during the twelfth Assembly.',[26,2],P3,None,None,'Legislative'),
('Member, Tamil Nadu Assembly','2006–2011','Re-elected in Andipatti for the thirteenth Assembly; exact legislative boundaries require notifications.',[27,2],P3,None,None,'Legislative'),
('Leader of Opposition, Tamil Nadu','2006–2011 period','Second opposition-leadership spell. The institutional obituary confirms two spells; exact start/end dates remain unverified.',[3,5],P3,None,None,'Legislative'),
('Member, Tamil Nadu Assembly','2011–2014','Srirangam membership ended following the assets conviction and disqualification.',[28,39],P4,None,None,'Legislative'),
('Member, Tamil Nadu Assembly','2015–2016 Assembly transition','RK Nagar by-election restored membership; sworn MLA in July 2015.',[39],P4,None,None,'Legislative'),
('Member, Tamil Nadu Assembly','2016','Retained RK Nagar at the general election; died while in office.',[42,1],P4,None,None,'Legislative')]
for n,(title,period,finding,ids,phase,start,end,cat) in enumerate(offices,1):
    f={'Position / institution':title,'Period':period,'Finding':finding,'Start date':start,'End date':end,'Position category':cat,'Jurisdiction':'Tamil Nadu / India' if n==1 else 'Tamil Nadu'}
    ck={'Finding':ids}
    if start: ck.update({'Start date':[2],'End date':[2]})
    add('Offices & Party',f'OF{n:02d}',f,ids,'Analysis',phase,f'E{phases.index(phase)+1}02',checked=ck,priority='High')

policies=[
('Cradle Baby Scheme','Introduced in Salem in 1992, with surrender and adoption intended to prevent female infanticide.','Implemented',[11],P2,'Government initiative during first term','Scholars find a possible contribution, not sole causation; follow-up and son-preference concerns remain.'),
('Amma Unavagam','Chennai canteens launched in February 2013 and reached all 200 wards by April; women’s groups operated the centres.','Implemented',[12],P4,'Launched and expanded under her government','Low prices establish an affordability mechanism; no independent nutrition or poverty effect is estimated.'),
('Rainwater harvesting','Compulsory provision for existing and new buildings became a prominent 2003 intervention.','Adopted / implemented',[14,15],P3,'Government requirement associated with her direction','Compliance, maintenance, rainfall and other water investments complicate outcome attribution.'),
('Essential-drug procurement','TNMSC incorporated on 1 July 1994 and began purchase, storage and distribution in January 1995.','Institution operating',[36],P2,'Established during her government','Health administrators and later governments also shaped the institution; universal drug availability is not inferred.'),
('69% reservation protection','State legislation and the 76th constitutional amendment preserved an existing reservation arrangement.','Legislation adopted',[16],P2,'State government pursued protection; Parliament amended Constitution','Multiple parties and Union institutions participated. No claim that she originated the quota or removed all future review.'),
('Vision 2023','Infrastructure strategy sought around 11% real annual GSDP growth and major sectoral investment.','Plan / targets',[37],P4,'Government strategy with chief-ministerial sponsorship','Targets are not realised growth. Project-level execution and fiscal evaluation are open.'),
('2011 household and student benefits','Court record documents appliance and laptop promises and subsequent procurement steps.','Promises plus procurement',[43],P4,'AIADMK pledge and state implementation','Procurement does not establish completion, beneficiary quality or educational effects.'),
('Employee-strike response','Government dismissed striking employees in 2003; litigation recorded reinstatement and review arrangements.','Administrative action / court review',[9],P3,'Government labour policy and litigation','Government employees’ right-to-strike holding is distinct from fairness of each individual sanction.'),
('Mullaperiyar litigation','2014 judgment permitted restoration to 142 feet under a supervisory committee.','Judicial relief',[21],P4,'State pursued long-running litigation','Outcome depended on prior litigation, technical evidence and court authority; no current safety conclusion.'),
('Sri Lankan Tamil demands','2013 Assembly resolution sought international investigation, embargo and an Eelam referendum.','Resolution / demand',[33],P4,'Personally moved resolution','Foreign-policy execution lay with Union institutions; no sanctions or referendum outcome is attributed to her.'),
('All-women police stations','Her speeches describe women-staffed stations begun in 1992 and intended to improve women’s access to policing.','Attributed programme claim',[32],P2,'Publicly advocated and claimed government implementation','Exact chronology and outcomes require police records; national/world first claims are withheld.'),
('Anti-conversion policy and reversal','2002 restriction and a reported 2004 withdrawal form a policy reversal; formal repeal chronology needs checking.','Enactment / reported reversal',[17,18],P3,'Government legislation and subsequent announced reversal','Minority criticism and stated religious-harmony rationale should be assessed with original debate and repeal records.'),
('2015 flood management','Reporting on CAG audit criticises reservoir management; government attributed the disaster to exceptional rainfall.','Post-tenure audit criticism',[41],P4,'Executive accountability for state agencies','Full audit, technical exhibits and agency responses remain open; no personal criminal responsibility established.')]
for n,(topic,finding,stage,ids,phase,role,limit) in enumerate(policies,1):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':topic,'Finding':finding,'Stage':stage,'Documented role':role,'Outcome / attribution limit':limit},ids,'Analysis',phase,f'E{phases.index(phase)+1}04',priority='High' if n in (1,11,12,13) else 'Normal')

ideas=[
('Cinema to organisation','Public recognition and MGR’s patronage created access; campaigning and succession conflict show that celebrity did not automatically supply authority.',[4,5],P1),
('Dravidian legitimacy','Editorial interpretation links Tamil identity, social justice and welfare to her political claims despite a background different from the movement’s dominant anti-Brahmin tradition.',[4,5,16],P2),
('Maternal identity','“Amma” personalised state provision through a protective maternal image; survey evidence of women’s support is a separate empirical question.',[5,12,38],P4),
('Centralised leadership','Journalistic assessments describe intense loyalty and limited internal dissent. They criticise the shortage of an independent second rank; this is interpretation, not a party-wide survey.',[4,5],P4),
('Coalition bargaining','Withdrawal of support in 1999 illustrates regional-party leverage in a coalition at the Centre; her demands did not confer constitutional authority to appoint a Union government.',[19],P3),
('Welfare competition','The 2013 Balaji judgment records competitive distribution promises by both DMK and AIADMK; institutional incentives extended beyond one leader.',[43],P4),
('Federal assertion','Water litigation used courts; Sri Lankan Tamil resolutions pressed the Union. Legal relief and political demand are distinct instruments.',[21,33],P4),
('Electoral social base','2016 survey analysis reports stronger female support across several demographic groups. It cautions against treating welfare or leadership credibility alone as a complete explanation.',[38],P4)]
for n,(topic,finding,ids,phase) in enumerate(ideas,1): add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding,'Evidence type':'Attributed interpretation or bounded synthesis'},ids,'Analysis',phase,f'E{phases.index(phase)+1}07')

matters=[
('1989 Assembly violence','Violence is documented; the specific allegation that her sari was pulled is disputed by DMK and later witnesses.','Political allegation and conflicting witness accounts','Jayalalithaa alleged assault and tearing of her sari; Duraimurugan and DMK denied the allegation.',[22],P2),
('TANSI transactions','Supreme Court sustained acquittal while condemning conflicts between public office and private purchase.','Acquittal sustained, 24 November 2003','Defence disputed criminal liability; acquittal does not cancel the court’s separate ethical criticism.',[7],P3),
('2001 CM appointment','Disqualification made the appointment invalid even with legislative majority support.','Appointment quashed, 21 September 2001','Defence relied on gubernatorial appointment and majority support; the court rejected this basis.',[6],P3),
('Disproportionate assets','2014 conviction was followed by 2015 acquittal; in 2017 appeals against her abated while co-accused convictions were restored.','Appeals against deceased Jayalalithaa abated; merits discussion remains','She challenged conviction and secured High Court acquittal during life. Death prevented final appellate relief against her.',[8,39],P4),
('2003 employee dismissals','Court recorded mass dismissals and arrangements for reinstatement or individual review.','Constitutional ruling and remedial arrangements','State agreed to reinstatement for categories of staff subject to undertakings; exceptions were reviewed separately.',[9],P3),
('Public spending on election promises','Petitioner challenged distribution schemes; court did not treat manifesto promises as corrupt practices under the law then in force.','2013 challenge rejected; ECI directed to frame guidelines','Government defended schemes through welfare purposes, eligibility rules and legislative approval.',[43],P4),
('2015 floods','DT Next reports audit criticism of reservoir operations and the government’s exceptional-rainfall explanation.','Audit criticism reported in 2018; original audit not fully inspected','Government attributed the deluge to unprecedented rainfall; the reported audit challenged administrative preparedness.',[41],P4),
('Posthumous death inquiry','2022 reports describe commission criticism and Sasikala’s denial; separate AIIMS reporting points toward medically appropriate care.','Research lead: inquiry findings and competing medical report; later disposition unverified','Sasikala denied interference and offered to face inquiry. No criminal finding or medical conclusion is certified here.',[34,35],P4),
('Anti-conversion law','A 2002 restriction and 2004 announced reversal raise questions about minority rights and policy consistency.','Legal and political controversy; repeal chain unreviewed','Reported government rationale was religious harmony; reversal was presented as responsiveness to minority concerns.',[17,18],P3)]
for n,(matter,finding,proc,response,ids,phase) in enumerate(matters,1):
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Procedural status':proc,'Subject / party response':response,'Status scope':'Latest inspected disposition stated; no exhaustive subsequent-litigation search claimed.'},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',checked={'Finding':ids,'Procedural status':ids,'Subject / party response':ids},priority='High')

legacy=[
('Electoral resilience','Eight wins across nine constituency contests, judicial interruptions and the 2016 return distinguish personal popularity from uninterrupted incumbency.',[23,24,25,26,27,28,29,42,2],'Workbook synthesis from election and office records'),
('Durable welfare delivery','Canteen institutions and procurement systems offer observable legacies; delivery, institutional survival and effects on welfare require different measures.',[12,13,36],'Administrative history and bounded synthesis'),
('Gender and agency','Survey evidence of women’s support strengthens the account of political identification. It does not establish that all women shared interests or gained equivalent organisational authority.',[38,5],'Survey analysts and editorial interpretation'),
('Institutional accountability','TANSI ethical criticism, the invalidated 2001 appointment and the assets-case disposition demand legal precision alongside electoral assessment.',[7,6,8],'Judicial record'),
('Power and succession','Indian Express’s editorial credits hard-won authority while criticising personality-centred leadership and lack of a strong second rank.',[5],'Attributed editorial assessment'),
('Protective welfare and its limits','Srinivasan and Bedi see a continuing role for surrender-based protection while warning about weak follow-up and the underlying devaluation of daughters.',[11],'Attributed scholarly assessment'),
('Growth ambition versus outcome','Vision 2023 broadens the record beyond subsidies, but its numerical ambitions cannot be substituted for an audited record of achievement.',[37],'Primary plan interpreted with attribution limits'),
('Memory and contested narratives','The 1989 clash and the posthumous inquiry show how political memory remains disputed. Later repetition cannot substitute for original records or adjudication.',[22,34,35],'Research limitation')]
for n,(theme,assessment,ids,assessor) in enumerate(legacy,1): add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor / basis':assessor},ids,'Analysis')

from author_context import populate_context,coverage
populate_context(add,phases)
def gap(n,topic,detail,action,records,priority='Normal',status='Open'):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':detail,'next_action':action,'status':status,'record_ids':records})
gap(1,'Original election returns','Historical vote counts use labelled secondary or contemporary-news fallbacks. Most shares are withheld.','Obtain ECI/CEO reports and Form 20; reconcile denominators, NOTA and postal votes.',['EL02','EL03','EL04','EL05','EL07','EL08','EL09','EL10','EL11'],'High')
gap(2,'2002 by-election arithmetic','Opponent count is derived; published totals and percentages conflict.','Inspect final Andipatti return rather than early counting reports.',['EL07'],'High')
gap(3,'Office boundaries','Exact Rajya Sabha days, propaganda-secretary interruptions, general-secretary selection and opposition-leader boundaries remain unresolved.','Inspect membership registers, Assembly bulletins and party resolutions.',['OF01','OF02','OF03','OF04'],'High')
gap(4,'2016 ministry boundary','Assembly list ends fifth ministry 21 May; summaries differ. No one-day vacancy inferred.','Check resignation acceptance, caretaker arrangements and oath notifications.',['OF09','OF10'],'High')
gap(5,'Flood audit','Canonical PDF returned 404; detail page failed. Secondary account inspected.','Retrieve full Report 4 of 2017, paragraph 5.8.5, technical annexes and government replies.',['PG13','CV07'],'High')
gap(6,'Death inquiry and later proceedings','Only limited 2022 reports collected, including conflicting medical and commission views.','Obtain full commission report, AIIMS panel report, responses and subsequent orders through cutoff.',['CV08','LA08'],'High')
gap(7,'Women’s policing','Speech excerpt only; first-station month and programme effects unresolved.','Inspect police policy notes and independent complaints/outcomes research; check Kerala precedent before national-first language.',['PG11','G07'],'High')
gap(8,'Religious-conversion repeal chain','2002 act, 2004 announcement and reported 2006 legislative dispute require primary reconciliation.','Retrieve original ordinance, repeal act and Assembly debate; separate political announcement from legal effect.',['PG12','CV09'],'High')
gap(9,'Independent welfare outcomes','Canteen, procurement, harvesting and laptop evidence is stronger on mechanisms than causal effects.','Collect audits, budgets, beneficiaries’ experience and independent evaluations across governments.',['PG02','PG03','PG04','PG07'],'High')
gap(10,'Economic delivery','Vision 2023 is a plan; state growth and infrastructure outcomes not independently evaluated.','Compare targets with consistent GSDP series and project-level audit, accounting for later governments.',['PG06','LA07'])
gap(11,'National coalition chronology','Formal withdrawal is checked, but original parliamentary narrative and confidence division remain unread.','Retrieve September 1999 JPI and 17 April Lok Sabha proceedings.',['TL14','IM05'],'High')
gap(12,'Social and gender mechanisms','Recruitment, women’s authority, caste-specific distribution and comparative media treatment lack matched data.','Extend Tamil-language archive work, women’s organisations and candidate-selection studies.',['G04','G05','G09'])
gap(13,'First-phase context','Economic and international influences on early choices remain unestablished.','Add period scholarship without projecting later policies onto her youth.',['E104','E105'])
gap(14,'Additional governance and controversies','Cauvery notification, tsunami recovery, TASMAC retail, press-defamation cases, 2001 Karunanidhi arrest and other criminal cases need dedicated original records.','Expand using budgets, judgments and Assembly debates; avoid treating this snapshot as exhaustive.',['OV18'],'High')
gap(15,'Birthplace and names','Broad Mysore used; exact village and name variants require stronger civil or archival evidence.','Reconcile institutional biographies with original records; retain public initials.',['OV01','OV02'])

base=Path(__file__).parent
data={'schema_version':1,'subject':'J. Jayalalithaa','as_of':ASOF,'guidance':'Four career phases; ten era dimensions per phase and ten gender dimensions across the career. Recorded fact, attributed statement, analysis and uncertainty remain distinct. Supported refers to registered fields only. Search excerpts remain unreviewed. Original returns and other gaps are listed in Research Queue.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
