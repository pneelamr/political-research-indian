"""Source register and inspected passages for Mamata Banerjee."""
ASOF = "2026-09-30"
ORIGINAL_ACCESS = "2026-09-25"
sources, retrievals = [], []

def src(n, title, author, url, published, kind, locator, passage, note='', origin=None, status='Passage inspected', accessed=ORIGINAL_ACCESS):
    sid = f'S{n:03d}'
    sources.append({'Source ID':sid, 'Title':title, 'Author / institution':author,
        'Publication date':published, 'URL':url, 'Access date':accessed, 'Source class':kind,
        'Primary / secondary':'Primary' if kind in ('Official record','Court judgment','Speech / interview') else 'Secondary',
        'Access status':status, 'Origin ID':origin or sid, 'Locator':locator,
        'Reliability / limitation':note or 'Only the identified passage supports the cited claim; official objectives are not independent outcome evaluations.',
        'Language / geography':'English / India'})
    retrievals.append({'id':f'R{n:03d}', 'source_id':sid, 'url_or_query':url, 'access_date':accessed,
        'route':'Canonical page or identified reproduction', 'access_status':status,
        'origin_id':origin or sid, 'locator':locator, 'passage_paraphrase':passage,
        'method':'web.run page text or PDF passage inspected',
        'result':'Relevant passage read' if status=='Passage inspected' else note,
        'next_action':'Reuse historical evidence; refresh current status for a later edition.'})

src(1,'Mamata Banerjee takes over as New Railway Minister','Ministry of Railways / PIB','https://www.pib.gov.in/newsite/erelcontent.aspx?lang=2&reg=48&relid=48855','2009-05-26','Official record','Profile paragraphs 1–7',
    'Assumed Railway charge 26 May 2009 after seventh Lok Sabha election. Born 5 January 1955 in Kolkata; MA, BEd, LLB. Congress women/youth organisation roles; first MP in 1984, reelected 1991, 1996, 1998, 1999, 2004, 2009. Junior HRD minister in 1991. Railways 13 October 1999–16 March 2001; later Coal and Mines. Author in Bengali and English; cultural and international conference activity.',
    'Contemporary official profile, not independent assessment. Says party founded 1997, whereas public launch is dated 1 January 1998 elsewhere. Early Mahila Congress dates differ from CMO profile; use broad period. May 26 is charge-taking, not oath.')
src(2,'Meet the CM: Mamata Banerjee (historical profile)','West Bengal Chief Minister’s Office','https://cm.wb.gov.in/ncmo/Public/CM_Profile.aspx',None,'Official record','Search-index profile body; Positions Held',
    'Historical profile lists 1991–93 junior HRD role, 8 September 2003–8 January 2004 minister without portfolio, 9 January–May 2004 Coal and Mines; CM oaths 20 May 2011, 27 May 2016 and 5 May 2021.',
    'Canonical page failed repeatedly. Cached profile is stale: still calls her CM. Candidate evidence only for chronology pending accessible corroboration; no support for current office.',status='Cached search text only')
src(3,'1984 Lok Sabha: constituency summaries','Election Commission of India; CEO Kerala mirror','https://www.ceo.kerala.gov.in/pdf/LOKSABHA-HISTORY/1984-LS.pdf','1984','Official record','PDF p.482, printed 478, Jadavpur',
    'Jadavpur poll 24 December 1984: INC Mamata Banerjee 331618; CPM Somnath Chatterjee 311958; margin 19660; valid votes 651905; electorate 871732.',
    'Official historical return; vote-share denominator is valid votes, excluding rejected ballots.')
src(4,'1989 Lok Sabha: constituency summaries','Election Commission of India; CEO Kerala mirror','https://www.ceo.kerala.gov.in/pdf/LOKSABHA-HISTORY/1989-LS.pdf','1989','Official record','PDF p.498, Jadavpur summary',
    'Jadavpur poll 24 November 1989: CPM Malini Bhattacharya 441188; INC Mamata Banerjee 410288; winning margin 30900; valid votes 879040.',
    'Personal defeat; distinct from Calcutta South, which she contested later.')
src(5,'Kolkata Dakshin historical election table','Elections.in','https://www.elections.in/west-bengal/parliamentary-constituencies/kolkata-dakshin.html','2019-06-28','Dataset','Historical table, 1991/1996/1999 rows',
    'Calcutta South: 1991 INC Banerjee 367896, CPM Biplab Das Gupta 274233; 1996 INC Banerjee 438252, CPM Bharati Mukherjee 334991; 1999 AITC Banerjee 469103, CPM Subhankar Chakraborty 255095.',
    'Secondary fallback. These rows agree with accessible indexed ECI tables. Page mislabels 2009/2011 candidates and has stale prose; those rows are excluded. Original 1991/1996/1999 PDFs remain retrieval gaps.')
