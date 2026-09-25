"""Inspected source passages for the Nirmala Sitharaman research snapshot."""
ASOF = '2026-09-24'
sources, retrievals = [], []

def src(n, title, author, url, published, kind, locator, passage, note='', origin=None, status='Passage inspected'):
    sid = f'S{n:03d}'
    sources.append({'Source ID':sid, 'Title':title, 'Author / institution':author,
        'Publication date':published, 'URL':url, 'Access date':ASOF, 'Source class':kind,
        'Primary / secondary':'Primary' if kind in ('Official record','Court judgment','Speech / interview') else 'Secondary',
        'Access status':status, 'Origin ID':origin or sid, 'Locator':locator,
        'Reliability / limitation':note or 'Only the identified passage supports the cited claim; official objectives are not independent outcome evaluations.',
        'Language / geography':'English / India'})
    retrievals.append({'id':f'R{n:03d}', 'source_id':sid, 'url_or_query':url, 'access_date':ASOF,
        'route':'Canonical page or identified reproduction', 'access_status':status,
        'origin_id':origin or sid, 'locator':locator, 'passage_paraphrase':passage,
        'method':'web.run page text or PDF passage inspected',
        'result':'Relevant passage read' if status=='Passage inspected' else note,
        'next_action':'Reuse historical evidence; refresh current status for a later edition.'})

src(1,'Rajya Sabha Who’s Who 2020','Rajya Sabha Secretariat','https://cms.rajyasabha.nic.in/UploadedFiles/ElectronicPublications/larrdis/WhosWho_2020.pdf','2021-02','Official record','Printed pp.320–322; PDF pp.353–355',
    'Born 18 August 1959, Madurai. Qualifications MA Economics, MPhil. NCW 2003–05; Finance/Corporate Affairs MoS 26 May–9 November 2014; Commerce independent charge 26 May 2014–3 September 2017; Defence 3 September 2017–30 May 2019; Finance/Corporate Affairs from 30 May 2019. First RS tenure ended by resignation 17 June 2016; second began July 2016. National executive since 2008; spokesperson 2010–14.',
    'Member-supplied parliamentary biography; historical cutoff December 2020. Office dates are parliamentary chronology, not necessarily charge-taking dates. Private contact details excluded.')
src(2,'Sitharaman to assume charge as Defence Minister','Ministry of Defence / PIB','https://www.pib.gov.in/newsite/PrintRelease.aspx?relid=170580&reg=48&lang=2','2017-09-06','Official record','Profile, lines 14–26',
    'Scheduled to take charge 7 September 2017 from Arun Jaitley; first full-time woman defence minister. Economics graduate of Seethalakshmi Ramaswamy College, MA at JNU, draft doctoral thesis. London research work; Hyderabad policy institute; NCW 2003–05. Says BJP joining 2008; spokesperson March 2010.',
    'BJP joining year conflicts with her 2010 interview (S007). A draft thesis does not establish a completed doctorate.')
src(3,'Sitharaman assumes charge of Finance and Corporate Affairs','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2024501&reg=48&lang=2','2024-06-12','Official record','Opening and minister’s remarks, lines 22–38',
    'Took charge again on 12 June 2024; thanked Modi and pledged continuation of reforms and development agenda.',
    'Charge-taking record, separate from 9 June oath and 10 June portfolio allocation; praise of government is attributed.')
src(4,'Smt. Nirmala Sitharaman','Department of Financial Services','https://financialservices.gov.in/smt-nirmala-sitharaman','2025-12-25','Official record','Minister listing; footer updated 29 January 2026',
    'Department lists Nirmala Sitharaman as Hon’ble Finance Minister.', 'Live office listing checked on access date; page is not a detailed career history.')
src(5,'Nirmala Sitharaman: Rajya Sabha MPTrack','PRS Legislative Research','https://prsindia.org/mptrack/rajya-sabha/nirmalasitharaman',None,'Dataset','Profile and minister-method note, lines 69–114',
    'Elected BJP member for Karnataka, third term, start 1 July 2022, in office. Minister activity is not reported: ministers do not sign attendance or ask questions or introduce private members’ bills; data through 13 August 2026.',
    'Education classified as Doctorate, contrary to the qualifications listed in S001; classification not adopted. Missing minister activity is not inactivity.')
