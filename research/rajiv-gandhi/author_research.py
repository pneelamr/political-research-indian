"""Rebuild Rajiv Gandhi research records; use the shared workbook builder next."""
import hashlib, json
from pathlib import Path
from author_sources import ASOF, sources, retrievals
P1='P1 | Formation and entry (1944–October 1984)'
P2='P2 | Succession and early reforms (October 1984–1986)'
P3='P3 | Contested premiership (1987–December 1989)'
P4='P4 | Opposition and assassination (December 1989–May 1991)'
phases=[P1,P2,P3,P4]
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

def ov(n,topic,value,ids,typ='Recorded fact',**kw):
    return add('Overview',f'OV{n:02d}',{'Topic':topic,'Finding / value':value},ids,typ,**kw)
ov(1,'Identity','Rajiv Gandhi (20 August 1944–21 May 1991), Congress(I) leader and Prime Minister of India; born in Bombay, assassinated at Sriperumbudur, Tamil Nadu.',[1,35,36],priority='High')
ov(2,'Prime-ministerial tenure','31 October 1984–2 December 1989: one continuous spell, with a new ministry after the December 1984 general election.',[1,39],priority='High')
ov(3,'Family and entry','Son of Indira and Feroze Gandhi, grandson of Jawaharlal Nehru. An airline pilot before politics, he entered after brother Sanjay’s death and won Amethi in 1981.',[1,3],'Analysis',context='G03; E107')
ov(4,'Education','Attended Doon School, Trinity College Cambridge and Imperial College London. These accounts establish study, not a completed university degree.',[1],note='No original education credential inspected; do not describe him as an engineering graduate.')
ov(5,'Electoral record','Four Amethi victories: 1981 by-election and 1984, 1989, 1991 general elections. The last result was posthumous; he did not serve in the tenth Lok Sabha.',[2,3,4,5,6],'Analysis',priority='High')
ov(6,'Party mandate versus personal seat','ECI reports Congress winning 404 seats in 1984 and 197 in 1989. Rajiv retained Amethi when his government lost power; party totals are separate from his personal results.',[4,5,1],'Analysis')
ov(7,'Reform record','Telecom development, education institutions, anti-defection legislation and a lower voting age marked the period. Institutional origins, enactment and later outcomes are distinguished.',[8,9,10,11,13],'Analysis')
ov(8,'Economic interpretation','Panagariya stresses partial liberalisation and fiscal fragility; Rodrik and Subramanian emphasise an earlier pro-business shift. Neither account makes Rajiv the sole origin of faster growth.',[37,38],'Analysis',independent=True)
ov(9,'Regional settlements','Negotiations produced accords in Punjab, Assam and Mizoram. Their trajectories differed: agreement did not bring immediate peace in Punjab or resolve Assam’s immigration disputes.',[15,16],'Analysis')
ov(10,'Foreign policy','Sri Lankan intervention, the China opening, assistance to Maldives and nuclear diplomacy show active regional and international engagement with sharply different results.',[17,18,19,20,21,22],'Analysis')
ov(11,'Accountability','The 1984 anti-Sikh attacks, Bofors, religious-policy decisions and Sri Lanka remain central to assessment. Commission findings, criminal procedures and political criticism are kept distinct.',[23,24,25,27,28,18],'Analysis')
ov(12,'Bofors update','Delhi High Court found no bribery evidence against Rajiv in 2004. NDTV reports dismissal of a remaining appeal concerning other defendants on 6 August 2026; the original 2026 order remains uncollected.',[25,26],'Analysis',priority='High',note='Neither event is described as a trial acquittal of Rajiv.')
ov(13,'Gender and representation','Education initiatives addressed women’s agency, while the Muslim Women Act provoked equality criticism. Programme design and legal controversy do not establish a uniform gender legacy.',[12,14,27,28],'Analysis',context='G07; G09')
ov(14,'Opposition and death','Served as recognised opposition leader from 18 December 1989 to 24 December 1990. Congress later withdrew support from Chandra Shekhar; Rajiv was killed during the 1991 campaign.',[2,34,35],'Analysis')
ov(15,'Scope','Research cutoff: 28 October 2026. Four career phases plus selected posthumous legal and legacy developments. English-language records predominate; this is a structured research profile, not an exhaustive archive.',[],'Method / scope')
ov(16,'Evidence navigation','Start with findings and review flags. All citations opens every source; Claims identifies reviewed fields. Expand the + column group for qualifications, dates and supporting details.',[],'Method / scope')
ov(17,'Numbers and dates','Votes are ballots in personal constituencies; national tallies are separate rows. Shares use valid votes. Missing values are unknown, not zero. Assent, commencement, oath and election-result dates are distinct.',[],'Method / scope')
ov(18,'Research priorities','1981 full election return; exact party and portfolio boundaries; original 1989 local-government bill and 2026 Bofors order; policy evaluations, security inquiries, vernacular archives and independent gender studies.',[],'Method / scope')
ov(19,'Family background','Married Sonia Gandhi in 1968. The profile’s account of his initially private aviation career and later family succession is used for political context, without inferring a spouse’s role in specific government decisions.',[1],'Analysis',context='G03')