src(6,'1998 Lok Sabha: constituency summaries','Election Commission of India; CEO Kerala mirror','https://www.ceo.kerala.gov.in/pdf/LOKSABHA-HISTORY/1998-LS.pdf','1998','Official record','PDF p.518, Calcutta South',
    'Calcutta South: WBTC Mamata Banerjee 503551; CPM Prasanta Sur 279470; margin 224081. ECI uses WBTC, not the later AITC abbreviation.',
    'Preserve historical party label; different delimitations make later constituency shares imperfectly comparable.')
src(7,'West Bengal Lok Sabha results 2004','Rediff','https://m.rediff.com/election/ls04wb.htm','2004','Dataset','Calcutta South row',
    'AITC Mamata Banerjee 393561; CPM Rabin Deb 295132; margin 98429.',
    'Contemporaneous result reproduction; primary detailed return not retrieved. Vote share omitted because inspected passage lacks a denominator.')
src(8,'General Elections 2009 statistical report','Election Commission of India; CEO Kerala mirror','https://www.ceo.kerala.gov.in/pdf/LOKSABHA-HISTORY/2009-LS.pdf','2009','Official record','PDF p.283, Kolkata Dakshin detailed result; p.95 women candidates',
    'Kolkata Dakshin: AITC Banerjee 576045 (575490 general plus 555 postal), 57.19%; CPM Rabin Deb 356474; total votes polled 1007225; constituency electorate 1505638.',
    'Share is of votes polled, not all electors. Use Kolkata Dakshin as the contemporary name.')
src(9,'Bhabanipur bypoll: Banerjee wins by 58835','Express Web Desk / Indian Express','https://indianexpress.com/article/cities/kolkata/mamata-banerjee-bhabanipur-bypoll-win-bengal-cm-7549594/','2021-10-04','Journalism','Opening results and post-result remarks',
    'September 30 bypoll, result October 3: Banerjee 85263; BJP Priyanka Tibrewal 26428; margin 58835; share71.9%. TMC total215 after delayed Jangipur and Samserganj elections. Banerjee alleged conspiracy in Nandigram and referred to her court petition.',
    'Candidate counts agree with other reports. Article contains inconsistent lower-ranked candidate and opponent-share details; those are excluded.')
src(10,'Bhabanipur 2026 candidate results','Election Commission of India','https://results.eci.gov.in/ResultAcGenMay2026/ConstituencywiseS25159.htm','2026-05-05','Official record','Candidate table, rounds20/20',
    'BJP Adhikari Suvendu 73917 (53.02%); AITC Mamata Banerjee 58812 (42.19%); total139413 including NOTA829. All20rounds complete.',
    'ECI website disclaimer: returning-officer data; final Form20 is authoritative. Derived signed margin for Banerjee is -15105, superseding inconsistent press figures.')
src(11,'Suvendu Adhikari takes oath as first BJP CM','Akashvani / News On AIR','https://newsonair.gov.in/suvendu-adhikari-takes-oath-as-first-bjp-cm-of-west-bengal/','2026-05-09','Official record','Opening and election context',
    'Governor RN Ravi administered CM oath to Suvendu Adhikari on9May2026. BJP207 seats and TMC80 reported, ending fifteen years of TMC government.',
    'Public broadcaster event report, not appointment gazette. 207/80 is the initial293-seat result; delayed Falta poll must be treated separately.')
src(12,'Supreme Court seeks update on TMC party-name dispute','Express News Service / Indian Express','https://indianexpress.com/article/legal-news/supreme-court-election-commission-mamata-banerjee-tmc-symbol-freeze-ritabrata-banerjee-10892752/lite/','2026-09-25','Journalism','September24 hearing, opening and final paragraphs',
    'SC asked ECI for a reasonable timeline to decide competing TMC name/symbol claims. Banerjee’s counsel challenged timing; rival counsel defended interim orders. Next hearing September29. Interim bypoll arrangement not disturbed in reported hearing.',
    'Hearing report, not signed order. Refers to September18 freeze; other reports date freeze17 and allotment18. Record17–18September until primary orders obtained.')