src(6,'Nirmala Sitharaman elected to RS from AP','New Indian Express, report citing official release','https://www.newindianexpress.com/states/andhra-pradesh/2014/Jun/26/nirmala-sitharaman-elected-to-rs-from-ap-629151.html','2014-06-26','Journalism','Opening paragraphs, lines 46–53',
    'Declared elected unopposed on 26 June 2014, the withdrawal deadline; Andhra Pradesh vacancy after N Janardhan Reddy’s death; TDP backed her.',
    'Official notification not independently downloaded. Earlier 24 June reports prematurely describe the election as complete.')
src(7,'BJP gets a JNU product as its woman spokesperson','Mohua Chatterjee / Times of India','https://timesofindia.indiatimes.com/india/bjp-gets-a-jnu-product-as-its-woman-spokesparson/articleshow/5706871.cms','2010-03-21','Speech / interview','First press conference profile, lines 122–129',
    'Sitharaman said she joined BJP in 2006 because she agreed with its ideology. Report discusses Nitin Gadkari’s team, her English and southern-language fluency, developing Hindi, and compares her with Sushma Swaraj and Jayanthi Natarajan.',
    'Contemporaneous attributed joining-year evidence preferred over later 2008 summaries. Reporter’s gender and nationalist framing is interpretation.')
src(8,'Sitharaman wins Rajya Sabha seat from Karnataka','Indo-Asian News Service / NDTV','https://www.ndtv.com/india-news/congress-wins-3-rajya-sabha-seats-from-karnataka-bjp-gets-1-1418017','2016-06-11','Journalism','Election results, lines 228–239',
    '11 June 2016 election: Sitharaman received 47 legislator votes; other winners Fernandes, Ramesh and Ramamurthy. Four vacancies; minimum reported requirement 45.',
    'News reproduction of election count; returning officer’s count sheet not retrieved. Multi-seat election has no single runner-up margin.',origin='IANS-2016-06-11-RS')
src(9,'BJP wins three of four Karnataka Rajya Sabha seats','Anusha Ravi Sood / South First','https://thesouthfirst.com/politics/bjp-wins-3-of-4-rajya-sabha-seats-in-karnataka-congress-bags-1-as-jds-refuses-support/','2022-06-11','Journalism','Road to victory, lines 71–82',
    'Sitharaman elected on Friday 10 June with 46 first-preference votes; second consecutive Karnataka election. Explains transfers and Congress–JD(S) rivalry.',
    'Primary returning officer’s count sheet not retrieved; avoid importing conflicting counts for other candidates.')
src(10,'Budget 2026–2027 speech','Nirmala Sitharaman / Ministry of Finance','https://www.indiabudget.gov.in/doc/budget_speech.pdf','2026-02-01','Official record','Paragraphs 1–4, 84, 91–100',
    '2026–27 speech proposes SHE-Marts; retains 41% vertical tax devolution; fiscal deficit 4.4% in 2025–26 revised estimates and 4.3% in 2026–27 budget estimates. Debt target 50±1% by 2030–31; new income-tax law to commence April 2026.',
    'Budget and revised estimates are not audited outturns. Generic current-budget URL may change after a future budget; title and date identify this version.')
src(11,'Union Budget 2026–27 analysis','PRS Legislative Research','https://prsindia.org/budgets/parliament/union-budget-2026-27-analysis','2026-02-01','Research / budget analysis','Budget highlights; tax proposals; infrastructure',
    '2026–27 expenditure Rs53,47,315 crore; interest 26% of spending and 40% of revenue receipts. Deficit target 4.3% of GDP. Public capex planned at Rs12.2 lakh crore. STT increases proposed for derivatives.',
    'Independent analysis of government estimates; not actual expenditure or causal evaluation. Tax proposals and enacted measures require separate dates.')
src(12,'Foreign Trade Policy 2015–2020 unveiled','Ministry of Commerce and Industry / PIB','https://www.pib.gov.in/newsite/printrelease.aspx?lang=2&reg=48&relid=117917','2015-04-01','Official record','Opening and scheme design, lines 15–24',
    'Sitharaman unveiled FTP 2015–20; MEIS and SEIS consolidated export incentives using transferable duty-credit scrips. Policy linked manufacturing, services and ease of doing business.',
    'Launch/design evidence; no demonstrated net export effect.')
