"""Reproducible offline authoring; no network or temporary-file dependencies."""
import hashlib,json
from pathlib import Path
from author_sources import sources,retrievals,ASOF
ROOT=Path(__file__).resolve().parent
tables={};claims=[];evidence=[]
S={s['Source ID']:s for s in sources};R={r['id']:r for r in retrievals}
phases=['P1 | Technical training, advice and Congress entry, 1970s–2003','P2 | UPA strategy, Parliament and environmental regulation, 2004–July 2011','P3 | Rural development and legislative reform, July 2011–May 2014','P4 | Parliamentary opposition, writing and communications, 2014–2026']
gender_items=['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time']
era_items=['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']
layouts={'Overview':['Overview ID','Topic','Finding / value'],'Context & Constraints':['Context ID','Career phase','Coverage item','Finding'],'Career Timeline':['Timeline ID','Period','Event','Finding'],'Elections':['Election ID','Year','Jurisdiction','Result','Finding'],'Offices & Party':['Position ID','Title','Period','Finding'],'Policy & Governance':['Policy ID','Initiative','Finding'],'Ideas & Political Method':['Idea ID','Topic','Finding'],'Controversies':['Matter ID','Matter','Finding'],'Legacy & Assessments':['Assessment ID','Theme','Finding']}
for name,lead in layouts.items():tables[name]={'lead_columns':lead,'date_columns':['Start date','End date','Election date'],'rows':[]}
def ids(ns):return [f'S{n:03d}' for n in ns]
def add(sheet,rid,fields,ns=(),kind='Recorded fact',phase=None,proof=None,status='Supported',note='',independent=False):
    row={layouts[sheet][0]:rid,**fields,'Claim type':kind,'Source IDs':'; '.join(ids(ns))}
    if phase:row['Career phase']=phases[phase-1]
    if note:row['Research note']=note
    row['Corroboration']='Primary record' if ns and any(S[x]['Primary or secondary']=='Primary' for x in ids(ns)) else 'Single credible source' if len(ns)==1 else 'Multiple cited sources'
    tables[sheet]['rows'].append(row)
    if kind=='Method / scope':return row
    if proof is None:proof={('Finding / value' if sheet=='Overview' else 'Finding'):ns}
    for i,(field,ss) in enumerate(proof.items(),1):
        cid=f'{rid}.{i:02d}';c={'id':cid,'sheet':sheet,'record_id':rid,'field':field,'statement':row[field],'fingerprint':hashlib.sha256(json.dumps(row[field],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':kind,'status':status,'priority':'High' if sheet in ['Overview','Elections','Controversies'] else 'Medium','candidate_source_ids':ids(ss),'evidence_ids':[],'contradictions':[],'review_note':note or ('Bounded synthesis of linked evidence; no causal estimate.' if kind=='Analysis' else 'Field wording checked against identified passages; attributions remain attributed.')}
        if independent and status=='Supported':c['requires_independent_corroboration']=True
        if status in ['Supported','Partially supported','Disputed']:
            for j,sid in enumerate(ids(ss),1):
                ret=R['R'+sid[1:]];eid=f'E-{cid}-{j}'
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':ret['id'],'locator':ret['locator'],'passage_paraphrase':ret['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex passage review','reviewed_at':ASOF,'note':'Supports the relevant component; combined sources support compound wording. A dispute record documents competing versions rather than validating either count.'})
                c['evidence_ids'].append(eid)
        claims.append(c)
    return row

OV=[
('Identity','Jairam Ramesh (also styled Shri Jairam Ramesh), born 9 April 1954 in Chikmagalur, Karnataka; Indian National Congress politician, policy specialist and author.',[1,5],'Recorded fact'),
('Education','B.Tech., M.S. and graduate study, at IIT Bombay, Carnegie Mellon University and MIT respectively. Graduate study is not presented as an MIT doctorate.',[1],'Recorded fact'),
('Current roles','Fourth-term elected Rajya Sabha MP from Karnataka; present term began 1 July 2022. Congress general secretary responsible for communications, publicity and media, including digital media.',[4,5,47],'Recorded fact'),
('Career pathway','Technical and economic-policy assignments preceded Congress strategy, indirect parliamentary election and Union ministries. Influence rests substantially on policy expertise and party access.',[1,2,3,48],'Analysis'),
('Electoral record','Four confirmed Rajya Sabha elections: Andhra Pradesh in 2004 and 2010, Karnataka in 2016 and 2022. These are indirect state-representative elections; party campaign outcomes are separate.',[1,6,9,51],'Recorded fact'),
('Executive scope','Held junior Commerce and Power portfolios, independent charge of Environment and Forests, and cabinet responsibility for Rural Development with a period of additional Drinking Water and Sanitation charge.',[1],'Recorded fact'),
('Environmental contribution','The Bt-brinjal moratorium, Niyamgiri forest-clearance decision and NGT establishment made environmental regulation a prominent part of his record. POSCO shows that his approach also permitted conditional development.',[12,14,15,17,18],'Analysis'),
('Legislative contribution','Helped steer the 2013 land-acquisition legislation. Its consent, social-impact, compensation and rehabilitation framework is a documented institutional contribution; later distributional outcomes are less firmly established here.',[21,22,23],'Analysis'),
('Rural-development attribution','Administered inherited rural programmes and women’s SHG credit expansion. NRLM launched on 3 June 2011, before his July appointment, so founding the mission is not credited to him.',[1,25,26,27],'Analysis'),
('Opposition and constitutional method','Used parliamentary debate, committee scrutiny and litigation. He supported Aadhaar’s underlying idea while contesting its Money Bill route; review petitions were dismissed in 2021 with a dissent.',[33,34,36,50],'Analysis'),
('Political communication','Communications appointment in June 2022 built on earlier strategy work. His yatra commentary connected party mobilisation to possible opposition cooperation, without proving a personal electoral effect.',[2,11,38],'Analysis'),
('Contested record','Critics challenged the Bt-brinjal freeze, POSCO clearance and aspects of his public rhetoric. These policy and political disputes differ from the Doval defamation proceedings and the ECI request for evidence.',[13,15,16,29,39,40,46],'Analysis'),
('Doval case — precise outcome','Apologised in December 2020. A January 2021 High Court order records his discharge on 19 December 2020 and transfer of the remaining case against other parties. This is not a conviction.',[39,40],'Recorded fact'),
('Intellectual and historical work','His publications combine insider policy documentation with historical biography, including Green Signals and A Chequered Brilliance. Author and publisher claims are distinguished from independent assessment.',[42,43,49],'Analysis'),
('Gender and social effects','Women’s SHGs and sanitation outreach had explicit gender relevance. Evidence of programme design and contemporary support is stronger than evidence of personal causal impact on women’s autonomy or safety.',[25,27,28,30],'Analysis'),
('Main open questions','The 2016 legislator vote count conflicts across reports; the official declaration confirms victory but not the count. Original 2004/2010/2022 detailed returns, policy outcomes and several gender mechanisms remain gaps.',[1,6,7,8,9,51],'Analysis')]
for i,(t,f,ns,k) in enumerate(OV,1):add('Overview',f'OV{i:02d}',{'Topic':t,'Finding / value':f},ns,k)
for i,(t,f) in enumerate([
 ('Scope and cutoff','Snapshot as of 16 November 2026. Four career phases, 40 era-context items and ten gender items. Source dates differ; historical findings are not live case-status certificates.'),
 ('How to read','Findings and review status appear first. Expand grouped columns for dates, role, implementation and cautions. All citations opens each source; Claims and Evidence preserve passage-level checks.'),
 ('Evidence meaning','Supported applies to the registered field, including explicit attribution or bounded analysis. It is not a completeness score. Unreviewed research limitations are not proof of absence. Blank counts mean unavailable or inapplicable, never zero.'),
 ('Election units','Rajya Sabha ballots are cast by elected legislators. Popular-vote shares and single-opponent victory margins are not calculated. The reported 2022 count is a first-preference tally; 2016 is withheld.'),
 ('Confirmed Rajya Sabha elections (calculated)',4),('Confirmed direct constituency contests in this register (calculated)',0)],17):add('Overview',f'OV{i:02d}',{'Topic':t,'Finding / value':f},kind='Method / scope')

TL=[
('1954-04-09','Birth','Born in Chikmagalur; later obtained engineering and public-management qualifications.',[1],1),
('1970s','Higher education','Studied at IIT Bombay, Carnegie Mellon and MIT; official profile distinguishes degrees from graduate study.',[1],1),
('1983–1989','Technical policy assignments','Worked on energy policy, CSIR reorganisation and technology missions.',[3],1),
('1991–1994','Economic policy advice','Advised the Prime Minister in 1991 and the Planning Commission deputy chairman in 1992–94.',[2],1),
('1996–1998','Finance advice','Served as adviser to the finance minister.',[2],1),
('1998–2003','Congress organisation','Official profile records AICC office-bearing alongside state economic-policy assignments.',[1,2],1),
('2000–2002','Karnataka Planning Board','Served as deputy chairman of the state Planning Board.',[1],1),
('2004','UPA strategy and Parliament','Participated in Congress strategy and Common Minimum Programme preparation; first elected to Rajya Sabha in June.',[1,2],2),
('2006-01-31','Commerce ministry','Became Minister of State in the Department of Commerce.',[1],2),
('2008-04-06','Concurrent Power assignment','Added a junior Power portfolio while continuing Commerce.',[1],2),
('2009-02-25','End of junior ministries','Official profile ends both Commerce and Power tenures on this date.',[1],2),
('2009-05-28','Environment and Forests','Took independent charge as Minister of State.',[1],2),
('2009–2010','Climate diplomacy','Represented India in the Copenhagen/BASIC process and led its delegation at Cancun.',[19,20],2),
('2010-02-09','Bt-brinjal moratorium','Commercialisation paused following public consultations and concerns recorded by the ministry.',[12],2),
('2010-06-07','Second Rajya Sabha election','Returned unopposed from Andhra Pradesh.',[6],2),
('2010-08-24','Niyamgiri decision','Ministry denied Stage-II forest clearance for the bauxite mining proposal.',[14],2),
('2010-10-18','NGT established','Specialised environmental tribunal created during his tenure.',[17,18],2),
('2011-01; 2011-05','POSCO clearances','Environmental approval with conditions followed by forest approval; contested in later proceedings.',[15,16],2),
('2011-07-12','Rural Development cabinet post','Shifted to Rural Development; additional Drinking Water and Sanitation responsibility began 13 July.',[1],3),
('2012-09–2012-10','Sanitation mobilisation','Promoted Nirmal Bharat outreach; comments comparing sanitation with temples drew criticism and support.',[28,29,30],3),
('2013','Land legislation and Telangana GoM','Steered land-acquisition amendments and participated in collective preparation for Andhra Pradesh bifurcation.',[21,31],3),
('2014-05-26','End of Union ministry','Rural Development tenure ended; subsequent work centred on Parliament and opposition.',[1,33,50],4),
('2015–2016','Defence of land law; Aadhaar dispute','Opposed changes to land protections and disputed Aadhaar’s Money Bill route while supporting its basic concept.',[33,50],4),
('2016-06-11; 2016-06-20','State representation transition','Elected from Karnataka, then resigned his Andhra Pradesh seat on 20 June.',[10,51],4),
('2019–2024','Committee leadership','Chaired the science/environment committee in two documented periods separated by the 2022 term transition.',[35,36],4),
('2020-12-19; 2021-01-11','Separate legal dispositions','Doval case discharge followed apology; Aadhaar review petition was dismissed in a separate constitutional matter.',[34,39,40],4),
('2022-06','Fourth election and communications post','Won again from Karnataka and was appointed Congress communications general secretary.',[9,11],4),
('2023–2024','Yatra and campaign communication','Discussed opposition outreach through the yatra; ECI later required evidence for a campaign allegation about DMs.',[38,46],4),
('2024–2026','Continuing opposition role','Ceased to chair the science/environment committee, continued as member, and remained Congress communications chief in current records.',[5,35,37,47],4)]
for i,(p,t,f,ns,phase) in enumerate(TL,1):add('Career Timeline',f'T{i:02d}',{'Period':p,'Event':t,'Finding':f},ns,phase=phase)

for i,year,place,date,f,ns,votes in [
 (1,2004,'Andhra Pradesh (undivided)',None,'First Rajya Sabha election in June 2004; indirect state representation. Exact declaration date and original detailed return not established.',[1,2],None),
 (2,2010,'Andhra Pradesh (undivided)','2010-06-07','Re-elected unopposed on 7 June 2010; no contested ballot tally or popular-vote share applies.',[1,6],None),
 (3,2016,'Karnataka','2016-06-11','Official Form 23 confirms election. Indian Express reports 47 votes, Times of India 46; numeric count withheld pending an official count sheet.',[7,8,51],None),
 (4,2022,'Karnataka','2022-06-10','Won; reported 46 first-preference legislator votes. Fourth term began 1 July 2022.',[4,9],46)]:
    row={'Year':year,'Jurisdiction':place,'Result':'Won','Finding':f,'Election date':date,'House / route':'Rajya Sabha / indirect','Party':'Indian National Congress','Candidate status':'Elected by state legislators','Candidate votes':votes,'Opponent votes':None,'Vote share':None,'Signed vote margin':None,'Count qualification':'Unavailable or inapplicable except reported 2022 first-preference tally; no head-to-head margin.','Term note':'2004/2010 Andhra Pradesh; 2016/2022 Karnataka. Election date is distinct from term commencement.'}
    add('Elections',f'EL{i:02d}',row,ns,phase=2 if i<3 else 4,status='Supported',proof={'Finding':ns,**({'Candidate votes':[9]} if votes else {})})
add('Elections','EL05',{'Year':None,'Jurisdiction':'India','Result':'Not a personal contest','Finding':'Congress strategy and communications roles in Lok Sabha campaigns do not establish a direct electoral mandate for Ramesh. No direct constituency contest is confirmed in this register.','House / route':'Party campaigning / not personally contesting','Party':'Indian National Congress','Candidate status':'Campaign strategist / communicator','Candidate votes':None,'Opponent votes':None,'Vote share':None,'Signed vote margin':None},[2,11,38,48],'Analysis',phase=4)
add('Elections','EL06',{'Year':2016,'Jurisdiction':'Karnataka','Result':'Count disputed','Finding':'Competing reported 2016 counts are 47 (S007) and 46 (S008). Form 23 supplies no count. Both versions remain visible; neither is entered as a verified total.','House / route':'Evidence note / excluded from contest counts','Candidate votes':None,'Opponent votes':None,'Vote share':None,'Signed vote margin':None},[7,8,51],'Disputed/uncertain',phase=4,status='Disputed',note='Winner/date resolved by S051; vote-total discrepancy remains open.')
claims[-1]['contradictions']=['S007 assigns Ramesh 47 votes; S008 assigns 46. S051 confirms election without a count.']

OFF=[
('Adviser to Prime Minister','1991',None,None,'Advisory','Prime Minister’s Office',[2],1),
('Adviser to Deputy Chairman, Planning Commission','1992–1994',None,None,'Advisory','Planning Commission',[2],1),
('Adviser to Finance Minister','1996–1998',None,None,'Advisory','Finance Ministry',[2],1),
('AICC office-bearer','1998–2003',None,None,'Party','Indian National Congress',[1],1),
('Deputy Chairman, Karnataka State Planning Board','2000–2002',None,None,'State advisory/executive','Government of Karnataka',[1,2],1),
('Member, Rajasthan Development Council','1999–2003',None,None,'State advisory','Government of Rajasthan',[1,2],1),
('Economic adviser, Chhattisgarh government','2001–2003',None,None,'State advisory','Government of Chhattisgarh',[2],1),
('Rajya Sabha MP — first term, Andhra Pradesh','June 2004–2010',None,None,'Indirectly elected','Parliament',[1,2],2),
('National Advisory Council member','2004-era role; endpoint not fixed',None,None,'Advisory','National Advisory Council',[2],2),
('Minister of State, Department of Commerce','31 January 2006–25 February 2009','2006-01-31','2009-02-25','Ministerial','Commerce and Industry Ministry',[1],2),
('Minister of State, Power','6 April 2008–25 February 2009','2008-04-06','2009-02-25','Ministerial','Power Ministry',[1],2),
('Minister of State (Independent Charge), Environment and Forests','28 May 2009–12 July 2011','2009-05-28','2011-07-12','Ministerial','Environment and Forests Ministry',[1],2),
('Rajya Sabha MP — second term, Andhra Pradesh','June 2010–20 June 2016',None,'2016-06-20','Indirectly elected','Parliament',[1,6,10],2),
('Cabinet Minister, Rural Development','12 July 2011–26 May 2014','2011-07-12','2014-05-26','Ministerial','Rural Development Ministry',[1],3),
('Minister, Drinking Water and Sanitation — additional charge','13 July 2011–28 October 2012','2011-07-13','2012-10-28','Ministerial','Drinking Water and Sanitation Ministry',[1],3),
('Member, GoM on Andhra Pradesh bifurcation','2013 attendance documented',None,None,'Collective executive','Union Group of Ministers',[31],3),
('Member, Health and Family Welfare committee','November 2014–September 2019',None,None,'Parliamentary','Parliament',[1],4),
('Member, joint committee on Land Acquisition amendment bill — first period','May 2015–June 2016',None,None,'Parliamentary','Parliament',[1],4),
('Rajya Sabha MP — third term, Karnataka','July 2016–June 2022',None,None,'Indirectly elected','Parliament',[1,35,51],4),
('Chair, science/environment standing committee — first period','September 2019–June 2022',None,None,'Parliamentary','Parliament',[1,35],4),
('Chair, ad hoc committee on online pornography and effects on children','December 2019–February 2020',None,None,'Parliamentary','Rajya Sabha',[1],4),
('Rajya Sabha MP — fourth term, Karnataka','1 July 2022–in office','2022-07-01',None,'Indirectly elected','Parliament',[4],4),
('Chair, science/environment standing committee — second period','13 September 2022–June 2024','2022-09-13',None,'Parliamentary','Parliament',[35,36],4),
('Member, science/environment standing committee','September 2024–current directory',None,None,'Parliamentary','Parliament',[35,37],4),
('General Secretary, communications, publicity and media','16 June 2022–current directory','2022-06-16',None,'Party','Indian National Congress',[5,11,47],4)]
for i,(title,period,start,end,cat,org,ns,phase) in enumerate(OFF,1):
    note=''
    if i==2:note='Adviser to the deputy chairman; do not label him deputy chairman of the national Planning Commission.'
    if i==13:note='Resignation, not routine retirement on 21 June 2016; representation remained Andhra Pradesh after bifurcation.'
    if i in [14,15]:note='Uses explicit Rajya Sabha Who’s Who dates; several short online biographies give different boundary dates.'
    if i==18:note='Second period is recorded separately in OF26; no continuous service asserted across June–August 2016.'
    add('Offices & Party',f'OF{i:02d}',{'Title':title,'Period':period,'Finding':f'{title}, {org}; {period}.','Start date':start,'End date':end,'Position category':cat,'Institution':org,'Party during political office':'Indian National Congress','Concurrent roles / function':'Power overlapped Commerce; ministries overlapped Rajya Sabha membership. Party communications is distinct from a government portfolio.' if i in [10,11,12,14,15,25] else 'Role-specific authority; no executive power inferred from committee membership.'},ns,phase=phase,note=note)

POL=[
('2004 Common Minimum Programme','National coalition programme','Helped prepare the UPA Common Minimum Programme, according to the contemporary CV.','Negotiated / contributed','A coalition policy framework','Documented participation','Later UPA programmes involved Cabinet, Parliament, states and many policy actors; individual authorship or effects are not established.',[2],2),
('Bt-brinjal moratorium','Biosafety / agriculture','Announced a moratorium on commercialisation on 9 February 2010 after consultations.','Decided','Pause release while addressing scientific, public and state concerns','Moratorium documented in parliamentary answer','Decision and rationale are documented. Neither proof of harm nor proof of lost productivity follows from the moratorium alone.',[12,13],2),
('Niyamgiri forest clearance','Forests / Adivasi rights','Denied Stage-II forest clearance in August 2010; subsequent Supreme Court proceedings required Gram Sabha consideration of rights.','Decided','Apply forest and community-rights safeguards','Administrative denial; later judicial directions in 2013','Forest communities, activists, statutory committees, Odisha government and courts had separate roles; Ramesh did not personally issue the 2013 judgment.',[14],2),
('POSCO conditional clearances','Industrial development / environment','Granted conditional clearances in 2011 despite disagreement over assessment and forest-rights compliance.','Approved','Permit industrial development subject to safeguards','Environmental approval January 2011; forest approval May 2011; later tribunal challenge','Clearance is distinct from completed investment. Disputed assessment quality and community rights constrain an uncomplicated pro-environment narrative.',[15,16],2),
('National Green Tribunal','Environmental justice','Supported establishment of the specialist tribunal in 2010 and publicly described its institutional role.','Implemented / ministerial sponsor','Provide specialised environmental remedies','Established 18 October 2010','Institutional creation is clear. Judicial decisions and long-run effectiveness belong to the tribunal and wider legal system, not solely the minister.',[17,18],2),
('Copenhagen and Cancun diplomacy','Climate / international relations','Participated in BASIC-era climate diplomacy and led India’s Cancun delegation.','Negotiated','Combine development space with climate commitments','Government communicated voluntary GDP-emissions-intensity target; COP16 role documented','The 20–25% target used 2005 as baseline and 2020 as target year. It is not an absolute-emissions reduction or an independently verified outcome here.',[19,20],2),
('Land acquisition and rehabilitation law','Land / displacement','Steered amendments leading to the 2013 compensation, consent and rehabilitation framework.','Sponsored / negotiated','Make compulsory acquisition more participatory and protective','Act 30 of 2013 enacted','Consent applies to defined private/PPP cases and affected-family categories; social-impact and compensation rules have exceptions. State implementation and later changes need separate evaluation.',[21,22,23],3),
('MGNREGA administration','Rural employment','Administered an inherited employment-guarantee programme; ministry answered scrutiny over payment delays, permissible works and grievance mechanisms.','Inherited / implemented','Improve delivery and convergence','2014 status statement addressed 27 committee recommendations','The programme predates his ministry. The record establishes accountability topics, not their resolution or an effect attributable to one minister.',[1,24],3),
('NRLM / Aajeevika','Rural livelihoods','Oversaw implementation of a mission launched on 3 June 2011, before his appointment.','Inherited / implemented','Organise poor households, especially women, for finance and livelihood support','SGSY and NRLM overlapped until March 2013; transition completed in April 2013','Launch and implementation stages differ. SHG formation or loan availability alone does not establish household income or autonomy gains.',[1,25,26],3),
('Women’s SHG interest subvention','Gender / financial inclusion','Government expanded subsidised credit terms during his rural-development tenure.','Implemented with other institutions','Reduce borrowing costs for women’s SHGs','May 2013 approval; February 2014 upfront 7% terms, up to Rs3 lakh in 150 selected districts; prompt repayment could reduce effective rate to 4%','Banking framework and rollout documented. Finance Ministry, RBI, NABARD, banks and states shared implementation; no personal causal estimate.',[25,27],3),
('Nirmal Bharat outreach','Sanitation','Promoted sanitation demand generation using a yatra, celebrity advocacy and proposed community-worker/SHG participation.','Led public advocacy','Expand sanitation demand and social participation','September 2012 launch plans and outreach statements','Announcements and rhetorical priority are documented. The ten-year ODF aspiration is not recorded as achieved; no tenure-bounded impact estimate is available.',[28,29,30],3),
('Andhra Pradesh bifurcation preparation','Federalism / state formation','Participated in the GoM chaired by Sushilkumar Shinde; Parliament subsequently enacted reorganisation.','Member of collective process','Prepare institutional and administrative arrangements','Official GoM attendance and reorganisation statute','Do not call him sole architect. Statehood movement, Cabinet, Parliament and affected regions were independent actors; settlement of later disputes not assessed.',[31,32],3),
('Opposition to land-law amendments','Agrarian policy / opposition','Opposed proposed exemptions from consent and social-impact safeguards after 2014.','Opposed','Preserve protections of the 2013 framework','Public opposition statement and comparative legislative brief','Opposition is documented; any claim that his intervention alone defeated or reshaped legislation would need further evidence.',[23,50],4),
('Aadhaar legislative procedure challenge','Constitutional process','Supported identity-linked subsidy reform while contesting certification as a Money Bill.','Challenged / litigated','Protect legislative scrutiny and safeguards','Review petition dismissed on 11 January 2021 by majority; dissent would await larger-bench consideration','Not an anti-Aadhaar position in principle. Litigation did not secure the requested review; the broader reference’s later status is not resolved here.',[33,34],4),
('Science and technology budget oversight','Parliamentary scrutiny','Chaired the committee that issued the 369th report on government responses to science-budget recommendations.','Chaired','Track departmental responses','Six accepted, six no longer pursued, four awaiting final replies out of 16','Report categories are collective parliamentary outputs; acceptance does not certify expenditure, research quality or impact.',[36],4),
('Environment committee membership after 2024','Parliamentary scrutiny','Continued as a committee member after chairmanship ended.','Member','Participate in oversight','Membership appears in the current PRS list','Membership alone does not establish authorship of each later report or a change in government policy.',[35,37],4),
('Energy, technology and economic advice','Technical policy','Worked on energy policy, technology missions and economic advice before elected office.','Advised','Supply technical and economic policy input','Official biography documents assignments','No independent allocation of 1991 reform credit or quantified impact is attempted; advice differs from Cabinet decision-making.',[2,3],1),
('Children and online content scrutiny','Child protection / digital media','Chaired a Rajya Sabha ad hoc committee on online pornography and its effects on children and society in 2019–2020.','Chaired','Examine harms and policy responses','Chairmanship recorded for December 2019–February 2020','This source verifies role. Recommendations, civil-liberties trade-offs and uptake require the full report and action-taken evidence.',[1],4)]
for i,(title,domain,f,role,obj,adopt,attr,ns,phase) in enumerate(POL,1):
    add('Policy & Governance',f'PG{i:02d}',{'Initiative':title,'Finding':f,'Policy domain':domain,'Figure’s role':role,'Stated objective / analytical purpose':obj,'Adoption / implementation evidence':adopt,'Attribution and outcome limit':attr,'Outcome measure':'No independently identified personal causal estimate in this register.'},ns,'Analysis',phase=phase,proof={'Finding':ns,'Adoption / implementation evidence':ns,'Attribution and outcome limit':ns})

IDEAS=[
('Technocratic route','Specialist advice, committee work and policy drafting supplied influence alongside party organisational access. This is a synthesis of roles, not a claim of political neutrality.',[1,2,3],1),
('Growth with ecological limits','In the Yale interview, Ramesh argued for faster growth constrained by ecological security. Treat this as his stated position, not a measured policy balance.',[44],4),
('Law and development','His OUP essay frames unauthorised industrial expansion as a legal-compliance issue rather than an unavoidable conflict between environment and development.',[45],4),
('Public consultation','Bt-brinjal consultations made public and state-government concerns part of ministerial decision-making. Critics questioned the weight accorded to opposition relative to expert clearance.',[12,13],2),
('Conditional development','The differing Niyamgiri and POSCO decisions show case-dependent choices. Their consistency remains contested; neither blanket industrial obstruction nor automatic clearance describes the record.',[14,15,16],2),
('Climate pragmatism','BASIC cooperation and voluntary emissions-intensity commitments combined international engagement with defence of domestic development space.',[19,20],2),
('Rights within development','Land-law interventions foreground consent, compensation, rehabilitation and social impact. This did not remove all state powers of compulsory acquisition.',[21,22,50],3),
('Bicameral scrutiny','His Aadhaar position distinguishes the policy idea from the legislative route; litigation extended parliamentary objections into constitutional adjudication.',[33,34],4),
('Organisation and networks','Contemporary accounts depict an adviser and strategist with wide party contacts. Congress nomination and communications responsibilities are better documented than an autonomous mass organisation.',[2,11,48],4),
('Communication and coalition outreach','His yatra commentary described possible opposition coordination towards 2024. Organisational and electoral effects are not inferred from a press statement.',[38],4),
('Provocative public advocacy','Sanitation comparisons drew both religious criticism and support from sanitation and women’s advocates; publicity increased visibility while creating message-management costs.',[29,30],3),
('Historical writing as political method','Insider documents and biographies place his political experience in wider historical argument. Publication and recognition do not make the author a disinterested witness.',[42,43,49],4)]
for i,(t,f,ns,phase) in enumerate(IDEAS,1):add('Ideas & Political Method',f'IM{i:02d}',{'Topic':t,'Finding':f},ns,'Attributed position' if i in [2,3] else 'Analysis',phase=phase)

CONS=[
('Bt-brinjal: expertise and precaution','2010','The moratorium prompted disagreement over precaution, public consultation and the authority of GEAC.','Indian Express critical analysis questioned overriding the regulator and awaiting consensus.','Ramesh’s parliamentary answer cited unresolved scientific concerns and state/public opposition.','Ministerial policy decision; political/scientific dispute, not a criminal finding.','Moratorium on commercialisation documented; this workbook does not adjudicate safety.',[12,13],2),
('POSCO approval and forest rights','2011–2012','Conditional approvals followed conflicting committee assessments and were challenged before NGT.','Critics disputed impact assessment and forest-rights processes; compiled materials record disagreement within the review committee.','Ministerial order relied on conditions and state assurances; ministry later argued the order amended earlier clearance.','Administrative clearance followed by tribunal intervention; no personal criminal finding established.','2012 reporting records suspension/review of the 2011 order. Full order and later project history remain a gap.',[15,16],2),
('Remarks about Chinese investment policy','2010-05','Public criticism of Home Ministry restrictions on Chinese companies created disagreement within the UPA government.','Reporting records a prime-ministerial reprimand after the criticism made during the China visit.','Ramesh met Chidambaram and was reported to have explained his position to the Prime Minister and Sonia Gandhi; exact private explanation not verified.','Political/ministerial-discipline controversy.','No resignation or legal penalty inferred from the inspected report.',[41],2),
('Toilets and temples','2012-10','Sanitation advocacy using a comparison with temples triggered a public dispute.','BJP spokesperson objected to the comparison; Congress reiterated equal respect for religious places.','Ramesh’s stated priority was sanitation. Pathak and Annie Raja defended that emphasis, the latter highlighting women’s safety concerns.','Political rhetoric and criticism; no legal adjudication established.','Support and opposition are documented; neither represents all religious citizens or all women.',[29,30],3),
('Vivek Doval criminal defamation','2019–2021','Doval brought a case following Ramesh’s repetition of magazine allegations at a press conference.','Doval contested the statements; the underlying allegations are not established by their repetition.','Ramesh apologised on 19 December 2020, acknowledging the need for independent verification; Doval accepted.','Discharged on 19 December 2020, as recorded by Delhi High Court on 15 January 2021.','Proceedings against other defendants were transferred separately. Do not describe a conviction or a full-trial acquittal.',[39,40],4),
('Aadhaar Money Bill route','2016–2021','Ramesh challenged the legislative certification while supporting Aadhaar’s underlying idea.','His objection concerned bicameral procedure and safeguards.','Government’s legal position prevailed in the 2018 majority and 2021 review; Chandrachud dissented.','Constitutional litigation brought by Ramesh, not a misconduct case against him.','Review petitions dismissed 11 January 2021; the broader Money Bill reference is analytically separate.',[33,34],4),
('Allegation about influence on district magistrates','2024-06','During counting preparations, Ramesh made an allegation concerning attempts to influence approximately 150 district magistrates.','ECI required the factual basis and stated that no DM had reported the alleged influence.','Ramesh requested a week to respond; ECI denied extension and set a same-day deadline. A substantive subsequent response was not verified.','ECI correspondence requesting substantiation; later final action not established.','Allegation is not adopted as fact; the letter is not a judicial finding of deliberate falsehood.',[46],4)]
for i,(matter,p,f,al,response,proc,out,ns,phase) in enumerate(CONS,1):
    add('Controversies',f'CO{i:02d}',{'Matter':matter,'Finding':f,'Period':p,'Allegation / criticism':al,'Subject response / relevant defence':response,'Procedural status':proc,'Finding or disposition':out,'Current-status limit':'Record is bounded to inspected evidence and dates; no later outcome is presumed.'},ns,'Analysis',phase=phase,proof={'Finding':ns,'Allegation / criticism':ns,'Subject response / relevant defence':ns,'Procedural status':ns,'Finding or disposition':ns},independent=i in [1,2,4,5])

LEG=[
('Environmental institutional contribution','NGT creation and high-visibility clearance decisions support an institutional-regulation interpretation of his tenure. The courts, legislators, officials and affected communities were also consequential actors.','Workbook synthesis',[12,14,17,18],2),
('Praise and limits of personal intervention','Himanshu Thakkar praised Ramesh’s environmental stature while questioning durable improvement in the ministry’s functioning and reputation. This is one identified assessment, not consensus.','Himanshu Thakkar, environmental commentator',[43],4),
('Regulatory discretion and predictability','Bt-brinjal and POSCO disputes reveal tensions between ministerial judgment, technical advice, rights and investment predictability. Evidence supports competing interpretations, not a single success score.','Workbook synthesis of contemporary criticism',[12,13,15,16],2),
('Land and displacement safeguards','His role in the 2013 law is a concrete legislative legacy. Design protections and implementation costs must be assessed separately, including later state amendments.','Workbook synthesis',[21,22,23],3),
('Rural welfare and women’s organisation','His ministry helped implement women-focused credit and sanitation outreach. NRLM predates his appointment, and benefits cannot be attributed solely to his tenure.','Workbook synthesis',[25,26,27,28],3),
('Opposition institutionalism','Land-law defence, Aadhaar litigation and committee work show an opposition method extending beyond media criticism. The Aadhaar review defeat limits claims of legal success.','Workbook synthesis',[33,34,36,50],4),
('Author and public historian','Publisher records document a substantial historical-writing strand and the NIF prize for his Krishna Menon biography. Insider accounts add evidence while requiring source criticism.','Publisher record and independent review',[42,43,49],4),
('Expertise, party access and mandate','A four-term indirect parliamentary career and major communications role show sustained party confidence. This does not establish a direct constituency mandate or independent control of Congress.','Workbook synthesis',[1,4,5,6,9,51],4),
('Communication accountability','The Doval apology/discharge illustrates the cost of repeating allegations without adequate verification. His later ECI dispute is a separate matter with an unresolved final status in this register.','Workbook synthesis',[39,40,46],4)]
for i,(t,f,a,ns,phase) in enumerate(LEG,1):add('Legacy & Assessments',f'LA{i:02d}',{'Theme':t,'Finding':f,'Assessor':a,'Consensus / dispute':'Attributed or bounded interpretation; no universal ranking.'},ns,'Analysis',phase=phase)

add('Offices & Party','OF26',{'Title':'Member, joint committee on Land Acquisition amendment bill — second period','Period':'August 2016–May 2019','Finding':'Returned to the joint committee on the 2015 land-acquisition amendment bill in August 2016; served through May 2019.','Position category':'Parliamentary','Institution':'Parliament','Start date':None,'End date':None},[1],phase=4)

ERA=[[
('Technical assignments under several administrations preceded formal Congress office-bearing. The inspected biographies do not give a complete account of early party recruitment.',[1,2,3],'M'),
('His early authority was advisory, operating through ministries and the Planning Commission. Cabinet or elected authority should not be inferred from access to senior decision-makers.',[1,2],'M'),
('No direct constituency contest is established for this phase. Technical appointments and party recruitment were distinct routes from a popular electoral mandate.',[1,2,48],'M'),
('Energy and technology policy work preceded advice during the early-1990s reform period. The record does not quantify his share of credit for liberalisation.',[2,3],'M'),
('Foreign education and later policy work provided international exposure, but a systematic account of how Cold War and post-Cold War changes affected his early choices was not assembled.',[1,2],'L'),
('Economic columns and television programmes formed part of his public-policy communication before high ministerial office; no audience-effect estimate is available.',[3],'M'),
('AICC office-bearing and state policy assignments connected organisational and expert networks. Sources document roles more securely than private recruitment decisions.',[1,2],'M'),
('Technical education supplied professional capital. Reliable evidence isolating caste, class, language or gender mechanisms in advancement was not established here.',[1,2],'L'),
('Karnataka, Rajasthan and Chhattisgarh advisory roles show a multi-state pathway. Their institutions and dates should not be collapsed into a single regional elected base.',[1,2],'M'),
('Official biographies and participant CVs dominate early-career evidence. Compressed titles can mislead: adviser to the national Planning Commission’s deputy chairman differs from deputy chairman of Karnataka’s board.',[1,2,3],'M')],[
('UPA coalition programme preparation linked Congress strategy to shared governing commitments; participation does not establish sole authorship.',[2],'M'),
('Independent ministerial charge coexisted with expert appraisal, statutory forest rules, litigation and Cabinet constraints. POSCO and Niyamgiri show these interacting authorities.',[1,14,15],'M'),
('Rajya Sabha entry from Andhra Pradesh was indirect; the 2010 re-election was unopposed. Neither produces a popular-vote share or an Adilabad constituency mandate.',[1,2,6],'M'),
('Industrial investment, agricultural technology and regulatory safeguards were contested together. Bt-brinjal and POSCO illustrate different balances rather than a uniform growth stance.',[12,13,15],'M'),
('Copenhagen/BASIC and Cancun put development equity and climate mitigation in the same negotiating agenda. India’s commitment was voluntary GDP-emissions intensity, not an absolute cap.',[19,20],'M'),
('Public consultations, press statements and media controversy made ministerial discretion unusually visible. Media attention is not proof of stronger enforcement.',[12,13,41],'M'),
('Coalition policy work and Congress strategy accompanied parliamentary office. The NAC role is documented in a CV, but its complete tenure and decision influence remain unclear.',[1,2],'M'),
('Niyamgiri litigation foregrounded forest communities and religious/community rights. Their agency must be retained rather than portraying them only as beneficiaries of a minister.',[14],'M'),
('He represented undivided Andhra Pradesh while exercising Union powers affecting projects in other states. State representation and national ministerial jurisdiction differ.',[2,14,15],'M'),
('Ministerial orders, parliamentary answers and later court records provide distinct evidentiary layers. Later decisions must not be projected backwards as his own acts.',[12,14,15,19],'M')],[
('Rural-development responsibility operated within the UPA government and collective parliamentary lawmaking. Ramesh’s amendments were part of a wider legislative process.',[1,21],'M'),
('Rural schemes depended on state administration, banks and local institutions; land legislation involved statutory social-impact and rehabilitation duties.',[22,24,25,27],'M'),
('His authority remained ministerial and Rajya Sabha based. Land and sanitation outreach were policy activities, not additional personal direct-election victories.',[1,21,28],'M'),
('Employment guarantees, SHG finance, sanitation and land acquisition combined welfare provision with development. Announced credit terms do not establish realised income gains.',[22,24,25,27],'M'),
('International development and sanitation debates provide plausible context, but the collected evidence is insufficient to attribute programme choices to international pressure or institutions.',[28],'L'),
('Sanitation advocacy used a yatra, celebrity messaging and community networks. The temple comparison created political criticism as well as supportive coverage.',[28,29,30],'M'),
('Women’s SHGs, frontline workers and interdepartmental coordination supplied implementation channels; these are not automatically Congress party organisations.',[25,27,28],'M'),
('Displacement, rural livelihoods and women’s access to finance/sanitation were explicit policy concerns. Implementation and distribution among marginalised groups remain evaluation gaps.',[22,25,28,30],'M'),
('The Telangana GoM and reorganisation Act changed the federal geography of his represented state. Collective preparation must be separated from later settlement of state disputes.',[31,32],'M'),
('Government releases are strong on announcements and intended mechanisms; parliamentary scrutiny exposes delivery problems. Independent longitudinal evaluation was not assembled.',[24,25,27,28],'M')],[
('After leaving government, he defended UPA legislation and held Congress communications responsibilities. Yatra outreach linked party mobilisation with broader opposition cooperation.',[11,38,50],'M'),
('Committee work and litigation supplied routes for opposition influence. Aadhaar review failed by majority; dissent and larger-bench questions remain distinct procedural matters.',[33,34,36],'M'),
('Karnataka elections in 2016 and 2022 continued the indirect route. Assembly party strength matters; rival statewide party tallies are not head-to-head popular margins for Ramesh.',[7,8,9,51],'M'),
('Land-law defence, environmental criticism and Aadhaar safeguards form an economic-policy agenda in opposition. Comparative effects on investment or poverty are not estimated.',[23,33,44,50],'M'),
('The 2015 environmental interview links domestic growth to ecological security. A comprehensive assessment of his later China policy or wider diplomacy is outside the assembled evidence.',[44],'L'),
('The communications portfolio explicitly includes social and digital media. The ECI correspondence illustrates demands for substantiation in rapid public messaging.',[5,11,46],'M'),
('Ramesh worked within a differentiated Congress communications structure alongside other office-holders; prominence does not establish control over nominations or the entire party.',[5,47],'M'),
('Landowner protections, women’s livelihoods and environmental rights continued as themes. Evidence identifying a stable social voting bloc personally attached to him is absent.',[33,44,50],'L'),
('He moved from Andhra Pradesh representation to Karnataka in 2016. Earlier Andhra Pradesh geography cannot be retroactively relabelled Telangana or a district constituency.',[10,32,51],'M'),
('Digital party directories are current snapshots, while judgments and committee reports have fixed dates. Media counts conflict in 2016; the primary declaration confirms only victory and date.',[4,5,7,8,34,36,51],'M')]]
comparison=['Contemporary policy advisers, planning officials and Congress organisational recruits','UPA ministers, expert regulators and Rajya Sabha nominees','UPA cabinet colleagues, state implementers and parliamentary sponsors','Opposition Rajya Sabha MPs, committee chairs and national party communicators']
cautions=['Do not infer later ideology or ministerial powers from early advisory roles.','Use the institutions and information available before later court judgments and climate agreements.','Distinguish the original 2013 law from later state amendments and later renamed programmes.','Do not treat current digital prominence as evidence of earlier mass support or later legal rulings as already decided.']
for pi,entries in enumerate(ERA,1):
    for i,(f,ns,disp) in enumerate(entries,1):
        add('Context & Constraints',f'CT-P{pi}-{i:02d}',{'Career phase':phases[pi-1],'Coverage dimension':'Era','Coverage item':era_items[i-1],'Finding':f,'Research disposition':'Material finding' if disp=='M' else 'Research limitation','Contemporary comparison group':comparison[pi-1],'Presentism caution':cautions[pi-1]},ns,'Analysis',status='Supported' if disp=='M' else 'Not reviewed')

GENDER=[
('Education, advisory work and party nomination are documented pathways. Evidence isolating a gender-related advantage or barrier in his recruitment was not found in the inspected material.',[1,2,48],'Research limitation'),
('The inspected career records do not establish a gender-related first or a contemporary claim of such a milestone. This is a research gap, not proof that gender was irrelevant.',[1,4],'Research limitation'),
('Professional and party networks are evident; no reliable causal account of dynastic, marriage or family networks in his political entry was established. Family detail is excluded without political relevance.',[1,2,48],'Research limitation'),
('Commerce, Power, Environment and Rural Development assignments are recorded. Attributing those choices to masculine expectations requires comparative evidence not assembled here.',[1],'Research limitation'),
('Sanitation rhetoric attracted criticism and support, but the inspected coverage does not establish that his own treatment was gendered. No matched media study of comparable men and women was conducted.',[29,30],'Research limitation'),
('No distinctive gender-based threat or security constraint affecting his career was established. Public disagreement and litigation are not automatically evidence of gendered persecution.',[39,40,41],'Research limitation'),
('NRLM’s women-centred SHG design, credit subvention and proposed sanitation outreach through frontline workers supply concrete gender-related policy mechanisms during his tenure.',[25,27,28],'Material finding'),
('Sanitation advocacy foregrounded women’s circumstances in public responses, but evidence that Ramesh deliberately mobilised his own male identity as a political strategy is insufficient.',[28,30],'Research limitation'),
('Women-focused programme design and Annie Raja’s support establish substantive policy relevance and an organisational response; they do not establish measured empowerment, reduced violence or representation of all women.',[25,27,30],'Material finding'),
('Contemporary sanitation supporters and critics can be identified. A longitudinal feminist or gender-comparative assessment of his career and policy effects was not assembled.',[29,30,43],'Research limitation')]
for i,(f,ns,disp) in enumerate(GENDER,1):
    add('Context & Constraints',f'CT-G-{i:02d}',{'Career phase':'Across phases; rural-policy evidence concentrated in 2011–2014','Coverage dimension':'Gender','Coverage item':gender_items[i-1],'Finding':f,'Research disposition':disp,'Contemporary comparison group':'Men and women with comparable Union ministerial, parliamentary and party responsibilities','Other identity relevance':'Place of birth, education and state representation are recorded; caste, religion and language-based voting support are not inferred.','Presentism caution':'Apply equal relevance to family, appearance and networks; distinguish programme targeting from demonstrated effects.'},ns,'Analysis',status='Supported' if disp=='Material finding' else 'Not reviewed')

for name,t in tables.items():
    if name=='Context & Constraints':continue
    for row in t['rows']:
        if row.get('Career phase') in phases:
            p=phases.index(row['Career phase'])+1
            row['Context IDs']=f'CT-P{p}-01; CT-P{p}-02; CT-P{p}-03'

GAPS=[
('High','2016 vote-count discrepancy','Official declaration confirms election and date but lacks counts. S007 gives 47, S008 gives 46. Numeric total remains withheld.','Retrieve Karnataka Returning Officer Form 23B or count proceedings; retain both reports until resolved.',['EL03','EL06']),
('Medium','Original election returns','2004 election month and 2010 unopposed return are supported; detailed original returns and the 2022 count sheet were not inspected.','Seek ECI/legislature original declarations and count sheets; preserve reported 2022 first-preference total as secondary.',['EL01','EL02','EL04']),
('Medium','Minor office boundaries','Some advisory, NAC and committee dates are only year/month precise. Official biography resolves rural/sanitation dates but secondary profiles differ.','Use appointment notifications for exact boundaries; do not add inferred day-level precision.',['OF01','OF02','OF03','OF09','OF14','OF15','OF20','OF23']),
('High','Policy outcomes and attribution','No independent tenure-bounded causal evaluation of land reform, SHG credit, sanitation, MGNREGA or regulatory performance was assembled.','Combine audit reports and independent evaluations with state implementation and counterfactual analysis; separate institutions from personal credit.',['PG07','PG08','PG09','PG10','PG11']),
('Medium','POSCO complete procedural chain','Compiled documents and 2012 reporting inspected; complete NGT order and later clearance/project history remain incomplete.','Retrieve original tribunal order and subsequent official project decisions before stating a final project outcome.',['CO02','PG04']),
('Medium','Broader Money Bill reference','The 2021 Aadhaar review disposition is verified; later disposition of the broader reference is not established here.','Check subsequent Supreme Court reference and listing records; do not assume dismissal of review settled every doctrinal issue.',['CO06','PG14']),
('Medium','ECI allegation follow-up','ECI’s 3 June 2024 letter is available, but a substantive subsequent response or final action was not verified.','Locate reply and final ECI action; no wrongdoing or exoneration should be inferred from the gap.',['CO07']),
('Medium','Gender mechanisms and historical comparisons','Eight gender dimensions and five era-context items remain explicit research limitations.','Seek matched recruitment, portfolio, media and security studies; absence of evidence is not evidence of no effect.',['CT-G-01','CT-G-05','CT-G-10','CT-P1-05','CT-P4-08']),
('Low','Committee recommendations and uptake','2019–2020 ad hoc role is verified, but full recommendations and implementation effects were not traced; DST report establishes response categories only.','Read full report and government action-taken responses; evaluate uptake separately from chairmanship.',['PG15','PG18']),
('Low','Book-based interpretation','Publisher descriptions and a review inspected; full historical books and their archival claims were not independently assessed.','Use the books alongside independent scholarship and cited archives for a fuller intellectual biography.',['IM12','LA07'])]
gaps=[{'id':f'G{i:02d}','priority':p,'topic':t,'gap':g,'next_action':n,'record_ids':rs,'status':'Open'} for i,(p,t,g,n,rs) in enumerate(GAPS,1)]
data={'schema_version':1,'subject':'Jairam Ramesh','as_of':ASOF,'guidance':'Four career phases. Official roles, attributed arguments and bounded analysis remain distinct. Review counts describe registered fields, not historical completeness. All 40 era and ten gender dimensions have explicit dispositions.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'coverage':{'Era':era_items,'Gender':gender_items},'phases':phases,'gaps':gaps}
for name,obj in [('research.json',data),('sources.json',sources),('retrievals.json',retrievals)]:
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(sources),'rows':sum(len(t['rows']) for t in tables.values()),'claims':len(claims),'evidence':len(evidence)}))