src(13,'Mamata challenges EC freeze; factions receive new names','New Indian Express with ANI inputs','https://www.newindianexpress.com/states/west-bengal/2026/Sep/18/mamata-banerjee-moves-supreme-court-against-ec-freeze-on-tmc-name-flowers-and-grass-symbol','2026-09-18','Journalism','Body paragraphs1–10',
    'Reports provisional Mamata All India Trinamool Congress name and Football Player symbol; rival Democratic Trinamool Congress and Envelope. Original name/symbol frozen for bypolls; substantive ECI determination pending. Banerjee vowed legal resistance and supported Congress in Nandigram after nominee withdrew.',
    'Attributed report; signed ECI orders not retrieved. Identifies rival authorised leader Arup Roy, while other reports call it Ritabrata faction. Do not equate interim freeze with party dissolution.')
src(14,'The Political Asceticism of Mamata Banerjee','Proma Ray Chaudhury / Politics & Gender, Cambridge University Press','https://www.cambridge.org/core/journals/politics-and-gender/article/political-asceticism-of-mamata-banerjee-female-populist-leadership-in-contemporary-india/618F669661A8387B2B8DFE39C43EF0F1','2021-09-15','Academic','Research Method; Brief Overview; gendered self-making and contestations sections',
    'Interpretive study uses autobiographical/party texts, press and snowball interviews in Kolkata region,2018–20. Analyses Didi kinship persona, austerity claims, regional rhetoric, religious iconography and gendered criticism; describes personalised party organisation.',
    'Author’s interpretation, not representative voter survey or causal election estimate. Fieldwork predates2021–26; contemporary party descriptions are historical. Personal imagery discussed only for political relevance.')
src(15,'Singur, Nandigram and Lalgarh remade Mamata Banerjee','Monobina Gupta, Didi: A Political Biography; excerpt at Indian History Collective','https://indianhistorycollective.com/singur-nandigram-lalgarh-remade-mamata-banerjee/','2021','Book excerpt','Editor’s framing and excerpt on2006–09 movements',
    'Gupta interprets land struggles as broadening Banerjee’s coalition beyond earlier admirers to peasants, intellectuals and former Left supporters; connects class reception, public protest and political opportunity.',
    'Retrospective biography excerpt with2021 editorial introduction; neither neutral proof of every participant’s motive nor complete history of the movements.')
src(16,'Kedar Nath Yadav v State of West Bengal','Supreme Court; Legal Authority reproduction','https://www.legalauthority.in/judgement/kedar-nath-yadav-vs-state-of-west-bengal-2174','2016-08-31','Court judgment','C.A.8438/2016; operative directions and separate opinions',
    'Judgment on Singur land acquisition under the former Left government; separate judicial opinions reach cancellation of acquisition and restoration of land.',
    'Judgment text reproduced by legal publisher after judicial academy PDF retrieval failed. Distinguish2006 acquisition decision from Banerjee’s later return-of-land policy; no causal conclusion about industrial growth.')
src(17,'Kanyashree Prakalpa in West Bengal: Justification and evaluation','Arijita Dutta and Anindita Sen / International Growth Centre','https://www.theigc.org/sites/default/files/2021/03/Dutta-September-2020-Final-Report.pdf','2020-09','Academic','PDFpp.75–79 conclusion; pp.10–18 programme background',
    'Study surveys1021households in three selected districts and applies matching plus difference-in-differences using baseline/cohort comparisons. Authors find reductions in underage marriage/dropout, more progressive aspirations, uneven coverage, and continuing education-cost/social-norm barriers.',
    'Cover dated2020; acknowledgements2017 and earlier field data. Nonrandomised study with selected districts; estimates depend on design assumptions and do not establish all-state2026 outcomes.')
src(18,'West Bengal Budget Analysis2025–26','PRS Legislative Research','https://prsindia.org/files/budget/budget_state/west-bengal/2025/West_Bengal_Budget_Analysis_2025-26.pdf','2025-02-18','Dataset','pp.1–2 budget highlights and Lakshmir Bhandar box',
    '2025–26BE net expenditure341462crore; fiscal deficit3.6%GSDP; revenue deficit1.7%. Lakshmir Bhandar provision over26000crore, around10%revenue receipts; transfers to eligible women25–60.',
    'Budget estimates, not actual spending. Finance minister Chandrima Bhattacharya presented the budget; collective government attribution.')
