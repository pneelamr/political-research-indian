"""Gender and phase-specific context, including explicit research gaps."""
coverage={
'Gender':['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
'Era':['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']}

def populate_context(add,phases):
    gender=[
    ('Theatre, cinema and DMK organisation provided entry routes. Sources do not isolate the advantage of being a male star relative to comparable female performers seeking political authority.',[1,23],'Research limitation','Compare recruitment and promotion of male and female cinema figures within the same party period.'),
    ('His chief-ministerial rise is a cinema-to-politics milestone. It is not evidence that women had equal access; eight women were elected to the Assembly in 1984.',[6,10],'Material finding','Distinguish individual office attainment from the distribution of opportunity.'),
    ('Fan clubs supported MGR’s organisation; Jayalalithaa’s party entry and Janaki’s later succession claim show distinct cinema, party and family pathways. Neither woman’s agency should be reduced to association alone.',[5,2],'Material finding','Compare resources, organisational work and legitimacy claims, rather than assuming a single dynastic route.'),
    ('In 1985, women ministers held welfare/meals and Khadi/handlooms while MGR retained administration and police. The allocation is documented; a gender-based selection motive is not established.',[6],'Research limitation','Observe portfolio distribution without inferring why each minister was selected.'),
    ('Protective screen roles are documented, but a systematic comparison of gendered media treatment of MGR and female contemporaries has not been collected.',[23,5],'Evidence not found','Need comparable media samples; heroic imagery alone does not measure a gender double standard.'),
    ('The 1967 shooting is documented. No inspected evidence identifies it as gender-targeted violence or establishes a gender-specific threat mechanism in his political career.',[23],'Evidence not found','Do not equate a personal attack with gender-based persecution.'),
    ('Women’s higher education and meal-related employment are substantive policy pathways. The 2004 meal assessment also records insecure work conditions; later employment totals cannot be backdated to his tenure.',[13,4],'Material finding','Separate creation, access, job quality and independently measured outcomes.'),
    ('Subramanian links AIADMK’s appeal to promises of protection for women and the poor. This is an interpretation of political identity and benefit expectations, not a claim that all women voted alike.',[5],'Material finding','Distinguish rhetorical positioning from voter-level response.'),
    ('Women’s university creation and female legislative presence are observable. No collected study measures MGR’s personal effect on women’s nominations, decision authority or long-term economic independence.',[13,6],'Research limitation','Separate descriptive representation, substantive provision and causal effect.'),
    ('Assessment changes across cinema, welfare administration and posthumous succession. Later female leadership cannot by itself prove that his organisation provided equal opportunity throughout his career.',[23,13,2],'Research limitation','Use phase-specific evidence and comparable institutions; avoid a single empowerment score.')]
    for n,(finding,ids,disposition,mechanism) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],'Career phase':'Across five phases','Research disposition':disposition,'Finding':finding,'Mechanism / interpretation':mechanism,'Contemporary comparison group':'Men and women with comparable cinematic prominence, party seniority and electoral route; no matched causal study collected.','Presentism caution':'Apply the same relevance test to personal lives and identity; distinguish observed patterns from unverified motives.'},ids,'Analysis',status='Not reviewed' if disposition=='Evidence not found' else 'Supported')
    era=[
    [
    ('Congress association followed by DMK membership placed him within a changing route from national-party affiliation to Dravidian organisation. Cinema became an important bridge.',[23,1],'Material finding'),
    ('Entry into the Legislative Council preceded Assembly election. The institutional route is incompletely documented and must not be represented as an established popular-vote victory.',[1],'Research limitation'),
    ('No direct Assembly contest is recorded for this phase; Council membership in 1962 is the verified milestone. The route and electorate require the original notification.',[1],'Research limitation'),
    ('Family hardship is documented, but a period-specific study connecting economic conditions to his early political choices has not been collected.',[1],'Evidence not found'),
    ('Birth in Ceylon is documented. The record does not establish how colonial or post-independence international alignments shaped his early political decisions.',[1],'Evidence not found'),
    ('Theatre training and major film roles preceded office; collaboration with Karunanidhi connected entertainment and political communication. These channels predated later televised campaigning.',[23],'Material finding'),
    ('DMK membership from 1953 and later fan-network mobilisation supplied organisational settings. Early membership alone does not establish formal control of the party.',[1,5],'Material finding'),
    ('Limited schooling and family hardship form a documented background. They should not be converted into proof that his later electorate shared an identical social experience.',[1],'Research limitation'),
    ('Movement from Ceylon to Kumbakonam and work in Tamil cinema connected different places. Later chief-ministerial jurisdiction should not be projected onto childhood geography.',[1,23],'Material finding'),
    ('Institutional biographies are commemorative and compress chronology; cinema accounts contain political errors. Specific passages are used with caveats, while original Council records remain missing.',[1,23],'Research limitation')
    ],
    [
    ('The 1972 rupture created a competing party claiming Annadurai’s legacy. Rivalry with Karunanidhi operated within a shared Dravidian political field.',[2,23],'Material finding'),
    ('AIADMK supported the Emergency according to the university history, while the DMK government was dismissed in 1976. This alignment shaped the setting before MGR entered government.',[10,6],'Material finding'),
    ('Won St. Thomas Mount twice, in 1967 and 1971, under the DMK label. These constituency results should not be confused with later statewide AIADMK performance.',[17,18],'Material finding'),
    ('Financial-accountability demands were prominent in the split. They establish a political issue, but do not provide an independently verified economic programme for this phase.',[2,23],'Research limitation'),
    ('No inspected evidence connects international alignments to his decisions in this phase. Later Sri Lankan involvement cannot be projected onto party formation.',[2,9],'Evidence not found'),
    ('Shooting-related hospital imagery and films carried political meaning. Sympathy is described in biography; the size of its electoral effect is not measured.',[23,17],'Research limitation'),
    ('Fan clubs supplied a mobilisation base after the party split. Scholarship also treats prior DMK associations as part of the organisational background.',[5],'Material finding'),
    ('Scholarship describes a protective appeal to poorer supporters and women. A broad social-base interpretation is not a substitute for disaggregated voting data.',[5],'Research limitation'),
    ('St. Thomas Mount supplied a legislative base, while fan networks extended political reach beyond it. Local vote totals and statewide organisation measure different things.',[17,18,5],'Material finding'),
    ('1967 figures come from an identified ECI reproduction; 1971 uses a secondary table. Source arithmetic is checked, while original-return access remains a separate gap.',[17,18],'Research limitation')
    ],
    [
    ('AIADMK formed the state government and later joined the Charan Singh Union coalition through two MPs. In 1980 Congress instead allied with the DMK.',[10],'Material finding'),
    ('The first ministry ended with central dismissal and dissolution in February 1980. This interruption matters when comparing electoral durability with continuous executive tenure.',[6,10],'Material finding'),
    ('His 1977 Aruppukkottai victory differs from AIADMK’s 1980 parliamentary setback. Personal Assembly records and party-level Lok Sabha performance cannot be combined as one win-loss series.',[19,10],'Material finding'),
    ('The quota dispute concerned distribution of public educational and employment access. The inspected record does not quantify its wider growth, income or fiscal consequences.',[15],'Research limitation'),
    ('No distinct international-policy mechanism for the first ministry is established in the collected material. State office did not confer sovereign foreign-policy authority.',[10],'Evidence not found'),
    ('Film-derived credibility and fan networks preceded entry into government. Office added administrative responsibility; popularity alone does not demonstrate implementation quality.',[23,5,10],'Material finding'),
    ('Scholarship’s account of pressure over quotas shows constraints from organised constituencies. Founder leadership did not remove the need to respond to supporters.',[5,15],'Material finding'),
    ('The income-ceiling controversy exposed tensions between economic and caste-based targeting. Withdrawal and expanded quota are observable; the private balance of motives remains uncertain.',[15,5],'Material finding'),
    ('1977 seats followed delimitation based on the 1971 census; MGR moved from St. Thomas Mount to Aruppukkottai. Raw shares across them are not a like-for-like geographic series.',[6,17,19],'Material finding'),
    ('Ministry chronology is supported by an institutional compilation and legislative review. Quota interpretation still lacks inspected original orders, so date precision is restrained.',[10,6,15],'Research limitation')
    ],
    [
    ('Return in the 1980 state election followed a parliamentary defeat; by 1984 AIADMK allied with Congress. National and state competitions generated different coalition incentives.',[10],'Material finding'),
    ('The second ministry began 9 June 1980. University statutes and administration required collective state institutions; they cannot be reduced to an individual announcement.',[10,12,13],'Material finding'),
    ('Won Madurai West in 1980 and Andipatti in 1984. The latter victory occurred during hospitalisation; a sympathy explanation remains distinct from the recorded result.',[20,21,10],'Material finding'),
    ('Meals expanded direct public provision while TASMAC organised wholesale liquor trade. Revenue, service delivery and distribution were concurrent concerns; no fiscal causal model has been collected.',[3,25],'Research limitation'),
    ('Later inquiry testimony places Sri Lankan Tamil affairs within state and Union concerns, but the collected aid passage concerns 1987. Detailed 1980–84 involvement remains unreviewed.',[9],'Evidence not found'),
    ('Cinemaazi describes use of hospital video during the 1984 campaign. Images and illness formed part of communication; their independent contribution to the victory is unmeasured.',[23,10],'Research limitation'),
    ('Welfare administration required departments and workers alongside party organisation. The later evaluation warns that formal institutionalisation does not ensure transparent data or secure employment.',[3,4],'Material finding'),
    ('Meal eligibility widened across age groups, and a women’s university was created. Access provisions are documented; effects across gender, caste and class require more disaggregated evidence.',[4,13],'Research limitation'),
    ('The meal programme expanded from rural to urban areas. University creation in Thanjavur and Kodaikanal represents geographically distinct institutional choices, without proving equal statewide access.',[3,12,13],'Material finding'),
    ('District and university histories establish programme milestones. The 2004 assessment critiques data quality; later staff counts and current menus are not backdated to 1982–84.',[3,4,13],'Research limitation')
    ],
    [
    ('The Congress alliance provided the electoral setting for the final ministry; the founder’s death produced a contested succession rather than an automatic transfer of authority.',[10,2],'Material finding'),
    ('Council abolition changed the legislature; press privilege proceedings later drew a constitutional adverse ruling. Legal validity of one act does not validate another.',[7,6,8],'Material finding'),
    ('The December 1984 victory preceded the February 1985 ministry. No new MGR Assembly election occurred between that mandate and his death; posthumous party contests are separate.',[21,6],'Material finding'),
    ('1987 medical-university legislation and restrictions on arrack illustrate concurrent educational and revenue-policy choices. Their net economic effect is not established by existence alone.',[11,25],'Research limitation'),
    ('Sri Lankan ethnic conflict generated aid and contested links to militants. The inquiry records competing recipient accounts; humanitarian purpose, actual use and personal responsibility need separate evidence.',[9],'Material finding'),
    ('The cartoon privilege case exposed conflict between a publication and legislative authority. Release in 1987 and constitutional redress in 1994 were separate stages.',[6,8],'Material finding'),
    ('Succession competition between Janaki and Jayalalithaa after his death shows uncertainty around authority in a leader-centred organisation. It does not establish either claimant lacked independent support.',[2,10],'Research limitation'),
    ('Vanniyar mobilisation and caste clashes challenge a uniform account of social inclusion. The 1989 MBC policy came later; no original inquiry assigning each death is collected.',[16],'Research limitation'),
    ('State institutions addressed education and local policing while Sri Lankan assistance crossed territorial boundaries. Chief-ministerial influence and Union foreign-policy authority should remain distinct.',[11,16,9],'Material finding'),
    ('Court judgments, legislative review and a reproduced inquiry offer different standards of evidence. Official remembrance and later honours do not resolve contested historical responsibility.',[8,6,9,24,22],'Research limitation')
    ]]
    comparisons=[
    'Compare cinema figures and party entrants before 1967, using similar prominence and organisational experience.',
    'Compare legislators and party founders within the same Dravidian political field; electoral, cultural and organisational routes differed.',
    'Compare chief ministers under the same federal dismissal powers and distributional pressures, with contemporary opposition arguments visible.',
    'Compare contemporary state governments’ welfare delivery, budgets and institution-building; separate policy outputs from causal outcomes.',
    'Compare press oversight, legislative checks and social-conflict responses under contemporary institutions; context does not excuse rights violations.'
    ]
    for p,items in enumerate(era,1):
        assert len(items)==10
        for n,(finding,ids,disposition) in enumerate(items,1):
            add('Context & Constraints',f'E{p}{n:02d}',{'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],'Career phase':phases[p-1],'Research disposition':disposition,'Finding':finding,'Available choices / comparison':comparisons[p-1],'Presentism caution':'Interpret against period institutions and available evidence. Comparison is an analytical frame, not a measured causal result.'},ids,'Analysis',status='Not reviewed' if disposition=='Evidence not found' else 'Supported')
