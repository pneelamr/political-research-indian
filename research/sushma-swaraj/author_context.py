"""Career-specific context: evidence limits remain visible."""
coverage={
'Gender':['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
'Era':['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']}

def populate_context(add,phases):
    gender=[
('Law, student activism and the JP movement are evidenced entry routes. Her 1977 ministry and later firsts demonstrate advancement; the sources do not isolate how gender affected nomination or promotion.',[1,2,4],'Material finding','Compare access pathways rather than assuming either barrier-free merit or gender alone.'),
('First woman Delhi CM, first woman Lok Sabha opposition leader and first full-time woman EAM are distinct milestones. Earlier female additional charge prevents an unqualified first-woman-EAM claim.',[2],'Material finding','Institution-specific firsts; symbolic inclusion is not an outcome evaluation.'),
('She described an RSS family, ABVP student politics and socialist connections through marriage. These politically relevant networks are documented without treating family relations as an adequate explanation of her career.',[4],'Material finding','Access through political networks; comparative gender effect unmeasured.'),
('Labour, education, broadcasting, health, parliamentary affairs and external relations gave her varied responsibilities. Appointment records do not explain selection in gender terms.',[3,14],'Evidence not found','Portfolio range is observed; a gendered allocation mechanism needs comparative appointment evidence.'),
('An Indian Express editorial discussed a conservative feminine public image; She Persisted analysed maternal labels and hostile imagery. These are attributed interpretations, not a systematic media-frequency study.',[30,32],'Material finding','Presentation and reception may differ; avoid adopting stereotypes as personality facts.'),
('She Persisted documents gendered and religious abuse, including calls for violence, after the 2018 interfaith-couple passport case. This establishes a specific harassment episode, not its prevalence across her entire career.',[30],'Material finding','Threats targeted at a woman in office; actual effects on her choices remain unmeasured.'),
('Private-member bills addressed women’s safety and welfare in 2005–2006; she supported women’s reservation in 2010 and accepted passport-document reform in 2016. The private bills lapsed; policy advocacy and enactment differ.',[47,31,20],'Material finding','Legislative initiative, party management and executive rules are different mechanisms.'),
('Her proposed 2004 protest against Sonia Gandhi used head-shaving and white-clothing symbolism, defended later as patriotism. Analysis should examine the political use of these symbols without treating women as a uniform political group.',[4],'Material finding','Gendered symbolism intersected with nationalist argument; effect on succession unproved.'),
('Institutional firsts and specific proposals are documented; no collected evaluation establishes that her rise increased women’s nominations, representation or material welfare overall.',[2,47,20],'Research limitation','Separate descriptive representation, substantive proposals, implementation and measured effects.'),
('The evidence varies across periods: early access routes, national-office firsts, opposition bills and later service reforms. Gendered harassment persisted alongside senior authority; a single empowerment verdict would erase these differences.',[2,4,47,20,30],'Research limitation','Assess change across the career while retaining uncertainty about causal mechanisms.')]
    for n,(finding,ids,disp,mech) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],'Career phase':'Across four phases','Research disposition':disp,'Finding':finding,'Mechanism / interpretation':mech,'Presentism caution':'Use evidenced contemporary institutions and choices; do not assume gender explains every event.'},ids,'Analysis',status='Not reviewed' if disp=='Evidence not found' else 'Supported')
    era=[
    [
    ('Janata candidacy in 1977/1980 and BJP candidacy by 1984 place her within changing opposition-party affiliations. Later RSS-family self-description should not erase the Janata electoral record.',[5,8,13,4],'Material finding'),
    ('A state Assembly seat and ministerial appointment were separate sources of authority; losing Karnal did not erase her Haryana career. Legal practice and movement participation were additional entry routes.',[1,3,5,6],'Material finding'),
    ('Two Ambala Cantt victories coexist with three Karnal defeats. Different electoral arenas prevent treating national-seat losses as a simple measure of all local support.',[5,6,8,13],'Material finding'),
    ('No inspected phase-specific record connects macroeconomic conditions to her early labour or education decisions. Cabinet membership alone cannot supply that causal history.',[3],'Evidence not found'),
    ('No direct evidence collected links international-system changes to her Haryana-era decisions. Later diplomatic prominence should not be projected backward.',[1,3],'Evidence not found'),
    ('Early parliamentary biographies document offices; her 2007 interview retrospectively frames formation. Neither is a representative archive of 1970s–1980s campaign communication.',[1,3,4],'Research limitation'),
    ('Student, family and movement networks offered multiple political connections. The record supports access routes, but not a quantified comparison with other Janata or BJP entrants.',[2,4],'Research limitation'),
    ('No constituency study collected identifies the caste, class, religious or gender composition of her early electoral coalition. Surname, party label and district location cannot substitute for evidence.',[5,6,8],'Evidence not found'),
    ('Ambala Cantt was an Assembly constituency; Karnal a Lok Sabha constituency. Votes from these units have different electorates and should not be plotted as a like-for-like popularity series.',[5,6,8],'Material finding'),
    ('Primary Karnal tables for 1980 and 1989 are inspected. Assembly returns and 1984 use labelled secondary fallbacks; exact dates and denominators remain uneven.',[5,6,8,13],'Research limitation')
    ],
    [
    ('Her national rise combined BJP parliamentary seats, Vajpayee ministries and a brief Delhi leadership assignment. Party sponsorship, parliamentary route and executive appointment operated together.',[2,3],'Material finding'),
    ('Rajya Sabha return allowed national office after the Bellary defeat. The 2003 tobacco bill also depended on earlier drafting, committee work and both Houses, not ministerial will alone.',[2,10,16],'Material finding'),
    ('South Delhi victories, Hauz Khas victory and Bellary defeat occurred in different contests. The 1998 personal Assembly win accompanied BJP’s wider Delhi defeat.',[7,9,10,12,41],'Material finding'),
    ('Film-industry recognition linked policy to institutional finance. PMSSY’s later approval shows why an announcement in one government phase must not be equated with completed investment.',[15,17],'Material finding'),
    ('The collected material is insufficient for a phase-specific account of international pressures shaping her broadcasting or health choices. Later foreign-policy roles provide no substitute.',[3,15,16],'Evidence not found'),
    ('Contemporary Delhi reporting foregrounded onion prices, power and water; her campaign defended administrative action. This provides an issue frame, not a measured explanation of voter behaviour.',[40,41],'Material finding'),
    ('The national BJP leadership moved her between parliamentary, Cabinet and Delhi roles. A retrospective editorial attributes mentorship to Vajpayee and Advani; nomination motives require more direct evidence.',[3,32],'Research limitation'),
    ('Delhi campaign reporting records household-price and service concerns. Evidence here does not quantify social-group voting or isolate the effects of gender, religion or class.',[40],'Research limitation'),
    ('Delhi leadership, a Karnataka campaign and later Upper House service extended her arena beyond Haryana. Bellary defeat should be read as a specific candidacy, not proof of Karnataka-wide rejection.',[3,10],'Material finding'),
    ('Contemporary policy statements are stronger on intended mechanisms than effects. Six AIIMS-type hospitals were announced in 2003, while the cited approval is 2006.',[15,16,17],'Research limitation')
    ],
    [
    ('Committee leadership and then Lok Sabha opposition leadership gave her channels of influence outside the executive. Cooperation on selected legislation could coexist with partisan confrontation.',[3,31,4],'Material finding'),
    ('Committee scrutiny, private-member bills and opposition leadership are different institutional tools. The inspected private-bill register marks her 2005–2006 proposals lapsed.',[3,47],'Material finding'),
    ('The 2009 Vidisha victory occurred after Congress’s nominee lost his nomination. The unusually lopsided result cannot be attributed to personal popularity without accounting for that contest structure.',[11,39],'Material finding'),
    ('Her 2007 interview emphasised inflation alongside growth. This is a stated opposition critique, not an independently established account of macroeconomic performance.',[4],'Material finding'),
    ('An External Affairs committee chairmanship is documented, but no inspected committee report establishes her specific international-policy influence in this phase.',[3],'Evidence not found'),
    ('Interviews and reporting preserve her explanations of Sonia Gandhi and Reddy controversies; an obituary editorial supplies a later civility narrative. These genres should not be treated as interchangeable evidence.',[4,33,32],'Research limitation'),
    ('Work with other BJP leaders over the women’s reservation bill illustrates internal party management. It shows an exercised option—party discipline—without proving universal control over MPs.',[31],'Material finding'),
    ('Women’s safety, girls’ education and welfare were subjects of her private bills. Proposal titles establish agenda selection, not beneficiary outcomes or a social-coalition estimate.',[47],'Research limitation'),
    ('The shift to Vidisha and Upper House service illustrates national-party mobility across constituencies. Exact Rajya Sabha state allocations still require original notifications.',[2,11],'Research limitation'),
    ('This phase has primary interview and legislative-register evidence, but constituency results use a secondary fallback. Contemporary criticism and retrospective assessments are kept separate.',[4,47,11,32],'Research limitation')
    ],
    [
    ('Cabinet membership placed her within Modi’s government; a retrospective editorial describes a PMO-centred foreign policy. That is an attributed interpretation, not a quantified measure of her autonomy.',[14,32],'Research limitation'),
    ('Portfolio allocation conferred executive responsibility, while Parliament, courts and diplomatic counterparts constrained action. The ICJ outcome followed her tenure and does not imply sole ministerial authorship.',[14,25],'Material finding'),
    ('She retained Vidisha in 2014 and did not contest in 2019, citing health. Her final ministerial years cannot be evaluated through a nonexistent 2019 personal election result.',[11,36],'Material finding'),
    ('Consular access and easier passport documentation addressed services rather than an economy-wide programme. The collected record does not isolate economic returns from these reforms.',[19,20],'Research limitation'),
    ('Yemen evacuation required coordination with foreign governments and operational agencies; Pakistan dialogue and the OIC address show other diplomatic settings. Announcements and access did not guarantee durable settlements.',[18,24,23],'Material finding'),
    ('MADAD institutionalised a grievance channel, while editorial and harassment research describe social-media visibility. Individual public replies and a tracking system are different service mechanisms.',[19,30,32],'Material finding'),
    ('The Bangladesh measure illustrates cross-party and state-level negotiation; Yemen illustrates shared Cabinet, ministerial and agency responsibilities. Both limit heroic single-person accounts.',[21,18],'Material finding'),
    ('Passport rules engaged varied family circumstances; the interfaith-passport abuse episode shows contested religious and gender boundaries. Neither source establishes all citizens’ experience of the ministry.',[20,30],'Material finding'),
    ('Bangladesh boundary legislation involved affected states and inherited agreements; the ministry’s consular work also served Indians outside the territorial electorate. These are distinct accountability settings.',[21,46,18],'Material finding'),
    ('Official statements document decisions and dated outputs; journalism and advocacy preserve criticism. Independent service-impact evidence and some failed official-source retrievals remain explicit gaps.',[18,20,26,28,30],'Research limitation')
    ]]
    comparisons=[
    'Comparison frame: Haryana entrants through law, movements and Janata/BJP networks. Electoral and executive routes were distinct; no matched candidate-selection study collected.',
    'Comparison frame: BJP national leaders under Vajpayee and Advani. Parliamentary election, Upper House return, Cabinet work and state campaigning were different available routes.',
    'Comparison frame: parliamentary opposition leaders and committee chairs. Scrutiny, private bills, party discipline and public protest were available methods; effects differ.',
    'Comparison frame: Cabinet foreign ministers operating with a strong prime minister and professional agencies. Public case intervention, institutional services and negotiated agreements served different purposes.'
    ]
    for p,items in enumerate(era,1):
        for n,(finding,ids,disp) in enumerate(items,1):
            add('Context & Constraints',f'E{p}{n:02d}',{'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],'Career phase':phases[p-1],'Research disposition':disp,'Finding':finding,'Available choices / comparison':comparisons[p-1],'Presentism caution':'Separate the institutions and evidence of this period from later reputation; comparison frame is analytical, not causal proof.'},ids,'Analysis',status='Not reviewed' if disp=='Evidence not found' else 'Supported')