src(19,'West Bengal Budget Analysis2026–27','PRS Legislative Research','https://prsindia.org/budgets/states/west-bengal-budget-analysis-2026-27','2026-06','Dataset','Table1 actuals/revised estimates; welfare and committed-expenditure boxes',
    'Successor government budget presented22June2026.2024–25actual fiscal deficit3.4%GSDP;2025–26revised3.4%,revenue deficit2.1%,liabilities38.3%. Reports Annapurna replacing Lakshmir Bhandar in2026–27.',
    'Successor government’s projections must not be attributed to Banerjee. Updated estimates can differ from earlier budgets; no personal causal inference.')
src(20,'School recruitment review petitions dismissed','Supreme Court of India','https://api.sci.gov.in/supremecourt/2025/23194/23194_2025_13_1001_63010_Order_05-Aug-2025.pdf','2025-08-05','Court judgment','PDFpp.1–13; paras5–7',
    'Review of3April2025decision dismissed. Court says entire selection was compromised, missing OMR records and cover-up frustrated separating valid selections; interests of untainted appointees had been considered.',
    'Judicial finding about recruitment process and authorities. It does not convict Banerjee personally; later hiring implementation requires separate evidence.')
src(21,'State of West Bengal: supernumerary-post investigation order','Supreme Court of India','https://api.sci.gov.in/supremecourt/2024/18822/18822_2024_1_44_60760_Order_08-Apr-2025.pdf','2025-04-08','Court judgment','PDFpp.1–3, operative paragraphs',
    'Set aside HC direction for CBI investigation into2022Cabinet decision creating supernumerary posts; limited relief expressly leaves other CBI investigations and chargesheets unaffected.',
    'Separate procedural relief; not reversal of recruitment cancellation or blanket exoneration of all actors.')

src(22,'Mamata Banerjee v Suvendu Adhikari','Calcutta High Court / Indian Kanoon reproduction','https://indiankanoon.org/doc/23754007/','2026-06-23','Court judgment','Order admitting election petition and preservation directions',
    'Election petition admitted; directions protect May 4 counting CCTV and relevant EVM/VVPAT material. Admission is not a merits determination that the Bhabanipur result was invalid.',
    'Last inspected order in this proceeding; no later merits disposal established.')
src(23,'In re RG Kar Medical College incident, 2024 INSC 613','Supreme Court of India','https://api.sci.gov.in/supremecourt/2024/37351/37351_2024_1_66_54902_Judgement_20-Aug-2024.pdf','2024-08-20','Court judgment','Paras 1–9 and National Task Force directions',
    'Records August 13 transfer to CBI; criticises state preparedness for August 15 hospital vandalism. Identifies systemic workplace safety failures and gendered risks; creates a national task force.',
    'Institutional safety proceeding, not personal criminal adjudication of the Chief Minister.')
src(24,'RG Kar: Sanjoy Roy sentenced to imprisonment for life','Tanusree Bose / Indian Express','https://indianexpress.com/article/cities/kolkata/rg-kar-rape-murder-sanjoy-roy-life-sentence-9788884/','2025-01-21','Journalism','Sentencing account and Banerjee response',
    'Sealdah court sentenced Roy on January 20 to imprisonment for the remainder of his life. Banerjee expressed dissatisfaction and demanded capital punishment.',
    'Use for dated sentence and response. Article incorrectly places CBI takeover in September; the Supreme Court records August 13. Later appeals not resolved by this report.')
src(25,'Supreme Court dismisses Bengal petition on Sandeshkhali CBI probe','Ananthakrishnan G / Indian Express','https://indianexpress.com/article/india/supreme-court-dismisses-bengal-govt-petition-cbi-to-continue-sandeshkhali-probe-9440059/','2024-07-08','Journalism','Court hearing and state counsel submissions',
    'SC rejected challenge to CBI investigation of Sandeshkhali allegations. State counsel argued transfer was excessively broad and infringed autonomy; bench criticised delay and upheld court-directed investigation.',
    'A probe order does not prove each allegation or personal guilt. No final trial outcome is inferred.')
src(26,'Subrata Chattoraj v Union of India','Supreme Court / Indian Kanoon reproduction','https://indiankanoon.org/doc/7781654/','2014-05-09','Court judgment','Paras 30–40',
    'Transferred Saradha and specified related investigations to CBI for interstate scope, money trail and public confidence. Recognised state police work, preserved recovery action, and expressly withheld a final view on complicity.',
    'Transfer decision, not conviction of Banerjee or every politician mentioned in subsequent reporting.')
