"""Reproducible Sushma Swaraj research; evidence review is field-specific."""
import hashlib, json
from pathlib import Path
from author_sources import ASOF, sources, retrievals
P1='P1 | Formation and Haryana (1973–1990)'
P2='P2 | National rise and NDA ministries (1990–2004)'
P3='P3 | Parliamentary opposition (2004–2014)'
P4='P4 | External Affairs and final year (2014–2019)'
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
    if typ!='Method / scope':
        cited=[s for s in sources if s['Source ID'] in ids]
        row['Corroboration']=('Unresolved' if status!='Supported' else ('Interested source only' if nums==[4] else ('Primary record' if any(s['Primary / secondary']=='Primary' for s in cited) else ('Single credible source' if len(cited)==1 else 'Multiple sources; inspect shared origins'))))
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
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':r['id'],'locator':r['locator'],'passage_paraphrase':r['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex: inspected-passage review','reviewed_at':ASOF,'note':'Sources jointly support the registered field. Analysis is a bounded inference; quoted positions remain attributed. Repeated passages are not independent corroboration.'})
        val=row[field]
        claims.append({'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':val,'fingerprint':hashlib.sha256(json.dumps(val,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':typ,'status':status,'priority':priority,'candidate_source_ids':support,'evidence_ids':evs,'contradictions':[],'review_note':note or ('Bounded interpretation of identified evidence.' if typ=='Analysis' else 'Full registered field checked; accompanying qualifications apply.')})
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
ov(1,'Identity','Sushma Swaraj (14 February 1952–6 August 2019), lawyer, parliamentarian and BJP leader; born in Ambala, in present-day Haryana.',[1])
ov(2,'Formation','Studied at SD College and Panjab University; began Supreme Court practice in 1973. JP-movement participation and her self-described RSS-family/ABVP background provide distinct strands of political formation.',[1,2,4],'Analysis',context='G01')
ov(3,'Trajectory','Moved from Haryana politics to both Houses of Parliament, Union ministries and a brief Delhi chief ministership; led the Lok Sabha opposition before becoming External Affairs Minister.',[1,2,3],'Analysis')
ov(4,'Party affiliations','Contested for Janata in 1977 and 1980, and for BJP by 1984. Her own account links an RSS family, student activism and socialist connections; these are not interchangeable organizational memberships.',[5,8,13,4],'Analysis')
ov(5,'Personal election record','Eleven direct contests: seven victories and four defeats; three additional Rajya Sabha elections. Assembly: three wins. Lok Sabha: four wins and four losses.',[1,5,6,7,8,9,10,11,12,13],'Analysis',priority='High')
ov(6,'Principal arenas','Ambala Cantt and Karnal in Haryana; South Delhi and Hauz Khas; the 1999 Bellary challenge; Vidisha in 2009 and 2014. Rajya Sabha service also provided a route back to national office.',[2,5,6,7,8,9,10,11,12,13],'Analysis')
ov(7,'Gender milestones','First woman Chief Minister of Delhi and first woman Leader of Opposition in Lok Sabha; first woman to hold External Affairs full time. The qualification matters: earlier women had held additional charge.',[2],context='G02')
ov(8,'Administrative record','Documented interventions include film-finance access, tobacco legislation, consular evacuation coordination, grievance tracking and passport-document reform. Implementation and long-term effects require separate evidence.',[15,16,18,19,20],'Analysis')
ov(9,'Diplomatic method','Her record combines citizen-facing services with parliamentary and bilateral negotiation. The Bangladesh boundary measure and Pakistan dialogue agreement illustrate collective government diplomacy rather than sole authorship.',[18,21,24,46],'Analysis')
ov(10,'Accountability questions','Major disputes concerned Lalit Modi’s travel papers and communication with families of Indians missing in Iraq. The workbook records criticism, her replies and the limits of procedural evidence.',[26,27,28,29],'Analysis',priority='High')
ov(11,'Historical assessment','Institutional firsts and accessible consular leadership are strong themes in remembrance. A balanced assessment also preserves partisan nationalism, controversies and limits on attributing government outcomes to one minister.',[2,4,18,26,28,32],'Analysis')
ov(12,'Scope and cutoff','Career through her death in August 2019; selected posthumous recognition. Sources accessed 5 October 2026. Historical legal dispositions are dated, not asserted as current case-status updates.',[],'Method / scope')
ov(13,'Reading guide','Expand the + columns for role, dates, context and qualifications. All citations opens every source for a row. Claims and Evidence identify the fields actually reviewed; a source link alone is not verification.',[],'Method / scope')
ov(14,'Election conventions','Signed margin = Swaraj votes minus the named principal opponent. For a loss the opponent is the winner, including third-place Karnal 1984. Shares use inspected valid-vote totals. Blank means unresolved or inapplicable, never zero.',[],'Method / scope')
ov(15,'Attribution standard','Policy announcements, legislative passage, implementation and evaluated effects are separate. Ministry tenure does not establish sole authorship. Claims about beliefs describe stated positions, not verified private motives.',[],'Method / scope')
ov(16,'Remaining gaps','Original returns for several older elections; some office and Rajya Sabha state-allocation boundaries; full 2018 India–US statement; institutional-renaming date; independent outcome and comparative gender studies.',[],'Method / scope')
ov(17,'Review limits','Each substantive row has a registered finding. Some fields contain several linked assertions; counts are review units, not a score of historical completeness. Unread candidate material stays Not reviewed.',[],'Method / scope')

timeline=[
('14 February 1952','Birth','Born in Ambala, present-day Haryana.',[1],'1952-02-14',P1),
('1973','Legal practice','Began practising at the Supreme Court after legal education.',[1],None,P1),
('1970s','Movement politics','Participated in the JP movement; her later interview describes ABVP activity and an RSS-family background.',[2,4],None,P1),
('1977','Assembly and ministry','Won Ambala Cantt for Janata and entered Haryana’s ministry.',[1,8],None,P1),
('1980 and 1984','Karnal defeats','Lost Karnal for Janata in 1980 and for BJP in 1984.',[5,13],None,P1),
('1987','Haryana return','Won Ambala Cantt for BJP and returned to the state ministry.',[3,8],None,P1),
('1989','Third Karnal attempt','Lost to Chiranjit Lal by 8673 votes.',[6],None,P1),
('April 1990','Rajya Sabha entry','First Rajya Sabha term began; later returned through elections in 2000 and 2006.',[2],None,P2),
('1996','Lok Sabha and Union ministry','Won South Delhi and served in the short May–June Vajpayee ministry.',[3,12],None,P2),
('1998','Delhi leadership transition','Retained South Delhi, served in I&B and then became Delhi Chief Minister in October.',[3,7],None,P2),
('November–December 1998','Personal win, party defeat','Won Hauz Khas but tendered resignation after BJP’s Delhi defeat; caretaker end date differs from resignation tender.',[9,41,3],None,P2),
('1999','Bellary challenge','Lost the Bellary Lok Sabha contest to Sonia Gandhi.',[10],None,P2),
('2000–2004','Ministerial return','Returned to Rajya Sabha and I&B, then held Health and Parliamentary Affairs.',[2,3],None,P2),
('30 April 2003','Tobacco bill','Moved the tobacco-control bill for Lok Sabha consideration; the debate concluded with passage.',[16],'2003-04-30',P2),
('2004–2009','Committee leadership','Chaired the parliamentary Home Affairs committee during opposition years.',[3],None,P3),
('2009','Vidisha and opposition leadership','Won Vidisha and became Lok Sabha Leader of Opposition in December.',[3,11],None,P3),
('2010','Women’s reservation advocacy','Supported a party whip for the women’s reservation bill when it reached Lok Sabha.',[31],None,P3),
('27 May 2014','Portfolio allocation','Allocated External Affairs and Overseas Indian Affairs after the new government’s formation.',[14],'2014-05-27',P4),
('2015','Diplomatic and consular initiatives','Yemen evacuation, MADAD launch, Bangladesh boundary bill and Pakistan dialogue agreement marked different aspects of the ministry’s work.',[18,19,21,24],None,P4),
('23 December 2016','Passport reform announcement','Accepted inter-ministerial recommendations simplifying family-related passport documentation.',[20],'2016-12-23',P4),
('20 March 2018','Iraq deaths confirmed','Announced the deaths of 39 Indians; earlier assurances became a major accountability dispute.',[28,29],'2018-03-20',P4),
('1 March 2019','OIC address','Addressed the OIC as guest of honour on a UAE invitation.',[23],'2019-03-01',P4),
('2019','Electoral retirement and death','Did not seek re-election, citing health; died on 6 August after completing her ministerial term.',[36,1],None,P4),
('2020 award year','Posthumous honour','Received the Padma Vibhushan posthumously; the inspected award notification is dated 2021.',[37],None,P4)]
for n,(period,event,desc,ids,date,phase) in enumerate(timeline,1):
    ck={'Description':ids}
    if date: ck['Start date']=ids
    add('Career Timeline',f'TL{n:02d}',{'Period':period,'Event':event,'Description':desc,'Start date':date,'Date precision':'Named action date' if date else 'Year / period'},ids,phase=phase,context=f'E{phases.index(phase)+1}02',checked=ck)

# Direct-election units are individual votes; no popular share for Rajya Sabha.
elections=[
(1977,'Assembly','Ambala Cantt','JNP','Won',19639,'Dev Raj Anand','INC',9815,30953,None,[8],P1,'Secondary historical return.'),
(1980,'Lok Sabha','Karnal','JNP','Lost',129458,'Chiranji Lal','INC(I)',151786,430635,'1980-01-03',[5],P1,'Primary ECI constituency table; poll date.'),
(1984,'Lok Sabha','Karnal','BJP','Lost',77870,'Chiranji Lal','INC',247063,None,None,[13],P1,'Third place; deficit shown against winner, not runner-up. Secondary fallback.'),
(1987,'Assembly','Ambala Cantt','BJP','Won',22473,'Ram Dass Dhamija','INC',14501,46248,None,[8],P1,'Secondary historical return.'),
(1989,'Lok Sabha','Karnal','BJP','Lost',265792,'Chiranjit Lal','INC',274465,595298,'1989-11-22',[6],P1,'Primary ECI constituency table; poll date.'),
(1990,'Rajya Sabha','State allocation: verification pending','BJP','Elected',None,None,None,None,None,None,[2],P2,'Term began April 1990; indirect route. State allocation not verified in collected primary text.'),
(1996,'Lok Sabha','South Delhi','BJP','Won',294570,'Kapil Sibal','INC',180564,None,None,[12],P2,'Secondary fallback; source’s male gender coding rejected. Share denominator unverified.'),
(1998,'Lok Sabha','South Delhi','BJP','Won',331756,'Ajay Makan (source spelling)','INC',215043,564561,'1998-02-16',[7],P2,'Share uses valid votes, excluding invalid ballots; not total votes polled.'),
(1998,'Assembly','Hauz Khas','BJP','Won',25267,'Professor Kiran Walia','INC',22652,51257,None,[9],P2,'Personal Assembly win despite BJP’s overall defeat.'),
(1999,'Lok Sabha','Bellary','BJP','Lost',358550,'Sonia Gandhi','INC',414650,802055,None,[10],P2,'Secondary fallback; no margin from an Assembly-segment subtotal.'),
(2000,'Rajya Sabha','State allocation: verification pending','BJP','Elected',None,None,None,None,None,None,[2],P2,'Term April 2000–April 2006; state reorganization/allocation requires original notifications.'),
(2006,'Rajya Sabha','State allocation: verification pending','BJP','Elected',None,None,None,None,None,None,[2],P3,'Term April 2006–May 2009; popular vote share inapplicable.'),
(2009,'Lok Sabha','Vidisha','BJP','Won',438235,'Choudhary Munabbar Salim','SP',48391,None,None,[11],P3,'Congress nominee’s rejected nomination changed the contest (S039). Secondary counts; share withheld.'),
(2014,'Lok Sabha','Vidisha','BJP','Won',714348,'Lakshman Singh','INC',303650,None,None,[11],P4,'Secondary counts; official result book inaccessible. Reconcile NOTA/denominator before adding share.')]
for n,(year,house,seat,party,result,votes,opp,oparty,ovotes,valid,date,ids,phase,note) in enumerate(elections,1):
    indirect=house=='Rajya Sabha'
    fields={'Year':year,'House / route':house+(' / indirect' if indirect else ' / direct'),'Constituency':seat,'Result':result,'Candidate votes':votes,'Party':party,'Principal opponent':opp,'Opponent party':oparty,'Opponent votes':ovotes,'Signed vote margin':None if ovotes is None else votes-ovotes,'Vote share':None if valid is None else votes/valid,'Valid votes':valid,'Vote-share basis':'Candidate / inspected valid votes' if valid else ('Not applicable: indirect election' if indirect else 'Unresolved; no checked denominator'),'Election date':date,'Date meaning':'Polling day' if date else 'Year; exact election day not verified','Vote unit':'MLA ballots; count not collected' if indirect else 'Individual candidate votes','Finding':f'{party} candidate Swaraj {result.lower()} this {house} election.'}
    checked={k:ids for k in ('Finding','Candidate votes','Opponent votes','Vote share','Valid votes','Election date') if fields[k] is not None}
    add('Elections',f'EL{n:02d}',fields,ids,phase=phase,context=f'E{phases.index(phase)+1}03',checked=checked,note=note,priority='High')

offices=[
('Haryana MLA, Ambala Cantt','1977–1982','First Assembly term; elected for Janata.',[3,8],None,None,P1,'Direct election'),
('Haryana Labour Minister','1977–1979','First state ministerial office.',[3],None,None,P1,'Executive appointment'),
('Haryana MLA, Ambala Cantt','1987–1990','Returned as BJP candidate.',[3,8],None,None,P1,'Direct election'),
('Haryana Education, Food and Civil Supplies','1987–1990','Held these portfolios in her second state-ministry period.',[3],None,None,P1,'Executive appointment'),
('Rajya Sabha member: first term','April 1990–April 1996','First term in the Upper House; state-allocation notification remains to be inspected.',[2],None,None,P2,'Indirect election'),
('Lok Sabha MP, South Delhi','1996–1998','Won the 1996 election.',[12],None,None,P2,'Direct election'),
('Union Information and Broadcasting','16 May–1 June 1996','Served in the brief Vajpayee ministry.',[3],'1996-05-16','1996-06-01',P2,'Cabinet appointment'),
('Lok Sabha MP, South Delhi','1998; moved to Delhi state politics','Won again in 1998; exact Lok Sabha vacancy notification uncollected.',[7,3],None,None,P2,'Direct election'),
('I&B; additional Telecommunications','19 March–12 October 1998','Returned to Union cabinet before taking Delhi leadership.',[3],'1998-03-19','1998-10-12',P2,'Cabinet appointment / additional charge'),
('Chief Minister, Delhi','October–3 December 1998','First woman Delhi CM. Resignation tendered 28 November; appointment day differs across collected accounts (12/13 October).',[2,3,41],None,'1998-12-03',P2,'Executive appointment; Assembly accountability'),
('Delhi MLA, Hauz Khas','Elected November 1998','Won personally; exact Assembly resignation date uncollected.',[9],None,None,P2,'Direct election'),
('Rajya Sabha member: second term','April 2000–April 2006','Returned to the Upper House after the Bellary defeat.',[2,10],None,None,P2,'Indirect election'),
('Union Information and Broadcasting','30 September 2000–29 January 2003','Third period heading I&B.',[3],'2000-09-30','2003-01-29',P2,'Cabinet appointment'),
('Union Health and Family Welfare; Parliamentary Affairs','29 January 2003–22 May 2004','Combined health administration and parliamentary coordination responsibilities.',[3],'2003-01-29','2004-05-22',P2,'Cabinet appointment'),
('Chair, parliamentary Home Affairs committee','August 2004–2009','Committee scrutiny role, distinct from running the Home Ministry.',[3],None,None,P3,'Parliamentary committee appointment'),
('Rajya Sabha member: third term','April 2006–May 2009','Third election; term ended with return to Lok Sabha.',[2],None,None,P3,'Indirect election'),
('Lok Sabha MP, Vidisha','2009–2014','First Vidisha victory.',[11],None,None,P3,'Direct election'),
('Chair, parliamentary External Affairs committee','31 August 2009–1 January 2010','Brief committee chairmanship spanning transition to opposition leadership.',[3],'2009-08-31','2010-01-01',P3,'Parliamentary committee appointment'),
('BJP Lok Sabha leader / Leader of Opposition','21 December 2009–May 2014','First woman Lok Sabha Leader of Opposition; party leadership and institutional office are related but distinct.',[2,3],'2009-12-21',None,P3,'Parliamentary party selection / recognition'),
('Lok Sabha MP, Vidisha','2014–2019','Second Vidisha term; did not seek re-election in 2019.',[11,36],None,None,P4,'Direct election'),
('Union External Affairs Minister','May 2014–May 2019','First full-time woman EAM; allocation dated 27 May 2014, distinct from oath day.',[1,2,14],'2014-05-27',None,P4,'Cabinet portfolio allocation'),
('Union Overseas Indian Affairs','Allocated May 2014; end-date reconciliation pending','Held Overseas Indian Affairs alongside External Affairs; precise cessation/merger notification not inspected.',[14],'2014-05-27',None,P4,'Additional Cabinet portfolio')]
for n,(title,period,finding,ids,start,end,phase,route) in enumerate(offices,1):
    ck={'Finding':ids}
    if start: ck['Start date']=[14] if n in (21,22) else [3]
    if end: ck['End date']=[3]
    add('Offices & Party',f'OF{n:02d}',{'Position / institution':title,'Period':period,'Finding':finding,'Selection route':route,'Start date':start,'End date':end},ids,phase=phase,context=f'E{phases.index(phase)+1}02',checked=ck)

policies=[
('Film industry status and finance','In 1998 she explained how industry recognition enabled institutional finance for film production and exhibition.','Administrative recognition / financing access','I&B minister explaining the financing mechanism','No inspected lending series isolates her effect; piracy and informal finance remained separate problems.',[15],P2,'E204'),
('Delhi cost-of-living and services','In the 1998 campaign she defended onion imports and ration supply measures amid price and service complaints.','Reported implementation / contested campaign claims','Chief Minister during a short pre-election transition','Inherited power/water problems and a brief tenure limit attribution; no independent outcome audit inspected.',[40],P2,'E203'),
('Tobacco-control legislation','Piloted the tobacco regulation bill in Lok Sabha on 30 April 2003, addressing advertising and passive-smoking concerns.','Legislative passage','Health Minister; parliamentary sponsor','The draft and committee work predated her health tenure. Passage is not proof of subsequent compliance or lower mortality.',[16],P2,'E202'),
('Six AIIMS-type institutions / PMSSY','The Prime Minister announced six AIIMS-type hospitals in August 2003, during her health tenure; PMSSY approval followed in March 2006.','Announcement, then later approval','Minister during announcement; collective government initiative','Do not say she opened six hospitals or personally delivered the later programme.',[17,3],P2,'E204'),
('Women’s reservation advocacy','In March 2010 she supported party discipline for the women’s reservation bill in Lok Sabha.','Advocacy / party management','Opposition leader working with other BJP leaders','The cited episode does not establish Lok Sabha passage or enactment.',[31],P3,'G07'),
('MADAD consular portal','The ministry launched MADAD on 21 February 2015 for consular grievances and tracking.','Service launched','Institutional reform during her EAM tenure','Later descriptions confirm the launch; current features and resolution totals are not backdated.',[19,14],P4,'E406'),
('Operation Raahat, Yemen','Her parliamentary statement reported 4741 Indians and 1947 foreign nationals evacuated by 18 April 2015.','Evacuation output; dated government count','Calls to Saudi counterpart and inter-agency coordination; PM, V.K. Singh, missions and transport agencies also acted','6688 people is the sum of those dated counts. Later reporting vintages differ; this is not a timeless final total.',[18],P4,'E405'),
('Bangladesh boundary measure','Piloted the inherited boundary bill and helped build parliamentary and state-level agreement; both Houses passed it in May 2015.','Legislative passage / negotiation','Ministerial sponsorship and coalition-building','1974 agreement, 2011 protocol and 2013 introduction predated her ministry; no sole-authorship claim.',[21,46],P4,'E409'),
('Pakistan Comprehensive Bilateral Dialogue','The 9 December 2015 joint statement agreed a dialogue framework and assigned modalities to foreign secretaries.','Diplomatic agreement on process','Met Pakistani leadership during Heart of Asia conference','An agreed mechanism does not establish that talks were sustained or disputes resolved.',[24],P4,'E405'),
('Passport-document reform','December 2016 changes allowed one parent or legal guardian details and eased marital-status documentation and self-declarations.','Reform announced','Accepted MEA/Women and Child Development committee recommendations','Shared inter-ministerial authorship; independent effects on take-up and exclusion not measured here.',[20],P4,'G07'),
('India–US inaugural 2+2','Candidate official statement identifies the 2018 ministerial dialogue and COMCASA; the original body could not be retrieved.','Candidate evidence / not reviewed','Reported joint ministerial forum','Kept visible as a research lead, not certified from a search extract.',[22],P4,'E405'),
('OIC engagement','Addressed the OIC as guest of honour on 1 March 2019 and argued that counterterrorism should not target a religion.','Diplomatic speech','Invited EAM, presenting the government’s position','The invitation and speech do not prove lasting shifts in OIC policy toward India.',[23],P4,'E405'),
('Jadhav consular litigation: attribution boundary','The ICJ’s July 2019 judgment found consular-rights violations and required review and reconsideration, with an execution stay.','Judicial outcome after her ministerial tenure','Relevant to the consular agenda, but a government and legal-team undertaking','The Court did not order release or exonerate Jadhav. Personal litigation authorship and current custody status are not established here.',[25,1],P4,'E402')]
for n,(title,finding,stage,role,limit,ids,phase,ctx) in enumerate(policies,1):
    add('Policy & Governance',f'PG{n:02d}',{'Initiative / decision':title,'Finding':finding,'Stage':stage,'Documented role':role,'Outcome / attribution limit':limit},ids,'Analysis',phase,ctx,status='Not reviewed' if n==11 else 'Supported')

ideas=[
('Formation across political networks','Her 2007 self-description combines an RSS family, ABVP activism and socialist marital connections; it should not be reduced to a single organizational pathway.',[4],P1,'G03','Attributed position'),
('Nationalism and foreign-origin leadership','She defended her 2004 threatened protest against Sonia Gandhi becoming PM as patriotic. This records her justification, not proof that the protest determined the succession.',[4],P3,'G08','Attributed position'),
('Inflation and growth','In the same interview she argued that headline economic growth did not remove the political importance of inflation control.',[4],P3,'E304','Attributed position'),
('Institutional financing','Her film-sector intervention used access to formal finance as a policy mechanism; the inspected evidence does not establish a comprehensive economic doctrine.',[15],P2,'E204','Analysis'),
('Parliamentary persuasion','The boundary-bill episode illustrates negotiation across party and state lines. It is a concrete example, not proof of universal consensus-building.',[21,46],P4,'E407','Analysis'),
('Citizen-facing diplomacy','Evacuation coordination and grievance systems placed individual consular needs within the ministry’s public work. Visibility and responsiveness are distinct from independently measured service quality.',[18,19,32],P4,'E406','Analysis'),
('Cultural symbolism','Her 2014 Gita proposal drew a parliamentary secularism objection. It demonstrates contested religious symbolism, not an enacted national-scripture policy.',[35],P4,'E408','Analysis'),
('Pluralist diplomatic language','At the OIC she invoked religious diversity and rejected equating counterterrorism with confrontation against a faith. This is her public diplomatic argument.',[23],P4,'E405','Attributed position'),
('Party loyalty and parliamentary civility','A retrospective Indian Express editorial presents her as ideologically committed yet personally civil, operating within leadership structures. Treat this as an attributed assessment.',[32],P3,'E307','Analysis'),
('Final Jammu and Kashmir message','The Rajya Sabha obituary recorded her final welcome for the government’s Jammu and Kashmir decision. The tribute establishes the message, not a detailed constitutional argument or legislative vote.',[2],P4,'E402','Attributed position')]
for n,(topic,finding,ids,phase,ctx,typ) in enumerate(ideas,1): add('Ideas & Political Method',f'IM{n:02d}',{'Topic':topic,'Finding':finding},ids,typ,phase,ctx)

controversies=[
('Lalit Modi travel assistance, 2015','Her acknowledged intervention over UK travel documents prompted Congress demands for resignation and conflict-of-interest questions.','She cited his wife’s cancer treatment and asked the UK to apply its rules; the UK Home Office said rules were followed.','Political/ethical controversy reported June 2015; no inspected judicial finding against Swaraj.',[26,27],P4,'Admission and defence share the minister’s tweet origin; two newsrooms do not independently prove motives.'),
('Iraq hostages: assurances and death announcement','Critics and families contrasted earlier assurances with the March 2018 confirmation of 39 deaths.','She said she required concrete evidence, cited DNA identification and defended informing Parliament first.','Deaths confirmed 20 March 2018; no adjudicated misconduct finding established in the inspected material.',[28,29],P4,'Her protocol explanation is attributed, not verified as a legal rule; no inference that intelligence claims were knowingly false.'),
('Foreign-origin PM protest, 2004','Her threatened symbolic protest against Sonia Gandhi becoming PM remains a contested episode of nationalist politics.','In the 2007 interview she defended the proposed protest as patriotic and political, not a personal attack.','Political controversy; interview records her defence, not a court ruling or proof of electoral causation.',[4],P3,'Single primary interview supports her position. Opponent interpretations require further direct sourcing.'),
('Reddy brothers association, 2011','Bellary political links and annual puja visits raised questions about her relationship with the Reddy brothers.','She denied arranging their ministerial appointments or protecting them; NDTV later reported her absence from the annual puja.','Public denial in May 2011 and reported distancing in August; no inspected finding of mining wrongdoing by Swaraj.',[33,34],P3,'Association is not proof of complicity; the puja absence cannot independently establish her motives.'),
('Gita national-scripture proposal, 2014','A Lok Sabha intervention criticised the reported proposal as inconsistent with constitutional secularism.','The cited debate reproduces the proposed recognition, but does not contain a full reply from Swaraj to this objection.','Parliamentary criticism on 11 December 2014; no enactment established.',[35],P4,'The objection is one MP’s position. Full original speech and ministerial response remain gaps.'),
('Delhi government defeat, 1998','BJP lost Delhi amid reported service and cost-of-living problems, although Swaraj won Hauz Khas personally.','During the campaign she defended onion imports and ration measures; after defeat she tendered her resignation.','Resignation submitted 28 November 1998; historical profile gives caretaker tenure through 3 December.',[40,41,3],P2,'Short tenure and inherited problems preclude attributing the entire party defeat to one leader.')]
for n,(matter,finding,response,proc,ids,phase,note) in enumerate(controversies,1):
    ck={'Finding':ids,'Response':ids,'Procedural status':ids}
    if n==1: ck['Response']=[26]
    if n==2: ck['Response']=[29]
    add('Controversies',f'CV{n:02d}',{'Matter':matter,'Finding':finding,'Response':response,'Procedural status':proc},ids,'Analysis',phase,f'E{phases.index(phase)+1}02',checked=ck,note=note,priority='High')

legacy=[
('Institutional firsts','Her firsts in Delhi, Lok Sabha opposition leadership and full-time External Affairs are securely recorded. Symbolic access does not by itself measure gains for women as a group.',[2],'Institutional record; bounded interpretation','G02'),
('Consular leadership','Citizen-facing diplomacy is a defensible legacy theme, grounded in evacuation and service mechanisms. Government teams and agencies share the record; personal visibility is not a causal estimate.',[18,19,32],'Documented actions and attributed editorial assessment','E410'),
('Parliamentary range','Her career spans executive work, committee scrutiny and opposition leadership. Boundary-bill negotiation offers a concrete instance of parliamentary coordination.',[2,3,21],'Synthesis of roles and a documented episode','E407'),
('Limits of the administrative record','Film financing, tobacco legislation and passport reform show different kinds of intervention. Comparable long-run outcome measures were not collected and should not be implied.',[15,16,20],'Outcome assessment remains incomplete','E210'),
('Contested remembrance','Commemorative portrayals coexist with unresolved accountability debates over travel assistance and Iraq assurances. Neither tributes nor accusations settle every contested question.',[1,26,28,29],'Competing records, not an aggregate moral score','E410'),
('Gendered visibility','Maternal imagery and the 2018 gender/religion-based abuse show that high office did not eliminate gendered treatment. One case study cannot estimate its career-wide prevalence.',[30,32],'Attributed research and retrospective commentary','G06'),
('Padma Vibhushan','Posthumous Padma Vibhushan for Public Affairs, award year 2020; notification/investiture chronology extends into 2021.',[37],'Official recognition','G10'),
('Foreign-service institute renaming','The institutional search index reports renaming on 14 February 2020. Original page retrieval failed; the exact date is retained as a research lead.',[38],'Not reviewed; source retrieval pending','E410')]
for n,(theme,assessment,ids,assessor,ctx) in enumerate(legacy,1):
    add('Legacy & Assessments',f'LA{n:02d}',{'Theme':theme,'Assessment':assessment,'Assessor / basis':assessor},ids,'Analysis',context=ctx,status='Not reviewed' if n==8 else 'Supported')

add('Policy & Governance','PG14',{'Initiative / decision':'Private-member welfare and education bills','Finding':'The Rajya Sabha register records her proposals on women’s safety, girls’ education and welfare in 2005, and workplace harassment, mother-tongue primary education and senior citizens in 2006; these bills lapsed.','Stage':'Introduced; lapsed','Documented role':'Private member introducing bills in opposition','Outcome / attribution limit':'No claim that these became law or that later government legislation was authored by her.'},[47],'Analysis',P3,'G07')

from author_context import populate_context, coverage
populate_context(add,phases)
def gap(n,topic,detail,action,records,priority='Normal'):
    gaps.append({'id':f'Q{n:02d}','priority':priority,'topic':topic,'gap':detail,'next_action':action,'status':'Open','record_ids':records})
gap(1,'Original election returns','Several Assembly and Lok Sabha results rely on identified secondary tables.','Retrieve original ECI/CEO constituency returns; reconcile spellings and exact poll dates.',['EL01','EL03','EL04','EL07','EL09','EL10','EL13','EL14'],'High')
gap(2,'Vote-share denominators','1996 and Vidisha shares omitted; different reported denominator conventions remain unresolved.','Inspect full returns and distinguish valid candidate votes, NOTA, rejected ballots and all votes polled.',['EL07','EL13','EL14'],'High')
gap(3,'Rajya Sabha allocations','Election years/terms are confirmed; state allocations, reorganization and vote counts not passage-verified.','Obtain election and allocation gazettes for 1990, 2000, 2006 and Uttar Pradesh reorganization.',['EL06','EL11','EL12'])
gap(4,'Precise office boundaries','Delhi appointment day differs (12/13 October); Delhi MLA and South Delhi vacancy dates, MOIA cessation need primary notices.','Inspect Delhi gazette and Parliament/Union portfolio notifications.',['OF08','OF10','OF11','OF22'])
gap(5,'2018 India–US 2+2','State archive returns technical error and Defense mirror 403.','Retrieve a usable official mirror of the full joint statement before upgrading the claim.',['PG11'])
gap(6,'Posthumous institute renaming','SSIFS pages failed; only indexed institutional wording available.','Find the dated MEA renaming announcement or institutional annual report.',['LA08'])
gap(7,'Independent policy outcomes','No comparable causal evaluations collected for financing, passports, consular access or health effects.','Collect implementation audits, access data and outcome studies; separate programme age from minister tenure.',['PG01','PG03','PG04','PG06','PG10'])
gap(8,'Controversy procedural records','Reviewed reports do not establish judicial misconduct findings; full later procedural histories uncollected.','Search relevant parliamentary motions and court records for a specific legal follow-up question; avoid inferring exoneration.',['CV01','CV02','CV04'],'High')
gap(9,'Original Gita speech and response','Parliamentary objection is inspected; complete original proposal/reply not collected.','Retrieve original 2014 event speech and any parliamentary ministerial response.',['CV05','IM07'])
gap(10,'Gender and social comparison','Institutional milestones and a documented harassment episode are stronger than evidence of nomination barriers or representative effects.','Seek contemporary candidate-selection, media and constituency studies with matched comparisons.',['G01','G04','G05','G09','E108','E208','E308'])
gap(11,'Early economic and international context','Direct links between broad era conditions and her early choices remain unestablished.','Add historical scholarship and contemporary policy records before advancing causal claims.',['E104','E105','E205','E305'])
gap(12,'Party organization chronology','The workbook verifies broad affiliations and Lok Sabha leadership; exact spokesperson and party-secretary appointment boundaries remain uncollected.','Retrieve BJP organizational records and contemporaneous appointment reports.',['OV04','OF19'])

base=Path(__file__).parent
data={'schema_version':1,'subject':'Sushma Swaraj','as_of':ASOF,'guidance':'Ten gender dimensions cover the career; ten era dimensions are examined in each of four phases. Formal powers, documented choices and outcome claims remain separate. Absence of collected evidence is not evidence of absence.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'gaps':gaps,'coverage':coverage,'phases':phases}
(base/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(base/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),'claims':len(claims),'evidence':len(evidence),'gaps':len(gaps)}))
