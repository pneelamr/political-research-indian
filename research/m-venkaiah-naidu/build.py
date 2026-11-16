#!/usr/bin/env python3
"""Rebuild author records and workbook; resets application/visual checks."""
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
output=REPO/'M_Venkaiah_Naidu_Political_Research.xlsx';reportpath=ROOT/'validation.json'
report=builder.build(data,retrievals,output,reportpath)
wb=load_workbook(output);ws=wb['Elections']
cols={c.value:c.column for c in ws[5]}
route=get_column_letter(cols['House / route']);result=get_column_letter(cols['Result'])
last=ws.max_row
direct=[r for r in data['tables']['Elections']['rows'] if r['House / route'].endswith(' / direct')]
assert len(direct)==6 and sum(r['Result']=='Won' for r in direct)==2
assert [r['Signed vote margin'] for r in direct]==[-89325,9660,20500,-830,-43620,-73273]
assert sum(r['Candidate votes'] is None for r in direct)==0
for row in range(6,last+1): ws.cell(row,cols['Turnout percent']).number_format='0.00'
ov=wb['Overview'];oc={c.value:c.column for c in ov[5]}
for rid,formula,expected in [
 ('OV20',f'=COUNTIF(Elections!{route}6:{route}{last},"* / direct")',6),
 ('OV21',f'=COUNTIFS(Elections!{route}6:{route}{last},"* / direct",Elections!{result}6:{result}{last},"Won")',2)]:
    row=next(r for r in range(6,ov.max_row+1) if ov.cell(r,1).value==rid)
    cell=ov.cell(row,oc['Finding / value']);cell.value=formula
    report['formula_checks'].append({'sheet':'Overview','cell':cell.coordinate,'formula':formula,'expected':expected,'record_id':rid,'column':'Finding / value'})
wb.save(output)
report['workbook_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
report['arithmetic_detail']={'confirmed_direct_contests':6,'direct_victories':2,'direct_defeats':4,'signed_margins':[-89325,9660,20500,-830,-43620,-73273],'vice_president_valid_ballots':516+244,'vice_president_invalid_ballots':771-760,'denominator_rule':'Valid votes for candidate shares; total polled/electorate for turnout; unresolved 1983 share omitted.'}
report['checks']['substantive_review']='PASS WITH EXPLICIT GAPS: election identity/units, office boundaries, policy attribution and procedural wording reviewed; unresolved matters remain in Research Queue.'
report['limitations']=['Research is a sourced snapshot, not an exhaustive biography.','Source S006 remains an indexed official lead; 1983 counts use inspected secondary S037 and share is omitted.','Allegations and attributed assessments are supported as reports, not established underlying truths.','Several context dimensions remain explicitly unreviewed.','Formula caches are not fabricated; applications recalculate on opening.','Application and visual checks must be rerun after every rebuild.']
reportpath.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'file':str(output),'checks':report['checks'],'evidence':report['evidence']},indent=2))