src(27,'CBI v State of West Bengal, WPA 10504/2021','Calcutta High Court / LiveLaw PDF','https://www.livelaw.in/pdf_upload/calcutta-hc-narada-mamata-banerjee-393599.pdf','2021-05-17','Court judgment','Eight-page interim order',
    'Records CBI submissions concerning pressure surrounding Narada arrests and Banerjee’s presence at its office; stayed special-court bail pending further consideration.',
    'Interim order; allegations and provisional judicial concerns are not a final finding against Banerjee. Later bail is registered separately.')
src(28,'Duare Sarkar and Paray Samadhan outreach','National Informatics Centre, West Bengal','https://wb.nic.in/news/duare-sarkar-govt-at-doorstep-and-paray-samadhan-solution-at-mohalla-two-massive-outreach-program-of-government-of-west-bengal-developed-by-nic-west-bengal/',None,'Official record','Programme description and first-round implementation',
    'Duare Sarkar began December 1, 2020, using local camps and NIC management systems to enrol residents and deliver services; Paray Samadhan addressed local infrastructure and service gaps.',
    'Administrative description; registration/service totals are not necessarily unique beneficiaries or independently measured effects.')
src(29,'Gorkhaland Territorial Administration agreement','Ministry of Home Affairs / PIB','https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=3&relid=78023','2011','Official record','GTA agreement paragraph',
    'Tripartite agreement among Government of India, West Bengal government and Gorkha Janmukti Morcha signed July 18, 2011 for a Gorkhaland Territorial Administration.',
    'Agreement creates an autonomy framework; not a grant of separate statehood or proof of permanent settlement.')
src(30,'Mamata turns her back on UPA','Rajib Chatterjee / Indian Express','https://indianexpress.com/article/news-archive/print/mamata-turns-her-back-on-upa/','2012-09-19','Journalism','Withdrawal announcement and economic objections',
    'Banerjee announced withdrawal of TMC support on September 18 over retail FDI, diesel prices and LPG restrictions; ministers were to resign on Friday.',
    'Distinguish announcement date from later effective resignations.')
src(31,'India–Bangladesh boundary accord; Teesta treaty on hold','NDTV Correspondent with PTI inputs','https://www.ndtv.com/india-news/india-bangladesh-sign-historic-boundary-agreement-teesta-treaty-on-hold-466837','2011-09-06','Journalism','Dhaka summit report, opening paragraphs',
    'Teesta pact was put on hold after Banerjee withdrew from the delegation amid reported objections to the draft sharing arrangement. Prime Minister Singh pledged a mutually acceptable arrangement.',
    'Dated account of the 2011 episode, not a statement of the treaty’s present status or a quantified hydrological assessment.')
src(32,'Mamata sworn in as West Bengal’s first woman CM','Indian Express','https://indianexpress.com/article/news-archive/web/mamata-banerjee-sworn-in-as-west-bengals-first-woman-cm/','2011-05-20','Journalism','Oath and political transition',
    'Banerjee sworn in May 20, 2011 as West Bengal’s first woman CM after the election ended 34 years of Left Front government.')
src(33,'Mamata sworn in for second term','Times of India','https://timesofindia.indiatimes.com/india/mamata-banerjee-sworn-in-as-west-bengal-chief-minister-for-second-time/articleshow/52464823.cms','2016-05-27','Journalism','Oath report',
    'Governor Keshri Nath Tripathi administered oath to Banerjee on May 27, 2016 for her second government.')
src(34,'Mamata takes oath as Bengal CM','Indian Express','https://indianexpress.com/article/india/mamata-banerjee-takes-oath-as-west-bengal-cm-7302681/','2021-05-05','Journalism','Third oath and first statements',
    'Third oath May 5, 2021; she identified COVID-19 as first priority and appealed for peace following election violence.')
src(35,'Nandigram assembly result 2021','NDTV election results','https://www.ndtv.com/elections/west-bengal-assembly-election-results-2021/nandigram','2021-05-02','Dataset','Candidate result table',
    'BJP Suvendu Adhikari 110764; AITC Mamata Banerjee 108808; margin 1956.',
    'Secondary result table; vote-share denominator differs among publishers. Shares excluded pending authoritative Form 20.')
src(36,'West Bengal assembly results 2016','Elections.in','https://www.elections.in/west-bengal/assembly-constituencies/2016-election-results.html','2016','Dataset','Bhabanipur row',
    'Mamata Banerjee 65520; INC Deepa Dasmunshi 40219; winning margin 25301.',
    'Secondary fallback. Original Form 20 located but could not be read; unrelated classification errors on the page are excluded.')