events=[
('20 August 1944','Birth','Born in Bombay to Indira and Feroze Gandhi.',[1],P1,'1944-08-20'),
('Before 1980','Education and aviation','Studied in Britain and worked as an Indian Airlines pilot before entering active politics.',[1],P1,None),
('1980','Family succession pathway','Sanjay’s death preceded Rajiv’s decision to enter politics.',[1],P1,None),
('14–15 June 1981','First parliamentary victory','Amethi poll on 14 June; declared elected on 15 June with 258,884 votes.',[3],P1,'1981-06-15'),
('17 August 1981','MP oath','Took his oath as a Lok Sabha member.',[7],P1,'1981-08-17'),
('1982–1984','Organisation','Asian Games organising and Congress general-secretary work preceded premiership.',[1],P1,None),
('31 October 1984','Prime Minister','Succeeded Indira Gandhi after her assassination.',[1,39],P2,'1984-10-31'),
('October–November 1984','Anti-Sikh attacks','Organised violence and police failures later examined by the Nanavati Commission; personal involvement and political responsibility require separate findings.',[23,24],P2,None),
('December 1984','Large majority','ECI records 404 Congress seats in the reported 514-seat election; Rajiv retained Amethi.',[4],P2,None),
('31 December 1984','Post-election ministry','Historical government table records a fresh ministry period beginning 31 December.',[39],P2,'1984-12-31'),
('15 February 1985','Anti-defection amendment','52nd Amendment received assent, adding the Tenth Schedule.',[9],P2,'1985-02-15'),
('July 1985','Punjab accord','Agreement with Harchand Singh Longowal proposed political and territorial arrangements; violence continued thereafter.',[15],P2,None),
('1985','Assam accord','Union government negotiated with AASU; settlement changed state politics without ending immigration disputes.',[15],P2,None),
('1985–1987','Open university','IGNOU established by statute in 1985 and began its first diploma programmes in 1987.',[13],P2,None),
('1986','Education and gender legislation','National education policy promoted equality; Muslim Women Act followed Shah Bano and provoked a different equality debate.',[12,27,28],P2,None),
('30 June 1986','Mizoram settlement','Peace accord concluded during his government; political leadership and civil-society roles were shared.',[15,16],P2,'1986-06-30'),
('22 July 1986','Rural telecom milestone','C-DOT’s first 128-line rural exchange commissioned at Kittur; the organisation itself had been founded before Rajiv became PM.',[8],P2,'1986-07-22'),
('1986–1987','Kashmir alliance and disputed poll','Rajiv–Farooq agreement preceded NC–Congress alliance; HRW records credible allegations of rigging and arrests in the 1987 election.',[33],P3,None),
('1987','Bofors controversy','Allegations concerning commissions in the howitzer purchase became a major accountability dispute; later court findings are recorded separately.',[25,26],P3,None),
('29 July 1987','Sri Lanka agreement','Rajiv and J.R. Jayewardene agreed a framework for ethnic accommodation and disarmament.',[17],P3,'1987-07-29'),
('5 May 1988','National Literacy Mission','Launched the national mission; later mass campaigns involved state, district and voluntary organisations.',[43],P3,'1988-05-05'),
('9 June 1988','Disarmament proposal','Presented a staged nuclear-disarmament plan at the UN special session.',[20],P3,'1988-06-09'),
('1988','Defamation bill withdrawn','Government withdrew the bill following organised press and wider opposition.',[30],P3,None),
('November 1988','Operation Cactus','India assisted Maldives following President Gayoom’s request against a coup attempt.',[22],P3,None),
('19–23 December 1988','China visit','Talks opened a boundary working-group process while expanding cooperation.',[19],P3,'1988-12-19'),
('31 December 1988','Pakistan nuclear-facility agreement','Bilateral non-attack agreement signed; entry into force followed in January 1991.',[21],P3,'1988-12-31'),
('February 1989','Bhopal settlement','Union government’s representation of victims culminated in a court-approved $470 million settlement, later contested.',[32],P3,None),
('28 March 1989','Voting age lowered','61st Amendment received assent, lowering the article 326 age threshold from 21 to 18.',[10],P3,'1989-03-28'),
('1989','Local-government bill failed','The 64th Amendment Bill failed in Rajya Sabha; later constitutional changes occurred under Rao.',[31],P3,None),
('2 December 1989','Premiership ended','Left office after the election reduced Congress to 197 seats.',[1,5],P3,'1989-12-02'),
('18 December 1989','Opposition leadership','Became recognised Leader of Opposition in Lok Sabha.',[2],P4,'1989-12-18'),
('1990–March 1991','Support and withdrawal','Congress supported the Chandra Shekhar minority government and later withdrew; the PM resigned on 6 March 1991.',[34],P4,None),
('21 May 1991','Assassination','Killed by an LTTE suicide attack while campaigning at Sriperumbudur.',[35,36],P4,'1991-05-21'),
('1991, after death','Result and honour','Declared elected from Amethi after death and awarded Bharat Ratna posthumously.',[2,6],P4,None)]
for n,(period,event,desc,ids,phase,dt) in enumerate(events,1):
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':dt,'Date precision':'Day' if dt else 'Year/range'},ids,'Analysis' if n in (8,15,18,19,29,32) else 'Recorded fact',phase,f'E{phases.index(phase)+1}01')