src(13,'Corporate tax rates reduced','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=1585641&lang=2&reg=48','2019-09-20','Official record','Ordinance and rate conditions, points 1–2; revenue estimate',
    'Sitharaman announced Taxation Laws Amendment Ordinance: optional 22% domestic-company base rate without specified incentives; 15% for qualifying new manufacturing; 25.17% effective ordinary rate with surcharge/cess. Estimated revenue forgone for package Rs1,45,000 crore.',
    'Base rates differ from effective rates; eligibility conditions apply. Revenue figure is an announcement estimate.')
src(14,'56th GST Council recommendations','GST Council / Ministry of Finance','https://www.gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau_0.pdf','2025-09-03','Official record','PDF pp.1–4, rate structure and commencement',
    'Council chaired by Sitharaman recommended main rates 5% and 18%, special 40% for selected supplies, individual life/health insurance exemption. Most changes scheduled 22 September; specified tobacco goods deferred.',
    'Recommendations require notifications; exceptions prevent describing every supply as taxed only at two rates.',origin='GST-56-RECOMMENDATIONS')
src(15,'FAQ 3 on 56th GST Council decisions','Ministry of Finance / PIB','https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2168426&lang=2&reg=3','2025-09-18','Official record','Questions 1–3',
    'Identifies 17 September 2025 notifications 9/2025 and 10/2025 Central Tax (Rate), replacing 2017 goods-rate and exemption notifications.',
    'Evidence of notification stage via official explanatory record, not a line-by-line commodity classification audit.')
src(16,'India 2021 Article IV consultation','International Monetary Fund','https://www.imf.org/-/media/Files/Publications/CR/2021/English/1INDEA2021001.ashx','2021-10-15','Research / institutional','Staff report paragraphs 16, 19 and 22; PDF pp.15–18',
    'Announced fiscal support: above-line 4.1% GDP, below-line 6.2%. IMF welcomes bringing food subsidies onto budget and recommends additional near-term support around 1% GDP above baseline.',
    'Staff report dated 31 August 2021. Historical estimate vintage; commitments and credit guarantees are not equivalent to expenditure. Distinguish baseline recommendation from adverse-scenario box.')
src(17,'2025 income-tax rebate and slab proposals','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&lang=2&reg=48','2025-02-01','Official record','Rebate explanation and rate table',
    'Budget proposes no normal-rate tax up to Rs12 lakh through rebate under new regime; salaried illustration Rs12.75 lakh with Rs75,000 standard deduction. Special-rate income excluded. Basic nil slab remains Rs4 lakh.',
    'Historical proposal description, not personalised tax advice. Rs12 lakh is a rebate threshold, not the nil-rate slab.')
src(18,'Pradhan Mantri Garib Kalyan relief package','Ministry of Finance / PIB','https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1608345&lang=2&reg=48','2020-03-26','Official record','Opening and cash transfer/SHG sections',
    'Sitharaman announced Rs1.70 lakh crore package with food, cash and insurance support. Women Jan Dhan holders were promised Rs500 monthly for three months; SHG collateral-free credit limit raised to Rs20 lakh.',
    'Announcement targets; does not establish every eligible person received relief. Grain units differ per individual and per household.')
src(19,'Retrospective taxation amendment Bill 2021','PRS Legislative Research','https://prsindia.org/billtrack/the-taxation-laws-amendment-bill-2021','2021-08','Research / legislative brief','Status chronology and bill summary',
    'Sitharaman introduced bill 5 August, passed Lok Sabha 6 August and Rajya Sabha 9 August 2021. Reverses pre-28 May 2012 indirect-transfer tax liability subject to withdrawal/waiver conditions; refund without interest.',
    'Parliamentary passage and bill provisions; not proof that all disputes were settled.')
src(20,'Air India strategic disinvestment completed','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=1792950&lang=2&reg=3','2022-01-27','Official record','Opening transaction paragraph',
    'Transfer to Tata subsidiary Talace completed: Rs2,700 crore cash to government and Rs15,300 crore debt retained in transferred airline entities; specified shares transferred.',
    'Rs18,000 crore enterprise value is not Rs18,000 crore cash revenue. Wider legacy liabilities excluded from this transaction summary.')
