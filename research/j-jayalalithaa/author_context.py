"""Required gender and phase-specific era coverage with explicit gaps."""
coverage={
'Gender':['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
'Era':['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']}
def populate_context(add,phases):
    gender=[
    ('Cinema and MGR mentorship opened access; campaigning and succession conflict were additional steps to leadership. Editorial accounts identify patriarchal barriers, without measuring their separate causal weight.',[4,5],'Material finding','Compare other cinema-linked aspirants within AIADMK, including men with senior party positions.'),
    ('First woman opposition leader in 1989. Janaki’s 1988 chief-ministership rules out calling Jayalalithaa the state’s first woman CM.',[1,2],'Material finding','Separate a gender milestone from a generic claim to being first.'),
    ('MGR’s patronage, Janaki’s family-based succession claim and Jayalalithaa’s own campaigning supplied different pathways. Sasikala’s later influence requires separate scrutiny from recruitment.',[4,5],'Material finding','Network access and independent organisational work can coexist; neither proves automatic succession.'),
    ('She attained broad chief-ministerial power, rather than being confined to a welfare role. The collected material does not establish how gender shaped allocation of portfolios to other women.',[2,3],'Research limitation','Formal authority is observable; gender-based selection motives require comparative cabinet and party records.'),
    ('An editorial explicitly interprets her career through patriarchal cinema and political institutions. A matched sample of media treatment of male and female rivals has not been assembled.',[5],'Research limitation','Attribute the interpretation; do not infer an identical gender mechanism behind every adverse report.'),
    ('The 1989 Assembly violence and her specific disrobing allegation had gendered political meaning; the allegation’s details remain contested. No comprehensive threat/security record was collected.',[22],'Material finding','Distinguish violence, allegation, denial, later recollection and protective arrangements.'),
    ('Cradle protection, women’s canteen employment and marriage-assistance rules provide substantive policy pathways. They do not by themselves establish improved autonomy or equality.',[11,12,43],'Material finding','Assess access, quality, institutional effects and outcomes separately; women are not a homogeneous beneficiary group.'),
    ('The maternal “Amma” image connected leadership with provision. It is an attributed strategy of representation, not evidence that voters lacked agency.',[5,12],'Material finding','Compare MGR’s protective image and DMK’s welfare competition in the same state setting.'),
    ('2016 post-poll analysis found a female voting advantage for AIADMK. Descriptive leadership, voter identification and redistribution are distinct from women’s authority within the party.',[38],'Material finding','Survey association does not identify which policy or identity cue caused the gender gap.'),
    ('Contemporary electoral analysis, the 2010 cradle study and later recollections of 1989 produce different kinds of assessment. None should become a timeless empowerment or victimhood label.',[38,11,22],'Material finding','Identify observer, period and evidence; retrospective testimony is not identical to contemporary observation.')]
    for n,(finding,ids,disposition,mechanism) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],'Career phase':'Across four phases','Research disposition':disposition,'Finding':finding,'Mechanism / interpretation':mechanism,'Contemporary comparison group':'AIADMK/DMK leaders, women and men in Tamil cinema and Tamil Nadu state politics of the same period.','Presentism caution':'Apply the same relevance test to personal lives; symbolic representation does not establish substantive equality.'},ids,'Analysis')
    era=[
    [
    ('Political entry occurred within MGR-led AIADMK; his death exposed a disputed succession rather than an automatically inherited office.',[4,5],'Material finding'),
    ('Rajya Sabha membership gave an institutional platform before Assembly leadership. State executive power and party position were separate routes.',[3,4],'Material finding'),
    ('1984 entry was an indirect parliamentary election; it must not be counted as a constituency popular-vote victory.',[1,3],'Material finding'),
    ('No inspected period study isolates how the changing economy affected her childhood, film work or early political choices.',[1,4],'Evidence not found'),
    ('No inspected evidence establishes a decisive international-system influence on her early choices. Later Sri Lankan positions must not be projected backwards.',[4,33],'Evidence not found'),
    ('Cinema visibility preceded party rallies and campaigning during MGR’s illness. Later television and digital assumptions cannot be applied to this entire phase.',[4],'Material finding'),
    ('Propaganda work and MGR’s patronage supplied organisational access; the later split demonstrates limits to uncontested authority.',[4,5],'Material finding'),
    ('Sources describe a Brahmin background and a female cinema-to-politics pathway within Dravidian politics. Identity alone does not explain party recruitment or voter acceptance.',[4,5],'Material finding'),
    ('Movement between Mysore, Bengaluru and Chennai preceded a Tamil Nadu political career. Historical birthplace and later constituency are different geographies.',[1,3],'Material finding'),
    ('Commemorative biographies compress offices and retrospective reporting contains chronology errors. Precise office registers and Tamil-language archives remain priorities.',[1,3,4],'Research limitation')
    ],
    [
    ('Leadership was consolidated through competition with the Janaki faction and DMK; first government followed the 1991 victory, then personal defeat in 1996.',[4,24,25],'Material finding'),
    ('Opposition leadership, Assembly confrontation and reservation legislation show the importance of legislative and Union institutions, alongside executive power.',[1,22,16],'Material finding'),
    ('Won Bodinayakkanur in 1989 and two seats in 1991, then lost Bargur in 1996. Seat-level records must remain separate from statewide mandate.',[23,24,25],'Material finding'),
    ('Welfare and procurement institutions expanded. A period-specific analysis linking liberalisation, state finances and her policy choices is not yet collected.',[11,36],'Research limitation'),
    ('A source-based account of how the post-Cold War and Sri Lankan conflict settings affected the first government remains incomplete.',[4,33],'Evidence not found'),
    ('The 1989 clash circulated through news reporting and later political memory. Contemporary reports and later witnesses differ over specific actions.',[22],'Material finding'),
    ('Her post-MGR leadership became increasingly centralised in journalistic accounts, while networks around Sasikala drew scrutiny.',[4,5],'Material finding'),
    ('Female-infanticide concern and reservation politics identify distinct gender and caste-policy pressures; neither policy alone measures equality.',[11,16],'Material finding'),
    ('Bargur and Kangayam victories show multiple electoral bases. Parliament’s role in quota protection demonstrates Centre-state interdependence.',[24,16],'Material finding'),
    ('Original election PDFs could not be read; secondary tables preserve counts with known transcription defects. Long-term policy evaluation requires other evidence.',[23,24,25,11],'Research limitation')
    ],
    [
    ('Regional-party leverage in the national coalition is directly visible in the 1999 withdrawal; state office resumed in 2001 and again in 2002.',[19,2],'Material finding'),
    ('Courts invalidated the 2001 appointment, sustained TANSI acquittal and considered mass employee dismissals: majority support did not remove institutional constraints.',[6,7,9],'Material finding'),
    ('Rejected 2001 nominations differ from the 2002 by-election win and 2006 Assembly victory. Legislative office and chief-ministerial appointment followed different rules.',[6,26,27],'Material finding'),
    ('Drought-related harvesting requirements and employee-strike policy illustrate resource and labour choices. A comparable fiscal series remains uncollected.',[14,15,9],'Research limitation'),
    ('The current evidence does not map her positions across the Sri Lankan war and global economic changes in this entire period.',[33],'Evidence not found'),
    ('Contemporary coalition reporting and later water-policy reporting provide different evidence windows. A systematic television/campaign archive has not been inspected.',[19,14],'Research limitation'),
    ('Party influence survived disqualification and absence from executive office. Coalition withdrawal and the subsequent electoral return show distinct uses of organisational authority.',[19,6,26],'Material finding'),
    ('The employee conflict and the revived cradle programme affected different constituencies. Neither identifies a uniform social response to her government.',[9,11],'Material finding'),
    ('Andipatti supplied a legislative base; Delhi coalition bargaining operated beyond state borders. The 2006 victory did not itself mean retention of government.',[26,27,19,2],'Material finding'),
    ('Judicial texts offer strong procedural evidence, while by-election reports disagree on totals. Review of legal holdings does not validate every reported political motive.',[6,7,9,26],'Research limitation')
    ],
    [
    ('Returned in 2011 and retained government in 2016; DMK remained a major rival. Vote distribution, alliances and gendered support complicate a single-cause explanation.',[2,38,40],'Material finding'),
    ('Assets litigation interrupted office; welfare litigation and interstate-water adjudication separately constrained government action.',[8,39,43,21],'Material finding'),
    ('Srirangam in 2011 and RK Nagar in 2015–16 were distinct contests. The 2015 opposition boycott limits comparison of margins and shares.',[28,29,39,42],'Material finding'),
    ('Vision 2023 combined infrastructure ambitions with a welfare-expansion period. Planned growth and the cost or effectiveness of benefits require independent evaluation.',[37,12,43],'Material finding'),
    ('Postwar Sri Lankan Tamil claims entered state politics through the 2013 resolution; implementation depended on Union and international institutions.',[33],'Material finding'),
    ('Video-conference canteen openings and personalised scheme branding linked administration and public communication. Digital-campaign effects are not measured here.',[12,5],'Material finding'),
    ('The Amma identity personalised party leadership and public provision. Editorial criticism of a weak second rank is an attributed institutional assessment.',[5,12],'Material finding'),
    ('Post-poll research found stronger female support across several groups; urban flood exposure and region also shaped reporting on the result.',[38,40],'Material finding'),
    ('Canteens operated through municipal institutions; water litigation joined two states. Neither statewide leadership nor local delivery was institutionally self-contained.',[12,13,21],'Material finding'),
    ('Born-digital plans, court judgments and surveys are relatively accessible; failed official links and limited posthumous inquiry access still constrain reconstruction.',[37,8,38,10,34],'Research limitation')
    ]]
    comparisons=[
    'MGR, Janaki, other AIADMK organisers and cinema-linked aspirants before the 1989 settlement.',
    'Karunanidhi, Janaki-faction leaders, state ministers and other regional parties operating under the same institutions.',
    'DMK and AIADMK governments, other coalition partners and public employees facing contemporaneous service rules.',
    'DMK and AIADMK programmes, municipal implementers and other states litigating interstate water disputes.'
    ]
    cautions=[
    'Differentiate childhood, film work and political entry within this long formation phase; do not project later persona or policy backwards.',
    'Interpret the existing quota and infant-protection debate within contemporary institutions; later acclaim is not contemporaneous outcome evidence.',
    'Use the law and coalition conditions then in force; later acquittal does not retrospectively validate a disqualified appointment.',
    'Evaluate proposals against the information and alternatives available then; do not assign post-2016 implementation to her.'
    ]
    for p,rows in enumerate(era):
        for n,(finding,ids,disposition) in enumerate(rows,1):
            ck={'Finding':[s for s in ids if s not in (10,34)]} if p==3 and n==10 else None
            add('Context & Constraints',f'E{p+1}{n:02d}',{'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],'Finding':finding,'Research disposition':disposition,'Contemporary comparison group':comparisons[p],'Presentism caution':cautions[p],'Feasible alternatives / scope':'Compare legislative negotiation, administrative implementation, litigation and electoral opposition as distinct available instruments; private motives are not inferred.'},ids,'Analysis',phases[p],checked=ck,status='Not reviewed' if disposition=='Evidence not found' else 'Supported')