elections=[
(1981,258884,None,None,None,None,[3],P1,'Lok Sabha / by-election','Won','Poll 14 June; declared 15 June. Runner-up and denominator unavailable. The petitioner’s 2,728 votes are not used as runner-up votes.'),
(1984,365041,'Maneka Gandhi','IND',50163,436263,[4],P2,'Lok Sabha / direct','Won','ECI constituency 25 Amethi; valid votes denominator; rejected ballots excluded.'),
(1989,271407,'Raj Mohan Gandhi','JD',69269,402500,[5],P3,'Lok Sabha / direct','Won','Personal victory despite loss of national office; valid votes denominator.'),
(1991,187138,'Ravindra Pratap','BJP',75053,351548,[6,2],P4,'Lok Sabha / direct','Won posthumously','Result declared after death; no service in tenth Lok Sabha. Valid votes denominator.')]
for n,(year,votes,opp,oparty,ovotes,denom,ids,phase,route,result,note) in enumerate(elections,1):
    fields={'Year':year,'House / route':route,'Constituency':'Amethi','Result':result,'Candidate votes':votes,'Party':'INC (Congress(I))','Opponent':opp,'Opponent party':oparty,'Opponent votes':ovotes,'Signed vote margin':None,'Vote share':votes/denom if denom else None,'Share denominator':denom,'Finding':f'{result} Amethi in {year}; individual constituency result.','Counting unit':'Candidate ballots','Geography':'Uttar Pradesh; historical constituency 25','Candidate status':'Personal contestant'}
    checked={'Finding':ids,'Candidate votes':ids[:1]}
    if ovotes: checked.update({'Opponent':ids[:1],'Opponent votes':ids[:1],'Share denominator':ids[:1],'Vote share':ids[:1]})
    add('Elections',f'EL{n:02d}',fields,ids,phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,note=note,priority='High')
for n,year,seats,total,sid,phase in [(5,1984,404,514,4,P2),(6,1989,197,529,5,P3),(7,1991,232,521,6,P4)]:
    add('Elections',f'EL{n:02d}',{'Year':year,'House / route':'Lok Sabha / party result','Constituency':'India: report coverage','Result':f'Congress: {seats} seats','Candidate votes':None,'Opponent votes':None,'Signed vote margin':None,'Vote share':None,'Congress seats':seats,'Seats reported':total,'Finding':f'Congress won {seats} of {total} seats covered by this ECI general-election report.','Candidate status':'Party leadership context; not another personal contest'},[sid],phase=phase,context=f'E{phases.index(phase)+1}03',note='Report coverage differs across election years because of deferred polling. The 1991 government formed after Rajiv’s death.')

