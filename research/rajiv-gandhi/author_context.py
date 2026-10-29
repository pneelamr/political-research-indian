"""Complete gender and phase-specific era coverage; gaps are not negative findings."""
coverage={
 'Gender':['Entry and advancement','Milestones','Networks and pathways','Role and portfolio allocation','Campaign and media treatment','Threats and security','Gender-related policy and organizations','Political use of identity','Representation and effects','Assessment over time'],
 'Era':['Party system','Constitutional and institutional environment','Electoral environment','Economic regime','International system','Media and campaign environment','Political organization','Social environment','State structure and political geography','Evidence environment']
}

def populate_context(add,phases):
    material='Material finding'; limit='Research limitation'; missing='Evidence not found'
    gender=[
      ('Family succession and Congress organisation supplied access to politics. The extent to which being a son rather than a daughter affected selection has not been demonstrated by a matched comparison.',[1,3],limit),
      ('The official profile identifies a youngest-prime-minister milestone, which concerns age. No gender-specific first or barrier-crossing is established in this source sample.',[1],missing),
      ('His mother’s and grandfather’s leadership and his brother’s death are relevant to the succession pathway. Family connection is examined as a mechanism for a male politician, without treating every later decision as dynastically determined.',[1,3],material),
      ('Premiership and additional Defence, Finance and External Affairs responsibilities are documented. No evidence comparing gendered portfolio allocation or promotion among contemporary Congress leaders was collected.',[2],limit),
      ('The official biography presents youth, aviation and technological interests favourably. That framing alone does not establish gender bias; comparative press, image and audience evidence remains missing.',[1],limit),
      ('Assassination by an LTTE suicide conspiracy is documented. The bomber’s sex does not establish a gender-based motive against Rajiv; security procedures and inquiry findings require further research.',[35,36],material),
      ('NPE equality commitments and Mahila Samakhya’s women’s collectives are documented, alongside the disputed Muslim Women Act. Institutional design, later legal interpretation and political criticism remain distinct.',[12,14,27,28],material),
      ('Family succession and a youthful administrative image are visible, but no inspected speech corpus establishes how Rajiv explicitly deployed masculinity or paternal identity to mobilise support.',[1],limit),
      ('Women’s educational agency was an explicit programme concern. The failed 1989 local-government proposal must be distinguished from reservations enacted under Rao in 1992; exact 1989 quota provisions remain unreviewed.',[14,31],material),
      ('Education scholarship and Hasan’s criticism of religious bargaining offer different perspectives. A longitudinal assessment of women’s own experiences, party influence and gender outcomes is still needed.',[14,28],limit)
    ]
    for n,(finding,ids,disposition) in enumerate(gender,1):
        add('Context & Constraints',f'G{n:02d}',{'Coverage dimension':'Gender','Coverage item':coverage['Gender'][n-1],'Research disposition':disposition,'Finding':finding,'Contemporary comparison group':'Congress and opposition leaders, including women, during the same 1980s–1991 institutions and electoral periods.','Presentism caution':'Equal scrutiny of male and female politicians; sex, kinship and women-targeted policy do not by themselves prove a gender mechanism.','Evidence-environment limitation':'No matched comparison dataset; missing evidence is not evidence of absence.'},ids,'Analysis',phase='Across four phases',status='Supported' if disposition==material else 'Not reviewed')

    eras=[
      [
       ('Entry came through Congress after Sanjay’s death, within a party led by his mother. Organisational office preceded national executive office.',[1],material),
       ('A by-election supplied the parliamentary mandate; party appointment supplied a different route to influence. His later succession as PM should not be projected backward onto his initial MP role.',[1,3],material),
       ('Amethi’s 1981 by-election was his first recorded personal contest. The Supreme Court record gives the winner’s total, but a complete primary return remains missing.',[3],material),
       ('Rodrik and Subramanian locate a pro-business shift under Indira before Rajiv became PM. Their interpretation warns against dating the entire growth transition to his accession.',[38],material),
       ('No inspected diplomatic record establishes how the Cold War directly affected his recruitment or advancement before October 1984. British study alone is not an international-policy mechanism.',[1],missing),
       ('Official biography highlights aviation and Asian Games organisation; comparative contemporary television and press evidence on his rise remains uncollected.',[1],limit),
       ('General-secretary work and Asian Games organisation accompanied family-based access. The sources establish overlapping pathways without estimating their relative weight.',[1],material),
       ('Family and occupational background are documented. Caste-based electoral mechanisms, household labour and social access were not established from independent evidence; surname is not used as a proxy.',[1,3],limit),
       ('Amethi was a parliamentary constituency in Uttar Pradesh; birthplace Bombay and national family networks were different geographical dimensions of the career.',[1,3],material),
       ('Retrospective official biography and judicial election facts are stronger than the available contemporary personal papers. Exact academic credentials, party dates and nomination deliberations remain gaps.',[1,2,3],limit)
      ],
      [
       ('The December 1984 ECI report gives Congress 404 seats out of 514 covered. This large parliamentary majority followed the October succession and violence.',[4,23],material),
       ('Appointment as PM was followed by a post-election ministry. The 52nd Amendment extended constitutional disqualification for defection across Parliament and state legislatures.',[39,9],material),
       ('Rajiv’s Amethi victory and the national Congress tally measure different mandates. Deferred regional polling limits comparisons using the report’s 514-seat denominator.',[4],material),
       ('Partial liberalisation and a more favourable business climate developed within an economy still characterised by extensive controls; scholars differ over the mechanism of acceleration.',[37,38],material),
       ('A dedicated contemporary account of US–Soviet relations during the early premiership has not been inspected. Later China and UN diplomacy cannot substitute for phase-specific evidence.',[20,19],limit),
       ('HRW criticises Rajiv’s public metaphor after the anti-Sikh attacks; official biography offers a favourable youth-and-modernisation narrative. Neither supplies a systematic audience study.',[24,1],material),
       ('Executive and party leadership overlapped, while negotiations with regional organisations opened channels beyond the Congress apparatus.',[1,15],material),
       ('Anti-Sikh violence, regional autonomy demands and debates over women’s rights formed distinct political pressures. The experience of victims and minorities cannot be reduced to national seat totals.',[23,24,15,27],material),
       ('Punjab, Assam and Mizoram settlements addressed different territorial, identity and constitutional arrangements within the Union; their implementation trajectories differed.',[15,16],material),
       ('Statutes and institutional milestones establish formal decisions. Commemorative sources, a later commission and retrospective scholarship answer different questions and require labelled limits.',[9,13,16,23,38],material)
      ],
      [
       ('Congress’s national tally fell to 197 seats in 1989, ending Rajiv’s premiership although he retained Amethi.',[5,1],material),
       ('Voting-age reform was enacted, the local-government constitutional proposal failed, and the Defamation Bill was withdrawn. Parliamentary outcomes differed despite the earlier large majority.',[10,31,30],material),
       ('In 1989 Rajiv won Amethi with 271,407 votes against Raj Mohan Gandhi’s 69,269. Constituency strength coexisted with national defeat.',[5],material),
       ('Panagariya links faster late-1980s growth to reform and unsustainable fiscal expansion; Rodrik/Subramanian offer a different account centred on earlier business attitudes.',[37,38],material),
       ('The late Cold War context appears explicitly in the UN disarmament proposal; China talks and interventions in Sri Lanka and Maldives show distinct diplomatic and security choices.',[20,19,17,22],material),
       ('Press resistance helped force withdrawal of the Defamation Bill. Bofors reporting and religious campaigning became important arenas of contested authority, without a measured estimate of vote effects.',[30,26,28],material),
       ('Negotiating with regional leaders, trying local-government reform and managing a majority government were overlapping political methods. Failure of a bill does not prove every organisational reform failed.',[15,31],material),
       ('Religious mobilisation around Ayodhya, the aftermath of Shah Bano and electoral disillusionment in Kashmir involved different communities and mechanisms; one uniform social-base description would obscure them.',[28,27,33],material),
       ('Kashmir alliance politics and the local-government proposal raise questions about power between Union, states and local institutions. Later changes to Jammu and Kashmir’s status are not projected onto 1987.',[33,31],material),
       ('Court and commission findings largely postdate the events. Contemporary allegations are distinguished from later rulings, and 2026 reporting is identified as a procedural update.',[25,26,23],material)
      ],
      [
       ('After the 1989 defeat, Congress retained sufficient parliamentary weight to support and later bring down Chandra Shekhar’s minority government.',[5,34],material),
       ('Recognised opposition leadership ended in December 1990; informal party leverage continued. The ninth Lok Sabha dissolved in March 1991, before his assassination.',[2,39,34],material),
       ('The 1991 Amethi result was posthumous. Congress’s eventual 232 seats and the Rao government cannot be described as a second Rajiv premiership.',[6,2,39],material),
       ('Economic scholarship places the 1991 crisis and systemic reforms in a longer sequence. Rajiv died before the Rao government; the later reform programme is not assigned to him.',[37,38,39],material),
       ('The Pakistan nuclear-facility agreement entered into force in January 1991 after Rajiv left office. A broader account of his opposition diplomacy and the changing world order remains incomplete.',[21],material),
       ('The surveillance dispute and election campaigning are documented in retrospective reporting. A systematic comparison of contemporary campaign media and changing opposition rhetoric is absent.',[34,36],limit),
       ('Party leadership enabled bargaining outside ministerial office. The available account records support and withdrawal but does not establish a single private motive.',[34],material),
       ('The assassination exposed acute political violence during campaigning. Victims’ experiences, public responses and community-level political effects need sources beyond criminal and electoral records.',[35,36],limit),
       ('The electoral base remained Amethi while assassination occurred during campaigning in Tamil Nadu. The LTTE connection links national electoral politics to the Sri Lankan conflict.',[6,35,36],material),
       ('Posthumous biography, court opinions and later sentence-release reporting require careful separation. No later political office, policy or family member’s action is attributed to Rajiv after May 1991.',[2,35,36],material)
      ]
    ]
    for p,rows in enumerate(eras,1):
        for n,(finding,ids,disposition) in enumerate(rows,1):
            add('Context & Constraints',f'E{p}{n:02d}',{'Coverage dimension':'Era','Coverage item':coverage['Era'][n-1],'Research disposition':disposition,'Finding':finding,'Contemporary comparison group':'Institutions, competing parties and regional actors active in this phase.','Presentism caution':'Interpret choices using contemporary institutions and feasible alternatives; later outcomes do not establish foresight or sole causation.','Evidence-environment limitation':'Source-specific standpoint and date retained; uncollected evidence is explicitly marked.'},ids,'Analysis',phase=phases[p-1],status='Supported' if disposition==material else 'Not reviewed')
