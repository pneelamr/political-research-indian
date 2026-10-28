"""Context coverage, with evidence gaps distinguished from negative findings."""
coverage = {
 'Gender': ['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
 'Era': ['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']
}

def populate_context(add, phases):
    gender = [
      ('Congress candidacy, ministerial appointment and TDP organisation supplied documented entry routes. Whether gender affected access relative to contemporary women has not been established.',[4,2],'Research limitation'),
      ('No substantiated gender-related first was located in the inspected profiles. Repeated CM terms establish seniority, not by themselves a gender milestone; this is a bounded search result.',[2,4,8],'Evidence not found'),
      ('The marriage connection to NTR and organisational work are politically relevant pathways. Apply the same scrutiny to male leaders as to women; kinship does not establish that every appointment resulted from family influence.',[4,5],'Material finding'),
      ('His assignments included Finance and Revenue, party organisation and executive leadership. Evidence comparing gender expectations in portfolio allocation was not collected.',[2,4],'Research limitation'),
      ('Managerial and reform-promoter framing appears in the scholarship and contemporary profile. A matched study of gendered media treatment, stereotypes or appearance commentary remains missing.',[17,4],'Research limitation'),
      ('The Alipiri attack is a security-research lead, but the full official passage was inaccessible. No inspected evidence establishes a gender-specific motive; neither an absence of threat nor a gender explanation is inferred.',[41],'Evidence not found'),
      ('Women’s self-help groups, school assistance delivered through mothers and free bus travel are documented mechanisms. Administrative coverage, service availability and substantive empowerment are separate measures.',[17,18,34,35],'Material finding'),
      ('At the free-bus launch Naidu used elder-brother language to describe his relationship to women beneficiaries. This is documented political positioning; how women received it requires separate evidence.',[34],'Material finding'),
      ('Programmes address women as beneficiaries and mothers. Those mechanisms do not demonstrate equal authority in TDP, women’s control over household resources, or a measured reduction in gender inequality.',[18,34,35],'Material finding'),
      ('Evidence ranges from reform-era scholarship and a successor-government budget to recent launch reports. Longitudinal feminist assessment and independent gender-impact studies remain a research gap.',[17,18,34,35],'Research limitation')
    ]
    for n,(finding,ids,disposition) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{
          'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],
          'Research disposition':disposition,'Finding':finding,
          'Contemporary comparison group':'Leaders and women organisers in the same party, offices and Andhra Pradesh electoral periods; no matched dataset assembled.',
          'Presentism caution':'Use the same relevance threshold for male and female politicians. Benefits directed to women do not establish their autonomous influence.',
          'Evidence-environment limitation':'English-language source sample; no inference of absence from an unlocated record.'
        },ids,'Analysis',phase='Across the six phases',status='Supported' if disposition=='Material finding' else 'Not reviewed')

    # Each tuple gives an independently reviewable finding, candidate evidence and disposition.
    material='Material finding'; limit='Research limitation'; missing='Evidence not found'
    eras = [
      [
       ('Career began in Congress(I), followed by TDP entry after the 1983 defeat. The 1984 NTR restoration campaign and party organisation changed his route to influence.',[4],material),
       ('He moved between elected office, ministerial appointment and party responsibilities. These selection mechanisms should not be treated as interchangeable popular mandates.',[2,4],material),
       ('Chandragiri contests in 1978 and 1983 preceded Kuppam victories in 1989 and 1994. Counts for the two Chandragiri contests are unavailable in this research.',[4,9,13],material),
       ('Finance and Revenue responsibilities are documented in 1994–95; a phase-specific fiscal or occupational-background study before his CM tenure was not obtained.',[2,4],limit),
       ('No inspected source establishes a direct international-system mechanism in his early recruitment or advancement. A national Cold War label alone would not explain this career phase.',[4],missing),
       ('The retrospective career account documents organisational campaigning, but comparative evidence on contemporary print, cinema and broadcasting influence was not collected.',[4],limit),
       ('TDP general-secretary work and the NTR restoration campaign preceded the deputy legislative-leader role. Family connection and organisational performance were overlapping pathways.',[4,2],material),
       ('Family networks and the shift from Chandragiri to Kuppam are documented. Reliable evidence for a caste-specific mechanism in nomination or voting remains uncollected; surname is not evidence.',[4,13],limit),
       ('The Chandragiri and early Kuppam contests were in undivided Andhra Pradesh. Later successor-state boundaries must not be projected onto those election returns.',[9,42],material),
       ('Coverage depends on a later biographical account, official profiles and the 1994 return. Original 1978, 1983 and 1989 returns and Telugu archives would improve precision.',[4,9,13],limit)
      ],
      [
       ('Naidu’s leadership followed the 1995 TDP revolt. United Front coordination in 1996 and BJP alignment in 1999 placed state politics within national coalition bargaining.',[4,5],material),
       ('The 1995 succession involved rival party claims and a legislative floor majority. The 2000 firing litigation illustrates judicial scrutiny of executive policing, without establishing a personal firing order.',[5,26],material),
       ('He retained Kuppam in 1999 and 2004; personal returns and the 2004 government defeat measure different levels of support. These are pre-delimitation constituency records.',[10,11,17],material),
       ('Fiscal reform, investment promotion, digital service delivery and Vision 2020 formed a managerial programme. Mooij describes uneven implementation and contests simple explanations of electoral defeat.',[17],material),
       ('The reform agenda engaged global development ideas and external finance as discussed by Mooij. This supports a globalisation context, not a claim that foreign institutions dictated every policy.',[17],material),
       ('Mooij examines deliberate promotion of the reform agenda; the 2003 profile reproduces a prominent managerial image. A comparative audit of television and newspaper coverage is absent.',[17,4],material),
       ('Janmabhoomi and stakeholder groups created channels alongside party structures and elected local bodies. Scholarship and the successor budget question their relationships to cadre and panchayats.',[17,18],material),
       ('Mooij places class change and distribution at the centre of reform politics. Women’s groups and tariff protesters should be studied as differentiated constituencies, not one uniform electorate.',[17,18,26],material),
       ('This government administered undivided Andhra Pradesh. Janmabhoomi’s relationship to local bodies is a distinct institutional question from later Andhra–Telangana division.',[17,18,42],material),
       ('Contemporary reporting, an official court record, a successor’s budget and retrospective scholarship offer different vantage points. Partisan criticism and academic explanation remain attributed.',[4,17,18,26],material)
      ],
      [
       ('TDP operated in opposition after 2004; in 2009 it joined TRS and the Left against Congress. An electoral coalition did not resolve all differences concerning statehood.',[2,39,42],material),
       ('Opposition leadership supplied legislative and party platforms without control of the state executive. Office records do not measure actual influence on government decisions.',[2],material),
       ('The 2009 Kuppam return belongs to the post-delimitation constituency framework. Comparing its share with 1999 or 2004 requires adjustment for boundaries and the voter base.',[10,11,12],material),
       ('The incoming Congress budget criticised the earlier development model and described welfare priorities. A full comparative fiscal assessment of the opposition decade has not been assembled.',[18],limit),
       ('No inspected source directly links international shocks or alignments to Naidu’s opposition strategy in this phase. A national macroeconomic chronology would be context, not personal causation.',[39],missing),
       ('The 2009 alliance is documented in contemporaneous reporting. Telugu media, campaign speeches and the 2012–13 padayatra require dedicated archival coverage.',[39],limit),
       ('The TDP–TRS–Left alliance combined distinct party organisations for the 2009 election. Constituency-level coordination and the later padayatra remain less well documented here.',[39],material),
       ('The alliance with TRS and the subsequent reorganisation make regional identity relevant. This evidence does not establish uniform preferences among Telangana or Andhra voters.',[39,42],material),
       ('The phase began within undivided Andhra Pradesh and ended with the 2014 reorganisation framework. Capital and territorial arrangements changed the setting for his next government.',[42],material),
       ('The official 2009 election return is stronger on counted votes than the collected reporting is on day-to-day opposition organisation. Regional-language and movement archives remain gaps.',[12,39],limit)
      ],
      [
       ('Naidu governed successor Andhra Pradesh in alliance with BJP before TDP left NDA in March 2018. Special-category status and reorganisation promises were stated reasons; BJP disputed the criticism.',[2,32],material),
       ('A state government could propose and administer capital development while relying on Union arrangements and external finance. It could not alone deliver every requested national concession.',[20,32,42],material),
       ('The 2014 Kuppam victory is distinct from the mandate to govern the new state. Vote counts here rely on a labelled secondary compilation; no unsupported share is supplied.',[13],material),
       ('Capital construction, land pooling and farm-debt relief combined investment promotion with redistribution. Announcements and design are better documented here than final fiscal and livelihood effects.',[20,22],material),
       ('The Amaravati proposal sought World Bank financing and encountered an accountability process. Lender involvement demonstrates an international institutional channel, not endorsement of every state action.',[20],material),
       ('Capital and special-status demands were communicated through news and official advocacy. A matched study of media ownership, Telugu coverage and campaign messaging remains unavailable.',[20,32],limit),
       ('TDP used both state-government authority and a national alliance; withdrawal changed that relationship in 2018. The later Congress alliance and local cadre adaptations need further documentation.',[32],material),
       ('Capital-region landowners and landless workers faced different arrangements and livelihood risks. Land-pooling participation cannot be used as a proxy for unanimous public consent.',[19,20],material),
       ('The 2014 division created successor Andhra Pradesh and a time-limited common-capital arrangement. Amaravati planning must be evaluated within that changed geography.',[20,42],material),
       ('The 2024 World Bank appraisal retrospectively documents the earlier programme and complaints. It is an interested institutional account; contemporaneous land records and independent fieldwork would strengthen assessment.',[20],material)
      ],
      [
       ('YSRCP won 151 Assembly seats in 2019 and TDP 23, placing Naidu in opposition. The scale of party defeat differs from his retained Kuppam seat.',[14,16],material),
       ('The skill-development prosecution brought arrest and judicial review into opposition politics. The 2024 split Supreme Court ruling concerned procedural protection; it was not a conviction or trial acquittal.',[23,24,25],material),
       ('Naidu retained Kuppam in 2019 by a reported 30,722 votes. Personal continuity did not imply statewide majority support or uninterrupted executive office.',[14,16],material),
       ('The World Bank records withdrawal of India’s earlier Amaravati financing request in July 2019. Responsibility for later state policy should not be assigned to an opposition leader merely because he initiated the capital project.',[20],material),
       ('The end of the earlier Bank-financing process is a documented international institutional event. Evidence of Naidu’s other international activity during opposition is not established in this sample.',[20],material),
       ('The arrest and litigation generated competing political accounts. A systematic assessment of social media, partisan outlets or changes in voter attitudes has not been collected.',[23,24,25],limit),
       ('Naidu remained the central TDP leader during opposition and legal conflict. The process of rebuilding organisation and negotiating the 2024 coalition needs fuller party and regional-language records.',[25,33],limit),
       ('The legal case was politically contested and denied by Naidu/TDP. Sources do not establish a caste-, class- or gender-specific causal explanation for public reactions.',[24,25],limit),
       ('The 2019 Assembly results concern successor Andhra Pradesh. Capital-policy conflict therefore arose within the new state framework rather than the undivided-state electorate.',[16,20,42],material),
       ('Court text is available for the 2024 split ruling, while later closure relies on two reports. Missing original orders and subsequent challenges limit conclusions about finality.',[23,24,25],material)
      ],
      [
       ('The TDP–Jana Sena–BJP alliance won 164 of 175 Assembly seats. TDP’s 16 Lok Sabha seats gave it influence in a coalition where BJP alone held 240 seats.',[8,33],material),
       ('State implementation, Union support, lender approvals and parliamentary legislation interact in capital development. Amaravati’s statutory designation in 2026 is legally distinct from completion of the city.',[19,21,40],material),
       ('The 2024 Kuppam margin was 48,006 in the ADR compilation. The denominator includes NOTA; shares cannot be compared mechanically with older candidate-only valid-vote denominators.',[15,9],material),
       ('Capital finance and AI infrastructure commitments coexist with pensions, school assistance and transport subsidies. Approval, investment commitment, expenditure and social outcome are separate stages.',[19,34,35,36,45,46],material),
       ('World Bank finance and Google’s AI-hub programme connect the state to international capital and infrastructure networks. Both institutions have interests in their own favourable project accounts.',[40,45,46],material),
       ('Corporate investment announcements and welfare-launch rhetoric shape the public development narrative. The Tirupati controversy also shows why public claims must be checked against later investigative evidence.',[29,30,31,34,45],material),
       ('The return to government combined a state electoral alliance and national coalition bargaining. These arrangements create multiple centres of contribution; benefits and decisions cannot all be attributed to one leader.',[8,33],material),
       ('Women’s mobility and education assistance, landless people’s livelihoods and religious public claims are distinct social-policy arenas. Evidence of design or rhetoric does not measure each group’s lived outcomes.',[19,20,29,34,35],material),
       ('The 2026 amendment names Amaravati within the notified APCRDA area, with deemed effect from 2 June 2024. Polavaram’s announced March 2027 target remains prospective at the cutoff.',[21,38],material),
       ('Recent evidence is rich in digital orders, press releases and launch reports but thin in independent long-run evaluations. The 28 October 2026 cutoff is a research snapshot, not continuous docket monitoring.',[21,24,34,35,40,46],material)
      ]
    ]
    peers=[
      'Congress and TDP aspirants, ministers and organisers in undivided Andhra Pradesh.',
      'Contemporary state chief ministers, Andhra Pradesh opposition leaders and elected local bodies.',
      'Congress government, TRS and Left leaders, and other legislative opposition leaders.',
      'Successor-state executives, Union coalition partners and capital-region local institutions.',
      'YSRCP government, TDP legislators and opposition leaders facing judicial proceedings.',
      'Jana Sena and BJP partners, YSRCP opposition, Union agencies and comparable state governments.'
    ]
    cautions=[
      'Do not project the later chief-ministerial reputation or 2014 boundaries onto entry and recruitment.',
      'Judge choices against contemporary reform, welfare and local-democracy debates; later IT growth is not all attributable to one tenure.',
      'Separate opposition advocacy from executive power, and avoid treating later state division as inevitable in every earlier decision.',
      'Adjust for the new state’s territory and institutions; legal designation, consent and delivered infrastructure are different tests.',
      'Retrospective closure does not erase the historical fact of arrest, and arrest does not establish guilt.',
      'Recent announcements have had limited time to produce measurable outcomes; present plans are not a completed legacy.'
    ]
    alternatives=[
      'Remaining in Congress, seeking office through TDP organisation, and contesting another constituency were distinct political routes; motives require evidence.',
      'Reform pace, welfare provision and the balance between stakeholder groups and elected local bodies were contestable policy choices.',
      'Legislative opposition, electoral coalitions and extra-parliamentary campaigning offered different channels of influence.',
      'Capital-development models, borrowing, welfare commitments and alliance bargaining involved different fiscal and distributional choices.',
      'Legislative challenge, litigation, mobilisation and coalition negotiation were available opposition methods; their relative effectiveness is unmeasured here.',
      'Allocation between infrastructure and welfare, project sequencing and negotiated Union support remain policy choices with trade-offs.'
    ]
    for pi, entries in enumerate(eras):
        for n,(finding,ids,disposition) in enumerate(entries,1):
            add('Context & Constraints',f'E{pi+1}{n:02d}',{
              'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],
              'Research disposition':disposition,'Finding':finding,
              'Contemporary comparison group':peers[pi],
              'Feasible alternatives / analytical frame':alternatives[pi],
              'Presentism caution':cautions[pi],
              'Evidence-environment limitation':'Only the registered finding is passage-reviewed; comparisons and alternatives are analytical frames, not measured counterfactuals.'
            },ids,'Analysis',phase=phases[pi],status='Supported' if disposition==material else 'Not reviewed')