src(21,'Income-tax Act 2025 comes into force','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=2248005&amp=&lang=1&reg=3','2026-04-01','Official record','Opening and commencement, lines 21–27',
    'New Act replaced 1961 Act from 1 April 2026; assent 21 August 2025; rules notified 20 March 2026. Ministry says recast simplifies structure without changing underlying tax policy.',
    'Commencement verified via official release; simplification benefits remain a government objective.')
src(22,'PRARAMBH 2026 tax awareness campaign','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=2243196&lang=2&reg=3','2026-03-20','Official record','Launch and minister’s remarks, lines 29–63',
    'Sitharaman launched multimedia tax-law awareness campaign and new website; called for empathetic administration, multilingual outreach, technological assistance, stability and fewer amendments.',
    'Evidence of an administrative launch and stated method, not measured taxpayer experience.')
src(23,'Naleen Kumar Kateel v State of Karnataka','Karnataka High Court; Indian Kanoon reproduction','https://indiankanoon.org/doc/5816233/','2024-12-03','Court judgment','Crl.P.10321/2024; paragraph 2; final order (ii)',
    'Electoral-bonds extortion complaint named Sitharaman as accused 1. Court found missing prima-facie extortion ingredients and quashed Crime224/2024 proceedings specifically for petitioner Kateel.',
    'Operative relief is expressly qua the petitioner. Does not by itself establish personal quashing for Sitharaman; official signed copy not retrieved.',origin='KHC-10321-2024')
src(24,'B Y Vijayendra v State of Karnataka','Karnataka High Court; Indian Kanoon reproduction','https://indiankanoon.org/doc/49072493/','2024-12-17','Court judgment','Crl.P.13192/2024; paragraphs 3–4 and final order',
    'Court says earlier reasoning addressed all accused but operative order covered Kateel only; Vijayendra therefore sought separate relief and obtained quashing as petitioner.',
    'This clarifies the limited scope of the earlier operative order. No later personal disposition for Sitharaman verified.',origin='KHC-13192-2024')
src(25,'High Court quashes electoral-bonds case: headline and report','Bar & Bench','https://www.barandbench.com/news/karnataka-high-court-quashes-electoral-bonds-case-against-nirmala-sitharaman-others','2024-12-03','Journalism','Headline and visible opening paragraphs',
    'Report describes case as quashed against Sitharaman and others following Kateel’s petition.',
    'Visible opening only; broad headline conflicts with narrow operative relief in S023 and clarification in S024. Retained as contradictory reporting, not proof of personal disposition.')
src(26,'Rafale review judgment explained','Supreme Court Observer','https://www.scobserver.in/reports/manohar-lal-sharma-narendra-modi-rafale-fighter-jet-deal-review-judgment-plain-english/','2019-11-15','Research / legal reporting','Review dismissal and scope, lines 33–58',
    'Supreme Court dismissed review petitions 14 November 2019; reiterated limited Article32 scrutiny of defence procurement. Acknowledged CAG/PAC wording error without finding government had misled it.',
    'Limited judicial review is not a criminal trial or unrestricted procurement audit. Its background misdates the initial announcement; not adopted.')
src(27,'Defence procurement and strategic relations interview','Sushant Singh interviewing Nirmala Sitharaman / Indian Express','https://indianexpress.com/article/india/defence-minister-nirmala-sitharaman-rafale-fighter-deal-controversy-india-pakistan-china-relations-doklam-5353413/','2018-09-13','Speech / interview','COMCASA and Rafale questions, lines 21–66',
    'Sitharaman defended US cooperation alongside Russian ties; justified 36 Rafales by urgent induction and infrastructure constraints, and described efforts to accelerate procurement.',
    'Her defence of policy is attributed; interview is not independent validation of pricing or readiness.')

def failed(n, sid, url, reason):
    retrievals.append({'id':f'RF{n:02d}', 'source_id':sid, 'url_or_query':url, 'access_date':ASOF,
        'route':'Attempted canonical institution or official mirror', 'access_status':'Unavailable',
        'origin_id':sid, 'locator':'No readable passage', 'passage_paraphrase':'',
        'method':'web.run retrieval', 'result':reason, 'next_action':'Use inspected alternative; revisit only with a new retrieval route.'})