src(37,'Mamata wins assembly bypoll','PTI / OneIndia','https://www.oneindia.com/2011/09/28/mamata-banerjee-wins-assembly-by-poll.html','2011-09-28','Journalism','PTI results paragraphs',
    'Bhowanipore bypoll held September 25: Banerjee 73635, CPM Nandini Mukherjee 19422, margin 54213; result September 28.',origin='PTI-2011-Bhabanipur')
src(38,'Nandigram election petition remains pending','Tanusree Bose / Indian Express','https://indianexpress.com/article/cities/kolkata/last-hearing-in-december-2021-mamatas-election-petition-against-suvendu-adhikari-over-nandigram-defeat-remains-pending-10588568/','2026-03-18','Journalism','Case-status account',
    'Reports Banerjee’s challenge to the 2021 Nandigram result still pending, with last hearing in December 2021.',
    'Status is dated March 18, not guaranteed through cutoff. Article’s opponent-vote figure is inconsistent with result records and is excluded.')
src(39,'Swasthya Sathi report, January 2021','Government of West Bengal','https://swasthyasathi.gov.in/Content/HomeTabItems/SS_REPORT_JAN_20212021-04-3--14-04-30.pdf','2021-01','Official record','Introduction, PDF pp.3–5',
    'Scheme launched December 30, 2016 and rolled out February 2017; cashless secondary/tertiary care cover up to Rs5 lakh per family per year. December 2020 expansion subject to exclusions for other government coverage.',
    'Dated programme design and administrative report; no independent evidence here of reduced out-of-pocket expenditure.')
src(40,'MGNREGA funds for West Bengal','Ministry of Rural Development / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=2100661&lang=2&reg=3','2025-02-07','Official record','Rajya Sabha reply',
    'Ministry said funds to West Bengal had been stopped since March 9, 2022 under section 27 for noncompliance with central directions.',
    'Union government’s stated reason. It does not establish every contested irregularity or workers’ receipt of arrears.')
src(41,'High Court orders CBI inquiry into post-poll murder and rape cases','Indian Express','https://indianexpress.com/article/cities/kolkata/west-bengal-post-poll-violence-calcutta-hc-orders-cbi-probe-into-murder-rape-cases-7461064/','2021-08-19','Journalism','Investigation directions',
    'HC ordered CBI investigation of grave post-poll violence cases and an SIT for other matters, following scrutiny of police response.',
    'Investigation orders must be distinguished from final findings in individual cases.')
src(42,'West Bengal Budget Analysis 2021–22','PRS Legislative Research','https://prsindia.org/budgets/states/west-bengal-budget-analysis-2021-22','2021-07','Dataset','Policy highlights',
    'Budget announced basic income support for women: Rs500 per month for general-category and Rs1000 for SC/ST beneficiaries; increased Krishak Bandhu assistance.',
    'Announcement and budget design, not proof of universal disbursement.')
src(43,'West Bengal Budget Analysis 2024–25','PRS Legislative Research','https://prsindia.org/budgets/states/west-bengal-budget-analysis-2024-25','2024-02','Dataset','Policy highlights and capital-outlay analysis',
    'Lakshmir Bhandar monthly rates increased to Rs1000 general and Rs1200 SC/ST; Karmasree proposed 50 days of work from May 2024. Capital-outlay underspending averaged 33% in 2015–16 to 2021–22 versus 19% across states.',
    'Historical budget vintage. Underspending compares actuals with estimates; cannot by itself establish why projects failed or measure all investment.')
src(44,'Commission reports on 1993 police firing','PTI / Business Standard','https://www.business-standard.com/article/pti-stories/1993-police-firing-worse-than-jallianwala-bagh-commission-114122900698_1.html','2014-12-29','Journalism','Commission findings and establishment',
    'Thirteen died in July 21, 1993 police firing during a Youth Congress demonstration. Commission appointed by Banerjee government in 2011 described firing as unnecessary in its 2014 report.',
    'Attributed findings of a later government-appointed commission; full report and all responses not retrieved. Avoid adopting the headline’s historical analogy.',origin='PTI-1993Commission-2014')
src(45,'Trinamool foundation day: messages from Mamata and Abhishek','Ei Samay','https://eisamay.com/west-bengal-news/kolkata-news/tmc-foundation-day-mamata-banerjee-abhishek-banerjees-social-post/200333582.cms','2025-01-01','Journalism','Bengali foundation-day report',
    'Dates TMC foundation to January 1, 1998 and reports Mamata’s service-oriented message and Abhishek’s organisational appeal as general secretary.',
    'Bengali source; English paraphrase by researcher. Party messages are self-presentations.')
