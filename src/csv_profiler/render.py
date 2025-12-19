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
        
        
# #task6
# def write_markdown(report: dict, path: str | Path) -> None:
#     p = Path(path)

#     #create parent folde if it does not exist and if exixst nothing happen
#     p.parent.mkdir(parents=True, exist_ok=True)

#     rows_count = report.get("rows", 0)
#     columns_dict = report.get("columns", {})
#     col_names = list(columns_dict.keys())

#     with open(p, "w", encoding="utf-8") as f:
#         #my titl
#         f.write("# CSV Profile Report\n\n")
#         f.write(f"- Rows: {rows_count}\n")
#         f.write(f"- Columns: {len(col_names)}\n\n")
#         f.write("## Missing Values by Column\n\n")
#         f.write("| Column | Missing |\n")#to do the table
#         f.write("|--------|---------|\n")

#         for col in col_names:
#             missing = columns_dict[col].get("missing", 0)
#             f.write(f"| {col}  |     {missing}      |\n")


def md_header(report: dict) -> str:
    return "# CSV Profile Report\n\n"

def write_markdown(report: dict, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = report["summary"]["rows"]
    cols = report["summary"]["columns"]
    columns_dict = report["columns"] 

    lines: list[str] = []
    lines.append(md_header(report))
    lines.append("## Summary\n")
    lines.append(f"- Rows: {rows}\n")
    lines.append(f"- Columns: {cols}\n\n")
    lines.append("## Columns Overview\n\n")
    lines.append("| Column | Type | Missing % | Unique |\n")
    lines.append("|--------|------|-----------:|-------:|\n")

    for col_name, col_report in columns_dict.items():
        missing = col_report["missing"]
        unique = col_report["unique"]
        col_type = col_report["type"]

        missing_pct = (missing / rows) if rows else 0.0
        lines.append(f"| {col_name} | {col_type} | {missing_pct:.1%} | {unique} |\n")

    lines.append("\n")

    #detail of column
    lines.append("## Column Details\n\n")
    for col_name, col_report in columns_dict.items():
        col_type = col_report["type"]
        lines.append(f"### {col_name}\n\n")
        lines.append(f"- Type: **{col_type}**\n")
        lines.append(f"- Missing: {col_report['missing']}\n")
        lines.append(f"- Unique: {col_report['unique']}\n")

        if col_type == "number":
            lines.append(f"- Min: {col_report.get('min')}\n")
            lines.append(f"- Max: {col_report.get('max')}\n")
            lines.append(f"- Mean: {col_report.get('mean')}\n")
        else:
            lines.append("\nTop values:\n\n")
            top = col_report.get("top", [])
            if not top:
                lines.append("- (none)\n")
            else:
                for item in top:
                    lines.append(f"- {item['value']}: {item['count']}\n")

        lines.append("\n")


    p.write_text("".join(lines), encoding="utf-8")