offices=[
('MP, seventh Lok Sabha','1981–1984','Elected from Amethi in the June 1981 by-election; oath on 17 August.',[3,7,2],P1,None,None,'Elected'),
('Congress general secretary','Before October 1984','Held organisational office before becoming Prime Minister; precise appointment day not established.',[1],P1,None,None,'Party'),
('Asian Games organiser','1982','Organisational involvement in the Delhi Asian Games helped establish a public administrative profile.',[1],P1,None,None,'Organisational / informal influence'),
('Prime Minister: first ministry','31 October–31 December 1984','Appointed after Indira Gandhi’s assassination; distinct initial ministry before the post-election government.',[1,39],P2,'1984-10-31','1984-12-31','Executive'),
('Prime Minister: second ministry','31 December 1984–2 December 1989','Led government following the general election; continuous premiership across the two ministries.',[1,39],P2,'1984-12-31','1989-12-02','Executive'),
('MP, eighth Lok Sabha','1984–1989','Returned from Amethi in 1984.',[4,2],P2,None,None,'Elected'),
('Congress president / party leader','1984–21 May 1991','PMO records party leadership with the 1984 succession; he continued to lead Congress in opposition and the 1991 campaign.',[1,34,35,40],P4,None,'1991-05-21','Party'),
('Defence and other additional portfolios','During premiership','Lok Sabha profile lists Defence, Finance, External Affairs and several other portfolios held alongside the premiership.',[2],P3,None,None,'Additional ministerial charge'),
('MP, ninth Lok Sabha','1989–13 March 1991','Re-elected from Amethi in 1989; the ninth Lok Sabha was dissolved on 13 March 1991.',[5,2,39],P4,None,'1991-03-13','Elected'),
('Leader of Opposition, Lok Sabha','18 December 1989–24 December 1990','Recognised opposition tenure as listed by the Lok Sabha Secretariat.',[2],P4,'1989-12-18','1990-12-24','Parliamentary'),
('External supporter of minority ministry','1990–March 1991','Led Congress while it supported and then withdrew support from Chandra Shekhar; this was not a ministerial office.',[34],P4,None,None,'Party / parliamentary influence'),
('1991 elected result; no term served','1991, result after death','Bioprofile lists election to tenth Lok Sabha but explicitly notes death before result; no tenth-Lok-Sabha service is claimed.',[2,6],P4,None,None,'Posthumous result only')]
for n,(office,period,finding,ids,phase,start,end,cat) in enumerate(offices,1):
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':office,'Period':period,'Finding':finding,'Start date':start,'End date':end,'Position category':cat,'Boundary note':'Blank dates preserve year/range precision; exact gazettes and party resolutions remain research priorities.'},ids,phase=phase,context='E202; E302' if n==5 else f'E{phases.index(phase)+1}02',checked={'Finding':[1,34,35]} if n==7 else None,note='Party president exact appointment/election chronology remains open; S040 is a candidate lead.' if n==7 else '')

