#task 5
from __future__ import annotations

import json
from pathlib import Path

def write_json(report: dict, path: str | Path) -> None:#takes input (what to write) and where to write it path
    p = Path(path)

    #reate parent folder if it does not exist and if exixst nothing happen
    p.parent.mkdir(parents=True, exist_ok=True)

    #writ my json
    with open(p, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
        
#task6
def write_markdown(report: dict, path: str | Path) -> None:
    p = Path(path)

    #create parent folde if it does not exist and if exixst nothing happen
    p.parent.mkdir(parents=True, exist_ok=True)

    rows_count = report.get("rows", 0)
    columns_dict = report.get("columns", {})
    col_names = list(columns_dict.keys())

    with open(p, "w", encoding="utf-8") as f:
        #my titl
        f.write("# CSV Profile Report\n\n")
        f.write(f"- Rows: {rows_count}\n")
        f.write(f"- Columns: {len(col_names)}\n\n")
        f.write("## Missing Values by Column\n\n")
        f.write("| Column | Missing |\n")#to do the table
        f.write("|--------|---------|\n")

        for col in col_names:
            missing = columns_dict[col].get("missing", 0)
            f.write(f"| {col}  |     {missing}      |\n")