failed(1,'S003','https://www.pib.gov.in/PressReleasePage.aspx?PRID=2024501&lang=2&reg=48','Cache miss; iframe version succeeded.')
failed(2,'S004','https://dea.gov.in/whos-who/nirmala-sitharaman','502; DFS listing used.')
failed(3,'S001','https://sansad.in/rs/members/biographyM/2288','Dynamic page returned no biography; parliamentary Who’s Who used.')
failed(4,'S001','https://doe.gov.in/smt-nirmala-sitharaman','No readable page returned.')
failed(5,'S001','https://www.dea.gov.in/index.php/our-teams/smt-nirmala-sitharaman','No readable page returned.')
failed(6,'S007','https://www.nirmalasitharaman.in/about/','Personal website inaccessible; contemporaneous interview used.')
failed(7,'S007','https://www.nirmalasitharaman.in/','Personal website home inaccessible; stop repeated variants.')
failed(8,'S016','https://www.elibrary.imf.org/view/journals/002/2021/230/article-A001-en.xml','Unavailable; IMF report PDF inspected instead.')

src(28,'WTO public stockholding decision WT/L/939','WTO General Council','https://www.wto.org/english/thewto_e/minist_e/mc9_e/nov14stockholding_e.htm','2014-11-27','Official record','Decision paragraphs 1–5',
    'Conditional protection from specified agricultural-subsidy challenges continues until a permanent solution is adopted; dedicated negotiations continue.',
    'Decision body dates 27 November; page heading says 28 November. Use signed decision identification. Protection is conditional, not unlimited exemption.')
src(29,'The Resilience of India’s Fourth Party System','Milan Vaishnav and Caroline Mallory / Carnegie Endowment','https://carnegieendowment.org/research/2024/09/india-election-bjp-party-politics','2024-09-26','Research / scholarly','Introduction and party-system sections, lines 49–88, 122–130',
    'Coalition politics characterised 1989–2014; BJP won majorities in 2014 and 2019. Its 240 seats in 2024 required allies. Authors argue BJP centrality persisted despite diminished dominance.',
    'Historical September 2024 analysis, not a current count of governments or MPs; causal application to Sitharaman is workbook analysis.')
src(30,'Sitharaman explains decision against Lok Sabha contest','ET Online reporting Times Now Summit','https://economictimes.indiatimes.com/news/elections/lok-sabha/india/i-do-not-have-the-kind-of-money-to-contest-lok-sabha-elections-nirmala-sitharaman/articleshow/108825590.cms','2024-03-28','Speech / interview','Summit remarks, lines 124–140; originally published 27 March',
    'She said Nadda offered Andhra Pradesh or Tamil Nadu; she declined citing personal campaign resources and community-based winnability, while agreeing to campaign for others.',
    'Attributed reasons; not an independently audited account of wealth, party finance or voter preferences.')
src(31,'BJP apologises over shared business-owner video','J Sam Daniel Stalin and Uma Sudhir / NDTV','https://www.ndtv.com/india-news/sree-annapoorna-owner-nirmala-sitharaman-video-k-annamalai-bjp-leaders-apology-for-sharing-nirmala-sitharaman-businessman-video-6556934','2024-09-13','Journalism','Report paragraphs, lines 228–255',
    'After Coimbatore GST questions and a purported apology video, Annamalai apologised for functionaries sharing a private conversation. Congress and DMK criticised treatment. Sitharaman had said she would consider the tax concern.',
    'NDTV explicitly could not authenticate the second video/conversation. Coercion and motive are not established; historic tax examples are not current tax guidance.')
src(32,'Electoral-bonds FIR and political responses','Press Trust of India / Rediff','https://www.rediff.com/news/report/electoral-bonds-court-orders-fir-against-nirmala-sitharaman/20240928.htm','2024-09-28','Journalism','FIR, allegation and responses, lines 40–59',
    'Police registered FIR on court direction after Adarsh Iyer’s complaint. Kumaraswamy rejected resignation demands, distinguishing personal benefit; BJP’s Ashoka promised a legal response.',
    'Allegations and political defences establish respective positions, not their truth.',origin='PTI-2024-09-28-ELECTORAL-BONDS')
src(33,'Sitharaman takes charge at Finance and Corporate Affairs','Ministry of Finance / PIB','https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1572921&lang=2&reg=48','2019-05-31','Official record','Opening; defence record; brief profile',
    'Took charge 31 May 2019; first full-time woman Finance Minister. Government credited her with Defence Planning Committee and procurement decisions.',
    'Charge-taking differs from parliamentary tenure date 30 May. Government praise is attributed. Repeats disputed 2008 BJP joining year.')