policies=[
('Telecommunications and C-DOT','Rural and digital exchange milestones occurred in 1986–88; C-DOT itself was established in August 1984 before Rajiv became PM.','Implemented institutional milestones',[8],P2,'Government sponsorship and expansion','Engineers, Pitroda and earlier/later governments shared the process; later telecom penetration is not measured here.'),
('Economic deregulation','Partial industrial liberalisation and a more supportive business climate developed during the 1980s.','Policy changes; contested growth explanation',[37,38],P2,'Government leadership / continuation','Competing accounts differ on timing and mechanism; fiscal expansion and the later crisis complicate a simple success narrative.'),
('Anti-defection law','52nd Amendment, assented to 15 February 1985, inserted the Tenth Schedule.','Enacted',[9],P2,'Government legislation; Parliament and President','Party discipline mechanism is documented; improved integrity or reduced opportunism is not presumed.'),
('Voting age','61st Amendment lowered the article 326 voting threshold from 21 to 18; assent came on 28 March 1989.','Enacted',[10],P3,'Government legislation; Parliament and President','Expanded eligibility is distinct from registration, turnout or a proven electoral advantage to Congress.'),
('Education policy and women’s equality','NPE set an explicit equality agenda through literacy, retention, curricula and technical education.','Policy commitment',[12],P2,'Government policy','Composite 1986/1992 text; outcome evaluation and clause-level version history remain open.'),
('Navodaya schools','Scheme launched in 1986 for talented children predominantly from rural areas.','Institutional launch',[11],P2,'Government programme','Later school counts and alumni outcomes are not outputs of the original tenure alone.'),
('IGNOU','University established by statute in 1985; began two diploma programmes in 1987.','Enacted and operational',[13],P2,'Government and Parliament; university implementation','Open-learning institution predates its later expansion; original-tenure learning outcomes not evaluated.'),
('Mahila Samakhya','Consultative formulation in 1988 led to a 1988–89 pilot centred on women’s educational collectives.','Formulation and pilot',[14],P3,'Government framework with women’s groups and educators','Not a one-person initiative; subsequent autonomous action and empowerment require separate evaluation.'),
('National Literacy Mission','Rajiv launched the mission on 5 May 1988; campaign methods depended on local government and voluntary mobilisation.','Launched; implementation evolved',[43],P3,'Launched / promoted','Later literacy gains are not attributed exclusively to Rajiv; targets are not attained counts.'),
('Punjab accord','July 1985 agreement proposed Chandigarh transfer, boundary resolution, water adjudication and relief measures.','Agreement; uneven follow-through',[15],P2,'Negotiated with Longowal','Continuing militancy and state coercion preclude treating signature as immediate peace.'),
('Assam accord','1985 negotiations with AASU produced an accord and changed electoral politics.','Negotiated settlement',[15],P2,'Union government leadership','Exact citizenship cutoffs and present legal implementation not adjudicated in this profile; original treaty remains a gap.'),
('Mizoram settlement','1986 accord, dated 30 June, helped end insurgency and opened a statehood and electoral settlement.','Agreement and political transition',[15,16],P2,'Steered negotiations; shared political sponsorship','Do not call Rajiv the formal signatory without original signature page; earlier talks, Laldenga and civil society also mattered.'),
('Sri Lanka accord and IPKF','July 1987 agreement sought ethnic accommodation and disarmament; intervention subsequently faced armed conflict and serious human-rights allegations.','Agreement and military intervention',[17,18,22],P3,'Signed agreement / executive leadership','Treaty intent, military performance and alleged abuses are distinct; no personal order for abuses established.'),
('China opening','December 1988 visit established a boundary working-group process while pursuing other cooperation.','Diplomatic process',[19],P3,'Led visit and negotiations','Boundary remained unsettled; Chinese official retrospective is one institutional perspective.'),
('Maldives / Operation Cactus','India responded to Gayoom’s appeal against the November 1988 coup attempt.','Military assistance implemented',[22],P3,'Executive authorisation / strategic leadership','Operational success described by the author does not validate every regional intervention.'),
('Nuclear disarmament','June 1988 UN address proposed staged nuclear elimination by 2010 and collective security arrangements.','Proposal',[20],P3,'Proposed','The record is evidence of stated policy, not an implemented treaty.'),
('Pakistan nuclear-facility accord','Agreement signed 31 December 1988; entered into force on 1 January 1991.','Signed; later entry into force',[21],P3,'Bilateral government diplomacy','Avoid conflating signature with commencement or with resolution of the wider relationship.'),
('Local-government constitutional proposal','64th Amendment Bill failed in Rajya Sabha in 1989; 73rd/74th amendments passed under Rao in 1992.','Proposed; not enacted during tenure',[31],P3,'Proposed legislation','Original 1989 women’s quota and federal design need the actual bill; later one-third reservation is not retroactively assigned.'),
('Muslim Women Act','1986 legislation followed Shah Bano. In 2001 Supreme Court upheld it while requiring future provision beyond iddat.','Enacted; later judicial interpretation',[27],P2,'Government legislation','Historical criticism is separately attributed; this row is not current individual legal guidance.'),
('Consumer protection','Search metadata identifies the 1986 Consumer Protection Act; original text and implementation remain unreviewed.','Evidence gap',[41],P2,'Legislation during tenure; detail pending','Do not certify redress outcomes or section-specific rights from metadata.'),
('Rural employment / JRY','Official audit search excerpt places the NREP/RLEGP merger into JRY in April 1989; full passage inaccessible.','Evidence gap',[42],P3,'Government programme; detail pending','No audited employment, spending or causal poverty result adopted.')]
for n,(topic,finding,stage,ids,phase,role,limit) in enumerate(policies,1):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':topic,'Finding':finding,'Stage':stage,'Documented role':role,'Outcome / attribution limit':limit},ids,'Analysis',phase,f'E{phases.index(phase)+1}04',priority='High' if n in (10,11,12,13,18,19) else 'Normal')