sources[-1]['Language / geography']='Bengali / West Bengal'
src(46,'For fighter Didi, the battle of a lifetime','Atri Mitra, Asad Rehman, Ravik Bhattacharya, Rinku Ghosh and Aishwarya Khosla / Indian Express','https://indianexpress.com/article/long-reads/for-fighter-didi-the-battle-of-a-lifetime-10661248/lite/','2026-04-30','Journalism','Career retrospective; passages quoting Monobina Gupta',
    'Describes Hazra assault in 1990, Congress break in 1997, party launch in 1998, and the Singur hunger strike. Reports nephew Abhishek’s rise. Biographer Gupta criticises continuity of cadre practices after the 2011 change.',
    'Pre-election analysis, first published April 29 and updated April 30; named assessments are attributed. Anonymous motive claims and unproven corruption assertions excluded.')
src(47,'Park Street: guilty will be punished, says CM','Times of India','https://timesofindia.indiatimes.com/city/kolkata/park-street-guilty-will-be-punished-cm/articleshow/12063569.cms','2012-02-28','Journalism','CM clarification and earlier remark',
    'Reports criticism of her initial claim that the Park Street rape allegation was fabricated. She said her remarks were misinterpreted and wanted the guilty punished.',
    'Reports her response, not validation of her characterisation or medical assertions; survivor identity omitted.')
src(48,'Eastern freight corridor work begins at Dankuni','Ministry of Railways / PIB','https://www.pib.gov.in/newsite/PrintRelease.aspx?relid=67218','2010-11-16','Official record','Opening and sanctioned amount',
    'Banerjee commenced Dankuni corridor work; initial 25.41-km Dankuni–Chandanpur line and Rs190.46 crore sanctioned in supplementary railway grant.',
    'Commencement and sanction, not completion or independently measured industrial benefits.')
src(49,'Sabooj Sathi scheme','Howrah district, Government of West Bengal','https://howrah.gov.in/scheme/saboojsathi/','2015-09-01','Official record','Scheme description',
    'Bicycle provision for classes IX–XII in government, aided and sponsored schools; retention and higher education are stated objectives. District credits CM with name and logo.',
    'Historical target and design; no impact evaluation or current delivery total established.')
src(50,'Khadya Sathi programme note','West Bengal Food and Supplies; WBXPress mirror','https://wbxpress.com/files/2023/12/KHADYA-SATHI.pdf',None,'Official record','Indexed programme PDF; canonical file now requires account',
    'Indexed note dates RKSY expansion to January 27, 2016 and describes subsidised grain beyond NFSA coverage.',
    'Access redirected to account gate. Candidate evidence only; do not treat as an inspected PDF.',status='Cached search text only')
src(51,'TMC makes gains in Bengal in 2024','Indian Express','https://indianexpress.com/article/political-pulse/tmc-holding-fort-gain-bengal-bjp-distant-second-9371492/','2024-06-05','Journalism','Final result and alliance paragraphs',
    'TMC won 29 of West Bengal’s 42 Lok Sabha seats, up from 22 in 2019; BJP won 12. TMC contested alone in Bengal while part of INDIA nationally.',
    'Party result, not a personal Lok Sabha contest by Banerjee.')
src(52,'Falta repoll result 2026','Election Commission of India','https://results.eci.gov.in/ResultAcGenMay2026/candidateswise-S25144.htm','2026-05-24','Official record','All 22 rounds complete',
    'Falta BJP candidate Debangshu Panda won with 149666 votes; AITC candidate Jahangir Khan received 7783. Delayed result adds a BJP seat to the initial 207-seat tally.',
    'Derived combined election total is BJP208, TMC80; this is not a continuously updated count after resignations or bypolls.')
src(53,'High Court grants interim bail to four Narada accused','Subrata Chattoraj / Times of India','https://timesofindia.indiatimes.com/india/calcutta-high-court-grants-bail-to-4-tmc-politicians-held-in-narada-case/articleshow/83053256.cms','2021-05-29','Journalism','Five-judge bench bail decision',
    'Four arrested politicians received interim bail on May 28; reporting describes bonds and directions against public case comments, evidence tampering and witness intimidation.',
    'Bail does not dispose of the criminal case. Later merits decisions remain outside inspected record.')

