#!/usr/bin/env python3
"""Rebuild normalized research and workbook; resets app/visual QA."""
import hashlib, importlib.util, json, runpy
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
runpy.run_path(str(ROOT/'author_research.py'),run_name='__main__')
spec=importlib.util.spec_from_file_location('shared_builder',REPO/'workflow/indian-political-figure-research/scripts/research_workbook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
data=json.loads((ROOT/'research.json').read_text());retrievals=json.loads((ROOT/'retrievals.json').read_text())
output=REPO/'Shashi_Tharoor_Political_Research.xlsx';reportpath=ROOT/'validation.json'
report=builder.build(data,retrievals,output,reportpath)
wb=load_workbook(output);ws=wb['Elections'];cols={c.value:c.column for c in ws[5]}
route=get_column_letter(cols['House / route']);result=get_column_letter(cols['Result']);last=ws.max_row
direct=[r for r in data['tables']['Elections']['rows'] if r['House / route'].endswith(' / direct')]
assert len(direct)==4 and all(r['Result']=='Won' for r in direct)
assert [r['Signed vote margin'] for r in direct]==[99998,15470,99989,16077]
assert [r['Share denominator'] for r in direct]==[737641,873441,1010180,962983]
assert 7897+1072+416==9385
for row in range(6,last+1):
    votes=ws.cell(row,cols['Candidate votes']).value
    denom=ws.cell(row,cols['Share denominator']).value
    if isinstance(votes,int) and isinstance(denom,int):
        cell=ws.cell(row,cols['Vote share']);cell.value=f'={get_column_letter(cols["Candidate votes"])}{row}/{get_column_letter(cols["Share denominator"])}{row}'
        cell.number_format='0.00%'
        report['formula_checks'].append({'sheet':'Elections','cell':cell.coordinate,'formula':cell.value,'expected':votes/denom,'record_id':ws.cell(row,1).value,'column':'Vote share'})
ov=wb['Overview'];oc={c.value:c.column for c in ov[5]}
for rid,formula in [('OV19',f'=COUNTIF(Elections!{route}6:{route}{last},"* / direct")'),('OV20',f'=COUNTIFS(Elections!{route}6:{route}{last},"* / direct",Elections!{result}6:{result}{last},"Won")')]:
    row=next(r for r in range(6,ov.max_row+1) if ov.cell(r,1).value==rid)
    cell=ov.cell(row,oc['Finding / value']);cell.value=formula
    report['formula_checks'].append({'sheet':'Overview','cell':cell.coordinate,'formula':formula,'expected':4,'record_id':rid,'column':'Finding / value'})
wb.save(output)
report['workbook_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
report['arithmetic_detail']={'direct_contests':4,'direct_victories':4,'signed_margins':[99998,15470,99989,16077],'party_election_margin':1072-7897,'candidate_shares':[r['Vote share'] for r in direct],'denominator_rule':'2009 valid candidate votes; 2014/2024 counted votes including NOTA; 2019 ADR denominator; Congress valid delegate ballots.'}
report['checks']['substantive_review']='PASS WITH EXPLICIT GAPS: chronology, election arithmetic, proposal/outcome distinction and judicial procedure reviewed. Claim status records unresolved dates and unreviewed context dimensions.'
report['limitations']=['Research is a sourced snapshot, not an exhaustive biography or current court-docket certificate.','S004 remains an indexed lead, excluded from supporting evidence.','2019 counts use inspected ADR compilation; original consolidated return remains a gap.','Current litigation outcomes and some exact tenure boundaries are unresolved.','Activity and recommendations do not establish causal policy outcomes.','Formula caches are not fabricated; application and visual QA must be rerun after each rebuild.']
reportpath.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'file':str(output),'checks':report['checks'],'evidence':report['evidence']},indent=2))