ideas=[
('Technology and administrative modernisation','Telecom and education institutions gave the modernisation agenda concrete mechanisms, while different institutions had different origins.',[8,11,13],P2),
('Business and state','Economic scholarship distinguishes partial deregulation and support for incumbent business from the more systemic reforms introduced after his death.',[37,38],P3),
('Dynasty and rapid advancement','Family succession and party organisation together explain the documented route from pilot to parliamentary and national leadership; relative contributions are not quantified.',[1,3],P1),
('Negotiation and national integration','The regional accords combined accommodation within the Union with executive authority; their varied results resist a single success label.',[15,16],P2),
('Party discipline and local democracy','Anti-defection enactment and the failed local-government proposal addressed different levels of representation; they need separate institutional assessments.',[9,31],P3),
('Secularism under pressure','Zoya Hasan argues that concessions over Muslim personal law and Ayodhya weakened secular credibility. This is an attributed interpretation of competing political decisions.',[28,29,27],P3),
('Press and accountability','Defence of the 1988 defamation bill, followed by withdrawal under protest, exposes tension between executive control and his stated support for a free press.',[30],P3),
('Regional security and global disarmament','Military intervention in neighbouring states coexisted with a UN disarmament proposal; stated universal principles and strategic practice should both be examined.',[17,20,22],P3),
('Opposition bargaining','Support for, then withdrawal from, a minority government illustrates party leverage after the loss of the premiership.',[34],P4)]
for n,(topic,finding,ids,phase) in enumerate(ideas,1):
    add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding,'Evidence type':'Documented acts or explicitly attributed interpretation'},ids,'Analysis',phase,f'E{phases.index(phase)+1}07')

matters=[
('1984 anti-Sikh violence','Nanavati found organised attacks and police failures but did not find evidence Rajiv organised them. HRW criticises impunity and his public metaphor after the violence.','Commission findings; political and executive accountability','Commission records peace appeals and emergency actions. These do not erase the failures of protection or criticisms of his rhetoric.',[23,24],P2,'1984; commission 2005; HRW 2014','Individual cases against others are not resolved by the commission’s statement about Rajiv. No personal instruction to kill is established.'),
('Bofors','2004 High Court found no bribery evidence against Rajiv and removed related corruption-conspiracy charges; separate charges against others remained then.','Court finding; later procedural history','Rajiv denied that commissions had been paid. The court’s conclusions and his denial are separate forms of evidence.',[25,26],P3,'1986–2004; reported update 6 August 2026','NDTV reports dismissal of an appeal involving other defendants in 2026. Original order missing; no trial acquittal of deceased Rajiv inferred.'),
('Shah Bano and the Muslim Women Act','1986 Act provoked criticism that the government sacrificed women’s equality to religious bargaining. Danial Latifi later upheld it with a protective interpretation.','Legislation; scholarly criticism; constitutional judgment','Statutory framework invoked protection of divorced women; Hasan contests its political effect. Court requires future provision beyond iddat.',[27,28],P2,'1985–1986; judgment 2001','Do not describe the 1986 Act as a blanket end to maintenance after three months, or treat 2001 as the last word on all later law.'),
('Ayodhya','Court ordered unlocking in February 1986; Hasan criticises Congress’s subsequent religious positioning and permission for shilanyas.','Judicial action and political controversy','Secular assurances coexisted with religious campaign appeals in Hasan’s account. A direct personal unlocking instruction is not established.',[28,29],P3,'1986–1989','Separate court order, administration and party choices; source chronology is not used to fix an exact November sequence.'),
('Sri Lanka / IPKF','Intervention intended to support a negotiated settlement became prolonged conflict. Amnesty recorded allegations of serious abuses by IPKF personnel.','Policy criticism; documented allegations','Agreement asserted unity and minority recognition; official military-accountability responses to the specific allegations were not obtained.',[17,18,22],P3,'1987–1989; Amnesty 1990','No judicial conviction or personal order by Rajiv is inferred; Sri Lankan state and armed groups also exercised agency.'),
('Kashmir: alliance and 1987 election','HRW describes credible rigging allegations and arrests after the Rajiv–Farooq alliance, linking electoral disillusionment to militancy.','Attributed historical assessment / electoral allegations','Direct Rajiv response and an authoritative adjudication of his personal involvement were not obtained.',[33],P3,'1986–1989; HRW 2006','Independent second origin and original election litigation remain gaps; no single-cause account of insurgency.'),
('Defamation Bill 1988','Government withdrew a Lok Sabha-passed bill after press, public and internal party resistance.','Withdrawn legislative proposal','Rajiv initially defended its necessity and later publicly affirmed democratic press freedom.',[30],P3,'1988; retrospective 2018','Bill never became law; exact text and legislative dates need primary records. Reported Bofors-related motive is not established as private intent.'),
('Bhopal disaster and compensation','Supreme Court records the $470 million settlement approved in February 1989; its 2023 judgment refused to reopen compensation through curative petitions.','Civil settlement, review and curative dismissal','Union government represented victims; later litigation challenged adequacy. Court approval does not establish that victims considered compensation sufficient.',[32],P3,'1984–1989; later judgments through 2023','Criminal proceedings and civil compensation differ. Personal instruction concerning Warren Anderson’s departure is unproven here.'),
('Assassination: criminal responsibility and release','Judicial account attributes the killing to an LTTE suicide conspiracy; remaining six convicted prisoners received premature release in November 2022.','Criminal proceedings; later sentence-related release','Reported judicial rationale concerned long custody and conduct. Release did not establish exoneration; Rajiv could not respond to posthumous proceedings.',[35,36],P4,'21 May 1991; appeals 1999; release 2022','Separate opinion not used as full-bench sentencing tally. Jain/Verma inquiry findings, security decisions and original 2022 orders remain uncollected.'),
('1991 withdrawal of support','Congress withdrew support from Chandra Shekhar following the surveillance dispute; he announced resignation on 6 March.','Political dispute / government resignation','Government described the police presence as routine and offered investigation; Congress did not accept that response.',[34],P4,'March 1991','Competing explanations of motive remain attributed; no judicial finding about a personal surveillance order.')]
for n,(matter,finding,procedure,response,ids,phase,period,caution) in enumerate(matters,1):
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Procedural status':procedure,'Response / competing account':response,'Period / latest checked evidence':period,'Scope / caution':caution},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',priority='High',independent=n in (1,3,4,5))