src(34,'Cabinet approves ten-bank consolidation into four','Ministry of Finance / PIB','https://www.pib.gov.in/PressReleasePage.aspx?PRID=1605149&lang=2&reg=48','2020-03-04','Official record','Approval, four combinations and effective date',
    'Cabinet approved ten PSBs combining into PNB, Canara, Union Bank and Indian Bank from 1 April 2020, aiming at scale, cost and technology benefits.',
    'Approval with effective date; claimed synergies require outcome evaluation. Cabinet decision under Modi; ministerial association does not imply sole authorship.')
src(35,'Statement to Parliament on India’s WTO stand','Nirmala Sitharaman / Ministry of Commerce','https://www.commerce.gov.in/wp-content/uploads/2020/04/CIM_parliamant_statement_WTO_28_11_2014.pdf','2014-11-28','Official record','Paragraphs 2–6, 12, 15–19',
    'Explained India withholding trade-facilitation consensus to secure stockholding protection; reported US agreement and WTO decisions, crediting Modi’s leadership and wider support.',
    'Minister’s negotiating account; compare actual multilateral decision S028. Claimed victory is not an independent welfare assessment.')
src(36,'MEA Annual Report 2018–19: first India–US 2+2','Ministry of External Affairs','https://www.mea.gov.in/Uploads/PublicationDocs/31719_MEA_AR18_19.pdf','2019','Official record','Printed p.185; PDF p.187; 2+2 Ministerial Dialogue',
    'Swaraj and Sitharaman met Pompeo and Mattis on 6 September 2018. COMCASA signed during visit, intended to enable secure communications and advanced US-origin systems.',
    'Agreement and ministerial participation verified; capability benefits are intended effects.')
src(37,'Vanathi Srinivasan credits women leaders’ support','ThePrint interview / profile','https://theprint.in/politics/how-woman-who-vanquished-kamal-haasan-in-coimbatore-became-bjp-star-campaigner-in-himachal/1210811/','2022-11','Speech / interview','Indexed passage headed Support from women leaders',
    'Vanathi Srinivasan credited encouragement from Irani, Swaraj and Sitharaman alongside Pon Radhakrishnan.',
    'Full page unavailable; relevant indexed paragraph inspected. Bounded attributed mentoring evidence, not a systematic study of women’s recruitment.')
retrievals[-1]['route']='Search-index displayed passage; full page unavailable'
retrievals[-1]['method']='Relevant attributed paragraph fully visible in web search result'
failed(9,'S036','https://meacms.mea.gov.in/Uploads/PublicationDocs/31719_MEA_AR18_19.pdf','Mirror failed; canonical www.mea.gov.in PDF succeeded.')
failed(10,'S031','https://www.ndtv.com/india-news/sree-annapoorna-owner-nirmala-sitharaman-video-k-annamalai-bjp-leaders-apology-for-sharing-nirmala-sitharaman-businessman-video-6556934/amp/1','AMP failed; canonical article inspected.')
failed(11,'S037','https://theprint.in/politics/how-woman-who-vanquished-kamal-haasan-in-coimbatore-became-bjp-star-campaigner-in-himachal/1210811/','Canonical page failed twice; indexed relevant passage is R037.')
src(38,'Union Budget 2024–25 analysis','PRS Legislative Research','https://prsindia.org/budgets/parliament/union-budget-2024-25-analysis','2024-07-23','Research / budget analysis','Policy highlights: employment, skilling and state assistance; lines 103–109',
    'Budget announced EPFO-linked employment incentives, internships and skilling; proposed Rs15,000 crore support for Andhra Pradesh capital development.',
    'Announcement-stage assessment; programme targets are not completed jobs or disbursement totals.')
src(39,'Atmanirbhar Bharat package progress','Ministry of Finance / PIB','https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1660691&lang=2&reg=48','2020-10-01','Official record','Opening and ECLGS section, lines 12–21',
    'Modi announced headline Rs20 lakh crore package; Sitharaman detailed it 13–17 May and reviewed implementation. Initial ECLGS guarantee envelope Rs3 lakh crore; ministry reported Rs1,32,246 crore disbursed by 29 September 2020.',
    'Administrative reporting by specified lenders, not independent causal evaluation. Loan disbursement is not government grant spending.')
