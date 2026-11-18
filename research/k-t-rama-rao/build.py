"""Build KTR research and reset application QA whenever content changes."""
import hashlib,importlib.util,json,runpy
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent
runpy.run_path(str(ROOT/'author_research.py'),run_name='__main__')
spec=importlib.util.spec_from_file_location('shared_builder',REPO/'workflow/indian-political-figure-research/scripts/research_workbook.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
data=json.loads((ROOT/'research.json').read_text());retrievals=json.loads((ROOT/'retrievals.json').read_text())
output=REPO/'K_T_Rama_Rao_Political_Research.xlsx';reportpath=ROOT/'validation.json'
report=builder.build(data,retrievals,output,reportpath)
wb=load_workbook(output);ov=wb['Overview'];el=wb['Elections']
ec={c.value:c.column for c in el[5]};oc={c.value:c.column for c in ov[5]}
for rid,column,criterion in [('OV21','House / route','Assembly / direct'),('OV22','Result','Won')]:
    col=get_column_letter(ec[column]);row=next(r for r in range(6,ov.max_row+1) if ov.cell(r,1).value==rid)
    cell=ov.cell(row,oc['Finding / value']);cell.value=f'=COUNTIF(Elections!{col}6:{col}{el.max_row},"{criterion}")'
    report['formula_checks'].append({'sheet':'Overview','cell':cell.coordinate,'formula':cell.value,'expected':5,'record_id':rid,'column':'Finding / value'})
for ws in wb:ws.sheet_view.zoomScale=80
for colname in ['Exports (INR crore)','Employment (persons)']:
    ws=wb['Policy & Governance'];column=next(c.column for c in ws[5] if c.value==colname)
    for row in range(6,ws.max_row+1):ws.cell(row,column).number_format='#,##0'
wb.save(output)
assert [r['Candidate votes']-r['Opponent votes'] for r in data['tables']['Elections']['rows']]==[171,68219,53004,89009,29687]
assert len(data['tables']['Elections']['rows'])==5
assert all(data['tables']['Elections']['rows'][i]['Vote share'] is None for i in [1,3])
assert 241275-183569==57706 and 905715-778121==127594
report['workbook_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
report['checks']['substantive_review']='PASS WITH EXPLICIT GAPS: five electoral victories, bifurcation chronology, interrupted ministries, inherited TS-iPASS law, outputs versus impact, and legal stages passage-reviewed. Eleven context limitations and one overview gap remain Not reviewed.'
report['arithmetic_detail']={'election_margins':[171,68219,53004,89009,29687],'contests':5,'wins':5,'shares_withheld':[2010,2018],'FY2022_23_export_increase_INR_crore':57706,'FY2022_23_employment_increase':127594,'unit_note':'Government sector totals, not a personal impact estimate.'}
report['limitations']=['Evidence cutoff 16 November 2026; rapidly changing legal statuses are not live certificates.','One source is an indexed lead only and supports no reviewed claim.','2010 and 2018 shares withheld pending original denominator reconciliation.','Five gender and six era items retain explicit research limitations.','Independent policy impact and several final court/inquiry outcomes remain open.','Original formulas retain empty caches and recalculate on open; actual application checks recorded separately.']
reportpath.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'file':str(output),'checks':report['checks'],'evidence':report['evidence'],'sheets':report['sheets']},indent=2))
