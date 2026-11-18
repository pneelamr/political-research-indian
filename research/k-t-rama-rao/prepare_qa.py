#!/usr/bin/env python3
"""Prepare a disposable expanded copy and audit unchanged cell values."""
import json, sys
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
root=Path(__file__).resolve().parent
original=root.parent.parent/'K_T_Rama_Rao_Political_Research.xlsx'
destination=Path(sys.argv[1]);destination.mkdir(parents=True,exist_ok=True)
wb=load_workbook(original); widths={}
for ws in wb:
    x=0; cols=[]
    for col in range(1,ws.max_column+1):
        dim=ws.column_dimensions[get_column_letter(col)]
        dim.hidden=False;dim.outlineLevel=0;dim.collapsed=False
        # Approximate point offsets; actual PDF geometry is inspected separately.
        w=dim.width*5.25
        cols.append({'header':ws.cell(5,col).value,'x':round(x),'width':round(w)})
        x+=w
    widths[ws.title]=cols
    ws.print_area=f'A1:{get_column_letter(ws.max_column)}{ws.max_row}'
wb.save(destination/'expanded.xlsx')
(destination/'columns.json').write_text(json.dumps(widths,indent=2)+'\n')
check=load_workbook(destination/'expanded.xlsx');base=load_workbook(original)
assert [[c.value for row in ws for c in row] for ws in check]==[[c.value for row in ws for c in row] for ws in base]
print('Expanded QA copy has identical cell values/formulas; all supplementary columns visible.')