src(40,'BJP removes functionary after Coimbatore video','Times of India','https://timesofindia.indiatimes.com/city/coimbatore/tamil-nadu-gst-hotelier-video-bjp-expels-functionary-for-posting-clip-of-mans-apology-to-fm/articleshow/113359434.cms','2024-09-15','Journalism','Opening; district party statement, line 162',
    'District BJP statement removed R Sathish from post and membership after circulating the hotelier video.',
    'Corroborates controversy and party response; does not establish that the minister compelled an apology.')
src(41,'Supreme Court dismisses electoral-bonds challenge','Ananthakrishnan G / Indian Express','https://indianexpress.com/article/india/supreme-court-dismisses-appeal-karnataka-high-court-quashing-fir-sitharaman-poll-bond-conspiracy-9814820/','2025-02-03','Journalism','Hearing and dismissal, lines 20–33',
    'SC dismissed Adarsh Iyer’s SLP on 3 February 2025, declining a speculative inquiry; preserved recourse for a person with material evidence.',
    'Headline and opening broadly describe Sitharaman; compare Kateel-specific petition identified in S042 and High Court operative orders.')
src(42,'Supreme Court declines challenge to Kateel quashing','Anmol Kaur Bawa / LiveLaw','https://www.livelaw.in/top-stories/vague-complaint-complete-assumptions-supreme-court-affirms-hc-order-quashing-fir-against-bjp-leader-over-alleged-electoral-bonds-extortion-282851','2025-02-03','Research / legal reporting','Hearing, clarification and case details; lines 205–242',
    'Adarsh R Iyer v State of Karnataka, SLP(Crl)1183/2025: challenge to Kateel relief dismissed; a supported fresh complaint was not barred. Court distinguished scheme constitutionality from case-specific coercion.',
    'Full relevant report inspected. Signed Supreme Court order not retrieved; no extension of operative relief to unnamed parties inferred.')
src(43,'Rafale review judgment, 14 November 2019','Supreme Court of India','https://api.sci.gov.in/supremecourt/2019/58/58_2019_1_1502_18275_Judgement_14-Nov-2019.pdf','2019-11-14','Court judgment','Kaul opinion paragraphs 11–13 and 25, PDF pp.6–7,12; Joseph opinion paragraphs 85–87, PDF pp.105–107',
    'Review petitions dismissed within Article32 limits. Joseph’s concurrence preserved lawful action on the complaint subject to prior approval under section17A.',
    'Official court PDF inspected. Dismissal of review is distinct from a personal criminal acquittal; no later investigation is inferred.',origin='SCI-RAFALE-REVIEW-2019')
src(44,'Rajya Sabha Secretariat Annual Report 2014: Table Office','Rajya Sabha Secretariat','https://cms.rajyasabha.nic.in/RSSFiles/1629116866724.84_tableoffice.pdf',None,'Official record','Section37.8; printed p.202, PDF p.3',
    'Lists Sitharaman among 2014 by-election entrants, representing Andhra Pradesh; records oath and entry in membership registers.',
    'Primary confirmation of election and state, but this passage does not state declaration day or unopposed status. Publication date not printed in extracted section.')
src(45,'Karnataka Rajya Sabha election: candidate counts','Johnson TA / Indian Express','https://indianexpress.com/article/political-pulse/karnataka-8-jds-mlas-cross-vote-congress-wins-three-rajya-sabha-seats-bjp-gets-one-2848076/','2016-06-12','Journalism','Opening and vote counts; lines 20–34',
    'Reports 47 votes for Sitharaman, matching BJP’s assigned support. Final formal EC declaration was delayed at publication after a JD(S) complaint.',
    'Independent corroboration of reported count, not a substitute for the signed final return. Distinguish polling date from declaration.',origin='IE-2016-06-12-KARNATAKA')
failed(12,'S043','https://scobserver-production.s3.amazonaws.com/uploads/case_document_resource/document_upload/496/58_2019_1_1502_18275_Judgement_14-Nov-2019.pdf','SCO mirror returned403; matching official Supreme Court PDF succeeded.')
failed(13,'S042','https://indiankanoon.org/search/?formInput=%22Adarsh%20R%22%20%221183%22','Search route unavailable; signed SC order still not retrieved.')
