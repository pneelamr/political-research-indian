"""Career-specific gender and era coverage, including explicit evidence gaps."""
coverage={
'Gender':['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
'Era':['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']}

def populate_context(add,phases):
    gender=[
('RSS, Jana Sangh, editorial work and parliamentary office are documented access routes. The collected evidence does not isolate how being a man affected access or advancement relative to comparable women.',[1,2,5],'Research limitation','Compare entry cohorts and organisational recruitment, not individual success alone.'),
('The record establishes senior party and governmental milestones, but no distinctive gender-first claim is warranted for Advani. His appointments should not be interpreted as evidence of equal access for women.',[1,2],'Research limitation','Institutional achievement and the distribution of opportunity are different questions.'),
('Cadre and party networks were central to his route. Their role is documented; the degree to which equivalent networks were available to women requires comparative organisational history.',[2,5],'Research limitation','Organisational access may structure opportunity; gender-specific effect remains unmeasured.'),
('Broadcasting, Home, Deputy PM and parliamentary leadership were his principal national roles. No inspected appointment record explains these allocations through gender, and stereotypes about masculine security leadership are not evidence.',[1,15,19],'Evidence not found','Compare actual selection records for contemporaneous ministers with similar seniority.'),
('Sources describe organisation, ideology, security and elder status. No systematic study collected compares gendered framing of Advani with female contemporaries; isolated leadership labels cannot establish a media pattern.',[29,31],'Evidence not found','Need a comparable media corpus, with period and office held constant.'),
('Emergency detention is documented, but it is not evidence of gender-targeted persecution. No collected record establishes a gender-specific threat mechanism affecting his career.',[2],'Evidence not found','Separate political repression, personal security and gender-targeted hostility.'),
('His December 1997 speech linked 33% reservation for women to more women candidates. A later UNDP/NDI study records the BJP’s 2008 organisational quota. Personal advocacy, party rules and achieved representation are separate.',[41,33],'Material finding','Commitment and formal rules are observable; implementation needs nomination and leadership data.'),
('In the 1997 address, women’s representation formed part of a broader candidate-selection and national-development argument. The evidence supports this political use of representation, not an assumption that women voters responded uniformly.',[41],'Material finding','Analyse rhetoric, candidate selection and electoral reception separately.'),
('No collected evaluation establishes that his advocacy caused more women to win nominations, exercise authority or receive material benefits. The party quota report itself distinguishes formal inclusion from meaningful participation.',[33,41],'Research limitation','Separate descriptive representation, substantive action and causal effect.'),
('Coverage spans formation, reservation advocacy, gendered needs raised in the Gujarat relief debate and later party rules. These permit specific questions, but not a single career-wide empowerment score.',[2,41,35,33],'Research limitation','Assess documented choices by period; do not convert missing evidence into a finding of no effect.')]
    for n,(finding,ids,disp,mech) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],'Career phase':'Across five phases','Research disposition':disp,'Finding':finding,'Mechanism / interpretation':mech,'Contemporary comparison group':'Men and women with comparable party seniority, electoral route and office; no matched causal study collected.','Presentism caution':'Identify documented gender mechanisms; do not infer motives, advantage or disadvantage from sex alone.'},ids,'Analysis',status='Not reviewed' if disp=='Evidence not found' else 'Supported')
    era=[
    [
    ('Jana Sangh organisation and later Janata office place him within opposition-party consolidation. Party change created access to government without erasing earlier ideological and cadre connections.',[1,2],'Material finding'),
    ('Metropolitan membership, Rajya Sabha election, Emergency detention and Cabinet appointment involved very different institutional powers and vulnerabilities. Detention constrained ordinary opposition activity.',[1,2],'Material finding'),
    ('Upper House terms began in 1970 and 1976; they were indirect routes. These cannot be counted as personal Lok Sabha victories or evidence of a constituency vote share.',[1],'Material finding'),
    ('No inspected period-specific material establishes how economic conditions shaped his early organisational or broadcasting choices. Holding a ministry does not supply a documented economic programme.',[1,2],'Evidence not found'),
    ('Partition migration is documented, but no collected study isolates the effects of Cold War alignments on his early decisions. Later national-security positions should not be projected backwards.',[5],'Evidence not found'),
    ('Organiser work and later I&B responsibility placed him on both the party-communication and governmental sides of media. The 1979 bill differed from the Verghese group’s proposed autonomy.',[5,1,17],'Material finding'),
    ('RSS and Jana Sangh recruitment, state work and Delhi leadership supplied a durable organisational route. The sources support these affiliations, not a quantified model of promotion.',[2,5],'Research limitation'),
    ('Partition migration and relocation from Sindh to Rajasthan/Delhi are evidenced formative conditions. They do not justify inferring the voting preferences of all Sindhi or displaced communities.',[2,5],'Research limitation'),
    ('Delhi Metropolitan Council service belonged to an earlier metropolitan institutional structure. It must not be recast as service in the later Delhi Assembly or as chief minister.',[1],'Material finding'),
    ('Parliamentary summaries and party biography verify broad offices; they conflict or compress some boundaries. The party page also has stale current-office wording, so exact dates require notifications.',[1,2],'Research limitation')
    ],
    [
    ('BJP organisation, Palampur endorsement and the temple campaign expanded the arenas in which Advani operated. Retrospective assessments credit organisation while contesting the social consequences of mobilisation.',[2,5,29],'Material finding'),
    ('The period combined parliamentary leadership, support withdrawal from V. P. Singh, state intervention against the yatra and legal scrutiny after the demolition and hawala allegations. Movement leadership did not remove institutional constraints.',[5,12,39],'Material finding'),
    ('New Delhi and Gandhinagar victories in 1991 were two contests in one general election, not two successive Lok Sabha terms. The narrow New Delhi margin warns against inferring identical support across constituencies.',[7,1],'Material finding'),
    ('The December 1997 speech placed basic services, decentralisation and social needs alongside economic debate about markets and domestic industry. This is a documented agenda, not proof of achieved economic outcomes.',[41],'Material finding'),
    ('No sufficiently specific source collected links the end of the Cold War to Advani’s individual strategic choices. A broad global transition is not used as an automatic explanation of BJP growth.',[41],'Evidence not found'),
    ('The Rath Yatra used a public journey and religious geography to secure national attention. Editorial and retrospective accounts show political salience but do not quantify persuasion or media effects.',[5,29],'Research limitation'),
    ('Repeated BJP presidencies and general-secretary service show organisational authority. His 1997 address also reveals campaign planning and a declared wish to broaden candidate selection.',[1,2,41],'Material finding'),
    ('Mandal and Ayodhya politics formed the setting of the 1990 mobilisation. The sources do not establish a constituency-level caste or religious vote decomposition, nor that one issue wholly displaced the other.',[5],'Research limitation'),
    ('His direct electoral geography shifted between New Delhi and Gandhinagar. Different electorate sizes and boundaries make raw vote totals unsuitable as a national popularity index.',[6,7],'Material finding'),
    ('Official 1989/1991 returns and a primary 1997 speech are stronger on votes and declared strategy than later profiles are on exact dates or motives. Judicial conclusions use the separate court record.',[6,7,41,11],'Research limitation')
    ],
    [
    ('The NDA operated through a coalition; Advani’s later speech explicitly distinguishes coalition priorities from continuing BJP ideological commitments. This limits claims of unconstrained ministerial or party control.',[41],'Material finding'),
    ('POTA’s joint sitting and the Gujarat relief debate expose parliamentary procedure, opposition scrutiny and centre–state questions. Advani acknowledged Election Commission authority over election arrangements.',[16,35],'Material finding'),
    ('Gandhinagar victories in 1998, 1999 and 2004 establish continued personal election success; the 2004 national defeat shows that local victory and formation of a Union government are separate outcomes.',[8,9,10,41],'Material finding'),
    ('Police-modernisation outlays and disaster-preparedness programmes are observable administrative inputs. No inspected audit isolates Advani’s contribution to productivity, fiscal efficiency or security outcomes.',[15],'Research limitation'),
    ('The Parliament attack and post-9/11 setting appear in his POTA justification; Kandahar and Hurriyat talks presented different combinations of coercion, negotiation and cross-border security concerns.',[16,15,22],'Material finding'),
    ('Parliamentary speeches preserve competing contemporary arguments; ministry reports promote and document departmental action. Later memoirs reconstruct crises from interested personal perspectives.',[16,35,15,22],'Research limitation'),
    ('Home leadership and the Deputy PM appointment increased formal responsibility within Vajpayee’s government. Coalition partners and opposition parties could contest choices, as the Gujarat debate demonstrates.',[19,35,36],'Material finding'),
    ('Gujarat relief debate included women’s safety and fears about returning home; identity-card and citizenship programmes raised membership and documentation questions. Neither source supplies a complete distributional-impact study.',[35,15],'Research limitation'),
    ('Reorganisation legislation and state police funding involved shared central, state and parliamentary powers. Regional movements and state institutions must remain visible alongside the sponsoring minister.',[24,25,15],'Material finding'),
    ('Ministry reports establish dates and reported outputs; independent impact evaluation is weak. The national-security review and exact 1998 appointment remain located-but-unread primary leads.',[15,18,37],'Research limitation')
    ],
    [
    ('The 2004 defeat returned him to opposition and party presidency. His own post-election address recognised miscalculation; the 2009 result again separated national ambition from local election success.',[41,28,10],'Material finding'),
    ('Opposition leadership offered parliamentary scrutiny without executive command. POTA repeal by the later government demonstrates the institutional reversibility of a major legislative initiative.',[1,23],'Material finding'),
    ('Won Gandhinagar in 2009 while the Advani-led BJP won 116 seats against Congress’s 206. The party result cannot be entered as a personal constituency defeat.',[10,28],'Material finding'),
    ('IPU records tax reductions among 2009 campaign proposals; his 2004 speech combined deregulation with social justice and ecological restraint. These establish positions, not implementation in opposition.',[28,41],'Material finding'),
    ('The Pakistan visit and Jinnah remarks had a domestic organisational consequence. Scholarship connects the dispute to tensions between coalition expansion and ideological expectations.',[20],'Material finding'),
    ('Party speeches, interviews and reporting became important evidence of self-interpretation and succession debate. The 2009 Jaswant interview is a participant account after expulsion, not a neutral Cabinet transcript.',[41,21,27],'Research limitation'),
    ('RSS intervention in the 2013 resignation and criticism over Jinnah illustrate organisational constraints on an individual party leader. Resignation, accommodation and succession were observable choices.',[20,27],'Material finding'),
    ('The BJP’s 2008 internal women’s quota changed formal organisational rules, while an IPU account records women’s parliamentary representation. Neither establishes Advani’s personal causal contribution.',[33,28],'Research limitation'),
    ('Gandhinagar remained his electoral base, but parliamentary opposition and the national campaign involved much broader constituencies. Boundary-adjusted comparison and voter studies are not collected.',[1,10,28],'Research limitation'),
    ('A primary speech and external scholarly country review complement contemporary news. Full commission and court records remain distinct missing pieces; multiple reproductions of Liberhan are one origin.',[41,20,14,40],'Research limitation')
    ],
    [
    ('Later accounts place Advani in an elder/advisory role while newer BJP leadership held executive power. Bharat Ratna records official recognition, not restored operational control.',[31,3,4],'Material finding'),
    ('Criminal acquittal, an appeal dismissed for standing and national honours operate under different procedures. They should not be collapsed into a single institutional verdict on a political career.',[12,13,3],'Material finding'),
    ('His final verified personal contest was Gandhinagar in 2014; the BJP nominated Amit Shah there in 2019. Later BJP victories are not additional Advani election wins.',[1,10,26],'Material finding'),
    ('No inspected material establishes a distinct economic programme under Advani’s authority in this phase. Earlier ministerial work cannot be credited with every later policy bearing a related theme.',[1,26],'Evidence not found'),
    ('No specific formal diplomatic role is established by the collected sources for this phase. A career assessment should not infer one from his earlier Pakistan visit or seniority.',[1,20,31],'Evidence not found'),
    ('The April 2019 blog states democratic principles in a public written format, while later commentary reinterprets earlier leadership. Present-day reception and the original historical record are different evidence types.',[26,29,31],'Material finding'),
    ('Scholarly commentary interprets the mentor role and public honour through party unity despite succession conflict. This is an attributed interpretation, not proof of ongoing influence over nominations or policy.',[31,27],'Research limitation'),
    ('Legacy debate weighs national party-building against communal polarisation and the Ayodhya movement. A 2024 honour does not establish social consensus or resolve minority experiences of earlier mobilisation.',[29,30,3],'Research limitation'),
    ('The 2014 vote-share denominator includes NOTA, unlike the earlier valid-candidate denominators used here. Historical constituency boundary changes also limit like-for-like comparisons of vote shares.',[10,6,7],'Research limitation'),
    ('Official award records are directly inspected; legal outcomes use identified reporting. Current-status updates include reported electoral-roll verification in September and hospital discharge on 19 October 2026; neither permits inferences about subsequent events.',[3,4,12,13,43,42],'Research limitation')
    ]]
    comparisons=[
    'Compare contemporary Jana Sangh/Janata organisers, metropolitan representatives and Upper House entrants. Organisation, journalism, elected service and coalition participation offered different routes.',
    'Compare BJP organisers and other national opposition leaders under the same electoral institutions. Available choices included parliamentary work, mass mobilisation, alliances and legal defence.',
    'Compare Home Ministers in coalition governments facing security crises and centre–state constraints. Legislation, policing, negotiation and oversight were distinct available instruments.',
    'Compare opposition leaders after electoral defeat and party presidents managing ideological networks. Campaign revision, accommodation and resignation were observable alternatives.',
    'Compare senior leaders moving from operational leadership to advisory status. Public statements, parliamentary service, honours and actual decision authority require separate evidence.'
    ]
    for p,items in enumerate(era,1):
        assert len(items)==10
        for n,(finding,ids,disp) in enumerate(items,1):
            # Source access gaps themselves are supported by the inspected retrieval log,
            # while concrete uninspected historical claims stay pending elsewhere.
            checked_ids=[s for s in ids if s not in (18,37)]
            add('Context & Constraints',f'E{p}{n:02d}',{'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],'Career phase':phases[p-1],'Research disposition':disp,'Finding':finding,'Available choices / comparison':comparisons[p-1],'Presentism caution':'Use period-specific institutions and feasible alternatives; context neither excuses conduct nor proves causation. The comparison frame is analytical, not a measured causal result.'},ids,'Analysis',checked={'Finding':checked_ids},status='Not reviewed' if disp=='Evidence not found' else 'Supported')
