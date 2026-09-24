#!/usr/bin/env python3
"""Preserve authored records and inspected passages; build with the shared builder.

Run with the repository's openpyxl environment. No network access is performed.
Review entries describe Codex passage checks, not independent human verification.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASOF = '2026-09-24'
sources, retrievals, claims, evidence = [], [], [], []

def src(n, title, author, url, published, kind, locator, passage, note='', status='Passage inspected', origin=None):
    sid = f'S{n:03d}'
    sources.append({'Source ID':sid, 'Title':title, 'Author / institution':author,
        'Publication date':published, 'URL':url, 'Access date':ASOF, 'Source class':kind,
        'Primary / secondary':'Primary' if kind in ('Official record','Court order','Party / campaign') else 'Secondary',
        'Access status':status, 'Origin ID':origin or sid,
        'Locator':locator, 'Reliability / limitation':note or 'Read only for the specified passage and claim; no blanket verification of the publication.',
        'Language / geography':'English / India'})
    retrievals.append({'id':f'R{n:03d}', 'source_id':sid, 'url_or_query':url,
        'access_date':ASOF, 'route':'Canonical page or identified institutional/news reproduction',
        'access_status':status, 'origin_id':origin or sid, 'locator':locator,
        'passage_paraphrase':passage, 'method':'web.run: page text inspected',
        'result':'Relevant passage read' if status=='Passage inspected' else note,
        'next_action':'Reuse historical passage; refresh time-sensitive status when updating.'})

src(1,'Rahul Gandhi: current member biography','Lok Sabha Secretariat','https://sansad.in/ls/members/biography/4074?from=members',None,'Official record','Member ID 4074','No usable biography body returned.','Dynamic page returned no readable text; not used to support reviewed findings.','Located only')
src(2,'Leader of Opposition','Lok Sabha Secretariat','https://sansad.in/ls/about/leader-of-opposition',None,'Official record','Present leader; lines 23–31','Rahul Gandhi is listed as the present Leader of Opposition, with tenure beginning 9 June 2024.')
src(3,'Rahul Gandhi: 18th Lok Sabha MPTrack','PRS Legislative Research','https://prsindia.org/mptrack/18-lok-sabha/rahul-gandhi',None,'Dataset','Profile and Parliamentary Activity; data through 13 August 2026','INC MP for Rae Bareli, fifth term, start 9 June 2024. PRS records 17 debates, 64 questions and zero private member bills for 24 June 2024–13 August 2026. Attendance is N/A because the LoP does not sign the register.','Tracker periods are not the workbook cutoff. Counts are activity measures, not a leadership score.')
src(4,'Shri Rahul Gandhi: past party president','Indian National Congress','https://inc.in/leadership/past-party-presidents/shri-rahul-gandhi',None,'Party / campaign','Family; Political journey; Presidency; Post-presidency','Born 19 June 1970 to Rajiv and Sonia Gandhi. Entered electoral politics in 2004; AICC general secretary from 24 September 2007; vice-president January 2013; president from 16 December 2017. Lists the 2022–23 and 2024 yatras.','Interested party biography. Its four-term/Wayanad present-tense description is stale. May 2019 resignation is distinguished from July public confirmation.')
src(5,'Rahul Gandhi turns 53: before joining politics','Explained Desk, Indian Express','https://indianexpress.com/article/explained/explained-politics/rahul-gandhi-turns-53-what-he-was-doing-before-politics-8672843/lite/','2023-06-19','Journalism','Education and After college; lines 40–61','Security concerns after family assassinations affected schooling and university transfers. Graduated from Rollins in 1994. Reports Cambridge confirmation of a 1995 MPhil in Development Studies. Worked at Monitor; founded Backops.','Education confirmation is reproduced reporting; underlying university statement not retrieved.')
src(6,'General Election 2024: constituency-wise detailed result','Election Commission of India','https://www.eci.gov.in/eci-backend/public/all_files/GE-2024-statistical-report/33-Constituency-Wise-Detailed-Result.pdf',None,'Official record','Printed pp.165 and 444; Wayanad and Rae Bareli','Wayanad: Gandhi 647445, Annie Raja 283023, total counted including NOTA 1084653, total polled 1086459. Rae Bareli: Gandhi 687649, Dinesh Pratap Singh 297619, total polled 1039951.','Final report distinguishes total polled, counted votes and valid candidate votes. Workbook vote shares for 2024 use total polled, not election-night denominator.')
src(7,'Analysis of Vote Share and Margin of Victory: Lok Sabha 2019','Association for Democratic Reforms / National Election Watch','https://adrindia.org/sites/default/files/Analysis_of_Vote_Share_Margin_Of_Victory_Lok_Sabha__2019.pdf','2019-07-18','Dataset','Printed pp.26 and 69; Wayanad and Amethi','Wayanad: Gandhi 706367 versus P.P. Suneer 274597; total votes 1092197; margin 431770. Amethi: Gandhi 413394 versus Smriti Irani 468514; total votes 942453; loss margin 55120.','ADR compilation from electoral returns; not independent of the underlying election counts.')
src(8,'Amethi: past election results','Moneycontrol election desk','https://www.moneycontrol.com/elections/lok-sabha-election/uttar-pradesh/constituencies/amethi-constituency-s24led2008p037/',None,'Dataset','Past election results; lines 459–466 and 510–520','2009: Gandhi 464195, Asheesh Shukla 93997, 71.78%. 2014: Gandhi 408651, Smriti Irani 300748.','Page contains conflicting 2014 shares (46.71/46.72%) and a broken 2024 row. Use inspected historical vote totals; leave 2014 share unresolved.')
src(9,'2004 India General Election results','Elections.in','https://www.elections.in/parliamentary-constituencies/2004-election-results.html',None,'Dataset','Uttar Pradesh, constituency 21 Amethi; line 545','Rahul Gandhi, INC, won Amethi with 390179 votes against Chandra Parkash Mishra Matiyari, BSP, 99326.','Secondary election compilation. Canonical ECI/official mirror route did not yield the Uttar Pradesh table; primary reconciliation remains open.')
src(10,'Rahul Gandhi v Purnesh Ishwarbhai Modi: stay order','Supreme Court of India','https://api.sci.gov.in/supremecourt/2023/27941/27941_2023_4_55_45901_Order_04-Aug-2023.pdf','2023-08-04','Court order','Order paragraphs 4–11; pp.2–4','The Court stayed the conviction pending appeal, noting lack of reasons for the maximum two-year sentence and effects on voters. It also criticised the remarks and reserved the merits for the appellate court.','Stay is not acquittal. A later merits disposition was not found in this research. The PDF itself misstates the RP Act year; workbook does not reproduce that year.')
src(11,'Rahul Gandhi’s MP status restored','Liz Mathew, Indian Express','https://indianexpress.com/article/political-pulse/rahul-gandhi-returns-mp-lok-sabha-supreme-court-8880307/','2023-08-07','Journalism','Opening and closing paragraphs','Lok Sabha Secretariat restored membership on 7 August 2023 after the Supreme Court stay. Disqualification operated from 23 March 2023 following the conviction.','Reports the parliamentary notification; formal announcement was on 24 March, effective from conviction date.')
src(12,'Private complaint cannot be ED’s foundation for National Herald case, say Gandhis','Sohini Ghosh, Indian Express','https://indianexpress.com/article/legal-news/national-herald-case-gandhis-oppose-ed-plea-private-complaint-10889668/','2026-09-23','Journalism','Case status, reply and The case; lines 59–88','ED challenged refusal to take cognisance. Gandhis disputed the private-complaint basis in replies filed 18 September. ED alleges a conspiracy involving AJL assets; Young Indian acquired recovery rights over an AICC loan.','Allegations and legal submissions are attributed; no guilt finding is established.')
src(13,'Gandhis’ reply to Delhi High Court on National Herald case','Prashant Jha / Bar & Bench','https://www.barandbench.com/news/only-case-where-ed-proceeded-on-private-complaint-sonia-and-rahul-gandhi-to-delhi-high-court-on-national-herald-case','2026-09-22','Journalism','Paragraphs describing complaint, orders and adjournment; lines 48–73','ED prosecution complaint filed 15 April 2025; trial court refused cognisance 16 December 2025; ED challenged on 17 December. High Court hearing on 22 September 2026 was adjourned to 12 October. Gandhis contest jurisdiction.','Current procedural reporting independently corroborates S012; trial and High Court orders were not downloaded.')
src(14,'Rahul Gandhi’s resignation letter and accountability statement','Vaibhav Tiwari / NDTV','https://www.ndtv.com/india-news/rahul-gandhis-open-letter-full-text-at-times-i-stood-completely-alone-2063455','2019-07-03','Journalism','Resignation discussion; lines 225–248','Letter public on 3 July; resignation offered 25 May. Gandhi accepted responsibility for the 2019 defeat. Congress won 52 seats. He called for accountability and said institutional neutrality had been weakened.','His institutional claims are positions; report is used for public confirmation and stated reasons.')
src(15,'Rahul Gandhi at the conclusion of Bharat Jodo Yatra','Bashaarat Masood, Indian Express','https://indianexpress.com/article/political-pulse/rahul-modi-shah-doval-srinagar-bharat-jodo-yatra-8413548/','2023-01-31','Journalism','Concluding rally; lines 19–36','The march begun in Kanyakumari on 7 September 2022 concluded in Srinagar on 30 January 2023. Gandhi invoked family loss and nonviolence; described security advice against walking in Kashmir.','Speech claims about opponents are not adopted as facts. Distances vary by route definitions; no exact mileage used.')
src(16,'Nyay Patra 2024: Equity','Indian National Congress','https://manifesto.inc.in/en/equity/','2024-04-05','Party / campaign','Social Justice 1–2; minority rights; LGBTQIA+ 11','Manifesto promises a socioeconomic caste census, raising the 50% reservation cap, minority rights protection and consultation toward a law recognising LGBTQIA+ civil unions.','Evidence of party proposals, not implementation or independent validation of its social statistics.',origin='INC-MANIFESTO-2024')
src(17,'Nyay Patra 2024: Women','Indian National Congress','https://manifesto.inc.in/en/women/','2024-04-05','Party / campaign','Mahalakshmi 1–3; Women’s Empowerment 1–2','Proposes Rs 1 lakh yearly for each poor family, normally paid to its oldest woman; staged rollout. Promises earlier women’s seat reservation and half of central government jobs for women.','Party promises; not a national programme implemented by Rahul Gandhi.',origin='INC-MANIFESTO-2024')
src(18,'Nyay Patra 2024: Youth','Indian National Congress','https://manifesto.inc.in/en/youth/','2024-04-05','Party / campaign','Jobs 1–3 and Education 2, 13','Promises a one-year apprenticeship paying Rs 1 lakh for diploma holders/graduates under 25; filling central vacancies; action on exam-paper leaks; education policy consultation with states.','Party platform, not proof of fiscal feasibility or delivered jobs.',origin='INC-MANIFESTO-2024')
src(19,'Nyay Patra 2024: Farmers','Indian National Congress','https://manifesto.inc.in/en/farmers/','2024-04-05','Party / campaign','Agriculture 1–6','Promises statutory MSP guarantees, a statutory CACP and choices of agricultural marketing channels.','Party proposal; farmer movements and state administrations are distinct actors.',origin='INC-MANIFESTO-2024')
src(20,'Nyay Patra 2024: National Security','Indian National Congress','https://manifesto.inc.in/en/national-security/','2024-04-05','Party / campaign','Defence and Foreign Policy','Defence platform calls for a national security strategy and ending Agnipath; foreign-policy platform stresses continuity in strategic autonomy.','Use only stated party positions; territorial and causal allegations are not independently validated.',origin='INC-MANIFESTO-2024')
src(21,'Dissent over Rahul’s internal election system','Shaju Philip, Indian Express','https://indianexpress.com/article/political-pulse/in-kerala-youth-cong-dissent-over-rahuls-internal-election-system/','2014-06-25','Journalism','Kerala Youth Congress camp; lines 101–110','Kerala Youth Congress figures criticised internal elections for factional conflict and diversion of resources; some favoured returning to nominations.','Local criticism is not a national causal evaluation.')
src(22,'Youth Congress to retain internal polls','Subodh Ghildiyal, Times of India','https://timesofindia.indiatimes.com/india/youth-congress-to-retain-internal-polls/articleshow/36734347.cms','2014-06-18','Journalism','Internal reform and Rajiv Satav response; lines 119–133','IYC chief Rajiv Satav defended continued elections. Rahul’s reform replaced nominations in IYC/NSUI, aiming to reduce nepotism; critics alleged greater money influence.','Identifies reform and competing views; does not measure durable democratisation.')
src(23,'Ridiculed for a decade, Rahul Gandhi slows Modi juggernaut','Reuters; hosted by MarketScreener','https://www.marketscreener.com/news/latest/Ridiculed-for-a-decade-India-s-Rahul-Gandhi-slows-Modi-juggernaut-46900641/','2024-06-05','Journalism','Opening and analyst Rahul Verma; lines 932–946','Reuters depicts a recovery in Gandhi’s image after two marches. Analyst Rahul Verma credits mobilisation and clearer ideological opposition. Kharge was party president while Gandhi remained its prominent campaign face.','Election-count reporting is provisional; use final returns elsewhere. A Reuters reproduction is one origin.',origin='REUTERS-2024-06-05-GANDHI')
src(24,'The Resilience of India’s Fourth Party System','Milan Vaishnav and Caroline Mallory, Carnegie Endowment','https://carnegieendowment.org/research/2024/09/india-election-bjp-party-politics','2024-09','Academic / research','Evolution of party systems; 2024 interpretation; lines 61–104','Authors distinguish the coalition era through 2014 from BJP dominance thereafter. The 2024 result weakened rather than ended BJP centrality; INDIA still lacked unified leadership, programme and organisation.','Attributed interpretation written in 2024, not a forecast confirmed through 2026.')
src(25,'The T-Shirt Debate Shows India Is All About Testosterone','Revati Laul, The Wire','https://m.thewire.in/article/politics/rahul-gandhi-t-shirt','2023-01','Journalism / opinion','Opening argument; lines 47–65','Laul interprets discussion of Gandhi walking in a T-shirt in cold weather through local masculine ideals of physical endurance and leadership.','Situated gender interpretation based on colleagues’ observations, not representative voter research.')
src(26,'Congress camp’s Bihar post-mortem','Asad Rehman, Indian Express','https://indianexpress.com/article/political-pulse/congress-camps-bihar-post-mortem-rahul-yatra-fiasco-allavaru-problem-weak-structure-10375553/','2025-11-21','Journalism','Opening; interviews with ten losing candidates; lines 17–52','Congress won 6 of 61 seats contested in Bihar in 2025. Interviewed losing candidates criticised organisation, nominations, war rooms, alliance coordination and the voter-rights campaign.','Retrospective testimony from losing candidates has selection and self-exculpation risks; causes are attributed.')
src(27,'Rahul reportedly accepts shared responsibility for Bihar loss','Asad Rehman, Indian Express','https://indianexpress.com/article/political-pulse/rahul-equallyresponsible-bihar-loss-poll-review-10390484/','2025-11-28','Journalism','Review meeting; lines 18–27','Unnamed meeting participants said Gandhi accepted shared responsibility while questioning whether organisation alone explained allied parties’ losses. Congress publicly alleged roll-revision malpractice.','Private-meeting account based on unnamed sources; same outlet as S026, not independent corroboration of every cause.')
src(28,'Rs 72,000 NYAY promise','PTI, hosted by NDTV','https://www.ndtv.com/india-news/rs-72-000-will-be-given-to-beneficiaries-under-nyay-scheme-rahul-gandhi-2031993','2019-05-02','Journalism','Simdega speech; lines 231–242','Gandhi campaigned on a Rs 72000 transfer under NYAY if Congress came to power. He criticised GST’s effect on poor people and promised protection of tribal land.','Campaign speech. Avoid the report’s ambiguous people/families denominator when quantifying coverage.',origin='PTI-NYAY-2019-05-02')
src(29,'Supreme Court closes Rafale-related contempt proceedings','Express Web Desk, Indian Express','https://indianexpress.com/article/india/rafale-case-sc-closes-defamation-case-against-rahul-gandhi-says-he-needs-to-be-more-careful/','2019-11-14','Journalism','Disposition and response; lines 61–78','Court closed Meenakshi Lekhi’s contempt petition after Gandhi’s unconditional apology for falsely attributing his campaign slogan to the Court; cautioned him about future statements.','Contempt is separate from merits of Rafale procurement. Underlying 2019 order not inspected.')
src(30,'Rahul Gandhi escalates EC criticism amid SIR dispute','Aastha Jha, Times of India','https://timesofindia.indiatimes.com/india/rahul-gandhi-press-conference-on-ec-gyanesh-kumar-resignation-sir-congress-vote-chori-election-bjp/articleshow/134457370.cms','2026-09-24','Journalism','Press conference and ECI response; lines 150–156,183','Gandhi alleged widespread election rigging and demanded accountability. ECI said internal notes were routine scrutiny and final decisions were unanimous and legally grounded.','Contested political allegations; neither a press conference nor internal dissent proves that all elections were rigged.')
src(31,'Gandhi’s voter deletion allegations and EC response','Asad Rehman, Indian Express','https://indianexpress.com/article/india/rahul-gandhi-vote-chori-cec-gyanesh-kumar-protecting-killing-democracy-10257103/','2025-09-19','Journalism','Allegations and EC response; lines 20–54','Gandhi alleged attempted deletions in Aland and additions in Rajura. EC rejected his charges, citing a 2023 FIR and data sharing; Congress said requested technical information remained missing.','Documents and competing statements are reported; electoral manipulation at national scale is not adjudicated here.')
src(32,'Land Acquisition Second Amendment Bill 2015','PRS Legislative Research','https://prsindia.org/billtrack/the-right-to-fair-compensation-and-transparency-in-land-acquisition-rehabilitation-and-resettlement-second-amendment-bill-2015','2015','Research / legislative brief','Introduction and Table 1','2013 law required consent for specified private/PPP acquisition and social-impact assessment. 2015 bill proposed exemptions for five project classes; referred to a joint committee on 12 May.','Bill design and status record; does not establish Gandhi alone caused any legislative outcome.')
src(33,'Women’s reservation Bill and OBC quota: Rahul Gandhi’s speech','Express News Service','https://indianexpress.com/article/india/lok-sabha-rahul-gandhi-women-reservation-bill-obc-quota-8948629/','2023-09-21','Journalism','Lok Sabha speech of 20 September; lines 73–90','Gandhi supported the women’s reservation bill, asked for an OBC women’s quota and immediate implementation without census/delimitation delay.','Supports speech position, not delivery of reservation or accuracy of all quoted statistics.')
src(34,'Rahul Gandhi accepts responsibility for UP result','NDTV Correspondent','https://www.ndtv.com/assembly/i-take-responsibility-says-rahul-gandhi-about-up-results-470319','2012-03-07','Journalism','Result and campaign; lines 284–294','Congress won 28 of 403 UP seats in 2012. Gandhi accepted campaign responsibility and said organisation was weak; contemporary coverage compared him with Akhilesh Yadav.','Party-wide election, not a personal assembly contest.')
src(35,'Rahul Gandhi welcomes caste-enumeration decision and seeks timeline','Mansi Jagani, Indian Express','https://indianexpress.com/article/india/rahul-gandhi-caste-census-population-congress-centre-cabinet-9975117/','2025-04-30','Journalism','Government decision and reactions; lines 20–40','Gandhi supported the government’s caste-enumeration decision, sought funding and a timeline, and repeated the demand to lift the reservation cap. Government criticised Congress’s earlier record.','Credit claims are disputed; announcement is not completed enumeration.')
src(36,'Government decision to include caste enumeration in census','Ministry of Home Affairs / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=2125576','2025-04-30','Official record','Release 2125576; lines 20–25','Home Ministry reports CCPA decision to include caste enumeration in the forthcoming census. Amit Shah attributes it to the Modi government and criticises Congress.','Official evidence for decision and government position; not neutral assessment of Congress.')
src(37,'Rahul Gandhi vows to oppose land bill','PTI, Economic Times','https://economictimes.indiatimes.com/news/politics-and-nation/rahul-gandhi-vows-to-oppose-land-bill-inside-and-outside-parliament/articleshow/47249971.cms','2015-05-12','Journalism','Parliamentary debate report','Gandhi opposed the land-acquisition amendments inside and outside Parliament; NDA allies Shiv Sena and Akali Dal also raised reservations.','Opposition was broader than one leader.',origin='PTI-LAND-2015-05-12')
src(38,'Rahul Gandhi criticises convicted-lawmakers ordinance','Prasad Sanyal, NDTV','https://www.ndtv.com/india-news/rahul-gandhi-calls-ordinance-on-convicted-lawmakers-nonsense-huge-embarrassment-for-pm-535906','2013-09-27','Journalism','Press Club remarks and responses; lines 225–233','Gandhi publicly repudiated the proposed ordinance protecting convicted legislators; BJP critics said this undermined Prime Minister Manmohan Singh. Gandhi framed his objection as opposition to compromise on corruption.')
src(39,'Government withdraws ordinance plan','Business Standard','https://www.business-standard.com/article/politics/govt-bows-before-rahul-withdraws-ordinance-plan-113100200706_1.html','2013-10-05','Journalism','Cabinet decision reported 2 October','Cabinet withdrew the proposed ordinance and related bill after Gandhi’s public criticism.','Multiple institutions and opponents were involved; distinguish influence from constitutional authority.')
src(40,'Assembly election results, December 2018','NDTV election desk','https://www.ndtv.com/india-news/election-results-2018-live-rajasthan-madhya-pradesh-telangana-chhattisgarh-mizoram-1960481','2018-12-12','Journalism','Lead; lines 230–233','Reports BJP setbacks and Congress gains in Rajasthan, Madhya Pradesh and Chhattisgarh under Gandhi’s presidency; also Congress losses in Mizoram and failure in Telangana.','Live article includes counting-stage language; no exact final seat totals adopted.')
src(41,'Elected members: Lok Sabha 2019','Chief Electoral Officer, Kerala','https://www.ceo.kerala.gov.in/electedmembers',None,'Official record','2019 Lok Sabha; Wayanad row','Wayanad Rahul Gandhi INC; victory margin 431770; vote share 64.67%.','The 431770 figure is margin, not candidate votes. Historic table, not current MP roster.')
src(42,'Rahul Gandhi: 17th Lok Sabha MPTrack','PRS Legislative Research','https://prsindia.org/mptrack/17-lok-sabha/rahul-gandhi',None,'Dataset','Profile; activity from 1 June 2019 to 10 February 2024','Wayanad term displayed 23 May 2019–5 June 2024. PRS records 51% attendance, 8 debates, 99 questions and zero private bills. Lists railway, farmers and connectivity interventions.','Displayed tenure does not split the 2023 disqualification; workbook does. Activity period is shorter than term.')
src(43,'Wayanad seat resignation','PTI, NDTV','https://www.ndtv.com/india-news/rahul-gandhi-resigns-from-wayanad-seat-retains-raebareli-5918402','2024-06-18','Journalism','Lok Sabha bulletin reproduction; lines 231–241','Speaker accepted resignation from Wayanad effective 18 June 2024. Gandhi retained Rae Bareli; Congress nominated Priyanka for the coming Wayanad by-election.','Reproduces institutional bulletin; canonical transcript timed out.',origin='LS-BULLETIN-2024-06-18')

S={s['Source ID']:s for s in sources}
R={r['source_id']:r for r in retrievals}
for sid in ('S007','S041'):
    S[sid]['Origin ID']='ECI-GE-2019'
    R[sid]['origin_id']='ECI-GE-2019'
R['S020']['passage_paraphrase']+=' Proposes parliamentary select-committee oversight of the NSC and NSA.'
tables={}
def table(name, lead, dates=()):
    tables[name]={'lead_columns':lead,'date_columns':list(dates),'rows':[]}
def add(name, rid, fields, ids, typ='Recorded fact', status='Supported', checked=None, note='', phase=None, priority='Normal', independent=False):
    idcol={'Overview':'Overview ID','Context & Constraints':'Context ID','Career Timeline':'Timeline ID','Elections':'Election ID','Offices & Party':'Position ID','Controversies':'Matter ID','Legacy & Assessments':'Assessment ID'}.get(name,'Record ID')
    row={idcol:rid,**fields,'Claim type':typ,'Source IDs':'; '.join(ids)}
    if phase: row['Career phase']=phase
    if note: row['Research note']=note
    tables[name]['rows'].append(row)
    if typ=='Method / scope': return row
    if checked is None:
        checked={k:ids for k in fields if k in ('Finding / value','Finding','Description','Record','Assessment','Position / institution')}
    for field, support in checked.items():
        cstatus=status
        if isinstance(support,dict):
            cstatus=support.get('status',status); support=support.get('ids',ids)
        val=row[field]
        cid=f'C-{rid}-{len([c for c in claims if c["record_id"]==rid])+1:02d}'
        evs=[]
        if cstatus in ('Supported','Partially supported','Disputed'):
            for sid in support:
                if R[sid]['access_status']!='Passage inspected': continue
                eid=f'EV-{len(evidence)+1:04d}';evs.append(eid)
                evidence.append({'id':eid,'claim_id':cid,'source_id':sid,'retrieval_id':R[sid]['id'],
                    'locator':R[sid]['locator'],'passage_paraphrase':R[sid]['passage_paraphrase'],
                    'relation':'Supports','reviewed_by':'Codex: passage-to-statement review','reviewed_at':ASOF,
                    'note':'Read as combined support where a field has several sources. Attributed statements establish what was said, not the underlying allegation.'})
        claims.append({'id':cid,'sheet':name,'record_id':rid,'field':field,'statement':val,
            'fingerprint':hashlib.sha256(json.dumps(val,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            'claim_type':typ,'status':cstatus,'priority':priority,'candidate_source_ids':support,
            'evidence_ids':evs,'contradictions':[], 'review_note':note or ('Analytical synthesis of cited records; causal limits retained.' if typ=='Analysis' else 'Statement checked against indicated passage(s).'),
            'requires_independent_corroboration':independent})
    return row

P1='P1 | Entry and UPA years (2004–2013)'
P2='P2 | Opposition and party presidency (2014–2019 election)'
P3='P3 | Resignation, yatras and recovery (2019–2024 election)'
P4='P4 | Leader of Opposition (June 2024–September 2026)'
phases=[P1,P2,P3,P4]

table('Overview',['Overview ID','Topic','Finding / value'])
table('Context & Constraints',['Context ID','Career phase','Coverage item','Finding'],['Start date','End date'])
table('Career Timeline',['Timeline ID','Period','Event','Description'],['Exact date'])
table('Elections',['Election ID','Year','Constituency','Result','Candidate votes','Signed vote margin'])
table('Offices & Party',['Position ID','Position / institution','Period','Finding'],['Start date','End date'])
table('Policy & Governance',['Record ID','Initiative / decision','Finding','Stage'])
table('Ideas & Political Method',['Record ID','Topic','Finding'])
table('Controversies',['Matter ID','Matter','Finding','Procedural status'],['Latest evidence date'])
table('Legacy & Assessments',['Assessment ID','Theme','Assessment'])

# Authored tables follow below.
def overview(rid, topic, finding, ids, typ='Recorded fact', **kw):
    return add('Overview',rid,{'Topic':topic,'Finding / value':finding},ids,typ,**kw)

overview('OV01','Subject','Rahul Gandhi (राहुल गांधी); Indian National Congress politician; born 19 June 1970; living.',['S004'])
overview('OV02','Current office','MP for Rae Bareli, Uttar Pradesh, in his fifth Lok Sabha term; Leader of Opposition, Lok Sabha, effective 9 June 2024.',['S002','S003'],priority='High')
overview('OV03','Political geography','Amethi (2004–2019), Wayanad (2019–2024, with a 2023 disqualification interruption), then Rae Bareli. Won Wayanad again in 2024 and relinquished it effective 18 June.',['S004','S011','S042','S043'],priority='High')
overview('OV04','Party leadership','AICC general secretary from September 2007; Congress vice-president from January 2013; president from 16 December 2017. Resigned after the 2019 defeat; confirmed departure publicly on 3 July.',['S004','S014'],priority='High')
overview('OV05','Education and access','Rollins graduate (1994), Cambridge MPhil in Development Studies (1995). Family political prominence aided access; assassinations and security concerns also shaped his early life.',['S005','S004'],typ='Analysis')
overview('OV06','Electoral record','Seven constituency contests across five general elections: six wins and one loss. The loss was Amethi in 2019; two wins in 2024 count as one parliamentary term.',['S006','S007','S008','S009'],typ='Analysis',priority='High')
overview('OV07','Career in brief','He moved from youth-organisation reform and party succession to national opposition campaigning, two cross-country yatras, and formal parliamentary opposition leadership.',['S004','S022','S015','S002'],typ='Analysis')
overview('OV08','Principal contributions','His clearest documented contributions are organisational experimentation, sustained opposition advocacy and public mobilisation. The caste-enumeration debate illustrates agenda influence with disputed credit.',['S021','S022','S023','S035','S036'],typ='Analysis')
overview('OV09','Policy focus','Caste representation, redistribution, employment, farmers’ protections, women’s representation and constitutional pluralism recur in his speeches and Congress’s platform.',['S016','S017','S018','S019','S033','S028'],typ='Analysis')
overview('OV10','Limitations and reversals','The 2012 UP setback, 2019 national defeat and Amethi loss, and the 2025 Bihar setback show that campaign visibility has not consistently produced electoral recovery.',['S034','S014','S007','S026'],typ='Analysis')
overview('OV11','Legal status','The 2023 defamation conviction was stayed, not overturned by the inspected order. In the National Herald money-laundering matter, ED’s challenge to refusal of cognisance remained before the High Court in September 2026.',['S010','S012','S013'],priority='High',note='Defamation appeal merits after the 2023 stay remain an open retrieval gap. National Herald latest inspected hearing report: 22 September 2026.')
overview('OV12','Gender and political reception','Dynastic access and security are evidenced; a specifically gender-based barrier to his advancement is not established. Commentary about physical endurance supplies a bounded example of masculine campaign imagery.',['S004','S005','S025'],typ='Analysis')
overview('OV13','Historical significance','A major test case for Congress’s adaptation to BJP-centred competition. The 2024 recovery enlarged opposition space; it did not itself end BJP centrality or settle Congress’s organisational weaknesses.',['S023','S024','S026'],typ='Analysis')
overview('OV14','Scope and cutoff','Research snapshot as of 24 September 2026. Four political phases; formative background before 2004. Later developments are included selectively, not as an exhaustive daily chronicle.',[],typ='Method / scope')
overview('OV15','Reading the evidence','Supported means the registered field was checked against an inspected passage, or explicitly identified synthesis. It does not certify every contextual implication. Interested sources verify stated positions; an allegation is not a finding.',[],typ='Method / scope')
overview('OV16','Open gaps','Original 2004–2014 election returns, two older vote shares, detailed committee tenure dates, later defamation appeal merits, constituency outcome attribution and systematic gender evidence need further work.',[],typ='Method / scope')
overview('OV17','Numbers and policy rules','Blank election values mean unresolved data. Signed margins are candidate minus principal opponent votes. 2024 shares use ECI total-polled denominators. Manifesto commitments remain proposals unless a separate adoption record is cited.',[],typ='Method / scope')
overview('OV18','Application check','Structural checks, arithmetic, passage review, application recalculation and visual inspection are separate. Formula-only viewers may show blank values before recalculation. The delivery note states the application checks completed.',[],typ='Method / scope')

timeline=[
('T01','1970','Birth and family','Born on 19 June 1970 to Rajiv and Sonia Gandhi.',['S004'],'1970-06-19',None),
('T02','1984–1995','Education under security constraints','Family assassinations prompted security-related education changes; completed Rollins graduation and a Cambridge MPhil.',['S005'],None,None),
('T03','Before 2004','Professional work','Worked with Monitor in London and established Backops before electoral entry.',['S005'],None,None),
('T04','2004','First Lok Sabha victory','Entered electoral politics and won Amethi for Congress.',['S009','S004'],None,P1),
('T05','September 2007','Youth and student organisation brief','Appointed AICC general secretary on 24 September, responsible for IYC and NSUI.',['S004'],'2007-09-24',P1),
('T06','2009','Second Amethi victory','Re-elected with 464195 votes, ahead of BSP candidate Asheesh Shukla.',['S008'],None,P1),
('T07','May 2011','Bhatta Parsaul mobilisation','Party biography records his arrest while supporting farmers protesting acquisition terms on 11 May.',['S004'],'2011-05-11',P1),
('T08','March 2012','UP campaign setback','Congress won 28 of 403 assembly seats; Gandhi publicly accepted responsibility for the campaign.',['S034'],None,P1),
('T09','January 2013','Congress vice-president','Became Congress vice-president.',['S004'],None,P1),
('T10','September–October 2013','Ordinance confrontation','Opposed the convicted-legislators ordinance on 27 September; Cabinet decided on 2 October to withdraw the proposal and related bill.',['S038','S039'],None,P1),
('T11','2014','National opposition phase','Retained Amethi while the BJP became the central party in the new national electoral system.',['S008','S024'],None,P2),
('T12','May 2015','Land-acquisition opposition','Led Congress opposition to proposed acquisition-law changes, using parliamentary and public mobilisation.',['S037'],None,P2),
('T13','December 2017','Congress presidency','Assumed Congress presidency on 16 December 2017.',['S004'],'2017-12-16',P2),
('T14','December 2018','Mixed state election results','Congress gains in Rajasthan, MP and Chhattisgarh accompanied setbacks in Telangana and Mizoram.',['S040'],None,P2),
('T15','May 2019','Dual contest and defeat','Won Wayanad but lost Amethi to Smriti Irani; Congress’s national tally was 52.',['S007','S014'],None,P2),
('T16','July 2019','Public resignation letter','Publicly confirmed departure from the presidency and accepted responsibility for the national defeat.',['S014'],'2019-07-03',P3),
('T17','November 2019','Rafale-related contempt closure','Supreme Court closed the contempt matter following an unconditional apology over attribution of a slogan to the Court.',['S029'],'2019-11-14',P3),
('T18','September 2022–January 2023','Bharat Jodo Yatra','March from Kanyakumari to Srinagar ran from 7 September 2022 to 30 January 2023.',['S015'],None,P3),
('T19','March–August 2023','Conviction, disqualification and return','Defamation conviction led to disqualification effective 23 March. Supreme Court stayed conviction 4 August; membership restored 7 August.',['S010','S011'],None,P3),
('T20','January–March 2024','Bharat Jodo Nyay Yatra','Party record dates the Manipur-to-Mumbai journey from 14 January to 16 March 2024.',['S004'],None,P3),
('T21','June 2024','Two constituency victories','Won Rae Bareli and Wayanad; later retained Rae Bareli and relinquished Wayanad.',['S006','S043'],None,P4),
('T22','June 2024','Leader of Opposition','Parliament records the office as effective from 9 June 2024.',['S002'],'2024-06-09',P4),
('T23','April 2025','Caste-enumeration announcement','Welcomed the government decision and sought an implementation timetable and funding.',['S035','S036'],'2025-04-30',P4),
('T24','November 2025','Bihar setback','Congress won six seats; press accounts described organisational criticism and Gandhi’s reported acceptance of shared responsibility.',['S026','S027'],None,P4),
('T25','September 2026','Current legal and electoral disputes','National Herald High Court proceedings and his renewed allegations against the Election Commission remained prominent. The latter are contested claims.',['S013','S030'],None,P4),
]
for rid,period,event,description,ids,day,phase in timeline:
    add('Career Timeline',rid,{'Period':period,'Event':event,'Description':description,'Exact date':day,'Date precision':'Day' if day else 'Year or stated range'},ids,
        'Attributed position' if rid in ('T07','T20','T23','T24','T25') else 'Recorded fact',phase=phase,
        checked={'Description':ids,**({'Exact date':ids} if day else {})})

elections=[
('EL01',2004,'Amethi','Uttar Pradesh','Won',390179,'Chandra Parkash Mishra Matiyari','BSP',99326,None,None,['S009'],P1,'Pre-2008 delimitation; numbered 21 in the inspected 2004 table. Vote share not recovered from an inspected primary return.'),
('EL02',2009,'Amethi','Uttar Pradesh','Won',464195,'Asheesh Shukla','BSP',93997,.7178,None,['S008'],P1,'Post-delimitation seat numbered 37. Share is the source-reported percentage; denominator not independently reconciled.'),
('EL03',2014,'Amethi','Uttar Pradesh','Won',408651,'Smriti Irani','BJP',300748,None,None,['S008'],P2,'Vote totals agree within source. Its two tables give 46.71% and 46.72%; share is left blank pending primary return.'),
('EL04',2019,'Amethi','Uttar Pradesh','Lost',413394,'Smriti Irani','BJP',468514,413394/942453,942453,['S007'],P2,'Share computed from ADR total votes. This personal defeat is separate from Congress’s national result.'),
('EL05',2019,'Wayanad','Kerala','Won',706367,'P.P. Suneer','CPI',274597,.6467,1092197,['S007','S041'],P2,'CEO Kerala reports 64.67%; ADR rounds the winner share to 64.70%. Both give a 431770 margin.'),
('EL06',2024,'Rae Bareli','Uttar Pradesh','Won',687649,'Dinesh Pratap Singh','BJP',297619,687649/1039951,1039951,['S006'],P4,'Share uses final ECI total votes polled, 1039951; 66.12% rounded. Retained this seat.'),
('EL07',2024,'Wayanad','Kerala','Won',647445,'Annie Raja','CPI',283023,647445/1086459,1086459,['S006','S043'],P4,'Share uses ECI total polled, 1086459: 59.59%. Election-night 59.69% uses 1084653 counted votes including NOTA. Relinquished effective 18 June 2024.'),
]
for rid,year,const,state,result,votes,opp,oparty,ovotes,share,denom,ids,phase,note in elections:
    fields={'Year':year,'Constituency':const,'Result':result,'Candidate votes':votes,'Signed vote margin':votes-ovotes,
        'Opponent':opp,'Opponent party':oparty,'Opponent votes':ovotes,'Vote share':share,'Share denominator':denom,
        'State':state,'Party':'INC','House / route':'Lok Sabha / direct','Candidate status':'Contestant',
        'Finding':f'{result}: {votes:,} votes against {opp} ({ovotes:,}); signed margin {votes-ovotes:+,}.',
        'Margin unit':'Votes; negative = loss','Geography / denominator note':note}
    checked={k:ids for k in ('Finding','Year','Candidate votes','Opponent votes','Signed vote margin')}
    if share is not None: checked['Vote share']=ids
    add('Elections',rid,fields,ids,checked=checked,note=note,phase=phase,priority='High')

offices=[
('OF01','MP, 14th Lok Sabha / Amethi','2004–2009','First elected term for INC; constituency inherited as a party stronghold, with candidature validated by election.',['S004','S009'],P1,None,None,'Elected'),
('OF02','MP, 15th Lok Sabha / Amethi','2009–2014','Second elected term, following the 2009 Amethi victory.',['S004','S008'],P1,None,None,'Elected'),
('OF03','MP, 16th Lok Sabha / Amethi','2014–2019','Third elected term; lost the seat in the 2019 election.',['S004','S007','S008'],P2,None,None,'Elected'),
('OF04','MP, 17th Lok Sabha / Wayanad','May 2019–March 2023','Elected from Wayanad in 2019; disqualified effective 23 March 2023 after the defamation conviction.',['S042','S011'],P3,'2019-05-23','2023-03-23','Elected; interrupted'),
('OF05','MP, 17th Lok Sabha / Wayanad, restored','7 August 2023–5 June 2024','Membership restored after the conviction stay; PRS records term ending 5 June 2024.',['S011','S042'],P3,'2023-08-07','2024-06-05','Reinstated'),
('OF06','Member-elect / Wayanad, 18th Lok Sabha','June 2024–18 June 2024','Won again but gave up Wayanad effective 18 June before the new House’s oath-taking sessions.',['S006','S043'],P4,None,'2024-06-18','Election followed by resignation'),
('OF07','MP, 18th Lok Sabha / Rae Bareli','9 June 2024–present','Fifth Lok Sabha term; retained Rae Bareli after winning two seats.',['S003','S043'],P4,'2024-06-09',None,'Elected'),
('OF08','Leader of Opposition / Lok Sabha','9 June 2024–present','Formal parliamentary office concurrent with Rae Bareli membership; effective date follows Lok Sabha’s register.',['S002','S003'],P4,'2024-06-09',None,'Recognition by Speaker'),
('OF09','AICC general secretary / IYC and NSUI brief','From 24 September 2007','Party appointment placed the youth and student organisations in his organisational brief. Exact end of each charge not independently established.',['S004'],P1,'2007-09-24',None,'Party appointment'),
('OF10','Vice-president / Indian National Congress','January 2013–December 2017','Served as vice-president before taking over the presidency in December 2017.',['S004'],P2,None,None,'Party appointment'),
('OF11','President / Indian National Congress','16 December 2017–2019 resignation','Resignation offered 25 May 2019 and publicly confirmed 3 July. Party biography dates departure to May; do not erase this distinction.',['S004','S014'],P2,'2017-12-16',None,'Party succession; resignation'),
('OF12','Parliamentary committees / historical memberships','Across parliamentary career','Party biography lists Defence, Home Affairs, External Affairs, Human Resource Development and Civil Aviation committee assignments. Detailed start/end dates require the original committee records.',['S004'],P3,None,None,'Committee membership'),
('OF13','Movement leadership / Bharat Jodo and Nyay yatras','2022–2024','Led public journeys combining political communication, listening and organisational mobilisation; this was a movement role rather than a government ministry.',['S004','S015'],P3,None,None,'Party-led mobilisation'),
]
for rid,title,period,finding,ids,phase,start,end,route in offices:
    add('Offices & Party',rid,{'Position / institution':title,'Period':period,'Finding':finding,'Start date':start,'End date':end,
        'Selection / exit':route,'Date note':'Blank endpoints mean ongoing or insufficient precision; read Period and Finding.'},ids,
        checked={'Finding':ids,**({'Start date':ids} if start else {}),**({'End date':ids} if end else {})},phase=phase)

policy=[
('PG01','Youth organisation elections','Introduced elections in IYC/NSUI to replace nominations. Critics reported factionalism; supporters defended wider access.','Organisational implementation','Led','No causal estimate of long-term membership quality or electoral effect.',['S021','S022'],P1),
('PG02','Convicted-lawmakers ordinance','Public opposition preceded Cabinet’s decision to withdraw the ordinance proposal and related bill in October 2013.','Government decision following advocacy','Opposed','Cabinet retained decision authority; other opponents and presidential scrutiny also mattered.',['S038','S039'],P1),
('PG03','Land-acquisition protections','Opposed proposed exemptions from consent and social-impact provisions; mobilised both in Parliament and outside it.','Legislative opposition','Opposed','PRS explains the bill; the wider coalition of resistance prevents exclusive personal attribution.',['S037','S032'],P2),
('PG04','NYAY income-support proposal','Campaigned in 2019 on a Rs 72000 transfer under NYAY if Congress won power.','Campaign proposal','Led advocacy','Congress remained in opposition; this record establishes a promise, not poverty reduction.',['S028','S014'],P2),
('PG05','Caste census and reservation ceiling','Congress’s 2024 platform promised caste enumeration and raising the reservation cap; Gandhi welcomed the government’s 2025 enumeration decision and sought a timetable.','Proposal; separate government adoption of enumeration','Advocated','The government made the decision. Completed census results and a causal estimate of Gandhi’s influence are outside inspected evidence.',['S016','S035','S036'],P4),
('PG06','Women’s legislative representation','Supported the 2023 women’s reservation bill while calling for an OBC women’s quota and earlier implementation.','Parliamentary advocacy','Supported with amendments sought','Speech support does not establish that his preferred amendments were adopted.',['S033'],P3),
('PG07','Mahalakshmi','Congress proposed Rs 1 lakh annually per poor family, generally paid to its oldest woman, through phased implementation.','2024 manifesto proposal','Associated: party platform','No national implementation or beneficiary outcome is credited to Gandhi.',['S017'],P3),
('PG08','Youth employment and examination integrity','Congress proposed paid one-year apprenticeships for qualified under-25s, filling government vacancies and action against paper leaks.','2024 manifesto proposal','Associated: party platform','Spending, take-up and job creation are unmeasured proposals here.',['S018'],P3),
('PG09','MSP legal guarantee','Congress’s manifesto proposed legal guarantees for MSP and statutory status for the CACP.','2024 manifesto proposal','Associated: party platform','Farmer organisations, legislatures and governments are distinct actors; feasibility is not assessed.',['S019'],P3),
('PG10','Military recruitment','Congress’s 2024 defence platform proposed scrapping Agnipath and restoring the previous recruitment system.','2024 manifesto proposal','Associated: party platform','No military command, defence ministry decision or implementation is attributed to Gandhi.',['S020'],P3),
('PG11','Constituency advocacy','PRS lists Wayanad railway, farmer-distress and connectivity interventions; later lists calls for rehabilitation following Wayanad landslides.','Parliamentary intervention','Advocated','Requests establish representation activity; project completion and disaster-recovery outcomes require administrative records.',['S042','S003'],P4),
('PG12','Parliamentary activity: 17th Lok Sabha','PRS records 51% attendance, 8 debates, 99 questions and zero private member bills for 1 June 2019–10 February 2024.','Observed activity','Participated','The period includes political mobilisation and the membership interruption. Counts cannot alone measure opposition effectiveness.',['S042'],P3),
('PG13','Parliamentary activity: 18th Lok Sabha','PRS records 17 debates, 64 questions and zero private member bills for 24 June 2024–13 August 2026. LoP attendance is N/A because he does not sign the register.','Observed activity','Participated','N/A is not zero attendance. This dataset ends before the workbook cutoff.',['S003'],P4),
]
for rid,title,finding,stage,role,limit,ids,phase in policy:
    add('Policy & Governance',rid,{'Initiative / decision':title,'Finding':finding,'Stage':stage,'Documented role':role,
        'Attribution / outcome limit':limit},ids,'Attributed position' if 'proposal' in stage.lower() or rid=='PG06' else 'Recorded fact',phase=phase)

ideas=[
('IM01','Dynastic access and legitimacy','Family name and organisational access assisted entry and leadership succession; opponents used the same background to challenge his credibility.',['S004','S023'],P1),
('IM02','Organisation and democratisation','Internal youth elections offered an alternative to nomination, but internal critics saw factional and financial competition. Democratisation is an objective and a disputed outcome.',['S021','S022'],P1),
('IM03','Confrontation within his own party','The 2013 ordinance episode displayed influence over a Congress-led government while exposing tension between party leadership and the prime minister.',['S038','S039'],P1),
('IM04','Economic inequality and farmer politics','Land-law opposition and NYAY linked criticism of concentrated economic power to a proposed redistributive alternative.',['S037','S028'],P2),
('IM05','Accountability after defeat','His 2019 letter accepted personal electoral responsibility and called for wider accountability; it simultaneously alleged unequal institutional conditions.',['S014'],P3),
('IM06','Yatra and listening','The yatras combined direct contact, repeated public appearances and a unity message. Image renewal is documented; the marches’ independent electoral effect is not isolated.',['S015','S023'],P3),
('IM07','Caste representation','Advocacy increasingly connected representation data, caste enumeration and affirmative action. His demands intersected with longstanding regional-party agendas.',['S016','S035'],P4),
('IM08','Pluralism and constitutional rights','Congress’s platform defends religious and linguistic minority rights; Gandhi’s march speeches framed violence and exclusion as political problems.',['S016','S015'],P3),
('IM09','Coalition method','In 2024 Gandhi campaigned within a multi-party opposition while Kharge headed Congress. Carnegie cautioned that INDIA lacked a common leadership and organisational structure.',['S023','S024'],P4),
('IM10','Gender and physical imagery','Revati Laul interpreted T-shirt/endurance discussion as masculine political messaging. This is a local, attributed interpretation, not evidence that all voters responded that way.',['S025'],P3),
('IM11','Electoral integrity as an opposition issue','From 2025 through September 2026 he used press conferences and roll data to allege manipulation. Election authorities rejected his broad charges; underlying national claims remain contested.',['S031','S030'],P4),
('IM12','Foreign-policy and security ideas','The 2024 party platform coupled strategic-autonomy language with demands for greater parliamentary security oversight. This is a proposed framework, not a diplomatic record in executive office.',['S020'],P3),
]
for rid,topic,finding,ids,phase in ideas:
    add('Ideas & Political Method',rid,{'Topic':topic,'Finding':finding},ids,'Analysis',phase=phase)

controversies=[
('CO01','Modi-surname defamation conviction and disqualification','Trial conviction brought a two-year sentence and parliamentary disqualification in March 2023. Supreme Court stayed conviction on 4 August; membership returned 7 August.','Conviction stayed; merits disposition after stay not confirmed','Gandhi pursued appeals and sought a stay.','Supreme Court criticised his remarks, questioned maximum-sentence reasoning and expressly reserved merits.','2023-08-07',['S010','S011'],P3),
('CO02','National Herald / ED proceedings','ED alleges wrongdoing in the AJL/Young Indian transaction. Trial court refused cognisance on 16 December 2025; ED challenged it. September 2026 reporting records pending High Court proceedings.','Refusal of cognisance challenged; no merits acquittal or conviction established','Gandhis contest the private-complaint foundation and call ED proceedings legally unsustainable.','Bar & Bench reports adjournment on 22 September to 12 October 2026; this future date is a listing, not an outcome.','2026-09-22',['S012','S013'],P4),
('CO03','Rafale-related contempt','Meenakshi Lekhi challenged Gandhi’s false attribution of a campaign slogan to the Supreme Court. Proceedings were closed on 14 November 2019 following an unconditional apology.','Contempt proceedings closed with caution','Gandhi tendered an unconditional apology.','Separate from whether every political allegation about the procurement was substantiated.','2019-11-14',['S029','S010'],P3),
('CO04','2013 ordinance and prime-ministerial authority','Critics said his public repudiation embarrassed Manmohan Singh and demonstrated unaccountable family power within Congress. Cabinet subsequently decided to withdraw the proposals.','Political criticism; Cabinet decision','Gandhi framed the intervention as refusing compromise over corruption.','The constitutional withdrawal decision belonged to Cabinet; motivations and propriety remain matters of political assessment.','2013-10-02',['S038','S039'],P1),
('CO05','Dynasty versus organisational reform','Opponents attacked his inherited prominence; youth-organisation reforms were also criticised by Congress figures for generating factional competition.','Political and organisational criticism','IYC chief Rajiv Satav defended elections as opening opportunities and supported continuation.','Dynastic entry and attempts at organisational reform can coexist; neither proves the full outcome of the other.','2014-06-25',['S021','S022','S023'],P2),
('CO06','Electoral-roll and rigging allegations','Gandhi alleged roll manipulation in 2025 and escalated claims in September 2026. ECI rejected the allegations and described internal dissent as part of normal decision-making.','Contested allegations; no national rigging finding established here','He says his data prove malpractice; Congress disputed completeness of information provided to investigators.','EC said an Aland FIR was registered and information shared; in 2026 it said final decisions were unanimous. Neither side’s assertion is treated as adjudication.','2026-09-24',['S031','S030'],P4),
('CO07','Electoral leadership and organisation','2012 UP and 2019 national defeats generated accountability questions; losing Congress candidates blamed organisational and campaign choices after Bihar 2025.','Electoral results and attributed criticism','Publicly accepted responsibility in 2012 and 2019; reportedly accepted shared responsibility at the Bihar review.','Bihar meeting report relies on unnamed sources; campaign failure cannot be reduced to a single cause.','2025-11-28',['S034','S014','S026','S027'],P4),
]
for rid,matter,finding,procedure,response,limit,day,ids,phase in controversies:
    add('Controversies',rid,{'Matter':matter,'Finding':finding,'Procedural status':procedure,'Subject / party response':response,
        'Finding / dispute qualification':limit,'Latest evidence date':day},ids,'Attributed position' if rid in ('CO05','CO06','CO07') else 'Recorded fact',phase=phase,
        checked={'Finding':ids,'Subject / party response':ids,'Finding / dispute qualification':ids},
        note='Reported allegations are supported as attributed statements, not as findings of wrongdoing.',priority='High')

legacy=[
('LA01','Recovery of political credibility','Reuters reported a revived image in 2024; analyst Rahul Verma credited mobilisation and ideological clarity. The observation does not isolate Gandhi’s contribution from allies or local candidates.','Reuters / Rahul Verma',['S023'],P4),
('LA02','Limits of the 2024 turning point','Vaishnav and Mallory argued that the 2024 verdict curbed BJP dominance while preserving BJP centrality. This qualifies claims that Gandhi had transformed the entire party system.','Carnegie research, September 2024',['S024'],P4),
('LA03','Organisational reform as unfinished work','Internal youth elections were a documented intervention. Supporters’ access claims and critics’ factionalism claims leave their durable institutional effect unsettled.','Synthesis of contemporaneous reporting',['S021','S022'],P1),
('LA04','Policy influence without executive control','Caste-enumeration advocacy reached a government decision, but government and opposition claim credit. The evidence establishes advocacy and adoption separately, not sole authorship.','Synthesis of official decision and responses',['S035','S036'],P4),
('LA05','Persistent implementation gap in political organisation','Bihar 2025 renewed questions about converting publicity into local organisation. Losing candidates’ explanations are evidence of internal criticism, not a controlled causal study.','Asad Rehman’s candidate interviews',['S026','S027'],P4),
('LA06','Provisional legacy','His career remains open. Formal opposition leadership, electoral resilience and social-justice advocacy are established areas for assessment; national executive performance is not demonstrated by this record.','Workbook synthesis',['S002','S003','S023','S035'],P4),
]
for rid,theme,assessment,assessor,ids,phase in legacy:
    add('Legacy & Assessments',rid,{'Theme':theme,'Assessment':assessment,'Assessor':assessor},ids,'Analysis',phase=phase)

# Historical context is reviewed separately for each political phase. A research
# gap is not disguised as a supported negative finding.
era_items=['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']
gender_items=['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time']

era={
P1:[
('Entry occurred within the coalition-party system that Carnegie dates from 1989 to 2014. Access to Congress leadership did not by itself confer government office.',['S024','S004']),
('The 2013 ordinance confrontation separated party influence from Cabinet authority: Gandhi publicly objected; Cabinet decided withdrawal.',['S038','S039']),
('His 2004 and 2009 victories were direct Lok Sabha elections from Amethi. The inspected tables use constituency numbers 21 and 37 respectively; boundaries should not be presumed identical.',['S009','S008']),
('The inspected record does not establish his personal responsibility for UPA-era economic performance. A phase-specific account of his economic interventions before 2013 needs further primary research.',['S004'],'Research limitation'),
('A phase-specific foreign-policy record was not established. Overseas education is biographical evidence, not evidence of diplomatic influence or a geopolitical doctrine.',['S005'],'Evidence not found'),
('Contemporaneous reporting in 2012 scrutinised the relation between prominent campaigning and weak local organisation. Publicity and assembly-seat gains were different measures.',['S034']),
('Youth-organisation elections were intended to broaden entry beyond nominations. The later 2014 debate supplies evidence of contested institutional effects, rather than a settled reform verdict.',['S021','S022']),
('Dynastic access and a safe-seat reputation shaped his entry; the 2012 UP setback showed that national family prominence did not ensure state-level campaign success.',['S004','S034']),
('The early electoral base was Amethi in Uttar Pradesh. State campaign leadership in 2012 must be distinguished from personally standing in a parliamentary constituency.',['S009','S008','S034']),
('The party biography supplies chronology but also partisan framing. Original early election returns remain a gap; the workbook retains inspected secondary totals and leaves an unrecovered share blank.',['S004','S009','S008']),
],
P2:[
('Carnegie characterises 2014 as the start of a BJP-centred party system. Congress’s 2019 total of 52 seats formed the immediate setting of Gandhi’s presidential resignation.',['S024','S014']),
('Land-law opposition operated through legislative debate and wider mobilisation. Gandhi acted as an opposition politician; the bill’s text and coalition of opponents are distinct evidence.',['S032','S037']),
('He won Amethi in 2014, then lost it while winning Wayanad in 2019. Two simultaneous candidacies produced one loss and one victory, not a single national mandate.',['S008','S007','S041']),
('Land acquisition and the NYAY transfer proposal framed his economic opposition. NYAY remained a campaign promise after Congress’s defeat; no delivered income effect follows from the promise.',['S037','S028','S014']),
('The inspected materials do not support a systematic account of his foreign-policy positions during 2014–2019. Comparison with the prime minister’s diplomatic output would use unlike offices.',['S014'],'Research limitation'),
('His public resignation letter linked defeat to wider institutional and communication conditions. These are Gandhi’s attributed explanations; the letter does not independently establish their causal weight.',['S014']),
('The move from vice-president to president increased formal party responsibility. Internal election disputes and the 2019 resignation show the difference between authority, reform ambition and results.',['S004','S021','S022','S014']),
('Farmer and tribal-land arguments connected economic policy to rural social constituencies. Evidence of a speech or protest does not establish how each caste, class or community voted.',['S037','S028']),
('The move into Wayanad widened his personal electoral geography from Uttar Pradesh to Kerala. It should be analysed alongside the simultaneous Amethi defeat.',['S007','S041']),
('Contemporaneous internal-party reporting preserves opposing views of organisational reform. Election compilations can disagree on rounded shares; exact vote totals are kept separate from disputed percentages.',['S021','S022','S008']),
],
P3:[
('After resigning the presidency, Gandhi retained prominence while Kharge later headed Congress. Reuters’s 2024 account describes a revival within a wider opposition campaign.',['S014','S023']),
('A trial conviction interrupted membership in 2023. The Supreme Court’s stay and subsequent restoration demonstrate the distinct roles of trial court, appellate court and parliamentary notification.',['S010','S011']),
('His 2019 Wayanad mandate continued through most of this phase, interrupted by disqualification. PRS’s continuous displayed tenure needs the separate 2023 interruption recorded beside it.',['S042','S011']),
('The 2024 platform linked apprenticeships, farm-price guarantees and transfers to employment and distribution. These are proposed instruments, not measured macroeconomic outcomes.',['S018','S019','S017']),
('Congress’s 2024 security platform supplied stated positions on recruitment and foreign-policy continuity. Gandhi’s association with that platform does not amount to executive implementation.',['S020']),
('The long marches created repeated personal contact and media attention. Contemporary discussion included physical endurance and dress; a later Reuters assessment described image recovery.',['S015','S025','S023']),
('Bharat Jodo and Bharat Jodo Nyay combined movement-style journeys with party campaigning. They supplemented formal party positions; their independent effect on constituency organisation remains unmeasured.',['S004','S015','S023']),
('Unity speeches and the 2024 platform addressed exclusion, caste representation and minority rights. Source material establishes this agenda, not uniform reception among the intended groups.',['S015','S016']),
('A Kerala constituency coexisted with national journeys and campaigning. The national route and local MP role should not be conflated when evaluating constituency service.',['S042','S004']),
('The court order provides direct procedural evidence; media coverage supplies immediate political consequences. A later merits disposition cannot be inferred from the 2023 stay.',['S010','S011']),
],
P4:[
('Carnegie judged the 2024 result a constraint on BJP dominance rather than the end of BJP centrality. Formal opposition leadership therefore coexists with continuing BJP-led government.',['S024','S002']),
('Lok Sabha records the formal LoP office from 9 June 2024. PRS gives attendance as N/A because the LoP does not sign the register; treating that field as zero would be wrong.',['S002','S003']),
('He won Rae Bareli and Wayanad in 2024 and retained Rae Bareli. Congress’s poor Bihar 2025 result concerns a later state campaign, not a personal parliamentary defeat.',['S006','S043','S026']),
('The inspected current policy record is chiefly opposition advocacy and a party platform. Constituency output and national distribution effects require administrative and fiscal evidence beyond proposal documents.',['S003','S017','S018'],'Research limitation'),
('A comprehensive account of his international engagements as LoP remains incomplete. The pre-election security platform alone cannot establish his diplomatic record through September 2026.',['S020','S002'],'Research limitation'),
('Electoral-roll allegations became a press-conference and document-based campaign theme. Gandhi’s charges and ECI’s rebuttals are recorded separately; publicity does not adjudicate them.',['S031','S030']),
('The Bihar review renewed criticism of local organisation and campaign choices. Reports of losing candidates and an internal review establish disagreement, not a single proven explanation for defeat.',['S026','S027']),
('Caste enumeration and representation remained central advocacy issues. The government’s 2025 decision and rival credit claims demonstrate shared political contestation rather than exclusive authorship.',['S035','S036']),
('Rae Bareli is his retained constituency. PRS nevertheless lists a Wayanad-landslide rehabilitation intervention, illustrating national opposition activity beyond the current seat.',['S003','S043']),
('Current reporting reaches September 2026, while PRS activity stops at 13 August. Legal-news reports update procedure but do not substitute for uninspected orders or future hearings.',['S003','S012','S013']),
]}
phase_notes={
P1:('Other Congress entrants and youth-organisation leaders; Akhilesh Yadav for the 2012 state campaign comparison.',
    'Contemporaneous 2012 reporting questioned campaign effectiveness; 2014 organisational reports looked back on youth reforms.',
    'Keep the 2004–2013 governing-party setting distinct from later opposition leadership; do not project 2024 constituencies backwards.',
    'Available alternatives included strengthening local organisation and maintaining nomination-based youth appointments; their counterfactual effects are unknown.'),
P2:('Congress office-holders and other parliamentary opposition leaders in 2014–2019; distinguish the governing prime minister.',
    'Internal critics and defenders disagreed about reforms; Gandhi accepted responsibility after the 2019 result.',
    'Do not interpret a 2019 proposal as later implementation, or use 2024 image recovery as contemporary 2019 consensus.',
    'Possible organisational responses included leadership retention or resignation and coalition cooperation; the workbook evaluates documented choices only.'),
P3:('Other opposition campaigners and Congress leaders under the party presidency of Mallikarjun Kharge in 2024.',
    'Contemporaneous yatra reporting and commentary differed in emphasis; Reuters’s 2024 recovery assessment was later than the first march.',
    'Preserve the 2023 membership interruption; do not convert a conviction stay into a final legal exoneration.',
    'Yatras, parliamentary interventions and formal party organisation were available channels; no source isolates their comparative electoral effectiveness.'),
P4:('Leaders of parliamentary opposition parties in the same Lok Sabha; state campaign leaders for Bihar comparisons.',
    'The 2024 recovery narrative coexists with 2025 organisational criticism and contested 2026 electoral allegations.',
    'The career is ongoing: neither a future court listing nor a policy announcement is a completed outcome.',
    'Institutional opposition, alliances and constituency organisation remain distinct routes; relative effectiveness is not causally estimated.')}
for pi,phase in enumerate(phases,1):
    comparison,contemporary,caution,alternatives=phase_notes[phase]
    for i,(item,entry) in enumerate(zip(era_items,era[phase]),1):
        finding,ids,*rest=entry
        disposition=rest[0] if rest else 'Material finding'
        pending=disposition in ('Research limitation','Evidence not found')
        add('Context & Constraints',f'CT-P{pi}-{i:02d}',{
            'Career phase':phase,'Coverage item':item,'Finding':finding,'Coverage dimension':'Era',
            'Research disposition':disposition,'Contemporary comparison group':comparison,
            'Contemporary assessment':contemporary,'Presentism caution':caution,
            'Plausible alternatives / limits':alternatives,
            'Retrospective assessment':'Workbook synthesis bounded by the cited record; see Legacy & Assessments for named interpretations.',
            'Evidence-environment limitation':'Sources are strongest for formal events and stated positions; effects and motives require additional evidence.'},ids,'Analysis',
            status='Not reviewed' if pending else 'Supported',
            note='Research gap: related sources orient further work but do not prove absence.' if pending else 'Contextual synthesis; comparison is a scope boundary, not a ranked performance score.')

gender=[
('Dynastic access is documented, but the inspected record does not isolate a male advantage from family prominence or party succession. Treat the gender-specific mechanism as unresolved.',['S004','S005','S023'],'Research limitation','Family, class and party access are materially relevant; a male-specific causal estimate is unavailable.'),
('No gender-related political first was established in the inspected record. Ordinary male occupancy of these offices does not itself establish a representative milestone.',['S002','S004'],'Evidence not found','Absence of a documented milestone in this research is not proof that no gender-relevant milestone exists.'),
('Family succession shaped access to Congress and Amethi. Sonia Gandhi’s leadership and Rahul’s later succession are documented; claims that gender determined the succession need further evidence.',['S004','S005'],'Material finding','Dynastic network is established; gender allocation within that network is not isolated.'),
('Youth and student organisation assignments are documented. No inspected appointment record demonstrates that gender expectations determined these allocations or excluded him from a portfolio.',['S004'],'Evidence not found','Party assignment and ministerial allocation are different; the causal gender question remains open.'),
('Revati Laul read T-shirt and endurance coverage during Bharat Jodo as masculine political framing. This is a named contemporary interpretation, not a representative media-content study.',['S025'],'Material finding','Relevant comparator is other prominent male national campaigners in the same media period.'),
('Security following the assassinations of his grandmother and father affected schooling and overseas study. The inspected biography links constraints to family violence, not a demonstrated gender mechanism.',['S005'],'Material finding','Security affected mobility; a specifically gendered explanation is not established.'),
('He supported the women’s reservation bill in 2023 while seeking OBC inclusion and faster implementation. The 2024 party platform proposed transfers to women and expanded representation.',['S033','S017'],'Material finding','Separate personal parliamentary advocacy from collective party promises and later implementation.'),
('Contemporary commentary interpreted bodily endurance and dress as political masculinity. His deliberate intention to mobilise a male identity is not established by that commentary.',['S025'],'Material finding','Observed framing must not be converted into an unrecorded personal motive.'),
('Symbolic representation and substantive effects remain distinct. His legislative support and the party’s women-focused proposals are evidenced; their independent effects on women’s material position are not measured here.',['S033','S017'],'Material finding','Proposal, adoption, implementation and effect require separate evidence.'),
('The available gender assessment is primarily contemporary journalism and issue-specific policy evidence. A longitudinal scholarly comparison of gendered treatment and reception remains incomplete.',['S025','S033','S017'],'Research limitation','Do not generalise one commentator’s interpretation across his whole career.'),
]
for i,(item,entry) in enumerate(zip(gender_items,gender),1):
    finding,ids,disposition,mechanism=entry
    add('Context & Constraints',f'CT-G-{i:02d}',{
        'Career phase':'Across phases; event periods specified in finding','Coverage item':item,'Finding':finding,
        'Coverage dimension':'Gender','Research disposition':disposition,'Gender relevance':mechanism,
        'Other identity relevance':'Family/party access is evidenced; no caste, religion or gender motive is inferred from a surname.',
        'Contemporary comparison group':'Politicians in comparable Congress or national opposition roles and the same period; no aggregate causal comparison conducted.',
        'Contemporary assessment':'Named contemporary commentary or documented action, as cited; gaps remain explicit.',
        'Retrospective assessment':'Limited by the lack of a systematic longitudinal gender study in inspected sources.',
        'Presentism caution':'Do not project present media frames onto 2004, or equate male office-holding with proof of a gender mechanism.'},ids,'Analysis',
        status='Not reviewed' if disposition in ('Research limitation','Evidence not found') else 'Supported',
        note='Related sources are candidate evidence, not proof of absence.' if disposition in ('Research limitation','Evidence not found') else 'Support is for the stated bounded finding; no general gender effect is claimed.')

# Link phase context and report corroboration without treating every citation as
# independent or transferring field review status to unregistered metadata.
for name,t in tables.items():
    for row in t['rows']:
        ids=row.get('Source IDs','').split('; ') if row.get('Source IDs') else []
        kinds={S[s]['Source class'] for s in ids}
        origins={S[s]['Origin ID'] for s in ids}
        row['Corroboration']=('Unresolved' if row.get('Research disposition') in ('Evidence not found','Research limitation')
            else 'Primary record' if kinds & {'Official record','Court order'}
            else 'Interested source only' if kinds=={'Party / campaign'}
            else 'Multiple independent sources' if len(origins)>1
            else 'Single credible source' if ids else 'Method / scope')
        if name!='Context & Constraints' and row.get('Career phase') in phases:
            pi=phases.index(row['Career phase'])+1
            row['Context IDs']=f'CT-P{pi}-01; CT-P{pi}-02; CT-P{pi}-03'
        if name=='Overview' and row.get('Overview ID')=='OV12': row['Context IDs']='CT-G-05; CT-G-07; CT-G-09'

gaps=[]
def gap(n,topic,finding,next_action,records,priority='Medium'):
    gaps.append({'id':f'G{n:02d}','priority':priority,'topic':topic,'gap':finding,'next_action':next_action,'status':'Open','record_ids':records})
gap(1,'Original election returns, 2004–2014','Early votes rely on secondary tables. 2004 share is unrecovered and the 2014 page conflicts between 46.71% and 46.72%.','Retrieve ECI full state statistical reports; reconcile valid/counting/polled denominators and post-delimitation boundaries.',['EL01','EL02','EL03'],'High')
gap(2,'Defamation appeal after 2023 stay','The 2023 stay and reinstatement are established; the later merits disposition was not confirmed by an inspected order.','Search appellate cause/case records by parties and case number; inspect the latest substantive order before updating the status.',['CO01'],'High')
gap(3,'National Herald primary orders','September 2026 procedure is supported by reporting, but the original cognisance and High Court orders were not obtained.','Retrieve 16 December 2025 trial order and latest Delhi High Court order; keep 12 October 2026 as a future listing until it occurs.',['CO02'],'High')
gap(4,'Election-integrity allegations','The record establishes allegations and rebuttals, not a nationwide adjudicated finding of manipulation.','Inspect original roll data, ECI correspondence, FIR/investigation records and competent court orders; test each constituency claim separately.',['CO06','IM11'],'High')
gap(5,'Committee and party tenure precision','Historical committee memberships and exact endpoint of early party responsibilities remain imprecise.','Retrieve Lok Sabha committee rosters and AICC appointment/resignation resolutions.',['OF09','OF11','OF12'])
gap(6,'Constituency outcomes','Parliamentary requests are documented; project delivery and beneficiary effects cannot be attributed from requests alone.','Use district expenditure/project records, audits and implementation timelines; identify other responsible authorities.',['PG11'])
gap(7,'Gender comparison','Gender-specific advancement, portfolio selection and longitudinal reception are insufficiently documented.','Review contemporaneous Hindi/English media, appointment records and scholarship using comparable party/office cohorts.',['CT-G-01','CT-G-02','CT-G-04','CT-G-10'])
gap(8,'International context and engagements','Phase-specific diplomatic ideas and later international engagements are not comprehensively reconstructed.','Inspect dated speeches, parliamentary foreign-affairs work and independent scholarship for each phase.',['CT-P1-05','CT-P2-05','CT-P4-05'])
gap(9,'Policy influence and causality','The record separates proposals, advocacy and government decisions; it does not estimate personal causal effects.','Add legislative process records, government implementation evidence and credible independent evaluations before assigning outcome credit.',['PG01','PG05','LA04'])
gap(10,'Language and source diversity','Inspected source base is predominantly English and is not an exhaustive historiography.','Add relevant Hindi and Malayalam reporting and scholarly books; record translation and standpoint.',['CT-P1-10','CT-P2-10','CT-P3-10','CT-P4-10'])
gap(11,'Current parliamentary activity','PRS activity ends 13 August 2026 although the research cutoff is 24 September.','Refresh PRS and original parliamentary records after the next update; never treat missing attendance as zero.',['PG13'])

# Preserve failed routes so a later pass does not silently reclassify them as read.
failed_routes=[
('S006','https://results.eci.gov.in/PcResultGenJune2024/ConstituencywiseS2436.htm','Not found','Election-night URL no longer returned a usable result; final ECI statistical PDF inspected instead.'),
('S006','https://results.eci.gov.in/PcResultGenJune2024/ConstituencywiseS114.htm','Not found','Election-night URL unavailable; final statistical PDF used.'),
('S041','https://www.ceo.kerala.gov.in/ceokerala/pdf/GE-2019/CANDIDATE_WISE_RESULTS.pdf','Retrieval failed','Repeated timeout; CEO historical elected-member table and ADR compilation used.'),
('S043','https://eparlib.sansad.in/bitstream/123456789/2981279/1/lsd_18_1_24-06-2024_eng_editorial.pdf','Retrieval failed','Parliamentary transcript timed out; PTI reproduction of resignation bulletin inspected.'),
('S009','https://www.ceo.kerala.gov.in/ceokerala/pdf/LOKSABHA-HISTORY/2004-LS.pdf','Inspected; target absent','Kerala report did not supply the Uttar Pradesh constituency needed.'),
]
for i,(sid,url,status,result) in enumerate(failed_routes,1):
    retrievals.append({'id':f'F{i:03d}','source_id':sid,'url_or_query':url,'access_date':ASOF,
        'route':'Alternate primary route','access_status':status,'origin_id':S[sid]['Origin ID'],
        'result':result,'next_action':'Use successful cached route; revisit only if it resolves the named gap.'})

data={'schema_version':1,'subject':'Rahul Gandhi','as_of':ASOF,'tables':tables,'sources':sources,
    'claims':claims,'evidence':evidence,'coverage':{'Gender':gender_items,'Era':era_items},
    'phases':phases,'gaps':gaps,
    'guidance':'Four career phases separate governing-party access, opposition presidency, yatra recovery and formal LoP leadership. All ten gender questions and ten era dimensions per phase are reviewed. Dispositions distinguish findings from gaps. Expand grouped columns for context, dates, attribution limits and comparison cautions. Evidence status applies only to registered fields; compound fields are review units, not a count of all historical claims.'}
ROOT.mkdir(parents=True,exist_ok=True)
(ROOT/'research.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(ROOT/'retrievals.json').write_text(json.dumps(retrievals,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'substantive_rows':sum(len(t['rows']) for t in tables.values()),'sources':len(sources),
    'claims':len(claims),'evidence_links':len(evidence),'context_rows':len(tables['Context & Constraints']['rows'])}))