legacy=[
('Institution building','C-DOT milestones, IGNOU and Navodaya are durable institutional reference points. Later scale reflects many governments and implementers.',[8,11,13],'Institutional histories',P2),
('Economic transition','Panagariya emphasises liberalisation and fiscal fragility; Rodrik/Subramanian locate the growth shift earlier and stress pro-business attitudes.',[37,38],'Competing scholarly explanations',P3),
('Regional accommodation','Mizoram is celebrated as a successful settlement; Punjab and Assam show that signed accords can leave persistent disputes.',[15,16],'NCERT synthesis and attributed commemorative view',P2),
('Democratic institutions','Lowering voting age was enacted; local-government constitutional change remained a failed proposal during his tenure and was enacted in different form later.',[10,31],'Legislative chronology',P3),
('Gender legacy','Educational collective-action programmes and the Muslim Women Act point to different mechanisms and competing assessments of women’s agency and rights.',[14,27,28],'Educational scholarship, judgment and political scholarship',P3),
('Security and diplomacy','China’s diplomatic process and the Maldives operation contrast in outcome and scope with the difficulties and alleged abuses of the Sri Lankan intervention.',[19,22,18],'Institutional and independent security/human-rights accounts',P3),
('Violence and accountability','The commission’s limited finding about Rajiv’s involvement in 1984 must coexist with the documented protection failures and survivors’ long justice struggle.',[23,24],'Commission and human-rights assessment',P2),
('Mandate, reputation and posthumous politics','An exceptional 1984 party majority was followed by government defeat in 1989. Assassination and posthumous honours shaped memory without resolving all policy or accountability debates.',[4,5,2,35],'Election and official biographical record',P4)]
for n,(theme,assessment,ids,assessor,phase) in enumerate(legacy,1):
    add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor / basis':assessor,'Limit':'Bounded synthesis of linked records; no composite greatness score.'},ids,'Analysis',phase,f'E{phases.index(phase)+1}10')

from author_context import populate_context, coverage
populate_context(add,phases)