src(54,'Break-up and after','Subrata Nagchoudhury / Indian Express','https://indianexpress.com/article/news-archive/latest-news/breakup-and-after/','2012-09-23','Journalism','In & Out chronology; coalition-breakup analysis',
    'Records junior HRD and youth/sports service ending in 1993; Railway ministry in BJP-led NDA from 1999, withdrawal in 2001 after Tehelka and a Congress alliance for the state election; Coal and Mines in 2004; entry into UPA-II in 2009 and exit in September 2012.',
    'Contemporary assessment of the 2012 breakup with a retrospective chronology. Its condensed return-to-NDA account omits the 2003 no-portfolio period; do not use it to date that appointment. Motive claims and rhetorical judgments are not adopted as fact.')

src(55,'Supreme Court gives Election Commission 3 months to resolve TMC name, party symbol issue','Ashish Shaji / Indian Express','https://indianexpress.com/article/legal-news/trinamool-symbol-in-4-months-supreme-court-tells-poll-panel-10897392/lite/','2026-09-29','Journalism','September 28 hearing; reported direction on pleadings and decision',
    'Reports September 28 hearing: parties have four weeks to complete documents and pleadings; ECI then has three months to decide the name and symbol dispute. ECI had requested six months.',
    'Updated September 29 report. Headline and URL use different shorthand: the body specifies four weeks followed by three months. Signed order not obtained; do not convert this to a fixed calendar deadline or final entitlement ruling.',accessed=ASOF)
src(56,'ECI gets 3 months to decide TMC name and symbol dispute','Raghav Ohri / Economic Times','https://economictimes.indiatimes.com/news/politics-and-nation/eci-gets-3-months-to-decide-tmc-name-and-symbol-dispute/articleshow/134549899.cms','2026-09-29','Journalism','Hearing report and by-election paragraphs',
    'Reports four weeks for pleadings and three months thereafter for ECI adjudication. Says the court declined to disturb by-elections after nominations and provisional symbols; Nandigram and Rejinagar polls scheduled October 6.',
    'Separate bylined report, not a signed order. Future polling schedule is not an election outcome; definitive party entitlement remains for ECI.',accessed=ASOF)

# Failed retrievals stay visible; none provides support for a factual claim.
for n,(sid,url,result) in enumerate([
    ('S005','https://www.ceo.kerala.gov.in/pdf/LOKSABHA-HISTORY/1991-LS.pdf','Canonical PDF unavailable; indexed constituency row located.'),
    ('S005','https://www.ceo.kerala.gov.in/pdf/LOKSABHA-HISTORY/1996-LS.pdf','Canonical PDF unavailable; secondary fallback retained.'),
    ('S005','https://ceomadhyapradesh.nic.in/Links/Books/99_Vol_I.pdf','Historical PDF route failed; no inspected primary 1999 return.'),
    ('S036','https://ceowestbengal.wb.gov.in/Downloads/Election/GE2016/Form20/159_Form20.pdf','Eleven-page PDF located; extraction and screenshot failed.'),
    ('S035','https://ceowestbengal.wb.gov.in/Downloads/Election/GE2021/Form20/210_Form20.pdf','Form20 route timed out; primary vote-share denominator unresolved.'),
    ('S031','https://bdnews24.com/bangladesh/no-teesta-treaty-no-transit','Cached report located; canonical open failed; NDTV passage used.'),
    ('S053','https://indianexpress.com/article/cities/kolkata/tmc-leaders-get-bail-calcutta-high-court-asks-cbi-why-arrests-now-7334899/lite/','Canonical open failed; Times of India passage used.'),
],101):
    retrievals.append({'id':f'R{n:03d}','source_id':sid,'url_or_query':url,'access_date':ORIGINAL_ACCESS,
        'route':'Alternate original or corroborating route','access_status':'Retrieval failed','origin_id':sid,
        'locator':'No inspected passage','passage_paraphrase':'','method':'web.run open / screenshot',
        'result':result,'next_action':'Retry archive, official repository or signed returning-officer document.'})

# Improve spacing in human-readable source prose without altering URLs or IDs.
import re
for entry in sources + retrievals:
    for key in ('Title','Locator','Reliability / limitation','locator','passage_paraphrase'):
        value=entry.get(key)
        if isinstance(value,str):
            value=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])', ' ', value)
            value=value.replace('PDFpp.', 'PDF pp.').replace('PDFp.', 'PDF p.')
            entry[key]=value
