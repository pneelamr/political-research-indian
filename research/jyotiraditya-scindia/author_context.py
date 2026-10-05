"""Career-specific gender and era coverage; uncertainty is explicit."""
coverage={
'Gender':['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
'Era':['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']}

def populate_context(add,phases):
    gender=[
('Family succession and Congress sponsorship are documented at entry. The collected sources do not isolate a male-gender effect from inherited networks, wealth or party selection.',[4], 'Material finding','Access pathway documented; gender causation unresolved.'),
('The2002 entry and later ministerial appointments are established milestones. No historically meaningful gender-first distinction is claimed for them.',[1], 'Research limitation','Compare equivalent male and female entrants only with evidence, not presumed novelty.'),
('The parliamentary biography lists association with Scindia Kanya Vidyalaya. An institutional connection with girls’ education does not alone establish policy leadership or beneficiaries’ outcomes.',[1], 'Material finding','Educational network; precise contribution requires institutional records.'),
('Economic and infrastructure portfolios recur. No inspected appointment evidence explains selection in terms of gender, so a gendered division of ministerial labour remains untested.',[1,5,7], 'Evidence not found','Portfolio chronology is evidence; motives require a separate comparison.'),
('Reports discuss family succession and the tone of constituency interactions. A systematic comparison of gendered media treatment was not located in this research.',[4,37,38], 'Evidence not found','No inference about appearance, marriage or gendered stereotypes from selective coverage.'),
('No reliable career-specific evidence of gender-based threats was located. General political conflict is insufficient to establish gender-specific intimidation or its absence.',[9,10], 'Evidence not found','Open evidence gap; candidate sources describe political conflict only.'),
('In2022 he advocated greater participation by women in aviation and a50% pilot aspiration. The event concerned professional pathways; it did not create a verified50% quota.',[29], 'Material finding','Ministerial advocacy; substantive implementation and effects remain separate.'),
('Public narratives connect him to Madhavrao and the Scindia family. That demonstrates political use of lineage; the collected material does not isolate a specifically masculine strategy.',[4,9], 'Material finding','Family identity is relevant; do not infer caste, religion or gender mechanism from surname.'),
('The stated15% women-pilot figure at the2022 event was a sector baseline, not an effect of his appointment. No evaluated causal gain from the aspiration is established here.',[29], 'Research limitation','Symbolic support differs from recruitment, retention, pay and leadership outcomes.'),
('Evidence is strongest for an aviation-sector intervention in2022. It cannot sustain a uniform assessment of gender policy across his earlier Congress and later Communications/DoNER roles.',[29,1,7,8], 'Research limitation','Career-wide assessment remains provisional; lack of collected evidence is not proof of inactivity.')]
    for n,(finding,ids,disp,mechanism) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],'Career phase':'Across five phases','Research disposition':disp,'Finding':finding,'Mechanism / interpretation':mechanism,'Presentism caution':'Use contemporary institutions and evidenced pathways; do not assume gender is decisive in every event.'},ids,'Analysis',status='Not reviewed' if disp=='Evidence not found' else 'Supported',note='Research gap, not a finding of no effect.' if disp=='Evidence not found' else 'Bounded reading of identified evidence.')
    era=[
# P1
[
('Congress entry linked constituency succession to national leadership. Parliamentary representation preceded junior executive office in2008.',[4,1],'Material finding'),
('Direct election and Union ministerial appointment were distinct routes. His first ministerial role was MoS, with authority within a larger departmental hierarchy.',[1],'Material finding'),
('The2002 by-election and2004 general election returned him from Guna. Historical counts have secondary support; checked popular-share denominators remain missing.',[14],'Research limitation'),
('Project Arrow addressed postal-service and technology modernisation within an established public network. Its later phased delivery extended beyond this ministerial tenure.',[19,2],'Material finding'),
('Foreign education is documented, but no direct evidence collected links international-system change to his political choices in this early phase.',[1,4],'Evidence not found'),
('Contemporaneous2001 reporting framed entry through family succession and Congress sponsorship. One article cannot represent the whole campaign-media environment.',[4],'Research limitation'),
('Sonia Gandhi formally admitted him and he publicly deferred to party seniors, illustrating national gatekeeping alongside a family constituency connection.',[4],'Material finding'),
('Family political capital is documented. The inspected evidence does not quantify caste, class, religious or gender composition of his early voters.',[4,14],'Research limitation'),
('Guna supplied the electoral route into a national legislature; his later postal role operated across India. Constituency influence and national executive authority are distinct.',[1,14],'Material finding'),
('Official biography supplies exact ministry dates, while historical constituency tables supply vote counts. The latter require primary-return reconciliation;2007/2008 ministry-year discrepancy is preserved.',[1,5,14],'Research limitation')],
# P2
[
('He remained a Congress MP during Commerce and Power service. Party membership, parliamentary mandate and portfolio responsibility overlap but are separately recorded.',[1,14],'Material finding'),
('Independent charge of Power fromOctober2012 increased departmental responsibility relative to a junior role; it did not change the office into Cabinet rank.',[1],'Material finding'),
('The2009 Guna win continued his parliamentary tenure. Comparison with earlier contests requires attention to constituency boundaries and denominator definitions.',[14],'Research limitation'),
('Export facilitation and interstate electricity transmission were central portfolio concerns. Grid integration was an institutional infrastructure project spanning earlier administrations.',[2,21,22],'Material finding'),
('The trade portfolio exposed him to cross-border commerce, but an inspected source linking global economic shocks to a particular decision remains missing.',[2,20],'Evidence not found'),
('Ministerial releases and parliamentary-committee presentations document public policy communication. They do not measure media reach or voter persuasion.',[21],'Research limitation'),
('His executive progression occurred within Congress-led government and parliamentary-party structures. A personal movement or separate party organisation is not evidenced in these records.',[1,2],'Research limitation'),
('Grid and postal/trade policies potentially affect diverse users, but distributional outcomes across communities are not established by the administrative milestones collected here.',[19,21,22],'Research limitation'),
('The grid milestone joined regional systems; national planning and technical institutions constrained individual discretion. A constituency-based mandate coexisted with nationwide responsibilities.',[21,22,14],'Material finding'),
('The synchronous-grid milestone is corroborated by a later ministry history. Export-cost savings appear in indexed parliamentary text only and are excluded from supported quantities.',[22,20],'Research limitation')],
# P3
[
('Congress opposition work included chief-whip and later western-UP organisational responsibilities. Electoral defeat and the2020 exit changed this relationship rather than merely changing a portfolio.',[2,16,9],'Material finding'),
('His2019 integration statement supported the policy direction while questioning process. As a defeated Lok Sabha candidate, this was a public statement, not a parliamentary vote in this record.',[13,16],'Material finding'),
('The2014 Guna win was followed by defeat in2019. His household’s political association with the seat did not guarantee continuing election.',[14,16],'Material finding'),
('He lacked Union executive control during this phase. Earlier Power/Commerce initiatives should not be extended across opposition years merely because his public profile remained national.',[1,2],'Research limitation'),
('No sufficiently direct source collected establishes how international events affected his opposition strategy. The J&K statement establishes a domestic political position, not a diplomatic role.',[13],'Evidence not found'),
('The2019 social-media statement allowed an issue-specific position to be publicised despite divergence from other Congress responses; influence on voters is unmeasured.',[13],'Material finding'),
('Chief-whip and AICC roles linked parliamentary coordination with geographic party organisation. Western-UP responsibility was a party assignment, not an elected seat there.',[2],'Material finding'),
('The Guna defeat invites analysis of local coalition change, but candidate totals alone cannot establish which social groups switched or why.',[16],'Research limitation'),
('His electoral base remained Guna while organisational responsibility extended to western Uttar Pradesh. These jurisdictions should not be collapsed into a single political base.',[2,16],'Material finding'),
('Institutional biographies identify roles; contemporary reports establish expressed positions and later rupture. Private motives and voter explanations remain inference unless independently studied.',[2,13,9],'Research limitation')],
# P4
[
('Joining BJP was followed by Rajya Sabha election and Cabinet service. In Madhya Pradesh, allied MLA departures preceded the fall of Congress’s government.',[9,10,18,5],'Material finding'),
('The2020 court decision separated a government’s confidence test from the Speaker’s resignation and disqualification powers. These constitutional processes cannot be reduced to a personal loyalty narrative.',[11],'Material finding'),
('Rajya Sabha election used an MLA electoral college. BJP and supporter outcomes in the2023 Assembly election are separate from his own indirect2020 result.',[18,12],'Material finding'),
('Aviation work combined divestment, subsidised regional connectivity and digitisation; steel used production incentives. These different instruments resist a single public-versus-private label.',[23,27,24,28],'Material finding'),
('Aviation and steel connect to international markets, but this study lacks an inspected source isolating external shocks in his portfolio outcomes. No foreign-policy leadership is inferred.',[23,28],'Evidence not found'),
('Facial-recognition services and consent complaints made digital infrastructure part of the public debate. Official assurances, media reports and independent privacy evaluation are different evidence types.',[24,25],'Material finding'),
('PTI’s nominated-supporter cohort had seven wins and six losses in2023. This shows mixed local performance, not a precise measure of faction size or control of the BJP.',[12],'Material finding'),
('Women’s aviation access entered ministerial advocacy. Sector representation statistics do not reveal barriers across income, training costs, region or caste without additional research.',[29],'Research limitation'),
('National ministerial work coexisted with Gwalior–Chambal campaigning. BJP’s18 of34 regional seats is a party tally and cannot all be causally credited to him.',[12,5],'Material finding'),
('Sources include official launches, independent reporting, a court judgment and CAG summary. Full audit replies remain unavailable; election-petition dismissal has a narrow legal scope.',[24,25,18,27],'Research limitation')],
# P5
[
('The2024 Guna victory returned him to directly elected Parliament as BJP candidate while he took new Union portfolios. This differs institutionally from his preceding Rajya Sabha route.',[17,7,8],'Material finding'),
('Communications minister, DoNER minister and NEC vice-chairman are related but distinct offices. NEC’s chairmanship remains separately listed under Amit Shah.',[3,43],'Material finding'),
('The2024 result table supports a540929 winning margin. Share comparison remains withheld because the inspected primary denominator is missing and indexed vintages differ.',[17,40],'Research limitation'),
('BSNL deployment, regional investment promotion and state-led project follow-through mix public infrastructure with private investment mobilisation. Reported activity is not yet an independent productivity or employment assessment.',[30,31,32],'Material finding'),
('International-market and border-region implications would merit study, but the collected investment releases do not establish realised cross-border economic or diplomatic effects.',[31,32],'Research limitation'),
('Sanchar Saathi criticism and the rapid mandate reversal show technology policy being contested publicly. The minister’s voluntary-use assurances are attributed positions, not a security audit.',[33,34,35,36],'Material finding'),
('Current work relies on ministry agencies, state governments and NEC task forces. Public ministerial prominence should not erase the distributed implementation structure.',[31,32,43],'Material finding'),
('The road-protest episode records a demand for local infrastructure and disagreement over political responsiveness. It provides no representative survey of Guna residents.',[37,38],'Research limitation'),
('DoNER and NEC coordinate development across Northeast states, while Guna remains his electoral constituency. State-level execution and other Union ministries mediate development results.',[31,32,17],'Material finding'),
('Recent data are chiefly ministry outputs and investment claims. Court follow-up, road completion and independent policy outcomes remain dated gaps; the cutoff does not imply all events are fully documented.',[30,32,18,37],'Research limitation')]
]
    for p,items in enumerate(era,1):
        assert len(items)==10
        for n,(finding,ids,disp) in enumerate(items,1):
            add('Context & Constraints',f'E{p}{n:02d}',{'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],'Career phase':phases[p-1],'Research disposition':disp,'Finding':finding,'Contemporary comparison group':'Same-era party colleagues, institutions and portfolio predecessors where evidence permits.','Presentism caution':'Interpret against the stated phase; later outcomes do not prove what was foreseeable at the time.'},ids,'Analysis',status='Not reviewed' if disp=='Evidence not found' or any(i in (20,40) for i in ids) else 'Supported',note='Candidate sources do not yet support a substantive causal finding.' if disp=='Evidence not found' else 'Context is limited to the cited career evidence; no general causal claim about the entire era.')