gapdata=[
('1981 constituency return','Winner total is in a Supreme Court record; runner-up votes and valid-vote denominator remain missing.','Obtain ECI by-election return or certified result; do not use petitioner’s votes as runner-up.',['EL01'],'High'),
('Party presidency and portfolio dates','PMO compresses party succession; UPI search lead gives 12 November 1984. Exact office appointments and additional-charge dates are not reconciled.','Inspect party resolutions, centenary election record and appointment gazettes; keep exact unverified dates blank.',['OF02','OF07','OF08'],'High'),
('1989 local-government bill','Later legislative history is inspected but original bill, proposed women’s quota and federal provisions are not.','Obtain 64th/65th bills and Rajya Sabha debates; separate proposed and enacted reservations.',['PG18','G09'],'High'),
('Bofors 2026 order','Latest dismissal is reported by NDTV; original order not obtained.','Retrieve 6 August 2026 Supreme Court docket/order and verify precise scope and remaining proceedings.',['CV02','OV12'],'High'),
('1984 accountability','Commission and 2014 rights report inspected; individual prosecutions and latest survivor accounts not systematically updated.','Review case-specific orders and independent victim histories; do not turn a 2014 justice assessment into a 2026 case count.',['CV01','LA07'],'High'),
('Assassination and security inquiries','Basic judicial account and 2022 release report inspected; full operative orders and Jain/Verma inquiry records missing.','Retrieve original judgments and inquiry findings; distinguish conspiracy, security negligence and sentence remission.',['CV09','G06'],'High'),
('Original regional accords','NCERT supplies broad Punjab/Assam/Mizoram account; formal signatories and clause-level implementation not checked against originals.','Obtain signed texts, notifications, statehood statute and independent regional histories.',['PG10','PG11','PG12'],'High'),
('Sri Lanka intervention','Agreement reproduction and Amnesty allegations inspected; original treaty, military records and responses to specific abuses remain gaps.','Retrieve MEA original, parliamentary statements, Sri Lankan/Tamil accounts and follow-up investigations.',['CV05','PG13'],'High'),
('Kashmir corroboration','Detailed 1986–1987 account currently rests on one rights-report synthesis.','Add independent scholarship, original election petitions and Congress/NC/MUF responses; avoid personal guilt inference.',['CV06','TL18'],'High'),
('Policy impact and fiscal record','Evidence is stronger on institutional design and milestones than independently measured outcomes.','Add contemporary budgets, Economic Surveys, CAG reports and credible evaluations of telecom, education and employment.',['PG01','PG02','PG05','PG06','PG08','PG09'],'High'),
('Consumer protection and rural employment','Statutory/audit originals inaccessible; records remain search-excerpt leads.','Recover the Act and JRY audit from official mirrors; inspect implementation and beneficiary evidence.',['PG20','PG21'],'High'),
('Gender mechanisms and reception','No matched study of recruitment, portfolio allocation, campaign framing or women’s party influence collected.','Use contemporary women leaders, feminist scholarship, women’s groups and audience evidence rather than assuming a male-leadership effect.',['G01','G04','G05','G08','G10'],'Normal'),
('Education version and biography','Education-policy transcription is composite; university degree and exact academic departure dates are unverified.','Retrieve original 1986 policy and education records; retain attendance-only wording.',['OV04','PG05'],'Normal'),
('Press, culture and other legislation','Original Defamation Bill and wider censorship record, Environment Act, Operation Blackboard and technology missions require expansion.','Inspect legislative debates, notifications and programme audits before adding section-specific or outcome claims.',['CV07','PG05'],'Normal'),
('Bhopal responsibility','Settlement chronology is established; victim perspectives and claims concerning Anderson’s departure lack a dedicated evidentiary review.','Obtain contemporaneous orders, testimony and independent reporting; separate state and Union decisions.',['CV08'],'High'),
('Historical sources and opposition phase','English-language institutional sources dominate; party reform speeches, regional media, Cold War ties and 1990–91 coalition negotiations need fuller treatment.','Add dated speeches, Hindi/regional archives, diplomatic records and contemporaneous opposition accounts.',['IM03','IM09','E105','E406'],'Normal')]
for n,(topic,detail,action,records,priority) in enumerate(gapdata,1):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':detail,'next_action':action,'status':'Open','record_ids':records})

base=Path(__file__).parent
data={'schema_version':1,'subject':'Rajiv Gandhi','as_of':ASOF,'guidance':'Four career phases; ten gender dimensions and ten era dimensions per phase. Separate personal and party elections, policy stages, commission findings and criminal procedures. Field-level review is not certification of every neighbouring cell. Open evidence gaps remain explicit.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
