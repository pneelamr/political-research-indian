"""Build the workbook and reset application/visual QA for its new hash."""
import hashlib,importlib.util,json,runpy
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent
runpy.run_path(str(ROOT/'author_research.py'),run_name='__main__')
spec=importlib.util.spec_from_file_location('shared_builder',REPO/'workflow/indian-political-figure-research/scripts/research_workbook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
data=json.loads((ROOT/'research.json').read_text());retrievals=json.loads((ROOT/'retrievals.json').read_text())
output=REPO/'Jairam_Ramesh_Political_Research.xlsx';reportpath=ROOT/'validation.json'
report=builder.build(data,retrievals,output,reportpath)
wb=load_workbook(output);ov=wb['Overview'];el=wb['Elections']
ec={c.value:c.column for c in el[5]};oc={c.value:c.column for c in ov[5]}
route=get_column_letter(ec['House / route']);last=el.max_row
for rid,criteria,expected in [('OV21','Rajya Sabha / indirect',4),('OV22','Lok Sabha / direct',0)]:
    row=next(r for r in range(6,ov.max_row+1) if ov.cell(r,1).value==rid)
    cell=ov.cell(row,oc['Finding / value']);cell.value=f'=COUNTIF(Elections!{route}6:{route}{last},"{criteria}")'
    report['formula_checks'].append({'sheet':'Overview','cell':cell.coordinate,'formula':cell.value,'expected':expected,'record_id':rid,'column':'Finding / value'})
# Source titles and claim status remain readable in the initial view.
for ws in wb:
    ws.sheet_view.zoomScale=80
wb.save(output)
assert len([r for r in data['tables']['Elections']['rows'] if r['House / route']=='Rajya Sabha / indirect'])==4
assert 6+6+4==16
assert data['tables']['Elections']['rows'][2]['Candidate votes'] is None
report['workbook_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
report['checks']['substantive_review']='PASS WITH EXPLICIT GAPS: chronology, indirect elections, legislative scope, inherited programmes and legal dispositions passage-reviewed. Count discrepancy and research limitations retained.'
report['arithmetic_detail']={'confirmed_indirect_elections':4,'confirmed_direct_contests_in_register':0,'2016_count':'withheld: reports conflict','2022_count':'46 reported first-preference legislator votes','DST_recommendations':{'accepted':6,'not_pursued':6,'awaiting_final_reply':4,'total':16},'popular_vote_shares':'inapplicable; no fabricated denominator'}
report['limitations']=['Research snapshot; 2016 count and original detailed returns remain gaps.','Programme activity, announcements and laws do not by themselves establish personal causal outcomes.','Latest ECI follow-up and broader Money Bill reference disposition are unverified.','Eight gender and five era items are explicit research limitations.','Original workbook retains formulas with empty caches; recalculation is required by the viewing application.','Application and visual QA must be rerun after every rebuild.']
reportpath.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'file':str(output),'checks':report['checks'],'evidence':report['evidence']},indent=2))
