"""Reproducible research snapshot; see author_sources.py for inspected passages."""
import hashlib,json
from pathlib import Path
from author_sources import sources,retrievals,ASOF
ROOT=Path(__file__).resolve().parent
tables={};claims=[];evidence=[]
S={s['Source ID']:s for s in sources};R={r['id']:r for r in retrievals}
phases=['P1 | Formation, movement and electoral entry, to June 2014','P2 | New state and first ministry, June 2014–December 2018','P3 | Party leadership and second ministry, December 2018–December 2023','P4 | Opposition and accountability, December 2023–November 2026']
gender_items=['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time']
era_items=['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']
layouts={'Overview':['Overview ID','Topic','Finding / value'],'Context & Constraints':['Context ID','Career phase','Coverage item','Finding'],'Career Timeline':['Timeline ID','Period','Event','Finding'],'Elections':['Election ID','Year','Jurisdiction','Result','Finding'],'Offices & Party':['Position ID','Title','Period','Finding'],'Policy & Governance':['Policy ID','Initiative','Finding'],'Ideas & Political Method':['Idea ID','Topic','Finding'],'Controversies':['Matter ID','Matter','Finding'],'Legacy & Assessments':['Assessment ID','Theme','Finding']}
for name,lead in layouts.items():tables[name]={'lead_columns':lead,'date_columns':['Start date','End date','Election date'],'rows':[]}
def ids(ns):return [f'S{n:03d}' for n in ns]
def add(sheet,rid,fields,ns=(),kind='Recorded fact',phase=None,proof=None,status='Supported',note='',independent=False):
    row={layouts[sheet][0]:rid,**fields,'Claim type':kind,'Source IDs':'; '.join(ids(ns))}
    if phase:row['Career phase']=phases[phase-1]
    if note:row['Research note']=note
    row['Corroboration']='Unresolved' if status!='Supported' else 'Primary record' if any(S[s]['Primary or secondary']=='Primary' for s in ids(ns)) else 'Multiple independent sources' if len({S[s]['Origin ID'] for s in ids(ns)})>1 else 'Single credible source'
    tables[sheet]['rows'].append(row)
    if kind=='Method / scope':return row
    if proof is None:proof={('Finding / value' if sheet=='Overview' else 'Finding'):ns}
    for i,(field,ss) in enumerate(proof.items(),1):
        cid=f'{rid}.{i:02d}'
        c={'id':cid,'sheet':sheet,'record_id':rid,'field':field,'statement':row[field],'fingerprint':hashlib.sha256(json.dumps(row[field],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'claim_type':kind,'status':status,'priority':'High' if sheet in ['Overview','Elections','Controversies'] else 'Medium','candidate_source_ids':ids(ss),'evidence_ids':[],'contradictions':[],'review_note':note or ('Bounded synthesis of cited passages; no causal estimate.' if kind=='Analysis' else 'Full registered wording checked; reported positions remain attributed.')}
        if independent and status=='Supported':c['requires_independent_corroboration']=True
        if status=='Supported':
            for j,sid in enumerate(ids(ss),1):
                ret=R['R'+sid[1:]];eid=f'E-{cid}-{j}'
                assert ret['access_status']=='Passage inspected'
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':ret['id'],'locator':ret['locator'],'passage_paraphrase':ret['passage_paraphrase'],'relation':'Supports','reviewed_by':'Codex passage review','reviewed_at':ASOF,'note':'Supports the relevant component of the registered field; procedural allegations are not validated as underlying facts.'})
                c['evidence_ids'].append(eid)
        claims.append(c)
    return row

OV=[
('Identity','Kalvakuntla Taraka Rama Rao, commonly K. T. Rama Rao or KTR; born 24 July 1976 in Siddipet, then Andhra Pradesh and now Telangana. Son of K. Chandrashekar Rao (KCR).',[1,2],'Recorded fact'),
('Current political position','Sircilla MLA and BRS working president; a former Telangana minister. Working president is a party office and does not mean party president, Chief Minister or formal Leader of Opposition.',[2,12,29,32],'Analysis'),
('Formation and education','His biography reports an MSc in Biotechnology at Pune and an MBA in Marketing/E-Commerce at CUNY, followed by US work. The election affidavit also records postgraduate education; degrees and employment were not independently audited.',[1,45],'Attributed position'),
('Electoral record','Five Sircilla victories: 2009, the 2010 by-election, 2014, 2018 and 2023. He retained his constituency when BRS lost government in 2023.',[3,4,5,7,8,25],'Recorded fact'),
('Executive chronology','Entered the first Telangana ministry in June 2014; added urban and industrial responsibilities in 2016. After a gap following the 2018 election, returned on 8 September 2019 and served until the December 2023 change of government.',[1,10,11,13,25],'Recorded fact'),
('Party continuity','TRS became Bharat Rashtra Samithi (BRS) in December 2022. This was a party renaming, not a personal party switch. His working-presidential appointment dates to December 2018.',[12,14],'Recorded fact'),
('Economic and institutional contribution','Promoted Telangana’s technology and investment economy and helped develop T-Hub and related institutions. Government IT-export and employment series grew substantially; the evidence does not isolate his causal contribution.',[15,16,17,19],'Analysis'),
('Urban governance','MAUD responsibilities included building-permission reform and disaster response. The TS-bPASS rollout is documented; flooding and encroachment exposed continuing urban-management problems.',[10,21,24],'Analysis'),
('Sircilla development','Weaver interviews credit public orders and local development while describing seasonal income and machinery constraints. Public procurement helped sustain work without resolving all livelihood vulnerabilities.',[22,23],'Analysis'),
('Gender record','WE Hub provides a concrete women-focused institutional contribution. His 2024 remarks about women on buses drew criticism, a commission inquiry and an apology; programme design and public rhetoric require separate assessment.',[17,18,39,47],'Analysis'),
('Political method','Combines constituency cultivation, investor-facing communication and family-based party access. Following defeat he said excessive administrative focus and MLA-centred organisation weakened worker connections.',[1,12,19,22,27],'Analysis'),
('Federal politics','At the March 2025 Chennai meeting on delimitation, argued against centralisation and population-led dilution of southern representation. This is an attributed position, not an enacted seat-allocation outcome.',[40],'Attributed position'),
('Formula E status','The High Court refused to quash the investigation in January 2025. A March 2026 chargesheet is reported; a discharge petition was filed later. The latest inspected hearing report adjourned the matter to 4 December 2026. No final guilt or discharge determination was established.',[28,29,30,31],'Analysis'),
('Phone-surveillance status','Questioned in January 2026 and denied involvement. October and 15 November reports anticipated a chargesheet naming him; a filed chargesheet or cognizance order against him was not inspected by the cutoff.',[32,33,34],'Analysis'),
('Central assessment','His strongest documented record combines repeated constituency victories with economic institution-building. Party defeat, concentrated family leadership, uneven local livelihoods and unresolved accountability disputes qualify celebratory accounts.',[8,16,22,25,28,41],'Analysis'),
('Main gaps','Original 2018 vote-share denominator, exact dates of some tenure boundaries, later court orders, and independent policy-impact evidence remain unresolved. Research Queue records specific next steps.',[6,7,13,28,30,31],'Uncertainty')]
for i,(t,f,ns,k) in enumerate(OV,1):
    add('Overview',f'OV{i:02d}',{'Topic':t,'Finding / value':f},ns,k,status='Not reviewed' if i==16 else 'Supported')
for i,(t,f) in enumerate([
('Scope and cutoff','Evidence snapshot: 16 November 2026. Four career phases, 40 era-context items and ten gender dimensions. Prepared across 16–17 November; later events are outside scope.'),
('How to use','Findings, review status and citation links appear first. Expand grouped columns for dates, counts, responses and qualifications. Claims and Evidence preserve field-level passage reviews.'),
('Evidence meaning','Supported refers to the registered wording, including attribution or bounded analysis; it is not a completeness score. Not reviewed marks explicit research limitations. Blank values never silently mean zero or exoneration.'),
('Election definitions','All five contests are direct Assembly elections. Party-wide and municipal campaigns appear elsewhere. Published shares are retained only for 2009, 2014 and 2023; 2010/2018 shares are withheld pending denominator reconciliation.'),
('Confirmed personal contests (calculated)',5),('Confirmed constituency wins (calculated)',5)],17):
    add('Overview',f'OV{i:02d}',{'Topic':t,'Finding / value':f},kind='Method / scope')

TL=[
('1976-07-24','Birth','Born in Siddipet; his later political pathway included the family of TRS founder KCR.',[1],1),
('1990s–2000s','Education and employment','Biography reports science and business education followed by work in the United States; exact employment and return chronology remains incompletely corroborated.',[1,45],1),
('2009','First Assembly election','Won Sircilla for TRS by 171 votes over independent K.K. Mahender Reddy.',[3],1),
('2010','Resignation and by-election','Resigned in support of Telangana statehood and won the ensuing Sircilla by-election; polling occurred on 27 July.',[4,9,49],1),
('2014-04-30','Third constituency victory','Polled in undivided Andhra Pradesh and won Sircilla again; Telangana state formation followed in June.',[5,44],1),
('2014-06-02','New state and ministry','Joined the first Telangana government with IT and Panchayat Raj responsibilities.',[1,44],2),
('2015-11','T-Hub','Startup institution launched after government, academic and business collaboration.',[16,17],2),
('2016-02-07','Municipal portfolio','MAUD transferred from KCR to KTR following the GHMC campaign and TRS victory.',[10],2),
('2016-04-25','Industrial portfolio reshuffle','Added Industries/Commerce and other portfolios; Panchayat Raj/Rural Development transferred away.',[11],2),
('2017-08','Nerella accountability','Met injured villagers and said police had overreacted after reported torture near Sircilla.',[37,38],2),
('2017–2018','Women’s entrepreneurship','Announced WE Hub in November 2017; government records operations from March 2018.',[17,18],2),
('2018-12','Fourth victory; party leadership','Re-elected from Sircilla. Appointed TRS working president on 14 December and took charge on 17 December.',[7,12],3),
('2018-12–2019-09','Ministerial interruption','Absent from the initial second-term Cabinet; reinducted on 8 September 2019.',[13],3),
('2020','Pandemic and flooding','Sircilla weavers faced disrupted work; Hyderabad flooding tested municipal response. Building-permission reform went live in November.',[21,23,24],3),
('2022','T-Hub expansion; party renaming','T-Hub phase 2 launched in June. ECI accepted TRS’s BRS name change on 8 December.',[14,46],3),
('2023-03-02','T-Works opening','Attended inauguration with Foxconn’s chairman, promoting hardware prototyping and manufacturing links.',[19],3),
('2023-03','TSPSC paper leak','Opposition demanded his dismissal; he denied departmental responsibility for the Commission’s day-to-day work.',[35,36],3),
('2023-12','Government defeat','Retained Sircilla with a reduced margin while BRS fell to 39 seats and Congress won 64.',[7,8,25],4),
('2024-01','Party self-critique','Accepted responsibility for defeat and described weak party-worker links.',[27],4),
('2024-08','Bus remarks and apology','Apologised after comments about women on buses triggered criticism and a commission inquiry.',[39],4),
('2025-01-07','Formula E quashing refused','High Court allowed investigation to proceed; observations were limited to the quashing petition.',[28],4),
('2025-03-22','Delimitation opposition','Participated in Stalin’s Chennai meeting and argued for protection of southern political representation.',[40],4),
('2025–2026','Family-party rupture','Kavitha’s BRS exit and later public attacks on KTR exposed an open succession and leadership dispute.',[41],4),
('2026-01-23','Phone-surveillance questioning','Questioned by SIT; denied involvement in alleged unlawful surveillance.',[32],4),
('2026-09–2026-11','Continuing legal developments','Formula E discharge sought; October hearing adjourned to December. Latest phone-surveillance reports still described a proposed chargesheet.',[29,30,31,33,34],4)]
for i,(period,event,f,ns,p) in enumerate(TL,1):
    add('Career Timeline',f'TL{i:02d}',{'Period':period,'Event':event,'Finding':f},ns,phase=p)

EL=[
(2009,'General','Andhra Pradesh','TRS',36783,'K.K. Mahender Reddy','Independent',36612,.2692,None,[3],1,'Published ECI share; pre-NOTA election. Candidate-valid total 136,637. First victory, narrow margin.'),
(2010,'By-election','Andhra Pradesh','TRS',87876,'K.K. Mahender Reddy','INC',19657,None,'2010-07-27',[4,9,48,49],1,'After statehood resignation. Wide Form 20 candidate columns corroborated by secondary transcription; complete denominator not reconciled.'),
(2014,'General','Andhra Pradesh at polling; Telangana after 2 June','TRS',92135,'Konduru Ravinder Rao','INC',39131,.5836,'2014-04-30',[5,44],1,'Published ECI share uses total including NOTA. Election preceded state formation; representation subsequently transferred to Telangana.'),
(2018,'General','Telangana','TRS',125213,'Kondam Karuna Mahender Reddy','INC',36204,None,None,[7],3,'Counts from inspected historical results paragraph. Original Form 20 fetch failed; share withheld rather than mixing candidate-valid and NOTA-inclusive denominators.'),
(2023,'General','Telangana','BRS (ECI code BHRS)',89244,'K.K. Mahender Reddy','INC',59557,.4728,None,[8],4,'Published ECI share includes NOTA; rejected votes are not interchangeable with the share denominator. Constituency retained despite statewide defeat.')]
for i,(year,typ,jur,party,votes,opp,opparty,ovotes,share,day,ns,p,note) in enumerate(EL,1):
    fields={'Year':year,'Jurisdiction':jur,'Result':'Won','Finding':f'Won Sircilla ({typ.lower()}) with {votes:,} votes against {opp}, {ovotes:,}; margin {votes-ovotes:,}.','Constituency':'Sircilla (AC 29)','House / route':'Assembly / direct','Contest type':typ,'Party':party,'Candidate votes':votes,'Opponent':opp,'Opponent party':opparty,'Opponent votes':ovotes,'Signed vote margin':votes-ovotes,'Vote share':share,'Election date':day,'Interpretation / denominator':note}
    proof={'Finding':ns,'Candidate votes':[7] if year==2018 else [4,48] if year==2010 else [ns[0]],'Opponent votes':[7] if year==2018 else [4,48] if year==2010 else [ns[0]]}
    if share is not None:proof['Vote share']=[ns[0]]
    if day:proof['Election date']=[9] if year==2010 else [5]
    add('Elections',f'EL{i:02d}',fields,ns,phase=p,proof=proof,note=note)

OFF=[
('MLA, first Sircilla mandate','2009–2010 resignation',None,None,'Legislative','Andhra Pradesh Assembly','TRS',[3,49],1,'First mandate interrupted by statehood resignation; exact resignation acceptance date not fixed.'),
('MLA, Sircilla by-election mandate','2010–2014',None,None,'Legislative','Andhra Pradesh Assembly','TRS',[4,9],1,'Poll date is not assumed to be oath date.'),
('MLA, Sircilla third mandate','2014–2018',None,None,'Legislative','Andhra Pradesh, then Telangana Assembly','TRS',[5,44],2,'Polling preceded bifurcation; state changed on 2 June 2014.'),
('Minister, IT and Panchayat Raj / Rural Development','2 June 2014–April 2016 portfolio reshuffle','2014-06-02',None,'Ministerial','Telangana government','TRS',[1,11],2,'Panchayat Raj/Rural Development transferred away in April 2016; IT responsibility continued.'),
('Minister, Municipal Administration and Urban Development','7 February 2016–December 2018','2016-02-07',None,'Ministerial','Telangana government','TRS',[10,13],2,'Allocation from KCR reported contemporaneously; exact first-term cessation date not fixed.'),
('Minister, Industries/Commerce and additional portfolios','25 April 2016–December 2018','2016-04-25',None,'Ministerial','Telangana government','TRS',[11,13],2,'Added Mines/Geology, Public Enterprises and NRI affairs; concurrent with IT and MAUD.'),
('MLA, Sircilla fourth mandate','2018–2023',None,None,'Legislative','Telangana Assembly','TRS; renamed BRS in December 2022',[7,14],3,'Legislative membership continued during ministerial interruption.'),
('Working president','Appointed 14 December 2018; took charge 17 December; continuing at cutoff','2018-12-14',None,'Party','TRS, renamed BRS','TRS → BRS',[12,14,29,32],3,'Party management office under KCR’s presidency; not a government appointment.'),
('Outside Cabinet','December 2018–7 September 2019',None,None,'Ministerial interruption','Telangana government','TRS',[13],3,'Excluded from initial Cabinet and February expansion; no continuous ministry asserted across this gap.'),
('Minister, IT, Industries/Commerce and MAUD','8 September 2019–December 2023','2019-09-08',None,'Ministerial','Telangana government','TRS → BRS',[1,13,14,25],3,'Second ministerial period ended with government transition; exact legal cessation day is not inferred from election day.'),
('MLA, Sircilla fifth mandate','Elected 2023; in office at cutoff',None,None,'Legislative','Telangana Assembly','BRS',[2,8],4,'PRS’s 3 December 2023 start field is result date; not used as an independently checked oath date.'),
('Opposition politician and party organiser','December 2023–cutoff',None,None,'Political role','BRS','BRS',[25,27,40],4,'Opposition activity is distinct from formal Leader of Opposition designation.')]
for i,(title,period,start,end,cat,inst,party,ns,p,note) in enumerate(OFF,1):
    fields={'Title':title,'Period':period,'Finding':f'{title}; {period}. {note}','Start date':start,'End date':end,'Position category':cat,'Institution':inst,'Party':party}
    add('Offices & Party',f'OF{i:02d}',fields,ns,phase=p,note=note)

POL=[
('IT/ITeS economy','Promoted investment and administered the IT portfolio during substantial growth in government-reported exports and employment.','Administered / promoted','Investment facilitation, infrastructure and skills','Official annual series documents outputs; no causal allocation to one minister','Hyderabad’s inherited cluster, private firms, workers, global demand, KCR and the bureaucracy also matter.',[1,15],2),
('T-Hub','Helped initiate a collaborative startup institution launched in November 2015; later expansion included phase 2 in June 2022.','Institution-building / sponsorship','Workspace, mentors, investor and corporate networks','Institution and expansion operational','Founders, universities, businesses and management shared responsibility; incubation counts do not measure additional firm survival.',[16,17,46],2),
('TASK','Government ecosystem records TASK’s establishment in 2014 to connect skills and industry.','Portfolio oversight','Training and employability partnerships','Institution established','Training activity is not equivalent to verified placements or a personally caused employment gain.',[1,17],2),
('State Innovation Cell','Government records the innovation cell’s establishment in 2017, extending the ecosystem beyond a single incubator.','Portfolio oversight','Support innovation and entrepreneurial networks','Institution established','No independent evaluation of geographical reach or incremental outcomes assembled.',[1,17],2),
('WE Hub','Announced women-focused incubation in 2017; operations began in March 2018.','Announced / sponsored','Finance access, mentorship and links to government for women entrepreneurs','Operating institution; government-reported participation','Design addresses barriers; participation cannot by itself establish profit, autonomy or equal access across social groups.',[17,18,47],2),
('WE Hub reported reach','The 2023 Socio Economic Outlook reports 2,194 startups/small or medium entrepreneurs incubated and 5,235 women engaged.','Administrative reporting','Incubation and outreach','Cumulative administrative counts','The enterprise categories are mixed; these are not all technology startups. Different-year promotional counts are not a harmonised impact series.',[46],3),
('T-Works','Inaugurated a 78,000-square-foot prototyping facility with Foxconn’s chairman on 2 March 2023.','Promoted / inaugurated','Equipment and technical support for hardware prototypes','Facility opened','Plans for investment or expansion are not completed factories or guaranteed jobs. International business outreach is not Union foreign-policy authority.',[19],3),
('TS-iPASS','Administered and promoted the industrial approval framework after acquiring Industries in 2016; the underlying Act was enacted in 2014.','Inherited / administered','Single-point approvals and officer accountability for delay','Statutory framework preceded his Industries appointment','Do not assign sole authorship; approvals and promised investment differ from operating units and realised employment.',[11,20],2),
('TS-bPASS','Building-permission system went live on 16 November 2020 during his MAUD tenure.','Portfolio oversight / implementation','Integrate and simplify building approvals','Rollout documented in official training material','Digital rollout does not prove universal compliance, safer construction or elimination of discretion.',[1,21],3),
('Sircilla textile procurement','Government textile orders, including Bathukamma sarees, supported work; local interviews also describe seasonal insecurity and demands for machinery upgrades.','Constituency advocacy / government procurement','Generate demand for local textile production','Reported work and visible development alongside uneven income','Interview evidence is local and non-representative; KTR was one actor among government agencies, firms and workers.',[22],3),
('Pandemic relief for weavers','In May 2020 the collector reported relief at KTR’s direction while workers described lost orders and distress.','Directed relief, according to collector','Cash and grocery assistance','Administrative response reported; adequacy contested by worker accounts','Relief announcement and distribution accounts do not establish full compensation for lost livelihoods.',[23],3),
('Hyderabad flood response','In October 2020 reported disaster losses and response, emphasising extreme rain while acknowledging encroachment.','Municipal oversight / crisis communication','Evacuation, disaster response and municipal coordination','Response reported contemporaneously','Rainfall exposure, urban land use and multi-agency responsibility complicate attribution; no final disaster audit assembled.',[24],3),
('Formula E city promotion','Promoted Hyderabad’s Formula E event; the later prosecution concerns payments for proposed subsequent seasons.','Promoted / defended','Use an international event to market the city','Event and disputed later payments must be separated','Commercial promotion is not proof of financial propriety; a criminal allegation is not proof that all event benefits were fictitious.',[28,29],3),
('Panchayat Raj and rural development','Held early rural portfolios before the April 2016 reshuffle. A complete tenure-specific implementation or outcome evaluation was not assembled.','Portfolio holder','Rural administration and local-government responsibilities','Office established; programme attribution remains incomplete','Avoid crediting every state rural programme or later water project solely to this short portfolio period.',[1,11],2)]
for i,(initiative,f,role,mechanism,stage,caution,ns,p) in enumerate(POL,1):
    add('Policy & Governance',f'PG{i:02d}',{'Initiative':initiative,'Finding':f,'KTR role':role,'Mechanism':mechanism,'Implementation / output':stage,'Outcome / attribution limit':caution},ns,'Analysis',p,proof={field:ns for field in ['Finding','KTR role','Mechanism','Implementation / output','Outcome / attribution limit']})
for i,(fy,exports,jobs) in enumerate([('2013–14',57258,323396),('2021–22',183569,778121),('2022–23',241275,905715)],15):
    add('Policy & Governance',f'PG{i:02d}',{'Initiative':f'IT/ITeS official series: FY{fy}','Finding':f'Telangana government reports exports of ₹{exports:,} crore and employment of {jobs:,} for FY{fy}.','Financial year':fy,'Exports (INR crore)':exports,'Employment (persons)':jobs,'KTR role':'Baseline predates Telangana ministry' if i==15 else 'Portfolio minister during period','Outcome / attribution limit':'Nominal export values and administrative employment stock; not a count of jobs personally created.'},[15],phase=1 if i==15 else 3,proof={'Finding':[15],'Exports (INR crore)':[15],'Employment (persons)':[15]})

IDEAS=[
('Statehood and development','Moved from statehood-linked electoral mobilisation to presenting Telangana as an investment and innovation destination. This combines regional political claims with economic promotion rather than proving a single doctrinal ideology.',[9,16,19,49],2),
('Family and professional pathway','KCR’s son combined family access with an education and professional biography attractive to business audiences. Neither family advantage nor professional credentials alone explains his repeated wins.',[1,3,8,12],2),
('Constituency cultivation','Sircilla linked political representation to textile procurement and visible development. Electoral durability coexisted with continuing worker demands.',[3,8,22],3),
('Urban campaigning','The 2016 GHMC campaign increased his prominence; the subsequent MAUD allocation connected party campaigning to executive responsibility. This was not his personal municipal election.',[10],2),
('Party organisation','Working-presidential appointment assigned day-to-day party management while KCR retained the presidency. Informal succession expectations are not an actual Chief Minister appointment.',[12],3),
('Investment communication','T-Hub and T-Works illustrate public-facing engagement with universities, founders and international businesses. Business events demonstrate outreach, not realised investment or all-voter approval.',[16,19],3),
('Self-critique after defeat','In January 2024 accepted responsibility and said administrative preoccupation and MLA-centred structures weakened links with workers. This is his explanation, not a controlled analysis of voter behaviour.',[27],4),
('Federalism and delimitation','Argued at the 2025 Chennai meeting against fiscal and political centralisation and against penalising southern states for population outcomes.',[40],4),
('Opposition strategy','Continued party organisation and criticism after the 2023 government loss and 2024 Lok Sabha rout. His own Assembly victory should not be read as a statewide endorsement of BRS.',[8,25,26,27],4),
('Reputation and legal response','Used court petitions and public denials in Formula E and surveillance matters; separately brought a defamation complaint as complainant. These different procedural roles must not be combined.',[28,30,32,42],4),
('Limits of concentrated leadership','Kavitha’s later break and criticism exposed conflict within the leadership family. Her account is a rival’s assessment and does not independently establish the causes of BRS decline.',[41],4),
('Welfare and enterprise','Women’s incubation and textile procurement sit alongside technology investment promotion. The mix resists a simple market-only description, but distributional success needs stronger outcome evidence.',[17,22,47],3)]
for i,(t,f,ns,p) in enumerate(IDEAS,1):add('Ideas & Political Method',f'IM{i:02d}',{'Topic':t,'Finding':f},ns,'Analysis',p)

CO=[
('Formula E payments','High Court rejected quashing on 7 January 2025; a March 2026 chargesheet and later discharge application are reported. Latest inspected hearing report adjourned the case to 4 December 2026.','Criminal investigation/prosecution; discharge sought; no final finding established','ACB alleged payments for proposed subsequent seasons lacked required sanction and safeguards.','KTR defends bringing the event to Hyderabad and alleges politically motivated prosecution.','Crl.P.15847/2024 rejected quashing; paragraph 43 limits observations. October 2026 appearance exemption is not discharge or acquittal.','Obtain later discharge, passport and trial orders; do not attribute another accused’s recalled warrant to KTR.',[28,29,30,31],4),
('Alleged unlawful phone surveillance','SIT questioned KTR on 23 January 2026. October and 15 November reports described plans to name him in a chargesheet; filing was not established in inspected records.','Questioning; prospective chargesheet reported; filing/cognizance unverified','Police-source reports alleged political direction and misuse of surveillance.','Denied involvement; his office challenged the relevance of aspects of the questioning.','No filed charging document against KTR or final judicial finding inspected by cutoff.','Anonymous-source reports of intended filing are not a filed charge or conviction.',[32,33,34],4),
('TSPSC examination paper leak','Examination cancellations prompted demands for KTR’s dismissal; he denied day-to-day responsibility for the constitutional commission.','Political accountability dispute alongside criminal investigation of leak','BJP linked IT support institutions to his portfolio and demanded action.','Said TSPSC was autonomous, initially blamed two employees and promised punishment/reforms.','No inspected finding establishes his participation in obtaining or selling papers.','His early two-person explanation is not treated as a final investigation conclusion.',[35,36],3),
('Nerella police torture, 2017','Reporting described an internal inquiry confirming torture of eight men; KTR met victims and said police had overreacted. Opposition alleged pressure involving contractors and the local MLA.','Reported police inquiry and court scrutiny; political allegation against MLA','Opposition sought independent investigation, compensation and action under SC/ST law.','Acknowledged police overreaction when meeting the injured villagers.','Original inquiry report and final case disposition not retrieved; no inspected finding that KTR ordered torture.','Reports disagree on detailed caste breakdown; use only the broad Dalit/BC description where relevant.',[37,38],2),
('Remarks about women on buses','August 2024 remarks prompted criticism and a Women’s Commission inquiry; KTR apologised.','Public criticism; inquiry commenced; apology','Critics objected to remarks about women doing break dances on buses.','Said he did not intend to offend and apologised to women.','No final commission finding inspected.','The apology is documented; do not infer either final exoneration or a legal finding from it.',[39],4),
('Surekha defamation complaint','KTR brought a complaint over statements linking him to actors’ divorce. A December 2025 report described a disputed warrant for the minister’s nonappearance; later status remains unresolved.','KTR is complainant; reported process dispute','He alleged defamatory statements by minister Konda Surekha.','His response was legal action; the minister’s staff disputed the reported warrant account.','Separate Nagarjuna complaint was withdrawn in November 2025; that does not close KTR’s case.','Original CC307/2025 orders and later hearing outcome not obtained; intimate allegations are not repeated as facts.',[42,43],4),
('Urban flooding and encroachment','The 2020 floods exposed the tension between metropolitan growth and flood-management capacity. KTR cited extreme rain and acknowledged encroachment.','Governance criticism; no personal criminal finding asserted','Municipal planning and preparedness faced public scrutiny.','Reported evacuation and disaster response; identified rainfall and land-use problems.','Contemporary response reporting; no final audit of individual responsibility assembled.','Shared agency responsibility does not erase ministerial accountability, but causation must be demonstrated.',[24],3),
('Dynastic concentration and succession dispute','Family access and a powerful working presidency invited succession scrutiny; Kavitha later publicly blamed KTR for decline.','Political criticism; not a judicial finding','Rival family member alleged harmful leadership and concentration of control.','A complete specific response to all October 2026 accusations was not established in inspected material.','Her exit and public dispute are documented; causal accusations remain attributed.','Do not infer a concluded succession or certify the registration/name of her separate platform.',[12,41],4),
('2023 affidavit disclosures','ADR’s reproduction records seven declared criminal cases and assets of ₹53,31,73,961 in the 2023 affidavit.','Election-era self-declaration; not current convictions register','Disclosure supplies electoral transparency, not a finding of illegal wealth.','Candidate’s sworn disclosure is the underlying account; no independent valuation undertaken.','Cases are declarations at nomination, not seven convictions or a current active-case total.','Asset totals include affidavit household/dependent categories; private identifiers are excluded.',[45],3)]
for i,(matter,f,status,allegation,response,finding,caution,ns,p) in enumerate(CO,1):
    fields={'Matter':matter,'Finding':f,'Procedural status':status,'Allegation / criticism':allegation,'KTR response / account':response,'Institutional finding / latest inspected stage':finding,'Qualification / next step':caution,'Status cutoff':ASOF}
    add('Controversies',f'CO{i:02d}',fields,ns,'Analysis',p,proof={'Finding':ns,'Procedural status':ns,'KTR response / account':ns,'Institutional finding / latest inspected stage':ns},independent=i in [1,2,3,4])

LEG=[
('Institution-builder','T-Hub, WE Hub and T-Works supply concrete institutional evidence for his development-oriented reputation. Their existence is better established than their additional economic impact attributable to him.',[16,17,19,47],'Documented institutions and bounded synthesis'),
('Technology-growth narrative','Official export and employment growth supports a strong sectoral expansion narrative. Baseline inheritance and wider economic forces prevent a one-person explanation.',[15],'Administrative evidence; causality unresolved'),
('Constituency durability','Five wins show durable Sircilla representation. The 2023 margin was much smaller than in 2018, and the 2009 victory had been exceptionally narrow.',[3,4,5,7,8],'Election-record comparison'),
('Uneven development','Weavers’ support for public orders coexisted with seasonal distress. Both benefits and limitations appear within the same local reporting, without requiring a false all-success/all-failure choice.',[22,23],'Independent local reporting, not a survey'),
('Party leadership test','The 2023 loss and 2024 parliamentary rout weakened the party he helped manage. His own explanation and Kavitha’s critique compete, but neither alone establishes a causal account.',[25,26,27,41],'Attributed competing political assessments'),
('Gender and representation','Women’s enterprise support is a substantive policy mechanism; the all-male early Cabinet context and later bus-remark controversy complicate a uniformly inclusive image.',[13,17,39,47],'Institutional design and reported conduct'),
('Accountability','Formula E, surveillance and Nerella require distinct levels of responsibility and proof. Refusal to quash, investigation, opposition accusation and conviction are different stages.',[28,31,32,34,37,38],'Procedural assessment; open outcomes'),
('Historical place','A prominent second-generation leader of Telangana’s statehood party, he connects movement-era electoral politics to post-formation investment promotion and later opposition. His long-term legacy remains unsettled.',[1,9,12,19,25,49],'Provisional synthesis, not a greatness ranking')]
for i,(t,f,ns,view) in enumerate(LEG,1):add('Legacy & Assessments',f'LA{i:02d}',{'Theme':t,'Finding':f,'Assessment basis':view},ns,'Analysis')

ERA=[
[
('TRS pursued a separate Telangana within undivided Andhra Pradesh; KTR’s first contests included opponents from Congress and an independent rival.',[3,4,49],'M'),
('Statehood required institutional action beyond a constituency mandate. The 2010 litigation concerned by-election rules; Parliament’s 2014 Act created Telangana.',[9,44],'M'),
('The narrow 2009 win and larger 2010 by-election victory belong to distinct contests; resignation linked the second contest to statehood mobilisation.',[3,4,49],'M'),
('The 2013–14 official IT baseline already records a substantial export and employment economy before his Telangana ministry. Subsequent growth did not begin from zero.',[15],'M'),
('His biography reports US education and work. Evidence isolating how international economic conditions shaped his early political choices was not assembled.',[1],'G'),
('Early campaign communication and media treatment were not systematically sampled. Later social-media prominence should not be projected backward.',[1,49],'G'),
('Family access to KCR and TRS coexisted with direct electoral competition; the 2010 resignation was a movement tactic rather than a routine term end.',[1,3,49],'M'),
('A constituency-level account of caste, class, gender and movement participation for the early phase remains incomplete; later weaving interviews cannot establish the 2009 voter coalition.',[3,22],'G'),
('Sircilla elections in 2009, 2010 and April 2014 were held in Andhra Pradesh. Telangana’s appointed day was 2 June 2014.',[3,9,5,44],'M'),
('ECI returns and court records support election facts more firmly than retrospective promotional biography supports motives; a faulty live-result article is used only for its historical resignation passage.',[3,9,49],'M')],
[
('KTR served in the first TRS government under KCR; his 2016 urban and industrial additions increased his executive responsibilities.',[1,10,11],'M'),
('The new state inherited legislative and administrative powers under the reorganisation framework. Ministerial decisions still operated through departments, Cabinet and statutory institutions.',[20,44],'M'),
('The GHMC campaign strengthened his urban profile, but municipal party results are distinct from his Sircilla Assembly mandate.',[5,10],'M'),
('Technology promotion and industrial approvals combined inherited Hyderabad capacity with new state-sponsored institutions such as T-Hub.',[15,16,20],'M'),
('T-Hub’s corporate networks and the GES-linked WE Hub announcement placed state economic promotion in international business circuits; this was subnational outreach.',[16,18],'M'),
('Startup coverage and public institutional launches supplied a visible development narrative. A systematic comparison of favourable and critical media exposure remains absent.',[16,18],'G'),
('Portfolio concentration under KCR and the later working-presidential appointment linked government prominence to party succession expectations; expectations were not appointments to the chief ministership.',[11,12],'M'),
('The all-male earlier Cabinet and reported torture of Dalit/BC villagers illustrate exclusions and accountability concerns alongside investment promotion.',[13,37,38],'M'),
('A Hyderabad-centred technology agenda operated alongside Sircilla representation and wider Telangana responsibilities; the two geographies should not be treated as identical.',[3,10,16,22],'M'),
('Contemporary portfolio reports, statute text and institutional reporting support chronology. Promotional claims and an uninspected original Nerella report limit stronger conclusions.',[10,11,20,37],'M')],
[
('TRS returned strongly in 2018, later renamed BRS; its 2023 defeat ended KTR’s ministerial period while he retained Sircilla.',[7,14,25],'M'),
('He held party office during a Cabinet gap, then resumed executive portfolios. TSPSC autonomy and building-permission law show distinct institutional responsibilities.',[12,13,21,36],'M'),
('The 2018 margin was 89,009 and the 2023 margin 29,687. A retained seat coexisted with a statewide loss; the sources do not isolate the reasons for each voter’s choice.',[7,8,25],'M'),
('Pandemic disruption exposed textile-worker vulnerability even as the official IT sector series expanded. Sectoral averages cannot represent all households.',[15,23],'M'),
('T-Works promotion linked Indian software and Taiwanese hardware capabilities; an opening ceremony and investment intentions are different from realised cross-border production.',[19],'M'),
('Flood briefings, pandemic reporting and examination-leak arguments made crisis communication part of his public role; official accounts and worker testimony did not always agree.',[23,24,35,36],'M'),
('Working presidency and BRS renaming broadened the party’s stated arena; his later admission of weak worker links is a retrospective diagnosis of organisation.',[12,14,27],'M'),
('Women entrepreneurs were explicitly targeted by WE Hub, while women textile workers also appeared in distress reporting. These are different social groups and policy relationships.',[23,46,47],'M'),
('Statewide urban responsibilities, a metropolitan startup cluster and a textile constituency created different demands; flood risk and local livelihoods qualify aggregate-growth narratives.',[22,24,46],'M'),
('Administrative outputs, interviews and live results use different units. The 2018 original denominator is unresolved; official 2023 results and reported 2018 counts are kept distinct.',[7,8,15,22],'M')],
[
('Congress won 64 seats and BRS 39 in 2023; BRS then suffered a Lok Sabha rout and defections in 2024. KTR’s influence now rested on legislative and party roles.',[25,26],'M'),
('Courts and investigating agencies became central arenas. The Formula E quashing refusal permitted investigation; it did not establish guilt.',[28,30,31,32],'M'),
('Sircilla’s 2023 win is a personal mandate; 2024 parliamentary losses are party outcomes. They must not be counted as a personal Lok Sabha defeat.',[8,26],'M'),
('He defended his earlier investment record from opposition. A comparable independent assessment of post-2023 economic outcomes and his influence was not assembled.',[29],'G'),
('International-event promotion reappeared as financial-accountability litigation. Evidence of a separate opposition-era diplomatic role was not established.',[28,29],'G'),
('Public denials, an apology and contentious family statements circulated through news and digital channels; no representative media-bias study was undertaken.',[32,39,41],'M'),
('Post-defeat self-critique and Kavitha’s exit exposed organisational and family tensions. Her accusations remain partisan testimony rather than an agreed explanation.',[27,41],'M'),
('Debate over women’s bus travel and southern representation placed gender and regional distribution in his opposition rhetoric; policy outcomes cannot be inferred from speeches.',[39,40],'M'),
('The 2025 delimitation intervention concerned future representation and centre–state relations. It did not itself change Telangana’s boundaries or allocate final seats.',[40],'M'),
('Fast-changing proceedings require dated procedural statements. November 2026 surveillance reporting still used future-tense filing language; later orders remain a priority gap.',[30,31,33,34],'M')]]
comparison=['TRS movement candidates and Congress/TDP-era legislators in undivided Andhra Pradesh','Other first-term Telangana ministers, urban administrators and state investment-promotion institutions','Contemporary Telangana ministers, opposition parties and pandemic-affected sectors','Opposition party organisers, legislators and similarly situated political litigants']
cautions=['Do not retroactively label pre-June 2014 elections as held in an existing Telangana state.','Do not treat later BRS branding or 2026 proceedings as contemporaneous facts of the first ministry.','Distinguish crisis conditions, inherited institutions and collective decisions from individual agency.','Do not treat an allegation, proposed charge or future delimitation scenario as a final outcome.']
for p,entries in enumerate(ERA,1):
    for i,(f,ns,disp) in enumerate(entries,1):
        add('Context & Constraints',f'CT-P{p}-{i:02d}',{'Career phase':phases[p-1],'Coverage dimension':'Era','Coverage item':era_items[i-1],'Finding':f,'Research disposition':'Material finding' if disp=='M' else 'Research limitation','Contemporary comparison group':comparison[p-1],'Presentism caution':cautions[p-1]},ns,'Analysis',status='Supported' if disp=='M' else 'Not reviewed')

GENDER=[
('Family access and direct electoral competition are documented. Comparative evidence isolating gender advantage or disadvantage in his recruitment was not assembled.',[1,3,12],'G'),
('His return to Cabinet in September 2019 coincided with two women joining after earlier all-male Cabinets. This is a representation milestone for the Cabinet, not a gender-first achievement of KTR.',[13],'M'),
('Family-based succession expectations are documented, but a matched comparison of male and female family members’ access and authority remains incomplete.',[12,41],'G'),
('IT, industry and urban portfolios are recorded; evidence that gender expectations determined those assignments is insufficient.',[1,10,11],'G'),
('The 2024 bus remarks and apology document controversy over his treatment of women. They do not by themselves prove that media treatment of KTR was gender-biased.',[39],'M'),
('No reliable gender-specific threat or security mechanism affecting his career was established in the inspected sources. Political criticism and legal process are not automatically gendered threats.',[28,32,41],'G'),
('WE Hub explicitly supports women through finance access, mentoring and institutional connections; official records establish an operating organisation.',[17,18,47],'M'),
('His apology addressed women as sisters, using kinship language. A sustained strategy of mobilising his own male identity is not established by this single instance.',[39],'M'),
('A male officeholder sponsored women-focused enterprise infrastructure. Symbolic inclusion and participation counts do not establish empowerment, profitability or representation of all women.',[17,46,47],'M'),
('Women’s entrepreneurship promotion and criticism of his later remarks offer contrasting episodes. A longitudinal feminist or gender-comparative assessment of the career was not assembled.',[18,39,47],'G')]
for i,(f,ns,disp) in enumerate(GENDER,1):
    add('Context & Constraints',f'CT-G-{i:02d}',{'Career phase':'Across phases; strongest policy evidence 2017–2023','Coverage dimension':'Gender','Coverage item':gender_items[i-1],'Finding':f,'Research disposition':'Material finding' if disp=='M' else 'Research limitation','Contemporary comparison group':'Men and women with comparable party, ministerial and family-network positions','Other identity relevance':'Family and place matter where evidenced; KTR’s caste or religion and voter identities are not inferred.','Presentism caution':'Apply equal scrutiny to family access; distinguish programme design, rhetoric and measured outcomes.'},ns,'Analysis',status='Supported' if disp=='M' else 'Not reviewed')
for name,t in tables.items():
    if name=='Context & Constraints':continue
    for row in t['rows']:
        if row.get('Career phase') in phases:
            p=phases.index(row['Career phase'])+1
            row['Context IDs']=f'CT-P{p}-01; CT-P{p}-02; CT-P{p}-03'

GAPS=[
('High','Phone-surveillance charging status','Latest inspected reports anticipate a chargesheet; filing and cognizance against KTR were not established.','Retrieve filed supplementary chargesheet and court cognizance/listing records as of the cutoff before changing status.',['CO02','OV14']),
('High','Formula E later orders','Discharge application and passport request reported; latest hearing adjourned to December. No final merits determination inspected.','Retrieve original discharge, passport and subsequent trial orders; preserve distinction between investigation threshold and guilt.',['CO01','OV13']),
('Medium','2010 and 2018 vote-share denominators','Candidate totals supported, but 2010 wide-table denominator incompletely reconciled and 2018 original return inaccessible.','Reconcile all candidate votes, NOTA and rejected ballots using original Form 20. Do not calculate shares from mismatched totals.',['EL02','EL04']),
('Medium','Exact tenure boundaries','Resignation acceptance in 2010 and end days of first/second ministry are not fixed from appointment or cessation notices.','Retrieve Speaker and governor/GAD notifications; preserve month/year precision until then.',['OF01','OF05','OF06','OF10']),
('High','Policy impact and distribution','Institutions, administrative outputs and local testimony do not isolate KTR’s causal contribution or equitable access.','Use independent audits, enterprise survival/placement data and constituency household evidence, with comparable baselines.',['PG01','PG05','PG08','PG10','LA02']),
('High','Nerella and TSPSC final accountability','Original inquiry documents and final dispositions establishing individual responsibilities were not assembled.','Retrieve police/court/commission records and distinguish ministerial, departmental and personal criminal responsibility.',['CO03','CO04']),
('Medium','Women’s Commission and defamation follow-up','Final commission finding and later KTR/Surekha orders unresolved; separate actor’s case withdrawn.','Obtain commission disposition and CC307/2025 orders; do not merge different complainants’ cases.',['CO05','CO06']),
('Medium','Early biography and gender mechanisms','Education and US-work narrative is substantially self-reported; five gender dimensions and six era items remain explicit research limitations.','Seek institutional biographical records and comparative recruitment, portfolio, security and media studies; avoid inferring absence of effects.',['OV03','CT-G-01','CT-G-10','CT-P1-05']),
('Low','Complete rural-administration record','Short early Panchayat Raj/Rural Development tenure is documented but not comprehensively evaluated.','Retrieve department annual reports and audits aligned to the actual 2014–2016 portfolio boundaries.',['PG14','OF04'])]
gaps=[{'id':f'G{i:02d}','priority':p,'topic':t,'gap':g,'next_action':n,'record_ids':rs,'status':'Open'} for i,(p,t,g,n,rs) in enumerate(GAPS,1)]
data={'schema_version':1,'subject':'K. T. Rama Rao (KTR)','as_of':ASOF,'guidance':'Five personal Assembly victories across four career phases. Offices, attributed positions and bounded analysis remain distinct. Ten gender and forty era dimensions have explicit dispositions. Review counts describe registered fields, not historical completeness.','tables':tables,'sources':sources,'claims':claims,'evidence':evidence,'coverage':{'Era':era_items,'Gender':gender_items},'phases':phases,'gaps':gaps}
for name,obj in [('research.json',data),('sources.json',sources),('retrievals.json',retrievals)]:
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'sources':len(sources),'rows':sum(len(t['rows']) for t in tables.values()),'claims':len(claims),'evidence':len(evidence)}))
